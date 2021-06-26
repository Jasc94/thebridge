import pandas as pd
import numpy as np

def column_names(df, column_names_dict):
    df.columns = column_names_dict["Description"].values()
    return df

def column_mapper(df, columns, dicts):
    try:
        for tup in dict(zip(columns, dicts)).items():
            df[tup[0]] = df[tup[0]].map(tup[1])
        return df

    except:
        raise ValueError("Check that 'columns' and 'dicts' parameters are lists")