import streamlit as st

import copy
import numpy as np
import pandas as pd
import joblib

from sqlalchemy import create_engine

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC

from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

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
import utils.dashboard_tb as da
import utils.mining_data_tb as md
import utils.visualization_tb as vi
import utils.folder_tb as fo
import utils.models as mo
import utils.sql_tb as sq


##################################################### INTERFACE #####################################################
menu = st.sidebar.selectbox("Menu:",
                            options = ["Home", "EDA", "Model testing", "Saved ML Models", "Predictor", "API", "Methodology"])

#########
if menu == "Home":
    da.home()

#########
if menu == "EDA":
    da.eda()

#########
if menu == "Model testing":
    da.model_testing()
    
#########
if menu == "Saved ML Models":
    da.saved_ml_models()
 
#########
if menu == "Predictor":
    da.predictor()

#########
if menu == "API":
    da.api()

#########
if menu == "Methodology":
    #da.methodology()
    pass
    