import requests
from bs4 import BeautifulSoup as bs
import html
import lxml

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold
from sklearn.preprocessing import StandardScaler

from imblearn.over_sampling import SMOTE

import sys, os


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
    def var_data(self, up_levels, filepath):

        path = dirname(__file__)
        for i in range(up_levels): path = dirname(path)

        fullpath = path + sep + filepath
        self.df = pd.read_csv(fullpath, index_col = 0)
        #return self.df

    #########
    def var_descr_detector(self, var_name):
        try:
            descr = self.df[self.df["vAr_nAmE"] == var_name]["var_descr"].values[0]
            return descr
        except:
            return var_name

################# READING DATA FROM FILES #################
#########
def read_data(up_levels, folder):

    path = dirname(__file__)
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
def read_all_data(up_levels, folders):
    dfs_list = []

    for folder in folders:
        dfs_list.append(read_data(up_levels, folder))

    return dfs_list

#########
def concatenate_dfs(data_dfs):
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
def concatenate_all_dfs(data_dfs_list):
    #end_dfs = []
    end_dfs = {}
    
    for data_dfs in data_dfs_list:
        files = concatenate_dfs(data_dfs)
        end_dfs = {**end_dfs, **files}
        #end_dfs.append(files)

    return end_dfs

#########
def merge_dfs(end_dfs):
    keys = list(end_dfs.keys())
    f_df = end_dfs.pop(keys[0])

    for name, df in end_dfs.items():
        f_df = pd.merge(f_df, df, how = "outer", on = "SEQN")

    return f_df

################# DATA CLEANING AND TRANSFORMATION #################
#########
def clean_columns(df):
    df = df.drop(["WTDRD1_y", "WTDR2D_y", "DRABF_y", "DRDINT_y", "WTSAF2YR_y", "LBXHCT_y"], axis = 1)

    columns_correction = {
        "WTDRD1_x" : "WTDRD1",
        "WTDR2D_x" : "WTDR2D",
        "DRABF_x" : "DRABF",
        "DRDINT_x" : "DRDINT",
        "WTSAF2YR_x" : "WTSAF2YR",
        "LBXHCT_x" : "LBXHCT"
    }

    df = df.rename(columns = columns_correction)

    return df

#########
def heart_disease(df):
    # Conditions to remove values of no interest from the columns of interest
    cond_b = df.MCQ160B != 9
    cond_c = df.MCQ160C != 7
    cond_d = (df.MCQ160D != 9) & (df.MCQ160D != 7)
    cond_e = df.MCQ160E != 9
    cond_f = df.MCQ160F != 9

    # Filter the data with the previous conditions
    heart_df = df[(cond_b) & (cond_c) & (cond_d) & (cond_e) & (cond_f)]

    # New column to group all heart diseases
    heart_df["heart_disease"] = 0

    # Conditions to filter by any heart disease
    pos_cond_b = heart_df.MCQ160B == 1
    pos_cond_c = heart_df.MCQ160C == 1
    pos_cond_d = heart_df.MCQ160D == 1
    pos_cond_e = heart_df.MCQ160E == 1
    pos_cond_f = heart_df.MCQ160F == 1

    # Given the previous conditions, place a "1" in the column if they are matched
    heart_df.loc[(pos_cond_b) | (pos_cond_c) | (pos_cond_d) | (pos_cond_e) | (pos_cond_f), "heart_disease"] = 1

    return heart_df

################# DATA PREP FOR ML #################
#########
def model_data(df, var_names, split, cv, epochs = 1, scaler = False, balance = None, seed = 42):
    features_nom = list(df.columns)
    features = [var_descr_detector(nom, var_names) for nom in features_nom]  

    ### Independent variables
    X = np.array(df.iloc[:, 1:])

    ### Dependent variable
    y = np.array(df.iloc[:, 0])

    ### Data scaling
    if scaler:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

    ### Train-test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = split, random_state = seed)

    ### Balancing data
    if balance != None:
        sm = SMOTE(sampling_strategy = balance, random_state = seed, n_jobs = -1)
        X_train, y_train = sm.fit_resample(X_train, y_train)

    ### Cross validation
    kfold = RepeatedStratifiedKFold(n_splits = cv, n_repeats = epochs, random_state = seed)


    return X_train, X_test, y_train, y_test, features, kfold

#########
def ml_trainer(X_train, y_train, kfold, model, features = None):
    train_scores = []
    val_scores = []
    count = 1

    for (train, val) in kfold.split(X_train, y_train):
        # Train-Validation sets
        x_t, y_t = X_train[train], y_train[train]
        x_v, y_v = X_train[val], y_train[val]


        # Internal structure
        y_t_unique, y_t_counts = np.unique(y_t, return_counts=True)
        y_v_unique, y_v_counts = np.unique(y_v, return_counts=True)

        # Training
        model.fit(x_t, y_t)

        # Scores
        train_score = model.score(x_t, y_t)
        val_score = model.score(x_v, y_v)

        train_scores.append(train_score)
        val_scores.append(val_score)

        print(f"\n-- Model {count} --")
        print("-" * 25)
        print("Set structure:")
        print("Train structure:", dict(zip(y_t_unique, y_t_counts / len(y_t))))
        print("Validation structure:", dict(zip(y_v_unique, y_v_counts / len(y_v))))
        print("-" * 25)
        print(">train score:", train_score)
        print(">test score:", val_score)
        print("#" * 75)

        count += 1

    try:
        importances = model.feature_importances_
        feature_importances = list(zip(features, importances))

        feature_importances_df = pd.DataFrame(feature_importances, columns = ["features", "importance"]).sort_values(by = "importance", ascending = False)

        return train_scores, val_scores, feature_importances_df
    
    except:
        return train_scores, val_scores