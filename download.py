import requests, json
from urllib.parse import urlparse
import os

# Replace with your GitHub Personal Access Token
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
assert GITHUB_TOKEN is not None, "GitHub token must be set."

# Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}

GRAPHQL_URL = "https://api.github.com/graphql"
REST_API_URL = "https://api.github.com/repos"

import re

def find_references(text):
    """Find references to issues or PRs in the given text."""
    return re.findall(r'(?:Fixes|Closes|Resolves) #(\d+)', json.dumps(text))

def fetch_related_issues(owner, repo, issue_number):
    """Fetch related issue details using GraphQL."""
    query = """
    query($owner: String!, $repo: String!, $issueNumber: Int!) {
      repository(owner: $owner, name: $repo) {
        issue(number: $issueNumber) {
          title
          body
          state
          comments(first: 10) {
            nodes {
              author {
                login
              }
              body
            }
          }
        }
      }
    }
    """
    variables = {"owner": owner, "repo": repo, "issueNumber": issue_number}
    return graphql_query(query, variables)


def extract_repo_and_pr(link):
    """Extract owner, repo, and PR number from a GitHub PR link."""
    parsed_url = urlparse(link)
    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) < 4 or path_parts[-2] != "pull":
        raise ValueError(f"Invalid pull request URL: {link}")
    owner, repo, _, pr_number = path_parts[:4]
    return owner, repo, int(pr_number)


def graphql_query(query, variables):
    """Perform a GraphQL query."""
    response = requests.post(
        GRAPHQL_URL, headers=HEADERS, json={"query": query, "variables": variables}
    )
    response.raise_for_status()
    return response.json()


def fetch_pr_data(owner, repo, pr_number):
    """Fetch PR data using GraphQL."""
    query = """
    query($owner: String!, $repo: String!, $prNumber: Int!) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $prNumber) {
          title
          body
          mergeCommit {
            oid
          }
          files(first: 100) {
            nodes {
              path
            }
          }
          comments(first: 100) {
            nodes {
              author {
                login
              }
              body
            }
          }
          reviews(first: 100) {
            nodes {
              author {
                login
              }
              body
            }
          }
        }
      }
    }
    """
    variables = {"owner": owner, "repo": repo, "prNumber": pr_number}
    return graphql_query(query, variables)


def fetch_pr_diff(owner, repo, pr_number):
    """Fetch the diff of a pull request using the REST API."""
    url = f"{REST_API_URL}/{owner}/{repo}/pulls/{pr_number}"
    headers = HEADERS.copy()
    headers["Accept"] = "application/vnd.github.v3.diff"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def process_pull_request(link, folder):
        """Process a single pull request link."""
        print(f"Processing PR: {link}")
        #try:
        owner, repo, pr_number = extract_repo_and_pr(link)

        # Fetch PR data using GraphQL
        data = fetch_pr_data(owner, repo, pr_number)
        pr_data = data["data"]["repository"]["pullRequest"]

        # Extract details
        title = pr_data["title"]
        description = pr_data["body"]
        merge_commit = pr_data["mergeCommit"]["oid"]
        file_paths = [f["path"] for f in pr_data["files"]["nodes"]]
        issue_comments = pr_data["comments"]["nodes"]
        review_comments = pr_data["reviews"]["nodes"]

        # Add PR description as a special "review comment"
        review_comments_with_description = [{"title":title}]+[
            {"author": {"login": "PR Description"}, "body": description}
        ] + review_comments + issue_comments

        # Find references in PR description, comments, and reviews
        references = find_references(review_comments_with_description)

        # Fetch related discussions
        related_discussions = []
        for issue_number in set(references):
            print(f"Fetching related discussion for issue #{issue_number}")
            discussion = fetch_related_issues(owner, repo, int(issue_number))
            related_discussions.append(discussion)

        review_comments_with_description += related_discussions

        # Print results
        print(f"\nPull Request #{pr_number} Summary:")
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Merge Commit SHA: {merge_commit}")
        print(f"Changed Files: {file_paths}")

        # Fetch and save the diff
        diff = fetch_pr_diff(owner, repo, pr_number)
        with open(f"{folder}/data_{folder}/pr_{pr_number}_diff.txt", "w") as diff_file:
            diff_file.write(diff)

        # Save results to files
        with open(f"{folder}/data_{folder}/pr_{pr_number}_files.json", "w") as files_file:
            json.dump({"commit": merge_commit, "files": file_paths}, files_file, indent=4)
        with open(f"{folder}/data_{folder}/pr_{pr_number}_review_comments.json", "w") as review_comments_file:
            json.dump(review_comments_with_description, review_comments_file, indent=4)


        print(f"\nData saved for PR #{pr_number}!")
        return review_comments_with_description
        #except Exception as e:
        #    print(f"Error processing PR {link}: {e}")
        return None


# List of pull request links
pr_links = [
    "https://github.com/deskflow/deskflow/pull/8062"
]

if __name__ == "__main__":
    os.makedirs('tmp/data_tmp', exist_ok=True)
    
    # Process each pull request
    for link in pr_links:
        process_pull_request(link, 'tmp')
