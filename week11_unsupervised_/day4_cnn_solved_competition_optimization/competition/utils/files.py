import os

def file_exists(filepath):
    if os.path.exists(filepath):
        return True
    else:
        return False
    
# Para guardar el mejor modelo
def rename_filename(filepath, number=1):
    name = os.path.splitext(filepath)[0]
    extension = os.path.splitext(filepath)[1]

    name += "_" + str(number)
    filepath = name + extension
    # Si el modelo existe, añadele _1
    if file_exists(filepath):
        return rename_filename(filepath=filepath, number=number+1)
    else:
        return filepath