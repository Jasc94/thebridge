from flask import Flask, request, render_template, Response

import pandas as pd

import sys
import os
import argparse

path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(path)

import src.utils.mining_data_tb as md
import src.utils.apis_tb as ap
import src.utils.folder_tb as fo


# path to "data" folder
data_path = fo.path_to_folder(2, "data")

# OFlask object
app = Flask(__name__)


###############################################################################################
# ############################ -- FLASK FUNCTIONS -- ############################

# ### Function for the server "home"
@app.route("/")
def home():
    # Return a basic html
    return app.send_static_file("test.html")

# ### Function to pull the nutrition data
@app.route("/nutrition-data", methods = ['GET'])
def nutrition_dataframe():
    # password request
    x = request.args['password']

    # check if the password is correct, and if so, return the data
    if x == "12341":
        path = data_path + os.sep + "Nutritional_values.csv"
        df = pd.read_csv(path)
        return df.to_json()
    # else, return an error message
    else:
        return "Wrong password"

# ### Function to pull the nutrition data
@app.route("/resources-data", methods = ['GET'])
def resources_dataframe():
    # password request
    x = request.args['password']

    # check if the password is correct, and if so, return the data
    if x == "12342":
        path = data_path + os.sep + "Food_production.csv"
        df = pd.read_csv(path)
        return df.to_json()
    # else, return an error message
    else:
        return "Wrong password"


###############################################################################################
# ############################ -- MAIN FUNCTIONS -- ############################
# ### Function to run the server
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


###############################################################################################
# ############################ -- TO RUN THE SERVER -- ############################
if __name__ == "__main__":
    # before running the server, ask through the terminal for a password
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", type=str,
                        help = "password to run the server", required = True)
    args = parser.parse_args()

    # if password is ok, run the server
    if args.password == "45395203B":
        main()

    # else, error message
    else:
        print("wrong password")