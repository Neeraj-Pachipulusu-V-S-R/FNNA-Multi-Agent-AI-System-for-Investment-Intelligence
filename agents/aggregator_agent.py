from typing import Dict, Any, List

def generate_investment_decision(sentiment: str, impact_level: str, risks: List[str], tickers: List[str]) -> str:
    """
    Generate investment decision based on analysis results
    
    Args:
        sentiment: Sentiment analysis result
        impact_level: Market impact level
        risks: List of identified risks
        tickers: List of identified tickers
        
    Returns:
        Investment decision string
    """
    # Calculate risk score
    high_risk_categories = {'regulatory', 'geopolitical', 'financial', 'legal'}
    risk_score = len([risk for risk in risks if risk in high_risk_categories])
    has_significant_risk = risk_score > 0 and 'none' not in risks
    
    # Decision logic
    if sentiment == "positive":
        if impact_level == "high":
            if not has_significant_risk:
                return "Strong Buy Signal - Positive sentiment with high market impact and manageable risks"
            else:
                return "Cautious Buy Signal - Positive sentiment but monitor identified risks"
        elif impact_level == "medium":
            if not has_significant_risk:
                return "Moderate Buy Signal - Positive sentiment with medium impact"
            else:
                return "Hold/Monitor - Positive sentiment offset by medium risks"
        else:  # low impact
            return "Weak Buy Signal - Positive sentiment but limited market impact expected"
    
    elif sentiment == "negative":
        if impact_level == "high":
            return "Strong Sell Signal - Negative sentiment with high market impact"
        elif impact_level == "medium":
            return "Moderate Sell/Avoid Signal - Negative sentiment with medium impact"
        else:  # low impact
            return "Monitor/Hold - Negative sentiment but limited market impact expected"
    
    else:  # neutral sentiment
        if impact_level == "high":
            if has_significant_risk:
                return "Cautious Hold - Neutral sentiment but high impact and significant risks"
            else:
                return "Monitor - Neutral sentiment with high potential impact"
        elif impact_level == "medium":
            return "Hold - Neutral sentiment with medium impact"
        else:  # low impact
            return "No Action - Neutral sentiment with low market impact"

def run(state):
    """
    Aggregator agent: Combine all analysis results and generate final decision
    
    Args:
        state: NewsState object with all analysis results
        
    Returns:
        Updated NewsState object with final analysis summary
    """
    try:
        # Extract analysis results
        sentiment = state.sentiment
        impact_level = state.market_impact
        risks = state.risks
        tickers = state.tickers
        
        # Generate investment decision
        decision = generate_investment_decision(sentiment, impact_level, risks, tickers)
        
        # Create comprehensive summary
        summary = {
            "sentiment": sentiment,
            "impact_level": impact_level,
            "risks": risks,
            "tickers": tickers,
            "decision": decision,
            "risk_score": len([risk for risk in risks if risk != "none"]),
            "has_tickers": len(tickers) > 0,
            "analysis_quality": "complete"
        }
        
        # Add confidence metrics
        confidence_factors = []
        if sentiment in ["positive", "negative"]:
            confidence_factors.append("clear_sentiment")
        if impact_level in ["high", "medium"]:
            confidence_factors.append("measurable_impact")
        if tickers:
            confidence_factors.append("identified_companies")
        
        summary["confidence_factors"] = confidence_factors
        summary["confidence_score"] = len(confidence_factors) / 3.0  # Normalized to 0-1
        
        state.final_analysis = summary
        
        print(f"Analysis aggregated - Decision: {decision}")
        print(f"Confidence Score: {summary['confidence_score']:.2f}")
        
        return state
        
    except Exception as e:
        print(f"Error in aggregator agent: {str(e)}")
        
        # Fallback summary
        state.final_analysis = {
            "sentiment": getattr(state, 'sentiment', 'neutral'),
            "impact_level": getattr(state, 'market_impact', 'low'),
            "risks": getattr(state, 'risks', ['none']),
            "tickers": getattr(state, 'tickers', []),
            "decision": "Unable to generate decision - Analysis incomplete",
            "analysis_quality": "incomplete",
            "confidence_score": 0.0
        }
        
        return state
