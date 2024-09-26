
# Add your models & start the development server to import these types
from app.datamodels.RawStarEvent import RawStarEvent
from app.datamodels.StargazerRepositoryInfo import StargazerRepositoryInfo
from moose_lib import StreamingFunction, cli_log, CliLogData
from typing import Optional
from datetime import datetime
import requests

def call_github_api(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fn(source: RawStarEvent) -> Optional[list[StargazerRepositoryInfo]]:
    if source.action == "deleted" or not source.starred_at:
        cli_log(CliLogData(action=source.action, message=f"Skipping deleted or without starred_at", message_type="Info"))
        return None
    
    repositories = call_github_api(source.sender["repos_url"])
    cli_log(CliLogData(action="Got repositories", message=f"{len(repositories)}", message_type="Info"))
    
    return [
        StargazerRepositoryInfo(
            starred_at=source.starred_at,
            stargazer_login=source.sender["login"],
            repo_name=repo["name"],
            repo_full_name=repo["full_name"],
            description=repo["description"],
            repo_url=repo["html_url"],
            repo_stars=repo["stargazers_count"],
            repo_watchers=repo["watchers_count"],
            language=repo["language"],
            repo_size_kb=repo["size"],
            created_at=repo["created_at"],
            updated_at=repo["updated_at"],
        )
        for repo in repositories
    ]
    
my_function = StreamingFunction(
    run=fn
)
