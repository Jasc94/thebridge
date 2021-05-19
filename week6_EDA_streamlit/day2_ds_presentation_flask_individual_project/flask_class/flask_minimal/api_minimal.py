from flask import Flask, flash, request, render_template, redirect, url_for
import pandas as pd
import os
import json

# Apuntamos a la carpeta static
UPLOAD_FOLDER = os.sep + "static" + os.sep
# Para destinar lo que vamos a crear a una clase Flask
# __file__ --> ruta al fichero
app = Flask(__name__)       # En este caso es sinónimo de poner __main__
# La carpeta donde se va a subir el contenido, es esta carpeta (static)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'hellohello'


# Creamos un diccionario con tres claves
options = {"Genre_list":["hola", "adios"],
"Platform_list":[1,2,3,4,5,6],
"Publisher_list":['Clara', 'Borja', 'Gabriel']}


# Vamos a crear dos funciones que van a ser accesibles desde la API
@app.route("/")
def home():
    # render_template le está pasando al fichero upload las opciones a seleccionar, que ya definimos arriba con el diccionario options
    return render_template("upload.html", 
                           Genre_list = options["Genre_list"],
                           Platform_list= options["Platform_list"], 
                           Publisher_list= options["Publisher_list"])
    
# Estoy usando un POST para publicar el contenido de la aplicación
# GET para recoger la información que introduce el usuario
@app.route("/upload_form", methods = ['POST', 'GET'])
def upload_form():
    # Si lo que hacemos es un "POST" -> con propósito de mostrar información
    if request.method == 'POST':
        genre_res = request.form['Genre']       # Saco esta info a través de Genre, porque lo estoy guardando en el HTML con este nombre
        platform_res= request.form['Platform']
        publisher_res = request.form['Publisher']
        # Aquí concateno toda la info que saqué del formulario
        all_returned = str(genre_res) + str(platform_res) + str(publisher_res)
        # La función retorna un diccionario transformado a json
        return json.dumps({"genre": genre_res,
                            "platform": platform_res,
                            "publisher": publisher_res,
                            "all_returned": all_returned})


if __name__ == '__main__':
    # host='127.0.0.1' --> No permite recibir llamadas desde el exterior
    # host='0.0.0.0' --> Permite recibir llamadas desde el exterior
    # si 0.0.0.0 no funciona externamente desde la IP privada de tu PC
    # es que tu ordenador o del dispositivo desde el que se accede 
    # tiene bloqueada la conexión (antivirus / firewall)
    app.run(host='0.0.0.0', port=1991, debug=True)

    # 0.0.0.0 hace el ordenador público
    # el "port" es un número totalmente arbitrario entre 10000 y 50000 y pico