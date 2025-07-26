from langgraph.graph import StateGraph
from agents import (
    preprocessing_agent,
    sentiment_agent,
    market_impact_agent,
    entity_risk_agent,
    aggregator_agent,
)
from pydantic import BaseModel
from typing import Dict, Any, List

# Define schema to represent the state passed between agents
class NewsState(BaseModel):
    """State schema for the news analysis pipeline"""
    news: Dict[str, Any]
    cleaned_content: str = ""
    tickers: List[str] = []
    sentiment: str = ""
    market_impact: str = ""
    risks: List[str] = []
    final_analysis: Dict[str, Any] = {}

class NewsAnalysisGraph:
    """Main graph builder for the financial news analysis pipeline"""
    
    def __init__(self):
        self.graph = None
    
    def build_graph(self):
        """Build and compile the LangGraph for news analysis"""
        if self.graph is not None:
            return self.graph
            
        graph = StateGraph(state_schema=NewsState)

        # Add all agent nodes
        graph.add_node("PreprocessingAgent", preprocessing_agent.run)
        graph.add_node("SentimentAnalysisAgent", sentiment_agent.run)
        graph.add_node("MarketImpactAgent", market_impact_agent.run)
        graph.add_node("EntityRiskAgent", entity_risk_agent.run)
        graph.add_node("AggregatorAgent", aggregator_agent.run)

        # Define the workflow
        graph.set_entry_point("PreprocessingAgent")
        graph.add_edge("PreprocessingAgent", "SentimentAnalysisAgent")
        graph.add_edge("SentimentAnalysisAgent", "MarketImpactAgent")
        graph.add_edge("MarketImpactAgent", "EntityRiskAgent")
        graph.add_edge("EntityRiskAgent", "AggregatorAgent")
        graph.set_finish_point("AggregatorAgent")
        
        self.graph = graph.compile()
        return self.graph
    
    def analyze_news(self, news_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single news article through the agent pipeline
        
        Args:
            news_data: Dictionary containing news article information
            
        Returns:
            Analysis results including sentiment, impact, risks, and final decision
        """
        graph = self.build_graph()
        result = graph.invoke({"news": news_data})
        return result

# Global instance for backward compatibility
_graph_instance = NewsAnalysisGraph()

def build_graph():
    """Legacy function for backward compatibility"""
    return _graph_instance.build_graph()

def analyze_news_article(news_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a news article through the agent pipeline"""
    return _graph_instance.analyze_news(news_data) 