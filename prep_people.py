#!/usr/bin/python3 

import pandas as pd
import os

excel_file = "~/Downloads/arnhem.xlsx"

columns_to_extract = [
    "Addressee Title", "Addressee First Name", "Addressee Last Name",
    "Addressee House Number", "Addressee Street", "Addressee Town/City",
    "Addressee Province/State", "Addressee Country"
]

data = pd.read_excel(excel_file, usecols=columns_to_extract, sheet_name="Box 3 Folders XVI-XXII")

# Combine first name and last name columns into a single "full_name" column
data["full_name"] = data["Addressee First Name"] + " " + data["Addressee Last Name"]

# Rename columns to lowercase and replace spaces with underscores
data.columns = [col.lower().replace('/', '_') for col in data.columns]
data.columns = [col.lower().replace(' ', '_') for col in data.columns]

# Drop duplicate rows to get unique combinations of values
unique_data = data.drop_duplicates(subset=["full_name", "addressee_town_city", "addressee_province_state", "addressee_country"])

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)
output_csv = os.path.join(output_dir, 'people.csv')

unique_data.to_csv(output_csv, index=False)

print(f"CSV file created with unique names in the '{output_dir}' directory.")
