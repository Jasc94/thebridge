import json

def read_json(fullpath):
    with open(fullpath, "r") as json_file:
        json_read = json.load(json_file)

    return json_read