import sys, os

def path_to_folder(up, folder = ""):
    # to better use the function
    dir = os.path.dirname

    # I start the way up
    path_up = dir(__file__)
    # Loop "up" times to reach the main folder
    for i in range(up): path_up = dir(path_up)

    # go down to the folder I want to pull the data from
    if folder:
        path_down = path_up + os.sep + folder + os.sep
    else:
        path_down = path_up + os.sep

    # return the path
    return path_down