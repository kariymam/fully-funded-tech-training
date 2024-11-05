# from dotenv import load_dotenv
import os
import requests
import pandas as pd
from csv2markdown import update_table

# load_dotenv()

AIRTABLE_KEY = os.environ["airtable_key"]
AIRTABLE_BASE_ID = os.environ["airtable_base_id"]
AIRTABLE_TABLEID = os.environ["airtable_tableid"]
url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLEID}/"
response = requests.get(url, headers={'Authorization': f'Bearer {AIRTABLE_KEY}'})
data = response.json()

# Prepare for CSV
def prep_for_csv(data):
   df = pd.json_normalize(data['records'])
   # drop 'createdTime', 'id'
   df.drop(df.columns[[0, 1]],axis=1,inplace=True)
   # strip out 'fields.' from column headers
   df.columns = df.columns.str.replace("fields.", "", regex=True)
   # reorder columns
   col_order = ['Company','Program','Instruction','Location','Description'] # Removed 'Applications','Start Date', 'Benefits'
   return df.reindex(columns=col_order)

# Save as CSV
df = prep_for_csv(data)
csv_file_path = 'test.csv'
df.to_csv(csv_file_path, index=False, encoding='utf-8')

# Clean columns in csv, excluding specific columns
def clean_text(path, exclude_columns=[]):
   df = pd.read_csv(path)
   for column in df.columns:
     if column not in exclude_columns:
        df[column] = df[column].str.replace(r"[^a-zA-Z0-9\s+,\|\/\.:\-_!?$]", "", regex=True)
   return df

df = clean_text(csv_file_path, exclude_columns=["Description", "Program"])
df.to_csv(csv_file_path, index=False, encoding='utf-8')

# Convert CSV to Markdown table and overwrite table in README.md
markdown_file_path = 'README.md'
update_table(csv_file_path, markdown_file_path) 