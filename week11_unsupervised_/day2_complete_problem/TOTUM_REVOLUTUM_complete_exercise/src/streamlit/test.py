import os, sys, json
from PIL import Image
import pandas as pd

path = os.path.abspath(__file__)
dir = os.path.dirname

for i in range(2): path = dir(path)

sys.path.append(path)
#####

from utils.stream_config import draw_map
from utils.dataframes import load_csv_for_map
import utils.sql_functions as sq

# with open(title_path, "r") as json_file:
#     read_json = json.load(json_file)

# print(read_json["Title"])

# data_path = dir(path) + "/data"
# image_path = data_path + "/img/happy.jpg"

# image = Image.open(image_path)
# print(image)

# csv_map_path = path + "/red_recarga_acceso_publico_2021.csv"
# df_map = load_csv_for_map(csv_map_path)
# draw_map(df_map)

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

#st.write(df.head())
print(df.head())

# Model training
X = df.iloc[:, :-1]

y = df.iloc[:, -1]

print(X.head())
print(y)