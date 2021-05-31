import streamlit as st

import pandas as pd

import sys
import os

path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(path)

import src.utils.mining_data_tb as md

# For paths
dir = os.path.dirname
path_up = dir(__file__)

for i in range(2): path_up = dir(path_up)

path_down = path_up + os.sep + "data"

def get_nutrition_data():
    path = path_down + os.sep + "Nutritional_values.csv"
    #df_path = "0_Project_EDA/data/Nutritional_values.csv"
    df = pd.read_csv(path)
    df2 = md.nutrition_prep(df)
    return df2

df = get_nutrition_data()
#for i in sys.path: print(i)
print(df.head())
