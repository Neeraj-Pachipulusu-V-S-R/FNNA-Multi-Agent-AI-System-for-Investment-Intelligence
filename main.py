

import streamlit as st
import json
import pandas as pd
from datetime import datetime
from io import StringIO
from core.graph import NewsAnalysisGraph, analyze_news_article
from utils.serper_client import fetch_financial_news
from utils.id_generator import generate_user_id
from config import config

# Validate configuration on startup
try:
    config.validate_config()
except ValueError as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

# Configure Streamlit page
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="📰",
    layout="wide",  # Changed to wide for better history display
    initial_sidebar_state="expanded"
)

# Initialize session state for history
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'selected_comparison' not in st.session_state:
    st.session_state.selected_comparison = []
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = None
if 'current_articles' not in st.session_state:
    st.session_state.current_articles = []
if 'selected_article_idx' not in st.session_state:
    st.session_state.selected_article_idx = 0

def add_to_history(topic, news_data, analysis_result):
    """Add analysis result to session history"""
    history_entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "topic": topic,
        "article_id": news_data["article_id"],
        "headline": news_data["headline"],
        "published_at": news_data["published_at"],
        "analysis": analysis_result.get("final_analysis", {}),
        "full_result": analysis_result
    }
    st.session_state.analysis_history.append(history_entry)
    
    # Keep only last 10 analyses to prevent memory issues
    if len(st.session_state.analysis_history) > 10:
        st.session_state.analysis_history = st.session_state.analysis_history[-10:]

def export_analysis(analysis_data, format_type="json"):
    """Export analysis data in specified format"""
    if format_type == "json":
        return json.dumps(analysis_data, indent=2)
    elif format_type == "csv":
        # Flatten the analysis for CSV export
        flat_data = {
            "timestamp": analysis_data["timestamp"],
            "topic": analysis_data["topic"],
            "headline": analysis_data["headline"],
            "sentiment": analysis_data["analysis"].get("sentiment", ""),
            "impact_level": analysis_data["analysis"].get("impact_level", ""),
            "decision": analysis_data["analysis"].get("decision", ""),
            "risks": ", ".join(analysis_data["analysis"].get("risks", [])),
            "tickers": ", ".join(analysis_data["analysis"].get("tickers", [])),
            "confidence_score": analysis_data["analysis"].get("confidence_score", 0)
        }
        df = pd.DataFrame([flat_data])
        return df.to_csv(index=False)

