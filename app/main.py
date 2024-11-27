from fastapi import FastAPI
from app.routers import investment

app = FastAPI(title="FinovAI: AI-Powered Capital Investment Advisor")

app.include_router(investment.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to FinovAI"}