import pandas as pd
from pandas.plotting import scatter_matrix
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import metrics

import os, sys

# Helpers
abspath = os.path.abspath
dirname = os.path.dirname
sep = os.sep

current_folder = dirname(abspath(__file__))
sys.path.append(current_folder)

import mining_data_tb as md

##################################################### PLOTTERS #####################################################
#####
class eda_plotter():
    def __init__(self, df, features_names):
        self.df = df
        self.features_names = features_names

    #####
    def __n_rows(self, n_columns):
        columns = list(self.df.columns)

        if len(columns) % n_columns == 0:
            axes_rows = len(columns) // n_columns
        else:
            axes_rows = (len(columns) // n_columns) + 1

        return axes_rows

    #####
    def rows_plotter(self, n_columns, kind, figsize, features_names = None):
        fig, axes = plt.subplots(1, n_columns, figsize = figsize)
        count = 0

        for column in range(n_columns):
            if kind == "strip":
                sns.stripplot(y = self.df.iloc[:, count], ax = axes[column])
            elif kind == "dist":
                sns.distplot(self.df.iloc[:, count], ax = axes[column])
            elif kind == "box":
                sns.boxplot(self.df.iloc[:, count], ax = axes[column])
            else:
                sns.histplot(self.df.iloc[:, count], ax = axes[column], bins = 30)

            try:
                axes[column].set(xlabel = self.features_names[count])
            except:
                pass

            if (count + 1) < df.shape[1]:
                    count += 1
            else:
                break

        return fig
        
    #####
    def multi_axes_plotter(self, n_columns, kind, figsize):
        # Calculating the number of rows from number of columns and variables to plot
        n_rows_ = self.__n_rows(n_columns)

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

        # Plotting rows and columns
        for row in range(axes_col):
            for column in range(axes_row):
                if kind == "strip":
                    sns.stripplot(y = self.df.iloc[:, count], ax = axes[row][column])
                elif kind == "dist":
                    sns.distplot(self.df.iloc[:, count], ax = axes[row][column])
                elif kind == "box":
                    sns.boxplot(self.df.iloc[:, count], ax = axes[row][column])
                else:
                    sns.histplot(self.df.iloc[:, count], ax = axes[row][column], bins = 30)

                try:
                    axes[row][column].set(xlabel = self.features_names[count])
                except:
                    pass

                if (count + 1) < self.df.shape[1]:
                    count += 1
                else:
                    break
        return fig

    #####
    def correlation_matrix(self, figsize):
        fig = plt.figure(figsize = figsize)
        sns.heatmap(self.df.corr(), annot = True, linewidths = .1,
                    cmap = "Blues", xticklabels = False,
                    yticklabels = self.features_names, cbar = False)

        return fig

##################################################### ML METRICS PLOTTERS #####################################################
#####
class ml_model_plotter():
    def __init__(self, ml_model):
        self.ml_model = ml_model

    #####
    def train_val_plot(self, figsize = (14, 6)):
        fig = plt.figure(figsize = figsize)
        sns.set_theme()

        sns.lineplot(data = [self.ml_model.train_scores, self.ml_model.val_scores], markers = True, dashes = False)

        plt.ylabel("Score")
        plt.xlabel("Round")
        plt.legend(["Train score", "Validation score"])
        
        return fig

    #####
    def test_metrics(self, figsize = (12, 12)):
        # Calculate the row/column totals for later use
        row_sums = self.ml_model.cm.sum(axis = 1, keepdims = True)
        column_sums = self.ml_model.cm.sum(axis = 0, keepdims = True)
        
        # Relative values to column/row sums
        rel_row = (self.ml_model.cm / row_sums) * 100
        rel_col = (self.ml_model.cm / column_sums) * 100

        # Plot
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = figsize, sharex = True, sharey = True)

        first_row_palette = sns.color_palette("light:b", as_cmap=True)
        second_row_palette = sns.light_palette("seagreen", as_cmap=True)
        fmt = "g"

        # ax1
        sns.heatmap(self.ml_model.cm, annot = True, linewidths = .1, cmap = first_row_palette, ax = ax1, cbar = False, fmt = fmt)
        ax1.set_ylabel("Actual class")
        ax1.set_title("Confusion matrix")

        # ax2
        sns.heatmap((self.ml_model.cm / self.ml_model.cm.sum()) * 100, annot = True, linewidths = .1, cmap = first_row_palette, ax = ax2, cbar = False, fmt = fmt)
        ax2.set_ylabel("Actual class")
        ax2.set_title("Confusion matrix - relative")

        # ax3
        sns.heatmap(rel_row, annot = True, linewidths = .1, cmap = second_row_palette, ax = ax3, cbar = False, fmt = fmt)
        ax3.set_xlabel("Predicted class")
        ax3.set_title("Relative to row sum (Recall)")

        # ax4
        sns.heatmap(rel_col, annot = True, linewidths = .1, cmap = second_row_palette, ax = ax4, cbar = False, fmt = fmt)
        ax4.set_xlabel("Predicted class")
        ax4.set_title("Relative to col sum (Precision)")

        return fig


