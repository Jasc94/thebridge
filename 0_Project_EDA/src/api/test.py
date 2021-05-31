import pandas as pd
import os, sys

#df = pd.read_csv("../../../data/daily_intakes.csv")
#print(df.head())
#print(__file__)

dir = os.path.dirname
path_up = dir(__file__)

for i in range(2): path_up = dir(path_up)

path_down = path_up + os.sep + "data"

df = pd.read_csv(path_down + os.sep + "daily_intakes.csv")
print(df.head())