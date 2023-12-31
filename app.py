import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query('''SELECT * FROM `sunpower-375201.sunpower_agg.sunpower_full_funnel` WHERE Date = "2023-10-17" LIMIT 10''')

# Print results.
st.header("Show a cell from each row individually")
st.write("Query Results:")
for row in rows:
    st.write("✍️ " + row['Campaign'])

import pandas_gbq
import pandas 

query = '''SELECT * FROM `sunpower-375201.sunpower_agg.sunpower_full_funnel` WHERE Date = "2023-10-17" LIMIT 10'''
df = pandas.read_gbq(query, credentials=credentials)

st.header("Write Query as a dataframe w/ pandas")
st.write(df)
