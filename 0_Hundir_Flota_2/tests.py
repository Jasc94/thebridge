from Classes import *
from Functions import *

import os
import time

player1_board = Player_board()
player2_board = Player_board()

player1_guess = ship_coordenates()
player2_guess = ship_coordenates()

print(player1_guess)
print(type(player1_guess))
print('-' * 30)
print(player2_guess)
print(type(player2_guess))
print('-' * 30)
print(player2_board.pointer(player1_guess))
print(player1_board.pointer(player2_guess))