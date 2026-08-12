#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
import click
# from tqdm.auto import tqdm

DATA_SOURCE_PREFIX = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/"
ZONE_DATA = "taxi_zone_lookup.csv"

POSTGRES = "postgresql"
PG_USER = "root"
PG_PASS = "root"
PG_DB = "ny_taxi"
PG_HOST = "localhost"
PG_PORT = "5432"
INGEST_TABLE = "zones"

@click.command()
@click.option('--pg-user', default=PG_USER, help='PostgreSQL user (default:root)')
@click.option('--pg-pass', default=PG_PASS, help='PostgreSQL password (default:root)')
@click.option('--pg-host', default=PG_HOST, help='PostgreSQL host (default:localhost)')
@click.option('--pg-port', default=PG_PORT, help='PostgreSQL port (default:5432)')
@click.option('--pg-db', default=PG_DB, help='PostgreSQL db (default:ny_taxi)')
@click.option('--ingest-table', default=INGEST_TABLE, help='table name to ingest (default:zones)')
def ingest_taxi_zone_data(pg_user, pg_pass, pg_host, pg_port, pg_db, ingest_table):
    zone_df = pd.read_csv(DATA_SOURCE_PREFIX+ZONE_DATA)
    engine = create_engine(f"{POSTGRES}://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")
    zone_df.to_sql(name=ingest_table, con=engine, if_exists='replace')

if __name__ == "__main__":
    ingest_taxi_zone_data()

# In[37]:


# # checking if downloading requires authentication
# import requests
# response = requests.get("https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv")
# print("\n".join(response.text.splitlines()[:100]))


# In[38]:


# !ls


# In[39]:


# check if pandas exist
# pd.__file__


# In[40]:




# In[44]:


# zone_df.head(10)


# In[42]:




# In[43]:




# In[45]:

# # preview taxi zone lookup table schema
# print(pd.io.sql.get_schema(zone_df, name=INGEST_TABLE_NAME, con=engine))


# In[47]:


# zone_df.shape


# In[48]:




# In[ ]:




