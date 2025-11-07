from answer_rocket.data import MaxDataset
from answer_rocket import AnswerRocketClient
from dotenv import load_dotenv
import argparse
import os

def get_dataset_metadata(dataset_id: str) -> MaxDataset:
    """Retrieve dataset metadata and schema information from AnswerRocket

    Args:
        dataset_id (str): The ID of the dataset to retrieve metadata for

    Returns:
        MaxDataset: Dataset metadata including schema, columns, and database information
    """
    load_dotenv()

    arc = AnswerRocketClient()
    response = arc.data.get_dataset(dataset_id=dataset_id)
    
    if response is None:
        raise Exception("Failed to retrieve dataset metadata: No response received")
    
    database_id = os.getenv('DATABASE_ID')

    if database_id is None:
        os.environ['DATABASE_ID'] = response.database.database_id

    return response

def main():
    """Main function to get dataset metadata"""
    parser = argparse.ArgumentParser(description='Get dataset metadata from AnswerRocket')
    parser.add_argument('dataset_id', help='ID of the dataset to retrieve metadata for')

    args = parser.parse_args()

    try:
        metadata = get_dataset_metadata(args.dataset_id)
        print(f"Dataset metadata retrieved successfully:")
        print(metadata)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
