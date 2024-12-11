import streamlit as st
from dotenv import load_dotenv
import os
import yfinance as yf
from utils.db import initialize_pinecone
from utils.ai import perform_chat_rag
from sentence_transformers import SentenceTransformer
import streamlit.components.v1 as components
from transformers import pipeline
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from pinecone import Pinecone
import utils.utils as ut
from openai import OpenAI


# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Initialize Pinecone for CHAT
index_name = "finov1"
pinecone_index = initialize_pinecone(PINECONE_API_KEY, "us-east-1", index_name)

# initialize Pinecone for Stock Analysis
pc = Pinecone(PINECONE_API_KEY)
index_name = "stocks"
namespace = "stock-description_detailed"
# Connect to the Pinecone index
pinecone_index = pc.Index(index_name)

# initialize OpenAI Client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY")
)

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
        latest_price = data["Close"][-1]
        monthly_avg = data["Close"].resample("ME").mean().iloc[-1]
        yearly_high = data["High"].max()
        yearly_low = data["Low"].min()

        net_income = stock_info.get("netIncome", None)
        total_equity = stock_info.get("totalStockholderEquity", None)
        roe = (net_income / total_equity * 100) if net_income and total_equity else None

        total_liabilities = stock_info.get("totalLiabilities", None)
        total_assets = stock_info.get("totalAssets", None)
        debt_ratio = (
            (total_liabilities / total_assets * 100)
            if total_liabilities and total_assets
            else None
        )

        pe_ratio = stock_info.get("trailingPE", None)

        return (
            latest_price,
            monthly_avg,
            yearly_high,
            yearly_low,
            roe,
            debt_ratio,
            pe_ratio,
        )
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
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <div style="background-color: #0F1116; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; width: 100%; position: relative; bottom: 0; left: 0; text-align: center;">
        <p style="color: #FFFFFF; font-style: italic; margin-bottom: 1rem;">
        "AI in finance isn't just about algorithms; it's about empowering individuals to make smarter financial decisions for a better tomorrow."
        </p>
        <p style="color: #FFFFFF;">Copyright © 2024 FinovAI</p>
        <div style="margin-top: 1rem;">
            <h4 style="color: #00FF9D;">Contact Us:</h4>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
                <!-- Abhinav Pandey -->
                <div style="text-align: center;">
                    <p style="color: #FFFFFF; margin-bottom: 0.5rem;">Abhinav Pandey</p>
                    <a href="https://www.linkedin.com/in/abhinavpandey-/" target="_blank" style="margin-right: 1rem;">
                        <i class="fa fa-linkedin" style="font-size: 24px; color: #00FF9D;"></i>
                    </a>
                    <a href="https://github.com/abhinavpklg" target="_blank">
                        <i class="fa fa-github" style="font-size: 24px; color: #00FF9D;"></i>
                    </a>
                </div>
                <!-- Anuj Sharma -->
                <div style="text-align: center;">
                    <p style="color: #FFFFFF; margin-bottom: 0.5rem;">Anuj Sharma</p>
                    <a href="https://www.linkedin.com/in/anujsharma787/" target="_blank" style="margin-right: 1rem;">
                        <i class="fa fa-linkedin" style="font-size: 24px; color: #00FF9D;"></i>
                    </a>
                    <a href="https://github.com/anujy787" target="_blank">
                        <i class="fa fa-github" style="font-size: 24px; color: #00FF9D;"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


