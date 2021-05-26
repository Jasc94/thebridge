import pandas as pd
import base58


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    #b58 = base58.b58encode(csv.encode()).decode()
    #b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:csv{csv}" download="table.csv">Download csv file</a>'
    return href