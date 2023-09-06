#!/usr/bin/python3 

import pandas as pd
import os

excel_file = "~/Downloads/arnhem.xlsx"

columns_to_extract = ['Addressee Town/City', 'Addressee Province/State', 'Addressee Country']

data = pd.read_excel(excel_file, usecols=columns_to_extract, sheet_name="Box 3 Folders XVI-XXII")
data.columns = ["city", "state", "country"]

# Now we also need to grab the data from the 'Postmark 1 Location' and 'Postmark 2 Location'
# and add them to the city column.
postmark_columns = ['Postmark 1 Location', 'Postmark 2 Location']

postmark_data = pd.read_excel(excel_file, usecols=postmark_columns, sheet_name="Box 3 Folders XVI-XXII")
# Recombine so that the two location columns are a single column of data
postmark_data = pd.concat([postmark_data['Postmark 1 Location'], postmark_data['Postmark 2 Location']])
# Now structure the data. We want to add the postmark data to the city column
postmark_data = postmark_data.to_frame()
postmark_data.columns = ["city"]
postmark_data["state"] = ""
postmark_data["country"] = ""

# Now we need to combine the two dataframes
data = pd.concat([data, postmark_data])

unique_data = data.drop_duplicates()
uniqque_data = data.dropna()

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)
output_csv = os.path.join(output_dir, 'locations.csv')

unique_data.to_csv(output_csv, index=False)

print(f"CSV file of locations created in the '{output_dir}' directory.")
