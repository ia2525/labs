import pandas as pd

def get_data_by_column(vintage_col: str, path="data/pcpiMvMd.xlsx") -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="pcpi", usecols=["DATE", vintage_col])
    df = df.rename(columns={"DATE": "date", vintage_col: "cpi"})
    return df

