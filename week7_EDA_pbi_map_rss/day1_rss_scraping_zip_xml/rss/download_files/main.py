# automation.py
from shutil import move
import os

dir = os.path.dirname
sep = os.sep


# directory paths
current_dir = dir(__file__)           # directorio del archivo actual
from_dir = current_dir + sep + "from_folder" + sep        # archivos de la carpeta XX
to_folder = current_dir + sep + "to_folder" + sep         # hacia la carpeta XX

doc_file = to_folder + sep + "doc" + sep      # Apuntamos a la carpeta "to_folder/doc" -> que no existe
img_file = to_folder + sep + "image" + sep    # Lo mismo que arriba

if not os.path.exists(to_folder):    # Si no existe la carpeta /img
  os.mkdir(to_folder)  
if not os.path.exists(img_file):    # Si no existe la carpeta /img
  os.mkdir(img_file)           # Creala
if not os.path.exists(doc_file):    # Lo mismo que arriba
  os.mkdir(doc_file)
       
# category wise file types
doc_types = ('.doc', '.docx', '.txt', '.pdf', '.xls', '.ppt', '.xlsx', '.pptx')
img_types = ('.jpg', '.jpeg', '.png', '.svg', '.gif', '.tif', '.tiff')

def get_non_hidden_files_except_current_file(root_dir):
  # nos va a devolver todos los f
  # if os.path.isfile(root_dir + f)   --> si son archivos
  # and not f.startswith('.')         --> y si no empieza por pto (esos son archivos ocultos)
  return [f for f in os.listdir(root_dir) if os.path.isfile(root_dir + f) and not f.startswith('.')]

def move_files(files):
  for file in files:      # para cada archivo en la lista
    # file moved and overwritten if already exists
    if file.endswith(doc_types):        # lo mueve a la carpeta doc si termina en ".doc, .docx, etc..."
      move(from_dir + file, doc_file)
      print('file {} moved to {}'.format(file, doc_file))
    elif file.endswith(img_types):       # lo mismo con imagenes
      move(from_dir + file, img_file)
      print('file {} moved to {}'.format(file, img_file))
    else:
          print("~~~~~~~~~~~~")
          print(str(file))
          print("This file is not an image or document")

if __name__ == "__main__":
  files = get_non_hidden_files_except_current_file(from_dir)
  move_files(files)