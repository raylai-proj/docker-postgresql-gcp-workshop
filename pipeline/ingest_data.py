#!/usr/bin/env python
# coding: utf-8



import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


YEAR = "2021"
MONTH = "01"

DATA_SOURCE_PREFIX = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
DATA_VERSION = f'yellow_tripdata_{YEAR}-{MONTH}.csv.gz'
DTYPE = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "Float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "str",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "Float64",
    "extra": "Float64",
    "mta_tax": "Float64",
    "tip_amount": "Float64",
    "tolls_amount": "Float64",
    "improvement_surcharge": "Float64",
    "total_amount": "Float64",
    "congestion_surcharge": "Float64",
}
PARSE_DATE = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

POSTGRES = "postgresql"
PG_USER = "root"
PG_PASSWORD = "root"
PG_LOCALHOST = "localhost"
PG_PORT = "5432"
PG_DB = "ny_taxi"
CHUNK_SZ = 100000
TABLE_NAME = "yellow_taxi_data"

# check if pandas exist
# pd.__file__

# df = pd.read_csv(DATA_SOURCE_PREFIX+DATA_VERSION, nrows=100)
df = pd.read_csv(
    DATA_SOURCE_PREFIX+DATA_VERSION,
    dtype=DTYPE,
    parse_dates=PARSE_DATE,
)


# In[5]:


# df.head()


# In[6]:


# df['VendorID']


# In[7]:


# df['tpep_pickup_datetime']


# In[8]:


# df.dtypes


# In[9]:


# df.shape


# In[10]:


# len(df)


# In[11]:


# !uv add sqlalchemy
# !uv add psycopg2-binary


# In[12]:


# create sqlalchemy engine
engine = create_engine(f'{POSTGRES}://{PG_USER}:{PG_PASSWORD}@{PG_LOCALHOST}:{PG_PORT}/{PG_DB}')


# In[13]:


# Ppreview SQL statement to create table
# 1. get schema from dataframe df,
# 2. get table name from name='yellow_taxi_data',
# 3. generate "postgresql" statement based on con=engine where engine was created for postgresql database in docker
print(pd.io.sql.get_schema(df, name='TABLE_NAME', con=engine))


# In[14]:


# df.head(0)


# In[15]:


# create empty table with schema only (column name + dtype)
df.head(0).to_sql(
    name='TABLE_NAME',
    con=engine,
    if_exists='replace',
)


# In[16]:


df_iter = pd.read_csv(
    DATA_SOURCE_PREFIX+DATA_VERSION,
    dtype=DTYPE,
    parse_dates=PARSE_DATE,
    iterator=True,
    chunksize=CHUNK_SZ,
)


# In[17]:


# df_iter


# In[18]:


# install tqdm and from tqdm.auto import tqdm to see progress of inserting data
# !uv add tqdm


# In[19]:


for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(
        name='TABLE_NAME',
        con=engine,
        if_exists='append'
    )


# In[ ]:




