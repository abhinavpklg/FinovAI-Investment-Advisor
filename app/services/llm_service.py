from langchain import LLMChain
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

class LLMService:
    def __init__(self):
        self.llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.5, "max_length": 512})
        self.prompt = PromptTemplate(
            input_variables=["age", "income", "expenditure", "goal", "context"],
            template="Given the following user information:\nAge: {age}\nMonthly Income: ${income}\nMonthly Expenditure: ${expenditure}\nFinancial Goal: {goal}\n\nAnd considering this financial context:\n{context}\n\nProvide a personalized monthly investment plan:"
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def generate_investment_plan(self, user_input, context):
        return self.chain.run(
            age=user_input.age,
            income=user_input.monthly_income,
            expenditure=user_input.monthly_expenditure,
            goal=user_input.financial_goal,
            context=context
        )