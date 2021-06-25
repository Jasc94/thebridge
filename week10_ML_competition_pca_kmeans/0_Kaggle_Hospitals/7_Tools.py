import pandas as pd
import numpy as np

def column_names(df, column_names_dict):
    df.columns = column_names_dict["Description"].values()
    return df