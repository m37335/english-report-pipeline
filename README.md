# English Report Pipeline

英語レポート生成パイプライン - AIを活用した英語学習レポートの自動生成システム

## 概要

このプロジェクトは、ユーザーのクエリを基に、英語学習に特化したレポートを自動生成するパイプラインです。Lawsyの設計思想を参考に、モジュラーアーキテクチャを採用しています。

## 機能

- **クエリ洗練**: ユーザーの入力を最適化
- **検索トピック生成**: 関連する学習トピックを自動生成
- **外部API検索**: 英語学習リソースからの情報収集
- **アウトライン生成**: 構造化された学習計画の作成
- **レポート執筆**: 最終的な英語学習レポートの生成

## セットアップ

### 1. 環境変数の設定

`.env`ファイルを作成し、必要なAPIキーを設定してください：

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. アプリケーションの実行

```bash
python main.py "your query here"
```

## Docker環境での実行

### ビルド

```bash
docker build -t english-report-pipeline .
```

### 実行

```bash
docker run -it --rm -e OPENAI_API_KEY=your_key english-report-pipeline "your query"
```

## 開発

### テストの実行

```bash
pytest tests/
```

### コードフォーマット

```bash
black src/
flake8 src/
```

## プロジェクト構造

```
english_report_pipeline/
├── src/                    # メインソースコード
│   ├── pipeline_orchestrator.py
│   ├── query_refiner.py
│   ├── query_expander.py
│   ├── external_api_client.py
│   ├── outline_creater.py
│   └── report_writer.py
├── config/                 # 設定ファイル
├── data/                   # データファイル
├── tests/                  # テストファイル
├── themes/                 # テーマファイル
├── main.py                 # エントリーポイント
├── requirements.txt        # 依存関係
└── README.md              # このファイル
```

## ライセンス

MIT License
