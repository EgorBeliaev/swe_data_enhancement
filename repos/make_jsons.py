import os
import json
from clone_repo import clone_and_checkout
import shutil
from process_gemini import query_gemini

import uuid

def read_py_files_from_repo(repo_path):
    code_files = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
                file_path = os.path.join(root, file)
                # Check if the file is a symbolic link and skip it if so
                if os.path.islink(file_path):
                    continue
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code_files[file_path] = f.read()
    return code_files

def load_json(json_string):
    try:
        data = json.loads(json_string.replace("```json", "").replace("`", ""))
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return None
    
def read_truncated_json(json_string):
    """
    Attempts to read a JSON string that may be truncated.
    Tries to recover as much data as possible.
    """
    json_string = json_string.replace("```json", "").replace("`", "")
    try:
        # Attempt to load the JSON string
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        # If there's a JSONDecodeError, try to recover
        print(f"Failed to decode JSON: {e}")
        # Find the position of the error
        error_position = e.pos
        # Attempt to truncate the string to the last complete JSON object
        truncated_string = json_string[:error_position] + "}"
        
        # Try to find the last complete JSON object
        while truncated_string:
            try:
                data = json.loads(truncated_string)
                return data
            except json.JSONDecodeError:
                # Remove the last character and try again
                truncated_string = truncated_string[:-2] + "}"
        # If no valid JSON can be recovered, return None
        return None
    
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# take sepasrately jsons which seem reasonable
def filter_and_save_pairs(new_repo_dir, small_json_path, big_json_path, output_directory):
    # Load JSON data
    small_json = load_json_file(small_json_path)
    big_json = load_json_file(big_json_path)

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
        shutil.move(f'repos/{new_repo_dir}.zip', f'repos_filtered/{new_repo_dir}.zip')



os.makedirs('validation', exist_ok=True)
os.makedirs('validation_filtered', exist_ok=True)
os.makedirs('repos', exist_ok=True)
os.makedirs('repos_filtered', exist_ok=True)

def process_repo(repo_url, repo_name):
    # Define paths
    data_folder = f"../{repo_name}/data_{repo_name}"

    # Iterate over all JSON files in the data folder
    for json_filename in os.listdir(data_folder):
        if json_filename.startswith("pr_") and json_filename.endswith("_files.json"):
            json_file_path = os.path.join(data_folder, json_filename)

            # Read the JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            commit_hash = data['commit']
            required_files = data['files']

            pr_number = json_filename.split('_')[1]
            repo_dir = f"{repo_name}_pr_{pr_number}_{commit_hash}"

            # read diff 
            diff_file_path = os.path.join(data_folder, f"pr_{pr_number}_diff.txt")
            with open(diff_file_path, 'r') as file:
                diff = file.read()

            # read sum
            sum_file_path = os.path.join(data_folder, f"pr_{pr_number}_sum.txt")
            with open(sum_file_path, 'r') as file:
                pr_question = file.read()


            #if not all_files_present:
            #    continue

            # Clone and checkout the repository
            #repo_url = f"https://github.com/{repo_name}/{repo_name}"
            
            new_repo_dir = clone_and_checkout(repo_url, commit_hash, required_files, repo_dir=repo_dir)

            if new_repo_dir:
                # if repo was processed successfully
                py_files = read_py_files_from_repo(new_repo_dir)

                response = query_gemini(py_files, pr_question, diff)

                required_files_big = required_files.copy()

                try:
                    print(response)
                    suggestion = read_truncated_json(response)

                    for fpath, score in suggestion.items():
                        if score > 4:
                            if not fpath in required_files:
                                print(f"Additional file: {fpath}, Score: {score}")
                                required_files_big.append(fpath)

                except:
                    print("Failed to provide more suggestions")

                shutil.rmtree(new_repo_dir)
                print(f"Removed cloned directory")

            repo_id =  str(uuid.uuid4()),
            
            if os.path.exists(f"{new_repo_dir}.zip"):
                shutil.move(f"{new_repo_dir}.zip", f"repos/{new_repo_dir}.zip")
                print(f"saving validation {new_repo_dir}")
                validation = {
                    "zip_path": f"repos/{new_repo_dir}.zip",
                    "repo_id": repo_id,
                    "validations": [
                        {
                            "query": pr_question,
                            "files": [f"{new_repo_dir}/{f}" for f in required_files],
                            "chunks": []
                        }
                    ],
                    "user_id": repo_id,
                }
                with open(f'validation/{new_repo_dir}.json', 'w') as outfile:
                    json.dump(validation, outfile, indent=4)

                validation_big = {
                    "zip_path": f"repos/{new_repo_dir}.zip",
                    "repo_id": repo_id,
                    "validations": [
                        {
                            "query": pr_question,
                            "files": [f"{new_repo_dir}/{f}" for f in required_files_big],
                            "chunks": []
                        }
                    ],
                    "user_id": repo_id,
                }

                with open(f'validation/{new_repo_dir}_big.json', 'w') as outfile:
                    json.dump(validation_big, outfile, indent=4)

                filter_and_save_pairs(new_repo_dir, small_json_path=f'validation/{new_repo_dir}.json', big_json_path=f'validation/{new_repo_dir}_big.json', output_directory='validation_filtered')


                print(f"Processed and zipped repository for PR {pr_number} with commit {commit_hash}\n\n")
            else:
                print(f"Error for PR {pr_number}\n\n")

# Example usage
process_repo("https://github.com/HabitRPG/habitica", 'habitica')
