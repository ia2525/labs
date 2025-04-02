import pandas as pd

def get_data_by_column(vintage_col: str, path="data/pcpiMvMd.xlsx") -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="pcpi", usecols=["DATE", vintage_col])
    df["DATE"] = pd.to_datetime(df["DATE"].str.replace(":", "-") + "-01", errors='coerce')
    df = df.rename(columns={"DATE": "date", vintage_col: "cpi"})

    # Convert CPI to numeric, coercing #N/A and other non-numeric to NaN
    df["cpi"] = pd.to_numeric(df["cpi"], errors="coerce")

    # Drop missing CPI values
    df = df.dropna(subset=["cpi"])

    return df
