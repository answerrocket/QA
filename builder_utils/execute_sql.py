from answer_rocket.data import ExecuteSqlQueryResult
from answer_rocket import AnswerRocketClient
from dotenv import load_dotenv
import argparse
import os
import pandas

def execute_sql(sql_query: str) -> pandas.DataFrame:
    """Execute a SQL query against a database in AnswerRocket

    Args:
        sql_query (str): The SQL query to execute against the database

    Returns:
        pandas.DataFrame: The result set from the SQL query execution
    """
    load_dotenv()

    database_id = os.getenv('DATABASE_ID')

    if database_id is None:
        raise Exception("Failed to run SQL query: No database ID provided. Get Database id from dataset metadata")

    arc = AnswerRocketClient()
    response: ExecuteSqlQueryResult = arc.data.execute_sql_query(database_id=database_id, sql_query=sql_query)
    
    if response is None:
        raise Exception("Failed to run SQL query: No response received")
    
    if response.df is None:
        raise Exception(f"Failed to run SQL query: No data returned")

    return response.df

def main():
    """Main function to execute a SQL query on a dataset"""
    parser = argparse.ArgumentParser(description='Execute a SQL query on a dataset')
    parser.add_argument('sql_query', help='SQL query to execute')

    args = parser.parse_args()

    try:
        response = execute_sql(args.sql_query)
        print(f"SQL query executed successfully:")
        print(response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