##################################################### NEURAL NETWORK PLOTTERS #####################################################
#####
class neural_network_plotter():
    def __init__(self, neural_network, dataset):
        self.model = neural_network
        self.dataset = dataset

    def model_progression(self, history):
        accuracy = history.history["binary_accuracy"]
        loss = history.history["loss"]

        fig, ax = plt.subplots(1, 2, figsize = (12, 6))
        ax[0].plot(accuracy)
        ax[0].set_title("Binary Accuracy")
        ax[1].plot(loss, c = "orange")
        ax[1].set_title("Loss")
        return fig

    def test_results(self, figsize = (14, 14)):
        X_train = self.dataset.X_train
        y_train = self.dataset.y_train
        X_test = self.dataset.X_test
        y_test = self.dataset.y_test

        ##### Batches structure
        y_t_unique, y_t_counts = np.unique(y_train, return_counts=True)
        y_v_unique, y_v_counts = np.unique(y_test, return_counts=True)

        # Predictions
        predictions = self.model.predict(X_test)
        predictions2 = np.array([1 if (prediction > .5) else 0 for prediction in predictions])

        ##### Confusion Matrix
        cm = metrics.confusion_matrix(y_test, predictions2)

        # Calculate the row/column totals for later use
        row_sums = cm.sum(axis = 1, keepdims = True)
        column_sums = cm.sum(axis = 0, keepdims = True)

        # Relative values to column/row sums
        rel_row = (cm / row_sums) * 100
        rel_col = (cm / column_sums) * 100

        # Plot
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = figsize, sharex = True, sharey = True)

        first_row_palette = sns.color_palette("light:b", as_cmap=True)
        second_row_palette = sns.light_palette("seagreen", as_cmap=True)
        fmt = "g"

        # ax1
        sns.heatmap(cm, annot = True, linewidths = .1, cmap = first_row_palette, ax = ax1, cbar = False, fmt = fmt)
        ax1.set_ylabel("Actual class")
        ax1.set_title("Confusion matrix")

        # ax2
        sns.heatmap((cm / cm.sum()) * 100, annot = True, linewidths = .1, cmap = first_row_palette, ax = ax2, cbar = False, fmt = fmt)
        ax2.set_ylabel("Actual class")
        ax2.set_title("Confusion matrix - relative")

        # ax3
        sns.heatmap(rel_row, annot = True, linewidths = .1, cmap = second_row_palette, ax = ax3, cbar = False, fmt = fmt)
        ax3.set_xlabel("Predicted class")
        ax3.set_title("Relative to row sum (Recall)")

        # ax4
        sns.heatmap(rel_col, annot = True, linewidths = .1, cmap = second_row_palette, ax = ax4, cbar = False, fmt = fmt)
        ax4.set_xlabel("Predicted class")
        ax4.set_title("Relative to col sum (Precision)")

        return fig