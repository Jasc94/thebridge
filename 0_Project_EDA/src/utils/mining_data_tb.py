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

import src.utils.folder_tb as fo


###############################################################################################
# ############################ -- GENERIC FUNCTIONS -- ############################
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

# ### Converts grams into liters
def gram_to_liter(x):
    return x * 0.001

# ### Convers liters into grams
def liter_to_gram(x):
    return x * 1000


###############################################################################################
# ############################ -- NUTRITION DATASET FUNCTIONS -- ############################

# -------------------------------- FILTERING FUNCTIONS --------------------------------
# ### To filter the RAW dataframe by nutrients (columns)
def nutrients_filter_1(num):
    '''
    This function takes the raw dataframe and filters the columns leaving the ones that we need. The filtering can be done in 4 levels:
    1 - columns required to compare with the recommended daily intake
    2 - some additional interesting nutrients: mainly fats, carbs, etc...
    3 - support columns, such as food description, food category, etc..
    4 - full filter

    args: num -> number between 1 and 4
    '''
    # Key nutrients for the comparison with recommended daily intake
    daily_intake_nutrients = ["Protein (g)", "Water\n(g)", "Fiber, total dietary (g)", "Vitamin A, RAE (mcg_RAE)", "Thiamin (mg)", "Riboflavin (mg)", "Niacin (mg)", "Vitamin B-6 (mg)", "Vitamin B-12 (mcg)", "Folate, total (mcg)", "Vitamin C (mg)", "Calcium (mg)", "Iron\n(mg)", "Magnesium (mg)", "Potassium (mg)", "Sodium (mg)", "Zinc\n(mg)"]

    # Additional interesting nutrients to explore
    additional_nutrients = ["Energy (kcal)", "Total Fat (g)", "Fatty acids, total saturated (g)", "Fatty acids, total monounsaturated (g)", "Fatty acids, total polyunsaturated (g)", "Cholesterol (mg)", "Vitamin D (D2 + D3) (mcg)", "Carbohydrate (g)"]

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

# ### To filter the CLEAN dataframe by nutrients (columns)
def nutrients_filter_2(num):
    '''
    This function is exactly the same, but with the final column names.
    It'll be used for column renaming and after that for filtering purposes.

    1 - columns required to compare with the recommended daily intake
    2 - some additional interesting nutrients: mainly fats, carbs, etc...
    3 - support columns, such as food description, food category, etc..
    4 - full filter

    args: num -> number between 1 and 4
    '''
    # Key nutrients for the comparison with recommended daily intake
    new_daily_intake_nutrients = ["Protein (g)", "Water (g)", "Fiber, total dietary (g)", "Vitamin A, RAE (mcg_RAE)", "Thiamin (mg)", "Riboflavin (mg)", "Niacin (mg)", "Vitamin B-6 (mg)", "Vitamin B-12 (mcg)", "Folate, total (mcg)", "Vitamin C (mg)", "Calcium (mg)", "Iron (mg)", "Magnesium (mg)", "Potassium (mg)", "Sodium (mg)", "Zinc (mg)"]

    # Additional interesting nutrients to explore
    new_additional_nutrients = ["Energy (kcal)", "Total Fat (g)", "Fatty acids, total saturated (g)", "Fatty acids, total monounsaturated (g)", "Fatty acids, total polyunsaturated (g)", "Cholesterol (mg)", "Vitamin D (D2 + D3) (mcg)", "Carbohydrate (g)"]

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

