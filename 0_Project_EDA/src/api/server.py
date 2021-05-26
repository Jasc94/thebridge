from flask import Flask, request, render_template, Response

import pandas as pd

import sys
import os

path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(path)

import src.utils.mining_data_tb as md
import src.utils.apis_tb as ap

# Objecto Flask
app = Flask(__name__)


# ------------------- Flask functions -------------------
@app.route("/")
def home():
    return app.send_static_file("test.html")

@app.route("/nutrition-data", methods = ['GET'])
def nutrition_dataframe():
    df = pd.read_csv("0_Project_EDA/data/Nutritional_values.csv")
    return df.to_json()

@app.route("/resources-data", methods = ['GET'])
def resources_dataframe():
    df = pd.read_csv("0_Project_EDA/data/Food_production.csv")
    return df.to_json()

# UPDATE THE URL
@app.route("/health-data", methods = ['GET'])
def health_dataframe():
    df = pd.read_csv("0_Project_EDA/data/daily_intakes.csv")
    return df.to_json()

# @app.route("/data", methods = ['GET'])
# def data_frame():
#     df = pd.read_csv("0_Project_EDA/data/daily_intakes.csv")
#     df = df.to_json()
#     return Response(df, mimetype = "application/json")


@app.route("/data_token", methods = ['GET'])
def data_frame_token():
    x = request.args['password']
    if x == "1234":
        df = pd.read_csv("0_Project_EDA/data/daily_intakes.csv")
        return df.to_json()
    else:
        return "Contraseña incorrecta"

# ------------------- Other functions -------------------
def main():
    print("--- STARTING PROCESS ---")
    print(__file__)

    settings_file = os.path.dirname(__file__) + "/settings.json"
    print(settings_file)

    json_read = ap.read_json(settings_file)

    SERVER_RUNNING = json_read["server_running"]
    print("SERVER_RUNNING", SERVER_RUNNING)

    if SERVER_RUNNING:
        DEBUG = json_read["debug"]
        HOST = json_read["host"]
        PORT_NUM = json_read["port"]

        app.run(debug = DEBUG, host = HOST, port = PORT_NUM)

    else:
        print("Server settings.json doesn't allow to start server. " + 
            "Please, allow it to run it.")

if __name__ == "__main__":
    main()