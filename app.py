import streamlit as st
from dotenv import load_dotenv
import os
from utils.db import initialize_pinecone, load_dataset_to_pinecone
from utils.prompts import financial_advisor_prompt
from utils.ai import initialize_huggingface_model, setup_retrieval_chain, generate_response
from multiprocessing import freeze_support

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
index_name = "finov1"
pinecone_index = initialize_pinecone(PINECONE_API_KEY, "us-east-1", index_name)

def main():
    # Initialize AI model
    huggingface_model = initialize_huggingface_model()

    # Sidebar for user input
    st.sidebar.title("User Details")
    gender = st.sidebar.radio("Gender", ("Male", "Female", "Other"))
    age = st.sidebar.slider("Age", 18, 80)
    income = st.sidebar.number_input("Monthly Income", min_value=0)
    expenditure = st.sidebar.number_input("Monthly Expenditure", min_value=0)
    savings = st.sidebar.number_input("Current Savings", min_value=0)
    objective = st.sidebar.text_input("Investment Objective")
    duration = st.sidebar.number_input("Investment Duration (years)", min_value=1)

    # Chat interface
    st.title("FinovAI - Your AI Financial Advisor")
    if "history" not in st.session_state:
        st.session_state["history"] = []

    user_input = st.text_input("Ask your question:")
    if user_input:
        context_message = financial_advisor_prompt.format(
            gender=gender,
            age=age,
            income=income,
            expenditure=expenditure,
            savings=savings,
            objective=objective,
            duration=duration,
            user_question=user_input
        )
        response = generate_response(huggingface_model, context_message)
        
        # Save the interaction in session state
        st.session_state["history"].append((user_input, response[0]["generated_text"]))

    # Display chat history
    for user_msg, ai_response in st.session_state["history"]:
        st.write(f"**You:** {user_msg}")
        st.write(f"**Advisor:** {ai_response}")

    # Reset button
    if st.sidebar.button("Reset Chat"):
        st.session_state["history"] = []

if __name__ == "__main__":
    freeze_support()
    main()
