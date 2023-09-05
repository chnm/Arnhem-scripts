#!/usr/bin/python3 

import pandas as pd
import os

excel_file = "~/Downloads/arnhem.xlsx"

columns_to_extract = ['Addressee Town/City', 'Addressee Province/State', 'Addressee Country']

data = pd.read_excel(excel_file, usecols=columns_to_extract, sheet_name="Box 3 Folders XVI-XXII")
data.columns = ["city", "state", "country"]

unique_data = data.drop_duplicates()

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)
output_csv = os.path.join(output_dir, 'locations.csv')

unique_data.to_csv(output_csv, index=False)

print(f"CSV file of locations created in the '{output_dir}' directory.")
