"""
Data sources management module for AI Stock Analyst.
Provides a unified interface to multiple financial data providers.
"""

import os
import json
import requests
import random
import time
import pandas as pd
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class DataSource(ABC):
    """Abstract base class for all data sources."""
    
    @abstractmethod
    def get_stock_data(self, ticker, period="1mo"):
        """Get historical stock price data."""
        pass
    
    @abstractmethod
    def get_company_info(self, ticker):
        """Get company information."""
        pass
    
    @abstractmethod
    def get_news(self, ticker, days=7):
        """Get news articles related to the ticker."""
        pass


class YahooFinanceSource(DataSource):
    """Yahoo Finance data source."""
    
    def __init__(self):
        """Initialize Yahoo Finance data source."""
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
        ]
        
        # Common company names to avoid API calls
        self.common_companies = {
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation',
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com, Inc.',
            'META': 'Meta Platforms, Inc.',
            'TSLA': 'Tesla, Inc.',
            'NVDA': 'NVIDIA Corporation',
            'NFLX': 'Netflix, Inc.',
            'JPM': 'JPMorgan Chase & Co.',
            'V': 'Visa Inc.'
        }
    
    def _get_random_user_agent(self):
        """Get a random user agent to avoid rate limiting."""
        return random.choice(self.user_agents)
    
    def get_stock_data(self, ticker, period="1mo"):
        """Get stock data using Yahoo Finance."""
        # Introduce random delay to avoid rate limiting
        time.sleep(random.uniform(0.5, 2))
        
        try:
            # Try direct download method
            import yfinance as yf
            data = yf.download(ticker, period=period, progress=False, timeout=15)
            if not data.empty and len(data) > 5:
                return data
        except Exception as e:
            print(f"Yahoo Finance direct download failed: {str(e)}")
        
        try:
            # Try direct API request with custom headers
            now = datetime.now()
            if period == "1mo":
                start = now - timedelta(days=30)
            elif period == "3mo":
                start = now - timedelta(days=90)
            else:
                start = now - timedelta(days=30)
                
            period1 = int(start.timestamp())
            period2 = int(now.timestamp())
            
            url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval=1d&events=history"
            
            headers = {'User-Agent': self._get_random_user_agent()}
            
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                from io import StringIO
                data = pd.read_csv(StringIO(response.text), parse_dates=['Date'])
                data.set_index('Date', inplace=True)
                return data
        except Exception as e:
            print(f"Yahoo Finance API request failed: {str(e)}")
        
        return pd.DataFrame()
    
    def get_company_info(self, ticker):
        """Get company information."""
        # Check if ticker is in common companies list
        if ticker in self.common_companies:
            return {
                'name': self.common_companies[ticker],
                'sector': 'Unknown',
                'industry': 'Unknown',
                'website': '',
                'description': '',
                'country': '',
                'employees': 0
            }
        
        # Try to get from Yahoo Finance
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'name': info.get('longName', ticker),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'website': info.get('website', ''),
                'description': info.get('longBusinessSummary', ''),
                'country': info.get('country', ''),
                'employees': info.get('fullTimeEmployees', 0)
            }
        except Exception as e:
            print(f"Failed to get company info for {ticker}: {str(e)}")
            
            # Return default info
            return {
                'name': ticker,
                'sector': 'Unknown',
                'industry': 'Unknown',
                'website': '',
                'description': '',
                'country': '',
                'employees': 0
            }
    
    def get_news(self, ticker, days=7):
        """Get news related to ticker (Yahoo Finance doesn't have this)."""
        return []


