import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import os
from dotenv import load_dotenv
import time
import random
import plotly.graph_objects as go
from datetime import datetime

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="AI Stock Analyst",
    page_icon="📈",
    layout="wide"
)

# Constants
API_URL = os.environ.get('API_URL', 'http://localhost:5001/api/stock/analyze')

# UI language options
LANGUAGES = {
    "English": {
        "title": "🤖 AI Stock Analyst",
        "subtitle": "Get AI-powered investment recommendations based on real-time news",
        "enter_ticker": "Enter Stock Ticker (e.g., AAPL, TSLA, MSFT)",
        "analyze_button": "Analyze",
        "please_enter": "Please enter a stock ticker.",
        "analyzing": "Analyzing {}... Please wait.",
        "api_error": "API Error: {}",
        "connection_error": "Cannot connect to API server: {}",
        "mock_data_warning": "⚠️ Using mock data because API server is not available. Please make sure the API server is running.",
        "sector": "Sector:",
        "industry": "Industry:",
        "country": "Country:",
        "employees": "Employees:",
        "website": "Website:",
        "current_price": "Current Price",
        "price_change": "Price Change (30d)",
        "sentiment": "Sentiment",
        "company_description": "Company Description",
        "price_trend": "Price Trend (Last 30 Days)",
        "ai_analysis": "AI Analysis",
        "recommendation": "Recommendation:",
        "summary": "Summary",
        "reasoning": "Reasoning",
        "recent_news": "Recent News",
        "no_news": "No recent news articles found for this company.",
        "read_more": "Read more",
        "how_it_works": "How it works",
        "step1": "1. Enter a stock ticker symbol (e.g., AAPL for Apple Inc.)",
        "step2": "2. Our system fetches the latest news about the company",
        "step3": "3. AI analyzes the news sentiment and market trends",
        "step4": "4. You receive a clear investment recommendation: Buy, Hold, or Sell",
        "powered_by": "Powered by AI models and real-time market data from multiple sources",
        "disclaimer": "Disclaimer: This tool provides analysis for informational purposes only. It is not intended as financial advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.",
        "footer": "© 2023 AI Stock Analyst | Built with Streamlit and Flask"
    },
    "Hebrew": {
        "title": "🤖 אנליסט מניות AI",
        "subtitle": "קבל המלצות השקעה מבוססות AI על סמך חדשות בזמן אמת",
        "enter_ticker": "הזן סימול מניה (לדוגמה: AAPL, TSLA, MSFT)",
        "analyze_button": "נתח",
        "please_enter": "אנא הזן סימול מניה.",
        "analyzing": "מנתח את {}... אנא המתן.",
        "api_error": "שגיאת API: {}",
        "connection_error": "לא ניתן להתחבר לשרת ה-API: {}",
        "mock_data_warning": "⚠️ משתמש בנתונים לדוגמה כי שרת ה-API אינו זמין. אנא ודא ששרת ה-API פועל.",
        "sector": "סקטור:",
        "industry": "תעשייה:",
        "country": "מדינה:",
        "employees": "עובדים:",
        "website": "אתר אינטרנט:",
        "current_price": "מחיר נוכחי",
        "price_change": "שינוי מחיר (30 ימים)",
        "sentiment": "סנטימנט",
        "company_description": "תיאור החברה",
        "price_trend": "מגמת מחיר (30 ימים אחרונים)",
        "ai_analysis": "ניתוח AI",
        "recommendation": "המלצה:",
        "summary": "סיכום",
        "reasoning": "נימוק",
        "recent_news": "חדשות אחרונות",
        "no_news": "לא נמצאו חדשות אחרונות עבור חברה זו.",
        "read_more": "קרא עוד",
        "how_it_works": "איך זה עובד",
        "step1": "1. הזן סימול מניה (לדוגמה: AAPL עבור Apple Inc.)",
        "step2": "2. המערכת מביאה את החדשות העדכניות ביותר על החברה",
        "step3": "3. AI מנתח את הסנטימנט של החדשות ואת מגמות השוק",
        "step4": "4. אתה מקבל המלצת השקעה ברורה: קנה, החזק או מכור",
        "powered_by": "מופעל על ידי מודלים של AI ונתוני שוק בזמן אמת ממקורות מרובים",
        "disclaimer": "הצהרה: כלי זה מספק ניתוח למטרות מידע בלבד. הוא אינו מיועד כייעוץ פיננסי. תמיד בצע מחקר עצמאי והתייעץ עם יועץ פיננסי מוסמך לפני קבלת החלטות השקעה.",
        "footer": "© 2023 אנליסט מניות AI | נבנה עם Streamlit ו-Flask"
    }
}

