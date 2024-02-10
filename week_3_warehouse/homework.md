-- Create our external table referring to the partitioned 2022 green taxi data stored as parquet files
CREATE OR REPLACE EXTERNAL TABLE ny_taxi_dataset.green_taxi_data_external
OPTIONS (
  format='PARQUET',
  uris=['gs://my-project-mage-data-bucket/green_taxi_2022/*.parquet']
);

-- Count number of records
-- 840402
SELECT SUM(1) FROM ny_taxi_dataset.green_taxi_data_external;


-- Create a non-partitioned internal table
-- Number of rows
-- 840,402
-- Total logical bytes
-- 120.52 MB
-- Active logical bytes
-- 120.52 MB
CREATE OR REPLACE TABLE ny_taxi_dataset.green_taxi_data_internal AS 
SELECT 
  * EXCEPT(lpep_pickup_datetime, lpep_dropoff_datetime),
  TIMESTAMP_MICROS(CAST(lpep_pickup_datetime/1000 AS INT64)) AS lpep_pickup_time,
  TIMESTAMP_MICROS(CAST(lpep_dropoff_datetime/1000 AS INT64)) AS lpep_dropoff_time,
FROM ny_taxi_dataset.green_taxi_data_external;

-- Get table sizes
SELECT
  *,
  ROUND(size_bytes / (1024 * 1024), 2) AS size_mb
FROM
  `my-project.ny_taxi_dataset.__TABLES__`;


-- Count Distinct pu_location_id in both tables
SELECT COUNT(DISTINCT pu_location_id) FROM ny_taxi_dataset.green_taxi_data_internal;

SELECT COUNT(DISTINCT pu_location_id) FROM ny_taxi_dataset.green_taxi_data_external;

-- Create a table with partition on the pickup time
CREATE OR REPLACE TABLE ny_taxi_dataset.green_taxi_data_partition
PARTITION BY
  DATE(lpep_pickup_time)
AS SELECT * FROM ny_taxi_dataset.green_taxi_data_internal;


-- Count number of fares where amount is zero
SELECT COUNT(*) FROM ny_taxi_dataset.green_taxi_data_internal WHERE fare_amount = 0;


-- Get distinct pu_location_id in the partitioned and non-partitioned tables and compare
SELECT DISTINCT pu_location_id FROM ny_taxi_dataset.green_taxi_data_partition
WHERE lpep_pickup_time BETWEEN '2022-06-01' AND '2022-06-30';

SELECT DISTINCT pu_location_id FROM ny_taxi_dataset.green_taxi_data_internal
WHERE lpep_pickup_time BETWEEN '2022-06-01' AND '2022-06-30';



