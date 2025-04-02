import duckdb
from cpi_loader.get_data import get_latest_data

def load_append(pull_date):
    df = get_latest_data(pull_date)
    con = duckdb.connect("duckdb_cpi.db")
    con.execute("CREATE TABLE IF NOT EXISTS cpi_append (date DATE, cpi DOUBLE)")
    con.execute("INSERT INTO cpi_append SELECT * FROM df")
