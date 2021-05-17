import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

from varname import nameof
import os
import sys

import classes as c


# ---------------------------- COORDENATES FUNCTIONS ----------------------------

# >>> To ask for ship's column 
def ship_column():
    try:
        column = int(input('Column: '))
        column_options = list(range(1, 11))

        if column in column_options:
            return column

        else:
            print("That's not allowed!!!!!")
            return ship_column()

    except Exception:
        print("That's not allowed!!!!!")
        return ship_column()

# >>> To ask for ship's row -
def ship_row():
    row = input('Row: ').upper()
    row_options = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    if row in row_options:
        return row

    else:
        print("That's not allowed!!!!!")
        return ship_row()

# >>> To ask for ship's allignment
def ship_allignment():
    allignment = input('Vertical (v) or Horizontal (h): ').lower()
    options = ['v', 'h']    # valid options

    # I check if the user enter a right option and if so, I just return it
    if allignment in options:
        return allignment

    # Otherwise, I call the function again and print a message
    else:
        print("That's not allowed!!!!!")
        ship_allignment()

# >>> To join ship's row and column
def ship_position():
    column = ship_column()
    row = ship_row()
    allignment = ship_allignment()

    return [column, row, allignment]

def ship_coordenates():
    column = ship_column()
    row = ship_row()

    return [column, row]

# ---------------------------- CHECK FUNCTIONS ----------------------------
# >>> To check the ship is within the board
def check_boundaries(size):
    # Call the functions for column, row and allignment
    col, row, allign = ship_position()

    # Indexes to check
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    columns = list(range(1, 11))

    # Zip into dict for later user
    d = dict(zip(rows, columns))

    # Pull the row index for later use
    row_index = d[row]

    if allign == 'v':
        # Calculate the last row with the indexes
        # -1 -> Because it starts drawing in the row entered, not the next one
        end_row = row_index + size - 1
        # As rows and columns have the same length and the previous calculation returns a number, we can use it to check the condition
        if end_row not in columns:
            print('Out of boundaries')
            return check_boundaries(size)
    
    else:
        # Calculate the last column
        end_col = col + size - 1
        # If it is not in the possible columns, then 'out of boundaries'
        if end_col not in columns:
            print('Out of boundaries')
            return check_boundaries(size)

    print('All right')
    return [col, row, allign, size]

# >>> To check the ship isn't overlapping
def check_overlap(board, size):
    col, row, allign, size = check_boundaries(size)

    # Indexes to check
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    columns = list(range(1, 11))

    # Zip into dict for later user
    d = dict(zip(rows, columns))

    # space list to store all the positions we need to check
    space = []

    if allign == 'v':
        row_start = d[row] -1
        row_end = d[row] + size -1

        for i in rows[row_start:row_end]:
            field = board.backend.loc[i][col]
            space.append(field)

    else:
        col_start = col - 1
        col_end = col + size - 1

        for i in columns[col_start:col_end]:
            field = board.backend.loc[row][i]
            space.append(field)


    if '*' in space or '/' in space:
        print("You already have a ship there or too close. Try another location")
        return check_overlap(board, size)

    else:
        ship_info = [col, row, allign, size]
        return ship_info

# >>> To draw ships
def ask_coordenates(board):
    # Ships to be entered
    ships_to_enter = {'2x1' : {'size' : 2, 'amount' : 4}, '3x1' : {'size' : 3, 'amount' : 3}, '4x1' : {'size' : 4, 'amount' : 2}, '5x1' : {'size' : 5, 'amount' : 1}}

    player_ships = []

    # Iterate through the keys (type of ship)
    for i in ships_to_enter.keys():

        count = 0
        # Iterate though the amount of ships for every type
        while count < ships_to_enter[i]["amount"]:
            print(board.backend)
            # Show the user the ship we are asking for
            print('For your ship {} of size {}, please enter the info:\n'.format(count + 1, i))
            # Ask information about the ship using the checker
            ship_info = check_overlap(board, int(i[0]))

            # Create the ship object and add it to the ships' list
            ship = c.ship(ship_info)
            player_ships.append(ship)

            # Draw the ship
            board.ship_drawer(ship.attributes())

            os.system('clear')
            count += 1

        count = 0

    print('Ships succesfully placed')


