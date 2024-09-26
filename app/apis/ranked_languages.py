
# This file is where you can define your API templates for consuming your data
# All query_params are passed in as strings, and are used within the sql tag to parameterize you queries

from moose_lib import MooseClient, cli_log, CliLogData

    
def run(client: MooseClient, params, jwt_payload):
    rank_by = params.get("rank_by", ["total_projects"])[0]
    
    if rank_by not in ["total_projects", "total_repo_size_kb", "avg_repo_size_kb"]:
        raise ValueError("Invalid rank_by value. Must be one of: total_projects, total_repo_size_kb, avg_repo_size_kb")
    
    cli_log(CliLogData(action="RankedLanguages", message=f"params: {params if params else 'no params'}", message_type="Info"))
    query = f'''
    SELECT 
        language, 
        countMerge(total_projects) AS total_projects, 
        sumMerge(total_repo_size_kb) AS total_repo_size_kb, 
        avgMerge(avg_repo_size_kb) AS avg_repo_size_kb 
    FROM 
        TopProgrammingLanguages 
    GROUP BY 
        language 
    ORDER BY 
        {rank_by} DESC
    '''
    return client.query(query, { "rank_by": rank_by })