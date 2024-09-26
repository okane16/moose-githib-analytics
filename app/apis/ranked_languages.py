
# This file is where you can define your API templates for consuming your data
# All query_params are passed in as strings, and are used within the sql tag to parameterize you queries

from moose_lib import MooseClient

def run(client: MooseClient, params):
    return client.query("SELECT language, countMerge(total_projects) AS total_projects, sumMerge(total_repo_size_kb) AS total_repo_size_kb, avgMerge(avg_repo_size_kb) AS avg_repo_size_kb FROM TopProgrammingLanguages GROUP BY language ORDER BY total_projects DESC", { })
