import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
import sys
from varname import nameof


import classes as c
import functions as f

# board1 = c.board('Player 1')

# to_plot = board1.backend.replace(['~', '*', 'O', 'X'], [1, 1, 0, -1])

# fig, (ax1, ax2) = plt.subplots(1, 2, sharey = True, figsize = (10, 10))

# sns.heatmap(to_plot, cmap="BrBG", center = 0, linewidths = 0.5,
#             linecolor = "white", square = True, cbar = False, ax = ax1)

# sns.heatmap(to_plot, cmap="BrBG", center = 0, linewidths = 0.5,
#             linecolor = "white", square = True, cbar = False, ax = ax2)

# fig.suptitle('\n\nTurn 1', fontsize=16)

# ax1.set_title('Player 1')
# ax2.set_title('Player 2')


# plt.show()
# time.sleep(3)
# plt.close('all')


# test = input('escribe algo')
# print(test)

# a, b = f.load_old_game("third_attempt")
# print(a)
# print('-' * 90)
# print(b)

a = f.show_saved_games()
a

