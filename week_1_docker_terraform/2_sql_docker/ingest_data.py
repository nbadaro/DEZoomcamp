#!/user/bin/env python
"""
Datasets:
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
"""
import os
import logging
import argparse
import pandas as pd
from sqlalchemy import create_engine


logger = logging.getLogger(__name__)


class CsvPipeline:
    """
    This pipeline downloads the yellow taxi trips data and writes it to a postgres db instance.
    """
    def __init__(self, params):
        self.user = params.user
        self.password = params.password
        self.host = params.host
        self.port = params.port
        self.db = params.db
        self.engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}')

        self.table_name = params.table_name

        self.url = params.url

    @property
    def csv_name(self):
        if self.url.endswith('.csv.gz'):
            return 'output.csv.gz'
        else:
            return 'output.csv'

    def _extract_data(self) -> None:
        """
        """
        logger.info("Downloading dataset...")
        os.system(f"wget {self.url} -O {self.csv_name}")

    def _update_destination(self):
        """
        """
        logger.info("Updating destination table...")
        df_iter = pd.read_csv(
            self.csv_name,
            iterator=True,
            chunksize=100000
        )

        df = next(df_iter)

        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

        df.head(n=0).to_sql(
            name=self.table_name,
            con=self.engine,
            if_exists='replace'
        )

        logger.info("Destination table updated !")

    def _load_data(self) -> None:
        """
        """
        df_iter = pd.read_csv(
            self.csv_name,
            iterator=True,
            chunksize=100000
        )

        while True:
            logger.info("Loading data into db...")
            try:
                df = next(df_iter)

                # Convert pickup and drop-off times from text to datetime
                df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
                df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])

                df.to_sql(name=self.table_name, con=self.engine, if_exists='append')

                logger.info(f'Inserted a chunk')
            except StopIteration:
                logger.info('Finished inserting data')
                break

    def run(self) -> None:
        self._extract_data()
        self._update_destination()
        self._load_data()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CSV ingestion pipeline to Postgres")
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    pipeline = CsvPipeline(params=args)
    pipeline.run()
