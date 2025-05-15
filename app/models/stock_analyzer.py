import yfinance as yf
import pandas as pd
import numpy as np
from newsapi import NewsApiClient
import openai
from datetime import datetime, timedelta
import json

class StockAnalyzer:
    """Class for analyzing stocks using AI and news data."""
    
    def __init__(self, news_api_key, openai_api_key):
        """Initialize with required API keys."""
        self.news_api = NewsApiClient(api_key=news_api_key)
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        
    def fetch_stock_data(self, ticker, period="1mo"):
        """Fetch historical stock data."""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            if data.empty:
                raise ValueError(f"No data found for ticker {ticker}")
            return data
        except Exception as e:
            raise Exception(f"Failed to fetch stock data for {ticker}: {str(e)}")
    
    def fetch_news(self, ticker, company_name=None, days=7):
        """Fetch news articles related to the stock."""
        try:
            # Use company name if provided, otherwise use ticker
            query = company_name if company_name else ticker
            
            # Calculate the date range for news
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Format dates for NewsAPI
            from_date = start_date.strftime('%Y-%m-%d')
            to_date = end_date.strftime('%Y-%m-%d')
            
            # Fetch news articles
            news = self.news_api.get_everything(
                q=query,
                from_param=from_date,
                to=to_date,
                language='en',
                sort_by='relevancy',
                page_size=10
            )
            
            if news['totalResults'] == 0:
                # If no results for company name, try ticker
                if company_name:
                    return self.fetch_news(ticker, None, days)
                else:
                    return []
            
            return news['articles']
        except Exception as e:
            raise Exception(f"Failed to fetch news for {ticker}: {str(e)}")
    
    def analyze_sentiment_with_ai(self, news_articles):
        """Use OpenAI to analyze news sentiment and provide investment recommendation."""
        if not news_articles:
            return {
                "summary": "No recent news articles found.",
                "sentiment": "Neutral",
                "recommendation": "Hold",
                "reasoning": "Insufficient news data to make a recommendation."
            }
        
        # Prepare news articles for analysis
        news_text = []
        for article in news_articles[:5]:  # Use top 5 most relevant articles
            news_text.append(f"Title: {article['title']}\nDescription: {article['description']}")
        
        news_content = "\n\n".join(news_text)
        
        # Create prompt for OpenAI
        prompt = f"""
        Based on the following news articles about a company, please provide:
        1. A concise summary of the key points (3-4 sentences)
        2. An analysis of the overall sentiment (Positive, Neutral, or Negative)
        3. An investment recommendation (Buy, Hold, or Sell)
        4. Brief reasoning for the recommendation
        
        News articles:
        {news_content}
        
        Format your response as a JSON object with the following structure:
        {{
            "summary": "your summary here",
            "sentiment": "Positive/Neutral/Negative",
            "recommendation": "Buy/Hold/Sell",
            "reasoning": "brief reasoning"
        }}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst providing investment insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )
            
            # Extract and parse the JSON response
            ai_analysis = response.choices[0].message['content'].strip()
            
            # Extract only the JSON part
            start_idx = ai_analysis.find('{')
            end_idx = ai_analysis.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = ai_analysis[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise ValueError("Failed to extract valid JSON from AI response")
                
        except Exception as e:
            raise Exception(f"AI analysis failed: {str(e)}")
    
    def get_company_name(self, ticker):
        """Get the company name for a given ticker."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return info.get('longName', ticker)
        except:
            return ticker
    
    def analyze(self, ticker):
        """Perform complete analysis on a stock ticker."""
        # Fetch stock data
        stock_data = self.fetch_stock_data(ticker)
        
        # Get company name
        company_name = self.get_company_name(ticker)
        
        # Fetch news articles
        news_articles = self.fetch_news(ticker, company_name)
        
        # Analyze news with AI
        ai_analysis = self.analyze_sentiment_with_ai(news_articles)
        
        # Prepare stock price data for chart
        price_data = []
        for date, row in stock_data.iterrows():
            price_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'close': row['Close']
            })
        
        # Calculate simple metrics
        if len(stock_data) > 0:
            current_price = stock_data['Close'].iloc[-1]
            price_change = stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]
            price_change_pct = (price_change / stock_data['Close'].iloc[0]) * 100
        else:
            current_price = None
            price_change = None
            price_change_pct = None
        
        # Combine all data and return
        result = {
            'ticker': ticker,
            'company_name': company_name,
            'current_price': current_price,
            'price_change': price_change,
            'price_change_pct': price_change_pct,
            'analysis': ai_analysis,
            'news': news_articles[:5],  # Return top 5 news articles
            'price_data': price_data
        }
        
        return result 