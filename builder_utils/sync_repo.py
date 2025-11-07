from answer_rocket.types import MaxResult
from answer_rocket import AnswerRocketClient
from dotenv import load_dotenv
import argparse
import os
import pandas

def sync_repo() -> bool:
    """Synchronize a MAX skill repository with AnswerRocket

    Returns:
        bool: True if the repository sync was successful, False otherwise
    """
    load_dotenv()

    repo_id = os.getenv('REPO_ID')

    if repo_id is None:
        raise Exception("Failed to sync repo: No repo ID provided.")

    arc = AnswerRocketClient()
    response: MaxResult = arc.chat.sync_max_skill_repository(repository_id=repo_id)
    
    if response.error:
        raise Exception(f"Failed to sync repo: No response received with error: {response.error}")

    return response.success

def main():
    """Main function to sync a repository in AnswerRocket"""
    try:
        if sync_repo():
            print(f"Repository synced successfully")
        else:
            print(f"Repository sync failed")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
