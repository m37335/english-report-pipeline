from . import query_refiner
from . import query_expander
from . import external_api_client
from . import outline_creater
from . import report_writer
from . import mindmap_generator
import asyncio
import logging
from typing import Dict, Any, List
import time

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    """
    Lawsyの設計を参考にした、より洗練されたパイプライン全体のフローを制御するクラス。
    STORMベースの処理フローを実装し、英語教育に特化した検索戦略を採用。
    """
    def __init__(self):
        """各モジュールの初期化"""
        self.refiner = query_refiner.QueryRefiner()
        self.expander = query_expander.QueryExpander()
        self.api_client = external_api_client.ExternalApiClient()
        self.outline_creator = outline_creater.OutlineCreator()
        self.writer = report_writer.ReportWriter()
        self.mindmap_generator = mindmap_generator.MindmapGeneratorModule()
        print("PipelineOrchestrator initialized with Lawsy-inspired design.")

    def run(self, initial_query: str) -> dict:
        """
        Lawsyの設計を参考にしたパイプラインを実行する。

        Args:
            initial_query: ユーザーからの最初のクエリ

        Returns:
            最終的に生成されたレポートとマインドマップを含む辞書
        """
        print(f"--- Running Lawsy-inspired pipeline for query: {initial_query} ---")
        start_time = time.time()

        try:
            # 1. クエリ洗練（Web検索用に変換）
            refined_query = self.refiner.refine(initial_query)
            print(f"Step 1: Refined query for web search: {refined_query}")

            # 2. ドメイン特化検索（英語教育関連サイト）
            education_search_results = self._search_education_domains(refined_query)
            print(f"Step 2: Education domain search completed")

            # 3. 一般的なWeb検索
            general_search_results = self._search_general_web(refined_query)
            print(f"Step 3: General web search completed")

            # 4. クエリ展開（複数のリサーチトピックに分解）
            search_topics = self.expander.expand(refined_query)
            print(f"Step 4: Expanded to search topics: {len(search_topics)} topics")

            # 5. 各トピックに対する詳細検索
            detailed_search_results = self._search_detailed_topics(search_topics)
            print(f"Step 5: Detailed topic search completed")

            # 6. 情報の統合とアウトライン生成
            combined_results = self._combine_search_results(
                education_search_results, 
                general_search_results, 
                detailed_search_results
            )
            outline = self.outline_creator.create(refined_query, combined_results)
            print(f"Step 6: Created comprehensive outline")

            # 7. レポート執筆（リード文、本文、関連事項、結論）
            final_report = self.writer.write(outline, combined_results, initial_query, refined_query)
            print("Step 7: Report written with all sections")

            # 8. マインドマップ生成
            mindmap_data = self.mindmap_generator.generate_mindmap(final_report)
            print("Step 8: Mindmap generated")

            # 9. 処理時間の計算
            processing_time = time.time() - start_time
            print(f"--- Pipeline finished in {processing_time:.2f} seconds ---")
            
            return {
                'report': final_report,
                'mindmap': mindmap_data,
                'query': initial_query,
                'refined_query': refined_query,
                'processing_time': processing_time,
                'search_stats': {
                    'education_results': len(education_search_results),
                    'general_results': len(general_search_results),
                    'detailed_results': len(detailed_search_results),
                    'total_topics': len(search_topics)
                }
            }
            
        except Exception as e:
            logger.error(f"Pipeline execution error: {e}")
            return self._get_fallback_result(initial_query, str(e))

    def _search_education_domains(self, refined_query: str) -> Dict[str, str]:
        """英語教育関連ドメインに特化した検索"""
        education_domains = [
            "jst.go.jp",  # 科学技術振興機構
            "mext.go.jp",  # 文部科学省
            "nier.go.jp",  # 国立教育政策研究所
            "bunka.go.jp",  # 文化庁
            "jasso.go.jp",  # 日本学生支援機構
        ]
        
        results = {}
        for domain in education_domains:
            try:
                domain_query = f"{refined_query} site:{domain}"
                result = self.api_client._search_basic_web(domain_query)
                results[f"education_{domain}"] = result
            except Exception as e:
                logger.warning(f"Education domain search failed for {domain}: {e}")
        
        return results

    def _search_general_web(self, refined_query: str) -> Dict[str, str]:
        """一般的なWeb検索"""
        try:
            return self.api_client.search([refined_query])
        except Exception as e:
            logger.error(f"General web search failed: {e}")
            return {"general_search": f"Search error: {str(e)}"}

    def _search_detailed_topics(self, search_topics: List[str]) -> Dict[str, str]:
        """各トピックに対する詳細検索"""
        try:
            return self.api_client.search(search_topics)
        except Exception as e:
            logger.error(f"Detailed topic search failed: {e}")
            return {"detailed_search": f"Search error: {str(e)}"}

    def _combine_search_results(self, education_results: Dict[str, str], 
                               general_results: Dict[str, str], 
                               detailed_results: Dict[str, str]) -> Dict[str, str]:
        """検索結果を統合"""
        combined = {}
        
        # 教育ドメイン検索結果を優先
        combined.update(education_results)
        
        # 一般的な検索結果を追加
        combined.update(general_results)
        
        # 詳細検索結果を追加
        combined.update(detailed_results)
        
        return combined

    def _get_fallback_result(self, initial_query: str, error_message: str) -> Dict[str, Any]:
        """エラー時のフォールバック結果"""
        return {
            'report': f"# エラーが発生しました\n\nクエリ: {initial_query}\n\nエラー: {error_message}\n\n申し訳ございませんが、しばらく時間をおいてから再度お試しください。",
            'mindmap': {
                "name": "Error Report",
                "children": [
                    {"name": "Error", "children": []},
                    {"name": "Please try again", "children": []}
                ]
            },
            'query': initial_query,
            'refined_query': initial_query,
            'processing_time': 0,
            'search_stats': {
                'education_results': 0,
                'general_results': 0,
                'detailed_results': 0,
                'total_topics': 0
            }
        }
