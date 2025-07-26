from utils.llm_client import gemini_prompt
from typing import Dict, Any

def run(state):
    """
    Sentiment analysis agent: Analyze financial sentiment of news content
    
    Args:
        state: NewsState object with cleaned_content
        
    Returns:
        Updated NewsState object with sentiment analysis
    """
    try:
        content = state.cleaned_content
        
        if not content:
            print("Warning: No cleaned content found for sentiment analysis")
            state.sentiment = "neutral"
            return state
        
        prompt = f"""Analyze the financial sentiment of the following news article content. 

Consider factors such as:
- Positive indicators: growth, profits, expansion, success, positive outlook
- Negative indicators: losses, decline, bankruptcy, failure, negative outlook
- Neutral indicators: routine announcements, mixed signals, uncertainty

Respond with ONLY one word: 'positive', 'negative', or 'neutral'.

Content:
\"\"\"
{content}
\"\"\"

Sentiment:"""
        
        # Get sentiment from Gemini
        sentiment_response = gemini_prompt(prompt, temperature=0.2, max_tokens=10)
        
        # Clean and validate response
        sentiment = sentiment_response.lower().strip()
        
        # Ensure valid sentiment
        valid_sentiments = ["positive", "negative", "neutral"]
        if sentiment not in valid_sentiments:
            # Try to extract valid sentiment from response
            for valid_sentiment in valid_sentiments:
                if valid_sentiment in sentiment:
                    sentiment = valid_sentiment
                    break
            else:
                print(f"Invalid sentiment response: {sentiment_response}. Defaulting to neutral.")
                sentiment = "neutral"
        
        state.sentiment = sentiment
        print(f"Sentiment analysis complete: {sentiment}")
        
        return state
        
    except Exception as e:
        print(f"Error in sentiment agent: {str(e)}")
        state.sentiment = "neutral"
        return state
