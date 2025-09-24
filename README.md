# 📰 AI News Research Tool

> **Professional Equity Research Assistant powered by Groq AI & NewsAPI**

An intelligent news research tool that combines real-time news data with advanced AI analysis to provide comprehensive market insights for equity research and investment decisions.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-red.svg)

🚀 Key Features


🤖 **AI-Powered Analysis**
- **Smart Summarization**: Uses Groq's advanced LLMs for intelligent news analysis
- **Market Insights**: Provides investment recommendations and risk assessments  
- **Sentiment Analysis**: Analyzes market sentiment from multiple news sources
- **Multiple AI Models**: Choose from Llama, Mixtral, and Gemma models


### 📰 **Real-Time News Integration**
- **Live News Feed**: Fetches latest articles from NewsAPI
- **Multi-Source Research**: Aggregates news from hundreds of sources
- **Smart Filtering**: Date ranges, source filtering, and relevance sorting
- **Credible Sources**: Focus on financial and business news outlets

### 📊 **Advanced Analytics**
- **Source Distribution**: Visual charts showing news source coverage
- **Timeline Analysis**: Track news trends over time
- **Research Metrics**: Comprehensive analytics dashboard
- **Export Options**: Download reports in multiple formats

### 🎯 **Professional UI/UX**
- **Clean Interface**: Modern, responsive design optimized for research
- **Tabbed Navigation**: Organized display of analysis, articles, and analytics
- **Real-time Updates**: Progress indicators and live status updates
- **Mobile Friendly**: Works seamlessly across devices

## 📁 Project Structure

```
news-research-tool/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings and constants
├── news_analyzer.py      # API clients and analysis functions
├── ui_components.py      # UI components and display functions
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection for API access

### 1. Clone Repository
```bash
git clone <repository-url>
cd news-research-tool
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get API Keys

