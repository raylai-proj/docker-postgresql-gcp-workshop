#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pandas as pd
from sqlalchemy import create_engine
# from tqdm.auto import tqdm


# In[36]:


DATA_SOURCE_PREFIX = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/"
ZONE_DATA = "taxi_zone_lookup.csv"


# In[37]:


# # checking if downloading requires authentication
# import requests
# response = requests.get("https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv")
# print("\n".join(response.text.splitlines()[:100]))


# In[38]:


# !ls


# In[39]:


# check if pandas exist
pd.__file__


# In[40]:


zone_df = pd.read_csv(DATA_SOURCE_PREFIX+ZONE_DATA)


# In[44]:


# zone_df.head(10)


# In[42]:


POSTGRES = "postgresql"
PG_USER = "root"
PG_PASS = "root"
PG_DB = "ny_taxi"
PG_HOST = "localhost"
PG_PORT = "5432"
INGEST_TABLE_NAME = "zones"


# In[43]:


engine = create_engine(f"{POSTGRES}://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}")


# In[45]:


print(pd.io.sql.get_schema(zone_df, name=INGEST_TABLE_NAME, con=engine))


# In[47]:


zone_df.shape


# In[48]:


zone_df.to_sql(name=INGEST_TABLE_NAME, con=engine, if_exists='replace')


# In[ ]:




