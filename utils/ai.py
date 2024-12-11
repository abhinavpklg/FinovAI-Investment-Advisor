from transformers import pipeline, BitsAndBytesConfig
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Pinecone
from langchain_community.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import torch
from huggingface_hub import login
import streamlit as st
from langchain_community.llms import HuggingFacePipeline

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
@st.cache_resource
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
            model_kwargs={"low_cpu_mem_usage": True}
        )  
        print("Model initialized successfully")
        return pipe
        
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        raise

def generate_response(pipe, messages):
    try:
        # Optimize generation parameters
        response = pipe(
            messages,
            max_length=512,  # Reduced from 2048 for faster responses
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            top_k=50,
            pad_token_id=pipe.tokenizer.eos_token_id,
            repetition_penalty=1.1,
            truncation=True
        )
        
        if response and isinstance(response, list) and len(response) > 0:
            return response[0]['generated_text']
        return "I apologize, but I couldn't generate a response. Please try again."
        
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return f"An error occurred: {str(e)}"

def setup_retrieval_chain(pipe, pinecone_index, embedding_model):
    # Convert the pipeline to a LangChain LLM
    llm = HuggingFacePipeline(pipeline=pipe)
    
    embedding_function = lambda text: embedding_model.encode(text).tolist()
    
    vectorstore = Pinecone(pinecone_index, embedding_function, "text")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    print("Retrieved documents:", retriever.get_relevant_documents("test query"))
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False
    )
    
    return qa_chain
