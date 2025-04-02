from cpi_loader.load_append import load_append
from cpi_loader.load_trunc import load_trunc
from cpi_loader.load_incremental import load_incremental
import duckdb

# Choose the CPI vintage column to test
vintage = "PCPI24M1"

# --- Run APPEND method ---
print("Running APPEND method:")
load_append(vintage)

# --- Run TRUNC method ---
print("Running TRUNC method:")
load_trunc(vintage)

# --- Run INCREMENTAL method ---
print("Running INCREMENTAL method:")
load_incremental(vintage)

# --- Inspect the result ---
con = duckdb.connect("duckdb_cpi.db")

print("\n=== Row counts after loading ===")
for table in ["cpi_append", "cpi_trunc", "cpi_inc"]:
    result = con.execute(f"SELECT COUNT(*) AS rows, COUNT(DISTINCT date) AS unique_dates FROM {table}").fetchdf()
    print(f"{table}:")
    print(result, "\n")