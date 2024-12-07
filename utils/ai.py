from transformers import pipeline, BitsAndBytesConfig
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import torch

# Load environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
# Use a pipeline as a high-level helper
def initialize_huggingface_model():
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_use_nested_quant=False
    )
    model_name = "MayaPH/FinOPT-Washington" 
    pipe = pipeline(
        "text-generation",
        model=model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        low_cpu_mem_usage=True,
        quantization_config=quantization_config
    )
    return pipe

def generate_response(pipe, messages):
    response = pipe(messages, max_length=4000, num_return_sequences=1)
    return response

def setup_retrieval_chain(llm, pinecone_index, embedding_function):
    retriever = Pinecone.from_existing_index(index_name=pinecone_index, embedding_function=embedding_function)
    return RetrievalQA(llm_chain=llm, retriever=retriever)
