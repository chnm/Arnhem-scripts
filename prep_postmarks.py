#!/usr/bin/python3 

import pandas as pd
import os
from datetime import datetime

filename = "~/Downloads/arnhem.xlsx"
sheet_name = "Box 3 Folders XVI-XXII"

columns_to_extract = ['Postmark 1 Date', 'Postmark 1 Location', 'Postmark 2 Date', 'Postmark 2 Location']

data = pd.read_excel(filename, usecols=columns_to_extract, sheet_name=sheet_name)

# First, we need to rename the columns to make them easier to work with
data = data.rename(columns={'Postmark 1 Date': 'Date 1', 'Postmark 1 Location': 'Location 1', 'Postmark 2 Date': 'Date 2', 'Postmark 2 Location': 'Location 2'})

# Next, we need to create a new dataframe with the columns we want
new_data = pd.DataFrame(columns=['date', 'location'])

# Now, we need to loop through the data and add the rows to the new dataframe
for index, row in data.iterrows():
    if pd.isnull(row['Location 1']):
        continue

    try:
        row['Date 1'] = pd.to_datetime(row['Date 1'], errors='coerce')
        row['Date 1'] = row['Date 1'].strftime('%Y-%m-%d')
    except:
        pass

    try:
        row['Date 2'] = row['Date 2'].strftime('%Y-%m-%d')
        row['Date 2'] = row['Date 2'].strftime('%Y-%m-%d')
    except:
        pass

    if pd.isnull(row['Date 1']):
        row['Date 1'] = "Date unknown"

    if pd.isnull(row['Date 2']):
        row['Date 2'] = "Date unknown"

    new_data = pd.concat([new_data, pd.DataFrame({'date': [row['Date 1']], 'location': [row['Location 1']]})])
    new_data = pd.concat([new_data, pd.DataFrame({'date': [row['Date 2']], 'location': [row['Location 2']]})])

# Drop rows that have no location 
new_data = new_data.dropna(subset=['location'])

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)
output_csv = os.path.join(output_dir, 'postmarks.csv')

# Save the new dataframe as a CSV
new_data.to_csv(output_csv, index=False)
print(f"CSV file created with unique postmarks in the '{output_dir}' directory.")
