import streamlit as st
from PIL import Image
import json

import sys, os
import pandas as pd


#""" Siempre que veas 'pass' es un TO-DO (por hacer)"""

#"""1"""
# Haz que se pueda importar correctamente estas funciones que están en la carpeta utils/
path = os.path.abspath(__file__)
dir = os.path.dirname

for i in range(2): path = dir(path)

sys.path.append(path)
#####

from utils.stream_config import draw_map
from utils.dataframes import load_csv_for_map
import utils.sql_functions as sq
import utils.ml as ml

data_path = dir(path) + "/data"

@st.cache
def pull_data():
    sql_path = dir(path) + os.sep + "config" + os.sep + "bd_info.json"

    with open(sql_path, "r") as json_file:
        read_json = json.load(json_file)

    IP_DNS = read_json["IP_DNS"]
    PORT = read_json["PORT"]
    USER = read_json["USER"]
    PASSWORD = read_json["PASSWORD"]
    BD_NAME = read_json["BD_NAME"]

    sql = sq.MySQL(IP_DNS, USER, PASSWORD, BD_NAME, PORT)

    sql.connect()

    select_sql = """SELECT * FROM fire_nrt_M6_96619"""
    #select_sql = '''
    #SELECT * FROM fire_archive_M6_96619
    #UNION
    #SELECT * FROM fire_archive_V1_96617
    #ORDER BY City;'''

    result = sql.execute_get_sql(select_sql)
    df = pd.DataFrame(result)

    return df

df = pull_data()

menu = st.sidebar.selectbox('Menu:',
            options=["No selected", "Load Image", "Map", "API", "MySQL", "Machine Learning"])

if menu == "No selected": 
    #"""2"""
    # Pon el título del proyecto que está en el archivo "config.json" en /config
    title_path = dir(path) + "/config/config.json"

    with open(title_path, "r") as json_file:
        read_json = json.load(json_file)

    st.title(read_json["Title"])
    # Pon la descripción del proyecto que está en el archivo "config.json" en /config
    st.write(read_json["Description"])
    
if menu == "Load Image": 
    #"""3"""
    # Carga la imagen que está en data/img/happy.jpg
    image_path = data_path + "/img/happy.jpg"

    image = Image.open(image_path)  
    st.image (image,use_column_width=True)

if menu == "Map":
    #"""4"""
    # El archivo que está en data/ con nombre 'red_recarga_acceso_publico_2021.csv'
    csv_map_path = data_path + "/red_recarga_acceso_publico_2021.csv"
    df_map = load_csv_for_map(csv_map_path)
    draw_map(df_map)

if menu == "API":
    #"""5"""
    # Accede al único endpoint de tu API flask y lo muestra por pantalla como tabla/dataframe
    url = f"http://localhost:6060/"
    flask_data = pd.read_json(url)

    st.table(flask_data)
    

if menu == "MySQL":
    #"""6"""

    # 1. Conecta a la BBDD
    # 2. Obtén, a partir de sentencias SQL (no pandas), la información de las tablas que empiezan por 'fire_archive*' (join)
    # 3. Entrena tres modelos de ML diferentes siendo el target la columna 'fire_type'. Utiliza un pipeline que preprocese los datos con PCA. Usa Gridsearch.  
    # 4. Añade una entrada en la tabla 'student_findings' por cada uno de los tres modelos. 'student_id' es EL-ID-DE-TU-GRUPO.
    # 5. Obtén la información de la tabla 'fire_nrt_M6_96619' y utiliza el mejor modelo para predecir la columna target de esos datos. 
    # 6. Usando SQL (no pandas) añade una columna nueva en la tabla 'fire_nrt_M6_96619' con el nombre 'fire_type_EL-ID-DE-TU-GRUPO'
    # 7. Muestra por pantalla en Streamlit la tabla completa (X e y)

    # sql_path = dir(path) + os.sep + "config" + os.sep + "bd_info.json"

    # with open(sql_path, "r") as json_file:
    #     read_json = json.load(json_file)

    # IP_DNS = read_json["IP_DNS"]
    # PORT = read_json["PORT"]
    # USER = read_json["USER"]
    # PASSWORD = read_json["PASSWORD"]
    # BD_NAME = read_json["BD_NAME"]

    # sql = sq.MySQL(IP_DNS, USER, PASSWORD, BD_NAME, PORT)

    # sql.connect()

    # select_sql = """SELECT * FROM fire_nrt_M6_96619"""
    # #select_sql = '''
    # #SELECT * FROM fire_archive_M6_96619
    # #UNION
    # #SELECT * FROM fire_archive_V1_96617
    # #ORDER BY City;'''

    # result = sql.execute_get_sql(select_sql)
    # df = pd.DataFrame(result)

    # ml.modeling(df)

    # #st.write(df.head())
    # st.table(df.head())

    st.table(df.head())


if menu == "Machine Learning":
    result = ml.modeling(df)

    st.write(result)