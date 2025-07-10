# Contributing to English Report Pipeline

## 開発環境のセットアップ

### 1. リポジトリをクローン
```bash
git clone https://github.com/m37335/english-report-pipeline.git
cd english-report-pipeline
```

### 2. 依存関係をインストール
```bash
make install
```

### 3. 環境変数を設定
```bash
cp env.example .env
# .envファイルを編集してAPIキーを設定
```

### 4. テストの実行
```bash
make test
```

## 開発ワークフロー

### 1. 新しいブランチを作成
```bash
git checkout -b feature/your-feature-name
# または
git checkout -b fix/your-bug-fix
```

### 2. 変更を加える
- コードを編集
- テストを追加
- ドキュメントを更新

### 3. コードフォーマット
```bash
make format
```

### 4. テストを実行
```bash
make test
```

### 5. 変更をコミット
```bash
git add .
git commit -m "feat: add your feature description"
# または
git commit -m "fix: fix your bug description"
```

### 6. プッシュ
```bash
git push origin feature/your-feature-name
```

### 7. プルリクエストを作成
1. GitHubでプルリクエストを作成
2. タイトルと説明を記入
3. レビューを待つ
4. 承認後にマージ

## コミットメッセージの規約

- `feat:` - 新機能
- `fix:` - バグ修正
- `docs:` - ドキュメント更新
- `style:` - コードスタイルの変更
- `refactor:` - リファクタリング
- `test:` - テストの追加・修正
- `chore:` - その他の変更

## テスト

### テストの実行
```bash
make test
```

### カバレッジの確認
```bash
pytest --cov=src tests/
```

## コードスタイル

### フォーマット
```bash
make format
```

### リント
```bash
make lint
```

## Docker

### ローカルでのビルド
```bash
make docker-build
```

### ローカルでの実行
```bash
make docker-run
```

## トラブルシューティング

### よくある問題

1. **依存関係のエラー**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **テストの失敗**
   ```bash
   pytest tests/ -v -s
   ```

3. **Dockerビルドエラー**
   ```bash
   docker system prune -a
   make docker-build
   ```

## 質問・サポート

- イシューを作成して質問してください
- プルリクエストでコードレビューを依頼してください
- ドキュメントの改善提案も歓迎します

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 