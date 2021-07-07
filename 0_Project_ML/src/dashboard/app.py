import streamlit as st

import numpy as np
import pandas as pd

#import plotly.plotly as py
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
import utils.mining_data_tb as md
import utils.visualization_tb as vi
import utils.folder_tb as fo


##################################################### PULLING THE DATA #####################################################
#########
@st.cache
def get_data():
    #### Variables data
    vardata_downpath = "data" + sep + "6_variables" + sep + "0_final_variables.csv"
    vardata = md.variables_data()
    vardata.load_data(2, vardata_downpath)

    #### Unprocessed Dataset
    raw_dataset_path = fo.path_to_folder(2, "data" + sep + "7_cleaned_data") + "raw_data.csv"
    raw_dataset = pd.read_csv(raw_dataset_path)

    return vardata, raw_dataset

###
vardata, raw_dataset = get_data()
vars_nom = list(raw_dataset.columns)
vars_descr = vardata.vars_descr_detector(vars_nom)
vars_nom_descr = vardata.vars_descr_detector(vars_nom, nom_included = True)

variables_df = vardata.df.iloc[:, [0, 1, -2]]

##################################################### INTERFACE #####################################################
menu = st.sidebar.selectbox("Menu:",
                            options = ["Home", "EDA", "Predictor", "Saved ML Models", "API", "Methodology"])

#########
if menu == "Home":
    #da.home()
    pic_path = fo.path_to_folder(2, "resources") + "home_image.jpeg"

    st.title("Health")
    st.header("Are you at risk?")
    st.image(pic_path)

#########
if menu == "EDA":
    #da.eda()

    # Filters
    st.sidebar.write("Filter by:")

    filter1 = st.sidebar.checkbox("Demographics")
    filter2 = st.sidebar.checkbox("Dietary")
    filter3 = st.sidebar.checkbox("Examination")
    filter4 = st.sidebar.checkbox("Laboratory")
    filter5 = st.sidebar.checkbox("Questionnaire")

    sort_by = st.sidebar.radio("Sort by:", options = ["Variable nomenclature", "Variable description", "Component"])
    translation = {
        "Variable nomenclature" : "vAr_nAmE",
        "Variable description" : "var_descr",
        "Component" : "component"
    }

    to_show = variables_df.sort_values(by = translation[sort_by])

    if filter1: to_show = to_show[to_show.component == "Demographics"]
    if filter2: to_show = to_show[to_show.component == "Dietary"]
    if filter3: to_show = to_show[to_show.component == "Examination"]
    if filter4: to_show = to_show[to_show.component == "Laboratory"]
    if filter5: to_show = to_show[to_show.component == "Questionnaire"]

    table_header = list(to_show.columns)
    table_data = [to_show.iloc[:, 0].values,
                to_show.iloc[:, 1].values,
                to_show.iloc[:, 2].values,
                ]

    fig = go.Figure(data = go.Table(
                    columnwidth = [40, 100, 40],
                    header = dict(values = table_header,
                    fill_color = "#3D5475",
                    align = "left"),
                    cells = dict(values = table_data,
                    fill_color = "#7FAEF5",
                    align = "left")
                    ))
    fig.update_layout(margin = dict(l = 0, r = 0, b = 0, t = 0))

    st.write(fig)

    ### Data
    #st.table(raw_dataset.df.head(10))

    #st.table(to_show)

    # Interface structure
    #expander = st.beta_expander("Filter the variables")

    # User filters
    # filters = []
    # for variable in vars_nom_descr[:20]:
    #     filter_ = expander.checkbox(label = variable)
    #     filters.append(filter_)
    


    


    ### Pot
    

#########
if menu == "Predictor":
    #da.predictor()
    pass

#########
if menu == "Saved ML Models":
    #da.saved_ml_models()
    pass

#########
if menu == "API":
    #da.api()
    data_checkbox = st.sidebar.checkbox(label = "Data")
    variables_checkbox = st.sidebar.checkbox(label = "Variables")

    password = st.sidebar.text_input("Password to access data")
    button = st.sidebar.button("Get data")

    if button:
        if data_checkbox:
            try:
                url = f"http://localhost:6060/data?password={password}"
                data = pd.read_json(url)
                st.table(data.head(20))
            except:
                st.header("It wasn't possible to gather the data")
                st.write("Please check the password or confirm that the server is running")

        if variables_checkbox:
            try:
                url = f"http://localhost:6060/variables-data?password={password}"
                data = pd.read_json(url)
                st.table(data.head(20))
            except:
                st.header("It wasn't possible to gather the data")
                st.write("Please check the password or confirm that the server is running")
    
#########
if menu == "Methodology":
    #da.methodology()
    pass
    