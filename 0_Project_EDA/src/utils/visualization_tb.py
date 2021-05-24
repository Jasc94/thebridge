import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------- TO PLOT --------------------------
def dailyintake_graph(df):
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