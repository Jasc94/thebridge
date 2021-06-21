import numpy as np
import pandas as pd

import urllib.request
from PIL import Image


sample = pd.read_csv("sample_submission.csv")

def chequeator(df_to_submit):
    """
    Esta función se asegura de que tu submission tenga la forma requerida por Kaggle.
    
    Si es así, se guardará el dataframe en un `csv` y estará listo para subir a Kaggle.
    
    Si no, LEE EL MENSAJE Y HAZLE CASO.
    
    Si aún no:
    - apaga tu ordenador, 
    - date una vuelta, 
    - enciendelo otra vez, 
    - abre este notebook y 
    - leelo todo de nuevo. 
    Todos nos merecemos una segunda oportunidad. También tú.
    """
    if df_to_submit.shape == sample.shape:
        if df_to_submit.columns.all() == sample.columns.all():
            if df_to_submit.id.all() == sample.id.all():
                print("You're ready to submit!")
                df_to_submit.to_csv("submission.csv", index = False) #muy importante el index = False
                #urllib.request.urlretrieve("https://i.kym-cdn.com/photos/images/facebook/000/747/556/27a.jpg", "gfg.png")     
                #img = Image.open("gfg.png")
                #img.show()   
            else:
                print("Check the ids and try again")
        else:
            print("Check the names of the columns and try again")
    else:
        print("Check the number of rows and/or columns and try again")
        print("\nMensaje secreto de Clara: No me puedo creer que después de todo este notebook hayas hecho algún cambio en las filas de `diamonds_test.csv`. Lloro.")


def ordinal_encoder(df):
    cut_dict = {
    "Fair" : 1,
    "Good" : 2,
    "Very Good" : 3,
    "Premium" : 4,
    "Ideal" : 5
    }

    clarity_dict = {
        "I1" : 1,
        "SI2" : 2,
        "SI1" : 3,
        "VS2" : 4,
        "VS1" : 5,
        "VVS2" : 6,
        "VVS1" : 7,
        "IF" : 8
    }

    # Create the columns in the df for them
    df["cut_encoded"] = df.cut.map(cut_dict)
    df["clarity_encoded"] = df.clarity.map(clarity_dict)

    return df


def nominal_encoder(df):
    df = pd.get_dummies(df, prefix = ["color"], columns = ["color"])

    return df


def outliers_remover(df):
    df = df[(df["depth"] > 45) & (df["depth"] < 75)]
    df = df[(df["table"] > 45) & (df["table"] < 90)]
    df = df[df["x"] != 0]
    df = df[(df["y"] > 0) & (df["y"] < 10)]
    df = df[(df["z"] > 2) & (df["z"] < 7)]

    return df

def variables_split(df, columns_to_drop = [], y = True):

    if y:
        columns_to_drop = columns_to_drop + ["price"]
        X = df.drop(columns_to_drop, axis = 1)
        y = df["price"]

        return X, y

    X = df.drop(columns_to_drop, axis = 1)
    return X