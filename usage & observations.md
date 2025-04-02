Manual Testing Instruction

This repository was created precisely for testing this function. You should be working from the "Labs" folder, under which you will see the pcpiMvMd excel file, which we will primarily be working with. I have created a simple function in get_data.py which reads the excel file and extracts two columns: dates from column 1 and the desired vintage as "cpi" in column 2.

We then run test_methods.py to store the data into a duckdb database via the following methods: append, trunc, and incremental to understand how they work differently. 

You can run it multiple times, first by extracting cpi data from PCPI24MI vintage and you will observe the following:

Append: Starts with 924 rows & unique dates, but table keeps growing - duplicating the number of rows with each run of test_methods, as append will simply stack new information in consequent rows. (I ran it two times to check the rows doubled in size - then cleaned it to start over).

Truncate: Table is wiped and replaced with current pull's data per run. So when you run your second vintage - all the old data will get wiped and you will be left with only new cpi values. Because now 2025M2 has more cpi data, you will see 937 instead of 924 rows - however, all these belong to cpi data from 2025M2

Incremental: Table grows, but no duplicates for the same date. This means that as you run the second vintage - the number of rows grows from 924 to 937, instead of all old values being wiped - only revisions replace old values and new values (from dates extending beyond those covered in 2024M1) are added. So like truncate, you will have 937 rows and techinically all the same data - this might be useful if you want faster performance when working with larger datasets, as incremental only chaned 71 rows and truncate replaced 937.

I then added a benchmark_methods.py and verified that after two runs/ two vintages parsed through the database loading methods - incremental was the fastest method of the three & I imagine with more vintages it will surpoass trunc by a bigger margin