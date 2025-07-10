import os
import requests
from typing import Dict, List
from dotenv import load_dotenv
import logging
from bs4 import BeautifulSoup
import time

# 環境変数を読み込み
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExternalApiClient:
    """
    外部API(Web検索)と通信するクライアント。
    """
    def __init__(self):
        """
        APIクライアントの初期化
        """
        self.google_api_key = os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY')
        self.google_engine_id = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_ID')
        self.serpapi_key = os.getenv('SERPAPI_API_KEY')
        
        # セッション設定
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        print("ExternalApiClient initialized.")

    def search(self, search_topics: list[str]) -> dict[str, str]:
        """
        与えられた検索トピックのリストに基づいてWeb検索を実行する。

        Args:
            search_topics: 検索トピックのリスト

        Returns:
            各トピックをキーとし、検索結果の要約を値とする辞書
        """
        print(f"Searching the web for topics: {search_topics}")
        all_results = {}

        for topic in search_topics:
            try:
                # レート制限を避けるため少し待機
                time.sleep(1)
                
                search_result = self._search_topic(topic)
                all_results[topic] = search_result
                
            except Exception as e:
                print(f"Error searching for topic '{topic}': {e}")
                all_results[topic] = f"No results found for '{topic}'."

        print(f"Finished web search. Found results for {len(all_results)} topics.")
        return all_results
    
    def _search_topic(self, topic: str) -> str:
        """個別のトピックを検索する"""
        # Google Custom Search APIを優先
        if self.google_api_key and self.google_engine_id:
            return self._search_google_custom(topic)
        # SerpAPIをフォールバック
        elif self.serpapi_key:
            return self._search_serpapi(topic)
        else:
            # フォールバック: 基本的なWebスクレイピング
            return self._search_basic_web(topic)
    
    def _search_google_custom(self, topic: str) -> str:
        """Google Custom Search APIを使用して検索"""
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.google_api_key,
                'cx': self.google_engine_id,
                'q': topic,
                'num': 5  # 最大5件の結果
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if 'items' in data:
                for item in data['items']:
                    title = item.get('title', '')
                    snippet = item.get('snippet', '')
                    results.append(f"Title: {title}\nSnippet: {snippet}")
            
            return "\n\n".join(results) if results else f"No results found for '{topic}'"
            
        except Exception as e:
            logger.error(f"Google Custom Search error: {e}")
            return f"Search error for '{topic}': {str(e)}"
    
    def _search_serpapi(self, topic: str) -> str:
        """SerpAPIを使用して検索"""
        try:
            url = "https://serpapi.com/search"
            params = {
                'api_key': self.serpapi_key,
                'q': topic,
                'engine': 'google',
                'num': 5
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if 'organic_results' in data:
                for result in data['organic_results'][:5]:
                    title = result.get('title', '')
                    snippet = result.get('snippet', '')
                    results.append(f"Title: {title}\nSnippet: {snippet}")
            
            return "\n\n".join(results) if results else f"No results found for '{topic}'"
            
        except Exception as e:
            logger.error(f"SerpAPI error: {e}")
            return f"Search error for '{topic}': {str(e)}"
    
    def _search_basic_web(self, topic: str) -> str:
        """基本的なWeb検索（フォールバック）"""
        try:
            # 教育関連のサイトを優先的に検索
            search_urls = [
                f"https://www.google.com/search?q={topic}+英語教育",
                f"https://www.google.com/search?q={topic}+英文法",
                f"https://www.google.com/search?q={topic}+英語学習"
            ]
            
            results = []
            for url in search_urls[:1]:  # 最初のURLのみ使用
                try:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # 検索結果のタイトルとスニペットを抽出
                    search_results = soup.find_all('div', class_='g')
                    for result in search_results[:3]:
                        title_elem = result.find('h3')
                        snippet_elem = result.find('div', class_='VwiC3b')
                        
                        if title_elem and snippet_elem:
                            title = title_elem.get_text().strip()
                            snippet = snippet_elem.get_text().strip()
                            results.append(f"Title: {title}\nSnippet: {snippet}")
                    
                    if results:
                        break
                        
                except Exception as e:
                    logger.error(f"Basic web search error: {e}")
                    continue
            
            return "\n\n".join(results) if results else f"Basic search completed for '{topic}'"
            
        except Exception as e:
            logger.error(f"Basic web search error: {e}")
            return f"Search error for '{topic}': {str(e)}"
