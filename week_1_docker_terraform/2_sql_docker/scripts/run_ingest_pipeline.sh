docker run -it --net=2_sql_docker_pgnetwork taxi:v001 \
  --user="root" \
  --password="root" \
  --host="pgdatabase" \
  --port="5432" \
  --db="ny_taxi" \
  --table_name="green_trip_data" \
  --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
