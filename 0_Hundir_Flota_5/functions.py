import classes as c
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


# ---------------------------- For the beginning of the game ----------------------------
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

            ship = c.ship([column, row, allignment, size])
            player_ships.append(ship)

            count += 1

        count = 0

    return player_ships