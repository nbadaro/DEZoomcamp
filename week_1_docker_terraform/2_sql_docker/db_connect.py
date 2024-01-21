"""

"""
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()

df_zones = pd.read_csv('taxi+_zone_lookup.csv')

df_zones.head()

df_zones.to_sql(name='zones', con=engine, if_exists='replace')
