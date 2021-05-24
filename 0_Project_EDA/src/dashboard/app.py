import streamlit as st

import pandas as pd

import sys
import os

path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(path)

import src.utils.mining_data_tb as md
import src.utils.visualization_tb as vis


# -------------------------- SUPPORT --------------------------
# >>> Function to pull the data
@st.cache
def get_nutrition_data():
    df_path = "../../data/Nutritional_values.csv"
    #df_path = "0_Project_EDA/data/Nutritional_values.csv"
    df = pd.read_csv(df_path)
    df2 = md.nutrition_prep(df)
    return df2

# Create the dataframe with the function
df = get_nutrition_data()

# >>> Some extra style
# st.markdown(
#     """
#     <style>
#     .css-1kzqdq1 e1ynspad1 {
#         width:95%;
#         border-collapse:collapse;
#     }
#     </style>
#     """,
#     unsafe_allow_html = True
# )

#header = st.beta_container()
menu = st.sidebar.selectbox('Menu:',
            options=["Home", "Nutrition Facts", "Nutrition Comparator", "Resources Facts",
                    "Resources Comparator"])

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
    #foodname_2 = st.sidebar.text_input("Choose a food item 2")

    # 3) Calculating the dataframe
    if foodname_1 == "":
        foodname_1 = "Cornstarch"
    food1_data = md.food_selector(foodname_1, df)

    # > Gender and age
    # 1) Choose age and gender to calculate recommended daily intake
    chosen_age = st.sidebar.slider(label = "Age", min_value = 20, max_value = 70, value = 20, step = 10)
    chosen_gender = st.sidebar.radio(label = "Gender", options = ["Men", "Women"], index = 0)

    # 2) Pull data of recommended daily intake based on gender & age
    url = "https://www.eatforhealth.gov.au/node/1813927/done?sid=806757&token=05ce5572f5618ac641c9f2395b28c59f"
    dailyintake_s = md.dailyintake_info(url)
    dailyintake = md.dailyintake_prep(dailyintake_s)

    
    # > Calculate food quality based on daily intake proportion
    food1_quality = md.foodquality(food1_data, dailyintake)


    # >>> Site
    st.header(f"Nutritional values for 100g of **{foodname_1}**")

    #df = get_nutrition_data()
    st.table(food1_quality.T)

    #fig = vis.dailyintake_graph(food1_quality)
    #col2.pyplot(fig)
    st.bar_chart(food1_quality.set_index("nutrient"))

    # Inputs from user to calculate the % of the nutrients daily intake
    
    
    
    #st.bar_chart(fig)
    #st.pyplot(fig)


# if menu == "Top food":
#     #TODO
#     st.write("TODO")

# if menu == "Definitions":
#     #TODO
#     st.write("TODO")
