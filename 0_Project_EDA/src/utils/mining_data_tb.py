# -------------------------- LIBRARIES --------------------------
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import re
from varname import nameof

import requests
from bs4 import BeautifulSoup
import html
import lxml


def test():
    return "funciona"
# -------------------------- GENERAL FUNCTIONS --------------------------
def num_cleaning(x):
    try:
        return re.match(r'[\d]*[\.\d]*', x)[0]
    except:
        return x

def to_float(x):
    try:
        return float(x)
    except:
        return x

def mapper(data):
    try:
        data.shape[1]       # This is actually to check whether it is a DataFrame or not
        return data.applymap(num_cleaning).applymap(to_float)
    except:
        return data.map(num_cleaning).map(to_float)

def gram_to_liter(x):
    return x * 0.001

def iu_to_mcg(x):
    # This is from international units to mcg retinol
    # I'll use this function to convert vimain a units to something that I can compare with the australian recommendation for daily intake
    return x * 0.3

def key_nutrients():
    return ["protein", "water", "fiber", "vitamin_a", "thiamin", "riboflavin",
            "niacin", "vitamin_b6", "vitamin_b12", "folate", "vitamin_c", "calcium",
            "irom", "magnesium", "potassium", "sodium", "zink"]


# -------------------------- FILTERING FUNCTIONS --------------------------
# >>> 
def nutrient_selector(nutrientname, df):
    try:
        return df.sort_values(by = nutrientname, ascending = False)
    except:
        return "More than one row selected"

# >>> 
def one_filter(df, to_filter, out = True):
    
    filter_ = df.index.str.contains(to_filter)

    if out:
        return df[filter_ == False]
    return df[filter_]

# >>> 
def several_filters(df, to_filter_list, out = True):

    if out == False:
        pos_df = pd.DataFrame(columns = df.columns)

        for f_ in to_filter_list:
            pos_filter = one_filter(df, f_, out)
            pos_df = pd.concat([pos_df, pos_filter])

        return pos_df

    else:
        for f_ in to_filter_list:
            df = one_filter(df, f_, out)

        return df

# >>> 
def food_selector(foodname, df):
    return df.loc[foodname]


# -------------------------- NUTRITION DATASET FUNCTIONS --------------------------
def nutrition_prep(df):
    nutrition = df
    nutrition.set_index("name", inplace = True)

    filter_ = key_nutrients()

    nutrition = nutrition[filter_]

    nutrition = mapper(nutrition)

    nutrition["water"] = nutrition["water"].map(gram_to_liter)
    nutrition["vitamin_a"] = nutrition["vitamin_a"].map(iu_to_mcg)

    return nutrition


# -------------------------- DAILY_INTAKE FUNCTIONS --------------------------
def dailyintake_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    di_table = soup.find(id = "tbl-calc")
    di_rows = di_table.find_all("tr")

    di_dict = {}

    for row in di_rows:
        items = row.find_all("td")
        if len(items) > 1:
            di_dict[items[0].text] = items[1].text

    s = pd.Series(di_dict)

    return s

def dailyintake_prep(serie):
    serie = mapper(serie)
    serie.drop("Iodine", inplace = True)
    serie.name = nameof(serie)
    serie.index = key_nutrients()
    return serie

def foodquality(food, dailyintake):
    if len(food) == len(dailyintake):
        s = (food / dailyintake) * 100
        s = s.sort_values(ascending = False)
        s = s.reset_index()
        s.columns = ["nutrient", "%OfDailyIntake"]
        return s