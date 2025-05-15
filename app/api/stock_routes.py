from flask import Blueprint, request, jsonify, current_app
from app.models.stock_analyzer import StockAnalyzer
import traceback

bp = Blueprint('stock', __name__, url_prefix='/api/stock')

@bp.route('/analyze', methods=['POST'])
def analyze_stock():
    """Analyze a stock based on its ticker symbol."""
    try:
        data = request.get_json()
        
        if not data or 'ticker' not in data:
            return jsonify({'error': 'No ticker symbol provided'}), 400
        
        ticker = data['ticker'].upper()
        
        # Create stock analyzer with API keys from app config
        analyzer = StockAnalyzer(
            news_api_key=current_app.config['NEWS_API_KEY'],
            openai_api_key=current_app.config['OPENAI_API_KEY'],
            alpha_vantage_api_key=current_app.config['ALPHA_VANTAGE_API_KEY']
        )
        
        # Perform analysis
        result = analyzer.analyze(ticker)
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error analyzing stock: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500 