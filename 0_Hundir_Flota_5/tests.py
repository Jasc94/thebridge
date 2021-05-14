import matplotlib.pyplot as plt
import seaborn as sns

import classes as c

board1 = c.board('Player 1')

to_plot = board1.backend.replace(['~', '*', 'O', 'X'], [1, 1, 0, -1])

fig, ax1 = plt.subplots(1, sharey = True, figsize = (6.4, 9))
sns.heatmap(to_plot, cmap="BrBG", center = 0, linewidths = 0.5,
            linecolor = "white", ax = ax1)
# sns.heatmap(to_plot, cmap="BrBG", center = 0, linewidths = 0.5,
#             linecolor = "white", ax = ax2)

plt.title('Test', fontdict = {'fontsize': 'xx-large', 'fontweight' : 'bold'})

# {'fontsize': rcParams['axes.titlesize'],
#  'fontweight' : rcParams['axes.titleweight'],
#  'verticalalignment': 'baseline',
#  'horizontalalignment': loc}

ax1.plot()
# ax2.plot()

plt.show()
# plt.pause(10)
# plt.close()