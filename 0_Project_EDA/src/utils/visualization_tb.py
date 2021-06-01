import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


###############################################################################################
# ############################ -- RESOURCES FUNCTIONS -- ############################
# >>> Changes the shape of the quality df returned by foodquality function (mining data)
def resources_plot(resource, df, entries = None):
    # Let's do some quick plotting
    sns.set_theme()
    fig, ax = plt.subplots(1, 1, figsize = (15, 15))

    # I keep those values that aren't NA
    filtered_data = df[df[resource].notna()]
    # I sort the dataframe by the variable of interest (already defined as x)
    sorted_data = filtered_data.sort_values(by = resource, ascending = False)

    # For a better view, I defined the axis and data out of the seaborn function
    data = sorted_data if entries == None else sorted_data.head(entries)
    y = sorted_data.index if entries == None else sorted_data.head(entries).index

    # Paint the graph
    sns.barplot(x = resource, y = y, data = data, palette = "RdBu", ax = ax)

    # Title
    if "land" in resource.lower():
        text_end = " measured in squared meters (m2)"
    elif "water" in resource.lower():
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
# ############################ -- NUTRITION FUNCTIONS -- ############################
# >>> Changes the shape of the quality df returned by foodquality function (mining data)
def full_comparison_plot(comparisons):
    comparison_di, comparison_fats, comparison_cholesterol, comparison_energy = comparisons

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (20, 20))

    food_groups = comparison_di["%OfDI"].unique()
    n_colors = len(food_groups)

    palette = sns.color_palette("Paired", n_colors = n_colors)

    # ax1 : Daily intake
    sns.barplot(x = "Values", y = "Nutrient", hue = "%OfDI", data = comparison_di, palette = palette, ax = ax1)

    ax1.axvline(x=100, color='r', linestyle='dashed')

    ax1.set_title("% Of the Recommended Daily Intake", fontdict = {'fontsize': 20,
        'fontweight' : "bold"}, pad = 15)

    # ax2: Fats
    # This one works for the three remaining axes
    sns.barplot(x = "Values", y = "Nutrient", hue = "Food group", data = comparison_fats, palette = palette, ax = ax2)

    ax2.set_title("Fats (g)", fontdict = {'fontsize': 20,
        'fontweight' : "bold"}, pad = 15)

    # ax3: Cholesterol
    sns.barplot(x = "Values", y = "Food group", data = comparison_cholesterol, palette = palette, ax = ax3)

    ax3.set_title("Cholesterol (mg)", fontdict = {'fontsize': 20,
        'fontweight' : "bold"}, pad = 15)

    # ax4: Energy
    sns.barplot(x = "Values", y = "Food group", data = comparison_energy, palette = palette, ax = ax4)

    ax4.set_title("Energy (Kcal)", fontdict = {'fontsize': 20,
        'fontweight' : "bold"}, pad = 15)

    fig.tight_layout(pad = 3)

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
    sns.set_theme()

    fig, ax1 = plt.subplots(1, 1, figsize = (12, 12))
    splot = sns.barplot(x = df[nutrient], y = df.index, data = df, palette = "coolwarm", ax = ax1)

    return fig
