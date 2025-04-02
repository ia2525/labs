import duckdb
from cpi_loader.get_data import get_data_by_column

def load_append(vintage_col):
    df = get_data_by_column(vintage_col)
    con = duckdb.connect("duckdb_cpi.db")
    con.execute("CREATE TABLE IF NOT EXISTS cpi_append (date DATE, cpi DOUBLE)")
    con.execute("INSERT INTO cpi_append SELECT * FROM df")
