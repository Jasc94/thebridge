"""
Siempre que veas 'pass' es un TO-DO (por hacer)

"""

"""1"""
# Llama a la función 'mi_funcion' que está en /flask/api.py. No puede dar error.
import sys, os

path_ = os.path.abspath(__file__)
dir = os.path.dirname

path = dir(path_) + os.sep + "flask"

sys.path.append(path)

import api

print(api.mi_funcion())