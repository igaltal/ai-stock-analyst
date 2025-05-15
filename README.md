# AI Stock Analyst\n\nAn intelligent financial analysis tool leveraging AI to provide investment recommendations based on real-time news.

## Overview

AI Stock Analyst is a powerful tool that processes stock ticker symbols and performs automated analysis of current news sentiment to generate actionable investment insights. By combining natural language processing with financial data visualization, it helps investors make informed decisions with minimal research effort.

## Features

- **Real-time News Analysis**: Automatically fetches and processes the latest news articles related to specified stocks
- **AI-Powered Insights**: Utilizes advanced language models to summarize news and analyze market sentiment
- **Clear Recommendations**: Generates straightforward "Buy," "Hold," or "Sell" recommendations based on comprehensive analysis
- **Visual Data Representation**: Displays stock price trends over the past month for additional context
- **User-Friendly Interface**: Simple, intuitive Streamlit frontend allows users to quickly obtain insights

## Technical Architecture

- **Backend**: RESTful API built with Flask providing endpoints for stock analysis
- **AI Processing**: Integration with OpenAI's GPT-3.5 for text summarization and sentiment analysis
- **Data Sources**: Real-time market news from NewsAPI.org and stock data from Yahoo Finance
- **Frontend**: Clean, responsive Streamlit interface for seamless user experience

## Installation

### Prerequisites

- Python 3.8+
- API keys for:
  - [NewsAPI.org](https://newsapi.org/)
  - [OpenAI](https://openai.com/api/)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-stock-analyst.git
   cd ai-stock-analyst
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file and add your API keys.

## Usage

### Running the Application

The easiest way to run the application is to use the provided `run.py` script:

```
python run.py
```

This will start both the Flask API server and the Streamlit UI.

### Command-line Options

- Run only the API server:
  ```
  python run.py --api-only
  ```

- Run only the Streamlit UI:
  ```
  python run.py --ui-only
  ```

### Running Components Separately

#### Flask API

Start the Flask API server:
```
python app.py
```

The API will be available at `http://localhost:5000`.

#### Streamlit Frontend

In a separate terminal, start the Streamlit app:
```
streamlit run streamlit_app.py
```

The Streamlit interface will be available at `http://localhost:8501`.

### API Endpoints

- **POST /api/stock/analyze**
  - Request body: `{"ticker": "AAPL"}`
  - Returns analysis data including news summary, sentiment, recommendation, and price data

## Example

Input a stock ticker like `AAPL` in the Streamlit interface to receive:
- Current stock price and price change
- Price trend chart for the past month
- AI-generated summary of recent news
- Sentiment analysis (Positive, Neutral, or Negative)
- Investment recommendation (Buy, Hold, or Sell) with reasoning
- Recent news articles related to the stock

## Disclaimer

This tool provides analysis for informational purposes only. It is not intended as financial advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
