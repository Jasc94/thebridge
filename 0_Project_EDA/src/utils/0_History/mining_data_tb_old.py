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

def resources_all_data():
    co2_per_kg = ["Land use change", "Animal Feed", "Farm", "Processing", "Transport", "Packging", "Retail", "Total_emissions"]
    return co2_per_kg

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
# >>> 
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
# >>> 
def pick_di(gender, age, df):
    url = df[(df["gender"] == gender) & (df["age"] == age)]["url"].values[0]
    return url

# >>> 
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

# >>> 
def dailyintake_prep(serie):
    serie = mapper(serie)
    serie.drop("Iodine", inplace = True)
    serie.name = "Daily_Intake"
    serie.index = key_nutrients()
    return serie

# >>> 
def foodquality(dailyintake, foods):
    df = pd.DataFrame(dailyintake)
    count = 1
    for food in foods:
        if len(food) == len(dailyintake):
            df = pd.merge(df, food, how = "outer", left_index = True, right_index = True)
            df["%OfDailyIntake_" + str(count)] = (food / dailyintake) * 100
            count += 1

    return df.T

# -------------------------- RESOURCES DATASET FUNCTIONS --------------------------
# >>> 
def landuse_prep(path):

    # I pull the data and do some manipulation
    land_use_kcal = pd.read_csv(path + "/land-use-kcal-poore.csv").drop(["Code", "Year"], axis = 1)
    land_use_kg = pd.read_csv(path + "/land-use-per-kg-poore.csv").drop(["Code", "Year"], axis = 1)
    land_use_protein = pd.read_csv(path + "/land-use-protein-poore.csv").drop(["Code", "Year"], axis = 1)

    # Merge the data into one dataframe
    land_use = pd.merge(land_use_kcal, land_use_kg, how = "outer", on = "Entity")
    land_use = pd.merge(land_use, land_use_protein, how = "outer", on = "Entity")

    # Rename the columns
    land_use.columns = ["Entity", "Land use per 1000kcal", "Land use per kg", "Land use per 100g protein"]

    return land_use

# >>> 
def wateruse_prep(path):

    # I pull the data and do some manipulation
    water_use_kcal = pd.read_csv(path + "/freshwater-withdrawals-per-kcal.csv").drop(["Code", "Year"], axis = 1)
    water_use_kg = pd.read_csv(path + "/freshwater-withdrawals-per-kg.csv").drop(["Code", "Year"], axis = 1)
    water_use_protein = pd.read_csv(path + "/freshwater-withdrawals-per-protein.csv").drop(["Code", "Year"], axis = 1)

    # Merge the data into one dataframe
    water_use = pd.merge(water_use_kcal, water_use_kg, how = "outer", on = "Entity")
    water_use = pd.merge(water_use, water_use_protein, how = "outer", on = "Entity")

    # Rename the columns
    water_use.columns = ["Entity", "Freswater withdrawls per 1000kcal", "Freswater withdrawls per kg", "Freswater withdrawls per 100g protein"]
    
    return water_use

# >>> 
def general_prep(path):
    general = pd.read_csv(path + "/Food_production.csv")
    general = general[["Food product", "Total_emissions"]]
    general.columns = ["Entity", "Total_emissions"]

    return general

# >>> 
def join_resources(path1, path2):
    # Cleaned general data
    general = general_prep(path1)

    # Cleaned land_use and water_use data
    land_use = landuse_prep(path2)
    water_use = wateruse_prep(path2)

    # Merge everything into sources
    resources = pd.merge(general, land_use, how = "outer", on = "Entity")
    resources = pd.merge(resources, water_use, how = "outer", on = "Entity")

    resources = resources.set_index("Entity")
    return resources