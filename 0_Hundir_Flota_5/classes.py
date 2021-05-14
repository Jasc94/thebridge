import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

class board:
    def __init__(self, player:str):
        # Player name
        self.player = player
        self.backend = self.backend_creator()
        self.life = 0

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

    # To plot the boards (frontend)
    def frontend_creator(self):
        # To translate the symbols into numbers that Seaborn can read
        to_plot = self.backend.replace(['~', '*', 'O', 'X'], [1, 1, 0, -1])

        # Plot the board using the dataframe
        plt.figure(figsize=(12, 8))
        sns.heatmap(to_plot, cmap="BrBG", center = 0, linewidths = 0.5, linecolor = "white")
        plt.title(f'{self.player} remaining lifes: {self.life}', fontdict = {'fontsize': 'xx-large', 'fontweight' : 'bold'})
        plt.show(block=False)
        plt.pause(3)
        plt.close()
        
    # Ship drawer
    def ship_drawer(self, ship_info):
        '''
        df -> game board
        ship_info -> list with 4 parameters: ship's size, allignment, column and row
        ''' 
        # Matrix to draw into
        df = self.backend

        # Unpacking the info
        column, row, allignment, size = ship_info

        # List of indexes and equivalent numeric position
        l1 = list(df.index)
        l2 = list(range(len(l1)))

        # Zip both lists
        d = dict(zip(l1, l2))

        # First I check the allignment
        if allignment == 'h':
            # Then I draw the ships starting from the given column and finishing in the column + size
            for i in range(column, column + size):
                df.loc[row][i] = '*'
            return df
        elif allignment == 'v':
            # Equivalent procedure for rows
            for i in range(d[row], d[row] + size):
                df.iloc[i][column] = '*'
            return df

    
    
    # To modify board's life
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

    # To draw oponent's guess
    def pointer(self, coordenate):
        column, row = coordenate

        # If oponent hits '~', then water
        if self.backend.loc[row][column] == '~':
            self.backend.loc[row][column] = 'O'

        # If he/she hits '*', then it's a correct guess
        elif self.backend.loc[row][column] == '*':
            self.backend.loc[row][column] = 'X'

        # The only remaining option is that the oponent hits either 'X' or 'O'. In both cases it means that he/she already tried there
        else:
            return 'repeated'
        
# ---------------------------- Class Ship ----------------------------
class ship:
    def __init__(self, ship_info):
        # Unpacking the info
        self.column, self.row, self.allignment, self.size = ship_info
        # Ship's life is equivalent to its size
        self.life = self.size

    def attributes(self):
        return [self.column, self.row, self.allignment, self.size, self.life]

    def modify_lifes(self):
        if self.life > 1:
            self.life -= 1
            return self.life
        elif self.life == 1:
            self.life -= 1
            return 'Enemy\'s ship sunk'