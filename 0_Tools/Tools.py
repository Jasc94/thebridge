# Para notebook
def get_root_path_notebook(n):
    path = os.getcwd()
    for i in range(n):
        path = os.path.dirname(path)
    print(path)
    sys.path.append(path)

# Para .py
def get_root_path_py(n):
    path = os.getcwd()
    for i in range(n):
        path = __file__
    print(path)
    sys.path.append(path)