# ### To filter by categories (rows) // They are negative as it's basically noise for the study
def negative_filters(filter_):
    '''
    This function will return columns names as a list, This will later on help us to filter out food categories in the nutrition dataframe. The purpose is to take out those foods we are not interested in analyzing, such as ice creams, pizzas, etc...
    0 - 'Formula, ready-to-feed', 'Formula, prepared from powder', 'Formula, prepared from concentrate', 'Sugar substitutes', 'Not included in a food category'
    1 - 'Baby food: yogurt', 'Baby food: snacks and sweets', 'Baby food: meat and dinners'
    2 - 'Ice cream and frozen dairy desserts', 'Milk shakes and other dairy drinks', 'Cakes and pies', 'Candy not containing chocolate', 'Doughnuts, sweet rolls, pastries', 'Crackers, excludes saltines', 'Cookies and brownies', 'Biscuits, muffins, quick breads', 'Pancakes, waffles, French toast', 'Cereal bars', 'Nutrition bars', 'Saltine crackers', 'Pretzels/snack mix', 'Potato chips', 'Candy containing chocolate', 'Pancakes, waffles, French toast'
    3 - 'Soft drinks', 'Diet soft drinks', 'Flavored or carbonated water', 'Other diet drinks', 'Beer', 'Liquor and cocktails', 'Wine', 'Nutritional beverages', 'Protein and nutritional powders', 'Sport and energy drinks', 'Diet sport and energy drinks'
    4 - 'Burritos and tacos', 'Other sandwiches (single code)', 'Burgers (single code)', 'Egg/breakfast sandwiches (single code)', 'Frankfurter sandwiches (single code)', 'Frankfurter sandwiches (single code)', 'Vegetables on a sandwich'
    5 - 'Rolls and buns', 'Egg rolls, dumplings, sushi', 'Pasta mixed dishes, excludes macaroni and cheese', 'Macaroni and cheese', 'Pizza', 'Meat mixed dishes', 'Stir-fry and soy-based sauce mixtures', 'Bean, pea, legume dishes', 'Seafood mixed dishes', 'Rice mixed dishes', 'Fried rice and lo/chow mein', 'Poultry mixed dishes'
    6 - 'Dips, gravies, other sauces''Pasta sauces, tomato-based', 'Mustard and other condiments', 'Mayonnaise', 'Jams, syrups, toppings'
    7 - full filter

    args: num -> number between 0 and 7
    '''
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

# ### To filter by categories (rows) // They are positive because they contain the foods we want to focus on
def positive_filters(filter_):
    '''
    This function will return columns names as a list, This will later on help us to filter food categories in the nutrition dataframe. The purpose is to take those foods we are interested in analyzing, such as meats, fish, soy products etc...
    0 - 'Human milk', 'Milk, reduced fat', 'Milk, whole', 'Milk, lowfat', 'Milk, nonfat', 'Flavored milk, whole', 'Yogurt, regular', 'Yogurt, Greek'
    1 - 'Cheese', 'Cottage/ricotta cheese'
    2 - 'Eggs and omelets', 'Butter and animal fats'
    3 - 'Lamb, goat, game', 'Ground beef', 'Cold cuts and cured meats', 'Bacon', 'Pork', 'Liver and organ meats', 'Frankfurters', 'Sausages'
    4 - 'Turkey, duck, other poultry', 'Chicken, whole pieces', 'Chicken patties, nuggets and tenders'
    5 - 'Fish', 'Shellfish'
    6 - 'Milk substitutes'
    7 - 'Beans, peas, legumes'
    8 - 'Processed soy products'
    9 - 'Nuts and seeds'
    10 - 'Peanut butter and jelly sandwiches (single code)', 'Oatmeal'
    11 - animal_filter
    12 - veggie_filter
    13 - full_positive_filter

    args: num -> number between 0 and 13
    '''
    #POSITIVE FILTERS
    milks = ['Human milk', 'Milk, reduced fat', 'Milk, whole', 'Milk, lowfat', 'Milk, nonfat', 'Flavored milk, whole', 'Yogurt, regular', 'Yogurt, Greek']
    cheese = ['Cheese', 'Cottage/ricotta cheese']
    other_animal_products = ['Eggs and omelets', 'Butter and animal fats']
    meats = ['Lamb, goat, game', 'Ground beef', 'Cold cuts and cured meats', 'Bacon', 'Pork', 'Liver and organ meats', 'Frankfurters', 'Sausages']
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

# ### It uses the filters to return the filtered dataframe
def conditional(df, to_filter, negative_filter = True):
    '''
    This function will make use of the filters (either positive_fitler or negative_filter) to filter the rows of the dataframe according to the Category Name.
    It only accepts one filter at the time.

    df : dataframe to filter
    to_filter : filter that will be used
    negative_filter : if True, it will filter out and if False, it will simply filter. By default, is True.
    '''
    if negative_filter == True:
        filter_ = negative_filters(to_filter)
        return df[~df["Category name"].isin(filter_)].index

    filter_ = positive_filters(to_filter)
    return df[df["Category name"].isin(filter_)].index

# ### It applies several filters at the time
def several_filters(df, to_filter_list, negative_filter = True):
    '''
    This function makes use of the conditional function to filter the dataframe by one or more filters at the same time.

    df : dataframe to filter
    to_filter : filter that will be used
    negative_filter : if True, it will filter out and if False, it will simply filter. By default, is True.
    '''

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

