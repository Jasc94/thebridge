from Classes import *
from varname import nameof
import json

# ---------------------------- Basic functions ----------------------------
# To ask for ship's column
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

# To ask for ship's row
def ship_row():
    row = input('Row: ').upper()
    row_options = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    if row in row_options:
        return row

    else:
        print("That's not allowed!!!!!")
        return ship_row()

# To join ship's row and column
def ship_coordenates():
    column = ship_column()
    row = ship_row()

    return [column, row]

# To ask for ship's allignment
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

# To ask for ship's size
def ship_size():
    size = input('5x1, 4x1, 3x1 or 2x1: ')
    size = int(size[0])
    return size

# To show both front boards together
def show_full_front_boards(df1, df2):
    result = df1

    # I create a divisor, as I want to print both boards together
    divisor = ['|' for i in range(10)]
    index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    divisor_df = pd.DataFrame(divisor, index = index, columns = ['|'])

    # I join the divisor to player's 1 board and then player's 2 board
    result = pd.merge(result, divisor_df, how = 'outer', right_index = True, left_index = True)
    result = pd.merge(result, df2, how = 'outer', right_index = True, left_index = True)

    # I print the result of the game
    return result


# ---------------------------- For the beginning of the game ----------------------------
# To draw ships
def ask_coordenates():
    ships_to_enter = {'2x1' : {'size' : 2, 'amount' : 4}, '3x1' : {'size' : 3, 'amount' : 3}, '4x1' : {'size' : 4, 'amount' : 2}, '5x1' : {'size' : 5, 'amount' : 1}}

    player_ships = []

    for i in ships_to_enter.keys():
        count = 0
        while count < ships_to_enter[i]['amount']:
            print('For your ship {} of size {}, please enter the info:\n'.format(count + 1,
            i))

            size = int(i[0])
            allignment = ship_allignment()
            column, row = ship_coordenates()

            ship = Ship([column, row, allignment, size])
            player_ships.append(ship)

            count += 1

        count = 0

    return player_ships


# ---------------------------- To save/load the game ----------------------------
# To load an old game
def load_old_game(game_name):
    # Dict to store all the dataframes that I upload with the names as keys, so that I can them match them with the respective player front/back boards
    dfs = []
    # path = '0_Hundir_Flota_2/json/' + game_name
    path = os.path.dirname(__file__) + '/json/' + game_name

    # As I will have 4 json (1 per player front/back matrix)
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
    # This is how they are laoded: ['player2_front.json', 'player1_back.json', 'player2_back.json', 'player1_front.json']

# To save the current game
def save_game(dfs_list, game_name):
    # I unpack the dfs in the list
    player1_front, player1_back, player2_front, player2_back = dfs_list

    # Creo una carpeta con el nombre del juego, donde voy a guardar todos los jsons (correspondientes a dfs)
    path = os.path.dirname(__file__) + '/json/' + game_name
    if not os.path.exists(path):
        os.makedirs(path)

    # I append the names to the locations
    path1 = path + '/' + nameof(player1_front) + '.json'
    path2 = path + '/' + nameof(player1_back) + '.json'
    path3 = path + '/' + nameof(player2_front) + '.json'
    path4 = path + '/' + nameof(player2_back) + '.json'

    # I save all the dfs as jsons
    player1_front.to_json(path1, orient = 'records', indent = 4)
    player1_back.to_json(path2, orient = 'records', indent = 4)
    player2_front.to_json(path3, orient = 'records', indent = 4)
    player2_back.to_json(path4, orient = 'records', indent = 4)

    return '\nSuccesfully saved\n'

# To pack the boards (dfs) so I can easier save them
def pack_dfs_to_save():
    # I create a list of dfs
    dfs = [player1_board.matrix_front, player1_board.matrix_back, player2_board.matrix_front, player2_board.matrix_back]

    return dfs

# To see the saved games when choosing "load old game"
def show_saved_games():
    # I use a try/except, just in case the folder of "json" doesn't exist yet -> this means, there is no saved game
    try:
        # I go up to my current folder location and append the "json"
        path = os.path.dirname(__file__) + '/json'
        # list of all files within the folder
        files = os.listdir(path)
        print('\n')
        # print all the files in the list
        for i in files:
            print(i)
        print('\n')
    except Exception:
        print("\nYou don't have any saved games\n")