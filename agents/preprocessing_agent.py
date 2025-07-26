import re
from typing import List, Dict, Any

def extract_tickers(content: str) -> List[str]:
    """
    Extract stock tickers from news content
    
    Args:
        content: News article content
        
    Returns:
        List of extracted ticker symbols
    """
    tickers = []
    
    # Common patterns for ticker symbols
    patterns = [
        r'\(NASDAQ:\s*([A-Z]{1,5})\)',  # (NASDAQ: TSLA)
        r'\(NYSE:\s*([A-Z]{1,5})\)',    # (NYSE: AAPL)
        r'\(([A-Z]{1,5})\)',            # (TSLA)
        r'\$([A-Z]{1,5})\b',            # $TSLA
        r'\b([A-Z]{1,5})\s+stock\b',    # TSLA stock
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        tickers.extend([match.upper() for match in matches])
    
    # Remove duplicates and common false positives
    false_positives = {'USD', 'CEO', 'CFO', 'IPO', 'ETF', 'SEC', 'FDA', 'DOJ', 'AI', 'API'}
    tickers = list(set([ticker for ticker in tickers if ticker not in false_positives]))
    
    return tickers

def clean_content(content: str) -> str:
    """
    Clean and normalize news content
    
    Args:
        content: Raw news content
        
    Returns:
        Cleaned content string
    """
    if not content:
        return ""
    
    # Remove extra whitespace and normalize
    cleaned = re.sub(r'\s+', ' ', content.strip())
    
    # Remove common noise patterns
    cleaned = re.sub(r'\[.*?\]', '', cleaned)  # Remove [tags]
    cleaned = re.sub(r'\(Reuters\)', '', cleaned)  # Remove (Reuters)
    cleaned = re.sub(r'\(AP\)', '', cleaned)  # Remove (AP)
    
    return cleaned.strip()

def run(state):
    """
    Preprocessing agent: Extract tickers and clean content
    
    Args:
        state: NewsState object with news data
        
    Returns:
        Updated NewsState object with cleaned content and extracted tickers
    """
    try:
        news = state.news
        
        if not news:
            print("Warning: No news data found in state")
            state.cleaned_content = ""
            state.tickers = []
            return state
        
        # Get content from news
        content = news.get("content", "")
        headline = news.get("headline", "")
        
        # Combine headline and content for analysis
        full_content = f"{headline}. {content}".strip()
        
        # Extract tickers from full content
        tickers = extract_tickers(full_content)
        
        # Clean the content
        cleaned_content = clean_content(full_content)
        
        # Update state
        state.tickers = tickers
        state.cleaned_content = cleaned_content
        
        print(f"Preprocessing complete: Found {len(tickers)} tickers, cleaned {len(cleaned_content)} characters")
        
        return state
        
    except Exception as e:
        print(f"Error in preprocessing agent: {str(e)}")
        state.cleaned_content = ""
        state.tickers = []
        return state
