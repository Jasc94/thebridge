import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------- SUPPORT FUNCTIONS --------------------------
def show_values_on_bars(axs, h_v="v", space=0.4):
    def _show_on_single_plot(ax):
        if h_v == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height()
                value = int(p.get_height())
                ax.text(_x, _y, value, ha="center") 
        elif h_v == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height()
                value = int(p.get_width())
                ax.text(_x, _y, value, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)


# -------------------------- TO PLOT --------------------------
def dailyintake_graph(df):
    sns.set_style("whitegrid", {'grid.linestyle': '--'})

    fig, ax1 = plt.subplots(1, 1, figsize = (12, 12))

    splot = sns.barplot(x = "nutrient", y = "%OfDailyIntake", data = df, ax = ax1)

    plt.ylim(0, df["%OfDailyIntake"].max() * 1.1)

    plt.xticks(rotation = 90)

    for p in splot.patches:
            splot.annotate(format(p.get_height(), '.1f') + '%', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        xytext = (0, 9), 
                        textcoords = 'offset points')

    return fig

def nutritionfacts_graph1(df, nutrient):

    df = df.sort_values(by = nutrient, ascending = False)

    sns.set_style("whitegrid", {'grid.linestyle': '--'})

    fig, ax1 = plt.subplots(1, 1, figsize = (12, 12))
    splot = sns.barplot(x = df.index, y = df[nutrient], data = df, palette = "coolwarm", ax = ax1)

    plt.xticks(rotation = 60)

    for p in splot.patches:
        splot.annotate(format(p.get_height(), '.2f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 9), 
                    textcoords = 'offset points')

    return fig

def emissions_graph(df, column):
    df = df.sort_values(by = column, ascending = False)
    df = df[df[column] > 0]

    sns.set_style("whitegrid", {'grid.linestyle': '--'})

    fig, ax = plt.subplots(figsize = (12, 15))

    colors = list(sns.color_palette("deep"))

    sns.barplot(x = column, y = df.index, data = df, color = colors[0])

    show_values_on_bars(ax, "h")

    land_labels = ["Land use per 1000kcal", "Land use per kg", "Land use per 100g protein"]
    water_labels = ["Freswater withdrawls per 1000kcal", "Freswater withdrawls per kg",
                    "Freswater withdrawls per 100g protein"]
    emissions_labels = ["Total_emissions"]

    if column in land_labels: plt.xlabel("Squared meters (m2) of CO2 per Kg of food product")
    elif column in water_labels: plt.xlabel("Liters (l) per Kg of food product")
    else: plt.xlabel("Kg of CO2 per Kg of food product")

    return fig