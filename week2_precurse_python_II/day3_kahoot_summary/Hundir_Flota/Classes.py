import pandas as pd
import os


# ---------------------------- Class Board ----------------------------
class Player_board:
    def __init__(self):
        # The one to show the oponent when guessing
        self.matrix_front = self.matrix_creator()
        # The one with the ships' coordinates info
        self.matrix_back = self.matrix_creator()
        # Board's lifes (ship's parts that haven't been hit)
        self.life = 0

    # To draw the board
    def matrix_creator(self):
        index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        d = {}
        d2 = {}

        for i in index:
            for j in range(1, len(index) + 1):
                d2[j] = '~'
            d[i] = d2

        df = pd.DataFrame(d)
        df = df.T
        return df

    # To draw the ships
    def ship_drawer(self, ship_info):
        '''
        df -> game board
        ship_info -> list with 4 parameters: ship's size, allignment, column and row
        '''

        df = self.matrix_back

        # parameters unpacking
        size, allignment, column, row = ship_info

        # I create a list with the the dataframe (board) indexes and another one with the equivalent numeric index
        l1 = list(df.index)
        l2 = list(range(len(l1)))

        # I zip both list for later use in one dict
        d = dict(zip(l1, l2))
        
        try:
            # If allignment is h (horizontal)
            # column + size - 1 -> because it starts counting the column position. For instance: column = 7, size = 4, ship'd be in 7, 8, 9, 10
            if allignment == 'h' and (column + size - 1) <= 10:
                # Loop through all the columns starting in the given one up to that column + the ship's size
                for i in range(column, column + size):
                    df.loc[row][i] = '*'
                return df

            # In other case (vertical)
            # d[row] + size - 1 -> same as before
            elif allignment == 'v' and (d[row] + size - 1) <= 10:
                # Loop through all the rows starting by the given one up to the row + ship's size
                for i in range(d[row], d[row] + size):
                    df.iloc[i][column] = '*'
                return df

        except:
            print('The given combination is out of ocean boundaries')

    # To calculate the board lifes
    def board_lifes(self):
        board = self.matrix_back

        self.life = 0
        column_lifes = {}

        for i in range(10):
            column_lifes = dict(board.iloc[i].value_counts())

            if '*' in column_lifes.keys():
                self.life += column_lifes['*']

        return self.life

    # To draw the oponent player's guess
    def pointer(self, coordinate):
        column, row = coordinate

        if self.matrix_back.loc[row][column] == '~':
            self.matrix_back.loc[row][column] = 'O'
            self.matrix_front.loc[row][column] = 'O'
            return self.matrix_front

        elif self.matrix_back.loc[row][column] == '*':
            self.matrix_back.loc[row][column] = 'X'
            self.matrix_front.loc[row][column] = 'X'
            return self.matrix_front

        else:
            return 'You already tried there'
        
        


# ---------------------------- Class Ship ----------------------------
class Ship:
    def __init__(self, size, coordinates):
        self.size = size
        self.allignment, self.column, self.row = coordinates
        self.life = size

    def attributes(self):
        return [self.size, self.allignment, self.column, self.row, self.life]

    def modify_lives(self):
        if self.life > 1:
            self.life -= 1
            return self.life
        elif self.life == 1:
            self.life -= 1
            return 'The ship was sunk'

#print('test\n' * 10)
#os.system('clear')