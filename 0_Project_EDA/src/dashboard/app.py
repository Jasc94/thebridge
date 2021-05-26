import streamlit as st

import pandas as pd

import sys
import os

import requests
import webbrowser

path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(path)

import src.utils.mining_data_tb as md
import src.utils.visualization_tb as vis
import src.utils.markdown as mark


# -------------------------- SUPPORT --------------------------
# >>> Function to pull the nutrition data
@st.cache
def get_nutrition_data():
    df_path = "../../data/Nutritional_values.csv"
    #df_path = "0_Project_EDA/data/Nutritional_values.csv"
    df = pd.read_csv(df_path)
    df2 = md.nutrition_prep(df)
    return df2

# >>> Function to pull the recommmended daily intake urls
@st.cache
def get_dailyintake_data():
    df_path = "../../data/daily_intakes.csv"
    df = pd.read_csv(df_path)
    return df

# >>> Function to pull the resources data
@st.cache
def get_resources_data():
    path1 = "../../data"
    path2 = "../../data/Resources_use"
    df = md.join_resources(path1, path2)
    return df


# Create the dataframes with the functions
df = get_nutrition_data()                       # For nutrition
dailyintake_df = get_dailyintake_data()         # For daily intake
resources_df = get_resources_data()


# >>> Sidebar menu to navigate through sections
menu = st.sidebar.selectbox('Menu:',
            options=["Home", "Nutrition Facts", "Nutrition Comparator", "Resources Facts",
                    "Resources Comparator", "Flask"])

# -------------------------- HOME --------------------------
if menu == "Home":
    st.title("Welcome to the Nutrition & Resources - EDA App")
    st.image("../../resources/home_cow.jpeg")


# -------------------------- NUTRITION FACTS --------------------------
if menu == "Nutrition Facts":
    # >>> User input to build tables and plots
    # Title
    st.sidebar.header("Play around")

    # 1) Pick nutrient
    chosen_nutrient = st.sidebar.selectbox('Nutrient:',
                                        options = md.key_nutrients())

    # 2) Pick how many you want to see of the top
    chosen_top = st.sidebar.slider(label = "How many foods?", min_value = 5, max_value = 50, value = 5, step = 5)

    # 3) Positive filters
    st.sidebar.write("\nTo filter:")
    soy = st.sidebar.checkbox(label = "Soy")
    tofu = st.sidebar.checkbox(label = "Tofu")
    meat = st.sidebar.checkbox(label = "Meat")
    chicken = st.sidebar.checkbox(label = "Chicken")
    fish = st.sidebar.checkbox(label = "Fish")

    pos_filters = []
    if soy == True: pos_filters.append("Soy")
    if tofu == True: pos_filters.append("Tofu")
    if meat == True: pos_filters.append("Meat")
    if chicken == True: pos_filters.append("Chicken")
    if fish == True: pos_filters.append("Fish")

    # 4) Negative filters
    st.sidebar.write("\nTo filter out:")
    beverages = st.sidebar.checkbox(label = "Beverages")
    supplements = st.sidebar.checkbox(label = "Supplements")
    nutritional = st.sidebar.checkbox(label = "Nutritional")
    concentrate = st.sidebar.checkbox(label = "Concentrate")

    neg_filters = []
    if beverages == True: neg_filters.append("Beverages")
    if supplements == True: neg_filters.append("supplement")
    if nutritional == True: neg_filters.append("nutritional")
    if concentrate == True: neg_filters.append("concentrate")

    # 5) Using the filters, create the df
    # first do the positive filtering
    if len(pos_filters) > 0: df = md.several_filters(df, pos_filters, out = False)
    # then the negative one
    if len(neg_filters) > 0: df = md.several_filters(df, neg_filters)
    # apply the rest
    top_foods = md.nutrient_selector(chosen_nutrient, df).head(chosen_top)

    # >>> Site
    st.header(f"Top food sources for **{chosen_nutrient}**")

    # 1) Plot
    st.subheader("Top foods representation")
    # st.bar_chart(top_foods, width = 1200, height = 600, 
    #                 use_container_width = True)             # REVISAR
    
    fig = vis.nutritionfacts_graph1(top_foods, chosen_nutrient)
    st.pyplot(fig)

    # 2) Table
    st.subheader("Top foods characteristics")
    st.table(top_foods)