# ### This function allows us to filter the columns of the dataframe by nutrient
def nutrient_selector(nutrientname, df):
    '''
    This function allows us to filter the columns of the dataframe by nutrient.

    args:
    nutrientname : nutrient to filter on
    df : dataframe to apply the filter to
    '''
    try:
        columns = ["Category name", "Category 2", "Category 3", nutrientname]
        return df[columns].sort_values(by = nutrientname, ascending = False)
    except:
        return "More than one row selected"

# -------------------------------- DATA EXTRACTION --------------------------------
# ### Prepares the data
def nutrition_data_prep(df):
    '''
    This function prepares the dataframe by fitlering the columns we need, renaming them, and adding two extra categories for better analysis.
    
    args: df -> dataframe
    '''
    # Step 1: Filtering the columns I need
    df = df[nutrients_filter_1(4)]

    # Step 2: Column rename
    df.columns = nutrients_filter_2(4)

    # Step 3: New index
    df.set_index("Food name", inplace = True)

    # Step 4: Adding two extra columns
    category_2 = ["milks", "cheese", "other_animal_products", "meats", "chicken", "fish", "milk_substitutes", "beans", "soy_products", "nuts", "other_veggie_products"]

    category_3 = ["animal", "veggie"]

    df["Category 2"] = "_others"
    df["Category 3"] = "_others"

    for ind, val in enumerate(category_2):
        condition = conditional(df, ind, False)
        df.loc[condition, "Category 2"] = val

    for ind, val in enumerate(category_3):
        condition = conditional(df, ind + 11, False)
        df.loc[condition, "Category 3"] = val

    return df

# ### Using all the functions together, delivers the ready-to-use dataframe
def get_nutrition_data(path, filename):
    '''
    Making use of the nutrition_data_prep function, this function takes the file path and returns the cleaned and transformed dataframe.

    args :
    path -> file path
    filename -> filename (end of the path)
    '''
    df = pd.read_excel(path + filename, skiprows = 1)

    df = nutrition_data_prep(df)

    return df

# ### To calculate center measures of the dataframe
def nutrients_stats(df):
    '''
    This function groups the dataframe by "Category 2" and calculates the mean of the groups.

    args : df -> dataframe
    '''
    nutrients_list = list(df.loc[:, "Protein (g)":"Carbohydrate (g)"].columns)
    stats = df.groupby("Category 2").agg({nutrient : np.mean for nutrient in nutrients_list})
    return stats


###############################################################################################
# ############################ -- DAILY INTAKE FUNCTIONS -- ############################
# ### Using gender and age, pick the corresponding daily intake
def pick_daily_intake(gender, age, df):
    '''
    The function goes to the daily intake csv file, where all the links are stored and with the given parameters, returns the corresponding url.

    args :
    gender -> male / female
    age -> multiple of 10, between 20 and 70
    df -> dataframe with the urls
    '''
    url = df[(df["gender"] == gender) & (df["age"] == age)]["url"].values[0]
    return url

# ### To pull the data from the website
def daily_intake_info(url):
    '''
    This function takes the url (return by pick_daily_intake) and pulls the daily intake data from it. It returns a pandas Series

    args :
    url -> url where daily intake data is stored
    '''
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

# ### To prepare the data
def daily_intake_prep(serie):
    '''
    This function cleans the data pull from the url and organize it in a way that we can later use it for comparisons. It returns a pandas Series.

    args :
    serie : pandas Series
    '''
    serie = mapper(serie)
    serie.drop("Iodine", inplace = True)
    serie.name = "Daily_Intake"
    serie.index = nutrients_filter_2(1)
    serie["Water (g)"] = liter_to_gram(serie["Water (g)"])
    return serie

# ### Using all the functions together, delivers the ready-to-use dataframe
def get_daily_intake_data(gender, age, df):
    '''
    This function makes will return the daily intake data for a given gender and age, by calling other functions to clean the daily intake data.

    args :
    gender -> male/female
    age -> multiple of 10, between 20 adn 70
    df -> dataframe where links are stored
    '''
    try:
        # Take the corresponding url according to gender and age
        url = pick_daily_intake(gender, age, df)

        # Take the info from the url and put it in a Serie
        serie = daily_intake_info(url)

        # Data cleaning and processing -> final output: ready-to-use Serie
        data = daily_intake_prep(serie)

        return data

    except:
        return "Out of index"


# ### To compare foods with the recommended daily intake
def foodquality(dailyintake, foods):
    '''
    This function will take the given foods and compared them one by one with the given daily intake. It returns a dataframe

    args:
    dailyintake -> dailyintake serie
    foods -> list of food series to compare with the daily intake one
    '''
    df = pd.DataFrame(dailyintake)
    count = 1
    for food in foods:
        if len(food) == len(dailyintake):
            df = pd.merge(df, food, how = "outer", left_index = True, right_index = True)
            df["%OfDI_" + food.name] = (food / dailyintake) * 100
            count += 1

    return df.T

