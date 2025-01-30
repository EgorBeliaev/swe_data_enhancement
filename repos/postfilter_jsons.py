import json
import os
import shutil

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def filter_and_save_pairs(small_json_path, big_json_path, output_directory):
    # Load JSON data
    small_json = load_json(small_json_path)
    big_json = load_json(big_json_path)

    # Count the number of files in each JSON
    num_small_files = len(small_json['validations'][0]['files'])
    num_big_files = len(big_json['validations'][0]['files'])

    # Apply filtering conditions
    if (num_small_files < 10 and num_big_files <= 20) or \
       (num_small_files >= 10 and num_big_files <= 2.5 * num_small_files):
        # Ensure the output directory exists
        #os.makedirs(output_directory, exist_ok=True)

        # Copy the valid JSON files to the output directory
        shutil.copy(small_json_path, output_directory)
        shutil.copy(big_json_path, output_directory)
        print(f"Saved valid pair: {small_json_path} and {big_json_path}")

def process_directory(input_directory, output_directory):
    # Iterate over all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.json') and not filename.endswith('_big.json'):
            # Construct the corresponding big JSON filename
            big_filename = filename.replace('.json', '_big.json')
            small_json_path = os.path.join(input_directory, filename)
            big_json_path = os.path.join(input_directory, big_filename)

            # Check if the big JSON file exists
            if os.path.exists(big_json_path):
                # Filter and save the valid pairs
                filter_and_save_pairs(small_json_path, big_json_path, output_directory)

# Example usage
input_directory = 'validation'
output_directory = 'validation_filtered'

os.makedirs(output_directory, exist_ok=True)

process_directory(input_directory, output_directory)
