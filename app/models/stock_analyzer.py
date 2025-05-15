import pandas as pd
import numpy as np
import openai
from datetime import datetime, timedelta
import json
import random
from app.models.data_sources import FinancialDataManager

class StockAnalyzer:
    """Class for analyzing stocks using AI and news data."""
    
    def __init__(self, news_api_key, openai_api_key, alpha_vantage_api_key=None):
        """Initialize with required API keys."""
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        
        # Initialize the data manager with all available API keys
        self.data_manager = FinancialDataManager(
            news_api_key=news_api_key,
            alpha_vantage_api_key=alpha_vantage_api_key
        )
    
    def fetch_stock_data(self, ticker, period="1mo"):
        """Fetch historical stock data using multiple sources."""
        return self.data_manager.get_stock_data(ticker, period)
    
    def fetch_news(self, ticker, company_name=None, days=7):
        """Fetch news articles related to the stock."""
        return self.data_manager.get_news(ticker, company_name, days)
    
    def analyze_sentiment_with_ai(self, news_articles):
        """Use OpenAI to analyze news sentiment and provide investment recommendation."""
        if not news_articles:
            return {
                "summary": "No recent news articles found.",
                "sentiment": "Neutral",
                "recommendation": "Hold",
                "reasoning": "Insufficient news data to make a recommendation."
            }
        
        # Check if OpenAI API key is available
        if not self.openai_api_key or self.openai_api_key == "your_openai_api_key_here":
            # Return mock analysis if no API key
            return self._mock_ai_analysis(news_articles)
        
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
            print(f"AI analysis failed: {str(e)}")
            # Return mock analysis if API fails
            return self._mock_ai_analysis(news_articles)
    
    def _mock_ai_analysis(self, news_articles):
        """Generate mock AI analysis when OpenAI API is not available."""
        # Extract sentiment from article titles for basic analysis
        positive_words = ['rise', 'gain', 'growth', 'profit', 'success', 'positive', 'up', 'high', 'record']
        negative_words = ['fall', 'drop', 'decline', 'loss', 'risk', 'negative', 'down', 'low', 'concern', 'worry']
        
        positive_count = 0
        negative_count = 0
        
        for article in news_articles[:5]:
            title = article['title'].lower()
            for word in positive_words:
                if word in title:
                    positive_count += 1
            for word in negative_words:
                if word in title:
                    negative_count += 1
        
        # Determine sentiment based on word count
        if positive_count > negative_count:
            sentiment = "Positive"
            recommendation = "Buy"
            reasoning = "Recent news suggests positive developments for the company."
        elif negative_count > positive_count:
            sentiment = "Negative"
            recommendation = "Sell"
            reasoning = "Recent news indicates challenges that may affect company performance."
        else:
            sentiment = "Neutral"
            recommendation = "Hold"
            reasoning = "Mixed or neutral news coverage does not suggest a change in position."
        
        # Create summary from first article if available
        if news_articles:
            summary = f"Recent news includes: {news_articles[0]['title']}."
            if len(news_articles) > 1:
                summary += f" Also: {news_articles[1]['title']}."
        else:
            summary = "Limited recent news available for analysis."
        
        return {
            "summary": summary,
            "sentiment": sentiment,
            "recommendation": recommendation,
            "reasoning": reasoning
        }
    
    def get_company_name(self, ticker):
        """Get the company name for a given ticker."""
        company_info = self.data_manager.get_company_info(ticker)
        return company_info['name']
    
    def get_company_info(self, ticker):
        """Get detailed company information."""
        return self.data_manager.get_company_info(ticker)
    
    def analyze(self, ticker):
        """Perform complete analysis on a stock ticker."""
        ticker = ticker.upper()
        
        # Get company information
        company_info = self.get_company_info(ticker)
        company_name = company_info['name']
        
        # Fetch news articles
        news_articles = self.fetch_news(ticker, company_name)
        
        # Fetch stock data
        stock_data = self.fetch_stock_data(ticker)
        
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
            'company_info': company_info,  # Add complete company info
            'news': news_articles[:5],  # Return top 5 news articles
            'price_data': price_data
        }
        
        return result 