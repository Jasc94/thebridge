import streamlit as st

import pandas as pd

import requests
import webbrowser

import sys
import os

# Helpers
abspath = os.path.abspath
dirname = os.path.dirname
sep = os.sep

# Path modification
current_folder = dirname(abspath(__file__))
for i in range(1): current_folder = dirname(abspath(current_folder))
sys.path.append(current_folder)

# Self-made packages
import utils.mining_data_tb as md
import utils.visualization_tb as vi
import utils.folder_tb as fo

raw_dataset_path = fo.path_to_folder(2, "data" + sep + "7_cleaned_data") + "raw_data.csv"
raw_dataset = pd.read_csv(raw_dataset_path)

print(raw_dataset.loc[:, ["MCQ010", "LBDHDD"]].dropna())