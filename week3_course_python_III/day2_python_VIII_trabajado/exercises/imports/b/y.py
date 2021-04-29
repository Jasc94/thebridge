import os
import sys

# Current file path
path = __file__

# I loop though the path all the way up to the folder from where I can access the x.py file
for i in range(2):
    path = os.path.dirname(path)

# I append the new path that I just saved to my sys.path
sys.path.append(path)

# I access the x.py file
import a.x as x

def f1y():
    return x.f1x()

def f2z():
    return x.f2x()

def f1z():
    return f1y()

#print('f1y:', f1y())
#print('f2z:', f2z())
#print('f1z:', f1z())

# Esta condición hace que solo cuando ejecutemos lo que está dentro de la condición desde el mismo archivo, se ejecute el programa
# Si tratamos de ejecutar esto desde otro archivo (importanto por ejemplo), esto no se va a mostrar
if __name__ == '__main__':
    print('Esto está debajo de la condición __main__')
    f1y()