import requests
from bs4 import BeautifulSoup as bs
import html
import lxml

import numpy as np
import pandas as pd

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
def var_data(up_levels, filepath):

    path = dirname(__file__)
    for i in range(up_levels): path = dirname(path)

    fullpath = path + sep + filepath
    data = pd.read_csv(fullpath, index_col = 0)

    return data

#########
def var_descr_detector(var_name, vars_df):
    try:
        descr = vars_df[vars_df["vAr_nAmE"] == var_name]["var_descr"].values[0]
        return descr
    except:
        return var_name