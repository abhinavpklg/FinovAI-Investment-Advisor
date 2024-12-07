import pandas as pd
from sentence_transformers import SentenceTransformer
import pinecone

# Initialize Pinecone
pinecone.init(api_key="PINECONE_API_KEY", environment="us-east-1")

# Create or connect to a vector index
index_name = "finov1"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=768)

index = pinecone.Index(index_name)

# Load and preprocess the dataset
data = pd.read_csv('Finance_data.csv')  
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Convert dataset to embeddings and store in Pinecone
for idx, row in data.iterrows():
    # Create a comprehensive text representation of all relevant fields
    text = f"""
    Profile: {row['gender']}, Age: {row['age']}
    Investment Preferences: {row['Investment_Avenues']}, {row['Avenue']}
    Experience: Mutual Funds: {row['Mutual_Funds']}, Equity: {row['Equity_Market']}, 
    Bonds: {row['Government_Bonds']}, Debentures: {row['Debentures']}, 
    FD: {row['Fixed_Deposits']}, PPF: {row['PPF']}, Gold: {row['Gold']}, Stocks: {row['Stock_Marktet']}
    Investment Factors: {row['Factor']}
    Objectives: {row['Objective']}, {row['Purpose']}
    Duration: {row['Duration']}
    Monitoring: {row['Invest_Monitor']}
    Expectations: {row['Expect']}
    Savings Objectives: {row['What are your savings objectives?']}
    Investment Reasons - Equity: {row['Reason_Equity']}, Mutual Funds: {row['Reason_Mutual']},
    Bonds: {row['Reason_Bonds']}, Fixed Deposits: {row['Reason_FD']}
    Source: {row['Source']}
    """
    embedding = model.encode(text).tolist()
    index.upsert([(str(idx), embedding, {"info": row.to_dict()})])
