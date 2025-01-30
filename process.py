from download import process_pull_request, extract_repo_and_pr
from summarization import summarize_changes
import os

folders = ['habitica', 'mocha', 'express', 'checkmate', 'transformers.js']


for folder in folders:

    os.makedirs(f'{folder}/data_{folder}', exist_ok=True)

    with open(f'{folder}/prs_js.txt') as f:
        for line in f.readlines():
            print(line.strip())
            owner, repo, pr_number = extract_repo_and_pr(line.strip())
            data = process_pull_request(line.strip(), folder)
            if data:
                summary = summarize_changes(data)
                if summary:
                    with open(f'{folder}/data_{folder}/pr_{pr_number}_sum.txt', 'w') as f:
                        f.write(summary)
                else:
                    print("Error summary")
                    import sys; sys.exit(1)

            else:
                print("Error")
                import sys; sys.exit(1)
