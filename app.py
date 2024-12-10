import streamlit as st
from dotenv import load_dotenv
import os
import yfinance as yf
from utils.db import initialize_pinecone, load_dataset_to_pinecone
from utils.prompts import financial_advisor_prompt
from utils.ai import initialize_huggingface_model, setup_retrieval_chain, generate_response
from multiprocessing import freeze_support
from sentence_transformers import SentenceTransformer
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
index_name = "finov1"
pinecone_index = initialize_pinecone(PINECONE_API_KEY, "us-east-1", index_name)

# Initialize AI model globally
@st.cache_resource
def get_model():
    return initialize_huggingface_model()

@st.cache_data
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    
    # Extract serializable parts
    stock_info = stock.info  # This is a dictionary and serializable
    return stock_info, data

def get_ticker_from_company_name(company_name):
    # Use yfinance to search for a company by name and retrieve the corresponding ticker symbol
    search_results = yf.Ticker(company_name)
    ticker_symbol = search_results.ticker
    return ticker_symbol

# Generate stock metrics
def calculate_kpis(data):
    if not data.empty:
        latest_price = data['Close'][-1]
        monthly_avg = data['Close'].resample('M').mean().iloc[-1]
        yearly_high = data['High'].max()
        yearly_low = data['Low'].min()
        return latest_price, monthly_avg, yearly_high, yearly_low
    return None, None, None, None

def trading_view_timeline():
    trading_view_html = """
    <div style="position: fixed; right: 0; top: 0; bottom: 0; width: 100%; height: 800; z-index: 1000;">
        <div class="tradingview-widget-container" style="height: 100%;">
            <div class="tradingview-widget-container__widget" style="height: 100%;"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
            {
                "feedMode": "all_symbols",
                "isTransparent": false,
                "displayMode": "regular",
                "width": "100%",
                "height": "100%",
                "colorTheme": "dark",
                "locale": "en"
            }
            </script>
        </div>
    </div>
    """
    components.html(trading_view_html, height=1650)

def create_header():
    header_html = """
        <div style="background-color: #0F1116; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: #FFFFFF; margin: 0;">FinovAI - AI powered Financial Advisor</h1>
        </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def create_footer():
    footer_html = """
        <div style="background-color: #0F1116; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; width: 100%; position: relative; bottom: 0; left: 0; text-align: center;">
            <p style="color: #FFFFFF; font-style: italic; margin-bottom: 1rem;">
                "AI in finance isn't just about algorithms; it's about empowering individuals to make smarter financial decisions for a better tomorrow."
            </p>
            <p style="color: #FFFFFF;">Copyright © 2024 FinovAI</p>
            <div style="margin-top: 1rem;">
                <h4 style="color: #00FF9D;">Contact Us:</h4>
                <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;">
                    <div>
                        <p style="color: #FFFFFF; margin-bottom: 0.5rem;">Abhinav Pandey</p>
                        <a href="https://www.linkedin.com/in/abhinavpandey-/" target="_blank" style="color: #00FF9D; text-decoration: none; margin-right: 1rem;">
                            [LinkedIn]
                        </a>
                        <a href="https://github.com/abhinavpklg" target="_blank" style="color: #00FF9D; text-decoration: none;">
                            [GitHub]
                        </a>
                    </div>
                    <div>
                        <p style="color: #FFFFFF; margin-bottom: 0.5rem;">Anuj Sharma</p>
                        <a href="https://www.linkedin.com/in/anujsharma787/" target="_blank" style="color: #00FF9D; text-decoration: none; margin-right: 1rem;">
                            [LinkedIn]
                        </a>
                        <a href="https://github.com/anujy787" target="_blank" style="color: #00FF9D; text-decoration: none;">
                            [GitHub]
                        </a>
                    </div>
                </div>
            </div>
        </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide")
    
    # Add header
    create_header()

    # Create two columns: one for main content (75%) and one for timeline (25%)
    main_col, timeline_col = st.columns([0.75, 0.25])

    # Main content in the left column
    with main_col:
        # Tabs inside the main content column
        tab1, tab2 = st.tabs(["📊 Ticker Information", "💬 Chat with FinovAI"])

        # Dashboard Tab
        with tab1:
            st.title("Financial Market Dashboard")
            company_input = st.text_input("Enter Stock Ticker or Company Name (e.g., AAPL, Tesla):", "AAPL")

            if company_input:
                with st.spinner('Fetching stock data...'):
                    try:
                        # First, check if the input is a ticker symbol
                        if company_input.upper() in yf.Tickers(company_input.upper()).tickers:
                            ticker = company_input.upper()
                        else:
                            # If it's a company name, resolve it to a ticker symbol
                            ticker = get_ticker_from_company_name(company_input)
                        
                        stock_info, data = fetch_stock_data(ticker)
                        
                        if not data.empty:
                            # Display company info
                            st.subheader(f"{stock_info.get('shortName', 'Unknown')} ({ticker.upper()})")
                            st.write(stock_info.get('longBusinessSummary', 'No summary available.'))

                            # Display KPIs
                            st.subheader("📈 Key Performance Indicators (KPIs):")
                            latest_price, monthly_avg, yearly_high, yearly_low = calculate_kpis(data)

                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Latest Price", f"${latest_price:.2f}")
                            col2.metric("Monthly Average", f"${monthly_avg:.2f}")
                            col3.metric("Yearly High", f"${yearly_high:.2f}")
                            col4.metric("Yearly Low", f"${yearly_low:.2f}")
                            
                            # Display stock chart
                            st.subheader("📉 Stock Price History (1 Year):")
                            st.line_chart(data["Close"])

                            # Display detailed metrics
                            st.subheader("Detailed Metrics:")
                            st.dataframe(data.tail(10))  # Show the last 10 rows of data
                        else:
                            st.error("No data available for the given ticker.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

        # Chat Tab
        with tab2:
            st.title("Chat with FinovAI")
            st.subheader("Provide Your Details")

            # Input fields for user details
            col1, col2 = st.columns(2)
            with col1:
                gender = st.radio("Gender", ("Male", "Female", "Other"))
                age = st.slider("Age", 18, 80)
                duration = st.number_input("Investment Duration (years)", min_value=1)
            with col2:
                income = st.number_input("Monthly Income", min_value=0)
                expenditure = st.number_input("Monthly Expenditure", min_value=0)
                savings = st.number_input("Current Savings", min_value=0)
            
            objective = st.text_input("Investment Objective")

            # Chat functionality
            if "history" not in st.session_state:
                st.session_state["history"] = []

            st.subheader("Ask Your Financial Question")
            user_input = st.text_input("Type your question:")
            if user_input:
                with st.spinner('Generating response...'):
                    try:
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
                        response = generate_response(get_model(), context_message)
                        if response:
                            st.session_state["history"].append((user_input, response))
                            st.write(f"**You:** {user_input}")
                            st.write(f"**Advisor:** {response}")
                        else:
                            st.error("Failed to get response from the model")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

            # Display chat history
            st.write("---")
            st.write("**Chat History:**")
            for i in range(len(st.session_state["history"]) - 1, -1, -1):
                user_msg, ai_response = st.session_state["history"][i]
                st.write(f"**You:** {user_msg}")
                st.write(f"**Advisor:** {ai_response}")

            # Reset button
            if st.button("Reset Chat"):
                st.session_state["history"] = []

    # Add footer at the end of the main function
    create_footer()

    # Timeline in the right column
    with timeline_col:
        trading_view_timeline()

if __name__ == "__main__":
    freeze_support()
    main()
