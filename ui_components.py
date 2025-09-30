"""UI components and display functions - API keys removed from UI"""

import streamlit as st
from typing import Dict, List
from datetime import datetime
from config import CUSTOM_CSS, ERROR_MESSAGES, SUCCESS_MESSAGES

def load_custom_css():
    """Load custom CSS styles"""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_header():
    """Render the main header"""
    st.markdown('<h1 class="main-header">📰 AI News Research Tool</h1>', unsafe_allow_html=True)
    st.markdown("### 🚀 Professional Equity Research Assistant")
    st.markdown("*Powered by Groq AI & NewsAPI for intelligent market analysis*")

# ============ SEARCH HISTORY FUNCTIONS ============

def initialize_search_history():
    """Initialize search history in session state"""
    if 'search_history' not in st.session_state:
        st.session_state['search_history'] = []

def add_to_search_history(query: str, results_count: int = 0):
    """Add a search query to history"""
    if not query or query.strip() == "":
        return
    
    initialize_search_history()
    
    history_entry = {
        'query': query.strip(),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'results_count': results_count,
        'date': datetime.now().strftime("%b %d, %Y"),
        'time': datetime.now().strftime("%I:%M %p")
    }
    
    # Remove duplicate if exists
    st.session_state['search_history'] = [
        h for h in st.session_state['search_history'] 
        if h['query'].lower() != query.lower()
    ]
    
    # Add to beginning
    st.session_state['search_history'].insert(0, history_entry)
    
    # Keep only last 20 searches
    st.session_state['search_history'] = st.session_state['search_history'][:20]

def clear_search_history():
    """Clear all search history"""
    st.session_state['search_history'] = []

