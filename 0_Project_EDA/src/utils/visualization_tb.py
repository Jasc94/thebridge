import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


###############################################################################################
# ############################ -- RESOURCES FUNCTIONS -- ############################
# >>> Changes the shape of the quality df returned by foodquality function (mining data)
def resources_plot(resource, df):
    # Let's do some quick plotting
    sns.set_theme()
    fig, ax = plt.subplots(1, 1, figsize = (15, 15))

    # I keep those values that aren't NA
    filtered_data = df[df[resource].notna()]
    # I sort the dataframe by the variable of interest (already defined as x)
    sorted_data = filtered_data.sort_values(by = resource, ascending = False)

    # For a better view, I defined the axis and data out of the seaborn function
    data = sorted_data
    y = sorted_data.index

    # Paint the graph
    sns.barplot(x = resource, y = y, data = data, palette = "RdBu", ax = ax)

    # Title
    if "water" in resource.lower():
        text_end = " measured in squared meters (m2)"
    elif "land" in resource.lower():
        text_end = " measured in liters (l)"
    else:
        text_end = " measured in kgs per kg of food"

    plt.title(resource + text_end, fontdict = {'fontsize': 20,
    'fontweight' : "bold"}, pad = 15
    )

    # Pull the name of the foods that are missing this value
    missing_values = list(df[df[resource].isna()].index)
    # Add it as note at the bottom of the plot
    textstr = f"We don't have the values for the following foods:\n{missing_values}"
    plt.text(0.25, 0.05, textstr, fontsize = 12, transform = plt.gcf().transFigure)

    # In notebooks it will plot twice, unless adding plt.show() at the end of the cell
    # That way, it associates the figure to that
    return fig

# >>> 
def plot_resources_stats(to_plot):
    number_of_axes = len(to_plot["Resource"].unique())

    fig, axes = plt.subplots(1, number_of_axes, figsize = (15, 7))

    resources = list(to_plot["Resource"].unique())

    for index in range(number_of_axes):
        sns.barplot(x = "Mean_median", y = "Values", hue = "Origin",
                    data = to_plot[to_plot["Resource"] == resources[index]], ax = axes[index])
        axes[index].set_title(resources[index], fontdict = {'fontsize': 14, 'fontweight' : "bold"})

    return fig


###############################################################################################
# ############################ -- TRANSFORMATION FUNCTIONS -- ############################
# >>> Changes the shape of the quality df returned by foodquality function (mining data)


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

def correlation_plot(corr_df):
    fig, ax = plt.subplots(1, 1, figsize = (10, 10))
    sns.heatmap(corr_df, annot = True, linewidths = .1, cmap="coolwarm", ax = ax)

    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)

    return fig


# -------------------------- TO PLOT --------------------------
def dailyintake_graph(df):
    sns.set_theme()
    #sns.set_style("whitegrid", {'grid.linestyle': '--'})

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

    sns.set_theme()
    #sns.set_style("whitegrid", {'grid.linestyle': '--'})

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
