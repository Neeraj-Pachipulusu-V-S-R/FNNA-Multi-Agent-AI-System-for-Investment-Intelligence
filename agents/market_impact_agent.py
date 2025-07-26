from utils.llm_client import gemini_prompt
from typing import Dict, Any

def run(state):
    """
    Market impact analysis agent: Evaluate potential market impact of news
    
    Args:
        state: NewsState object with cleaned_content and sentiment
        
    Returns:
        Updated NewsState object with market impact assessment
    """
    try:
        content = state.cleaned_content
        sentiment = state.sentiment
        tickers = state.tickers
        
        if not content:
            print("Warning: No cleaned content found for market impact analysis")
            state.market_impact = "low"
            return state
        
        # Build context-aware prompt
        ticker_context = f" The analysis involves: {', '.join(tickers)}." if tickers else ""
        sentiment_context = f" The sentiment is {sentiment}."
        
        prompt = f"""Evaluate the potential market impact of the following financial news content.{ticker_context}{sentiment_context}

Consider factors such as:
- High impact: Major corporate events (earnings surprises, M&A, regulatory changes), market-moving announcements
- Medium impact: Standard earnings reports, product launches, management changes, industry trends
- Low impact: Routine announcements, minor updates, general market commentary

Respond with ONLY one word: 'high', 'medium', or 'low'.

Content:
\"\"\"
{content}
\"\"\"

Market Impact:"""
        
        # Get impact assessment from Gemini
        impact_response = gemini_prompt(prompt, temperature=0.2, max_tokens=10)
        
        # Clean and validate response
        impact = impact_response.lower().strip()
        
        # Ensure valid impact level
        valid_impacts = ["high", "medium", "low"]
        if impact not in valid_impacts:
            # Try to extract valid impact from response
            for valid_impact in valid_impacts:
                if valid_impact in impact:
                    impact = valid_impact
                    break
            else:
                print(f"Invalid impact response: {impact_response}. Defaulting to low.")
                impact = "low"
        
        state.market_impact = impact
        print(f"Market impact analysis complete: {impact}")
        
        return state
        
    except Exception as e:
        print(f"Error in market impact agent: {str(e)}")
        state.market_impact = "low"
        return state
