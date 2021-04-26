from Classes import *

import os

# ---------------------------- For the beginning of the game ----------------------------
# I ask the users for the coordinates to place their ships
def ask_coordinates():
    # I store the amount and size of the different ships to enter in a dictionary for later use
    ships_to_enter = {'2x1' : {'size' : 2, 'amount' : 4}, '3x1' : {'size' : 3, 'amount' : 3}, '4x1' : {'size' : 4, 'amount' : 2}, '5x1' : {'size' : 5, 'amount' : 1}}

    player_ships = []

    # for every key (2x1, 3x1, ..) 
    for i in ships_to_enter.keys():
        # count to compare with the amount of ships I need of every type
        count = 0
        # while the count is lower than the amount I need, keep going
        while count < ships_to_enter[i]['amount']:
            print('Lets enter the position for your ship {} of size {}'.format(count + 1, i))
            # size will be automatically taken from the dict with amount/size info
            size = ships_to_enter[i]['size']

            # I ask the user for the coordinates
            allignment = input('vertical (v) or horizontal (h): ').lower()
            column = int(input('Column to start counting'))
            row = input('Row to start counting').upper()

            coord = [allignment, column, row]

            # I append the coordinates to the corresponding list within the dictionary
            ship = Ship(size, coord)
            player_ships.append(ship)
            # +1 for the ocunt
            count += 1
            os.system('clear')

        # After every while round, I reset the count
        count = 0

    return player_ships


# ---------------------------- For the game ----------------------------
# I ask the user to guess the location of enemy ships
def ask_enemy_coordinates():
    column = int(input('Column'))
    row = input('Row').upper()
    # I pack both values into a list
    coordinate = [column, row]

    # I return the list, which I'll pass into the pointer method of the boards
    return coordinate