from download import process_pull_request, extract_repo_and_pr
from summarization import summarize_changes
import os

# Explore subfolders in the "java" directory
java_directory = 'csharp'
folders = [os.path.join(java_directory, name) for name in os.listdir(java_directory) if os.path.isdir(os.path.join(java_directory, name))]



for folder in folders:

    os.makedirs(f'{folder}/data_{folder}', exist_ok=True)

    with open(f'{folder}/prs_js.txt') as f:
        for line in f.readlines():
            print(line.strip())
            owner, repo, pr_number = extract_repo_and_pr(line.strip())
            try:
                data = process_pull_request(line.strip(), folder)
            except Exception as e:
                print(e)
                data = None
            if data:
                summary = summarize_changes(data)
                if summary:
                    with open(f'{folder}/data_{folder}/pr_{pr_number}_sum.txt', 'w') as f:
                        f.write(summary)
                else:
                    print("Error summary")
                    import sys; sys.exit(1)

            else:
                #print("Error")
                #import sys; sys.exit(1)
                continue
