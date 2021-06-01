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
import src.utils.folder_tb as fo
import src.utils.markdown as mark
import src.utils.dashboard as da

###############################################################################################
# ############################ -- PULLING THE DATA -- ############################

# To get the data and save it in the cache
@st.cache
def get_data():
    # Resources data
    path1 = fo.path_to_folder(2, "data")
    path2 = fo.path_to_folder(2, "data/Resources_use")
    resources_df = md.get_resources_data(path1, path2)

    # Nutritional values data
    path3 = fo.path_to_folder(2, "data")
    filename1 = "2017-2018 FNDDS At A Glance - FNDDS Nutrient Values.xlsx"
    nutrition_df = md.get_nutrition_data(path3, filename1)

    food_groups_stats = md.nutrients_stats(nutrition_df)

    # Recommended Daily Intake data
    path4 = fo.path_to_folder(2, "data")
    filename2 = "daily_intakes.csv"
    daily_intake_df = pd.read_csv(path4 + filename2)

    return resources_df, nutrition_df, food_groups_stats, daily_intake_df

# Store the data in dfs
resources_df, nutrition_df, food_groups_stats, daily_intake_df = get_data()


###############################################################################################
# ############################ -- FRONTEND -- ############################

# ### Sidebar menu to navigate through sections
menu = st.sidebar.selectbox('Menu:',
            options=["Home", "Resources Facts", "Nutrition Facts", "Glosary", "Flask"])

# ### HOME
if menu == "Home":
    cow_path = fo.path_to_folder(2, "resources")
    cow_file = "home_cow.jpeg"

    st.title("Welcome to the Nutrition & Resources - EDA App")
    st.image(cow_path + cow_file)

# ### RESOURCES FACTS
if menu == "Resources Facts":
    submenu = st.sidebar.radio(label = "What do you want to do?", options = ["Resources facts", "Comparator"])

    # Title
    st.sidebar.subheader("Play around")

    if submenu == "Resources facts":
        # User input
        chosen_resource = st.sidebar.selectbox('Choose a resource:', options = resources_df.columns)
        entries = st.sidebar.slider(label = "Entries:", min_value = 10,
                                    max_value = 50, value = 10, step = 10)

        # Page title
        st.title("This is the resources facts section")
        st.header(f"You are currently checking the top {entries} by **{chosen_resource}**")

        # Data extraction and transformation
        fig = vis.resources_plot(chosen_resource, resources_df, entries)
        table = resources_df[chosen_resource].sort_values(ascending = False).head(entries)
        
        # Data visualization
        st.pyplot(fig)
        st.table(table)
        
    else:
        st.sidebar.header("Choose resources to compare")
        st.sidebar.write("You have to choose > 1")

        resources = []

        for resource in resources_df.columns[:-1]:
            resources.append(st.sidebar.checkbox(label = resource))

        if resources.count(True) > 1:
            stats_filter = resources_df.columns[:-1][resources]
            stats = md.resources_stats(resources_df, stats_filter)
            to_plot = md.stats_to_plot(stats)
            fig = vis.plot_resources_stats(to_plot)
            
            st.pyplot(fig)
            st.table(stats.T)

        else:
            st.title(f"You still have to choose {2 - resources.count(True)} elements")


