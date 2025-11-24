# 使用例

このフォルダには、python-uv-templateの使用例を示すJupyter notebookが含まれています。

## ノートブック一覧

### basic_usage.ipynb

計算機モジュールの基本的な使い方を示します。

**内容:**
- 基本的な計算（加算、減算、乗算、除算、べき乗）
- NumPy配列との組み合わせ
- エラーハンドリング
- 研究用途での実践例

## 実行方法

### Jupyter Notebookの起動

```bash
# Jupyter Labをインストール（まだの場合）
uv pip install jupyterlab

# Jupyter Labを起動
jupyter lab
```

### Google Colabで実行

1. GitHubリポジトリをクローン
2. `examples/` フォルダのノートブックを開く
3. ランタイムを接続して実行

## 新しいノートブックを追加する場合

1. `examples/` フォルダに新しい `.ipynb` ファイルを作成
2. 必要に応じて `sys.path.append('../src')` を追加
3. このREADMEに説明を追加
4. コミット前に全てのセルを実行して動作を確認

## 注意事項

- ノートブックは再現性を保つため、ランダムシードを設定してください
- 大きなデータファイルはGitにコミットせず、`.gitignore` に追加してください
- 実行結果をクリアしてからコミットすることを推奨します
