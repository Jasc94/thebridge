import streamlit as st

import copy
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
def get_data(allow_output_mutation=True):
    #### Variables data
    vardata_downpath = "data" + sep + "6_variables" + sep + "0_final_variables.csv"
    vardata = md.variables_data()
    vardata.load_data(2, vardata_downpath)

    #### Unprocessed Dataset
    # raw_dataset_path = fo.path_to_folder(2, "data" + sep + "7_cleaned_data") + "raw_data.csv"
    # raw_dataset = pd.read_csv(raw_dataset_path)

    #### Dataset
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

    # Correction
    vardata.df = vardata.df[vardata.df.vAr_nAmE.isin(list(dataset.df.drop("MCQ160H", axis = 1).columns))]

    return vardata, dataset

###
vardata, dataset = get_data()
ml_dataset = copy.deepcopy(dataset)        # Support object for "Predictor section"
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

    ##### SECTION 1: Exploring variables
    st.header("1) Explore the data")
    # Table filters
    st.sidebar.subheader("1) Variables exploration")
    sort_by = st.sidebar.radio("Sort by:", options = ["Variable nomenclature", "Variable description"])
    translation = {
        "Variable nomenclature" : "vAr_nAmE",
        "Variable description" : "var_descr",
    }

    filter_by = st.sidebar.radio("Filter by:", options = ["Demographics", "Dietary", "Examination", "Laboratory", "Questionnaire"])
    
    to_show = variables_df.sort_values(by = translation[sort_by])
    to_show = to_show[to_show.component == filter_by]

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
                    font = dict(size = 20, color = "white")),

                    cells = dict(values = table_data,
                    fill_color = "#7FAEF5",
                    align = "left",
                    font = dict(size = 16),
                    height = 30)
                    ))
    table.update_layout(height = 300, margin = dict(l = 0, r = 0, b = 0, t = 0))

    st.write(table)
    
    ##### SECTION 2: Chossing and plotting variables
    st.header("2) Choose and plot some variables")

    # Plot filters
    st.sidebar.subheader("2) Data plotting")
    y = st.sidebar.text_input("Choose your target variable (y):")
    X = st.sidebar.text_area("Choose your explanatory variables (X):")
    X = X.split("\n")

    button = st.sidebar.button("Submit selection")

    # Plots
    if button:
        # Data preprocessing
        features = [y] + X
        data = dataset.filter_columns(features)
        filtered_data = data.dropna()

        data_stats = filtered_data.describe().T
        data_stats = data_stats.reset_index()
        data_stats = data_stats.drop("count", axis = 1)
        data_stats = data_stats.applymap(lambda x: md.round_number(x, 3))
        data_columns = list(data_stats.columns)

        corr = np.array(filtered_data.corr().applymap(lambda x: round(x, 3)))

        y_descr = vardata.var_descr_detector(y)
        X_descr = vardata.vars_descr_detector(X, cut = 30)
        descrs = [y] + X_descr

        # Stats table
        table_header = data_columns
        table_data = [data_stats.iloc[:, column].values for column in range(len(data_columns))]

        table = go.Figure(data = go.Table(
                        columnwidth = [20, 10, 10, 10, 10, 10, 10, 10],
                        header = dict(values = table_header,
                        fill_color = "#3D5475",
                        align = "left",
                        font = dict(size = 20, color = "white")),

                        cells = dict(values = table_data,
                        fill_color = "#7FAEF5",
                        align = "left",
                        font = dict(size = 16),
                        height = 30)
                        ))
        if len(features) < 6:
            table.update_layout(autosize = False, width = 600, height = 150,
                                margin = dict(l = 0, r = 0, b = 0, t = 0))
        else:
            table.update_layout(autosize = False, width = 600, height = 200,
                                margin = dict(l = 0, r = 0, b = 0, t = 0))

        st.write(table)

        # Data insights
        expander = st.beta_expander("Insights on the data")
        with expander:
            st.write("**Chosen variables**:")
            for feature in features:
                st.write(vardata.var_descr_detector(feature, nom_included = True))
            
            st.write("**Number of observations**:")
            st.write(f"- Before dropping the NaN values:\t{data.shape[0]}")
            st.write(f"- After dropping the NaN values:\t{filtered_data.shape[0]}")
            st.write("\n")
            st.write("**Target variable (y) values**:")
            st.table(filtered_data.loc[:, y].value_counts())

            nahnes_url = "https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2017"
            st.write("More info in the following link:")
            st.markdown(nahnes_url, unsafe_allow_html=True)

        # Correlation plot
        st.write(y_descr)
        colorscale = [[0, "white"], [1, "cornflowerblue"]]
        correlation_plot = ff.create_annotated_heatmap(corr,
                                                       #x = descrs,
                                                       y = descrs,
                                                       colorscale = colorscale)
        st.write(correlation_plot)

        # Distribution plots
        for x in X:
            x_descr = vardata.var_descr_detector(x, cut = 30, nom_included = True)
            expander = st.beta_expander(x_descr)

            with expander: 
                to_plot = filtered_data.loc[:, [y, x]].dropna()
                histogram = px.histogram(to_plot, x = x, color = y,
                                        marginal = "box",
                                        labels = {x : x_descr},
                                        width = 600)
                st.write(histogram)

