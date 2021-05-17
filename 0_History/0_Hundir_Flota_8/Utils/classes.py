import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json


# ---------------------------- CLASS BOARD ----------------------------
class board:
    def __init__(self, player:str):
        # Player name
        self.player = player
        # Board with the ships
        self.backend = self.backend_creator()
        # Player's lifes (amount of '*' in the board)
        self.life = 0

    # >>> To create the board with the ships: ~, *, X and O
    def backend_creator(self):
        # Board's index
        index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        # Two dicts for later use
        d = {}
        d2 = {}

        # The outer dict is for the indexes and the inner for the columns
        for i in index:
            for j in range(1, len(index) + 1):
                # I fill it with '~'
                d2[j] = '~'
                d[i] = d2

        # Dataframe out of the dicts
        df = pd.DataFrame(d)
        # Transpose it to have the letters to be the index and the numbers the columns
        df = df.T
        return df

    # >>> To plot the boards with the heatmap (frontend)
    def frontend_creator(self):
        # To translate the symbols into numbers that Seaborn can read
        to_plot = self.backend.replace(['~', '/', '*', 'O', 'X'], [1, 1, 1, 0, -1])

        # Plot the board using the dataframe
        plt.figure(figsize=(12, 8))
        
        # we fix center at 0, so that the 1's (~, *) are always blue and the -1's are always brown
        sns.heatmap(to_plot, cmap="BrBG", center = 0, linewidths = 0.5, linecolor = "white")
        
        # we'll use the title to guide the players through the game, adding the info about the 
        plt.title(f'{self.player} remaining lifes: {self.life}', fontdict = {'fontsize': 'xx-large', 'fontweight' : 'bold'})
        
        # From here, it's just show the plot, keep it open for X seconds and then close it
        plt.show(block=False)
        plt.pause(5)
        plt.close()
        
    # >>> Ship drawer
    def ship_drawer(self, ship_info):
        # Matrix to draw into
        df = self.backend

        # Unpacking the info
        column, row, allignment, size = ship_info

        # List of indexes and equivalent numeric position
        l1 = list(df.index)             # A, B, C, D, ...
        l2 = list(range(len(l1)))       # 1, 2, 3, 4, ...

        # Zip both lists
        d = dict(zip(l1, l2))       # {'A' : 1, 'B' : 2, ...}

        if allignment == 'h':

            # Paint outermost points
            left = column - 1 if column - 1 > 0 else 0
            right = column + size if column + size < 10 else 10
            df.loc[row][left] = '/'
            df.loc[row][right] = '/'

            for i in range(column, column + size):
                
                # Paint horizontal surroundings
                above = d[row] - 1 if d[row] - 1 > 0 else 0
                below = d[row] + 1 if d[row] + 1 < 9 else 9     # Because we're using the index, which only goes up to 9
                df.iloc[above][i] = '/'
                df.iloc[below][i] = '/'

                # Paint the ship
                df.loc[row][i] = '*'

            return df

        else:

            # Paint the outermost points
            left = d[row] - 1 if d[row] - 1 > 0 else 0
            right = d[row] + size if d[row] + size < 10 else 10
            df.iloc[left][column] = '/'
            df.iloc[right][column] = '/'

            for i in range(d[row], d[row] + size):

                # Paint the vertical surroundings
                above = column - 1 if column - 1 > 0 else 0
                below = column + 1 if column + 1 < 10 else 10
                df.iloc[i][above] = '/'
                df.iloc[i][below] = '/'

                # Paint the ship
                df.iloc[i][column] = '*'

            return df

    # >>> To modify board's life
    def board_lifes(self):
        board = self.backend

        self.life = 0
        # As I calculate the lifes per column and then, add them up, I'll use a dict to keep a track of everything
        column_lifes = {}

        # I check all the columns
        for i in range(10):
            column_lifes = dict(board.iloc[i].value_counts())

            # Every '*' is a remaining life
            if '*' in column_lifes.keys():
                self.life += column_lifes['*']

        return self.life

    # >>> To draw oponent's guess
    def pointer(self, coordenate):
        column, row = coordenate

        # If oponent hits '~', then water
        if self.backend.loc[row][column] == '~' or self.backend.loc[row][column] == '/':
            self.backend.loc[row][column] = 'O'

        # If he/she hits '*', then it's a correct guess
        elif self.backend.loc[row][column] == '*':
            self.backend.loc[row][column] = 'X'

        # The only remaining option is that the oponent hits either 'X' or 'O'. In both cases it means that he/she already tried there
        else:
            return 'repeated'
        

# ---------------------------- CLASS SHIP ----------------------------
class ship:
    def __init__(self, ship_info):
        # Unpacking the info
        self.column, self.row, self.allignment, self.size = ship_info
        # Ship's life is equivalent to its size
        self.life = self.size

    # >>> To get the ship's attributes
    def attributes(self):
        return [self.column, self.row, self.allignment, self.size]