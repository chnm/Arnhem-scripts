#!/usr/bin/python3 

import pandas as pd

excel_file = "~/Downloads/arnhem.xlsx"

columns_to_extract = ['Addressee Town/City', 'Addressee Province/State', 'Addressee Country']

data = pd.read_excel(excel_file, usecols=columns_to_extract, sheet_name="Box 3 Folders XVI-XXII")
data.columns = ["city", "state", "country"]

unique_data = data.drop_duplicates()

output_csv = 'locations.csv'

unique_data.to_csv(output_csv, index=False)

print("CSV file created.")
