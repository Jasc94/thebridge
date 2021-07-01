import pandas as pd
from pandas.plotting import scatter_matrix
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import os, sys

dirname = os.path.dirname
current_folder = dirname(__file__)
sys.path.append(current_folder)

import mining_data_tb as md

##################################################### PLOTTERS #####################################################
#####
def n_rows(df, n_columns):
    columns = list(df.columns)

    if len(columns) % n_columns == 0:
        axes_rows = len(columns) // n_columns
    else:
        axes_rows = (len(columns) // n_columns) + 1

    return axes_rows

#####
def rows_plotter(df, n_columns, kind, figsize, var_names = None):
    fig, axes = plt.subplots(1, n_columns, figsize = figsize)
    count = 0

    for column in range(n_columns):
        if kind == "strip":
            sns.stripplot(y = df.iloc[:, count], ax = axes[column])
        elif kind == "dist":
            sns.distplot(df.iloc[:, count], ax = axes[column])
        elif kind == "box":
            sns.boxplot(df.iloc[:, count], ax = axes[column])
        else:
            sns.histplot(df.iloc[:, count], ax = axes[column], bins = 30)

        try:
            axes[column].set(xlabel = md.var_descr_detector(df.iloc[:, count].name, var_names))
        except:
            pass

        if (count + 1) < df.shape[1]:
                count += 1
        else:
            break

    return fig
    
#####
def multi_axes_plotter(df, n_columns, kind, figsize, var_names = None):
    # Calculating the number of rows from number of columns and variables to plot
    n_rows_ = n_rows(df, n_columns)

    # Creating the figure and as many axes as needed
    fig, axes = plt.subplots(n_rows_, n_columns, figsize = figsize)
    # To keep the count of the plotted variables
    count = 0

    # Some transformation, because with only one row, the shape is: (2,)
    axes_col = axes.shape[0]
    try:
        axes_row = axes.shape[1]
    except:
        axes_row = 1

    
    for row in range(axes_col):
        for column in range(axes_row):
            if kind == "strip":
                sns.stripplot(y = df.iloc[:, count], ax = axes[row][column])
            elif kind == "dist":
                sns.distplot(df.iloc[:, count], ax = axes[row][column])
            elif kind == "box":
                sns.boxplot(df.iloc[:, count], ax = axes[row][column])
            else:
                sns.histplot(df.iloc[:, count], ax = axes[row][column], bins = 30)

            try:
                axes[row][column].set(xlabel = md.var_descr_detector(df.iloc[:, count].name, var_names))
            except:
                pass

            if (count + 1) < df.shape[1]:
                count += 1
            else:
                break

    return fig
