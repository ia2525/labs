import time
import duckdb
from cpi_loader.load_append import load_append
from cpi_loader.load_trunc import load_trunc
from cpi_loader.load_incremental import load_incremental
import os

# Vintages to test (can repeat same vintage to test duplication/replacement behavior)
vintages = ["PCPI24M1", "PCPI25M2"] # comparing speeds as database grows & changes

# Helper to run and time a full test sequence
def time_method(method_func, method_name, table_name):
    # Reset database before all three tests to ensure fair comparison
    if os.path.exists("duckdb_cpi.db"):
        os.remove("duckdb_cpi.db")

    con = duckdb.connect("duckdb_cpi.db")

    print(f"\nRunning {method_name.upper()} method")
    start = time.time()

    for vintage in vintages:
        method_func(vintage)

    duration = time.time() - start

    # Count final rows and unique dates
    summary = con.execute(f"""
        SELECT COUNT(*) AS rows, COUNT(DISTINCT date) AS unique_dates
        FROM {table_name}
    """).fetchdf()

    return {
        "method": method_name,
        "time": duration,
        "rows": summary.loc[0, "rows"],
        "unique_dates": summary.loc[0, "unique_dates"]
    }

# Run all tests in sequence on the same vintages
if __name__ == "__main__":
    print("=== Benchmarking Append vs Trunc vs Incremental ===")

    results = [
        time_method(load_append, "append", "cpi_append"),
        time_method(load_trunc, "trunc", "cpi_trunc"),
        time_method(load_incremental, "incremental", "cpi_inc"),
    ]

    print("\n=== Summary ===")
    for res in results:
        print(f"{res['method'].ljust(12)} | Time: {res['time']:.4f}s | Rows: {res['rows']} | Unique Dates: {res['unique_dates']}")
