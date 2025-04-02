from cpi_loader.load_append import load_append
from cpi_loader.load_trunc import load_trunc
from cpi_loader.load_incremental import load_incremental
import duckdb

# Define pull dates to simulate multiple script runs
pull_dates = ["2004-01-15", "2004-02-15"]

# --- Run APPEND method ---
print("Running APPEND method:")
for date in pull_dates:
    print(f"  Loading data for {date}")
    load_append(date)

# --- Run TRUNCATE method ---
print("\nRunning TRUNC method:")
for date in pull_dates:
    print(f"  Loading data for {date}")
    load_trunc(date)

# --- Run INCREMENTAL method ---
print("\nRunning INCREMENTAL method:")
for date in pull_dates:
    print(f"  Loading data for {date}")
    load_incremental(date)

# --- Inspect results ---
con = duckdb.connect("duckdb_cpi.db")

print("\n=== Table Row Counts ===")
for method in ["append", "trunc", "inc"]:
    query = f"""
        SELECT 
            COUNT(*) AS total_rows, 
            COUNT(DISTINCT date) AS unique_dates 
        FROM cpi_{method}
    """
    print(f"cpi_{method}:")
    print(con.execute(query).fetchdf())
