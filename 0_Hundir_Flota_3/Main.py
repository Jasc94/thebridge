from Classes import *
from Functions import *

import os
import time

# ---------------------------- Game preparation ----------------------------
# 1.A) Create empty player boards
player1_board = Player_board()
player2_board = Player_board()

# 1.B) new game or old game?
new_or_old_game = input('Do you want to start a new game(new) or load an old one(old)?\n').lower()

# If new game...
if new_or_old_game == 'new':
    # 2) Ask players for the coordenates
    print('Player 1, please place your ships:\n')
    player1_ships = ask_coordenates()
    print('Player 2, please place your ships:\n')
    player2_ships = ask_coordenates()

    # 3) Draw the ships
    for i in range(len(player1_ships)):
        # I loop through the player1 ships
        to_draw_1 = player1_ships[i].attributes()[:-1]
        player1_board.ship_drawer(to_draw_1)

        # I loop through the player 2 ships
        to_draw_2 = player2_ships[i].attributes()[:-1]
        player2_board.ship_drawer(to_draw_2)

    

# If old game...
else:
    show_saved_games()
    game_name = input('Enter the name of the game you want to load:\n')
    # This is how they are laoded: ['player2_front.json', 'player1_back.json', 'player2_back.json', 'player1_front.json']
    player2_board.matrix_front, player1_board.matrix_back, player2_board.matrix_back, player1_board.matrix_front = load_old_game(game_name)
    
    # player2_board.matrix_front.index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    # player1_board.matrix_back.index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    # player2_board.matrix_back.index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    # player1_board.matrix_front.index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    # player2_board.matrix_front.columns = list(range(1, 11))
    # player1_board.matrix_back.columns = list(range(1, 11))
    # player2_board.matrix_back.columns = list(range(1, 11))
    # player1_board.matrix_front.columns = list(range(1, 11))

    player1_board.board_lifes()
    player2_board.board_lifes()

# 4) I update the boards lifes situation
player1_board.board_lifes()
player2_board.board_lifes()

# print('Player 1 lifes: ', player1_board.life)
# print(player1_board.matrix_front)

# print('Player 2 lifes: ', player2_board.life)
# print(player2_board.matrix_front)

time.sleep(3)
# Now we are all set to start the game

# ---------------------------- Beginning of the game ----------------------------

# We clear the output
os.system('clear')

turn = 1

print('Player 1 remaining lifes: ', player1_board.life, '\t|\t',
          'Player 2 remaining lifes: ', player2_board.life, '\n')
          
full_board = show_full_front_boards(player1_board.matrix_front, player2_board.matrix_front)

print(full_board, '\n')

while player1_board.life > 25 and player2_board.life > 25:

    print('Player 1 remaining lifes: ', player1_board.life, '\t|\t',
          'Player 2 remaining lifes: ', player2_board.life, '\n')

    # Keep playing or save the game?
    keep_playing = input('Do you want to keep playing(yes) or save the game(no)?\n').lower()
    if keep_playing == 'yes':
        pass

    else:
        game_name = input('Please enter a name to save the game:\n')
        dfs = [player1_board.matrix_front, player1_board.matrix_back, player2_board.matrix_front, player2_board.matrix_back]
        save_game(dfs, game_name)
        print('The game was succesfully saved as:', game_name)
        print('Status summary:\n')
        print('Player 1 remaining lifes: ', player1_board.life, '\n')
        print('Player 2 remaining lifes: ', player2_board.life, '\n')
        print(full_board)
        break
    
    # To keep a track of the turns
    print('-' * 40)
    print("\nIt's the turn - {}\n".format(turn))
    print('-' * 40)
    turn += 1

    # 2) Player 1 turn
    # I show him oponent's front matrix
    print(player2_board.matrix_front)

    # Then, I ask for the guess
    print('Player 1, its your turn:\n')
    player1_guess = ship_coordenates()

    # I update the situation after the attack
    player2_board.pointer(player1_guess)
    player2_board.board_lifes()

    # I show the result
    print('This is your enemy situation after your attack:\n')
    print('Player 2 remaining lifes: ', player2_board.life, '\n')
    print(player2_board.matrix_front)

    # Transition time
    time.sleep(3)

    # 3) Player 2 turn
    # I show him oponent's front matrix
    print(player1_board.matrix_front)

    # Then, I ask for the guess
    print('Player 2, its your turn:\n')
    player2_guess = ship_coordenates()

    # I update the situation after the attack
    player1_board.pointer(player2_guess)
    player1_board.board_lifes()

    # I show the result
    print('This is your enemy situation after your attack:\n')
    print('Player 1 remaining lifes: ', player1_board.life, '\n')
    print(player1_board.matrix_front)

    full_board = show_full_front_boards(player1_board.matrix_front, player2_board.matrix_front)

    # Transition time
    time.sleep(3)

    # We clear the output
    os.system('clear')


# ---------------------------- End of the game ----------------------------
if keep_playing != 'yes':
    pass

else:
    print('End of the game:\n')
    print('keep_playing value:', keep_playing)

    # Print players' remaining lifes
    print('Player 1 - remaining lifes:', player1_board.life)
    print('Player 2 - remaining lifes', player2_board.life)
    print('-' * 40)

    # print winner
    if player1_board.life > player2_board.life:
        print('\nPlayer 1 is the winner!\n')
    if player1_board.life < player2_board.life:
        print('\nPlayer 2 is the winner!\n')
    else:
        print("\nIt's a draw!\n")

    # Print the boards'
    # For that I store player's 1 back matrix in 'result'
    result = player1_board.matrix_back

    # I create a divisor, as I want to print both boards together
    divisor = ['|' for i in range(10)]
    index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    divisor_df = pd.DataFrame(divisor, index = index, columns = ['|'])

    # I join the divisor to player's 1 board and then player's 2 board
    result = pd.merge(result, divisor_df, how = 'outer', right_index = True, left_index = True)
    result = pd.merge(result, player2_board.matrix_back, how = 'outer', right_index = True, left_index = True)

    # I print the result of the game
    print('\n', result)