def render_history_sidebar():
    """Render the analysis history sidebar"""
    with st.sidebar:
        st.header("📈 Analysis History")
        
        if st.session_state.analysis_history:
            # Summary stats
            total_analyses = len(st.session_state.analysis_history)
            positive_count = sum(1 for h in st.session_state.analysis_history 
                               if h["analysis"].get("sentiment") == "positive")
            high_impact_count = sum(1 for h in st.session_state.analysis_history 
                                  if h["analysis"].get("impact_level") == "high")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total", total_analyses)
                st.metric("Positive", positive_count)
            with col2:
                st.metric("High Impact", high_impact_count)
                avg_confidence = sum(h["analysis"].get("confidence_score", 0) 
                                   for h in st.session_state.analysis_history) / total_analyses
                st.metric("Avg Confidence", f"{avg_confidence:.2f}")
            
            st.divider()
            
            # History entries
            st.subheader("Recent Analyses")
            for i, analysis in enumerate(reversed(st.session_state.analysis_history)):
                idx = len(st.session_state.analysis_history) - 1 - i
                
                # Create sentiment emoji
                sentiment = analysis["analysis"].get("sentiment", "neutral")
                sentiment_emoji = {"positive": "📈", "negative": "📉", "neutral": "➡️"}
                
                with st.expander(f"{sentiment_emoji.get(sentiment, '📊')} {analysis['topic']} ({analysis['timestamp']})"):
                    st.write(f"**Headline**: {analysis['headline'][:60]}...")
                    st.write(f"**Sentiment**: {sentiment.title()}")
                    st.write(f"**Impact**: {analysis['analysis'].get('impact_level', 'Unknown').title()}")
                    st.write(f"**Decision**: {analysis['analysis'].get('decision', 'N/A')[:50]}...")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📋 View", key=f"view_{idx}"):
                            st.session_state.selected_for_detail = idx
                    with col2:
                        if st.button("⚖️ Compare", key=f"compare_{idx}"):
                            if idx not in st.session_state.selected_comparison:
                                if len(st.session_state.selected_comparison) < 3:
                                    st.session_state.selected_comparison.append(idx)
                                else:
                                    st.warning("Maximum 3 analyses for comparison")
                            else:
                                st.session_state.selected_comparison.remove(idx)
                    with col3:
                        # Export dropdown
                        export_format = st.selectbox(
                            "Export", ["JSON", "CSV"], 
                            key=f"export_format_{idx}",
                            label_visibility="collapsed"
                        )
                        if st.button("💾", key=f"export_{idx}"):
                            format_type = export_format.lower()
                            export_data = export_analysis(analysis, format_type)
                            st.download_button(
                                f"Download {export_format}",
                                export_data,
                                file_name=f"analysis_{analysis['timestamp'].replace(':', '-')}.{format_type}",
                                mime="application/json" if format_type == "json" else "text/csv",
                                key=f"download_{idx}"
                            )
            
            # Bulk actions
            if st.session_state.analysis_history:
                st.divider()
                st.subheader("Bulk Actions")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📊 Export All (CSV)"):
                        all_data = []
                        for analysis in st.session_state.analysis_history:
                            flat_data = {
                                "timestamp": analysis["timestamp"],
                                "topic": analysis["topic"],
                                "headline": analysis["headline"],
                                "sentiment": analysis["analysis"].get("sentiment", ""),
                                "impact_level": analysis["analysis"].get("impact_level", ""),
                                "decision": analysis["analysis"].get("decision", ""),
                                "risks": ", ".join(analysis["analysis"].get("risks", [])),
                                "tickers": ", ".join(analysis["analysis"].get("tickers", [])),
                                "confidence_score": analysis["analysis"].get("confidence_score", 0)
                            }
                            all_data.append(flat_data)
                        
                        df = pd.DataFrame(all_data)
                        csv_data = df.to_csv(index=False)
                        st.download_button(
                            "Download All Analyses",
                            csv_data,
                            file_name=f"financial_analysis_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                
                with col2:
                    if st.button("🗑️ Clear History"):
                        st.session_state.analysis_history = []
                        st.session_state.selected_comparison = []
                        st.rerun()
        else:
            st.info("No analyses yet. Start by entering a financial topic!")

def render_comparison_view():
    """Render comparison view for selected analyses"""
    if st.session_state.selected_comparison:
        st.header("⚖️ Analysis Comparison")
        
        # Show selected analyses for comparison
        comparison_data = [st.session_state.analysis_history[i] for i in st.session_state.selected_comparison]
        
        # Create comparison table
        comparison_df = pd.DataFrame([
            {
                "Topic": analysis["topic"],
                "Headline": analysis["headline"][:50] + "...",
                "Sentiment": analysis["analysis"].get("sentiment", "").title(),
                "Impact": analysis["analysis"].get("impact_level", "").title(),
                "Risks": ", ".join(analysis["analysis"].get("risks", [])),
                "Tickers": ", ".join(analysis["analysis"].get("tickers", [])),
                "Confidence": f"{analysis['analysis'].get('confidence_score', 0):.2f}",
                "Decision": analysis["analysis"].get("decision", "")[:30] + "..."
            }
            for analysis in comparison_data
        ])
        
        st.dataframe(comparison_df, use_container_width=True)
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Sentiment distribution
            sentiment_counts = comparison_df['Sentiment'].value_counts()
            st.bar_chart(sentiment_counts)
            st.caption("Sentiment Distribution")
        
        with col2:
            # Impact distribution
            impact_counts = comparison_df['Impact'].value_counts()
            st.bar_chart(impact_counts)
            st.caption("Impact Level Distribution")
        
        # Clear comparison button
        if st.button("Clear Comparison"):
            st.session_state.selected_comparison = []
            st.rerun()

# Main content
st.title(config.APP_TITLE)
st.markdown(f"*{config.APP_DESCRIPTION}*")

# Render sidebar
render_history_sidebar()

# Main content area
if st.session_state.selected_comparison:
    # Show comparison view if analyses are selected
    render_comparison_view()
    st.divider()

# Analysis section
st.header("🔍 New Analysis")

def main():
    """Main Streamlit application"""
    
    # User input for new topic
    topic = st.chat_input("Enter a financial topic you'd like to analyze (e.g., 'Tesla earnings', 'Apple stock'):")
    
    # Handle new topic input
    if topic:
        st.session_state.current_topic = topic
        st.session_state.selected_article_idx = 0
        
        st.info(f"🔍 Searching for financial news about: **{topic}**")
        
        # Fetch news articles
        with st.spinner("🛰️ Fetching latest news from Google..."):
            try:
                articles = fetch_financial_news(topic, num_results=5)
                st.session_state.current_articles = articles
            except Exception as e:
                st.error(f"Error fetching news: {str(e)}")
                return

        if not articles:
            st.error("❌ No relevant news found. Please try another topic or check your API configuration.")
            st.session_state.current_articles = []
            return
    
    # Display article selection and analysis if we have articles
    if st.session_state.current_articles:
        articles = st.session_state.current_articles
        
        st.subheader(f"📰 Articles for: {st.session_state.current_topic}")
        
        # Article selection
        if len(articles) > 1:
            # Use a key to ensure the selectbox updates properly
            new_selected_idx = st.selectbox(
                "Select an article to analyze:",
                range(len(articles)),
                index=st.session_state.selected_article_idx,
                format_func=lambda x: f"{articles[x]['headline'][:80]}..." if len(articles[x]['headline']) > 80 else articles[x]['headline'],
                key="article_selector"
            )
            
            # Check if selection changed
            if new_selected_idx != st.session_state.selected_article_idx:
                st.session_state.selected_article_idx = new_selected_idx
                st.rerun()
        else:
            st.session_state.selected_article_idx = 0
            st.info("Analyzing the only available article:")

        # Display selected article
        selected_article = articles[st.session_state.selected_article_idx]
        
        with st.container():
            st.markdown(f"**📰 Headline**: {selected_article['headline']}")
            st.markdown(f"**📄 Content**: {selected_article['content']}")
            st.markdown(f"**📅 Published**: {selected_article['published_at']}")
            if selected_article.get('source'):
                st.markdown(f"**📰 Source**: {selected_article['source']}")

        # Generate article ID
        article_id = generate_user_id(selected_article['headline'])
        st.caption(f"🆔 Article ID: `{article_id}`")

        # Prepare news data for analysis
        news_data = {
            "article_id": article_id,
            "headline": selected_article["headline"],
            "content": selected_article["content"],
            "published_at": selected_article["published_at"]
        }

        # Run analysis
        st.subheader("🧠 AI Analysis")
        
        with st.spinner("🤖 Analyzing news through AI agent pipeline..."):
            try:
                result = analyze_news_article(news_data)
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                return

        # Display results
        if "final_analysis" in result and result["final_analysis"]:
            analysis = result["final_analysis"]
            
            # Add to history
            add_to_history(st.session_state.current_topic, news_data, result)
            
            # Create columns for better layout
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Sentiment", analysis.get("sentiment", "Unknown").title())
                st.metric("📈 Market Impact", analysis.get("impact_level", "Unknown").title())
            
            with col2:
                risks = analysis.get("risks", [])
                risk_text = ", ".join(risks) if risks and risks != ["none"] else "None identified"
                st.metric("⚠️ Risks", risk_text)
                
                confidence = analysis.get("confidence_score", 0)
                st.metric("🎯 Confidence", f"{confidence:.2f}")
            
            with col3:
                tickers = analysis.get("tickers", [])
                ticker_text = ", ".join(tickers) if tickers else "None identified"
                st.metric("🏷️ Tickers", ticker_text)
                
                risk_score = analysis.get("risk_score", 0)
                st.metric("⚡ Risk Score", f"{risk_score}")

            # Investment decision
            decision = analysis.get("decision", "No decision available")
            if "buy" in decision.lower() or "upside" in decision.lower():
                st.success(f"💰 **Investment Signal**: {decision}")
            elif "downturn" in decision.lower() or "monitor" in decision.lower():
                st.warning(f"⚠️ **Investment Signal**: {decision}")
            else:
                st.info(f"📊 **Investment Signal**: {decision}")

            # Detailed analysis
            with st.expander("🔍 Detailed Analysis Results"):
                st.json(analysis)
                
            # Quick action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 Add to Comparison"):
                    latest_idx = len(st.session_state.analysis_history) - 1
                    if latest_idx not in st.session_state.selected_comparison:
                        if len(st.session_state.selected_comparison) < 3:
                            st.session_state.selected_comparison.append(latest_idx)
                            st.success("Added to comparison!")
                        else:
                            st.warning("Maximum 3 analyses for comparison")
            with col2:
                export_data = export_analysis(st.session_state.analysis_history[-1], "json")
                st.download_button(
                    "💾 Export JSON",
                    export_data,
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            with col3:
                export_data = export_analysis(st.session_state.analysis_history[-1], "csv")
                st.download_button(
                    "📊 Export CSV",
                    export_data,
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
        else:
            st.error("❌ Analysis failed. Please try again or check the logs.")
    
    elif st.session_state.current_topic is None:
        # Show instructions when no topic has been entered yet
        st.info("👆 Enter a financial topic above to start analyzing news articles!")

if __name__ == "__main__":
    main()