# ### To compare foods with the recommended daily intake
def transformation_for_barplot(quality_df):
    '''
    This function takes the dataframe resulting from foodquality and return a new one ready-to-plot for barplots.

    args : quality_df -> dataframe resulting from foodquality function.
    '''
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

# ### This function makes a full comparison: daily intake, carbs & fats, cholesterol and energy
def full_comparison(daily_intake, df, foods):
    '''
    This function makes following comparison between foods: vs daily intake, fats & carbs, cholesterol and energy.

    args : 
    daily_intake -> daily intake serie with the cleaned data
    df -> dataframe where the foods are
    foods -> list of food names to compare with the daily intake, and then do the other comparisons. They should be in the dataframe.
    '''
    ### Filter the data for later use
    # For daily intake
    filter_di = nutrients_filter_2(1)

    # For the rest: fats + carbs, cholesterol and energy
    filter_fats_calories = nutrients_filter_2(2)

    filter_fats = [filter_fats_calories[-1]] + filter_fats_calories[1:5]
    filter_cholesterol = filter_fats_calories[-2]
    filter_energy = filter_fats_calories[0]

    ### Daily intake comparison
    stats_di = df[filter_di]

    food_series = [df.loc[food][filter_di] for food in foods]

    comparison_di = foodquality(daily_intake, food_series)
    comparison_di = comparison_di.iloc[list(range(2, len(food_series) * 2 + 2, 2))]
    comparison_di = comparison_di.unstack().reset_index()
    comparison_di.columns = ["Nutrient", "%OfDI", "Values"]

    # Fats comparison
    stats_fats = df[filter_fats]
    comparison_fats = stats_fats.loc[foods]
    comparison_fats = comparison_fats.unstack()
    comparison_fats = comparison_fats.reset_index()
    comparison_fats.columns = ["Nutrient", "Food group", "Values"]

    # Cholesterol comparison
    comparison_cholesterol = df[filter_cholesterol]
    comparison_cholesterol = comparison_cholesterol.loc[foods]
    comparison_cholesterol = comparison_cholesterol.reset_index()
    comparison_cholesterol.columns = ["Food group", "Values"]

    # Kcal comparison
    comparison_energy = df[filter_energy]
    comparison_energy = comparison_energy.loc[foods]
    comparison_energy = comparison_energy.reset_index()
    comparison_energy.columns = ["Food group", "Values"]

    return comparison_di, comparison_fats, comparison_cholesterol, comparison_energy

###############################################################################################
# ############################ -- RESOURCES DATASET FUNCTIONS -- ############################
# ### To prepare the land use data
def land_use_prep(path):
    '''
    This function follows the path and pulls the land use data from the different files and then merges it. It returns a dataframe.

    args : path -> path to folder with the land use files
    '''

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

# ### To prepare the water use data
def water_use_prep(path):
    '''
    This function follows the path and pulls the land use data from the different files and then merges it. It returns a dataframe.

    args : path -> path to folder with the water use files
    '''

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

# ### To prepare thegeneral data (emissions)
def general_prep(path):
    '''
    This function follows the path and pulls the emissions data from the different files and does some cleaning of the data. It returns a dataframe.

    args : path -> path to folder with the water use files
    '''
    general = pd.read_csv(path + "Food_production.csv")
    general = general[["Food product", "Total_emissions"]]
    general.columns = ["Food", "Total_emissions"]

    return general

# ### Join all the data in one dataframe
def join_resources(path1, path2):
    '''
    This function calls the land_use, water_use and general functions and joins the resulting dataframes. It returns a cleaned dataframe.

    args :
    path1 -> path to land use folder
    path2 -> path to water use folder
    '''
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

# ### 
def combine_data(column1, column2, df):
    '''
    This function combines two foods' values in the resources data. For instancem "Tofu" and "Tofu (soybeans)", as they are the same food, and one has the missing values of the other.

    
    '''
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

# ### 
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

# ### 
def resources_stats(df, resources_list):
    stats = df.groupby("Origin").agg({resource : (np.mean, np.median) for resource in resources_list})
    
    return stats

# ### 
def stats_to_plot(stats):
    to_plot = stats.unstack()
    to_plot = to_plot.reset_index()
    to_plot.columns = ["Resource", "Mean_median", "Origin", "Values"]
    return to_plot