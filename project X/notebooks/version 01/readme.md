## first trial for data load 

1. Archived Source Files -> Archive Schema
2. Latest Source Files -> Bronze Schema
3. Archive Schema -> Silver Schema
4. Bronze Schema -> Silver Schema

Load 1 is a one off hydration loads
Load 3 is a load into Silver loading grouping the data in archive based on export date and performing load.. ensuring adding new rows to target table based on Business key of the table and updating rows where match is found. this is loaded chronologically based on the Export date.. Or alternatively could just get the latest export record for each business Key row
Loads 2 and 4 are are daily Incremental loads, ensuring adding new rows to target table based on Business key of the table and updating rows where match is found.






