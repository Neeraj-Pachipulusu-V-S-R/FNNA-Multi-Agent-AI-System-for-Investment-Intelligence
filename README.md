# 📰 Financial News Analysis Agent

A sophisticated AI-powered multi-agent system for analyzing financial news using **Google Gemini API**. This application provides comprehensive sentiment analysis, market impact assessment, risk evaluation, and investment recommendations for financial news articles.

## 🌟 Features

- **🤖 AI-Powered Analysis**: Leverages Google Gemini's advanced language model for intelligent analysis
- **📊 Multi-Agent Pipeline**: Specialized agents for different aspects of financial analysis
- **🎯 Sentiment Analysis**: Determines positive, negative, or neutral sentiment of financial news
- **📈 Market Impact Assessment**: Evaluates potential high, medium, or low market impact
- **⚠️ Risk Identification**: Identifies regulatory, financial, operational, and other risk categories
- **💡 Investment Recommendations**: Generates actionable investment signals and decisions
- **🏷️ Ticker Extraction**: Automatically identifies stock symbols from news content
- **🌐 Real-time News Fetching**: Integration with Serper API for latest financial news
- **📱 Interactive Web UI**: Beautiful Streamlit interface with enhanced user experience
- **🔧 Comprehensive Evaluation**: Built-in evaluation system for testing analysis accuracy
- **📈 Session History & Analytics**: Track, compare, and export multiple analyses
- **⚖️ Analysis Comparison**: Side-by-side comparison of up to 3 analyses
- **💾 Export Capabilities**: Export individual or bulk analyses in JSON/CSV formats
- **📊 Real-time Metrics**: Session statistics and confidence scoring

## 🚀 New Enhanced UI Features

### 📈 Session History Management
- **Automatic Tracking**: All analyses are automatically saved to session history
- **Smart Summaries**: Quick overview with sentiment counts, impact levels, and confidence scores
- **Visual Indicators**: Emoji-based sentiment indicators for quick recognition
- **Memory Management**: Automatically keeps last 10 analyses to prevent memory issues

### ⚖️ Analysis Comparison System
- **Multi-Analysis Comparison**: Compare up to 3 analyses side-by-side
- **Tabular View**: Structured comparison table with key metrics
- **Visual Charts**: Sentiment and impact distribution graphs
- **Pattern Recognition**: Identify trends across different news topics

### 💾 Advanced Export Options
- **Individual Export**: Export single analyses in JSON or CSV format
- **Bulk Export**: Export entire session history as structured CSV
- **Formatted Downloads**: Timestamped filenames for easy organization
- **Multiple Formats**: JSON for detailed data, CSV for spreadsheet analysis

### 📊 Real-time Analytics
- **Session Metrics**: Total analyses, positive sentiment count, high impact count
- **Confidence Tracking**: Average confidence scores across analyses
- **Risk Scoring**: Quantified risk assessment for each analysis
- **Interactive Controls**: Clear history, manage comparisons, quick actions

## 🏗️ Architecture

```
Financial News Analysis Agent/
├── core/                    # Core business logic
│   └── graph.py            # LangGraph pipeline definition
├── agents/                 # Specialized analysis agents
│   ├── preprocessing_agent.py    # Content cleaning & ticker extraction
│   ├── sentiment_agent.py        # Sentiment analysis
│   ├── market_impact_agent.py    # Market impact assessment
│   ├── entity_risk_agent.py      # Risk identification
│   └── aggregator_agent.py       # Final analysis aggregation
├── utils/                  # Utility modules
│   ├── llm_client.py      # Google Gemini API client
│   ├── serper_client.py   # News fetching client
│   └── id_generator.py    # Unique ID generation
├── evaluation/            # Evaluation and testing
│   └── evaluator.py      # Analysis evaluation system
├── config.py             # Configuration management
├── main.py              # Enhanced Streamlit web application
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free at [ai.google.dev](https://ai.google.dev/))
- Serper API key (free at [serper.dev](https://serper.dev/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Neeraj-Pachipulusu-V-S-R/FNNA-Multi-Agent-AI-System-for-Investment-Intelligence.git
   cd FNNA-Multi-Agent-AI-System-for-Investment-Intelligence
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Google Gemini API Configuration
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Serper API Configuration  
   SERPER_API_KEY=your_serper_api_key_here
   
   # Optional: Model Configuration
   GEMINI_MODEL=gemini-1.5-flash
   DEFAULT_TEMPERATURE=0.3
   DEFAULT_MAX_TOKENS=500
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Access the web interface**
   
   Open your browser and navigate to `http://localhost:8501`

