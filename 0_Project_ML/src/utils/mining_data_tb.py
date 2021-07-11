import requests
from bs4 import BeautifulSoup as bs
import html
import lxml
import json
import joblib

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

from imblearn.over_sampling import SMOTE

import sys, os

# Helpers
abspath = os.path.abspath
dirname = os.path.dirname
sep = os.sep


##################################################### DATA EXTRACTION #####################################################
# All the variables are encoded and for the actual names and descriptions, I need to pull the data from the website

######### 
def obtain_rows(url):
    r = requests.get(url)
    soup = bs(r.text, "lxml")
    table = soup.find(id = "GridView1")
    rows = table.find_all("tr")

    return rows

#########
def obtain_row_info(rows):
    var_names = []
    var_descrs = []
    file_names = []
    file_descrs = []
    start_years = []
    end_years = []
    components = []
    constraints = []

    for row in range(1, len(rows)):
        var_name, var_descr, file_name, file_descr, start_year, end_year, component, constraint = rows[row].find_all("td")

        var_names.append(var_name.text)
        var_descrs.append(var_descr.text)
        file_names.append(file_name.text)
        file_descrs.append(file_descr.text)
        start_years.append(start_year.text)
        end_years.append(end_year.text)
        components.append(component.text)
        constraints.append(constraint.text)

    return list(zip(var_names, var_descrs, file_names, file_descrs, start_years, end_years, components, constraints))

#########
def df_creator(field_list):
    df = pd.DataFrame(field_list, columns = ["var_name", "var_descr", "file_name", "file_descr", "start_year", "end_year", "component", "constraint"])

    return df

#########
def ready_to_use(url):
    return df_creator(obtain_row_info(obtain_rows(url)))


##################################################### DATA WRANGLING #####################################################
################# VARIABLE NAMES #################
class variables_data:
    def __init__(self):
        self.df = None

    #########
    def load_data(self, up_levels, filepath):

        path = dirname(abspath(__file__))
        for i in range(up_levels): path = dirname(path)

        fullpath = path + sep + filepath
        self.df = pd.read_csv(fullpath, index_col = 0)
        #return self.df

    #########
    def var_descr_detector(self, var_name, cut = None, nom_included = False):
        try:     
            if nom_included:
                descr = var_name + ": " + self.df[self.df["vAr_nAmE"] == var_name]["var_descr"].values[0][:cut]
            else:
                descr = self.df[self.df["vAr_nAmE"] == var_name]["var_descr"].values[0][:cut]
            return descr
        except:
            return var_name

    #########
    def vars_descr_detector(self, var_names, cut = None, nom_included = False):
        var_names = [self.var_descr_detector(nom, cut, nom_included) for nom in var_names] 

        return var_names

