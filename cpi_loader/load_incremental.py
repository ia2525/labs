import duckdb
from cpi_loader.get_data import get_latest_data

def load_incremental(pull_date):
    df = get_latest_data(pull_date)
    con = duckdb.connect("duckdb_cpi.db")
    con.execute("CREATE TABLE IF NOT EXISTS cpi_inc (date DATE, cpi DOUBLE)")
    
    # Avoids duplication
    df_existing = con.execute("SELECT DISTINCT date FROM cpi_inc").fetchdf()
    df_new = df[~df["date"].isin(df_existing["date"])]
    
    if not df_new.empty:
        con.execute("INSERT INTO cpi_inc SELECT * FROM df_new")
