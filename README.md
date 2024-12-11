<<<<<<< HEAD
# FinovAI-Investment-Advisor
FinovAI : AI-Powered Investment Advisor
=======
# FinovAI : AI-Powered Investment Advisor

FinovAI is an intelligent investment advisory system that leverages artificial intelligence to provide personalized investment strategies and stock recommendations. The system uses Retrieval Augmented Generation (RAG) with vector databases to analyze market data and provide informed investment advice.

## Features

- Personalized investment strategy generation based on user profiles
- Stock recommendations using RAG with SEC company data
- Portfolio allocation guidelines based on risk profile and investment goals
- Real-time market data analysis through Yahoo Finance integration
- Semantic search capabilities for company information
- Interactive web interface built with Streamlit for easy user interaction

## User Interface

The application features a modern, user-friendly interface built using Streamlit, offering:

- Clean, intuitive design for easy navigation
- Interactive forms for user profile input
- Real-time graphs for visualization
- Dynamic stock recommendation displays
- Easy-to-understand investment strategy presentations

## AI Model Configuration

The system leverages Groq's high-performance API for fast AI inference, utilizing state-of-the-art language models:

### Primary Model
- Model: `llama-3.1-70b-versatile`
- Features:
  - High-accuracy financial analysis
  - Comprehensive market understanding
  - Sophisticated investment strategy generation
  - Fast inference through Groq's optimized infrastructure
  - Real-time response capabilities

### Fallback Model
- Model: `llama-3.1-8b-instant`
- Purpose: Automatic fallback for high-traffic periods or when primary model is unavailable
- Benefits:
  - Lower latency
  - Reduced resource requirements
  - Maintains service availability
  - Suitable for basic queries and analysis

### Performance Optimization
- Groq API integration for superior inference speed
- Automatic model switching based on:
  - System load
  - Query complexity
  - Response time requirements
  - Service availability
- Optimized prompt engineering for financial domain
- Efficient context handling for RAG implementation

## Setup Instructions

1. Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your API keys:
```
PINECONE_API_KEY=your_pinecone_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

4. Initialize the vector database:
```bash
python setup.py
```
This will set up the Pinecone vector database for RAG-based investment strategy generation.

5. Run the Jupyter notebook:
```bash
jupyter notebook Financial_Analysis_&_Automation.ipynb
```
This notebook contains code for setting up the vector DB in Pinecone for stock recommendations using SEC data.

6. Launch the Streamlit application:
```bash
streamlit run app.py
```
This will start the web interface on your local machine, typically at http://localhost:8501

## Example Conversations

The system can handle various investment-related queries:

1. Investment Strategy Generation:
```
User: I'm 30 years old with a monthly income of $8000, monthly expenditure of $5000, 
      and current savings of $50000. What investment strategy do you recommend?

FinovAI: Based on your age and financial profile, here's a recommended portfolio allocation:
- Equity/Stocks: 70%
- Mutual Funds: 15%
- Government Bonds: 10%
- Fixed Deposits: 5%

This aggressive allocation leverages your long investment horizon and risk capacity.
```

2. Stock Analysis:
```
User: Which companies are making electric cars?

