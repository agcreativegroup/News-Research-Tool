# app.py
"""
News Research Tool - Main Application
AI-Powered Equity Research Assistant using Groq and NewsAPI
"""

import streamlit as st
from datetime import datetime
import time

# Import custom modules
from config import APP_CONFIG
from news_analyzer import GroqAnalyzer, NewsAPIClient, NewsProcessor, create_download_content, validate_api_keys
from ui_components import (
    load_custom_css, render_header, render_sidebar_config, render_search_interface,
    display_news_card, display_ai_summary, display_analytics_dashboard,
    display_error_message, display_success_message, render_footer, render_help_section,
    create_download_button
)

def initialize_app():
    """Initialize the Streamlit app with configuration"""
    st.set_page_config(
        page_title=APP_CONFIG["page_title"],
        page_icon=APP_CONFIG["page_icon"],
        layout=APP_CONFIG["layout"],
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    if 'research_history' not in st.session_state:
        st.session_state.research_history = []
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None

def main():
    """Main application function"""
    
    # Initialize app
    initialize_app()
    
    # Render header
    render_header()
    
    # Render sidebar configuration
    config = render_sidebar_config()
    
    # Render search interface
    query, search_btn, clear_btn = render_search_interface()
    
    # Handle clear button
    if clear_btn:
        st.session_state.current_analysis = None
        st.rerun()
    
    # Validate inputs before processing
    if search_btn:
        # Validate API keys
        if not config['groq_api_key']:
            display_error_message("no_groq_key")
            return
        
        if not config['news_api_key']:
            display_error_message("no_news_key")
            return
        
        if not query:
            display_error_message("no_query")
            return
        
        # Validate API key formats
        keys_valid, key_errors = validate_api_keys(config['groq_api_key'], config['news_api_key'])
        if not keys_valid:
            for error in key_errors:
                st.error(f"❌ {error}")
            return
        
        # Process the research request
        process_research_request(query, config)
    
    # Display results if available
    if st.session_state.current_analysis:
        display_research_results(st.session_state.current_analysis, config)
    
    # Render help section
    render_help_section()
    
    # Render footer
    render_footer()

def process_research_request(query: str, config: dict):
    """Process the research request and fetch/analyze news"""
    
    try:
        # Initialize API clients
        news_client = NewsAPIClient(config['news_api_key'])
        groq_analyzer = GroqAnalyzer(config['groq_api_key'])
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Fetch news articles
        status_text.text("🔍 Fetching latest news articles...")
        progress_bar.progress(25)
        
        news_data = news_client.fetch_articles(
            query=query,
            days_back=config['days_back'],
            page_size=config['max_articles']
        )
        
        if "error" in news_data:
            display_error_message("api_error", news_data["error"])
            progress_bar.empty()
            status_text.empty()
            return
        
        articles = news_data.get('articles', [])
        
        if not articles:
            display_error_message("no_articles")
            progress_bar.empty()
            status_text.empty()
            return
        
        # Step 2: Validate and process articles
        status_text.text("📊 Processing articles...")
        progress_bar.progress(50)
        
        valid_articles, warnings = NewsProcessor.validate_articles(articles)
        
        if warnings:
            st.warning(f"⚠️ Found {len(warnings)} articles with missing information")
        
        # Step 3: Prepare content for analysis
        status_text.text("🤖 Preparing AI analysis...")
        progress_bar.progress(75)
        
        news_content = NewsProcessor.prepare_content_for_analysis(
            valid_articles, 
            max_articles=min(10, len(valid_articles))
        )
        
        # Step 4: Generate AI summary
        status_text.text("🧠 Generating intelligent summary...")
        progress_bar.progress(90)
        
        summary = groq_analyzer.generate_summary(
            query=query,
            news_content=news_content,
            model=config['model_choice']
        )
        
        # Step 5: Extract metadata
        status_text.text("📈 Finalizing analysis...")
        progress_bar.progress(100)
        
        metadata = NewsProcessor.extract_article_metadata(valid_articles)
        
        # Format articles for display
        formatted_articles = [
            NewsProcessor.format_article_for_display(article, i) 
            for i, article in enumerate(valid_articles)
        ]
        
        # Store results in session state
        st.session_state.current_analysis = {
            'query': query,
            'summary': summary,
            'articles': formatted_articles,
            'metadata': metadata,
            'timestamp': datetime.now(),
            'config': config.copy()
        }
        
        # Add to research history
        st.session_state.research_history.append({
            'query': query,
            'timestamp': datetime.now(),
            'article_count': len(valid_articles)
        })
        
        # Clean up progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Show success message
        display_success_message("articles_fetched", str(len(valid_articles)))
        
        # Automatically scroll to results
        time.sleep(0.5)  # Small delay for better UX
        
    except Exception as e:
        display_error_message("general_error", str(e))
        st.session_state.current_analysis = None

def display_research_results(analysis_data: dict, config: dict):
    """Display the research results in tabs"""
    
    st.markdown("---")
    st.subheader(f"🎯 Research Results for: '{analysis_data['query']}'")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Analysis", "📰 News Articles", "📊 Analytics", "📋 Export"])
    
    with tab1:
        # Display AI summary
        display_ai_summary(
            summary=analysis_data['summary'],
            query=analysis_data['query'],
            metadata=analysis_data['metadata'],
            settings=config
        )
        
        # Quick action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Regenerate Analysis", key="regen"):
                st.info("Regenerating analysis with same data...")
                # Could implement re-analysis with different model
        
        with col2:
            if st.button("📤 Share Analysis", key="share"):
                st.success("Analysis URL copied to clipboard! (Feature coming soon)")
        
        with col3:
            if st.button("⭐ Save to Favorites", key="fav"):
                st.success("Analysis saved to favorites! (Feature coming soon)")
    
    with tab2:
        st.subheader(f"📰 News Articles ({len(analysis_data['articles'])} found)")
        
        # Sorting options
        sort_col1, sort_col2, sort_col3 = st.columns(3)
        
        with sort_col1:
            sort_by = st.selectbox(
                "Sort by:", 
                ["Relevance", "Date", "Source"],
                key="sort_articles"
            )
        
        with sort_col2:
            filter_source = st.selectbox(
                "Filter by source:",
                ["All Sources"] + analysis_data['metadata'].get('sources_list', []),
                key="filter_source"
            )
        
        with sort_col3:
            articles_per_page = st.selectbox(
                "Articles per page:",
                [5, 10, 15, 20, "All"],
                index=1,
                key="articles_per_page"
            )
        
        # Apply filters and sorting
        filtered_articles = analysis_data['articles'].copy()
        
        if filter_source != "All Sources":
            filtered_articles = [
                article for article in filtered_articles 
                if article['source'] == filter_source
            ]
        
        # Sort articles
        if sort_by == "Date":
            filtered_articles.sort(key=lambda x: x['published_at'], reverse=True)
        elif sort_by == "Source":
            filtered_articles.sort(key=lambda x: x['source'])
        
        # Pagination
        if articles_per_page != "All":
            articles_to_show = filtered_articles[:articles_per_page]
        else:
            articles_to_show = filtered_articles
        
        # Display articles
        if not articles_to_show:
            st.info("No articles match the current filters.")
        else:
            for article in articles_to_show:
                display_news_card(article, config)
                st.markdown("---")
        
        # Show total count
        if len(filtered_articles) != len(analysis_data['articles']):
            st.info(f"Showing {len(articles_to_show)} of {len(filtered_articles)} filtered articles "
                   f"(total: {len(analysis_data['articles'])})")
    
    with tab3:
        # Display comprehensive analytics
        display_analytics_dashboard(analysis_data['metadata'], analysis_data['articles'])
        
        # Research history
        if len(st.session_state.research_history) > 1:
            st.subheader("📜 Research History")
            
            history_data = []
            for item in reversed(st.session_state.research_history[-10:]):  # Last 10 searches
                history_data.append({
                    'Query': item['query'],
                    'Articles': item['article_count'],
                    'Time': item['timestamp'].strftime('%H:%M:%S'),
                    'Date': item['timestamp'].strftime('%Y-%m-%d')
                })
            
            st.dataframe(history_data, use_container_width=True)
    
    with tab4:
        st.subheader("📋 Export & Download Options")
        
        # Generate download content
        download_content = create_download_content(
            summary=analysis_data['summary'],
            query=analysis_data['query'],
            metadata=analysis_data['metadata']
        )
        
        # Create filename
        safe_query = analysis_data['query'].replace(' ', '_').replace('/', '_')
        timestamp = analysis_data['timestamp'].strftime('%Y%m%d_%H%M%S')
        filename = f"research_report_{safe_query}_{timestamp}.txt"
        
        # Download button
        create_download_button(download_content, filename)
        
        st.markdown("---")
        
        # Export options 
        st.subheader("📊 Export Formats")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # PDF Export (using reportlab or weasyprint alternative)
            pdf_content = create_pdf_content(
                summary=analysis_data['summary'],
                query=analysis_data['query'],
                metadata=analysis_data['metadata'],
                articles=analysis_data['articles'][:5]  # Include top 5 articles
            )
            
            st.download_button(
                label="📄 Export as PDF",
                data=pdf_content,
                file_name=f"research_report_{safe_query}_{timestamp}.html",
                mime="text/html",
                help="Download as HTML file (can be converted to PDF)",
                use_container_width=True
            )
        
        with col2:
            # CSV Export
            csv_content = create_csv_content(analysis_data['articles'], analysis_data['metadata'])
            
            st.download_button(
                label="📊 Export to CSV",
                data=csv_content,
                file_name=f"articles_data_{safe_query}_{timestamp}.csv",
                mime="text/csv",
                help="Download articles data as CSV file",
                use_container_width=True
            )
        
        with col3:
            # Email functionality
            if st.button("📧 Email Report", use_container_width=True):
                email_content = create_email_template(
                    summary=analysis_data['summary'],
                    query=analysis_data['query'],
                    metadata=analysis_data['metadata']
                )
                
                # Show email content in expandable section
                with st.expander("📧 Email Content Preview"):
                    st.text_area(
                        "Email Subject:",
                        value=f"Market Research Report: {analysis_data['query']}",
                        height=50
                    )
                    st.text_area(
                        "Email Body:",
                        value=email_content,
                        height=300
                    )
                    st.info("Copy the content above to send via your email client")
        
        # Advanced export options
        with st.expander("🔧 Advanced Export Options"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                # JSON Export
                import json
                json_data = {
                    'query': analysis_data['query'],
                    'summary': analysis_data['summary'],
                    'articles': analysis_data['articles'],
                    'metadata': analysis_data['metadata'],
                    'timestamp': analysis_data['timestamp'].isoformat(),
                    'config': {k: v for k, v in analysis_data['config'].items() if k not in ['groq_api_key', 'news_api_key']}
                }
                
                json_content = json.dumps(json_data, indent=2, default=str)
                
                st.download_button(
                    label="📋 Export as JSON",
                    data=json_content,
                    file_name=f"research_data_{safe_query}_{timestamp}.json",
                    mime="application/json",
                    help="Download complete research data as JSON",
                    use_container_width=True
                )
            
            with col_b:
                # Summary-only export
                summary_content = f"""
MARKET RESEARCH SUMMARY
Query: {analysis_data['query']}
Generated: {analysis_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}

{analysis_data['summary']}

---
Articles Analyzed: {len(analysis_data['articles'])}
Sources: {analysis_data['metadata'].get('unique_sources', 'N/A')}
Model Used: {analysis_data['config']['model_choice']}
                """
                
                st.download_button(
                    label="📝 Summary Only",
                    data=summary_content,
                    file_name=f"summary_{safe_query}_{timestamp}.txt",
                    mime="text/plain",
                    help="Download AI summary only",
                    use_container_width=True
                )
        
        # Raw data preview
        with st.expander("🔍 Raw Data Preview"):
            st.json({
                'query': analysis_data['query'],
                'article_count': len(analysis_data['articles']),
                'sources': len(analysis_data['metadata'].get('sources_list', [])),
                'timestamp': analysis_data['timestamp'].isoformat(),
                'model_used': analysis_data['config']['model_choice']
            })

def create_pdf_content(summary: str, query: str, metadata: dict, articles: list) -> str:
    """Create HTML content that can be saved as PDF"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Market Research Report: {query}</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 2rem; text-align: center; border-radius: 10px; }}
            .content {{ background: #f9f9f9; padding: 2rem; margin-top: 2rem; border-radius: 10px; }}
            .article {{ border-bottom: 1px solid #ddd; padding: 1rem 0; }}
            .metrics {{ display: flex; justify-content: space-around; margin: 2rem 0; }}
            .metric {{ text-align: center; background: #e3f2fd; padding: 1rem; border-radius: 8px; }}
            h1, h2, h3 {{ color: #333; }}
            .footer {{ text-align: center; margin-top: 3rem; color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Market Research Report</h1>
            <h2>Query: "{query}"</h2>
            <p>Generated: {timestamp}</p>
        </div>
        
        <div class="content">
            <h2>🤖 AI Analysis Summary</h2>
            <div>{summary.replace('\n', '<br>')}</div>
            
            <div class="metrics">
                <div class="metric">
                    <h3>{metadata.get('total_articles', 'N/A')}</h3>
                    <p>Articles</p>
                </div>
                <div class="metric">
                    <h3>{metadata.get('unique_sources', 'N/A')}</h3>
                    <p>Sources</p>
                </div>
                <div class="metric">
                    <h3>{metadata.get('date_range', {}).get('span_days', 'N/A')} days</h3>
                    <p>Time Span</p>
                </div>
            </div>
            
            <h2>📰 Key Articles</h2>
            {''.join([f'''
            <div class="article">
                <h3>{article.get('title', 'No Title')}</h3>
                <p><strong>Source:</strong> {article.get('source', 'Unknown')} | 
                   <strong>Date:</strong> {article.get('published_at', 'Unknown')}</p>
                <p>{article.get('description', 'No description available')}</p>
                {f'<p><a href="{article.get("url", "")}" target="_blank">Read Full Article</a></p>' if article.get('url') else ''}
            </div>
            ''' for article in articles])}
        </div>
        
        <div class="footer">
            <p>Generated by AI News Research Tool</p>
            <p>Powered by Groq AI & NewsAPI</p>
        </div>
    </body>
    </html>
    """
    
    return html_content

def create_csv_content(articles: list, metadata: dict) -> str:
    """Create CSV content with articles data"""
    
    import io
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow([
        'Article_Number',
        'Title',
        'Source',
        'Author',
        'Published_Date',
        'Description',
        'URL'
    ])
    
    # Write article data
    for i, article in enumerate(articles, 1):
        writer.writerow([
            i,
            article.get('title', '').replace('\n', ' ').replace('\r', ''),
            article.get('source', ''),
            article.get('author', ''),
            article.get('published_at', ''),
            article.get('description', '').replace('\n', ' ').replace('\r', ''),
            article.get('url', '')
        ])
    
    # Add summary row
    writer.writerow([])
    writer.writerow(['Summary Statistics'])
    writer.writerow(['Total Articles', len(articles)])
    writer.writerow(['Unique Sources', metadata.get('unique_sources', 'N/A')])
    writer.writerow(['Date Range (days)', metadata.get('date_range', {}).get('span_days', 'N/A')])
    
    return output.getvalue()

def create_email_template(summary: str, query: str, metadata: dict) -> str:
    """Create email template content"""
    
    timestamp = datetime.now().strftime('%B %d, %Y at %H:%M')
    
    email_content = f"""Dear Recipient,

Please find below the market research analysis for "{query}" generated on {timestamp}.

EXECUTIVE SUMMARY:
{summary[:500]}...

KEY METRICS:
• Articles Analyzed: {metadata.get('total_articles', 'N/A')}
• News Sources: {metadata.get('unique_sources', 'N/A')}
• Time Period: {metadata.get('date_range', {}).get('span_days', 'N/A')} days

This analysis was generated using advanced AI technology and multiple news sources to provide comprehensive market insights.

For the complete detailed report with all articles and charts, please refer to the attached files or contact me for the full analysis.

DISCLAIMER: This report is for informational purposes only and should not be considered as financial advice. Always consult with qualified financial advisors before making investment decisions.

Best regards,
AI News Research Tool
Powered by Groq AI & NewsAPI

---
Generated automatically by the AI News Research Tool
Visit our platform for real-time market analysis
"""
    
    return email_content

if __name__ == "__main__":
    main()