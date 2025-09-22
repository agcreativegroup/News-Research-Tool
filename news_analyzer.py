# news_analyzer.py
"""News analysis and API interaction functions"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from config import GROQ_CONFIG, NEWSAPI_CONFIG, ANALYSIS_PROMPT_TEMPLATE

class GroqAnalyzer:
    """Handle Groq API interactions for news analysis"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = GROQ_CONFIG["api_url"]
        
    def generate_summary(self, query: str, news_content: str, model: str = None) -> str:
        """Generate AI summary using Groq API"""
        try:
            model = model or GROQ_CONFIG["default_model"]
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = ANALYSIS_PROMPT_TEMPLATE.format(
                query=query,
                news_content=news_content
            )
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": GROQ_CONFIG["temperature"],
                "max_tokens": GROQ_CONFIG["max_tokens"]
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            return f"Error: Network issue - {str(e)}"
        except Exception as e:
            return f"Error generating summary: {str(e)}"


class NewsAPIClient:
    """Handle NewsAPI interactions"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = NEWSAPI_CONFIG["api_url"]
        
    def fetch_articles(self, 
                      query: str, 
                      days_back: int = None, 
                      page_size: int = None,
                      sort_by: str = None,
                      language: str = None) -> Dict:
        """Fetch news articles from NewsAPI"""
        try:
            # Set defaults from config
            days_back = days_back or NEWSAPI_CONFIG["default_days_back"]
            page_size = page_size or NEWSAPI_CONFIG["default_page_size"]
            sort_by = sort_by or NEWSAPI_CONFIG["default_sort"]
            language = language or NEWSAPI_CONFIG["language"]
            
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            params = {
                'q': query,
                'apiKey': self.api_key,
                'language': language,
                'sortBy': sort_by,
                'pageSize': min(page_size, 100),  # API limit
                'from': from_date
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"NewsAPI Error: {response.status_code} - {response.text}"}
                
        except requests.exceptions.Timeout:
            return {"error": "Request timed out. Please try again."}
        except requests.exceptions.RequestException as e:
            return {"error": f"Network issue: {str(e)}"}
        except Exception as e:
            return {"error": f"Error fetching news: {str(e)}"}


class NewsProcessor:
    """Process and format news data"""
    
    @staticmethod
    def prepare_content_for_analysis(articles: List[Dict], max_articles: int = 10) -> str:
        """Prepare news content for AI analysis"""
        news_content = ""
        
        for i, article in enumerate(articles[:max_articles]):
            title = article.get('title', 'No title')
            description = article.get('description', 'No description')
            source = article.get('source', {}).get('name', 'Unknown source')
            published_at = article.get('publishedAt', 'Unknown date')
            
            news_content += f"""
            Article {i+1}:
            Title: {title}
            Description: {description}
            Source: {source}
            Published: {published_at[:10]}
            ---
            """
        
        return news_content
    
    @staticmethod
    def extract_article_metadata(articles: List[Dict]) -> Dict:
        """Extract metadata from articles for analytics"""
        if not articles:
            return {}
            
        # Extract sources
        sources = [article.get('source', {}).get('name', 'Unknown') 
                  for article in articles]
        source_counts = {}
        for source in sources:
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Extract dates
        dates = [article.get('publishedAt', '')[:10] 
                for article in articles if article.get('publishedAt')]
        
        # Calculate date range
        date_range = {}
        if dates:
            date_range = {
                'earliest': min(dates),
                'latest': max(dates),
                'span_days': (datetime.strptime(max(dates), '%Y-%m-%d') - 
                             datetime.strptime(min(dates), '%Y-%m-%d')).days
            }
        
        return {
            'total_articles': len(articles),
            'unique_sources': len(set(sources)),
            'source_distribution': source_counts,
            'date_range': date_range,
            'sources_list': list(set(sources))
        }
    
    @staticmethod
    def format_article_for_display(article: Dict, index: int) -> Dict:
        """Format article data for UI display"""
        return {
            'index': index,
            'title': article.get('title', 'No title available'),
            'description': article.get('description', 'No description available'),
            'source': article.get('source', {}).get('name', 'Unknown Source'),
            'published_at': article.get('publishedAt', 'Unknown date')[:19].replace('T', ' '),
            'url': article.get('url', ''),
            'url_to_image': article.get('urlToImage', ''),
            'author': article.get('author', 'Unknown author')
        }
    
    @staticmethod
    def validate_articles(articles: List[Dict]) -> Tuple[List[Dict], List[str]]:
        """Validate and filter articles, return valid articles and warnings"""
        valid_articles = []
        warnings = []
        
        for i, article in enumerate(articles):
            if not article.get('title') and not article.get('description'):
                warnings.append(f"Article {i+1}: Missing title and description")
                continue
                
            if not article.get('source', {}).get('name'):
                warnings.append(f"Article {i+1}: Unknown source")
            
            valid_articles.append(article)
        
        return valid_articles, warnings


# Utility functions
def create_download_content(summary: str, query: str, metadata: Dict) -> str:
    """Create formatted content for download"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    content = f"""
NEWS RESEARCH REPORT
Generated: {timestamp}
Query: {query}

{'='*50}
EXECUTIVE SUMMARY
{'='*50}

{summary}

{'='*50}
RESEARCH METADATA  
{'='*50}

Total Articles Analyzed: {metadata.get('total_articles', 'N/A')}
Unique News Sources: {metadata.get('unique_sources', 'N/A')}
Date Range: {metadata.get('date_range', {}).get('earliest', 'N/A')} to {metadata.get('date_range', {}).get('latest', 'N/A')}

Sources Distribution:
"""
    
    source_dist = metadata.get('source_distribution', {})
    for source, count in sorted(source_dist.items(), key=lambda x: x[1], reverse=True):
        content += f"- {source}: {count} articles\n"
    
    content += f"""
{'='*50}
DISCLAIMER
{'='*50}

This report is generated by AI and should not be considered as financial advice.
Always consult with qualified financial advisors before making investment decisions.
The information provided is based on publicly available news sources and may not be complete or accurate.

Report generated by News Research Tool - Powered by Groq AI & NewsAPI
"""
    
    return content

def validate_api_keys(groq_key: str, news_key: str) -> Tuple[bool, List[str]]:
    """Validate API keys format"""
    errors = []
    
    if not groq_key or len(groq_key) < 10:
        errors.append("Invalid Groq API key format")
    
    if not news_key or len(news_key) < 10:
        errors.append("Invalid NewsAPI key format")
    
    return len(errors) == 0, errors