"""

Crea una API flask con un solo endpoint que muestre por pantalla el json 'googleplaystore.json'
de la carpeta /data. En resumen, el endpoint tiene que leer el fichero 'googleplaystore.json' y retornarlo.

Además, este fichero contiene otra función que está fuera de la funcionalidad de la API flask

"""

from flask import Flask, request, render_template, Response
import sys, os
import json

# Adding path up
path = os.path.abspath(__file__)
dir = os.path.dirname

for i in range(3): path = dir(path)

# Flask object
app = Flask(__name__)

""" 1: No es una función de flask"""
def mi_funcion():
    """
    TODO - Esta función ha de llamar a la función 'funcion_flask_1' que está en /utils/flask_functions.py y
    mostrar por pantalla lo que retorne esa función. 
    """
    route = os.path.abspath(__file__)
    for i in range(2):
        route = os.path.dirname(route)
    sys.path.append(route)

    from utils.flask_functions import funcion_flask_1

    return funcion_flask_1()

def flask_settings():
    flask_path = path + "/config/flask_settings.json"

    with open(flask_path, "r") as json_file:
        read_json = json.load(json_file)

    return read_json


@app.route("/")
def home():
    googleplaystore_path = path + "/data/googleplaystore.json"

    with open(googleplaystore_path, "r") as json_file:
        read_json = json.load(json_file)

    return read_json

###############################################################################################
# ############################ -- MAIN FUNCTIONS -- ############################
# ### Function to run the server
def main():
    print("--- STARTING PROCESS ---")
    print(__file__)

    settings_file = path + "/config/flask_settings.json"
    print(settings_file)

    read_json = flask_settings()

    SERVER_RUNNING = read_json["server_running"]
    print("SERVER_RUNNING", SERVER_RUNNING)

    if SERVER_RUNNING:
        DEBUG = read_json["debug"]
        HOST = read_json["host"]
        PORT_NUM = read_json["port"]

        app.run(debug = DEBUG, host = HOST, port = PORT_NUM)

    else:
        print("Server settings.json doesn't allow to start server. " + 
            "Please, allow it to run it.")


""" PARTE PURA DE FLASK """
if __name__ == '__main__':
    """ Todo lo que está aquí debajo tiene que ver con la funcionalidad del flask """
    
    """2"""
    main()