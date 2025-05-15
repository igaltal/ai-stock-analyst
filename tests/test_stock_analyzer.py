import unittest
import os
import sys
import pandas as pd
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.stock_analyzer import StockAnalyzer


class TestStockAnalyzer(unittest.TestCase):
    
    def setUp(self):
        # Use dummy API keys for testing
        self.analyzer = StockAnalyzer(
            news_api_key='test_news_api_key',
            openai_api_key='test_openai_api_key'
        )
    
    def test_demo_data_generation(self):
        """Test that demo data is generated correctly."""
        data = self.analyzer._create_demo_data('TEST')
        
        # Check that the data has the correct structure
        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(len(data), 25)  # Should have at least 25 days of data
        self.assertIn('Open', data.columns)
        self.assertIn('High', data.columns)
        self.assertIn('Low', data.columns)
        self.assertIn('Close', data.columns)
        self.assertIn('Volume', data.columns)
    
    def test_mock_ai_analysis(self):
        """Test the mock AI analysis functionality."""
        # Create test news data
        test_news = [
            {
                'title': 'Company XYZ reports record growth in Q2',
                'description': 'Positive news about growth'
            },
            {
                'title': 'Profits up 20% for XYZ',
                'description': 'More good news'
            }
        ]
        
        # Run mock analysis
        analysis = self.analyzer._mock_ai_analysis(test_news)
        
        # Check analysis structure
        self.assertIn('summary', analysis)
        self.assertIn('sentiment', analysis)
        self.assertIn('recommendation', analysis)
        self.assertIn('reasoning', analysis)
        
        # With positive news, should recommend "Buy"
        self.assertEqual(analysis['sentiment'], 'Positive')
        self.assertEqual(analysis['recommendation'], 'Buy')
        
        # Try with negative news
        negative_news = [
            {
                'title': 'Company XYZ reports declining sales',
                'description': 'Bad news about decline'
            },
            {
                'title': 'Losses mount for XYZ as competition increases',
                'description': 'More bad news'
            }
        ]
        
        analysis = self.analyzer._mock_ai_analysis(negative_news)
        self.assertEqual(analysis['sentiment'], 'Negative')
        self.assertEqual(analysis['recommendation'], 'Sell')
    
    def test_get_company_name(self):
        """Test the company name lookup from the hardcoded list."""
        # Test a known company
        company_name = self.analyzer.get_company_name('AAPL')
        self.assertEqual(company_name, 'Apple Inc.')
        
        # Test an unknown company (should return ticker)
        company_name = self.analyzer.get_company_name('UNKNOWN')
        self.assertEqual(company_name, 'UNKNOWN')


if __name__ == '__main__':
    unittest.main() 