#########
if menu == "Predictor":
    #da.predictor()
    
    # st.header("Train your own Machine Learning algorithm")
    # st.subheader("Try to make the best predictions possible by adjusting the model parameters")
 
    ##### SECTION 1: Chossing variables
    st.sidebar.subheader("1) Data for the model")
    y = st.sidebar.text_input("Choose your target variable (y):")
    X = st.sidebar.text_area("Choose your explanatory variables (X):")
    X = X.split("\n")

    features = [y] + X

    # To train the model
    train_button = st.sidebar.button("Train model")
    test_button = st.sidebar.button("Test model")

    ##### SECTION 2: Processing the data
    ### Subsection 2.1
    cols = st.beta_columns(2)

    # Data processing
    cols[0].subheader("2) Data processing for the model")
    split = cols[0].slider(label = "How big do you want the test batch to be?",
                                min_value = 0.1, max_value = 1.0, step = .1)
    cv = cols[0].slider(label = "How mane validation batches do you want?",
                                min_value = 1, max_value = 5, step = 1)                            
    balance = cols[0].slider(label = "Do you want to oversample the minority class?",
                                min_value = 0.0, max_value = 1.0, step = .2)
    balance = balance if balance > 0 else None
    scaler = cols[0].radio(label = "Do you want to scale the data?",
                              options = [False, True])

    ##### SECTION 3: Model selection
    # Model settings
    cols[1].subheader("3) ML model settings")
    seed = 42
    chosen_model = cols[1].selectbox(label = "Choose the model",
                         options = ["Logistic Regression", "Random Forest Classifier", "SVM"])
    
    if chosen_model == "Logistic Regression":
        max_iter = cols[1].slider(label = "Max iterations", min_value = 100, max_value= 400, step = 100)
        model = LogisticRegression(n_jobs = -1, random_state = seed,
                                   max_iter = max_iter)
    
    if chosen_model == "Random Forest Classifier":
        n_estimators = cols[1].slider(label = "Number of estimators", min_value = 100, max_value= 250, step = 50)
        max_depth = cols[1].slider(label = "Max depth", min_value = 10, max_value= 30, step = 5)
        max_features = cols[1].radio("Max features", options = ["auto", "sqrt", "log2"])
        model = RandomForestClassifier(n_jobs = -1, random_state = seed,
                                       n_estimators = n_estimators,
                                       max_depth = max_depth,
                                       max_features = max_features)

    if chosen_model == "SVM":
        max_iter = cols[1].slider(label = "Max iterations", min_value = 100, max_value= 200, step = 20)
        model = LinearSVC(random_state = seed,
                          max_iter = max_iter)

    
    ##### Model training
    if train_button:
        # Data processing according to chosen settings
        ml_dataset.filter_columns(features, inplace = True)
        ml_dataset.df = ml_dataset.df.dropna()
        ml_dataset.model_data(split, cv, scaler = scaler, balance = balance)

        # Model training
        my_model = md.ml_model(model)
        my_model.load_data(ml_dataset.X_train, ml_dataset.X_test, ml_dataset.y_train, ml_dataset.y_test, features, ml_dataset.kfold)
        my_model.ml_trainer()

        # Results output
        expander = st.beta_expander("More info on the model and training")
        with expander:
            st.write("**Train structures**")
            st.write(my_model.train_set_structures)
            st.write("**Validation structures**")
            st.write(my_model.val_set_structures)
            try:
                st.write("**Feature importances**:")
                st.table(my_model.feature_importances)
            except:
                pass


        fig = go.Figure()
        x_axis = list(range(len(my_model.train_scores)))
        fig.add_trace(go.Scatter(x = x_axis, y = my_model.train_scores, name = "Train scores"))
        fig.add_trace(go.Scatter(x = x_axis, y = my_model.val_scores, name = "Validation scores"))

        st.write(fig)

    if test_button:
        
    ### Output

    
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
    