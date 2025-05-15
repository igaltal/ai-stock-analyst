# AI Stock Analyst

A comprehensive financial analysis platform that leverages artificial intelligence to provide investment recommendations based on real-time news, market data, and technical analysis.

## Overview

AI Stock Analyst is an advanced financial tool designed to assist investors in making data-driven decisions. The platform combines multiple data sources, natural language processing, and machine learning techniques to analyze stock performance, news sentiment, and market trends. This system reduces the need for extensive manual research by automating the collection and interpretation of financial data.

## Key Features

- **Multi-Source Data Integration**: Fetches financial data from multiple providers (Yahoo Finance, Alpha Vantage) with automatic fallback mechanisms
- **News Sentiment Analysis**: Processes recent news articles using AI to determine market sentiment
- **Investment Recommendations**: Generates actionable "Buy," "Hold," or "Sell" recommendations with supporting rationale
- **Interactive Data Visualization**: Displays dynamic charts and metrics for comprehensive market analysis
- **Company Profile Analysis**: Provides detailed company information including sector, industry, employees, and business description
- **Multilingual Support**: Full interface available in both English and Hebrew
- **Responsive Design**: Adapts to different screen sizes and device types
- **Fault-Tolerant Architecture**: Gracefully handles API failures and rate limiting with fallback mechanisms

## Technologies Used

### Languages
- **Python**: Primary backend and data processing language
- **JavaScript/HTML/CSS**: Frontend styling via Streamlit and custom components

### Frameworks & Libraries
- **Flask**: Backend API server with RESTful architecture
- **Streamlit**: Interactive frontend user interface
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **Matplotlib**: Static chart generation
- **NumPy**: Numerical computing for financial calculations
- **Requests**: HTTP networking for API integrations

### AI & Machine Learning
- **OpenAI GPT-3.5**: Natural language processing for news sentiment analysis
- **Custom Analysis Algorithms**: Proprietary algorithms for financial data interpretation

### Data Sources
- **Yahoo Finance API**: Real-time and historical stock price data
- **Alpha Vantage API**: Comprehensive financial data and company information
- **NewsAPI**: Current news articles relevant to target companies
- **Mock Data Generator**: Fallback data generation when APIs are unavailable

### DevOps & Infrastructure
- **Git**: Version control and code management
- **Virtual Environment**: Isolated Python environment management
- **Environment Variables**: Secure API key storage and configuration
- **Exception Handling**: Robust error management for production stability

## Technical Architecture

### Backend Structure
The application follows a modular design pattern with distinct components:

1. **API Layer** (Flask)
   - Provides REST endpoints for stock analysis
   - Handles request validation and error responses

2. **Data Management Layer**
   - `FinancialDataManager`: Coordinates multiple data sources
   - Rate-limiting mechanisms to avoid API throttling
   - Fallback patterns for data source failures

3. **Analysis Engine**
   - `StockAnalyzer`: Processes financial data and generates insights
   - Sentiment analysis of news content
   - Technical indicators for price movement prediction

4. **Frontend Interface** (Streamlit)
   - Interactive UI with real-time feedback
   - Language localization support
   - Responsive data visualization

## Installation

### Prerequisites

- Python 3.8+
- API keys for:
  - [NewsAPI.org](https://newsapi.org/)
  - [OpenAI](https://openai.com/api/)
  - [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/igaltal/ai-stock-analyst.git
   cd ai-stock-analyst
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file and add your API keys.

## Usage

### Running the Application

The simplest way to run the application is using the provided Makefile:

```
make run
```

This will start both the Flask API server and the Streamlit UI concurrently.

### Command-line Options

- Run only the API server:
  ```
  make run-api
  ```

- Run only the Streamlit UI:
  ```
  make run-ui
  ```

### API Endpoints

- **POST /api/stock/analyze**
  - Request body: `{"ticker": "AAPL"}`
  - Returns comprehensive analysis including:
    - Company profile and financial data
    - News sentiment analysis
    - AI-generated investment recommendation
    - Historical price data for visualization

## Implementation Details

### Data Source Priority

The system attempts to fetch data from multiple sources in this order:
1. Yahoo Finance (primary source)
2. Alpha Vantage (secondary source)
3. Mock data generator (fallback when both APIs fail)

### Rate Limit Management

- Dynamic delays between API requests
- Random user-agent rotation to avoid detection
- Caching of commonly requested data
- Pre-cached data for popular stocks to reduce API calls

### Error Handling

- Comprehensive exception handling for all API interactions
- Graceful degradation when services are unavailable
- Informative user feedback during service disruptions

## Future Enhancements

Planned improvements to the platform include:
- Portfolio management capabilities
- Historical recommendation tracking
- Advanced technical indicators
- Machine learning price prediction models
- Expanded language support
- Mobile application

## Disclaimer

This tool provides analysis for informational purposes only. It is not intended as financial advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for discussion.
