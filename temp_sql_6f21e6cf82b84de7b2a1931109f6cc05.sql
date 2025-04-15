
    SET enable_profiling = JSON;
    SET profiling_output = './profile_output/profile_10MB.csv.json';

    DROP TABLE IF EXISTS t;
    CREATE TABLE t AS SELECT * FROM read_csv_auto('./data/10MB.csv');
    