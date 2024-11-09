import os
import re
import requests
import pandas as pd

def fetch_airtable():
    AIRTABLE_KEY = os.environ["airtable_key"]
    AIRTABLE_BASE_ID = os.environ["airtable_base_id"]
    AIRTABLE_TABLEID = os.environ["airtable_tableid"]
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLEID}/"
    response = requests.get(url, headers={'Authorization': f'Bearer {AIRTABLE_KEY}'})
    return response.json()


def prepare_csv(data, path_to_export, exclude_columns: str = []):
    df = pd.json_normalize(data['records'])

    # Strip out 'fields.' from column headers
    df = df.rename(columns=lambda name: re.sub(r"^fields.", "", name, flags = re.M) if name.startswith('fields.') else name)

    # Drop unselected columns
    selected_columns = ['Company','Program','Instruction','Location','Description']
    df = df.reindex(columns=selected_columns)

    # Create a temp csv file to clean text columns in csv
    df.to_csv(path_to_export, index=False, encoding='utf-8')

    # Read CSV file
    temp = pd.read_csv(path_to_export)

    # Clean the multiselect Airtable tags that look like ['This'], so remove formatting with regex function
    for column in temp.columns:
      temp[column] = pd.Series(temp[column], dtype="string")
      if column not in exclude_columns:
        temp[column] = temp[column].str.replace(r"[\[\[\]\']", "", regex=True)
    return temp.to_csv(path_to_export, index=False, encoding='utf-8')

# Define Markdown table 
def mkd_table_regex():
    rgx = r"((\r?\n){2}|^)([^\r\n]*\|[^\r\n]*(\r?\n)?)+(?=(\r?\n){2}|$)"
    return rgx

# Find Markdown table
def find_table(path: str) -> bool:
    with open(path, "r") as f:
        content = f.read()

        # Use regex to find Markdown table in file content
        try:
            match = re.findall(mkd_table_regex(), content, flags=re.M)
            return bool(match)
        # Throw an error if can't determine a table exists
        except IndexError:
            print("Can't determine if table exists")
            raise

# Update Markdown table in README.md
def update_table(csv_path, markdown_path):
    df = pd.read_csv(csv_path)

    # Convert CSV to Markdown
    markdown_table = df.to_markdown()

    # Run find_table check
    check = find_table(markdown_path)

    # In the markdown file
    with open (markdown_path, 'r' ) as f:
        content = f.read()
        replace_table = re.sub(mkd_table_regex(), f"\n\n{markdown_table}", content, flags = re.M)
        if check is True:
            # Overwrite table at the end of the file
            with open(markdown_path, 'w') as f:
                f.write(replace_table)
        elif check is False:
            # Append table to the end of the file
            with open(markdown_path, 'a') as f:
                f.write('\n\n'+markdown_table)

def main():
    data = fetch_airtable()
    csv_file_path = 'test.csv'
    markdown_file_path = 'README.md'

    # Clean CSV multiselect text, excluding columns with markdown links
    prepare_csv(data, csv_file_path, exclude_columns=["Description", "Program"])

    # Convert to Markdown table overwrite table in README.md
    update_table(csv_file_path, markdown_file_path)

main()