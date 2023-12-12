from datetime import datetime
import re
import yaml

class CustomDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

# Read the input YAML file
def read_input_file(input_file_path):
    with open(input_file_path, "r") as file:
        data_lines = file.readlines()
    return data_lines

# Process data
def process_data(data_lines, constant_model):
    output_data = []
    existing_locations = set()  # To track existing locations
    pk_counter = 1

    for line in data_lines:
        pairs = [pair.strip() for pair in line.replace("'", "").strip("{}\n ").split(",")]
        entry = {
            "model": constant_model,
            "pk": pk_counter,
            "fields": {
                "town_city": "",
                "country": "",
                "latitude": 0.0,
                "longitude": 0.0,
                "province_state": "",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
        }

        for pair in pairs:
            key_value = pair.split(":")
            # print the key val pairs to check the data
            if len(key_value) == 2:
                key, value = [item.strip() for item in key_value]
                key = key.lstrip('- ') # remove hypthen from city key

                if value.lower() == "nan":
                    value = ""
                
                if key == "city":
                    entry["fields"]["town_city"] = value
                elif key == "state":
                    entry["fields"]["province_state"] = value
                elif key in ["latitude", "longitude"]:
                    entry["fields"][key] = float(value) if value else 0.0
                elif key == "country":
                    entry["fields"][key] = value

        # Check if location already exists or if it's an invalid location
        location_tuple = (entry["fields"]["town_city"], entry["fields"]["country"], entry["fields"]["province_state"], entry["fields"]["latitude"], entry["fields"]["longitude"])
        if location_tuple not in existing_locations and (entry["fields"]["town_city"] or entry["fields"]["country"] or entry["fields"]["province_state"]) and (entry["fields"]["latitude"] != 0.0 or entry["fields"]["longitude"] != 0.0):
            output_data.append(entry)
            existing_locations.add(location_tuple)  # Add location to the set of existing locations
            pk_counter += 1

    return output_data

def str_presenter(dumper, data):
    if data.startswith(' '):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

# Write the output YAML file
def write_output_file(output_data, output_file_path):
    with open(output_file_path, "w") as file:
        yaml.dump(
            output_data,
            file,
            default_flow_style=False,
            Dumper=CustomDumper,
            explicit_start=False,
        )

def main():
    input_file_path = "locations_input.yaml"
    output_file_path = "locations.yaml"
    constant_model = "postcards.location".strip()
    data_lines = read_input_file(input_file_path)
    output_data = process_data(data_lines, constant_model)
    write_output_file(output_data, output_file_path)
    print(f"Conversion completed. Output written to {output_file_path}")

if __name__ == "__main__":
    main()