def summarize_text(text, max_length=130):
    try:
        prompt = f"""Please summarize the following text in a concise way (around {max_length} characters):

Text: {text}

Summary:"""
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # or "llama-3.1-70b-versatile"
            messages=[
                {"role": "system", "content": "You are a text summarization expert. Provide clear, concise summaries while maintaining key information."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error summarizing text: {str(e)}")
        return "Summary not available."


def fetch_news(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return articles
    else:
        print(f"Failed to fetch news: {response.status_code}")
        return []


def create_gauge_chart(value, title, min_value=0, max_value=100):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={"axis": {"range": [min_value, max_value]}},
        )
    )
    return fig


def format_matches(top_matches):
    seen_tickers = set()
    ticker_details = []

    for match in top_matches["matches"]:
        ticker = match["metadata"]["Ticker"]

        # Skip if we've already seen this ticker
        if ticker in seen_tickers:
            continue

        seen_tickers.add(ticker)
        ticker_details.append(
            {
                "ticker": ticker,
                "name": match["metadata"]["Name"],
                "business_summary": match["metadata"]["Business Summary"],
                "website": match["metadata"]["Website"],
                "revenue_growth": match["metadata"]["Revenue Growth"],
                "gross_margins": match["metadata"]["Gross Margins"],
                "target_m_price": match["metadata"]["Target Mean Price"],
                "current_price": match["metadata"]["Current Price"],
                "52weekchange": match["metadata"]["52 Week Change"],
                "sector": match["metadata"]["Sector"],
                "market_cap": match["metadata"]["Market Cap"],
                "volume": match["metadata"]["Volume"],
                "recommendation_key": match["metadata"]["Recommendation Key"],
                "text": match["metadata"]["text"],
            }
        )
    return ticker_details


def get_huggingface_embeddings(
    text, model_name="sentence-transformers/all-mpnet-base-v2"
):
    model = SentenceTransformer(model_name)
    return model.encode(text)


def augment_query_context(query, top_matches_formatted):
    context = "<CONTEXT>\n"
    for ticker in top_matches_formatted:
        context += f"\n\n--------\n\n {ticker['text']}\n Sector is {ticker['sector']}. \n Market Cap is {ticker['market_cap']}. \n Volume is {ticker['volume']}."
    augmented_query = f"{context} \nMY QUESTION:\n {query}"
    return augmented_query


# Perform rag
def perform_rag(query, user_filters):
    # embed the query
    raw_query_embedding = get_huggingface_embeddings(query)

    # apply filter to the metadata
    if user_filters:

        market_cap = user_filters["Market Cap"]
        volume = user_filters["Volume"]
        recommendation_keys = user_filters["Recommendation Keys"]

        filter = {
            "$and": [
                {"Market Cap": {"$gte": market_cap}},
                {"Volume": {"$gte": volume}},
                {"52 Week Change": {"$gte": -0.2}},
                {"Recommendation Key": {"$in": recommendation_keys}},
            ]
        }
    else:
        filter = {
            "$and": [
                {"52 Week Change": {"$gt": 0}},
                {"Recommendation Key": {"$in": ["buy", "strong buy", "hold"]}},
            ]
        }

    # print("filter: ", filter)

    # find the top matches
    top_matches = pinecone_index.query(
        vector=raw_query_embedding.tolist(),
        filter=filter,
        top_k=12,
        include_metadata=True,
        namespace=namespace,
    )
    top_matches_formatted = format_matches(top_matches)

    # with open("top_matches.txt", "w") as file:
    # # Convert top_matches to a JSON string for better readability
    #     file.write(json.dumps(top_matches, indent=4))  # Use indent for pretty printing

    augmented_query = augment_query_context(query, top_matches_formatted)

    system_prompt = """You are a financial expert at providing answers about stocks. Please answer my question provided.
            Analyze the stocks' in detail and explain current performance and potential future trends.
            Identify any notable connections or relationships with other stocks (e.g., industry, market correlation, or shared factors).
            Provide a concise, actionable insight to guide investment decisions.
    """
    try:
        llm_response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": augmented_query},
            ],
        )
    except:
        llm_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": augmented_query},
            ],
        )

    response = llm_response.choices[0].message.content
    return top_matches_formatted, response