#### **Groq API Key (Free)**
1. Visit [groq.com](https://groq.com)
2. Sign up for a free account
3. Navigate to API Keys section  
4. Create a new API key
5. Copy the key (starts with `gsk_`)

#### **NewsAPI Key (Free)**
1. Go to [newsapi.org](https://newsapi.org)
2. Register for a free developer account
3. Get your API key from the dashboard
4. Free tier includes 1,000 requests/month

### 4. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🎯 Usage Guide

### Basic Usage

1. **Enter API Keys**: Input your Groq and NewsAPI keys in the sidebar
2. **Configure Settings**: Choose AI model, date range, and article limits
3. **Search**: Enter your research query (e.g., "Tesla earnings", "Apple stock")
4. **Analyze**: Review AI summary, browse articles, and check analytics
5. **Export**: Download reports for offline analysis

### Advanced Features

#### **Query Examples**
- **Company Analysis**: `Tesla Q4 earnings report`
- **Industry Research**: `semiconductor shortage impact`
- **Market Trends**: `cryptocurrency adoption news`
- **Comparative Analysis**: `Tesla vs Ford EV sales`

#### **AI Model Selection**
- **openai/gpt-oss-120b**: Fast processing, good for quick analysis
- **llama-3.1-8b-instant**: Detailed analysis, best for comprehensive research
- **moonshotai/kimi-k2-instruct-0905**: Balanced performance and quality
- **mixtral-8x7b-32768**: Efficient processing with good results

#### **Research Settings**
- **Date Range**: 1-30 days (adjust based on research needs)
- **Article Limit**: 5-50 articles (more articles = deeper analysis)
- **Source Filtering**: Focus on specific news sources
- **Sorting Options**: By relevance, date, or source

## 📊 Features Deep Dive

### AI Analysis Tab
- **Executive Summary**: Key developments and market sentiment
- **Market Implications**: Investment impact and price expectations  
- **Risk Assessment**: Potential risks and opportunities
- **Investment Recommendations**: Buy/Hold/Sell signals with reasoning

### News Articles Tab
- **Card-based Display**: Clean, organized article presentation
- **Source Information**: Publisher, author, and publication date
- **Direct Links**: Access to full articles
- **Image Support**: Article thumbnails when available

### Analytics Dashboard
- **Source Distribution**: Bar charts showing news source coverage
- **Research Metrics**: Article counts, source diversity, date ranges
- **Historical Data**: Track previous research queries
- **Export Options**: Download data in various formats

## 🔧 Configuration

### API Rate Limits
- **Groq API**: Varies by model and plan
- **NewsAPI**: 1,000 requests/month (free tier)

### Customization Options
- **UI Themes**: Modify `CUSTOM_CSS` in `config.py`
- **Default Settings**: Adjust `DEFAULT_SETTINGS` in `config.py`
- **Prompt Templates**: Customize `ANALYSIS_PROMPT_TEMPLATE`

## 🚨 Important Notes

### Limitations
- **API Dependencies**: Requires active internet connection
- **Rate Limits**: Free tiers have usage restrictions
- **Data Privacy**: No user data is stored locally
- **Language**: Currently supports English news only

### Disclaimers
- **Not Financial Advice**: Tool provides research analysis only
- **AI Limitations**: Analysis quality depends on source data
- **Source Reliability**: Always verify critical information
- **Investment Risk**: Past performance doesn't predict future results

## 🛡️ Security & Privacy

### Data Handling
- **No Storage**: API keys and queries are not stored
- **Secure Transmission**: All API calls use HTTPS
- **Privacy First**: No user tracking or analytics
- **Local Processing**: All data processing happens in your browser

### Best Practices
- **API Key Security**: Never share or commit API keys
- **Regular Updates**: Keep dependencies updated
- **Backup Keys**: Store API keys securely
- **Monitor Usage**: Track API usage to avoid limits

## 🤝 Contributing

### Development Setup
```bash
# Fork the repository
# Clone your fork
git clone <your-fork-url>

# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git commit -m "Add your feature"

# Push and create pull request
git push origin feature/your-feature
```

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Include error handling
- Write clear variable names

## 📈 Roadmap

### Upcoming Features
- [ ] **PDF Export**: Export reports as formatted PDF documents
- [ ] **Email Integration**: Send reports via email
- [ ] **Scheduled Research**: Automated periodic research
- [ ] **Portfolio Tracking**: Track multiple stocks/companies
- [ ] **Advanced Charts**: Interactive financial charts
- [ ] **Sentiment Scoring**: Numerical sentiment analysis
- [ ] **News Alerts**: Real-time notifications for keywords
- [ ] **API Integration**: Support for more data sources

### Performance Improvements
- [ ] **Caching System**: Cache API responses for faster access
- [ ] **Async Processing**: Parallel API calls for better speed
- [ ] **Database Integration**: Store research history
- [ ] **Mobile App**: Native mobile application

## 🐛 Troubleshooting

### Common Issues

**"Invalid API Key Error"**
- Verify API key format and validity
- Check for extra spaces or characters
- Ensure API key has proper permissions

**"Rate Limited"** 
- Wait before making new requests
- Consider upgrading API plans
- Optimize query frequency

**"No Articles Found"**
- Try broader or different keywords
- Adjust date range settings
- Check NewsAPI service status

**"Connection Error"**
- Verify internet connection
- Check firewall settings
- Try different network if needed

### Getting Help
- Check the troubleshooting guide in the app
- Review API documentation for rate limits
- Open an issue on GitHub for bugs
- Contact support for API-related issues

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq**: For providing advanced AI models
- **NewsAPI**: For comprehensive news data access
- **Streamlit**: For the excellent web framework
- **Open Source Community**: For inspiration and resources

## 📞 Support

### Documentation
- **In-app Help**: Comprehensive guide within the application
- **API Documentation**: [Groq Docs](https://docs.groq.com) | [NewsAPI Docs](https://newsapi.org/docs)

### Contact
- **Issues**: Open a GitHub issue for bugs or feature requests
- **Questions**: Use GitHub Discussions for general questions
- **Security**: Email security concerns privately

---

**⚡ Built with cutting-edge AI for modern equity research**

*Disclaimer: This tool is for research purposes only and does not constitute financial advice. Always consult with qualified financial advisors before making investment decisions.*#   N e w s - R e s e a r c h - T o o l 
 
 

