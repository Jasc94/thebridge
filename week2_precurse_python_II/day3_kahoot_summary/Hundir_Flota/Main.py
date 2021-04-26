from Classes import *
from Functions import *

import os
import time

#player1 = Player_board()
#print(player1.matrix_front)

#a = ['v', 8, 'G']
#ship1 = Ship(2, a)
#ship2 = Ship(2, a)
#ship3 = Ship(2, a)
#ships = [ship1, ship2, ship3]
#for i in ships:
#    print(i.attributes())


# ---------------------------- Game preparation ----------------------------
# 1) Create empty player boards
player1_board = Player_board()
player2_board = Player_board()

# 2) Ask players for the coordenates
print('Player 1, please place your ships:\n')
player1_ships = ask_coordinates()
print('Player 2, please place your ships:\n')
player2_ships = ask_coordinates()

# 3) Draw the ships
for i in range(len(player1_ships)):
    # I loop through the player1 ships
    to_draw_1 = player1_ships[i].attributes()[:-1]
    player1_board.ship_drawer(to_draw_1)

    # I loop through the player 2 ships
    to_draw_2 = player2_ships[i].attributes()[:-1]
    player2_board.ship_drawer(to_draw_2)

# I clear the output before further continuing
#os.system('clear')

# 4) I update the boards lifes situation
player1_board.board_lifes()
player2_board.board_lifes()

print('Player 1 lifes: ', player1_board.life)
print(player1_board.matrix_front)

print('Player 2 lifes: ', player2_board.life)
print(player2_board.matrix_front)

time.sleep(3)
# Now we are all set to start the game

# ---------------------------- Game start ----------------------------

while player1_board.life > 25 and player2_board.life > 25:
    # 1) I print the initial situation
    print('Player 1 lifes: ', player1_board.life)
    print(player1_board.matrix_front)

    print('Player 2 lifes: ', player2_board.life)
    print(player2_board.matrix_front)

    # 2) Player 1 turn
    # I ask for the guess
    print('Player 1, its your turn:\n')
    player1_guess = ask_enemy_coordinates()

    # I update the situation after the attack
    player2_board.pointer(player1_guess)
    player2_board.board_lifes()

    # I show the result
    print('This is your enemy situation after your attack')
    print(player2_board.life)
    #print(player2_board.matrix_back)
    print(player2_board.matrix_front)


    # 3) Player 2 turn
    # I ask for the guess
    print('Player 2, its your turn:\n')
    player2_guess = ask_enemy_coordinates()

    # I update the situation after the attack
    player1_board.pointer(player2_guess)
    player1_board.board_lifes()

    # I show the result
    print('This is your enemy situation after your attack')
    print(player1_board.life)
    #print(player1_board.matrix_back)
    print(player1_board.matrix_front)

    time.sleep(5)
    # We clear the output
    os.system('clear')

print('End of the game:\n')
print('Player 1 end lives:', player1_board.life)
print('Player 2 end lives:', player2_board.life)