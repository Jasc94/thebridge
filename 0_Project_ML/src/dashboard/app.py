import streamlit as st

import numpy as np
import pandas as pd

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
    # raw_dataset_path = fo.path_to_folder(2, "data" + sep + "7_cleaned_data") + "raw_data.csv"
    # raw_dataset = pd.read_csv(raw_dataset_path)

    dataset = md.dataset()
    folders = ["1_demographics", "2_dietary", "3_examination", "4_laboratory", "5_questionnaire"]
    dataset.load_data(2, folders)
    columns_correction = {
            "WTDRD1_x" : "WTDRD1",
            "WTDR2D_x" : "WTDR2D",
            "DRABF_x" : "DRABF",
            "DRDINT_x" : "DRDINT",
            "WTSAF2YR_x" : "WTSAF2YR",
            "LBXHCT_x" : "LBXHCT"
        }
    dataset.clean_columns(columns_correction)
    dataset.heart_disease()


    vardata.df = vardata.df[vardata.df.vAr_nAmE.isin(list(dataset.df.drop("heart_disease", axis = 1).columns))]

    return vardata, dataset

###
vardata, dataset = get_data()
vars_nom = list(dataset.df.columns)
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

    ### Filters
    # Table filters
    st.sidebar.subheader("Table tools")
    sort_by = st.sidebar.radio("Sort by:", options = ["Variable nomenclature", "Variable description"])
    translation = {
        "Variable nomenclature" : "vAr_nAmE",
        "Variable description" : "var_descr",
    }

    filter_by = st.sidebar.radio("Filter by:", options = ["Demographics", "Dietary", "Examination", "Laboratory", "Questionnaire"])
    
    to_show = variables_df.sort_values(by = translation[sort_by])
    to_show = to_show[to_show.component == filter_by]

    # Plot filters
    st.sidebar.subheader("Plotting tools")
    y = st.sidebar.text_input("Choose your target variable (y):")
    X = st.sidebar.text_area("Choose your explanatory variables (X):")
    X = X.split("\n")

    button = st.sidebar.button("Submit selection")
    
    ### Plots
    # Table
    table_header = ["Variable name", "Variable description"]
    table_data = [to_show.iloc[:, 0].values,
                to_show.iloc[:, 1].values
                ]

    table = go.Figure(data = go.Table(
                    columnwidth = [40, 100],
                    header = dict(values = table_header,
                    fill_color = "#3D5475",
                    align = "left",
                    font = dict(size = 20)),

                    cells = dict(values = table_data,
                    fill_color = "#7FAEF5",
                    align = "left",
                    font = dict(size = 16),
                    height = 30)
                    ))
    table.update_layout(margin = dict(l = 0, r = 0, b = 0, t = 0))

    st.write(table)

    # Plots
    if button:
        # Data preprocessing
        columns = [y] + X
        data = dataset.df.loc[:, columns].dropna()

        corr = np.array(data.corr())

        y_descr = vardata.var_descr_detector(y)
        X_descr = vardata.vars_descr_detector(X)
        descrs = [y] + X_descr

        # Title
        st.subheader(y_descr)

        # Correlation plot
        colorscale = [[0, "white"], [1, "cornflowerblue"]]
        correlation_plot = ff.create_annotated_heatmap(corr,
                                                       x = descrs,
                                                       y = descrs,
                                                       colorscale = colorscale)
        st.write(correlation_plot)

        for x in X:
            x_descr = vardata.var_descr_detector(x, cut = 30, nom_included = True)
            expander = st.beta_expander(x_descr)

            with expander:
                # Distribution plots
                to_plot = data.loc[:, [y, x]].dropna()
                histogram = px.histogram(to_plot, x = x, color = y,
                                        marginal = "box",
                                        labels = {x : x_descr},
                                        width = 600)
                st.write(histogram)

#########
if menu == "Predictor":
    #da.predictor()
    st.title("Train your own Machine Learning algorithm")
    st.header("Try to make the best predictions possible by adjusting the model parameters")

    ### User filters
    # Data
    st.sidebar.subheader("Data for the model")
    y = st.sidebar.text_input("Choose your target variable (y):")
    X = st.sidebar.text_area("Choose your explanatory variables (X):")
    X = X.split("\n")

    button = st.sidebar.button("Submit selection")

    # Data processing
    st.sidebar.subheader("Data processing for machine learning")
    scaler = st.sidebar.radio(label = "Do you want to scale the data?",
                              options = [False, True])
    balance = st.sidebar.slider(label = "Do you want to oversample the minority class?",
                                min_value = 0.0, max_value = 1.0, step = .2)

    # Model settings
    st.sidebar.subheader("Machine Learning settings")
    seed = 42
    chosen_model = st.sidebar.selectbox(label = "Choose the model",
                         options = ["Logistic Regression", "Random Forest Classifier", "SVM"])
    
    if chosen_model == "Logistic Regression":
        max_iter = st.sidebar.slider(label = "Max iterations", min_value = 100, max_value= 400, step = 100)
        model = LogisticRegression(n_jobs = -1, random_state = seed,
                                   max_iter = max_iter)
    
    if chosen_model == "Random Forest Classifier":
        n_estimators = st.sidebar.slider(label = "Number of estimators", min_value = 100, max_value= 250, step = 50)
        max_depth = st.sidebar.slider(label = "Max depth", min_value = 10, max_value= 30, step = 5)
        max_features = st.sidebar.radio("Max features", options = ["auto", "sqrt", "log2"])
        model = RandomForestClassifier(n_jobs = -1, random_state = seed,
                                       n_estimators = n_estimators,
                                       max_depth = max_depth,
                                       max_features = max_features)

    if chosen_model == "SVM":
        max_iter = st.sidebar.slider(label = "Max iterations", min_value = 100, max_value= 200, step = 20)
        model = LinearSVC(random_state = seed,
                          max_iter = max_iter)


    ### Output
    # Data stats
    if button:
        features = [y] + X
        data = dataset.filter_columns(features)

        st.table(data.head())
        st.write(data.describe())


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
    