import os
import requests
import pandas as pd

api_key = os.environ.get("AIRTABLE_KEY")
base = os.environ.get("AIRTABLE_BASE_ID")
table = os.environ.get("AIRTABLE_TABLEID")
url = f"https://api.airtable.com/v0/{base}/{table}/"
headers = {
    f"Authorization: Bearer {api_key}"
}
response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})
data = response.json()

# dataframe
df = pd.json_normalize(data['records'])
col_order = ['fields.Name','fields.URL','fields.Instruction','fields.Eligible Residents (Cities)','fields.Description','fields.Applications','fields.Start Date','fields.Benefits', 'createdTime', 'id', 'fields.City']
df=df.reindex(columns=col_order)

# save to csv
df.to_csv('test.csv', index=False, encoding='utf-8')
