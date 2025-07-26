import requests
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SerperClient:
    """Client for Google Serper API to fetch financial news"""
    
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.base_url = "https://google.serper.dev/news"
        
        if not self.api_key:
            raise ValueError("SERPER_API_KEY environment variable is required")
    
    def fetch_financial_news(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch financial news articles for a given query
        
        Args:
            query: Search query for financial news
            num_results: Number of results to return (default: 10)
            
        Returns:
            List of news articles with headline, content, and published_at
        """
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": query,
            "num": num_results
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get("news", [])
            
            # Parse and format articles
            parsed_articles = []
            for article in articles:
                parsed_article = {
                    "headline": article.get("title", ""),
                    "content": article.get("snippet", ""),
                    "published_at": article.get("date", ""),
                    "link": article.get("link", ""),
                    "source": article.get("source", "")
                }
                
                # Only include articles with meaningful content
                if parsed_article["headline"] and parsed_article["content"]:
                    parsed_articles.append(parsed_article)
            
            return parsed_articles
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return []

# Global client instance - lazy initialization
_serper_client: Optional[SerperClient] = None

def _get_client() -> SerperClient:
    """Get or create the serper client instance"""
    global _serper_client
    if _serper_client is None:
        _serper_client = SerperClient()
    return _serper_client

def fetch_financial_news(query: str, num_results: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch financial news articles (backward compatibility function)
    
    Args:
        query: Search query for financial news
        num_results: Number of results to return
        
    Returns:
        List of news articles
    """
    try:
        client = _get_client()
        return client.fetch_financial_news(query, num_results)
    except ValueError as e:
        print(f"Configuration error: {str(e)}")
        return []
