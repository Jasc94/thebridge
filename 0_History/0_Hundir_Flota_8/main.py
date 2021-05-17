import sys
import os

sys.path.append(os.path.dirname(__file__) + '/Utils')

from Utils import game

if __name__ == "__main__":
    game.game()