# ---------------------------- BOARD PAINTING FUNCTIONS ----------------------------
# >>> To see the full board
def full_boards(board1, board2, turn, winner = None):

    if winner == None:
        # Replace the backend values for numbers, so that sns.heatmap can interpret it
        to_plot1 = board1.backend.replace(['~', '/', '*', 'O', 'X'], [1, 1, 1, 0, -1])
        to_plot2 = board2.backend.replace(['~', '/', '*', 'O', 'X'], [1, 1, 1, 0, -1])

        # Create the grid with two plots
        fig, (ax1, ax2) = plt.subplots(1, 2, sharey = True, figsize = (10, 10))

        # Plot board 1
        sns.heatmap(to_plot1, cmap="BrBG", center = 0, linewidths = 0.5,
                linecolor = "white", square = True, cbar = False, ax = ax1)

        # Plot board 2
        sns.heatmap(to_plot2, cmap="BrBG", center = 0, linewidths = 0.5,
                linecolor = "white", square = True, cbar = False, ax = ax2)
    
        fig.suptitle(f'\n\nTurn {turn}\n\nClose the window to continue with the game', fontsize=16)

        ax1.set_title(f'{board1.player} - Board\nRemaining lifes: {board1.life}')
        ax2.set_title(f'{board2.player} - Board\nRemaining lifes: {board2.life}')

        plt.show()
    
    else:
        # Replace the backend values for numbers, so that sns.heatmap can interpret it
        to_plot1 = board1.backend.replace(['~', '/', '*', 'O', 'X'], [1, 1, -0.25, 0, -1])
        to_plot2 = board2.backend.replace(['~', '/', '*', 'O', 'X'], [1, 1, -0.25, 0, -1])

        # Create the grid with two plots
        fig, (ax1, ax2) = plt.subplots(1, 2, sharey = True, figsize = (10, 10))

        # Plot board 1
        sns.heatmap(to_plot1, cmap="BrBG", center = 0, linewidths = 0.5,
                linecolor = "white", square = True, cbar = False, ax = ax1)

        # Plot board 2
        sns.heatmap(to_plot2, cmap="BrBG", center = 0, linewidths = 0.5,
                linecolor = "white", square = True, cbar = False, ax = ax2)

        fig.suptitle(f'\n\nThe game ended on turn {turn}\n\nThe winner is {winner}', fontsize=16)

        ax1.set_title(f'{board1.player} - Board\nRemaining lifes: {board1.life}')
        ax2.set_title(f'{board2.player} - Board\nRemaining lifes: {board2.life}')

        plt.show()

    #plt.pause(5) 
    plt.close('all')
    

# ---------------------------- SUPPORT FUNCTIONS ----------------------------
# >>> To check who is the winner
def winner(board1, board2):

    if board1.life > board2.life:
        return board1.player

    elif board1.life < board2.life:
        return board2.player

    else:
        return "It's a Tie"


# ---------------------------- SAVE GAME FUNCTIONS ----------------------------
# >>> To pack the backends into a list
def pack_dfs_to_save(board1, board2):
    # Pack the backends into a list
    dfs = board1.backend, board2.backend

    return dfs

# >>> To save the current game
def save_game(backends_list, game_name):
    # Unpack the backends in the list
    board1_backend, board2_backend = backends_list

    # Creo una carpeta con el nombre del juego, donde voy a guardar todos los jsons (correspondientes a dfs)
    path = os.path.dirname(__file__) + '/json/' + game_name
    if not os.path.exists(path):
        os.makedirs(path)

    # I append the names to the locations
    path1 = path + '/' + nameof(board1_backend) + '.json'
    path2 = path + '/' + nameof(board2_backend) + '.json'

    # I save all the dfs as jsons
    board1_backend.to_json(path1, orient = 'records', indent = 4)
    board2_backend.to_json(path2, orient = 'records', indent = 4)

    return '\nSuccesfully saved\n'



# ---------------------------- LOAD OLD GAME FUNCTIONS ----------------------------
# >>> To see the saved games when choosing "load old game"
def show_saved_games():
    # I go up to my current folder location and append the "json"
    path = os.path.dirname(__file__) + '/json'
    # list of all files within the folder
    files = os.listdir(path)
    print('\n')
    # print all the files in the list
    for i in files:
        print(i)
    print('\n')


# >>> To load an old game
def load_old_game(game_name):
    try:
        #List to store all the dataframes that I upload
        dfs = []
        path = os.path.dirname(__file__) + '/json/' + game_name

        # I check all the items in the folder
        for i in os.listdir(path):
            # I append the name to the path, so that I can read it later
            full_path = path + '/' + str(i)
            # I read it
            with open(full_path, 'r+') as outfile:
                # Now I have the dict
                old_game = json.load(outfile)
                # Not I have the df
                old_df = pd.DataFrame(old_game)

                # I recover the indexes, as they get lost when saved as jsons
                old_df.index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
                old_df.columns = list(range(1, 11))
                
                # I append the df, with the corresponding name, to the dict
                dfs.append(old_df)

        return dfs
        # This is how they are laoded: [board1_backend, board2_backend]

    except:
        game_name = input('Please enter an existing name:\n')
        return load_old_game(game_name)