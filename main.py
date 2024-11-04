# from dotenv import load_dotenv
import os
import requests
import pandas as pd

# load_dotenv()

AIRTABLE_KEY = os.environ["airtable_key"]
AIRTABLE_BASE_ID = os.environ["airtable_base_id"]
AIRTABLE_TABLEID = os.environ["airtable_tableid"]
url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLEID}/"
response = requests.get(url, headers={'Authorization': f'Bearer {AIRTABLE_KEY}'})
data = response.json()

# dataframe with Airtable records
df = pd.json_normalize(data['records'])

# drop 'createdTime', 'id'
drop_cols = [0, 1]
df.drop(df.columns[drop_cols],axis=1,inplace=True)

# strip out 'fields.' from column headers
df.columns = df.columns.str.replace("fields.", "", regex=True)

# reorder columns
col_order = ['Name','URL','Instruction','Eligible Residents (Cities)','Description','Applications','Start Date','Benefits']
df = df.reindex(columns=col_order)

# clean text and save to csv
csv_file_path = 'test.csv'
df.to_csv(csv_file_path, index=False, encoding='utf-8')

def clean_text(path):
  df = pd.read_csv(path)
  for column in df.columns:
    df[column] = df[column].str.replace(r"[^a-zA-Z0-9\s,\/\.:\-\$]", "", regex=True)
  return df

df = clean_text(csv_file_path)
df.to_csv(csv_file_path, index=False, encoding='utf-8')


#TODO: Convert CSV to Markdown and append to README either here or in a frontend folder