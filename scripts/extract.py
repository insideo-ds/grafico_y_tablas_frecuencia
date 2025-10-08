import pandas as pd

def extract(path):
    df_extracted = pd.read_excel(path)
    return df_extracted