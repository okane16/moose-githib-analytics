import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

def fetch_stargazers_with_timestamps(owner, repo, token):
    stargazers = []
    page = 1
    per_page = 100  # Maximum per page
    has_more = True

    headers = {
        'Accept': 'application/vnd.github.v3.star+json',
        'Authorization': f'token {token}'
    }

    while has_more:
        url = f'https://api.github.com/repos/{owner}/{repo}/stargazers'
        params = {
            'per_page': per_page,
            'page': page
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f'Error fetching stargazers: {response.status_code} {response.reason}')
            break

        data = response.json()

        if not data:
            has_more = False
        else:
            stargazers.extend(data)
            page += 1

    return stargazers

# Usage example
if __name__ == '__main__':
    load_dotenv()
    owner = '514-labs'        # Replace with your repository owner
    repo = 'moose'          # Replace with your repository name
    token = os.getenv('GITHUB_ACCESS_TOKEN')   # Get GitHub personal access token from environment variable

    if not token:
        raise ValueError("Please set the GITHUB_ACCESS_TOKEN environment variable.")

    stargazers = fetch_stargazers_with_timestamps(owner, repo, token)

    # Determine environment
    env = os.getenv('ENV', 'development').lower()  # Default to 'development' if not set
    print(f"Environment: {env}")

    if env == 'production':
        ingest_url = "https://your-production-url.com/ingest/HistoricalStargazer"
    else:
        ingest_url = "http://localhost:4000/ingest/HistoricalStargazer"

    count = 0
    for stargazer in stargazers:
        yesterday_evening = datetime.utcnow().replace(hour=18, minute=0, second=0, microsecond=0) - timedelta(days=1)
        starred_at_datetime = datetime.strptime(stargazer["starred_at"], "%Y-%m-%dT%H:%M:%SZ")
        if starred_at_datetime < yesterday_evening:
            count += 1
            print(count)
            print(f"({count}) {stargazer['user']['login']} starred at {stargazer['starred_at']}. Find their repositories at {stargazer['user']['repos_url']}")
            res = requests.post(ingest_url, json={
                "starred_at": stargazer["starred_at"],
                "login": stargazer["user"]["login"],
                "avatar_url": stargazer["user"]["avatar_url"],
                "repos_url": stargazer["user"]["repos_url"]
            })