# Function to generate mock data when API is not available
def generate_mock_data(ticker):
    """Generate mock data when API is not available."""
    
    # Create mock price data
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30, freq='D')
    base_price = random.uniform(100, 200)
    closes = [base_price + (i * 0.2) + random.uniform(-5, 5) for i in range(len(dates))]
    
    price_data = [{'date': d.strftime('%Y-%m-%d'), 'close': c} for d, c in zip(dates, closes)]
    
    # Calculate simple metrics
    current_price = closes[-1]
    price_change = closes[-1] - closes[0]
    price_change_pct = (price_change / closes[0]) * 100
    
    # Generate mock analysis
    sentiments = ["Positive", "Neutral", "Negative"]
    recommendations = ["Buy", "Hold", "Sell"]
    
    sentiment = random.choice(sentiments)
    if sentiment == "Positive":
        recommendation = "Buy"
        reasoning = "Recent news suggests positive developments for the company."
    elif sentiment == "Negative":
        recommendation = "Sell"
        reasoning = "Recent news indicates challenges that may affect company performance."
    else:
        recommendation = "Hold"
        reasoning = "Mixed or neutral news coverage does not suggest a change in position."
    
    # Create mock company info
    company_info = {
        'name': f"{ticker} Inc.",
        'sector': random.choice(['Technology', 'Healthcare', 'Finance', 'Consumer Goods', 'Energy']),
        'industry': random.choice(['Software', 'Hardware', 'Pharmaceuticals', 'Banking', 'Retail', 'Oil & Gas']),
        'website': f"https://www.{ticker.lower()}.com",
        'description': f"This is a demo description for {ticker}. The API server appears to be offline, so we're showing mock data.",
        'country': random.choice(['USA', 'Canada', 'UK', 'Germany', 'Japan']),
        'employees': random.randint(1000, 100000)
    }
    
    # Create mock news
    news = []
    headlines = [
        f"{ticker} Reports Strong Quarterly Results",
        f"{ticker} Announces New Product Launch",
        f"Analysts Upgrade {ticker} Stock Rating"
    ]
    
    for i, headline in enumerate(headlines):
        news.append({
            'title': headline,
            'description': f"This is mock news article {i+1} about {ticker}. The API server appears to be offline.",
            'source': {'name': random.choice(['Financial Times', 'Bloomberg', 'CNBC'])},
            'url': "#",
            'publishedAt': (pd.Timestamp.now() - pd.Timedelta(days=i)).strftime('%Y-%m-%d')
        })
    
    # Assemble complete response
    return {
        'ticker': ticker,
        'company_name': company_info['name'],
        'current_price': current_price,
        'price_change': price_change,
        'price_change_pct': price_change_pct,
        'analysis': {
            'sentiment': sentiment,
            'recommendation': recommendation,
            'reasoning': reasoning,
            'summary': f"This is mock data for {ticker} since the API server is not available."
        },
        'company_info': company_info,
        'news': news,
        'price_data': price_data
    }

