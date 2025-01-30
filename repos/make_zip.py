import os
import json
from clone_repo import clone_and_checkout

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


            #if not all_files_present:
            #    continue

            # Clone and checkout the repository
            #repo_url = f"https://github.com/{repo_name}/{repo_name}"
            pr_number = json_filename.split('_')[1]
            repo_dir = f"{repo_name}_pr_{pr_number}_{commit_hash}"
            clone_and_checkout(repo_url, commit_hash, required_files, repo_dir=repo_dir)

            print(f"Processed and zipped repository for PR {pr_number} with commit {commit_hash}\n\n")

# Example usage
process_repo("https://github.com/expressjs/express", 'express')