## 🎯 Usage

### Web Interface

1. **Enter a Financial Topic**: Type a financial topic like "Tesla earnings" or "Apple stock" in the chat input
2. **Select Article**: Choose from the fetched news articles or analyze the top result
3. **View Analysis**: Get comprehensive analysis including:
   - Sentiment classification
   - Market impact assessment
   - Risk identification
   - Investment recommendation
   - Extracted ticker symbols
   - Confidence scoring

### 📈 Using Session History
4. **Review History**: Check the sidebar for automatically tracked analyses
5. **Compare Analyses**: Select multiple analyses for side-by-side comparison
6. **Export Data**: Download individual analyses or bulk session data
7. **Track Patterns**: Monitor sentiment trends and impact distributions

### Programmatic Usage

```python
from core.graph import analyze_news_article

# Prepare news data
news_data = {
    "article_id": "example_001",
    "headline": "Tesla Reports Record Quarterly Earnings",
    "content": "Tesla Inc. announced record quarterly earnings...",
    "published_at": "2024-01-15"
}

# Run analysis
result = analyze_news_article(news_data)
final_analysis = result["final_analysis"]

print(f"Sentiment: {final_analysis['sentiment']}")
print(f"Market Impact: {final_analysis['impact_level']}")
print(f"Investment Decision: {final_analysis['decision']}")
print(f"Confidence Score: {final_analysis['confidence_score']}")
```

## 🤖 Agent Pipeline

The system uses a multi-agent architecture with specialized components:

### 1. Preprocessing Agent
- **Purpose**: Clean and normalize news content
- **Functions**: Extract ticker symbols, remove noise, format content
- **Output**: Clean content and identified tickers

### 2. Sentiment Agent
- **Purpose**: Analyze financial sentiment
- **Analysis**: Positive, negative, or neutral sentiment classification
- **Factors**: Growth indicators, risk signals, market outlook

### 3. Market Impact Agent
- **Purpose**: Assess potential market impact
- **Levels**: High, medium, or low impact classification
- **Considerations**: Event significance, company size, market conditions

### 4. Entity Risk Agent
- **Purpose**: Identify potential risks
- **Categories**: Regulatory, financial, operational, geopolitical, legal, cyber
- **Output**: List of applicable risk categories

### 5. Aggregator Agent
- **Purpose**: Synthesize all analyses into final recommendations
- **Features**: Investment signals, confidence scoring, risk-adjusted decisions
- **Output**: Comprehensive analysis summary with actionable insights

## 📊 Evaluation System

The system includes a comprehensive evaluation framework:

```bash
# Run evaluation with built-in test cases
python evaluation/evaluator.py
```

**Evaluation Metrics:**
- Sentiment classification accuracy
- Market impact prediction accuracy
- Risk identification overlap
- Overall analysis quality score

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | - | ✅ |
| `SERPER_API_KEY` | Serper API key for news | - | ✅ |
| `GEMINI_MODEL` | Gemini model to use | `gemini-1.5-flash` | ❌ |
| `DEFAULT_TEMPERATURE` | LLM temperature | `0.3` | ❌ |
| `DEFAULT_MAX_TOKENS` | Max response tokens | `500` | ❌ |

### Model Configuration

The system uses Google Gemini 1.5 Flash by default, which provides:
- **Free tier availability**: No cost for moderate usage
- **High performance**: Fast response times
- **Advanced reasoning**: Superior financial analysis capabilities
- **Reliable output**: Consistent response formatting

