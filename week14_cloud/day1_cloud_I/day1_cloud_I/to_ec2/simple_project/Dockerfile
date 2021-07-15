# Se descarga un linux mínimo con la versión de python especificada
FROM python:3.7

# Copia todo lo que ahaya a la misma altura de Dockerfile a una carpeta /app
COPY . /app

# Muevo el lugar de trabajo a la carpeta /app
WORKDIR /app

#RUN pip install -r requirements.txt
# This run 
# Instala todas las librerías que encuentra en el archivo requirements.txt dentro del contenedor
# La segunda parte del comando (después de |) hace que vaya instalando las librerías una a una por si alguna da error
# Y gestiona mejor la memoria cache
RUN cat requirements.txt | xargs -n 1 pip install --no-cache-dir

# Puerto de flask
EXPOSE 6060:6060
# Puerto de streamlit
EXPOSE 8501:8501


# No pueden haber dos CMDs en un Dockerfile
#RUN python3 ./src/api/server.py -x Nombre &
#CMD ["python3","./src/api/server.py", "-x", "Nombre"]
#CMD ["streamlit","run", "./src/dashboard/app.py"]
# Para ejecutar server.py utilizando python3
CMD ["python3","./src/api/server.py"]               