def render_search_history_sidebar():
    """Render search history in sidebar"""
    initialize_search_history()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown('<h3 class="sidebar-header">🕐 Search History</h3>', unsafe_allow_html=True)
    
    history = st.session_state.get('search_history', [])
    
    if not history:
        st.sidebar.info("📝 No search history yet")
        return None
    
    st.sidebar.markdown(f"**Total Searches:** {len(history)}")
    
    if st.sidebar.button("🗑️ Clear History", use_container_width=True):
        clear_search_history()
        st.rerun()
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    selected_query = None
    
    for idx, item in enumerate(history[:10]):
        with st.sidebar.container():
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 50%); 
                        padding: 0.8rem; 
                        border-radius: 10px; 
                        margin-bottom: 0.8rem;
                        border-left: 4px solid #2196F3;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="color: #1565C0; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.3rem;">
                    🔍 {item['query'][:50]}{"..." if len(item['query']) > 50 else ""}
                </div>
                <div style="color: #666; font-size: 0.75rem;">
                    📅 {item['date']} • ⏰ {item['time']}
                    {f" • 📰 {item['results_count']} articles" if item['results_count'] > 0 else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.sidebar.columns([1, 1])
            
            with col1:
                if st.button("🔄 Search", key=f"history_search_{idx}", use_container_width=True):
                    selected_query = item['query']
            
            with col2:
                if st.button("❌", key=f"history_remove_{idx}", use_container_width=True):
                    st.session_state['search_history'].pop(idx)
                    st.rerun()
    
    if len(history) > 10:
        st.sidebar.markdown(f"*...and {len(history) - 10} more*")
    
    return selected_query

# ============ END SEARCH HISTORY FUNCTIONS ============

def render_sidebar_config():
    """Render sidebar configuration panel - NO API KEY INPUTS"""
    
    st.sidebar.markdown('<h3 class="sidebar-header">⚙️ Analysis Settings</h3>', unsafe_allow_html=True)
    
    model_choice = st.sidebar.selectbox(
        "🤖 AI Model",
        ["llama-3.1-8b-instant", "llama-3.1-70b-versatile", "mixtral-8x7b-32768", "gemma-7b-it"],
        help="Choose the AI model for analysis"
    )
    
    days_back = st.sidebar.slider(
        "📅 Days to look back", 
        1, 30, 7,
        help="How many days back to search for news"
    )
    
    max_articles = st.sidebar.slider(
        "📄 Max articles to analyze", 
        5, 50, 15,
        help="Maximum number of articles to fetch and analyze"
    )
    
    with st.sidebar.expander("🔧 Advanced Settings"):
        show_source_images = st.checkbox("Show article images", value=True)
        show_article_authors = st.checkbox("Show article authors", value=False)
        enable_sentiment_analysis = st.checkbox("Enhanced sentiment analysis", value=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown('<h3 class="sidebar-header">🔑 API Status</h3>', unsafe_allow_html=True)
    
    try:
        from api_config import GROQ_API_KEY, NEWS_API_KEY
        groq_status = "✅ Connected" if GROQ_API_KEY and len(GROQ_API_KEY) > 10 else "❌ Not configured"
        news_status = "✅ Connected" if NEWS_API_KEY and len(NEWS_API_KEY) > 10 else "❌ Not configured"
        
        st.sidebar.info(f"**Groq API:** {groq_status}")
        st.sidebar.info(f"**NewsAPI:** {news_status}")
        
        if "❌" in groq_status or "❌" in news_status:
            st.sidebar.warning("⚠️ Configure API keys in api_config.py")
    except ImportError:
        st.sidebar.error("❌ api_config.py not found")
        groq_api_key = ""
        news_api_key = ""
    else:
        groq_api_key = GROQ_API_KEY
        news_api_key = NEWS_API_KEY
    
    # Add search history to sidebar
    selected_from_history = render_search_history_sidebar()
    
    if selected_from_history:
        st.session_state["selected_query"] = selected_from_history
    
    return {
        'groq_api_key': groq_api_key,
        'news_api_key': news_api_key,
        'model_choice': model_choice,
        'days_back': days_back,
        'max_articles': max_articles,
        'show_source_images': show_source_images,
        'show_article_authors': show_article_authors,
        'enable_sentiment_analysis': enable_sentiment_analysis
    }

def render_search_interface():
    """Render the main search interface"""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("🔍 Enter Your Research Query")

        query = st.text_input(
            "Research Query",
            value=st.session_state.get("selected_query", ""),
            placeholder="e.g., Tesla earnings Q4, Apple stock analysis, Bitcoin price prediction",
            help="Enter keywords, company names, stock symbols, or industry terms"
        )

        st.markdown("**💡 Quick Suggestions:**")
        col_a, col_b, col_c = st.columns(3)

        if col_a.button("📈 Tesla Stock"):
            st.session_state["selected_query"] = "Tesla stock price analysis"
            st.rerun()

        if col_b.button("🍎 Apple Earnings"):
            st.session_state["selected_query"] = "Apple quarterly earnings report"
            st.rerun()

        if col_c.button("₿ Crypto Market"):
            st.session_state["selected_query"] = "cryptocurrency market trends"
            st.rerun()

    with col2:
        st.subheader("📊 Actions")
        search_btn = st.button("🚀 Start Research", type="primary", use_container_width=True)
        clear_btn = st.button("🗑️ Clear All", use_container_width=True)

        if clear_btn:
            st.session_state["selected_query"] = ""
            st.rerun()

        st.markdown("---")
        st.markdown("**Status:** Ready to search")

    final_query = st.session_state.get("selected_query", query)

    return final_query, search_btn, clear_btn

def render_news_section_header(total_articles: int):
    """Render header for news articles section"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); 
                color: white; padding: 1.5rem; text-align: center; 
                border-radius: 15px; margin: 1rem 0 2rem 0; 
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
        <h2 style="margin: 0; color: white; font-size: 2rem;">📰 News Articles ({total_articles} found)</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Latest articles from trusted sources</p>
    </div>
    """, unsafe_allow_html=True)

def display_news_card(article_data: Dict, settings: Dict):
    """Display news article in professional list view with clean expandable details"""
    
    title = article_data.get('title', 'No title available')
    description = article_data.get('description', 'No description available')
    source = article_data.get('source', 'Unknown Source')
    author = article_data.get('author', 'Unknown author')
    published_at = article_data.get('published_at', 'Date unavailable')
    
    # Create a concise 4-line summary in paragraph format
    summary_lines = []
    sentences = description.split('. ')
    
    for sentence in sentences[:4]:
        if sentence.strip() and len(sentence.strip()) > 20:
            clean_sentence = sentence.strip()
            if not clean_sentence.endswith('.'):
                clean_sentence += '.'
            summary_lines.append(clean_sentence)
            if len(summary_lines) == 4:
                break
    
    if len(summary_lines) < 4:
        words = description.split()
        chars_per_line = 80
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= chars_per_line:
                current_line += word + " "
            else:
                if current_line:
                    clean_line = current_line.strip()
                    if not clean_line.endswith('.'):
                        clean_line += '.'
                    summary_lines.append(clean_line)
                current_line = word + " "
                if len(summary_lines) == 4:
                    break
        
        if current_line and len(summary_lines) < 4:
            clean_line = current_line.strip()
            if not clean_line.endswith('.'):
                clean_line += '.'
            summary_lines.append(clean_line)
    
    summary_text = " ".join(summary_lines[:4])
    
    with st.container():
        col_num, col_headline = st.columns([0.5, 11.5])
        
        with col_num:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; 
                        padding: 0.8rem 0.6rem; 
                        border-radius: 10px; 
                        text-align: center; 
                        font-weight: 700; 
                        font-size: 1rem;
                        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);">
                {article_data['index'] + 1}
            </div>
            """, unsafe_allow_html=True)
        
        with col_headline:
            st.markdown(f"""
            <div style="background: white; 
                        padding: 1.2rem 1.8rem; 
                        border-radius: 12px; 
                        border-left: 5px solid #2196F3;
                        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
                        transition: all 0.3s ease;">
                <h3 style="margin: 0; 
                           color: #1565C0; 
                           font-size: 1.15rem; 
                           font-weight: 600;
                           line-height: 1.5;">
                    {title}
                </h3>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("📖 Read Summary & Details", expanded=False):
            
            col_source, col_date = st.columns([1, 1])
            
            with col_source:
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, #f5f7fa 0%, #c3cfe2 100%); 
                            padding: 0.8rem 1.2rem; 
                            border-radius: 8px;
                            border-left: 4px solid #1976D2;
                            display: inline-block;">
                    <span style="color: #1976D2; font-weight: 600; font-size: 0.95rem;">
                        📰 {source}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_date:
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, #f5f7fa 0%, #c3cfe2 100%); 
                            padding: 0.8rem 1.2rem; 
                            border-radius: 8px;
                            border-left: 4px solid #1976D2;
                            display: inline-block;">
                    <span style="color: #555; font-size: 0.9rem;">
                        📅 {published_at}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if settings.get('show_source_images') and article_data.get('url_to_image'):
                col_img, col_summary = st.columns([1.2, 2])
                
                with col_img:
                    try:
                        st.image(article_data['url_to_image'], use_column_width=True)
                        st.markdown(f"""
                        <div style="text-align: center; color: #666; font-size: 0.85rem; 
                                    margin-top: 0.5rem; font-style: italic;">
                            📸 {source}
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 100%); 
                                    padding: 4rem 1rem; text-align: center; border-radius: 12px; 
                                    border: 2px dashed #bdbdbd;">
                            <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">📰</div>
                            <div style="color: #999; font-size: 0.9rem;">Image Unavailable</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col_summary:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                                padding: 2rem; border-radius: 15px; border: 2px solid #2196F3;
                                box-shadow: 0 4px 20px rgba(33, 150, 243, 0.25); height: 100%;">
                        <h4 style="color: #1565C0; margin: 0 0 1.2rem 0; font-size: 1.2rem;
                                   font-weight: 700; display: flex; align-items: center; gap: 0.5rem;">
                            ✨  Summary
                        </h4>
                        <p style="font-size: 1rem; line-height: 1.8; color: #263238;
                                  margin: 0; text-align: justify;">
                            {summary_text}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                            padding: 2rem 2.5rem; border-radius: 15px; border: 2px solid #2196F3;
                            box-shadow: 0 4px 20px rgba(33, 150, 243, 0.25);">
                    <h4 style="color: #1565C0; margin: 0 0 1.2rem 0; font-size: 1.2rem;
                               font-weight: 700; display: flex; align-items: center; gap: 0.5rem;">
                        ✨ 4-Line Summary
                    </h4>
                    <p style="font-size: 1rem; line-height: 1.8; color: #263238;
                              margin: 0; text-align: justify;">
                        {summary_text}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if article_data.get('url'):
                    if st.button("🔗 Full Article", key=f"read_{article_data['index']}", 
                               use_container_width=True, type="primary"):
                        st.markdown(f'<meta http-equiv="refresh" content="0; url={article_data["url"]}">', 
                                  unsafe_allow_html=True)
                        st.info(f"Opening: {article_data['url']}")
            
            with col2:
                if st.button("📋 Copy", key=f"copy_{article_data['index']}", 
                           use_container_width=True, type="primary"):
                    st.code(title, language=None)
                    st.success("✅ Title copied!")
            
            with col3:
                if st.button("📤 Share", key=f"share_{article_data['index']}", 
                           use_container_width=True, type="primary"):
                    st.info(f"🔗 {article_data.get('url', 'N/A')}")
            
            with col4:
                if st.button("⭐ Save", key=f"fav_{article_data['index']}", 
                           use_container_width=True, type="primary"):
                    st.success("✅ Saved!")
        
        st.markdown("""
        <div style='margin: 1.2rem 0; height: 1px; 
                    background: linear-gradient(90deg, transparent 0%, #e0e0e0 20%, 
                                               #e0e0e0 80%, transparent 100%);'>
        </div>
        """, unsafe_allow_html=True)

def display_ai_summary(summary: str, query: str, metadata: Dict, settings: Dict):
    """Display AI-generated summary"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1.5rem; text-align: center; 
                border-radius: 15px; margin: 1rem 0 2rem 0; 
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
        <h2 style="margin: 0; color: white; font-size: 2rem;">🤖 AI-Generated Market Analysis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"### 📊 {query}")
    st.write(summary)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        articles_count = metadata.get('total_articles', 0)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF6B6B, #FF8E53); color: white; 
                    padding: 2rem; border-radius: 15px; text-align: center;margin-bottom: 1.5rem;
                    box-shadow: 0 4px 15px rgba(255,107,107,0.3);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📰</div>
            <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">{articles_count}</div>
            <div style="font-size: 1rem; opacity: 0.9;">Articles</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        sources_count = metadata.get('unique_sources', 0)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4ECDC4, #44A08D); color: white; 
                    padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 1.5rem;
                    box-shadow: 0 4px 15px rgba(78,205,196,0.3);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏢</div>
            <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">{sources_count}</div>
            <div style="font-size: 1rem; opacity: 0.9;">Sources</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        date_range = metadata.get('date_range', {})
        days_count = date_range.get('span_days', 0) if date_range else 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #A8E6CF, #7FCDCD); color: white; 
                    padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 1.5rem;
                    box-shadow: 0 4px 15px rgba(168,230,207,0.3);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📅</div>
            <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">{days_count}</div>
            <div style="font-size: 1rem; opacity: 0.9;">Days</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        time_now = datetime.now().strftime("%H:%M")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFB6C1, #FFA07A); color: white; 
                    padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 1.5rem;
                    box-shadow: 0 4px 15px rgba(255,182,193,0.3);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">⏰</div>
            <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">{time_now}</div>
            <div style="font-size: 1rem; opacity: 0.9;">Generated</div>
        </div>
        """, unsafe_allow_html=True)

def display_analytics_dashboard(metadata: Dict, articles: List[Dict]):
    """Display comprehensive analytics dashboard"""
    st.subheader("📊 Research Analytics Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="📰 Total Articles", value=metadata.get('total_articles', 0))
    
    with col2:
        st.metric(label="🏢 Unique Sources", value=metadata.get('unique_sources', 0))
    
    with col3:
        date_range = metadata.get('date_range', {})
        if date_range:
            st.metric(label="📅 Date Range", value=f"{date_range.get('span_days', 0)} days")
    
    with col4:
        avg_per_day = 0
        if date_range.get('span_days', 0) > 0:
            avg_per_day = round(metadata.get('total_articles', 0) / date_range['span_days'], 1)
        st.metric(label="📈 Avg/Day", value=avg_per_day)
    
    if metadata.get('source_distribution'):
        st.subheader("📊 Sources Distribution")
        source_data = metadata['source_distribution']
        top_sources = dict(sorted(source_data.items(), key=lambda x: x[1], reverse=True)[:10])
        st.bar_chart(top_sources)
        
        st.subheader("📋 Source Details")
        source_details = []
        for source, count in sorted(source_data.items(), key=lambda x: x[1], reverse=True):
            percentage = round((count / metadata['total_articles']) * 100, 1)
            source_details.append({'Source': source, 'Articles': count, 'Percentage': f"{percentage}%"})
        st.dataframe(source_details, use_container_width=True)

def display_error_message(error_type: str, details: str = ""):
    """Display formatted error messages"""
    if error_type in ERROR_MESSAGES:
        message = ERROR_MESSAGES[error_type].format(error=details) if details else ERROR_MESSAGES[error_type]
        st.error(message)
    else:
        st.error(f"❌ {error_type}: {details}")

def display_success_message(success_type: str, details: str = ""):
    """Display formatted success messages"""
    if success_type in SUCCESS_MESSAGES:
        message = SUCCESS_MESSAGES[success_type].format(count=details) if details else SUCCESS_MESSAGES[success_type]
        st.success(message)
    else:
        st.success(f"✅ {success_type}")

def render_footer():
    """Render the footer section"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🚀 Features:**")
        st.markdown("- AI-Powered Analysis\n- Real-time News\n- Multi-source Research")
    
    with col2:
        st.markdown("**⚡ Performance:**")
        st.markdown("- Fast Processing\n- Smart Caching\n- Reliable Sources")
    
    with col3:
        st.markdown("**🔒 Security:**")
        st.markdown("- Secure API Handling\n- No Data Storage\n- Privacy Protected")
    
    st.markdown("""
    <div class="footer-text">
        <p>🚀 <strong>News Research Tool</strong> - Powered by Groq AI & NewsAPI</p>
        <p>💡 Professional equity research made simple with artificial intelligence</p>
        <p>⚠️ <em>This tool provides analysis for research purposes only. Not financial advice.</em></p>
    </div>
    """, unsafe_allow_html=True)

def render_help_section():
    """Render help and instructions section"""
    with st.expander("📖 How to Use This Tool"):
        st.markdown("""
        ### 🚀 Getting Started:
        
        **Step 1: Configure API Keys**
        - Open `api_config.py` and add your API keys
        - Get Groq API key from [groq.com](https://groq.com)
        - Get NewsAPI key from [newsapi.org](https://newsapi.org)
        
        **Step 2: Start Research**
        - Enter your query (company name, stock symbol, industry term)
        - Click "Start Research" to begin analysis
        - View news articles first, then AI analysis
        
        ### 🎯 Query Examples:
        - `Tesla Q4 earnings report`
        - `Apple iPhone sales decline`
        - `Bitcoin ETF approval news`
        - `Microsoft AI developments`
        """)

def create_download_button(content: str, filename: str, mime_type: str = "text/plain"):
    """Create a download button with custom styling"""
    return st.download_button(
        label="💾 Download Analysis Report",
        data=content,
        file_name=filename,
        mime=mime_type,
        help="Download complete analysis as text file",
        use_container_width=True
    )
