# config.py
"""Configuration file for News Research Tool"""

import streamlit as st

# App Configuration
APP_CONFIG = {
    "page_title": "News Research Tool",
    "page_icon": "📰",
    "layout": "wide"
}

# Groq API Configuration
GROQ_CONFIG = {
    "api_url": "https://api.groq.com/openai/v1/chat/completions",
    "available_models": [
        "openai/gpt-oss-120b",
        "llama-3.1-8b-instant", 
        "moonshotai/kimi-k2-instruct-0905",
        "gemma-7b-it"
    ],
    "default_model": "openai/gpt-oss-120b",
    "temperature": 0.3,
    "max_tokens": 1000
}

# NewsAPI Configuration
NEWSAPI_CONFIG = {
    "api_url": "https://newsapi.org/v2/everything",
    "language": "en",
    "default_sort": "relevancy",
    "default_page_size": 15,
    "default_days_back": 7,
    "max_articles": 50
}

# UI Configuration
UI_CONFIG = {
    "max_days_back": 30,
    "min_articles": 5,
    "max_articles_display": 50
}

# Custom CSS Styles
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #1565c0;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .news-card {
        border: 1px solid #e0e0e0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(145deg, #ffffff, #f5f5f5);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .news-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.15);
    }
    .summary-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border-left: 4px solid #1f77b4;
    }
    .sidebar-header {
        color: #1f77b4;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .footer-text {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-top: 2rem;
    }
</style>
"""

# Prompt Templates
ANALYSIS_PROMPT_TEMPLATE = """
As an expert equity research analyst with 15+ years of experience, analyze the following news articles related to: "{query}"

News Content:
{news_content}

Please provide a comprehensive analysis including:

📊 **EXECUTIVE SUMMARY:**
- Key developments and breaking news
- Overall market sentiment (Bullish/Bearish/Neutral)

📈 **MARKET IMPLICATIONS:**
- Short-term price impact expectations
- Long-term investment thesis changes
- Sector-wide effects

⚠️ **RISK ASSESSMENT:**
- Potential downside risks
- Regulatory or competitive threats
- Market volatility factors

🎯 **INVESTMENT RECOMMENDATIONS:**
- Buy/Hold/Sell signals
- Price targets and timeframes
- Portfolio allocation suggestions

📰 **NEWS CREDIBILITY:**
- Source reliability assessment
- Information confirmation status

Keep the analysis professional, data-driven, and actionable for institutional investors.
"""

# Error Messages
ERROR_MESSAGES = {
    "no_groq_key": "❌ Please enter your Groq API key in the sidebar",
    "no_news_key": "❌ Please enter your NewsAPI key in the sidebar", 
    "no_query": "❌ Please enter a search query",
    "no_articles": "⚠️ No articles found for your query. Try different keywords.",
    "api_error": "❌ API Error: {error}",
    "general_error": "❌ An error occurred: {error}"
}

# Success Messages  
SUCCESS_MESSAGES = {
    "summary_downloaded": "✅ Summary downloaded successfully!",
    "articles_fetched": "✅ Successfully fetched {count} articles",
    "analysis_complete": "✅ AI analysis completed"
}

# Default Settings
DEFAULT_SETTINGS = {
    "model": GROQ_CONFIG["default_model"],
    "days_back": NEWSAPI_CONFIG["default_days_back"],
    "max_articles": NEWSAPI_CONFIG["default_page_size"]
}