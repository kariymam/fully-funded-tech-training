import re
import pandas as pd

# Regex for finding a table
rgx = r"((\r?\n){2}|^)([^\r\n]*\|[^\r\n]*(\r?\n)?)+(?=(\r?\n){2}|$)"

# Check if there's a table in README.md
def find_table(path: str):
    with open(path, "r") as f:
        content = f.read()
        file_str = content
        try:
            match = re.findall(rgx, file_str, flags=re.M)
            return bool(match)
        except IndexError:
            print("Can't determine if table exists in README")
            raise

# Update table in README.md
def update_table(csv_path, markdown_path):
    df = pd.read_csv(csv_path)
    markdown_table = df.to_markdown()
    check = find_table(markdown_path)
    with open (markdown_path, 'r' ) as f:
        content = f.read()
        replace_table = re.sub(rgx, f"\n\n{markdown_table}", content, flags = re.M)
        if check is True:
            # Overwrite table at the end of the file
            with open(markdown_path, 'w') as f:
                f.write(replace_table)
        elif check is False:
            # Append table to the end of the file
            with open(markdown_path, 'a') as f:
                f.write('\n\n'+markdown_table)