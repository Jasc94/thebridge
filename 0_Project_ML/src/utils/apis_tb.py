from flask import Flask, request, render_template, Response
from imblearn.over_sampling import SMOTE
from sqlalchemy import create_engine

import numpy as np
import pandas as pd
import joblib
import json

import sys, os, argparse

# Helpers
abspath = os.path.abspath
dirname = os.path.dirname
sep = os.sep

current_folder = dirname(abspath(__file__))
sys.path.append(current_folder)

#for i in sys.path: print(i)

import folder_tb as fo
import mining_data_tb as md
import sql_tb as sq

#  Flask object
app = Flask(__name__)

# API password
data_password = "12345"
variables_password = "123456"
sql_password = "1234567"
model_password = "12345678"

##################################################### FLASK FUNCTIONS #####################################################
#####
@app.route("/")
def home():
    return "Gracias por venir"

#####
@app.route("/data", methods = ["GET"])
def data():
    '''
    Access to the cleaned dataset
    '''
    x = request.args["password"]

    if x == data_password:
        data_path = fo.path_to_folder(2, "data" + sep + "7_cleaned_data") + "cleaned_data.csv"
        df = pd.read_csv(data_path)
        return df.to_json()

    else:
        return "Wrong password"

#####
@app.route("/variables-data", methods = ["GET"])
def variables_data():
    '''
    Access to the variables data
    '''
    x = request.args["password"]

    if x == variables_password:
        data_path = fo.path_to_folder(2, "data" + sep + "6_variables") + "0_final_variables.csv"
        df = pd.read_csv(data_path)
        return df.to_json()

    else:
        return "Wrong password"

#####
@app.route("/sql-database", methods = ["GET"])
def sql_database():
    '''
    To insert the claned dataset into the sql database
    '''
    x = request.args["password"]

    if x == sql_password:
        # Data
        data_path = fo.path_to_folder(2, "data" + sep + "7_cleaned_data") + "cleaned_data.csv"
        data = pd.read_csv(data_path)

        # Server settings
        settings_path = fo.path_to_folder(1, "sql") + "sql_server_settings.json"
        read_json = md.read_json_to_dict(settings_path)

        IP_DNS = read_json["IP_DNS"]
        USER = read_json["USER"]
        PASSWORD = read_json["PASSWORD"]
        DB_NAME = read_json["DB_NAME"]
        PORT = read_json["PORT"]

        # Server connection
        sql_db = sq.MySQL(IP_DNS, USER, PASSWORD, DB_NAME, PORT)
        sql_db.connect()

        db_connection_str = sql_db.SQL_ALCHEMY
        db_connection = create_engine(db_connection_str)

        count = 1
        table_created = False

        while table_created == False:
            try:
                save_name = "api_table_" + str(count)
                data.to_sql(save_name, con = db_connection, index = False)
                table_created = True
            except:
                count += 1
        
        sql_db.close()
        
        return "Table succesfully created"
    
    else:
        return "Wrong password"

##################################################### MAIN FUNCTION #####################################################
def main():
    print("--- STARTING PROCESS ---")
    print(__file__)

    settings_path = fo.path_to_folder(2, "src" + sep + "api") + "settings.json"
    print("settings path:\n", settings_path)

    read_json = md.read_json(settings_path)

    SERVER_RUNNING = read_json["SERVER_RUNNING"]
    print("SERVER_RUNNING", SERVER_RUNNING)

    if SERVER_RUNNING:
        DEBUG = read_json["DEBUG"]
        HOST = read_json["HOST"]
        PORT = read_json["PORT"]

        app.run(debug = DEBUG, host = HOST, port = PORT)

    else:
        print("Server settings.json doesn't allow to start server. " + 
            "Please, allow it to run it.")