import duckdb
from cpi_loader.get_data import get_latest_data

def load_trunc(pull_date):
    df = get_latest_data(pull_date)
    con = duckdb.connect("duckdb_cpi.db")
    con.execute("DROP TABLE IF EXISTS cpi_trunc")
    con.execute("CREATE TABLE cpi_trunc AS SELECT * FROM df")
