import argparse
from src.pipeline_orchestrator import PipelineOrchestrator

def main():
    """
    パイプライン実行のエントリーポイント。
    コマンドラインから初期クエリを受け取る。
    """
    parser = argparse.ArgumentParser(description="English Report Pipeline")
    parser.add_argument("query", type=str, help="The initial query to generate a report for.")
    args = parser.parse_args()

    orchestrator = PipelineOrchestrator()
    final_report = orchestrator.run(args.query)

    # 生成されたレポートをコンソールに出力
    print("\n--- Generated Report ---")
    print(final_report)

    # TODO: レポートをファイルに保存する処理を追加
    # with open("data/output/final_report.md", "w") as f:
    #     f.write(final_report)

if __name__ == "__main__":
    main()
