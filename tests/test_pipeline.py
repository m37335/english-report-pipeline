import pytest
from unittest.mock import Mock, patch
from src.pipeline_orchestrator import PipelineOrchestrator


class TestPipelineOrchestrator:
    """PipelineOrchestratorのテストクラス"""

    def setup_method(self):
        """各テストメソッドの前に実行されるセットアップ"""
        self.orchestrator = PipelineOrchestrator()

    def test_initialization(self):
        """初期化のテスト"""
        assert self.orchestrator is not None
        assert hasattr(self.orchestrator, 'refiner')
        assert hasattr(self.orchestrator, 'expander')
        assert hasattr(self.orchestrator, 'api_client')
        assert hasattr(self.orchestrator, 'outline_creator')
        assert hasattr(self.orchestrator, 'writer')

    @patch('src.pipeline_orchestrator.query_refiner.QueryRefiner')
    @patch('src.pipeline_orchestrator.query_expander.QueryExpander')
    @patch('src.pipeline_orchestrator.external_api_client.ExternalApiClient')
    @patch('src.pipeline_orchestrator.outline_creater.OutlineCreator')
    @patch('src.pipeline_orchestrator.report_writer.ReportWriter')
    def test_run_pipeline(self, mock_writer, mock_outline, mock_api, mock_expander, mock_refiner):
        """パイプライン実行のテスト"""
        # モックの設定
        mock_refiner.return_value.refine.return_value = "refined query"
        mock_expander.return_value.expand.return_value = ["topic1", "topic2"]
        mock_api.return_value.search.return_value = {"topic1": "data1", "topic2": "data2"}
        mock_outline.return_value.create.return_value = "test outline"
        mock_writer.return_value.write.return_value = "final report"

        # パイプライン実行
        result = self.orchestrator.run("test query")

        # 結果の検証
        assert result == "final report"
        
        # 各モジュールが正しく呼び出されたことを確認
        mock_refiner.return_value.refine.assert_called_once_with("test query")
        mock_expander.return_value.expand.assert_called_once_with("refined query")
        mock_api.return_value.search.assert_called_once_with(["topic1", "topic2"])
        mock_outline.return_value.create.assert_called_once_with("refined query", {"topic1": "data1", "topic2": "data2"})
        mock_writer.return_value.write.assert_called_once()

    def test_run_with_empty_query(self):
        """空のクエリでの実行テスト"""
        with pytest.raises(Exception):
            self.orchestrator.run("")

    def test_run_with_none_query(self):
        """Noneクエリでの実行テスト"""
        with pytest.raises(Exception):
            self.orchestrator.run(None)


if __name__ == "__main__":
    pytest.main([__file__]) 