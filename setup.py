from dotenv import load_dotenv
import os
from utils.db import initialize_pinecone, load_dataset_to_pinecone

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


def setup_database():
    # Initialize Pinecone
    index_name = "finov1"
    pinecone_index = initialize_pinecone(PINECONE_API_KEY, "us-east-1", index_name)

    # Load dataset (only needs to be done once)
    load_dataset_to_pinecone(pinecone_index, "data/Finance_data.csv")


if __name__ == "__main__":
    setup_database()
