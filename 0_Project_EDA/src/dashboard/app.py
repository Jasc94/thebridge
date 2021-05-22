import streamlit as st

import pandas as pd

#header = st.beta_container()
menu = st.sidebar.selectbox('Menu:',
            options=["No selected", "Normal Dataframe", "Load Dataframe Columns", "Graphs", "Map"])

# with header:
#     st.title("First test of Streamlit")
#     st.text("Some more test text")

#     df = pd.read_csv("../../data/Nutritional_values.csv")
#     st.write(df.head(10))

with menu:
    st.write("Anything")