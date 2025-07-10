from . import query_refiner
from . import query_expander
from . import external_api_client
from . import outline_creater
from . import report_writer

class PipelineOrchestrator:
    """
    パイプライン全体のフローを制御するクラス。
    各ステップを順番に実行し、データの受け渡しを管理する。
    """
    def __init__(self):
        """各モジュールの初期化"""
        self.refiner = query_refiner.QueryRefiner()
        self.expander = query_expander.QueryExpander()
        self.api_client = external_api_client.ExternalApiClient()
        self.outline_creator = outline_creater.OutlineCreator()
        self.writer = report_writer.ReportWriter()
        print("PipelineOrchestrator initialized.")

    def run(self, initial_query: str) -> str:
        """
        パイプラインを実行する。

        Args:
            initial_query: ユーザーからの最初のクエリ

        Returns:
            最終的に生成されたレポート
        """
        print(f"--- Running pipeline for query: {initial_query} ---")

        # 1. クエリ洗練
        refined_query = self.refiner.refine(initial_query)
        print(f"Step 1: Refined query: {refined_query}")

        # 2. 検索トピック生成
        search_topics = self.expander.expand(refined_query)
        print(f"Step 2: Expanded to search topics: {search_topics}")

        # 3. 外部Web検索
        search_results = self.api_client.search(search_topics)
        print(f"Step 3: Fetched data from external DB: {list(search_results.keys())}")

        # 4. アウトライン生成
        outline = self.outline_creator.create(refined_query, search_results)
        print(f"Step 4: Created outline:\n{outline}")

        # 5. レポート執筆
        final_report = self.writer.write(outline, search_results, initial_query, refined_query)
        print("Step 5: Report written.")

        print("--- Pipeline finished ---")
        return final_report
