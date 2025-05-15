import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="AI Stock Analyst",
    page_icon="📈",
    layout="wide"
)

# Constants
API_URL = os.environ.get('API_URL', 'http://localhost:5000/api/stock/analyze')

# Page title
st.title("🤖 AI Stock Analyst")
st.markdown("### Get AI-powered investment recommendations based on real-time news")

# Input form for ticker
with st.form("stock_form"):
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT)", value="")
    submitted = st.form_submit_button("Analyze")

# Process form submission
if submitted and ticker:
    with st.spinner(f"Analyzing {ticker.upper()}... Please wait."):
        try:
            # Call the API
            response = requests.post(
                API_URL,
                json={"ticker": ticker.upper()},
                headers={"Content-Type": "application/json"}
            )
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                
                # Display results in columns
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Stock information and recommendation
                    st.subheader(f"{data['company_name']} ({data['ticker']})")
                    
                    # Current price and metrics
                    price_metrics = st.container()
                    with price_metrics:
                        price_col1, price_col2, price_col3 = st.columns(3)
                        price_col1.metric("Current Price", f"${data['current_price']:.2f}")
                        
                        change_value = f"{data['price_change']:.2f}"
                        change_pct = f"{data['price_change_pct']:.2f}%"
                        delta_value = f"{change_value} ({change_pct})"
                        delta_color = "normal" if data['price_change'] == 0 else ("inverse" if data['price_change'] < 0 else "normal")
                        
                        price_col2.metric("Price Change (30d)", delta_value, delta_color=delta_color)
                        price_col3.metric("Sentiment", data['analysis']['sentiment'])
                    
                    # Price trend chart
                    st.subheader("Price Trend (Last 30 Days)")
                    
                    # Convert price data to DataFrame for plotting
                    price_df = pd.DataFrame(data['price_data'])
                    price_df['date'] = pd.to_datetime(price_df['date'])
                    price_df.set_index('date', inplace=True)
                    
                    # Create and display the chart
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(price_df.index, price_df['close'])
                    ax.set_xlabel('Date')
                    ax.set_ylabel('Price ($)')
                    ax.grid(True, alpha=0.3)
                    
                    # Customize colors based on trend
                    if data['price_change'] >= 0:
                        ax.plot(price_df.index, price_df['close'], color='green')
                    else:
                        ax.plot(price_df.index, price_df['close'], color='red')
                    
                    st.pyplot(fig)
                    
                with col2:
                    # AI Analysis results
                    st.subheader("AI Analysis")
                    
                    # Recommendation
                    rec = data['analysis']['recommendation']
                    rec_color = "green" if rec == "Buy" else ("red" if rec == "Sell" else "orange")
                    st.markdown(f"### Recommendation: <span style='color:{rec_color}'>{rec}</span>", unsafe_allow_html=True)
                    
                    # Summary
                    st.markdown("#### Summary")
                    st.write(data['analysis']['summary'])
                    
                    # Reasoning
                    st.markdown("#### Reasoning")
                    st.write(data['analysis']['reasoning'])
                    
                    # News articles
                    st.subheader("Recent News")
                    for article in data['news']:
                        st.markdown(f"**{article['title']}**")
                        st.markdown(f"*{article['publishedAt'][:10]}* - {article['source']['name']}")
                        st.markdown(f"{article['description']}")
                        st.markdown(f"[Read more]({article['url']})")
                        st.markdown("---")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    if submitted:
        st.warning("Please enter a stock ticker.")
    
    # Display placeholder content
    st.markdown("""
    ## How it works
    
    1. Enter a stock ticker symbol (e.g., AAPL for Apple Inc.)
    2. Our system fetches the latest news about the company
    3. AI analyzes the news sentiment and market trends
    4. You receive a clear investment recommendation: Buy, Hold, or Sell
    
    *Powered by OpenAI's language models and real-time market data*
    """)
    
    # Disclaimer
    st.markdown("""
    **Disclaimer**: This tool provides analysis for informational purposes only. 
    It is not intended as financial advice. Always conduct your own research and 
    consult with a qualified financial advisor before making investment decisions.
    """)

# Footer
st.markdown("---")
st.markdown("© 2023 AI Stock Analyst | Built with Streamlit and Flask") 