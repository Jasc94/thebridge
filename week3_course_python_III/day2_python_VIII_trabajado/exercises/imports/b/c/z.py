import os
import sys

# Current file path
path = __file__

# I loop though the path all the way up to the folder from where I can access the x.py file
for i in range(3):
    path = os.path.dirname(path)

path2 = os.path.dirname(os.path.dirname(__file__))

# I append the new path that I just saved to my sys.path
sys.path.append(path)
sys.path.append(path2)

import a.x as x
import y

def f2z():
    return x.f2x()

def f1z():
    return y.f1y()

#print('f2z:', f2z())
#print('f1z:', f1z())
#print(os.path.dirname(os.path.dirname(__file__)))