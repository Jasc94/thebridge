# -------------------------- LIBRARIES --------------------------
import pandas as pd
import numpy as np

import re
from varname import nameof

import requests
from bs4 import BeautifulSoup
import html
import lxml

import sys, os

dir = os.path.dirname
sys.path.append(dir(os.getcwd()))

import src.utils.mining_data_tb as md
import src.utils.folder_tb as fo


# -------------------------------- SUPPORT FUNCTIONS --------------------------------
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

def liter_to_gram(x):
    return x * 1000

###############################################################################################
# ############################ -- NUTRITION DATASET FUNCTIONS -- ############################
# -------------------------------- FILTER FUNCTIONS --------------------------------
# >>> To filter by nutrients (columns)
def nutrients_filter_1(num):
    # Key nutrients for the comparison with recommended daily intake
    daily_intake_nutrients = ["Protein (g)", "Water\n(g)", "Fiber, total dietary (g)", "Vitamin A, RAE (mcg_RAE)", "Thiamin (mg)", "Riboflavin (mg)", "Niacin (mg)", "Vitamin B-6 (mg)", "Vitamin B-12 (mcg)", "Folate, total (mcg)", "Vitamin C (mg)", "Calcium (mg)", "Iron\n(mg)", "Magnesium (mg)", "Potassium (mg)", "Sodium (mg)", "Zinc\n(mg)"]

    # Additional interesting nutrients to explore
    additional_nutrients = ["Energy (kcal)", "Total Fat (g)", "Fatty acids, total saturated (g)", "Fatty acids, total monounsaturated (g)", "Fatty acids, total polyunsaturated (g)", "Cholesterol (mg)", "Vitamin D (D2 + D3) (mcg)"]

    # For grouping and categorization
    support_columns = ["Main food description", "WWEIA Category number", "WWEIA Category description"]

    full_column_filter = support_columns + daily_intake_nutrients + additional_nutrients

    if num == 1:
        return daily_intake_nutrients
    elif num == 2:
        return additional_nutrients
    elif num == 3:
        return support_columns
    elif num == 4:
        return full_column_filter
    else:
        print("Number not allowed")

# >>> To filter by nutrients (columns) after renaming
def nutrients_filter_2(num):
    # Key nutrients for the comparison with recommended daily intake
    new_daily_intake_nutrients = ["Protein (g)", "Water (g)", "Fiber, total dietary (g)", "Vitamin A, RAE (mcg_RAE)", "Thiamin (mg)", "Riboflavin (mg)", "Niacin (mg)", "Vitamin B-6 (mg)", "Vitamin B-12 (mcg)", "Folate, total (mcg)", "Vitamin C (mg)", "Calcium (mg)", "Iron (mg)", "Magnesium (mg)", "Potassium (mg)", "Sodium (mg)", "Zinc (mg)"]

    # Additional interesting nutrients to explore
    new_additional_nutrients = ["Energy (kcal)", "Total Fat (g)", "Fatty acids, total saturated (g)", "Fatty acids, total monounsaturated (g)", "Fatty acids, total polyunsaturated (g)", "Cholesterol (mg)", "Vitamin D (D2 + D3) (mcg)"]

    # For grouping and categorization
    new_support_columns = ["Food name", "Category number", "Category name"]

    new_full_column_filter = new_support_columns + new_daily_intake_nutrients + new_additional_nutrients

    if num == 1:
        return new_daily_intake_nutrients
    elif num == 2:
        return new_additional_nutrients
    elif num == 3:
        return new_support_columns
    elif num == 4:
        return new_full_column_filter
    else:
        print("Number not allowed")

