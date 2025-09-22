"""UI components and display functions"""

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

def render_sidebar_config():
    """Render sidebar configuration panel"""
    st.sidebar.markdown('<h3 class="sidebar-header">🔑 API Configuration</h3>', unsafe_allow_html=True)
    
    # API Keys input
    groq_api_key = st.sidebar.text_input(
        "Groq API Key", 
        type="password", 
        help="Get your free API key from groq.com",
        placeholder="gsk_..."
    )
    
    news_api_key = st.sidebar.text_input(
        "NewsAPI Key", 
        type="password", 
        help="Get your free API key from newsapi.org",
        placeholder="Enter your NewsAPI key"
    )
    
    st.sidebar.markdown("---")
    
    # Settings
    st.sidebar.markdown('<h3 class="sidebar-header">⚙️ Analysis Settings</h3>', unsafe_allow_html=True)
    
    model_choice = st.sidebar.selectbox(
        "🤖 AI Model",
        ["openai/gpt-oss-120b", "llama-3.1-8b-instant", "moonshotai/kimi-k2-instruct-0905", "whisper-large-v3-turbo", "mixtral-8x7b-32768", "gemma2-9b-it"],
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
    
    # Advanced settings in expander
    with st.sidebar.expander("🔧 Advanced Settings"):
        show_source_images = st.checkbox("Show article images", value=True)
        show_article_authors = st.checkbox("Show article authors", value=False)
        enable_sentiment_analysis = st.checkbox("Enhanced sentiment analysis", value=True)
    
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

        # Use session state for default value
        query = st.text_input(
            "Research Query",
            value=st.session_state.get("selected_query", ""),
            placeholder="e.g., Tesla earnings Q4, Apple stock analysis, Bitcoin price prediction",
            help="Enter keywords, company names, stock symbols, or industry terms"
        )

        # Quick search suggestions
        st.markdown("**💡 Quick Suggestions:**")
        col_a, col_b, col_c = st.columns(3)

        if col_a.button("📈 Tesla Stock"):
            st.session_state["selected_query"] = "Tesla stock price analysis"

        if col_b.button("🍎 Apple Earnings"):
            st.session_state["selected_query"] = "Apple quarterly earnings report"

        if col_c.button("₿ Crypto Market"):
            st.session_state["selected_query"] = "cryptocurrency market trends"

    with col2:
        st.subheader("📊 Actions")
        search_btn = st.button("🚀 Start Research", type="primary", use_container_width=True)
        clear_btn = st.button("🗑️ Clear All", use_container_width=True)

        if clear_btn:
            st.session_state["selected_query"] = ""  # Clear query

        st.markdown("---")
        st.markdown("**Status:** Ready to search")

    # Final query comes from session state or text input
    final_query = st.session_state.get("selected_query", query)

    return final_query, search_btn, clear_btn

def display_news_card(article_data: Dict, settings: Dict):
    """Display individual news article """
    
    title = article_data.get('title', 'No title available')
    description = article_data.get('description', 'No description available')
    source = article_data.get('source', 'Unknown Source')
    author = article_data.get('author', 'Unknown author')
    
    with st.container():
        if settings.get('show_source_images') and article_data.get('url_to_image'):
            col_image, col_text = st.columns([1, 2])
            
            with col_image:
                try:
                    st.image(
                        article_data['url_to_image'], 
                        caption=f"Source: {source}",
                        use_column_width=True
                    )
                except Exception:
                    st.markdown("""
                    <div style="background-color: #f0f0f0; padding: 2rem; text-align: center; 
                                border-radius: 8px; color: #666;">
                        📰<br>No Image<br>Available
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_text:
                st.markdown(f"""
                <div style="background-color: #e3f2fd; color: #1976d2; padding: 0.3rem 0.6rem; 
                            border-radius: 12px; font-size: 0.8rem; font-weight: bold; 
                            display: inline-block; margin-bottom: 0.5rem;">
                    Article #{article_data['index'] + 1}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"### {title}")
                st.markdown(f"""
                <div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">
                    📰 <strong>{source}</strong> | 📅 {article_data['published_at']}
                    {f" | ✍️ {author}" if settings.get('show_article_authors') and author != 'Unknown author' else ""}
                </div>
                """, unsafe_allow_html=True)
                st.write(description)
        else:
            st.markdown(f"""
            <div style="background-color: #e3f2fd; color: #1976d2; padding: 0.3rem 0.6rem; 
                        border-radius: 12px; font-size: 0.8rem; font-weight: bold; 
                        display: inline-block; margin-bottom: 0.5rem;">
                Article #{article_data['index'] + 1}
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"### {title}")
            st.markdown(f"""
            <div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">
                📰 <strong>{source}</strong> | 📅 {article_data['published_at']}
                {f" | ✍️ {author}" if settings.get('show_article_authors') and author != 'Unknown author' else ""}
            </div>
            """, unsafe_allow_html=True)
            st.write(description)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if article_data.get('url'):
                st.markdown(f"[🔗 Read Full Article]({article_data['url']})")
        
        with col2:
            if st.button(f"📋 Copy Title", key=f"copy_{article_data['index']}", use_container_width=True):
                st.code(title, language=None)
                st.success("✅ Title displayed above - select and copy!")
        
        with col3:
            if st.button("⭐", key=f"fav_{article_data['index']}", help="Save to favorites", use_container_width=True):
                st.success("✅ Saved!")
        
        st.markdown("<br>", unsafe_allow_html=True)


def display_ai_summary(summary: str, query: str, metadata: Dict, settings: Dict):
    """Display AI-generated summary with header and content"""
    
    st.subheader("🤖 AI-Generated Market Analysis")
    
    # Create one unified block with header and content
    with st.container():
        # Header with gradient background
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1.5rem; text-align: center; 
                    border-radius: 15px 15px 0 0; margin: 0; 
                    box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
            <h3 style="margin: 0; color: white; font-size: 2.4rem;text-transform: uppercase;">📊 Analysis for: "{query}"</h3>
        </div>
        """, unsafe_allow_html=True)
        
       
        
        # Display the AI summary content
        st.markdown(summary)
        
        # Close the content container
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Analysis metadata with colored backgrounds
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF6B6B, #FF8E53); color: white; 
                    padding: 1.5rem; border-radius: 12px; text-align: center; 
                    box-shadow: 0 4px 15px rgba(255,107,107,0.3); margin: 1.5rem;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">📰</div>
            <div style="font-size: 1.8rem; font-weight: bold;">{metadata.get('total_articles', 'N/A')}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Articles</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4ECDC4, #44A08D); color: white; 
                    padding: 1.5rem; border-radius: 12px; text-align: center; 
                    box-shadow: 0 4px 15px rgba(78,205,196,0.3); margin: 1.5rem;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">🏢</div>
            <div style="font-size: 1.8rem; font-weight: bold;">{metadata.get('unique_sources', 'N/A')}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Sources</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        date_range = metadata.get('date_range', {})
        span_text = f"{date_range.get('span_days', 'N/A')} days" if date_range else "N/A"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #A8E6CF, #7FCDCD); color: white; 
                    padding: 1.5rem; border-radius: 12px; text-align: center; 
                    box-shadow: 0 4px 15px rgba(168,230,207,0.3); margin: 1.5rem;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">📅</div>
            <div style="font-size: 1.8rem; font-weight: bold;">{span_text.split()[0]}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">{"days" if "days" in span_text else "Time Span"}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        timestamp = datetime.now().strftime("%H:%M")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFB6C1, #FFA07A); color: white; 
                    padding: 1.5rem; border-radius: 12px; text-align: center; 
                    box-shadow: 0 4px 15px rgba(255,182,193,0.3); margin: 1.5rem;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">⏰</div>
            <div style="font-size: 1.8rem; font-weight: bold;">{timestamp}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Generated</div>
        </div>
        """, unsafe_allow_html=True)

def format_summary_text(summary: str) -> str:
    """ the AI summary text """
    
    # Split summary into lines and process
    lines = summary.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Format different types of content
        if line.startswith('**') and line.endswith('**'):
            # Main headers
            clean_line = line.replace('**', '')
            formatted_lines.append(f'<h3 style="color: #1f77b4; margin-top: 1.5rem; margin-bottom: 0.5rem;">{clean_line}</h3>')
            
        elif line.startswith('*') and line.endswith('*'):
            # Sub headers
            clean_line = line.replace('*', '')
            formatted_lines.append(f'<h4 style="color: #333; margin-top: 1rem; margin-bottom: 0.5rem;">{clean_line}</h4>')
            
        elif line.startswith('•') or line.startswith('-'):
            # Bullet points
            clean_line = line[1:].strip()
            formatted_lines.append(f'<li style="margin-bottom: 0.5rem; line-height: 1.6;">{clean_line}</li>')
            
        elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.'):
            # Numbered lists
            formatted_lines.append(f'<li style="margin-bottom: 0.5rem; line-height: 1.6;">{line}</li>')
            
        elif '|' in line and len(line.split('|')) >= 3:
            #  content
            parts = [part.strip() for part in line.split('|') if part.strip()]
            if len(parts) >= 3:
                formatted_lines.append(f'''
                <div style="background-color: #e3f2fd; padding: 1rem; margin: 0.5rem 0; 
                           border-radius: 8px; border-left: 4px solid #1976d2;">
                    <strong>{parts[0]}</strong><br>
                    <span style="color: #666;">{" | ".join(parts[1:])}</span>
                </div>
                ''')
            else:
                formatted_lines.append(f'<p style="margin-bottom: 1rem; line-height: 1.6;">{line}</p>')
        else:
            # Regular paragraphs
            if len(line) > 10:  # Avoid formatting very short lines
                formatted_lines.append(f'<p style="margin-bottom: 1rem; line-height: 1.6;">{line}</p>')
    
    # Join all  content
    formatted_content = '\n'.join(formatted_lines)
    
    # Wrap bullet points in proper lists
    formatted_content = formatted_content.replace('<li', '<ul><li').replace('</li>\n<p', '</li></ul>\n<p')
    formatted_content = formatted_content.replace('</li>\n<h', '</li></ul>\n<h')
    
    return formatted_content

def display_analytics_dashboard(metadata: Dict, articles: List[Dict]):
    """Display comprehensive analytics dashboard"""
    
    st.subheader("📊 Research Analytics Dashboard")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📰 Total Articles",
            value=metadata.get('total_articles', 0)
        )
    
    with col2:
        st.metric(
            label="🏢 Unique Sources", 
            value=metadata.get('unique_sources', 0)
        )
    
    with col3:
        date_range = metadata.get('date_range', {})
        if date_range:
            st.metric(
                label="📅 Date Range",
                value=f"{date_range.get('span_days', 0)} days"
            )
    
    with col4:
        avg_per_day = 0
        if date_range.get('span_days', 0) > 0:
            avg_per_day = round(metadata.get('total_articles', 0) / date_range['span_days'], 1)
        st.metric(
            label="📈 Avg/Day",
            value=avg_per_day
        )
    
    # Source distribution chart
    if metadata.get('source_distribution'):
        st.subheader("📊 Sources Distribution")
        source_data = metadata['source_distribution']
        
        # Limit to top 10 sources for better visualization
        top_sources = dict(sorted(source_data.items(), key=lambda x: x[1], reverse=True)[:10])
        
        st.bar_chart(top_sources)
        
        # Source details table
        st.subheader("📋 Source Details")
        source_details = []
        for source, count in sorted(source_data.items(), key=lambda x: x[1], reverse=True):
            percentage = round((count / metadata['total_articles']) * 100, 1)
            source_details.append({
                'Source': source,
                'Articles': count,
                'Percentage': f"{percentage}%"
            })
        
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
    
    # Quick stats
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
    
    # Main footer
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
        
        **Step 1: Get Your API Keys**
        - **Groq API**: Visit [groq.com](https://groq.com) → Sign up → Get free API key
        - **NewsAPI**: Visit [newsapi.org](https://newsapi.org) → Register → Get free API key
        
        **Step 2: Configure Settings**
        - Enter both API keys in the sidebar
        - Choose your preferred AI model
        - Set date range and article limits
        
        **Step 3: Start Research**
        - Enter your query (company name, stock symbol, industry term)
        - Click "Start Research" to begin analysis
        - Review AI summary, browse articles, and check analytics
        
        ### 🎯 Best Practices:
        
        **Effective Queries:**
        - Use specific company names: "Tesla", "Apple Inc"
        - Include relevant terms: "earnings", "stock price", "merger"
        - Try industry keywords: "semiconductor", "renewable energy"
        
        **Query Examples:**
        - `Tesla Q4 earnings report`
        - `Apple iPhone sales decline`
        - `Microsoft Azure cloud growth`
        - `Bitcoin ETF approval news`
        
        ### 🔧 Features Overview:
        
        **🤖 AI Analysis Tab:**
        - Comprehensive market analysis
        - Investment recommendations
        - Risk assessment
        - Sentiment analysis
        
        **📰 News Articles Tab:**
        - Real-time article feed
        - Source credibility
        - Direct links to full articles
        - Article metadata
        
        **📊 Analytics Tab:**
        - Source distribution charts
        - Timeline analysis
        - Research metrics
        - Data export options
        """)

def create_shareable_link(query: str, timestamp: str) -> str:
    """Create a shareable link for the analysis"""
    import urllib.parse
    
    # Create a URL-encoded query parameter
    encoded_query = urllib.parse.quote(query)
    base_url = "https://your-app-domain.com"  # Replace with actual domain
    
    return f"{base_url}?query={encoded_query}&timestamp={timestamp}"

def format_for_social_media(query: str, summary: str, metadata: dict) -> str:
    """Format analysis for social media sharing"""
    
    summary_preview = summary[:200] + "..." if len(summary) > 200 else summary
    
    social_content = f"""🚀 Market Research Alert: {query}

📊 AI Analysis Summary:
{summary_preview}

📈 Quick Stats:
• {metadata.get('total_articles', 'N/A')} articles analyzed
• {metadata.get('unique_sources', 'N/A')} news sources
• {metadata.get('date_range', {}).get('span_days', 'N/A')} days coverage

#MarketResearch #AI #NewsAnalysis #Investment
Generated by AI News Research Tool
"""
    
    return social_content

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