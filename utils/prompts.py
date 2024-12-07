from langchain.prompts import PromptTemplate

financial_advisor_prompt = PromptTemplate(
    template="""
    You are a financial advisor with expertise in wealth management. Based on the following user details, generate a systematic and friendly investment strategy:
    Gender: {gender}
    Age: {age}
    Income: {income}
    Expenditure: {expenditure}
    Savings: {savings}
    Investment Objective: {objective}
    Duration: {duration}

    User Question: {user_question}
    """,
    input_variables=["gender", "age", "income", "expenditure", "savings", "objective", "duration", "user_question"]
)