# >>> To filter by categories (rows) // They are negative as it's basically noise for the study
def negative_filters(filter_):
    # NEGATIVE FILTERS
    others = ['Formula, ready-to-feed', 'Formula, prepared from powder', 'Formula, prepared from concentrate', 'Sugar substitutes', 'Not included in a food category']
    baby_food = ['Baby food: yogurt', 'Baby food: snacks and sweets', 'Baby food: meat and dinners', ]
    desserts_and_snacks = ['Ice cream and frozen dairy desserts', 'Milk shakes and other dairy drinks', 'Cakes and pies', 'Candy not containing chocolate', 'Doughnuts, sweet rolls, pastries', 'Crackers, excludes saltines', 'Cookies and brownies', 'Biscuits, muffins, quick breads', 'Pancakes, waffles, French toast', 'Cereal bars', 'Nutrition bars', 'Saltine crackers', 'Pretzels/snack mix', 'Potato chips', 'Candy containing chocolate', 'Pancakes, waffles, French toast']
    drinks = ['Soft drinks', 'Diet soft drinks', 'Flavored or carbonated water', 'Other diet drinks', 'Beer', 'Liquor and cocktails', 'Wine', 'Nutritional beverages', 'Protein and nutritional powders', 'Sport and energy drinks', 'Diet sport and energy drinks']
    sandwiches = ['Burritos and tacos', 'Other sandwiches (single code)', 'Burgers (single code)', 'Egg/breakfast sandwiches (single code)', 'Frankfurter sandwiches (single code)', 'Frankfurter sandwiches (single code)', 'Vegetables on a sandwich']
    prepared_dishes = ['Rolls and buns', 'Egg rolls, dumplings, sushi', 'Pasta mixed dishes, excludes macaroni and cheese', 'Macaroni and cheese', 'Pizza', 'Meat mixed dishes', 'Stir-fry and soy-based sauce mixtures', 'Bean, pea, legume dishes', 'Seafood mixed dishes', 'Rice mixed dishes', 'Fried rice and lo/chow mein', 'Poultry mixed dishes']
    sauces = ['Dips, gravies, other sauces''Pasta sauces, tomato-based', 'Mustard and other condiments', 'Mayonnaise', 'Jams, syrups, toppings']
    full_negative_filter = others + baby_food + desserts_and_snacks + drinks + sandwiches + prepared_dishes + sauces

    if filter_ == 0:
        return others

    elif filter_ == 1:
        return baby_food

    elif filter_ == 2:
        return desserts_and_snacks

    elif filter_ == 3:
        return drinks

    elif filter_ == 4:
        return sandwiches

    elif filter_ == 5:
        return prepared_dishes

    elif filter_ == 6:
        return sauces

    elif filter_ == 7:
        return full_negative_filter

    else:
        return "Filter not available"

# >>> To filter by categories (rows) // They are positive because they contain the foods we want to focus on
def positive_filters(filter_):
    #POSITIVE FILTERS
    milks = ['Lamb, goat, game', 'Human milk', 'Milk, reduced fat', 'Milk, whole', 'Milk, lowfat', 'Milk, nonfat', 'Flavored milk, whole', 'Yogurt, regular', 'Yogurt, Greek']
    cheese = ['Cheese', 'Cottage/ricotta cheese']
    other_animal_products = ['Eggs and omelets', 'Butter and animal fats']
    meats = ['Ground beef', 'Cold cuts and cured meats', 'Bacon', 'Pork', 'Liver and organ meats', 'Frankfurters', 'Sausages']
    chicken = ['Turkey, duck, other poultry', 'Chicken, whole pieces', 'Chicken patties, nuggets and tenders']
    fish = ['Fish', 'Shellfish']
    milk_substitutes = ['Milk substitutes']
    beans = ['Beans, peas, legumes']
    soy_products = ['Processed soy products']
    nuts = ['Nuts and seeds']
    other_veggie_products = ['Peanut butter and jelly sandwiches (single code)', 'Oatmeal']
    animal_filter = milks + cheese + other_animal_products + meats + chicken + fish
    veggie_filter = milk_substitutes + beans + soy_products + nuts + other_veggie_products
    full_positive_filter = animal_filter + veggie_filter

    if filter_ == 0:
        return milks

    elif filter_ == 1:
        return cheese

    elif filter_ == 2:
        return other_animal_products

    elif filter_ == 3:
        return meats

    elif filter_ == 4:
        return chicken

    elif filter_ == 5:
        return fish

    elif filter_ == 6:
        return milk_substitutes

    elif filter_ == 7:
        return beans

    elif filter_ == 8:
        return soy_products

    elif filter_ == 9:
        return nuts

    elif filter_ == 10:
        return other_veggie_products

    ###
    elif filter_ == 11:
        return animal_filter

    elif filter_ == 12:
        return veggie_filter

    elif filter_ == 13:
        return full_positive_filter

    else:
        return "Filter not available" 

# >>> It uses the filters to return the filtered dataframe
def conditional(df, to_filter, negative_filter = True):
    '''
    df : dataframe to filter
    to_filter : filter that will be used
    out : if True, it will filter out and if False, it will simply filter. By default, is True.
    '''
    if negative_filter == True:
        filter_ = negative_filters(to_filter)
        return df[~df["Category name"].isin(filter_)].index

    filter_ = positive_filters(to_filter)
    return df[df["Category name"].isin(filter_)].index

