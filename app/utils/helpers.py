import json
import re
from datetime import datetime, timedelta

def format_currency(amount, currency_symbol='$'):
    """Format a number as currency."""
    if amount is None:
        return 'N/A'
    return f"{currency_symbol}{amount:,.2f}"

def format_percentage(value):
    """Format a decimal as percentage."""
    if value is None:
        return 'N/A'
    return f"{value:.2f}%"

def get_date_range(days=30):
    """Get the date range for a given number of days from today."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """Format a datetime object as string."""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except ValueError:
            return dt
    return dt.strftime(format_str)

def clean_html(text):
    """Remove HTML tags from text."""
    if not text:
        return ''
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def extract_json_from_text(text):
    """Extract JSON object from text that might contain other content."""
    if not text:
        return None
    
    # Find the first opening brace
    start_idx = text.find('{')
    if start_idx == -1:
        return None
    
    # Find the matching closing brace
    brace_count = 0
    for i in range(start_idx, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                # Found the matching closing brace
                json_str = text[start_idx:i+1]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # Try another approach if this fails
                    pass
    
    # If we couldn't parse it precisely, try a more aggressive approach
    try:
        # Find any JSON-like structure
        matches = re.findall(r'({.*})', text, re.DOTALL)
        if matches:
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
    except:
        pass
    
    return None 