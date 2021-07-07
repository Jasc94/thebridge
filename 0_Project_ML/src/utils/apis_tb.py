from flask import Flask, request, render_template, Response
from imblearn.over_sampling import SMOTE

import pandas as pd

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

#  Flask object
app = Flask(__name__)

# API password
data_password = "12345"
variables_password = "123456"

##################################################### FLASK FUNCTIONS #####################################################
#####
@app.route("/")
def home():
    return "Gracias por venir"

@app.route("/data", methods = ["GET"])
def data():
    x = request.args["password"]

    if x == data_password:
        data_path = fo.path_to_folder(2, "data" + sep + "7_cleaned_data") + "cleaned_data.csv"
        df = pd.read_csv(data_path)
        return df.to_json()

    else:
        return "Wrong password"

@app.route("/variables-data", methods = ["GET"])
def variables_data():
    x = request.args["password"]

    if x == variables_password:
        data_path = fo.path_to_folder(2, "data" + sep + "6_variables") + "0_final_variables.csv"
        df = pd.read_csv(data_path)
        return df.to_json()

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