import os
import time

import classes as c
import functions as f

board1 = c.board('Player 1')
board2 = c.board('Player 2')

# board1.frontend_creator()
# board2.frontend_creator()

# 2) Ask players for the coordenates
print('Player 1, please place your ships:\n')
p1_ships = f.ask_coordenates()
os.system('clear')

print('Player 2, please place your ships:\n')
p2_ships = f.ask_coordenates()

# 3) Draw the ships
for i in range(len(p1_ships)):
    # I loop through the player1 ships
    to_draw_1 = p1_ships[i].attributes()[:-1]
    board1.ship_drawer(to_draw_1)

    # I loop through the player 2 ships
    to_draw_2 = p2_ships[i].attributes()[:-1]
    board2.ship_drawer(to_draw_2)

print('Método: ', board1.board_lifes())
print('Atributo: ', board1.life)
print(board1.backend)

# time.sleep(3)
# os.system('clear')

# board1.frontend_creator()
# board2.frontend_creator()
