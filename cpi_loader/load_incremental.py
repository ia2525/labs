import duckdb
from cpi_loader.get_data import get_data_by_column
import numpy as np

def load_incremental(vintage_col):
    df = get_data_by_column(vintage_col)
    con = duckdb.connect("duckdb_cpi.db")
    con.execute("CREATE TABLE IF NOT EXISTS cpi_inc (date DATE, cpi DOUBLE)")

    # Load existing data
    df_existing = con.execute("SELECT * FROM cpi_inc").fetchdf()

    # Merge on date, find new or changed rows
    df_merged = df.merge(df_existing, on="date", how="left", suffixes=("", "_existing"))
    df_changed = df_merged[df_merged["cpi"] != df_merged["cpi_existing"]]

    # Compare CPI values with some tolerance (e.g., 0.001)
    df_merged["is_changed"] = ~np.isclose(df_merged["cpi"], df_merged["cpi_existing"], atol=0.001)
    df_changed = df_merged[df_merged["is_changed"] | df_merged["cpi_existing"].isna()]

    if not df_changed.empty:
        print(f"Inserting {len(df_changed)} updated or new rows:")
        print(df_changed.head(10))  # preview what it’s catching

        df_changed = df_changed[["date", "cpi"]]

        con.register("df_temp", df_changed)
        con.execute("""
            DELETE FROM cpi_inc
            WHERE date IN (SELECT date FROM df_temp)
        """)
        con.execute("INSERT INTO cpi_inc SELECT * FROM df_temp")
        con.unregister("df_temp")
    else:
        print("No new or revised rows detected.")

    
    
