from pinecone import Pinecone
import pandas as pd
from sentence_transformers import SentenceTransformer

def initialize_pinecone(api_key, environment, index_name):
    pc = Pinecone(api_key=api_key)
    if index_name in pc.list_indexes().names():
        return pc.Index(index_name)
    else:
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric='cosine'
        )
        return pc.Index(index_name)

def load_dataset_to_pinecone(index, dataset_path, model_name="BAAI/bge-large-en-v1.5"):
    model = SentenceTransformer(model_name) 
    data = pd.read_csv(dataset_path)
    for idx, row in data.iterrows():
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
        
        # Convert all values to strings to ensure compatibility
        metadata = {k: str(v) for k, v in row.to_dict().items()}
        
        index.upsert([(str(idx), embedding, metadata)])
