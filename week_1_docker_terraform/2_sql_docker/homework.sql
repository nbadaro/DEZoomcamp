-- Q: How many taxi trips were totally made on September 18th 2019?
-- A: 15612
WITH filtered_rides AS (
	SELECT
		*
	FROM public.green_trip_data
	WHERE lpep_pickup_datetime::date = '2019-09-18'
	AND lpep_dropoff_datetime::date = '2019-09-18'
)
SELECT
	COUNT(*) as total_rows,
	COUNT(DISTINCT index::varchar) as unique_ids
FROM filtered_rides;


-- Q: Which was the pick up day with the largest trip distance. Use the pick up time for your calculations.
-- A: 2019-09-26
SELECT
	lpep_pickup_datetime::date as pickup_day,
	MAX(trip_distance) as total_day_distance
FROM public.green_trip_data
GROUP BY pickup_day
ORDER BY total_day_distance DESC
LIMIT 1


-- Q: Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown.
-- Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
-- A: "Brooklyn" "Manhattan" "Queens"

WITH filtered_rides AS (
	SELECT
		"PULocationID" as location_id,
		SUM(total_amount) as sum_total_amount
	FROM public.green_trip_data
	WHERE lpep_pickup_datetime::date = '2019-09-18'
	GROUP BY location_id
),
rides_sum AS (
	SELECT
		z."Borough",
		SUM(fr.sum_total_amount) as sum_total_amount
	FROM filtered_rides AS fr
	LEFT JOIN public.zones AS z ON (fr.location_id = z."LocationID" AND z."Borough" != 'Unknown')
	GROUP BY "Borough"
)
SELECT
	*
FROM rides_sum
WHERE sum_total_amount >= 50000;


-- Q: For the passengers picked up in September 2019 in the zone name Astoria,
-- which was the drop off zone that had the largest tip? We want the name of the zone, not the id.
-- A: JFK Airport

WITH max_tip_location AS (
	SELECT
		"DOLocationID" as dropoff_location_id
	FROM public.green_trip_data
	WHERE lpep_pickup_datetime::date >= '2019-09-01'
	AND lpep_pickup_datetime::date <= '2019-09-30'
	AND "PULocationID" = 7
	ORDER BY tip_amount DESC
	LIMIT 1
)
SELECT
	z."Zone"
FROM public.zones AS z
JOIN max_tip_location AS mt ON mt.dropoff_location_id = z."LocationID";


SELECT * FROM public.zones z LIMIT 10;
SELECT * FROM public.green_trip_data LIMIT 10;