Manual Testing Instruction

This repository was created precisely for testing this function. You should be working from the "Labs" folder, under which you will see the pcpiMvMd excel file, which we will primarily be working with. I have created a simple function in get_data.py which reads the excel file and extracts two columns: dates from column 1 and the desired vintage as "cpi" in column 2.

We then run test_methods.py to store the data into a duckdb database via the following methods: append, trunc, and incremental to understand how they work differently. 

You can run it multiple times, first by extracting cpi data from PCPI24MI vintage and you will observe the following:

Append: Starts with 938 rows & unique dates, but table keeps growing - duplicating the number of rows with each run of test_methods, as append will simply stack new information in consequent rows. (I ran it three times to check this and reached 2814 rows - then cleaned it to start over).

Trunc: Table is wiped and replaced with current pull's data per run. So when you run your second vintage - all the old data will get wiped and you will be left with only new cpi values.

Incremental: Table grows, but no duplicates for the same date. This means that as you run the second vintage - the number of rows will not grow, but any cpi revisions will replace older values. So while in this case you techinically will get the same result as truncate, it may be useful for when there are additional