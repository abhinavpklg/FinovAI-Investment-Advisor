# FinovAI : AI-Powered Investment Advisor

FinovAI is an intelligent investment advisory system that leverages artificial intelligence to provide personalized investment strategies and stock recommendations. The system uses **Retrieval Augmented Generation (RAG)** with vector databases to analyze market data and provide informed investment advice.

---
## 🚀 Live: https://finovai.streamlit.app/
---

## 🖥️ System Architecture

![Screenshot 2024-12-11 185208](https://github.com/user-attachments/assets/af4a891d-0471-4150-97e8-c8cc822d9957)


---

## ✨ Features

- 🌟 **Personalized Investment Strategies**: Tailored recommendations based on user profiles.
- 📈 **Stock Recommendations**: Insights powered by RAG and SEC company data.
- ⚖️ **Portfolio Allocation**: Guidelines aligned with risk profiles and investment goals.
- ⏱️ **Real-Time Market Data**: Integration with Yahoo Finance for live updates.
- 🔍 **Semantic Search**: Efficient company information retrieval.
- 🖥️ **Interactive Web Interface**: Built with Streamlit for seamless user experience.

---

## 🎨 User Interface

The application features a modern, user-friendly interface built using Streamlit, offering:

- 🧭 **Clean Navigation**: Intuitive design for easy exploration.
- ✍️ **Interactive Forms**: Simplified user profile input.
- 📊 **Real-Time Graphs**: For better visualization of data.
- 🔄 **Dynamic Recommendations**: Instant and data-driven.
- 📝 **Clear Presentations**: Easy-to-understand investment strategies.

---

## 🛠️ Technology Stack

- **🐍 Python**: Core programming language for building the application.
- **🌐 Streamlit**: Framework for creating an interactive and user-friendly web interface.
- **📦 Pinecone**: Vector database used for Retrieval Augmented Generation (RAG) capabilities.
- **💹 Yahoo Finance API**: Provides real-time market data for stock analysis.
- **📒 Jupyter Notebook**: Used for data analysis, processing, and workflow setup.
- **🚀 Groq API**: Enables high-performance AI inference for fast and accurate predictions.


---

## 🤖 AI Model Configuration

### 🌟 Primary Model
- **Model**: `llama-3.1-70b-versatile`
- **Features**:
  - ✅ High-accuracy financial analysis
  - ⚙️ Comprehensive market understanding
  - 💡 Sophisticated investment strategy generation
  - 🚀 Fast inference using Groq's infrastructure
  - ⏳ Real-time response capabilities

### ❄️ Fallback Model
- **Model**: `llama-3.1-8b-instant`
- **Purpose**: Automatic fallback during high-traffic periods or model unavailability.
- **Benefits**:
  - ⏫ Lower latency
  - 📈 Handles basic queries efficiently

### 🔄 Performance Optimization
- **Groq API** for high-speed inference.
- **Automatic model switching** based on:
  - System load
  - Query complexity
  - Response time requirements
  - Service availability
- **Optimized prompt engineering** for the financial domain.
- **Efficient context handling** for RAG implementation.

---

🗂️ Project Structure

The project is organized as follows:

The following is an overview of the project's folder structure:

```plaintext
.
├── Financial_Analysis_&_Automation.ipynb   # Notebook for SEC data processing and analysis
├── README.md                               # Project documentation
├── app.py                                  # Streamlit application script
├── company_tickers.json                    # JSON file with company tickers
├── data                                    # Fine Tuning Dataset and RAG Knowledge Base
│   ├── Finance_data.csv
|   ├── training_data1.csv
|   ├── training_data2.csv
|   └── training_data3.csv
├── requirements.txt                        # List of project dependencies
├── setup.py                                # Script for initializing Pinecone vector database
├── successful_tickers.txt                  # File with successfully processed tickers
├── text_embeddings.py                      # Script for generating text embeddings
├── unsuccessful_tickers.txt                # File with unsuccessfully processed tickers
└── utils
    ├── ai.py                               # AI-related utility functions
    ├── db.py                               # Database interaction scripts
    ├── prompts.py                          # Prompt engineering for AI models
    └── utils.py                            # General utility functions

```
---

## 🔧 Setup Instructions

1. **Create and activate a Python virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file with your API keys:
   ```plaintext
   PINECONE_API_KEY=your_pinecone_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Initialize the vector database**:
   ```bash
   python setup.py
   ```
   This will set up the Pinecone vector database for RAG-based investment strategy generation.

5. **Run the Jupyter notebook**:
   ```bash
   jupyter notebook financial_analysis_automation.ipynb
   ```
   This notebook contains code for setting up the vector database in Pinecone for stock recommendations using SEC data.

6. **Launch the Streamlit application**:
   ```bash
   streamlit run app.py
   ```
   This will start the web interface on your local machine, typically at [http://localhost:8501](http://localhost:8501).

---

## 🧪 Test Suite Documentation

### 📊 Test Categories

1. **📈 Stock Analysis Testing**
   - ✅ Market cap & volume filter validation
   - 🔄 Data processing pipeline verification
   - 📊 Financial metrics computation accuracy
   - 💹 Historical data integrity checks

2. **👤 User Profile Validation**
   - 🔒 Age verification (18-100 years)
   - 💰 Income & expenditure validation
   - ⏳ Investment horizon checks (1-40 years)
   - 🎯 Financial goals assessment
   - 📝 Profile completeness verification

3. **🤖 Recommendation Engine Testing**
   - 🎯 Algorithm accuracy validation
   - 📋 Output format compliance
   - 🔍 Recommendation filtering logic
   - 📊 Risk-profile alignment checks
   - ⚖️ Portfolio balance verification

4. **⚠️ Error Handling & Edge Cases**
   - 🚫 Invalid profile data handling
   - ⚡ API failure recovery
   - 🔄 Service integration resilience
   - 📝 Missing data management
   - 🛡️ Input sanitization verification

### ⚙️ Test Execution Guide

Run the comprehensive test suite using:

```bash
pytest tests/test_financial_analysis.py -v --html=report.html
```

This command:
- 🔍 Executes all test cases with verbose output
- 📄 Generates an HTML report for easy review
- ⏱️ Displays execution time for each test
- 📊 Provides detailed failure analysis

---

## 📝 Example Conversations

### ✅ Investment Strategy Generation:
```
Question: Generate a financial strategy

Response: Financial Investment Strategy for Wealth Creation

Disclaimer: Investments carry risks, and past performance is not a guarantee of future results. It is essential to diversify your portfolio and consult a financial advisor before making any investment decisions.

Client Profile:

Age: 28
Monthly Income: $7,000
Monthly Expenditure: $3,000
Current Savings: $300,000
Investment Objective: Wealth creation
Investment Duration: 7 years
Initial Assessment: Based on the provided data, the client has a substantial monthly surplus (4,000) and a sizeable savings amount (4,000)and a sizeable savings amount(300,000), which can be leveraged to create wealth through investments.

Investment Allocation: The recommended portfolio allocation is:

Equity/Stocks: 40% (Risk Profile: Age-based risk capacity allows for 72% equity exposure; we are taking 40% to balance risk and reward)
Mutual Funds: 25% (balancing risk and providing liquidity)
Government Bonds: 20% (mitigating interest rate risk and providing a stable return component)
Fixed Deposits: 10% (providing liquidity and return with minimal risk)
Gold: 5% (hedging against inflation and uncertainty)
Justification:

Age: The client is 28, with a medium to high-risk profile. This allows for a balanced allocation between equities, mutual funds, and bonds.
Time Horizon: With a 7-year investment duration, we have a medium-term time horizon, which can help to mitigate potential market fluctuations.
Monthly Surplus: The client has a substantial surplus, which can be used to invest and grow wealth.
Recommendations:

Minimum Investment Horizon: A minimum investment horizon of 5 years is recommended to help smooth out potential market fluctuations.
Diversification: A diversified portfolio will help to minimize risk and maximize potential returns.
Cautionary Advice: Markets can be volatile; we strongly advise against making emotional decisions during market downturns. Sticking to a well-thought-out investment plan is crucial for long-term success.
Investment Principles:

Dollar-Cost Averaging: Invest a fixed amount of money at regular intervals, regardless of market conditions, to smooth out market volatility.
Regular Portfolio Rebalancing: Periodically review and rebalance your portfolio to maintain the target allocation and minimize risk.
Standard Disclaimer: This investment strategy is based on generally accepted investment principles and may not be suitable for every investor. Past performance is not a guarantee of future results, and investments carry inherent risks.
```

### 📊 Stock Analysis:
```
User: I want to invest in Battery technologies?

Response:

Based on the provided information, I will analyze the stocks in detail, identify notable connections, and provide concise, actionable insights to guide investment decisions related to battery technologies.

Stock Analysis:

Generac Holdings Inc.: As a leading manufacturer of energy technology products and solutions, Generac is a significant player in the battery technology space. Their residential storage solution, which consists of a system of batteries, an inverter, photovoltaic optimizers, power electronic controls, and other components, positions them well for growth in the energy storage market. With a strong product lineup and proven expertise in the energy technology sector, Generac is an attractive investment opportunity for those looking to capitalize on the growing demand for battery technologies.
AMETEK, Inc.: Although AMETEK is a diversified company with a wide range of products and services, their offerings in the energy storage space are relatively limited compared to Generac. However, their EIG segment's focus on power quality monitoring devices, uninterruptible power supplies, and sensors for gas turbines could potentially benefit from advancements in battery technologies.
Albemarle Corporation: As a leading supplier of lithium, a critical component in battery technologies, Albemarle is well-positioned to capitalize on the growing demand for energy storage solutions. Their Energy Storage segment offers lithium compounds, which are used in a variety of battery applications, including electric vehicles and renewable energy systems.
GE Vernova Inc.: GE Vernova's Electrification segment offers grid solutions, power conversion, solar, and storage solutions, including electrification software. While they may not be a direct player in battery technologies, their involvement in the energy storage space and focus on grid modernization could benefit from advancements in battery technologies.
Notable Connections:

Lithium supply chain: Albemarle Corporation's dominance in the lithium market provides a critical component for battery technologies. As demand for lithium-ion batteries increases, Albemarle is well-positioned to benefit from the growth.
Industry partnerships: Generac Holdings Inc. and GE Vernova Inc. may benefit from partnerships in the energy storage space, potentially leveraging each other's expertise to drive innovation and growth.
Grid modernization: GE Vernova's focus on grid modernization and electrification could lead to increased demand for energy storage solutions, benefiting companies like Generac Holdings Inc. and Albemarle Corporation.
Actionable Insights:

Invest in Generac Holdings Inc.: With a strong product lineup and proven expertise in the energy technology sector, Generac is well-positioned to capitalize on the growing demand for battery technologies.
Monitor Albemarle Corporation: As a leading supplier of lithium, Albemarle is poised to benefit from the growing demand for energy storage solutions. Their stock price may fluctuate based on lithium demand and supply dynamics.
Watch for partnerships and innovations: Keep an eye on potential partnerships between Generac Holdings Inc., GE Vernova Inc., and other industry players, as well as innovations in battery technologies that could drive growth and adoption.
Investment Strategy:

Long-term growth: Invest in Generac Holdings Inc. and Albemarle Corporation for long-term growth potential in the battery technology space.
Diversification: Consider adding GE Vernova Inc. to a diversified portfolio to capture growth opportunities in the energy storage and grid modernization space.
Monitor and adapt: Continuously monitor industry developments, partnerships, and innovations to adjust investment strategies accordingly.
```

---
## 📊 Source Data

The system utilizes data from the following sources:

### 1. Investment Dataset
- **Source**: [Kaggle Investment Dataset](https://www.kaggle.com/datasets/samulasrikanthreddy/investment-dataset)
- **Content**:
  - Comprehensive investment patterns
  - User demographics and preferences
  - Risk tolerance indicators
  - Investment outcomes
- **Purpose**: Training and fine-tuning investment strategy recommendations

### 2. SEC Company Data
- **Source**: [Company Tickers JSON](https://raw.githubusercontent.com/abhinavpklg/FinovAI-Investment-Advisor/refs/heads/main/company_tickers.json)
- **Content**:
  - Company identifiers and tickers
  - SEC filing information
  - Industry classifications
  - Company metadata
- **Purpose**: Stock analysis and company information retrieval

 Both datasets are processed and vectorized for use in our RAG system, enabling accurate and context-aware investment recommendations.
---

## 📂 RAG Knowledge Base

The system utilizes two main data sources for its RAG capabilities:

### 1. Investment Strategy Data:
- **Source**: `Finance_data.csv`
- **Content**:
  - Survey data of investment patterns and preferences
  - Includes age, income, investment preferences, risk tolerance, etc.
- **Purpose**: Generating personalized investment strategies.

### 2. SEC Company Data:
- **Source**: SEC EDGAR database
- **Content**:
  - Business descriptions
  - Financial metrics
  - Industry classifications
  - Market performance indicators
- **Purpose**: Providing informed stock recommendations.

The data is processed and stored in the Pinecone vector database, enabling semantic search and intelligent retrieval.

---

## 📊 Portfolio Allocation Guidelines

The system follows these key principles:
- 🧓 **Age-Based Risk Capacity**: `100 - age = maximum equity exposure`.
- ⏱️ **Time Horizon Consideration**:
  - Short-term: < 5 years
  - Medium-term: 5-10 years
  - Long-term: > 10 years
- 💰 **Monthly Surplus Analysis**.
- 🌐 **Diversification Across Asset Classes**.
- 🔒 **Conservative Allocation** for lower surplus ratios.

---

## 📈 Fine-Tuning Datasets

The system's AI models are fine-tuned on specialized financial datasets to enhance performance:

### 1. Investment Survey Dataset:
- **Size**: 10,000+ records of investment decisions and outcomes.
- **Source**: `Finance_data.csv`
- **Features**:
  - Demographics (age, gender, income).
  - Investment preferences and risk tolerance.
  - Historical investment outcomes.
- **Purpose**: Training the investment strategy recommendation model.

### 2. Market Analysis Dataset:
- **Source**: SEC EDGAR database
- **Coverage**: All publicly traded companies in US markets.
- **Content**:
  - Company descriptions
  - Financial statements
  - Industry classifications
  - Market performance indicators
- **Purpose**: Fine-tuning the stock recommendation system.

### 3. Model Training Process:
- Initial training on general financial knowledge.
- Fine-tuning on domain-specific datasets.
- Continuous learning from new market data.
- Regular model updates with the latest financial information.

---


## 🔮 Prompt Engineering & Investment Guidelines

### 📋 Input Validation Rules
- **Age**: Must be between 18 and 100 years.
- **Monthly Income**: Must be greater than 0.
- **Monthly Expenditure**: Must be less than monthly income.
- **Current Savings**: Must be ≥ 0.
- **Investment Duration**: Must be between 1 and 40 years.

### 📊 Portfolio Allocation Constraints
- **Asset Class Limits (Total = 100%)**:
  - Equity/Stocks: 0-75%
  - Mutual Funds: 0-50%
  - Government Bonds: 10-60%
  - Fixed Deposits: 5-40%
  - Gold: 0-25%
  - Others: 0-20%

### 🔎 Investment Advisory Restrictions
The system avoids:
- Individual stock/securities advice.
- Market timing strategies.
- Tax planning.
- Insurance products.
- Real estate investments.
- Cryptocurrency/Forex trading.
- Complex derivatives.

### 🎯 Prompt Engineering Principles
1. **Response Structure**:
   - Clear section-wise organization.
   - Explicit percentage allocations.
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
