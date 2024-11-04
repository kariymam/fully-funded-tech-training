import os
import requests
import pandas as pd

AIRTABLE_KEY = os.environ["airtable_key"]
AIRTABLE_BASE_ID = os.environ["airtable_base_id"]
AIRTABLE_TABLEID = os.environ["airtable_tableid"]
url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLEID}/"
response = requests.get(url, headers={'Authorization': f'Bearer {AIRTABLE_KEY}'})
data = response.json()

# dataframe
df = pd.json_normalize(data['records'])
col_order = ['fields.Name','fields.URL','fields.Instruction','fields.Eligible Residents (Cities)','fields.Description','fields.Applications','fields.Start Date','fields.Benefits', 'createdTime', 'id', 'fields.City']
df=df.reindex(columns=col_order) # reorder columns
df.drop(columns=['createdTime', 'id', 'fields.City'],axis=1,inplace=True)  # drop columns

# save to csv
df.to_csv('test.csv', index=False, encoding='utf-8')

#TODO: Figure out how to remove brackets from Eligible Residents & Benefits, and cleanup header names by removing 'fields.' from th first 8
#TODO: Convert CSV to Markdown and append to README either here or in a frontend folder