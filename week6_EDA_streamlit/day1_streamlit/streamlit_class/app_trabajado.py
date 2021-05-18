# -*- coding: utf-8 -*-
import streamlit as st
import os
from utils.stream_config import create_sliders, draw_map
from utils.dataframes import get_data_from_df, load_csv_df, load_csv_for_map, load_normal_csv

path = os.path.dirname(__file__)
df = None
    
menu = st.sidebar.selectbox('Menu:',
            options=["Bienvenida", "Analizador", "Mapa con globos"])

# st.title('Wine Quality Classifier Web App')
# st.write('This is a web app to classify the quality of your wine based on\
#          several features that you can see in the sidebar. Please adjust the\
#          value of each feature. After that, click on the Predict button at the bottom to\
#          see the prediction of the classifier.')

if menu == 'Bienvenida':
    st.title("Bienvenidos al bootcamp the TheBridge")
    st.write("Es un placer tenerte por aquí")

if menu == "Analizador":
    # Sidebar para subir el dataframe
    slider_csv = st.sidebar.file_uploader("Selecciona un CSV o un PNG", type=['csv', 'png'])
    # Cargar el dataframe
    if type(slider_csv) != type(None):          # Se cumple cuando subamos un archivo
        filtro_edades = st.sidebar.checkbox("Filtrar edades")
        df_slider = load_normal_csv(slider_csv)
        # Si se cumple la condición, creará un nuevo df_slider
        if filtro_edades:
            df_slider = df_slider[df_slider["age"] < 10]
        st.bar_chart(df_slider)
        st.table(df_slider)
    
if menu == "Mapa con globos":
    csv_map_path = path + os.sep + "data" + os.sep + 'red_recarga_acceso_publico_2021.csv'
    df_map = load_csv_for_map(csv_map_path)
    draw_map(df_map)