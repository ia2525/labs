import pandas as pd

def get_data_by_column(vintage_col: str, path="data/pcpiMvMd.xlsx") -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="pcpi", usecols=["DATE", vintage_col])
    
    # Convert from 'YYYY:MM' to datetime (first day of month)
    df["DATE"] = pd.to_datetime(df["DATE"].str.replace(":", "-") + "-01")

    df = df.rename(columns={"DATE": "date", vintage_col: "cpi"})
    return df