import duckdb

con = duckdb.connect("duckdb_cpi.db")

for table in ["cpi_append", "cpi_trunc", "cpi_inc"]:
    print(f"=== {table} ===")
    df = con.execute(f"SELECT * FROM {table} ORDER BY date LIMIT 10").fetchdf()
    print(df)
    print("\n")
