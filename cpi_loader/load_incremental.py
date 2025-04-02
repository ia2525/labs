import duckdb
from cpi_loader.get_data import get_data_by_column

def load_incremental(vintage_col):
    df = get_data_by_column(vintage_col)
    con = duckdb.connect("duckdb_cpi.db")
    con.execute("CREATE TABLE IF NOT EXISTS cpi_inc (date DATE, cpi DOUBLE)")

    # Avoid duplication by checking for existing dates
    df_existing = con.execute("SELECT DISTINCT date FROM cpi_inc").fetchdf()
    df_new = df[~df["date"].isin(df_existing["date"])]

    if not df_new.empty:
        con.execute("INSERT INTO cpi_inc SELECT * FROM df_new", {"df_new": df_new})
