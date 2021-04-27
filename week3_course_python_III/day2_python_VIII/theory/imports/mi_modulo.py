def suma_2(a, b):
    return a + b

def resta_2(a, b):
    return a - b

x = 2

# os.getcwd() NO da la ruta en la que está el archivo para los .py
# En el caso de los archivos .py, tenemos que usar:
print('\n')
print(__file__)
print('\n')

# Resumen
# En archivos '.py' --> utilizamos '__file__'
# En archivos '.ipynb' --> utilizamos 'os.getcwd()'