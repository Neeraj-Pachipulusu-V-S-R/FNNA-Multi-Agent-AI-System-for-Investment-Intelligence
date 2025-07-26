from utils.llm_client import gemini_prompt
from typing import Dict, Any, List
import json
import re

def parse_risks(risks_text: str) -> List[str]:
    """
    Parse risk categories from LLM response
    
    Args:
        risks_text: Raw response from LLM
        
    Returns:
        List of risk categories
    """
    # Try to extract list-like content
    risks = []
    
    # Remove common formatting
    cleaned = risks_text.strip().lower()
    
    # Try different parsing approaches
    
    # 1. Look for Python list format
    list_match = re.search(r'\[(.*?)\]', cleaned)
    if list_match:
        try:
            # Clean and split
            items = list_match.group(1).replace("'", "").replace('"', "").split(',')
            risks = [item.strip() for item in items if item.strip()]
        except Exception:
            pass
    
    # 2. Look for comma-separated values
    if not risks:
        # Split by common separators
        for separator in [',', ';', '\n']:
            if separator in cleaned:
                risks = [item.strip() for item in cleaned.split(separator) if item.strip()]
                break
    
    # 3. Look for individual risk categories
    if not risks:
        risk_categories = ['regulatory', 'geopolitical', 'financial', 'operational', 'market', 'credit', 'liquidity', 'reputation', 'cyber', 'legal']
        risks = [category for category in risk_categories if category in cleaned]
    
    # Filter out common non-risks
    filtered_risks = []
    for risk in risks:
        risk = risk.strip().lower()
        if risk and risk not in ['none', 'no', 'nil', 'na', 'n/a', '']:
            filtered_risks.append(risk)
    
    return filtered_risks if filtered_risks else ["none"]

def run(state):
    """
    Entity risk analysis agent: Identify potential risks in financial news
    
    Args:
        state: NewsState object with cleaned_content
        
    Returns:
        Updated NewsState object with risk assessment
    """
    try:
        content = state.cleaned_content
        sentiment = state.sentiment
        tickers = state.tickers
        
        if not content:
            print("Warning: No cleaned content found for risk analysis")
            state.risks = ["none"]
            return state
        
        # Build context-aware prompt
        ticker_context = f" The analysis involves: {', '.join(tickers)}." if tickers else ""
        
        prompt = f"""Identify potential risks mentioned or implied in the following financial news content.{ticker_context}

Consider these risk categories:
- regulatory: Government regulations, compliance issues, policy changes
- geopolitical: International relations, trade wars, sanctions
- financial: Credit risks, liquidity issues, market volatility
- operational: Business operations, supply chain, management issues
- market: Competition, market share, industry trends
- legal: Lawsuits, litigation, legal disputes
- reputation: Brand damage, public relations issues
- cyber: Technology risks, data breaches, security issues

Respond with a comma-separated list of relevant risk categories (e.g., "regulatory, financial, market"). If no specific risks are identified, respond with "none".

Content:
\"\"\"
{content}
\"\"\"

Risks:"""
        
        # Get risk assessment from Gemini
        risks_response = gemini_prompt(prompt, temperature=0.3, max_tokens=100)
        
        # Parse the response
        risks = parse_risks(risks_response)
        
        state.risks = risks
        print(f"Risk analysis complete: {', '.join(risks)}")
        
        return state
        
    except Exception as e:
        print(f"Error in entity risk agent: {str(e)}")
        state.risks = ["none"]
        return state
