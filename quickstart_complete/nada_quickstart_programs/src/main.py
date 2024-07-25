import requests


GITHUB_TOKEN = 'github-token'
REPO_OWNER = 'owner_name'
REPO_NAME = 'nillion-python-starter'

def get_pull_requests(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        'Authorization': f'token {github-token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

pull_requests = get_pull_requests(REPO_OWNER, REPO_NAME)

print("Open Pull Requests:")
for pr in pull_requests:
    number = pr['number']
    title = pr['title']
    user = pr['user']['login']
    created_at = pr['created_at']
    pr_url = pr['html_url']
    print(f"PR #{number}: {title} by {user} - Created at {created_at}")
    print(f"URL: {pr_url}\n")

