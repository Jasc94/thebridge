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


# ### Sidebar menu to navigate through sections
menu = st.sidebar.selectbox('Menu:',
            options=["Home", "Resources Facts", "Nutrition Facts", "Glosary", "Flask"])

# ### HOME
if menu == "Home":
    da.home()

# ### RESOURCES FACTS
if menu == "Resources Facts":
    da.resources_facts()

# ### NUTRITION FACTS
if menu == "Nutrition Facts":
    da.nutrition_facts()

# ### GLOSARY
if menu == "Glosary":
    da.glosary()

# ### FLASK
if menu == "Flask":
    da.flask_interface()