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
df=df.reindex(columns=col_order)

# save to csv
df.to_csv('test.csv', index=False, encoding='utf-8')