# -------------------------- NUTRITION COMPARATOR --------------------------
if menu == "Nutrition Comparator":
    # >>> User input to build tables and plots
    # Title
    st.sidebar.header("Play around")

    # > Food items
    # 1) Pick the food items
    foodname_1 = st.sidebar.text_input("Choose a food item 1")
    foodname_2 = st.sidebar.text_input("Choose a food item 2")

    # 3) Calculating the dataframe
    if foodname_1 == "":
        foodname_1 = "Cornstarch"

    if foodname_2 == "":
        foodname_2 = "Cornstarch"

    food1_data = md.food_selector(foodname_1, df)
    food2_data = md.food_selector(foodname_2, df)

    # 4) List of items
    food_items =[food1_data, food2_data]

    # > Gender and age
    # 1) Choose age and gender to calculate recommended daily intake
    chosen_gender = st.sidebar.radio(label = "Gender", options = ["Male", "Female"], index = 0).lower()
    chosen_age = st.sidebar.slider(label = "Age", min_value = 20, max_value = 70, value = 20, step = 10)

    # 2) Pull data of recommended daily intake based on gender & age
    #url = "https://www.eatforhealth.gov.au/node/1813927/done?sid=806757&token=05ce5572f5618ac641c9f2395b28c59f"
    url = md.pick_di(chosen_gender, chosen_age, dailyintake_df)
    dailyintake = md.dailyintake_info(url)
    dailyintake_cleaned = md.dailyintake_prep(dailyintake)

    
    # > Calculate food quality based on daily intake proportion
    food_quality = md.foodquality(dailyintake_cleaned, food_items)


    # >>> Site
    st.header(f"Nutritional values for 100g")
    st.subheader(f"**{foodname_1}** vs **{foodname_2}**")

    # Comparison table
    st.table(food_quality)

    #fig = vis.dailyintake_graph(food1_quality)
    #col2.pyplot(fig)
    st.bar_chart(food_quality.iloc[2])

    # Inputs from user to calculate the % of the nutrients daily intake
    
    
    
    #st.bar_chart(fig)
    #st.pyplot(fig)


if menu == "Resources Facts":
    # >>> User input to build tables and plots
    # Title
    st.sidebar.header("Play around")

    # Resource
    selected_resource = st.sidebar.selectbox(options = resources_df.columns,
                                            label = "Select an option",
                                            index = len(resources_df.columns) - 1)

    # How big the top
    selected_top = st.sidebar.slider(label = "Entries",
                    min_value = 10, max_value = 50, value = 10, step = 10)


    # Calculate df
    resources_df_to_show = resources_df.sort_values(by = selected_resource,
                            ascending = False).head(selected_top)


    # >>> Site
    # Plot
    fig = vis.emissions_graph(resources_df_to_show, selected_resource)
    st.pyplot(fig)

    # Data
    st.table(resources_df_to_show)
    
    

if menu == "Resources Comparator":
    #TODO
    st.radio(label = "Test", options = ["option 1", "option 1", "option 1"])


if menu == "Flask":
    # >>> User input to pull data from server
    # Title
    st.sidebar.header("Choose datasets")

    nutrition_checkbox = st.sidebar.checkbox(label = "Nutrition dataset")
    resources_checkbox = st.sidebar.checkbox(label = "Resources dataset")
    health_checkbox = st.sidebar.checkbox(label = "Health dataset")

    button = st.sidebar.button("Show table")

    if button:
        if nutrition_checkbox:
            # Pull the data from the server
            url = "http://localhost:6060/nutrition-data"
            nutrition_data = pd.read_json(url)

            # nutrition_data_1 = nutrition_data[:round(len(nutrition_data) / 2)]
            # nutrition_data_2 = nutrition_data[round(len(nutrition_data) / 2):]

            # Streamlit output
            st.header("Here you have the **nutrition** dataset")
            # st.markdown(mark.get_table_download_link(nutrition_data_1), unsafe_allow_html = True)
            # st.markdown(mark.get_table_download_link(nutrition_data_2), unsafe_allow_html = True)
            st.table(nutrition_data.head())

        if resources_checkbox:
            # Pull the data from the server
            url = "http://localhost:6060/resources-data"
            resources_data = pd.read_json(url)
            # Streamlit output
            st.header("Here you have the **resources** dataset")
            st.markdown(mark.get_table_download_link(resources_data), unsafe_allow_html = True)
            st.table(resources_data.head())

        if health_checkbox:
            # Pull the data from the server
            url = "http://localhost:6060/health-data"
            health_data = pd.read_json(url)
            # Streamlit output
            st.header("Here you have the **health** dataset")
            st.markdown(mark.get_table_download_link(health_data), unsafe_allow_html = True)
            st.table(health_data.head())

# if menu == "Definitions":
#     #TODO
#     st.write("TODO")
