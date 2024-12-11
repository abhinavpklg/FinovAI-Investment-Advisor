from langchain_community.vectorstores import Pinecone
import os
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from utils.prompts import financial_advisor_prompt

# Load environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

def setup_chat_model(client, system_prompt):
    def generate_chat_response(query):
        try:
            response = client.chat.completions.create(
                model='llama-3.1-70b-versatile',
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating chat response: {str(e)}")
            return f"An error occurred: {str(e)}"
    
    return generate_chat_response

def setup_retrieval_chain(client, pinecone_index, embedding_model, system_prompt):
    chat_model = setup_chat_model(client, system_prompt)
    
    embedding_function = lambda text: embedding_model.encode(text).tolist()
    vectorstore = Pinecone(pinecone_index, embedding_function, "text")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    return chat_model, retriever

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
            truncation=True,
        )

        if response and isinstance(response, list) and len(response) > 0:
            return response[0]["generated_text"]
        return "I apologize, but I couldn't generate a response. Please try again."

    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return f"An error occurred: {str(e)}"

def get_huggingface_embeddings(text, model_name="sentence-transformers/all-mpnet-base-v2"):
    model = SentenceTransformer(model_name)
    return model.encode(text)

def perform_chat_rag(query, user_profile, pinecone_index):
    # embed the query
    raw_query_embedding = get_huggingface_embeddings(query)
    
    # find the top matches from finov1 index
    top_matches = pinecone_index.query(
        vector=raw_query_embedding.tolist(),
        top_k=5,
        include_metadata=True
    )

    # Create context from matches
    context = "Based on our financial database:\n"
    for match in top_matches['matches']:
        if 'text' in match['metadata']:
            context += f"\n- {match['metadata']['text']}"

    # Format the prompt using the template
    formatted_prompt = financial_advisor_prompt.format(
        gender=user_profile['gender'],
        age=user_profile['age'],
        income=user_profile['income'],
        expenditure=user_profile['expenditure'],
        savings=user_profile['savings'],
        objective=user_profile['objective'],
        duration=user_profile['duration'],
        user_question=f"{query}\n\nAdditional Context:\n{context}"
    )

    try:
        llm_response = client.chat.completions.create(
            model='llama-3.1-70b-versatile',
            messages=[
                {"role": "system", "content": formatted_prompt}
            ]
        )
        return llm_response.choices[0].message.content
    except Exception as e:
        print(f"Error in chat completion: {str(e)}")
        # Fallback to smaller model
        llm_response = client.chat.completions.create(
            model='llama-3.1-8b-instant',
            messages=[
                {"role": "system", "content": formatted_prompt}
            ]
        )
        return llm_response.choices[0].message.content