class AlphaVantageSource(DataSource):
    """Alpha Vantage data source."""
    
    def __init__(self, api_key=None):
        """Initialize Alpha Vantage data source."""
        self.api_key = api_key or os.environ.get('ALPHA_VANTAGE_API_KEY', '')
    
    def get_stock_data(self, ticker, period="1mo"):
        """Get stock data using Alpha Vantage."""
        if not self.api_key:
            return pd.DataFrame()
        
        try:
            # Map period to Alpha Vantage output size
            output_size = "full" if period != "1mo" else "compact"
            
            # API endpoint for daily time series
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize={output_size}&apikey={self.api_key}"
            
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                # Check if we got valid data
                if "Time Series (Daily)" not in data:
                    print(f"Alpha Vantage API error: {data.get('Error Message', 'Unknown error')}")
                    return pd.DataFrame()
                
                # Convert to DataFrame
                time_series = data["Time Series (Daily)"]
                df = pd.DataFrame.from_dict(time_series, orient='index')
                
                # Rename columns to match Yahoo Finance format
                df.index = pd.DatetimeIndex(df.index)
                df.columns = [col.split('. ')[1].capitalize() for col in df.columns]
                
                # Filter to requested period
                if period == "1mo":
                    df = df.iloc[:30]
                elif period == "3mo":
                    df = df.iloc[:90]
                
                # Convert columns to numeric
                for col in df.columns:
                    df[col] = pd.to_numeric(df[col])
                
                return df
        except Exception as e:
            print(f"Alpha Vantage API request failed: {str(e)}")
        
        return pd.DataFrame()
    
    def get_company_info(self, ticker):
        """Get company information from Alpha Vantage."""
        if not self.api_key:
            return {
                'name': ticker,
                'sector': 'Unknown',
                'industry': 'Unknown',
                'website': '',
                'description': '',
                'country': '',
                'employees': 0
            }
        
        try:
            # API endpoint for company overview
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={self.api_key}"
            
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                # Check if we got valid data
                if not data or "Symbol" not in data:
                    return {
                        'name': ticker,
                        'sector': 'Unknown',
                        'industry': 'Unknown',
                        'website': '',
                        'description': '',
                        'country': '',
                        'employees': 0
                    }
                
                return {
                    'name': data.get('Name', ticker),
                    'sector': data.get('Sector', 'Unknown'),
                    'industry': data.get('Industry', 'Unknown'),
                    'website': '',  # Not provided by Alpha Vantage
                    'description': data.get('Description', ''),
                    'country': data.get('Country', ''),
                    'employees': int(data.get('FullTimeEmployees', 0)) if data.get('FullTimeEmployees', '').isdigit() else 0
                }
        except Exception as e:
            print(f"Alpha Vantage company info request failed: {str(e)}")
        
        return {
            'name': ticker,
            'sector': 'Unknown',
            'industry': 'Unknown',
            'website': '',
            'description': '',
            'country': '',
            'employees': 0
        }
    
    def get_news(self, ticker, days=7):
        """Get news related to ticker (Alpha Vantage doesn't have this)."""
        return []


class MockDataSource(DataSource):
    """Mock data source for demo/fallback."""
    
    def get_stock_data(self, ticker, period="1mo"):
        """Generate mock stock data."""
        print(f"Creating demo data for {ticker}")
        
        # Create a date range for the last 30, 60, or 90 days based on period
        end_date = datetime.now()
        if period == "1mo":
            days_back = 30
        elif period == "3mo":
            days_back = 90
        else:
            days_back = 30
            
        start_date = end_date - timedelta(days=days_back)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate random prices around $150 with a slight trend
        base_price = 150.0
        # Create price that trends slightly upward
        closes = [base_price + (i * 0.5) + random.uniform(-5, 5) for i in range(len(dates))]
        
        # Create dataframe
        data = pd.DataFrame({
            'Open': closes,
            'High': [price + random.uniform(0, 2) for price in closes],
            'Low': [price - random.uniform(0, 2) for price in closes],
            'Close': closes,
            'Volume': [int(random.uniform(5000000, 15000000)) for _ in range(len(dates))]
        }, index=dates)
        
        return data
    
    def get_company_info(self, ticker):
        """Generate mock company info."""
        return {
            'name': f"{ticker} Corporation",
            'sector': random.choice(['Technology', 'Healthcare', 'Finance', 'Consumer Goods', 'Energy']),
            'industry': random.choice(['Software', 'Hardware', 'Pharmaceuticals', 'Banking', 'Retail', 'Oil & Gas']),
            'website': f"https://www.{ticker.lower()}.com",
            'description': f"This is a demo description for {ticker}. No actual company data is available.",
            'country': random.choice(['USA', 'Canada', 'UK', 'Germany', 'Japan']),
            'employees': random.randint(1000, 100000)
        }
    
    def get_news(self, ticker, days=7):
        """Generate mock news articles."""
        # Create random dates
        dates = [(datetime.now() - timedelta(days=random.randint(0, days))).strftime("%Y-%m-%d") 
                for _ in range(3)]
        
        # Sample headlines
        headlines = [
            f"{ticker} Reports Strong Quarterly Results",
            f"{ticker} Announces New Product Launch",
            f"Analysts Upgrade {ticker} Stock Rating",
            f"{ticker} Expands into New Markets",
            f"CEO of {ticker} Discusses Future Growth",
            f"{ticker} Partners with Industry Leader",
            f"Investors React to {ticker}'s Latest Announcement"
        ]
        
        # Generate mock news
        mock_news = []
        for i in range(min(5, len(headlines))):
            mock_news.append({
                'title': headlines[i],
                'description': f"This is a sample news article about {ticker}. No actual news data is available.",
                'source': {'name': random.choice(['Financial Times', 'Bloomberg', 'CNBC', 'Reuters', 'Wall Street Journal'])},
                'url': f"https://example.com/news/{ticker.lower()}/{i}",
                'publishedAt': dates[i % len(dates)]
            })
        
        return mock_news


