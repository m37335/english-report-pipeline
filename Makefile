.PHONY: help install test lint format clean docker-build docker-run docker-compose-dev docker-compose-prod run-streamlit

help: ## このヘルプを表示
	@echo "利用可能なコマンド:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 依存関係をインストール
	pip install -r requirements.txt

test: ## テストを実行
	pytest tests/ -v

lint: ## コードの静的解析を実行
	flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
	black --check src/

format: ## コードをフォーマット
	black src/
	flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics

clean: ## キャッシュファイルを削除
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

docker-build: ## Dockerイメージをビルド
	docker build -t english-report-pipeline .

docker-run: ## Dockerコンテナを実行
	docker run -it --rm -e OPENAI_API_KEY=$(OPENAI_API_KEY) english-report-pipeline "test query"

docker-compose-dev: ## Docker Composeで開発環境を起動
	docker-compose --profile dev up --build

docker-compose-prod: ## Docker Composeで本番環境を起動
	docker-compose --profile prod up --build

run: ## アプリケーションを実行
	python main.py "test query"

run-streamlit: ## Streamlitアプリを実行
	streamlit run app.py --server.port 8501 --server.address 0.0.0.0

setup: install ## 開発環境をセットアップ
	@echo "開発環境のセットアップが完了しました"
	@echo "環境変数を設定してください:"
	@echo "export OPENAI_API_KEY=your_api_key_here" 