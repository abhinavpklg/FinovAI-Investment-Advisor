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
from transformers import pipeline
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

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
    stock_info = stock.info
    return stock_info, data

def get_ticker_from_company_name(company_name):
    search_results = yf.Ticker(company_name)
    ticker_symbol = search_results.ticker
    return ticker_symbol

def calculate_kpis(data, stock_info):
    if not data.empty:
        latest_price = data['Close'][-1]
        monthly_avg = data['Close'].resample('M').mean().iloc[-1]
        yearly_high = data['High'].max()
        yearly_low = data['Low'].min()

        net_income = stock_info.get('netIncome', None)
        total_equity = stock_info.get('totalStockholderEquity', None)
        roe = (net_income / total_equity * 100) if net_income and total_equity else None

        total_liabilities = stock_info.get('totalLiabilities', None)
        total_assets = stock_info.get('totalAssets', None)
        debt_ratio = (total_liabilities / total_assets * 100) if total_liabilities and total_assets else None

        pe_ratio = stock_info.get('trailingPE', None)

        return latest_price, monthly_avg, yearly_high, yearly_low, roe, debt_ratio, pe_ratio
    return None, None, None, None, None, None, None

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

summarizer = pipeline("summarization")

def summarize_text(text, max_length=130, min_length=30):
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error summarizing text: {str(e)}")
        return "Summary not available."

def fetch_news(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return articles
    else:
        print(f"Failed to fetch news: {response.status_code}")
        return []

def create_gauge_chart(value, title, min_value=0, max_value=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [min_value, max_value]}}
    ))
    return fig

def main():
    st.set_page_config(layout="wide")
    create_header()

    main_col, timeline_col = st.columns([0.75, 0.25])

    with main_col:
        tab1, tab2 = st.tabs(["📊 Ticker Information", "💬 Chat with FinovAI"])

        with tab1:
            st.title("Financial Market Dashboard")
            company_input = st.text_input("Enter Stock Ticker or Company Name (e.g., AAPL, Tesla):", "AAPL")
            if company_input:
                with st.spinner('Fetching stock data...'):
                    try:
                        if company_input.upper() in yf.Tickers(company_input.upper()).tickers:
                            ticker = company_input.upper()
                        else:
                            ticker = get_ticker_from_company_name(company_input)
                        stock_info, data = fetch_stock_data(ticker)
                        if not data.empty:
                            st.subheader(f"{stock_info.get('shortName', 'Unknown')} ({ticker.upper()})")
                            long_summary = stock_info.get('longBusinessSummary', 'No summary available.')
                            summarized_summary = summarize_text(long_summary)
                            st.write(summarized_summary)

                            st.subheader("📈 Key Performance Indicators (KPIs):")
                            latest_price, monthly_avg, yearly_high, yearly_low, roe, debt_ratio, pe_ratio = calculate_kpis(data, stock_info)
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Latest Price", f"${latest_price:.2f}")
                            col2.metric("Monthly Average", f"${monthly_avg:.2f}")
                            col3.metric("52-Week High", f"${yearly_high:.2f}")
                            col4.metric("52-Week Low", f"${yearly_low:.2f}")

                            st.subheader("Financial Ratios")
                            col5, col6, col7 = st.columns(3)
                            roe = stock_info.get('returnOnEquity', 0) * 100
                            debt_ratio = stock_info.get('debtToEquity', 0) * 100
                            pe_ratio = stock_info.get('trailingPE', 0)
                            col5.plotly_chart(create_gauge_chart(roe, "ROE (%)"), use_container_width=True)
                            col6.plotly_chart(create_gauge_chart(debt_ratio, "Debt Ratio (%)"), use_container_width=True)
                            col7.plotly_chart(create_gauge_chart(pe_ratio, "P/E Ratio"), use_container_width=True)

                            st.subheader("📉 Stock Price History (1 Year):")
                            fig = go.Figure(data=[go.Candlestick(
                                x=data.index,
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close']
                            )])
                            fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
                            st.plotly_chart(fig, use_container_width=True)

                            st.subheader("📊 Additional Insights:")

                            st.write("### Volume Distribution")
                            volume_data = data['Volume'].resample('M').sum()
                            fig1 = px.pie(
                                values=volume_data.values,
                                names=volume_data.index.strftime('%b'),
                                title='Monthly Volume Distribution',
                                hole=0.3
                            )
                            fig1.update_layout(
                                autosize=False,
                                width=400,
                                height=400,
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=-0.2,
                                    xanchor="center",
                                    x=0.5
                                )
                            )
                            st.plotly_chart(fig1)

                            st.write("### Monthly Average Close Price")
                            monthly_close_avg = data['Close'].resample('M').mean()
                            fig2 = px.bar(x=monthly_close_avg.index.strftime('%b'), y=monthly_close_avg, labels={'x': 'Month', 'y': 'Average Close Price'}, title='Monthly Average Close Price')
                            st.plotly_chart(fig2, use_container_width=True)

                            st.write("### Daily Price Change Histogram")
                            daily_change = data['Close'].diff().dropna()
                            fig3 = px.histogram(daily_change, nbins=30, title='Daily Price Change Distribution', labels={'value': 'Price Change', 'count': 'Frequency'})
                            st.plotly_chart(fig3, use_container_width=True)

                            st.subheader("Detailed Metrics:")
                            st.dataframe(data.tail(10))
                        else:
                            st.error("No data available for the given ticker.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

        with tab2:
            st.title("Chat with FinovAI")
            st.subheader("Provide Your Details")
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

            st.write("---")
            st.write("**Chat History:**")
            for i in range(len(st.session_state["history"]) - 1, -1, -1):
                user_msg, ai_response = st.session_state["history"][i]
                st.write(f"**You:** {user_msg}")
                st.write(f"**Advisor:** {ai_response}")

            if st.button("Reset Chat"):
                st.session_state["history"] = []

    create_footer()

    with timeline_col:
        trading_view_timeline()
        st.subheader("📰 Latest News")
        if company_input:
            news_articles = fetch_news(ticker)
            if news_articles:
                for article in news_articles[:5]:
                    st.markdown(f"**[{article['title']}]({article['url']})**")
                    st.write(article['description'])
                    st.write(f"Published at: {article['publishedAt']}")
                    st.write("---")
            else:
                st.write("No news articles found.")

if __name__ == "__main__":
    freeze_support()
    main()
