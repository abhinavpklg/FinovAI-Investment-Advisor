from transformers import pipeline, BitsAndBytesConfig
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import torch
from huggingface_hub import login

# Load environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Modify the device selection to be more robust
device = "cpu"  # Default to CPU
if torch.backends.mps.is_available():
    try:
        device = "mps"
    except:
        print("MPS (Metal Performance Shaders) available but encountered an error. Falling back to CPU.")

# Use a pipeline as a high-level helper
def initialize_huggingface_model():
    try:
        print("Initializing HuggingFace model...")

        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  
        
        login(token=HUGGINGFACE_API_KEY)
        
        pipe = pipeline(
            "text-generation",
            model=model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            truncation=True,
            max_length=2048
        )  
        print("Model initialized successfully")
        return pipe
        
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        raise

def generate_response(pipe, messages):
    try:
        # Add more specific parameters for the pipeline
        response = pipe(
            messages,
            max_length=2048,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7,
            pad_token_id=pipe.tokenizer.eos_token_id
        )
        
        # Add debug logging
        print("Raw response:", response)
        
        # Check if response is valid and extract text
        if response and isinstance(response, list) and len(response) > 0:
            return response[0]['generated_text']
        return "I apologize, but I couldn't generate a response. Please try again."
        
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return f"An error occurred: {str(e)}"

def setup_retrieval_chain(llm, pinecone_index, embedding_function):
    retriever = Pinecone.from_existing_index(index_name=pinecone_index, embedding_function=embedding_function)
    return RetrievalQA(llm_chain=llm, retriever=retriever)