def render_stock_block(stock):
    st.markdown(
        """<style>
        .small-font {font-size:12px; color:rgb(128, 128, 128);}
        .number-font {font-size:20px; font-weight:bold;}
        .metric-container {display: inline-block; width: 33%; margin-bottom: 10px;}
    </style>""",
        unsafe_allow_html=True,
    )

    # Create a container for the stock block
    with st.container():
        # Header information
        st.markdown(f"#### {stock['name']} ({stock['ticker']})")
        st.markdown(f"Website: {stock['website']}", unsafe_allow_html=True)

        # Use HTML/CSS grid instead of Streamlit columns
        metrics_html = f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
            <div class="metric-container">
                <div class="small-font">Revenue Growth</div>
                <div class="number-font">{ut.safe_format(stock['revenue_growth'])}</div>
            </div>
            <div class="metric-container">
                <div class="small-font">Gross Margins</div>
                <div class="number-font">{ut.safe_format(stock['gross_margins'])}</div>
            </div>
            <div class="metric-container">
                <div class="small-font">Market Cap</div>
                <div class="number-font">{ut.format_large_number(stock['market_cap'])}</div>
            </div>
            <div class="metric-container">
                <div class="small-font">Volume</div>
                <div class="number-font">{ut.format_large_number(stock['volume'])}</div>
            </div>
            <div class="metric-container">
                <div class="small-font">Valuation</div>
                <div class="number-font">{ut.format_colored_number((stock['target_m_price'] - stock['current_price']) / stock['current_price'])}</div>
            </div>
            <div class="metric-container">
                <div class="small-font">52 Week Change</div>
                <div class="number-font">{ut.format_colored_number(stock['52weekchange'])}</div>
            </div>
        </div>
        """
        st.markdown(metrics_html, unsafe_allow_html=True)


def main():
    st.set_page_config(layout="wide")
    create_header()

    main_col, timeline_col = st.columns([0.75, 0.25])

    with main_col:
        tab1, tab2, tab3 = st.tabs(
            ["📊 Ticker Information", "💬 Chat with FinovAI", "📉 AI Stock Analysis"]
        )

        with tab1:
            st.title("Financial Market Dashboard")
            company_input = st.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")
            if company_input:
                with st.spinner("Fetching stock data..."):
                    try:
                        if (
                            company_input.upper()
                            in yf.Tickers(company_input.upper()).tickers
                        ):
                            ticker = company_input.upper()
                        else:
                            ticker = get_ticker_from_company_name(company_input)
                        stock_info, data = fetch_stock_data(ticker)
                        if not data.empty:
                            st.subheader(
                                f"{stock_info.get('shortName', 'Unknown')} ({ticker.upper()})"
                            )
                            long_summary = stock_info.get(
                                "longBusinessSummary", "No summary available."
                            )
                            summarized_summary = summarize_text(long_summary)
                            st.write(summarized_summary)

                            st.subheader("📈 Key Performance Indicators (KPIs):")
                            (
                                latest_price,
                                monthly_avg,
                                yearly_high,
                                yearly_low,
                                roe,
                                debt_ratio,
                                pe_ratio,
                            ) = calculate_kpis(data, stock_info)
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Latest Price", f"${latest_price:.2f}")
                            col2.metric("Monthly Average", f"${monthly_avg:.2f}")
                            col3.metric("52-Week High", f"${yearly_high:.2f}")
                            col4.metric("52-Week Low", f"${yearly_low:.2f}")

                            st.subheader("Financial Ratios")
                            col5, col6, col7 = st.columns(3)
                            roe = stock_info.get("returnOnEquity", 0) * 100
                            debt_ratio = stock_info.get("debtToEquity", 0) * 100
                            pe_ratio = stock_info.get("trailingPE", 0)
                            col5.plotly_chart(
                                create_gauge_chart(roe, "ROE (%)"),
                                use_container_width=True,
                            )
                            col6.plotly_chart(
                                create_gauge_chart(debt_ratio, "Debt Ratio (%)"),
                                use_container_width=True,
                            )
                            col7.plotly_chart(
                                create_gauge_chart(pe_ratio, "P/E Ratio"),
                                use_container_width=True,
                            )

                            st.subheader("📉 Stock Price History (1 Year):")
                            fig = go.Figure(
                                data=[
                                    go.Candlestick(
                                        x=data.index,
                                        open=data["Open"],
                                        high=data["High"],
                                        low=data["Low"],
                                        close=data["Close"],
                                    )
                                ]
                            )
                            fig.update_layout(
                                title="Candlestick Chart",
                                xaxis_title="Date",
                                yaxis_title="Price",
                            )
                            st.plotly_chart(fig, use_container_width=True)

                            st.subheader("📊 Additional Insights:")

                            st.write("### Volume Distribution")
                            volume_data = data["Volume"].resample("ME").sum()
                            fig1 = px.pie(
                                values=volume_data.values,
                                names=volume_data.index.strftime("%b"),
                                title="Monthly Volume Distribution",
                                hole=0.3,
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
                                    x=0.5,
                                ),
                            )
                            st.plotly_chart(fig1)

                            st.write("### Monthly Average Close Price")
                            monthly_close_avg = data["Close"].resample("ME").mean()
                            fig2 = px.bar(
                                x=monthly_close_avg.index.strftime("%b"),
                                y=monthly_close_avg,
                                labels={"x": "Month", "y": "Average Close Price"},
                                title="Monthly Average Close Price",
                            )
                            st.plotly_chart(fig2, use_container_width=True)

                            st.write("### Daily Price Change Histogram")
                            daily_change = data["Close"].diff().dropna()
                            fig3 = px.histogram(
                                daily_change,
                                nbins=30,
                                title="Daily Price Change Distribution",
                                labels={"value": "Price Change", "count": "Frequency"},
                            )
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

            user_profile = {
                "gender": gender,
                "age": age,
                "income": income,
                "expenditure": expenditure,
                "savings": savings,
                "objective": objective,
                "duration": duration
            }

            if "history" not in st.session_state:
                st.session_state["history"] = []

            st.write("---")
            for i in range(len(st.session_state["history"]) - 1, -1, -1):
                user_msg, ai_response = st.session_state["history"][i]
                st.write(f"**Question:** {user_msg}")
                st.write(f"**Response:** {ai_response}")

            user_input = st.text_input("Type your question here:", key="user_input")

            if user_input:
                with st.spinner("Generating response..."):
                    try:
                        # Use RAG-enhanced chat completion
                        response = perform_chat_rag(user_input, user_profile, pinecone_index)
                        
                        if response:
                            st.session_state["history"].append((user_input, response))
                            st.write(f"**You:** {user_input}")
                            st.write(f"**Advisor:** {response}")
                        else:
                            st.error("Failed to get response from the model")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

            if st.button("Reset Chat"):
                st.session_state["history"] = []

        with tab3:
            st.title("📉 AI Stock Analysis")
            st.caption("Get Automated Stock Analysis done right here!")
            user_query = st.text_area(
                "Enter a description for the kind of stocks you are looking for:",
                placeholder="Type here",
            )

            with st.expander("Apply filters"):
                market_cap = st.number_input(
                    "Market Cap",
                    min_value=0,
                    max_value=10000000000000,
                    value=1000000,
                    step=1000,
                )
                volume = st.number_input(
                    "Volume", min_value=0, max_value=1000000000, value=10000, step=100
                )
                recommendation_keys = [
                    "strong buy",
                    "buy",
                    "hold",
                    "sell",
                    "strong sell",
                ]
                selected_recommendation_keys = st.multiselect(
                    "Recommendation Keys:",
                    recommendation_keys,
                    ["strong buy", "buy", "hold"],
                )

                user_filters = {
                    "Market Cap": market_cap,
                    "Volume": volume,
                    "Recommendation Keys": selected_recommendation_keys,
                }

            if st.button("Find Stocks", key="find_stocks_button"):
                top_matches, results = perform_rag(user_query, user_filters)
                with st.container():
                    if top_matches:
                        cols_main = st.columns(2)
                        with cols_main[0]:
                            for match in top_matches[:2]:
                                render_stock_block(match)

                        with cols_main[1]:
                            for match in top_matches[2:4]:
                                render_stock_block(match)
                    else:
                        st.write("No stocks found. Please refine your query.")

                    st.divider()
                    st.write("## Analysis")
                    st.write(results)

    create_footer()

    with timeline_col:
        trading_view_timeline()
        st.subheader("📰 Latest News")
        if company_input:
            news_articles = fetch_news(ticker)
            if news_articles:
                for article in news_articles[:5]:
                    st.markdown(f"**[{article['title']}]({article['url']})**")
                    st.write(article["description"])
                    st.write(f"Published at: {article['publishedAt']}")
                    st.write("---")
            else:
                st.write("No news articles found.")


if __name__ == "__main__":
    #freeze_support()
    main()
