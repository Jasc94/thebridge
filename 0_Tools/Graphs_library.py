## Función para crear varios gráficos a la vez

import seaborn
import matplotlib.pyplot as plt

def graphs():
    #TODO

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey = True)

    sns.histplot(titanic["age"], bins = 10, ax = ax1)
    sns.histplot(titanic["age"], bins = 20, ax = ax2)
    sns.histplot(titanic["age"], bins = 50, ax = ax3)