import duckdb
from cpi_loader.get_data import get_data_by_column

def load_trunc(vintage_col):
    df = get_data_by_column(vintage_col)
    con = duckdb.connect("duckdb_cpi.db")
    con.execute("DROP TABLE IF EXISTS cpi_trunc")
    con.execute("CREATE TABLE cpi_trunc AS SELECT * FROM df")
