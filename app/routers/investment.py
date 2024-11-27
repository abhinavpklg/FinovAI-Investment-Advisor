from fastapi import APIRouter, Depends
from app.models import UserInput, InvestmentPlan
from app.services.llm_service import LLMService
from app.services.vector_store_service import VectorStoreService

router = APIRouter()

@router.post("/investment-plan", response_model=InvestmentPlan)
async def generate_investment_plan(
    user_input: UserInput,
    llm_service: LLMService = Depends(LLMService),
    vector_store_service: VectorStoreService = Depends(VectorStoreService)
):
    context = vector_store_service.query_vectorstore(f"investment advice for {user_input.age} year old with {user_input.financial_goal} goal")
    recommendation = llm_service.generate_investment_plan(user_input, context)
    return InvestmentPlan(recommendation=recommendation)