## 🆚 Comparison with Base Version

| Aspect | Base - Together AI | New - Google Gemini |
|--------|----------------------|-------------------|
| **API Cost** | Paid service | **Free tier available** |
| **Model Quality** | Llama 3.3 70B | **Gemini 1.5 Flash** |
| **Performance** | Good | **Enhanced** |
| **Reliability** | Variable | **More consistent** |
| **Architecture** | Monolithic | **Modular multi-agent** |
| **Error Handling** | Basic | **Comprehensive** |
| **Evaluation** | Limited | **Full evaluation suite** |
| **UI/UX** | Basic | **Enhanced with History & Analytics** |
| **Session Management** | None | **Full session tracking** |
| **Export Options** | None | **JSON/CSV export capabilities** |
| **Analysis Comparison** | None | **Side-by-side comparison** |
| **Real-time Metrics** | None | **Live statistics and confidence scoring** |

## 💡 UI Enhancement Features

### 📊 Session Analytics Dashboard
- **Live Metrics**: Total analyses, sentiment distribution, impact levels
- **Confidence Tracking**: Average confidence scores with real-time updates
- **Visual Indicators**: Emoji-based sentiment representation
- **Smart Organization**: Chronological history with easy navigation

### ⚖️ Advanced Comparison System
- **Multi-Select Comparison**: Compare up to 3 analyses simultaneously
- **Structured Data View**: Tabular comparison with key metrics
- **Visual Analytics**: Bar charts for sentiment and impact distribution
- **Export Comparisons**: Download comparison data for further analysis

### 💾 Professional Export Options
- **Format Flexibility**: JSON for technical use, CSV for business analysis
- **Bulk Operations**: Export entire session or selected analyses
- **Timestamped Files**: Automatic filename generation with timestamps
- **Data Integrity**: Structured export maintaining all analysis details

## 🛠️ Development

### Adding New Agents

1. Create a new agent file in the `agents/` directory
2. Implement the `run(state: Dict[str, Any]) -> Dict[str, Any]` function
3. Add the agent to the graph in `core/graph.py`
4. Update the state schema if needed

### Extending Analysis

- **Custom Risk Categories**: Modify `entity_risk_agent.py`
- **Additional Sentiment Factors**: Update `sentiment_agent.py`
- **New Impact Metrics**: Enhance `market_impact_agent.py`
- **Different Decision Logic**: Customize `aggregator_agent.py`

### Enhancing UI Features

- **Additional Visualizations**: Extend `render_comparison_view()` function
- **New Export Formats**: Modify `export_analysis()` function
- **Custom Metrics**: Add new calculations to `render_history_sidebar()`
- **Advanced Filtering**: Implement search and filter capabilities

### Testing

```bash
# Run unit tests
python -m pytest tests/

# Run evaluation
python evaluation/evaluator.py

# Test individual components
python -c "from core.graph import analyze_news_article; print('System ready!')"
```

## 🔒 Security & Best Practices

- **Environment Variables**: Never commit API keys to version control
- **Rate Limiting**: Respect API rate limits for both Gemini and Serper
- **Error Handling**: Comprehensive error handling throughout the pipeline
- **Input Validation**: Sanitization of news content and user inputs
- **Session Management**: Secure session state handling in Streamlit
- **Data Privacy**: No persistent storage of sensitive analysis data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini**: For providing powerful and accessible AI capabilities
- **Serper**: For reliable financial news data access
- **LangGraph**: For enabling sophisticated multi-agent workflows
- **Streamlit**: For the intuitive web interface framework
- **Pandas**: For data processing and export capabilities

## 📞 Support

For questions, issues, or contributions:

- **Issues**: [GitHub Issues](https://github.com/Neeraj-Pachipulusu-V-S-R/FNNA-Multi-Agent-AI-System-for-Investment-Intelligence/issues)
- **Email**: [neerajpachipulusuvsr@gmail.com](mailto:neerajpachipulusuvsr@gmail.com)

---

**🚀 Ready to analyze financial news with enhanced AI-powered insights and session management? Get started now!** 