class FinancialDataManager:
    """Manager class to coordinate multiple data sources."""
    
    def __init__(self, news_api_key=None, alpha_vantage_api_key=None):
        """Initialize with data sources in priority order."""
        self.data_sources = [
            YahooFinanceSource(),
            AlphaVantageSource(api_key=alpha_vantage_api_key),
            MockDataSource()  # Fallback source
        ]
        
        # For news-specific APIs
        self.news_api_key = news_api_key
    
    def get_stock_data(self, ticker, period="1mo"):
        """Get stock data from available sources."""
        # Try each data source in order until we get data
        for source in self.data_sources:
            data = source.get_stock_data(ticker, period)
            if not data.empty and len(data) > 5:
                return data
        
        # If all sources fail, return empty DataFrame
        return pd.DataFrame()
    
    def get_company_info(self, ticker):
        """Get company information from available sources."""
        # Try each data source in order until we get data
        for source in self.data_sources:
            info = source.get_company_info(ticker)
            if info and info['name'] != ticker:
                return info
        
        # If all sources fail, get from mock source
        return self.data_sources[-1].get_company_info(ticker)
    
    def get_news(self, ticker, company_name=None, days=7):
        """Get news articles related to the ticker."""
        try:
            # First try NewsAPI if available
            if self.news_api_key:
                from newsapi import NewsApiClient
                news_api = NewsApiClient(api_key=self.news_api_key)
                
                # Use company name if provided, otherwise use ticker
                query = company_name if company_name else ticker
                
                # Calculate the date range for news
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
                
                # Format dates for NewsAPI
                from_date = start_date.strftime('%Y-%m-%d')
                to_date = end_date.strftime('%Y-%m-%d')
                
                # Fetch news articles
                news = news_api.get_everything(
                    q=query,
                    from_param=from_date,
                    to=to_date,
                    language='en',
                    sort_by='relevancy',
                    page_size=10
                )
                
                if news['totalResults'] > 0:
                    return news['articles']
                
                # If no results for company name, try ticker
                if company_name and query != ticker:
                    news = news_api.get_everything(
                        q=ticker,
                        from_param=from_date,
                        to=to_date,
                        language='en',
                        sort_by='relevancy',
                        page_size=10
                    )
                    
                    if news['totalResults'] > 0:
                        return news['articles']
        except Exception as e:
            print(f"NewsAPI request failed: {str(e)}")
        
        # Try other data sources
        for source in self.data_sources:
            news = source.get_news(ticker, days)
            if news:
                return news
        
        # If all sources fail, return mock news
        return self.data_sources[-1].get_news(ticker, days) 