# Sidebar for settings
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/economic-growth.png", width=80)
    language = st.selectbox("Language / שפה", options=list(LANGUAGES.keys()))
    
    # Get translation dictionary based on selected language
    t = LANGUAGES[language]
    
    # Show current time in sidebar
    st.write(f"**{datetime.now().strftime('%Y-%m-%d %H:%M')}**")
    
    # Quick links to popular stocks
    st.subheader("Popular Stocks")
    popular_stocks = {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "GOOGL": "Google",
        "AMZN": "Amazon",
        "TSLA": "Tesla"
    }
    
    # Create buttons for popular stocks
    col1, col2 = st.columns(2)
    for i, (ticker, name) in enumerate(popular_stocks.items()):
        if i % 2 == 0:
            if col1.button(f"{ticker} - {name}"):
                st.session_state.ticker = ticker
                st.session_state.submitted = True
        else:
            if col2.button(f"{ticker} - {name}"):
                st.session_state.ticker = ticker
                st.session_state.submitted = True

# Page title
st.title(t["title"])
st.markdown(f"### {t['subtitle']}")

# Initialize session state for ticker and submission
if "ticker" not in st.session_state:
    st.session_state.ticker = ""
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Input form for ticker
with st.form("stock_form"):
    ticker = st.text_input(t["enter_ticker"], value=st.session_state.ticker)
    submitted = st.form_submit_button(t["analyze_button"], use_container_width=True)
    
    if submitted:
        st.session_state.ticker = ticker
        st.session_state.submitted = True