################# READING DATA FROM FILES #################
class dataset:
    def __init__(self):
        # Raw data
        self.__dfs_list = []
        self.__joined_dfs = {}
        self.__raw_df = None
        self.df = None

        # Processed data for ML
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.kfold = None

    ######### DATA PROCESSING #########
    #########
    def __read_data(self, up_levels, folder):
        path = dirname(abspath(__file__))
        for i in range(up_levels): path = dirname(path)

        data_path = path + sep + "data" + sep + folder

        data_dfs = {}
        for file_ in os.listdir(data_path):
            if file_ != "history":
                try:
                    # Path to file
                    filepath = data_path + sep + file_

                    # Reading as dataframe
                    df = pd.read_csv(filepath, index_col = 0)
                    df["SEQN"] = df["SEQN"].map(int)
                    df.set_index("SEQN", inplace = True)

                    # Saving it in a dictionary
                    dict_key = file_[:-4].lower()
                    data_dfs[dict_key] = df
                except:
                    pass

        return data_dfs

    #########
    def __read_all_data(self, up_levels, folders):
        for folder in folders:
            self.__dfs_list.append(self.__read_data(up_levels, folder))

    #########
    def __concatenate_dfs(self, data_dfs):
        files = {}
        count = 0

        for key, dfs in data_dfs.items():
            key_ = key[:-2]

            if count == 0:
                files[key_] = dfs
            else:
                if key_ not in files.keys():
                    files[key_] = dfs
                else:
                    files[key_] = pd.concat([files[key_], dfs])

            count +=1

        return files

    #########
    def __concatenate_all_dfs(self):
        for data_dfs in self.__dfs_list:
            files = self.__concatenate_dfs(data_dfs)
            self.__joined_dfs = {**self.__joined_dfs, **files}


    #########
    def __merge_dfs(self):
        keys = list(self.__joined_dfs.keys())
        self.df = self.__joined_dfs.pop(keys[0])

        for name, df in self.__joined_dfs.items():
            self.df = pd.merge(self.df, df, how = "outer", on = "SEQN")
            
    #########
    def __clean_rows(self):
        important_values = [7.0, 9.0]
        # Asthma
        self.df = self.df[~self.df.MCQ010.isin(important_values)]
        # Heart problems
        self.df = self.df[~self.df.MCQ160B.isin(important_values)]
        self.df = self.df[~self.df.MCQ160C.isin(important_values)]
        self.df = self.df[~self.df.MCQ160D.isin(important_values)]
        self.df = self.df[~self.df.MCQ160E.isin(important_values)]
        self.df = self.df[~self.df.MCQ160F.isin(important_values)]

    def __update_target_values(self):
        self.df.MCQ010 = self.df.MCQ010.replace(2, 0)
        self.df.MCQ160B = self.df.MCQ160B.replace(2, 0)
        self.df.MCQ160C = self.df.MCQ160C.replace(2, 0)
        self.df.MCQ160D = self.df.MCQ160D.replace(2, 0)
        self.df.MCQ160E = self.df.MCQ160E.replace(2, 0)
        self.df.MCQ160F = self.df.MCQ160F.replace(2, 0)

    #########
    def __clean_columns(self, correction_map):
        to_drop = [key[:-2] + "_y" for key in correction_map.keys()]
        self.df = self.df.drop(to_drop, axis = 1)
        self.df = self.df.rename(columns = correction_map)

    #########
    def __heart_disease(self):
        self.df["MCQ160H"] = 0

        # Conditions to filter by any heart disease
        pos_cond_b = self.df.MCQ160B == 1
        pos_cond_c = self.df.MCQ160C == 1
        pos_cond_d = self.df.MCQ160D == 1
        pos_cond_e = self.df.MCQ160E == 1
        pos_cond_f = self.df.MCQ160F == 1

        # Given the previous conditions, place a "1" in the column if they are matched
        self.df.loc[(pos_cond_b) | (pos_cond_c) | (pos_cond_d) | (pos_cond_e) | (pos_cond_f), "MCQ160H"] = 1

    #########
    def load_data(self, up_levels, folders, correction_map):
        self.__read_all_data(up_levels, folders)
        self.__concatenate_all_dfs()
        self.__merge_dfs()
        self.__clean_rows()
        self.__update_target_values()
        self.__clean_columns(correction_map)
        self.__heart_disease()
        # Dataset backup
        self.__raw_df = self.df
    
    ######### SUPPORT FUNCTIONS #########
    #########
    def filter_columns(self, features, inplace = False):
        if inplace:
            self.df = self.df.loc[:, features]
        else:
            return self.df.loc[:, features]

    #########
    def drop_columns(self, columns):
        self.df = self.df.drop(columns, axis = 1)

    #########
    def drop_nans(self):
        self.df = self.df.dropna()

    #########
    def dummies_transform(self, variable, mapper):
        # Mapping values
        self.df.loc[:, variable] = self.df.loc[:, variable].map(mapper)
        # Getting dummies
        self.df = pd.get_dummies(self.df, prefix = "", prefix_sep = "", columns = [variable])
        #return df

    #########
    def __pair_mean(self, pair_list, new_name, drop_old = False):
        self.df[new_name] = self.df.loc[:, pair_list].mean(axis = 1)
        
        if drop_old:
            self.df = self.df.drop(pair_list, axis = 1)

    #########
    def pairs_mean(self, combination_list, drop_old = False):
        for combination in combination_list:
            self.__pair_mean(combination[0], combination[1], drop_old = drop_old)

    #########
    def reset_dataset(self):
        self.df = self.__raw_df

    #########
    def model_data(self, split, cv, epochs = 1, scaler = False, balance = None, seed = 42): 
        # Independent variables
        X = np.array(self.df.iloc[:, 1:])

        # Dependent variable
        y = np.array(self.df.iloc[:, 0])

        # Data scaling
        if scaler:
            scaler = StandardScaler()
            X = scaler.fit_transform(X)

        # Train-test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size = split, random_state = seed)

        # Balancing data
        if balance != None:
            sm = SMOTE(sampling_strategy = balance, random_state = seed, n_jobs = -1)
            self.X_train, self.y_train = sm.fit_resample(self.X_train, self.y_train)

        # Cross validation
        self.kfold = RepeatedStratifiedKFold(n_splits = cv, n_repeats = epochs, random_state = seed)  

##################################################### OTHERS #####################################################
#########
def read_json(fullpath):
    '''
    This function reads the json an returns it in a format we can work with it

    args : fullpath -> path to the json to be read
    '''
    with open(fullpath, "r") as json_file:
        read_json_ = json.load(json_file)

    return read_json_

#########
def read_json_to_dict(json_fullpath):
    """
    Read a json and return a object created from it.
    Args:
        json_fullpath: json fullpath

    Returns: json object.
    """
    try:
        with open(json_fullpath, 'r+') as outfile:
            read_json = json.load(outfile)
        return read_json
    except Exception as error:
        raise ValueError(error)

#########
def round_number(x, dec):
    try:
        return round(x, dec)
    except:
        return x

#########
def to_float(x):
    try:
        return float(x)
    except:
        return x