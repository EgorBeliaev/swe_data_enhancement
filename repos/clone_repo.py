import os
import shutil
import git
from git import Repo
import zipfile

def clone_and_checkout(repo_url, merge_commit_sha, required_files, repo_dir='cloned_repo'):
    # Clone the repository
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    repo = Repo.clone_from(repo_url, repo_dir)

    # Checkout to the parent commit
    try:

        # Get the parent commit of the merge commit
        merge_commit = repo.commit(merge_commit_sha)
        parent_commit_sha = merge_commit.parents[0].hexsha

    
        repo.git.checkout(parent_commit_sha)
        print(f"Checked out to parent commit: {parent_commit_sha}")

        # Remove the .git directory
        git_dir = os.path.join(repo_dir, '.git')
        if os.path.exists(git_dir):
            shutil.rmtree(git_dir, ignore_errors=True)
        print(".git directory removed")

        # Remove non-code files
        remove_non_code_files(repo_dir)

        # Check if all required files are present
        all_files_present = True
        for required_file in required_files:
            file_path = os.path.join(repo_dir, required_file)
            if not os.path.exists(file_path):
                print(f"Required file {required_file} is missing for {repo_dir}. Skipping.")
                all_files_present = False
                #break


        # Rename the directory
        new_repo_dir = f"{repo_dir}_{parent_commit_sha}"
        os.rename(repo_dir, new_repo_dir)
        print(f"Renamed directory to: {new_repo_dir}")

        # Zip the directory
        zip_filename = f"{new_repo_dir}.zip"
        shutil.make_archive(new_repo_dir, 'zip', new_repo_dir)
        print(f"Zipped directory to: {zip_filename}")
    except Exception as e:
        print(f"An error occurred while checking out and zipping the repository: {e}")

    # Delete the directory
    try:
        #shutil.rmtree(new_repo_dir)
        print(f"Returned directory: {new_repo_dir}")
        return new_repo_dir
    except Exception as e:
        shutil.rmtree(repo_dir)
        print(f"Deleted directory: {repo_dir}")
        return None

def remove_non_code_files(directory):
    # Define file extensions to keep (common code file extensions)
    code_extensions = {'.dart','.gradle', 'Makefile', '.json', '.md', '.yaml', '.gui', '.m', '.py', 'LICENSE', '.ejs', '.hbs', '.ejs', '.tmpl', '.erb', '.haml', '.jade', '.mustache', '.njk', '.pug', '.slim', '.twig','.svelte', '.sh', '.css', '.html', '.java', '.cpp', '.h', '.hpp','.c', '.cs', '.rb', '.go', '.php', '.swift', '.kt', '.rs', '.md', '.ts', '.js', '.jsx', '.tsx', '.json', '.vue', '.xml', '.yml', '.toml', 'Dockerfile', 'Gemfile', 'Rakefile', 'Makefile', 'Pipfile', '.txt', '.lua', '.sql', '.config', '.log'}

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not any(file.endswith(ext) for ext in code_extensions):
                try:
                    os.remove(file_path)
                    #print(f"Removed non-code file: {file_path}")
                except Exception as e:
                    print(f"Error removing file {file_path}: {e}")

if __name__ == "__main__":
    # Example usage
    repo_url = "https://github.com/expressjs/express"
    merge_commit_sha = "6bcdfef6ad148672872e4f5930a01a5a45dd9df0"  # Replace with your merge commit SHA
    repo_dir = "express"
    clone_and_checkout(repo_url, merge_commit_sha, [], repo_dir=repo_dir)