# ### NUTRITION FACTS
if menu == "Nutrition Facts":
    st.title("This is the nutrition facts section")

    submenu = st.sidebar.radio(label = "What do you want to do?", options = ["Top products", "Food groups", "Foods"])

    st.sidebar.title("Play around")

    if submenu == "Top products":
        # User input
        chosen_nutrient = st.sidebar.selectbox("Nutrient", options = md.nutrients_filter_2(4)[3:])
        entries = st.sidebar.slider(label = "How many foods?", min_value = 5, max_value = 50, 
                                    value = 5, step = 5)

        # Data extraction and transformation
        table = md.nutrient_selector(chosen_nutrient, nutrition_df).head(entries)
        fig = vis.nutritionfacts_graph1(table, chosen_nutrient)

        # Data visualization
        st.pyplot(fig)
        st.table(table)

    elif submenu == "Food groups":
        
        # User input
        gender = st.sidebar.radio("Gender", options = ["Male", "Female"]).lower()
        age = st.sidebar.slider(label = "Age", min_value = 20, max_value = 70, value = 20, step = 10)

        st.subheader("Food group filters")
        col1, col2, col3 = st.beta_columns(3)

        #food_groups_stats = md.nutrients_stats(nutrition_df)
        food_groups = []

        for food_group in food_groups_stats.index[:4]:
            food_groups.append(col1.checkbox(label = food_group))

        for food_group in food_groups_stats.index[4:8]:
            food_groups.append(col2.checkbox(label = food_group))

        for food_group in food_groups_stats.index[8:12]:
            food_groups.append(col3.checkbox(label = food_group))

        
        # Data extraction and transformation
        index = food_groups_stats[food_groups].index
        
        table = food_groups_stats[food_groups].T
        
        daily_intake = md.get_daily_intake_data(gender, age, daily_intake_df)
        comparison = md.full_comparison(daily_intake, food_groups_stats, index)

        if len(index) > 0:
            fig = vis.full_comparison_plot(comparison)

            # Data visualization
            st.subheader("Visualization")
            st.pyplot(fig)

        st.subheader("Absolute nutritional values")
        st.table(table)

    else:

        # User input
        gender = st.sidebar.radio("Gender", options = ["Male", "Female"]).lower()
        age = st.sidebar.slider(label = "Age", min_value = 20, max_value = 70, value = 20, step = 10)

        daily_intake = md.get_daily_intake_data(gender, age, daily_intake_df)

        st.subheader("Food filters")

        food_group_filter = st.selectbox('Food groups:',
            options = food_groups_stats.index)

        filter_button = st.button("Filter")

        foods_filtered = nutrition_df[nutrition_df["Category 2"] == food_group_filter].index

        with st.form("Submit"):
            chosen_foods = st.text_area("Foods you want to compare. Make sure you enter one value each line")
            submit_button = st.form_submit_button("Submit")

            # if submit_button:
            #     chosen_foods = chosen_foods.split("\n")
            #     st.write(chosen_foods)

            #     comparison = md.full_comparison(daily_intake, nutrition_df, chosen_foods)
            #     fig = vis.full_comparison_plot(comparison)

            #     # Data visualization
            #     st.subheader("Visualization")
            #     st.pyplot(fig)


        if submit_button:
            chosen_foods = chosen_foods.split("\n")
            chosen_foods = list(filter(None, chosen_foods))

            comparison = md.full_comparison(daily_intake, nutrition_df, chosen_foods)
            fig = vis.full_comparison_plot(comparison)

            # Data visualization
            st.subheader(f"Visualization of\n{chosen_foods}")
            st.pyplot(fig)

        if filter_button:
            st.table(foods_filtered)

if menu == "Flask":
    # >>> User input to pull data from server
    # Title
    st.sidebar.header("Choose datasets")

    nutrition_checkbox = st.sidebar.checkbox(label = "Nutrition dataset")
    resources_checkbox = st.sidebar.checkbox(label = "Resources dataset")

    password = st.sidebar.text_input("Password to access data")

    button = st.sidebar.button("Show table")

    if button:
        if nutrition_checkbox:
            try:
                # Pull the data from the server
                url = f"http://localhost:6060/nutrition-data?password={password}"
                nutrition_data = pd.read_json(url)

                # Streamlit output
                st.header("Here you have the **nutrition** dataset")
                # st.markdown(mark.get_table_download_link(nutrition_data_1), unsafe_allow_html = True)
                # st.markdown(mark.get_table_download_link(nutrition_data_2), unsafe_allow_html = True)
                st.table(nutrition_data.head())
            except:
                st.title("Wrong password")


        if resources_checkbox:
            try:
                # Pull the data from the server
                url = f"http://localhost:6060/resources-data?password={password}"
                resources_data = pd.read_json(url)

                # Streamlit output
                st.header("Here you have the **resources** dataset")
                st.markdown(mark.get_table_download_link(resources_data), unsafe_allow_html = True)
                st.table(resources_data.head())
            except:
                st.title("Wrong password")