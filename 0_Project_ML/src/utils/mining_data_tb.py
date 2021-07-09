import requests
from bs4 import BeautifulSoup as bs
import html
import lxml
import json

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
        self.raw_df = None
        self.df = None

        # Processed data for ML
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.kfold = None



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
        #end_dfs = []
        #end_dfs = {}
        
        for data_dfs in self.__dfs_list:
            files = self.__concatenate_dfs(data_dfs)
            self.__joined_dfs = {**self.__joined_dfs, **files}
            #end_dfs.append(files)

        #return self.__joined_dfs

    #########
    def __merge_dfs(self):
        keys = list(self.__joined_dfs.keys())
        self.df = self.__joined_dfs.pop(keys[0])

        for name, df in self.__joined_dfs.items():
            self.df = pd.merge(self.df, df, how = "outer", on = "SEQN")
            self.raw_df = pd.merge(self.df, df, how = "outer", on = "SEQN")

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

    #########
    def load_data(self, up_levels, folders, clean = False):
        self.__read_all_data(up_levels, folders)
        self.__concatenate_all_dfs()
        self.__merge_dfs()
        self.__clean_rows()

    #########
    def clean_columns(self, correction_map):
        to_drop = [key[:-2] + "_y" for key in correction_map.keys()]
        self.df = self.df.drop(to_drop, axis = 1)
        
        self.df = self.df.rename(columns = correction_map)
    
    #########
    def heart_disease(self):
        # Conditions to remove values of no interest from the columns of interest
        cond_b = self.df.MCQ160B != 9
        cond_c = self.df.MCQ160C != 7
        cond_d = (self.df.MCQ160D != 9) & (self.df.MCQ160D != 7)
        cond_e = self.df.MCQ160E != 9
        cond_f = self.df.MCQ160F != 9

        # Filter the data with the previous conditions
        self.df = self.df[(cond_b) & (cond_c) & (cond_d) & (cond_e) & (cond_f)]

        # New column to group all heart diseases
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
    def filter_columns(self, features, inplace = False):
        if inplace:
            self.df = self.df.loc[:, features]
        else:
            return self.df.loc[:, features]

    #########
    def model_data(self, split, cv, epochs = 1, scaler = False, balance = None, seed = 42): 
        ### Independent variables
        X = np.array(self.df.iloc[:, 1:])

        ### Dependent variable
        y = np.array(self.df.iloc[:, 0])

        ### Data scaling
        if scaler:
            scaler = StandardScaler()
            X = scaler.fit_transform(X)

        ### Train-test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size = split, random_state = seed)

        ### Balancing data
        if balance != None:
            sm = SMOTE(sampling_strategy = balance, random_state = seed, n_jobs = -1)
            self.X_train, self.y_train = sm.fit_resample(self.X_train, self.y_train)

        ### Cross validation
        self.kfold = RepeatedStratifiedKFold(n_splits = cv, n_repeats = epochs, random_state = seed)

################# DATA PREP FOR ML #################
class ml_model:
    #########
    def __init__(self, model):
        # Data
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.features = None
        self.kfold = None

        # Training
        self.model = model
        self.train_scores = []
        self.val_scores = []
        self.train_set_structures = []
        self.val_set_structures = []
        self.feature_importances = None

        # Test
        self.train_score = None
        self.test_score = None
        self.train_structure = None
        self.test_structure = None
        self.prediction = None
        self.cm = None        

        # Metrics
        self.accuracy = None
        self.precision = None
        self.recall = None
        self.f1_score = None
        self.precisions = None
        self.recalls = None
        self.thresholds = None

    #########
    def load_data(self, X_train, X_test, y_train, y_test, features, kfold):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.features = features
        self.kfold = kfold

    #########
    def ml_trainer(self, verb = False):
        count = 1

        for (train, val) in self.kfold.split(self.X_train, self.y_train):
            # Train-Validation sets
            x_t, y_t = self.X_train[train], self.y_train[train]
            x_v, y_v = self.X_train[val], self.y_train[val]

            # Internal structure
            y_t_unique, y_t_counts = np.unique(y_t, return_counts=True)
            y_v_unique, y_v_counts = np.unique(y_v, return_counts=True)

            self.train_set_structures.append(dict(zip(y_t_unique, y_t_counts / len(y_t))))
            self.val_set_structures.append(dict(zip(y_v_unique, y_v_counts / len(y_v))))

            # Training
            self.model.fit(x_t, y_t)

            # Scores
            train_score = self.model.score(x_t, y_t)
            val_score = self.model.score(x_v, y_v)

            self.train_scores.append(train_score)
            self.val_scores.append(val_score)

            if verb:
                print(f"\n-- Model {count} --")
                print("-" * 25)
                print(">train score:", train_score)
                print(">test score:", val_score)
                print("-" * 25)
                print("Set structure:")
                print("Train structure:", dict(zip(y_t_unique, y_t_counts / len(y_t))))
                print("Validation structure:", dict(zip(y_v_unique, y_v_counts / len(y_v))))
                print("#" * 75)

            count += 1

        try:
            importances = self.model.feature_importances_
            feature_importances = list(zip(self.features, importances))

            self.feature_importances = pd.DataFrame(feature_importances, columns = ["features", "importance"]).sort_values(by = "importance", ascending = False)
            #return train_scores, val_scores, feature_importances_df
        
        except:
            pass
            #return train_scores, val_scores

    #########
    def ml_tester(self, verb = False):
        # Internal structure
        y_train_unique, y_train_counts = np.unique(self.y_train, return_counts=True)
        y_test_unique, y_test_counts = np.unique(self.y_test, return_counts=True)

        self.train_structure =dict(zip(y_train_unique, y_train_counts / len(self.y_train) * 100))
        self.test_structure = dict(zip(y_test_unique, y_test_counts / len(self.y_test) * 100))

        # Scores
        self.train_score = self.model.score(self.X_train, self.y_train)
        self.test_score = self.model.score(self.X_test, self.y_test)

        # Prediction
        self.prediction = self.model.predict(self.X_test)

        # Confusion matrix
        self.cm = metrics.confusion_matrix(self.y_test, self.prediction)

        ##### Precision metrics
        self.accuracy = (self.cm[0][0] + self.cm[1][1]) / self.cm.sum()
        self.precision = self.cm[1][1] / (self.cm[1][1] + self.cm[0][1])
        self.recall = self.cm[1][1] / (self.cm[1][1] + self.cm[1][0])
        self.f1_score = 2 * ((self.precision * self.recall) / (self.precision + self.recall))

        ##### Roc curve
        self.precisions, self.recalls, self.thresholds = metrics.precision_recall_curve(self.y_test, self.prediction, pos_label = 1)

        if verb:
            print("Train structure:", self.train_structure)
            print("Test structure:", self.test_structure)
            print("#" * 75)
            print(">Train score:", self.train_score)
            print(">Test score:", self.test_score)
            print("#" * 75)
            print("Confusion matrix")
            print(self.cm)
            print("#" * 75)
            print("Precision metrics")
            print("Accuracy:", self.accuracy)
            print("Precision:", self.precision)
            print("Recall:", self.recall)
            print("F1 score:", self.f1_score)

    #########
    def ml_predictions(self, to_predict):
        new_predictions = self.model.predict(to_predict)
        return new_predictions


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