import re
import pandas as pd

# File path to csv file
markdown_file_path = 'README.md'
csv_file_path = 'test.csv'
rgx = r"((\r?\n){2}|^)([^\r\n]*\|[^\r\n]*(\r?\n)?)+(?=(\r?\n){2}|$)"
df = pd.read_csv(csv_file_path) 
markdown_table = df.to_markdown()

#Check if there's a table in README.md
def find_table(path, regex):
    with open(path, "r") as f:
        content = f.read()
        file_str = content
        try:
            match = re.findall(regex, file_str, flags=re.M)
            return bool(match)
        except:
            return print("There's something weird going on here")

def update_table(path, regex):
    check = find_table(path, regex)
    with open (path, 'r' ) as f:
        content = f.read()
        replace_table = re.sub(regex, f"\n{markdown_table}", content, flags = re.M)
        if check is True:
            # Overwrite table at the end of the file
            with open(path, 'w') as f:
                f.write(replace_table)
        elif check is False:
            # Append table to the end of the file
            with open(path, 'a') as f:
                f.write('\n'+ markdown_table)

update_table(markdown_file_path, rgx)

#TODO: Convert CSV to Markdown and append to README.md either here or in a frontend folder