FinovAI: Based on market analysis, here are some key players:
- Tesla (TSLA): Leading EV manufacturer with global presence
- EVgo (EVGO): Focuses on EV charging infrastructure
- Other automotive companies with significant EV initiatives
```

## RAG Knowledge Base

The system utilizes two main data sources for its RAG capabilities:

1. Investment Strategy Data:
- Source: `Finance_data.csv`
- Contains survey data of investment patterns and preferences
- Used for generating personalized investment strategies
- Data includes age, income, investment preferences, risk tolerance, etc.

2. SEC Company Data:
- Fetched from SEC database via the Financial_Analysis_&_Automation.ipynb notebook
- Contains detailed company information including:
  - Business descriptions
  - Financial metrics
  - Industry classifications
  - Market performance indicators
- Used for providing informed stock recommendations

The data is processed and stored in Pinecone vector database, enabling semantic search and intelligent retrieval for both investment strategies and stock recommendations.

## Portfolio Allocation Guidelines

The system follows these key principles:
- Age-based risk capacity (100 - age = maximum equity exposure)
- Time horizon consideration (Short: <5 years, Medium: 5-10 years, Long: >10 years)
- Monthly surplus analysis
- Diversification across asset classes
- Conservative allocation for lower surplus ratios

## Fine-tuning Datasets

The system's AI models are fine-tuned on specialized financial datasets to enhance their performance in investment advisory tasks:

1. Investment Survey Dataset:
- Size: 10,000+ records of investment decisions and outcomes
- Source: `Finance_data.csv`
- Features:
  - Demographic information (age, gender, income)
  - Investment preferences and risk tolerance
  - Investment outcomes and performance metrics
  - Historical investment decisions
- Used for: Training the investment strategy recommendation model

2. Market Analysis Dataset:
- Source: SEC EDGAR database
- Coverage: All publicly traded companies in US markets
- Data points:
  - Company descriptions and business summaries
  - Financial statements and metrics
  - Industry classifications
  - Market performance indicators
- Used for: Fine-tuning the stock recommendation system

3. Model Training Process:
- Initial training on general financial knowledge
- Fine-tuning on domain-specific datasets
- Continuous learning from new market data
- Regular model updates with latest financial information

The fine-tuning process ensures that the AI models understand:
- Market-specific terminology and concepts
- Complex financial relationships
- Risk assessment patterns
- Investment timing strategies
- Industry-specific trends and indicators

## Prompt Engineering & Investment Guidelines

### Input Validation Rules
The system enforces strict validation on user inputs to ensure reliable advice:
- Age: Must be between 18 and 100 years
- Monthly Income: Must be greater than 0
- Monthly Expenditure: Must be less than Monthly Income
- Current Savings: Must be greater than or equal to 0
- Investment Duration: Must be between 1 and 40 years

### Portfolio Allocation Constraints
All portfolio allocations must follow these guidelines:

1. Asset Class Limits (Total must be exactly 100%):
   - Equity/Stocks: 0-75%
   - Mutual Funds: 0-50%
   - Government Bonds: 10-60%
   - Fixed Deposits: 5-40%
   - Gold: 0-25%
   - Others: 0-20%

2. Risk Profile Calculation:
   - Maximum equity exposure = (100 - age)
   - Time horizon categorization:
     * Short-term: < 5 years
     * Medium-term: 5-10 years
     * Long-term: > 10 years
   - Conservative allocation if monthly surplus < 20% of income

### Investment Advisory Restrictions
The system is explicitly designed NOT to provide advice on:
- Individual stocks or securities
- Market timing strategies
- Tax planning
- Insurance products
- Real estate investments
- Cryptocurrency
- Forex trading
- Complex derivatives

### Prompt Engineering Principles
1. Response Structure:
   - Clear section-wise organization
   - Explicit percentage allocations
   - Brief explanations for each recommendation
   - Standard risk disclaimers

2. Advisory Guidelines:
   - Must include at least one cautionary advice
   - Must specify minimum investment horizon
   - Must emphasize diversification principle
   - No specific stock/fund recommendations
   - No tax advice unless explicitly qualified

3. Context Integration:
   - Incorporates user profile data
   - References similar investment patterns
   - Considers market conditions
   - Adapts to investment objectives
   - Accounts for risk tolerance

This structured prompt engineering ensures consistent, responsible, and personalized investment advice while maintaining regulatory compliance and risk management.

## Disclaimer

This is an AI-powered advisory tool and should not be considered as financial advice. Always consult with a qualified financial advisor before making investment decisions.
```
>>>>>>> 5eec6fd (updated comprehensive README.md)
