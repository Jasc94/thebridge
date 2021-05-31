import os, sys

# Para notebook
def get_root_path_notebook(n):
    '''
    This function is to find the folder up n levels and append it to the sys.path. It is for jupyter notebooks.

    args:
    n: how many levels you want to go up in the path
    '''
    path = os.getcwd()
    for i in range(n):
        path = os.path.dirname(path)
    print(path)
    sys.path.append(path)

# Para .py
def get_root_path_py(n):
    '''
    This function is to find the folder up n levels and append it to the sys.path. It is for .py files.

    args:
    n: how many levels you want to go up in the path
    '''
    path = os.getcwd()
    for i in range(n):
        path = __file__
    print(path)
    sys.path.append(path)