# >>> It applies several filters at the time
def several_filters(df, to_filter_list, negative_filter = True):

    if negative_filter == False:
        positive_df = pd.DataFrame(columns = df.columns)

        for filter_ in to_filter_list:
            condition = conditional(df, filter_, negative_filter)
            positive_filter = df.loc[condition]
            positive_df = pd.concat([positive_df, positive_filter])

        return positive_df

    else:
        for filter_ in to_filter_list:
            condition = conditional(df, filter_, negative_filter)
            df = df.loc[condition]

        return df


# -------------------------------- DATA EXTRACTION --------------------------------
# >>> Prepares the data
def nutrition_data_prep(df):
    # Step 1: Filtering the columns I need
    df = df[nutrients_filter_1(4)]

    # Step 2: Column rename
    df.columns = nutrients_filter_2(4)

    # Step 3: New index
    df.set_index("Food name", inplace = True)

    # Step 4: Adding two extra columns
    category_2 = ["milks", "cheese", "other_animal_products", "meats", "chicken", "fish", "milk_substitutes", "beans", "soy_products", "nuts", "other_veggie_products"]

    category_3 = ["animal", "veggie"]

    df["Category 2"] = None
    df["Category 3"] = None

    for ind, val in enumerate(category_2):
        condition = conditional(df, ind, False)
        df.loc[condition, "Category 2"] = val

    for ind, val in enumerate(category_3):
        condition = conditional(df, ind + 11, False)
        df.loc[condition, "Category 3"] = val

    return df

# >>> Using all the functions together, delivers the ready-to-use dataframe
def get_nutrition_data(path, filename):
    df = pd.read_excel(path + filename, skiprows = 1)

    df = nutrition_data_prep(df)

    return df

# ###
def nutrients_stats(df):
    nutrients_list = list(df.loc[:, "Protein (g)":"Vitamin D (D2 + D3) (mcg)"].columns)
    stats = df.groupby("Category 2").agg({nutrient : np.mean for nutrient in nutrients_list})
    return stats


###############################################################################################
# ############################ -- DAILY INTAKE FUNCTIONS -- ############################
# >>> Using gender and age, pick the corresponding daily intake
def pick_daily_intake(gender, age, df):
    url = df[(df["gender"] == gender) & (df["age"] == age)]["url"].values[0]
    return url

# >>> To pull the data from the website
def daily_intake_info(url):
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

# >>> To prepare the data
def daily_intake_prep(serie):
    serie = mapper(serie)
    serie.drop("Iodine", inplace = True)
    serie.name = "Daily_Intake"
    serie.index = nutrients_filter_2(1)
    serie["Water (g)"] = liter_to_gram(serie["Water (g)"])
    return serie

# >>> Using all the functions together, delivers the ready-to-use dataframe
def get_daily_intake_data(path, filename, gender, age):
    # Put together the path and pull the data
    full_path = path + filename
    df = pd.read_csv(full_path)

    # Take the corresponding url according to gender and age
    url = pick_daily_intake(gender, age, df)

    # Take the info from the url and put it in a Serie
    serie = daily_intake_info(url)

    # Data cleaning and processing -> final output: ready-to-use Serie
    data = daily_intake_prep(serie)

    return data

# >>> To compare foods with the recommended daily intake
def foodquality(dailyintake, foods):
    df = pd.DataFrame(dailyintake)
    count = 1
    for food in foods:
        if len(food) == len(dailyintake):
            df = pd.merge(df, food, how = "outer", left_index = True, right_index = True)
            df["%OfDI_" + food.name] = (food / dailyintake) * 100
            count += 1

    return df.T

# >>> To compare foods with the recommended daily intake
def transformation_for_barplot(quality_df):
    count = 2
    list_of_series = []

    while count < len(quality_df):
        food_values = quality_df.iloc[count]
        food_values.name = "Values"

        food_name = pd.Series([quality_df.iloc[count].name for x in range(len(food_values))], index = food_values.index, name = "Item")

        food = pd.concat([food_values, food_name], axis = 1)
        list_of_series.append(food)

        count += 2

    barplot_df = pd.concat(list_of_series)
    return barplot_df

