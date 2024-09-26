
# This file is where you can define your SQL queries to shape and manipulate batches
# of data using Blocks. Blocks can also manage materialized views to store the results of 
# your queries for improved performance. A materialized view is the recommended approach for aggregating
# data. For more information on the types of aggregate functions you can run on your existing data, 
# consult the Clickhouse documentation: https://clickhouse.com/docs/en/sql-reference/aggregate-functions

from moose_lib import (
    AggregationCreateOptions,
    AggregationDropOptions,
    Blocks,
    ClickHouseEngines,
    TableCreateOptions,
    create_aggregation,
    drop_aggregation,
)


mv_name = "TopProgrammingLanguagesMV"
table_name = "TopProgrammingLanguages"

create_table_options = TableCreateOptions(
    name=table_name,
    columns={
        "language": "String",
        "total_projects": "AggregateFunction(count, Int64)",
        "total_repo_size_kb": "AggregateFunction(sum, Int64)",
        "avg_repo_size_kb": "AggregateFunction(avg, Int64)"
    },
    engine=ClickHouseEngines.AggregatingMergeTree,
    order_by="language",
)

select_query = f'''
SELECT
    language,
    countState(*) AS total_projects,
    sumState(repo_size_kb) AS total_repo_size_kb,
    avgState(repo_size_kb) AS avg_repo_size_kb
FROM
    StargazerRepositoryInfo_0_0
GROUP BY
    language
'''

teardown_queries = drop_aggregation(AggregationDropOptions(view_name=mv_name, table_name=table_name))

setup_queries = create_aggregation(AggregationCreateOptions(
    materialized_view_name=mv_name,
    select=select_query,
    table_create_options=create_table_options,
))

block = Blocks(teardown=teardown_queries, setup=setup_queries)