# Process form submission
if st.session_state.submitted and st.session_state.ticker:
    ticker = st.session_state.ticker.upper()
    
    with st.spinner(t["analyzing"].format(ticker)):
        try:
            # Try to call the API
            response = requests.post(
                API_URL,
                json={"ticker": ticker},
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
            else:
                st.error(t["api_error"].format(response.json().get('error', 'Unknown error')))
                data = generate_mock_data(ticker)
                st.warning(t["mock_data_warning"])
        
        except requests.exceptions.RequestException as e:
            st.error(t["connection_error"].format(str(e)))
            data = generate_mock_data(ticker)
            st.warning(t["mock_data_warning"])
        
        try:
            # Display results in nice card-like containers
            if 'price_change_pct' in data and data['price_change_pct'] is not None:
                # Top section with company name and current status
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h2>{data['company_name']} ({data['ticker']})</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Main content
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Company information
                    if 'company_info' in data:
                        company_info = data['company_info']
                        
                        # Create card-like container
                        st.markdown("""
                        <style>
                        .info-card {
                            background-color: white;
                            border-radius: 10px;
                            padding: 20px;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                            margin-bottom: 20px;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        with st.container():
                            st.markdown('<div class="info-card">', unsafe_allow_html=True)
                            info_cols = st.columns(2)
                            with info_cols[0]:
                                st.write(f"**{t['sector']}** {company_info.get('sector', 'N/A')}")
                                st.write(f"**{t['industry']}** {company_info.get('industry', 'N/A')}")
                                st.write(f"**{t['country']}** {company_info.get('country', 'N/A')}")
                            with info_cols[1]:
                                st.write(f"**{t['employees']}** {company_info.get('employees', 0):,}" if company_info.get('employees', 0) else f"**{t['employees']}** N/A")
                                if company_info.get('website'):
                                    st.write(f"**{t['website']}** [{company_info.get('website').replace('https://', '')}]({company_info.get('website')})")
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Price metrics
                    with st.container():
                        st.markdown('<div class="info-card">', unsafe_allow_html=True)
                        price_col1, price_col2, price_col3 = st.columns(3)
                        
                        price_col1.metric(t["current_price"], f"${data['current_price']:.2f}")
                        
                        change_value = f"{data['price_change']:.2f}"
                        change_pct = f"{data['price_change_pct']:.2f}%"
                        delta_value = f"{change_value} ({change_pct})"
                        delta_color = "normal" if data['price_change'] == 0 else ("inverse" if data['price_change'] < 0 else "normal")
                        
                        price_col2.metric(t["price_change"], delta_value, delta_color=delta_color)
                        
                        # Use different colors for sentiment
                        sentiment = data['analysis']['sentiment']
                        sentiment_color = "green" if sentiment == "Positive" else ("red" if sentiment == "Negative" else "orange")
                        price_col3.markdown(f"<h4>{t['sentiment']}</h4>", unsafe_allow_html=True)
                        price_col3.markdown(f"<h3 style='color:{sentiment_color}'>{sentiment}</h3>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Company description (if available)
                    if 'company_info' in data and data['company_info'].get('description'):
                        with st.expander(t["company_description"]):
                            st.write(data['company_info']['description'])
                    
                    # Price trend chart using Plotly for better interactivity
                    st.subheader(t["price_trend"])
                    
                    # Convert price data to DataFrame for plotting
                    price_df = pd.DataFrame(data['price_data'])
                    price_df['date'] = pd.to_datetime(price_df['date'])
                    
                    # Create plotly chart
                    fig = go.Figure()
                    color = 'green' if data['price_change'] >= 0 else 'red'
                    
                    fig.add_trace(go.Scatter(
                        x=price_df['date'],
                        y=price_df['close'],
                        mode='lines',
                        line=dict(color=color, width=2),
                        name='Price'
                    ))
                    
                    fig.update_layout(
                        title='',
                        xaxis_title='Date',
                        yaxis_title='Price ($)',
                        hovermode='x unified',
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0),
                        template='plotly_white',
                        xaxis=dict(
                            showgrid=True,
                            gridcolor='lightgray',
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridcolor='lightgray',
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # AI Analysis results in a card
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.subheader(t["ai_analysis"])
                    
                    # Recommendation
                    rec = data['analysis']['recommendation']
                    rec_color = "green" if rec == "Buy" else ("red" if rec == "Sell" else "orange")
                    st.markdown(f"### {t['recommendation']} <span style='color:{rec_color}'>{rec}</span>", unsafe_allow_html=True)
                    
                    # Summary
                    st.markdown(f"#### {t['summary']}")
                    st.write(data['analysis']['summary'])
                    
                    # Reasoning
                    st.markdown(f"#### {t['reasoning']}")
                    st.write(data['analysis']['reasoning'])
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # News articles in a card
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.subheader(t["recent_news"])
                    
                    if not data['news']:
                        st.info(t["no_news"])
                    
                    for article in data['news']:
                        st.markdown(f"**{article['title']}**")
                        published_date = article.get('publishedAt', '')[:10] if article.get('publishedAt') else ''
                        source_name = article.get('source', {}).get('name', '') if article.get('source') else ''
                        
                        if published_date or source_name:
                            st.markdown(f"*{published_date}*{' - ' + source_name if source_name else ''}")
                        
                        st.markdown(f"{article.get('description', '')}")
                        
                        if article.get('url'):
                            st.markdown(f"[{t['read_more']}]({article['url']})")
                        
                        st.markdown("---")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Invalid data received from API")
                st.write("Raw API response:", data)
        except Exception as e:
            st.error(f"Error displaying data: {str(e)}")
            st.write("Raw API response:", data)
elif st.session_state.submitted:
    st.warning(t["please_enter"])
else:
    # Display placeholder content
    st.markdown(f"""
    ## {t["how_it_works"]}
    
    {t["step1"]}
    {t["step2"]}
    {t["step3"]}
    {t["step4"]}
    
    *{t["powered_by"]}*
    """)
    
    # Disclaimer
    st.info(t["disclaimer"])

# Footer
st.markdown("---")
st.markdown(t["footer"])

# Custom CSS to improve the look and feel
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3, h4 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stMetric {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 5px;
    }
    .stSidebar {
        background-color: #f8f9fa;
    }
    button {
        border-radius: 5px !important;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
    }
    .stButton>button:hover {
        background-color: #0069d9;
        color: white;
    }
</style>
""", unsafe_allow_html=True) 