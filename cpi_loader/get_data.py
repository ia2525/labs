import pandas as pd
import os
from datetime import datetime

def get_latest_data(pull_date: str, data_dir="data") -> pd.DataFrame:
    pull_dt = datetime.strptime(pull_date, "%Y-%m-%d")

    files = [f for f in os.listdir(data_dir) if f.startswith("PCPI") and f.endswith(".xlsx")]
    latest_file = None
    latest_date = None

    for file in files:
        try:
            vintage_str = file[4:9]  # e.g., '24M1'
            vintage_dt = datetime.strptime(vintage_str, "%yM%m")
            if vintage_dt <= pull_dt:
                if latest_date is None or vintage_dt > latest_date:
                    latest_file = file
                    latest_date = vintage_dt
        except Exception:
            continue

    if latest_file is None:
        raise ValueError("No vintage available for given pull date")

    df = pd.read_excel(os.path.join(data_dir, latest_file))
    return df[["date", "cpi"]]
