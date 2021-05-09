from Classes import *
from Functions import *

import os
import time


# 1) Create empty player boards
# player1_board = Player_board()
# player2_board = Player_board()

# dfs = load_old_game()
# print(dfs)
# player1_board.matrix_back

# def game_start():

#     # 2) Ask players for the coordenates
#     print('Player 1, please place your ships:\n')
#     player1_ships = ask_coordenates()
#     print('Player 2, please place your ships:\n')
#     player2_ships = ask_coordenates()

#     # 3) Draw the ships
#     for i in range(len(player1_ships)):
#         # I loop through the player1 ships
#         to_draw_1 = player1_ships[i].attributes()[:-1]
#         player1_board.ship_drawer(to_draw_1)

#         # I loop through the player 2 ships
#         to_draw_2 = player2_ships[i].attributes()[:-1]
#         player2_board.ship_drawer(to_draw_2)

#     # 4) I update the boards lifes situation
#     player1_board.board_lifes()
#     player2_board.board_lifes()

#     print('Player 1 lifes: ', player1_board.life)
#     print(player1_board.matrix_front)

#     print('Player 2 lifes: ', player2_board.life)
#     print(player2_board.matrix_front)

# game_start()

# old = input('enter game')
# a = load_old_game(old)
# print(a.keys())

# old = input('enter game')
# b = load_old_game(old)
# print(b.keys())

#print(__file__)
#print(os.path.dirname(__file__))
#print(os.listdir(os.path.dirname(__file__) + '/json'))

def show_saved_games():
    try:
        path = os.path.dirname(__file__) + '/json'
        files = os.listdir(path)
        print('\n')
        for i in files:
            print(i)
        print('\n')
    except Exception:
        print("\nYou don't have any saved games\n")

#show_saved_games()

def matrix_creator():
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

df1 = matrix_creator()
df2 = matrix_creator()

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

a = show_full_front_boards(df1, df2)
print(a)