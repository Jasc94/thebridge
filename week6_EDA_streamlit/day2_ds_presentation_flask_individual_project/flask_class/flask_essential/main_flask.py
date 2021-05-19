from flask import Flask, request, render_template
from utils.functions import read_json
import os

# Mandatory
app = Flask(__name__)  # __name__ --> __main__  

# ---------- Flask functions ----------
@app.route("/")  # @ --> esto representa el decorador de la función
def home():
    """ Default path """
    return app.send_static_file('greet.html')

# /algo -> representa el endpoint
@app.route("/greet")
def greet():
    username = request.args.get('name')
    return render_template('index.html', name=username)


# /algo -> representa el endpoint
@app.route("/recibe-informacion")
def recibe_info():
    return [{"column1" : "0", "column2" : "8"}]


@app.route("/info")
def create_json():
    return 'Tienes que acceder al endpoint "/give_me_id" pasando por parámetro "password" con la contraseña correcta' 

@app.route('/give_me_id', methods=['GET'])
def give_id():
    x = request.args['password']
    if x == "12345":
        return request.args
    else:
        return "No es la contraseña correcta"

# ---------- Other functions ----------

def main():
    print("---------STARTING PROCESS---------")
    print(__file__)
    
    # Get the settings fullpath
    # \\ --> WINDOWS
    # / --> UNIX
    # Para ambos: os.sep
    settings_file = os.path.dirname(__file__) + os.sep + "settings.json"
    print(settings_file)
    # Load json from file
    json_readed = read_json(fullpath=settings_file)
    
    # Load variables from jsons
    # En el json tenemos toda la información sobre el servidor que vamos a utilizar
    SERVER_RUNNING = json_readed["server_running"]
    print("SERVER_RUNNING", SERVER_RUNNING)
    if SERVER_RUNNING:      # Si existe SERVER_RUNNING, ejecutame el resto
        DEBUG = json_readed["debug"]
        HOST = json_readed["host"]
        PORT_NUM = json_readed["port"]
        app.run(debug=DEBUG, host=HOST, port=PORT_NUM)
    else:
        print("Server settings.json doesn't allow to start server. " + 
            "Please, allow it to run it.")

if __name__ == "__main__":
    main()