###############################################################################################
# ############################ -- RESOURCES DATASET FUNCTIONS -- ############################
# >>> To prepare the land use data
def land_use_prep(path):

    # I pull the data and do some manipulation
    land_use_kcal = pd.read_csv(path + "/land-use-kcal-poore.csv").drop(["Code", "Year"], axis = 1)
    land_use_kg = pd.read_csv(path + "/land-use-per-kg-poore.csv").drop(["Code", "Year"], axis = 1)
    land_use_protein = pd.read_csv(path + "/land-use-protein-poore.csv").drop(["Code", "Year"], axis = 1)

    # Merge the data into one dataframe
    land_use = pd.merge(land_use_kcal, land_use_kg, how = "outer", on = "Entity")
    land_use = pd.merge(land_use, land_use_protein, how = "outer", on = "Entity")

    # Rename the columns
    land_use.columns = ["Food", "Land use per 1000kcal", "Land use per kg", "Land use per 100g protein"]

    return land_use

# >>> To prepare the water use data
def water_use_prep(path):

    # I pull the data and do some manipulation
    water_use_kcal = pd.read_csv(path + "/freshwater-withdrawals-per-kcal.csv").drop(["Code", "Year"], axis = 1)
    water_use_kg = pd.read_csv(path + "/freshwater-withdrawals-per-kg.csv").drop(["Code", "Year"], axis = 1)
    water_use_protein = pd.read_csv(path + "/freshwater-withdrawals-per-protein.csv").drop(["Code", "Year"], axis = 1)

    # Merge the data into one dataframe
    water_use = pd.merge(water_use_kcal, water_use_kg, how = "outer", on = "Entity")
    water_use = pd.merge(water_use, water_use_protein, how = "outer", on = "Entity")

    # Rename the columns
    water_use.columns = ["Food", "Freswater withdrawls per 1000kcal", "Freswater withdrawls per kg", "Freswater withdrawls per 100g protein"]
    
    return water_use

# >>> To prepare thegeneral data (emissions)
def general_prep(path):
    general = pd.read_csv(path + "Food_production.csv")
    general = general[["Food product", "Total_emissions"]]
    general.columns = ["Food", "Total_emissions"]

    return general

# >>> Join all the data in one dataframe
def join_resources(path1, path2):
    # Cleaned general data
    general = general_prep(path1)

    # Cleaned land_use and water_use data
    land_use = land_use_prep(path2)
    water_use = water_use_prep(path2)

    # Merge everything into sources
    resources = pd.merge(general, land_use, how = "outer", on = "Food")
    resources = pd.merge(resources, water_use, how = "outer", on = "Food")

    resources = resources.set_index("Food")
    return resources

# >>> 
def combine_data(column1, column2, df):
    # To store the new values of combining both columns
    new_values = []

    # Iterate through the length of the column1 (both columns should have the same length)
    for i in range(len(df.loc[column1])):
        # If column1 is nan, return the value of the other column
        if np.isnan(df.loc[column1][i]):
            new_values.append(df.loc[column2][i])
        # else, keep the one from column 1
        else:
            new_values.append(df.loc[column1][i])

    # Join the values together with an index (should be the same for both columns)
    # and transpose it
    df = pd.DataFrame(new_values, index = df.loc[column1].index, columns = [column1 + "_"])
    return df.T

# >>> 
def get_resources_data(path1, path2):
    df = join_resources(path1, path2)

    tofu = combine_data("Tofu", "Tofu (soybeans)", df)
    wheat = combine_data("Wheat & Rye", "Wheat & Rye (Bread)", df)
    maize = combine_data("Maize", "Maize (Meal)", df)
    barley = combine_data("Barley", "Barley (Beer)", df)

    df = df.append([tofu, wheat, maize, barley])
    df = df.drop(["Tofu", "Tofu (soybeans)",
                "Wheat & Rye", "Wheat & Rye (Bread)",
                "Maize", "Maize (Meal)",
                "Barley", "Barley (Beer)",])

    df["Origin"] = ['plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based',
       'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based',
       'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'plant based', 'animal based',
       'animal based', 'animal based', 'animal based', 'animal based', 'animal based', 'animal based', 'animal based', 'animal based', 'animal based',
       'animal based', 'animal based', 'animal based', 'animal based', 'animal based', 'animal based']

    return df

# >>> 
def resources_stats(df, resources_list):
    stats = df.groupby("Origin").agg({resource : (np.mean, np.median) for resource in resources_list})
    
    return stats

# >>> 
def stats_to_plot(stats):
    to_plot = stats.unstack()
    to_plot = to_plot.reset_index()
    to_plot.columns = ["Resource", "Mean_median", "Origin", "Values"]
    return to_plot