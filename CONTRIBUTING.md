# コントリビューションガイド

python-uv-templateへの貢献に興味を持っていただきありがとうございます！

このドキュメントでは、プロジェクトへの貢献方法について説明します。

## 行動規範

このプロジェクトに参加するすべての人は、相互尊重と建設的なコミュニケーションを心がけてください。

## 貢献の方法

### バグレポート

バグを見つけた場合は、以下の情報を含めてIssueを作成してください：

1. **明確なタイトル**: 問題を簡潔に説明
2. **再現手順**: 問題を再現する詳細な手順
3. **期待される動作**: 何が起こるべきか
4. **実際の動作**: 実際に何が起こったか
5. **環境情報**: OS、Pythonバージョン、パッケージバージョン
6. **最小限の再現コード**: 可能であれば

### 機能リクエスト

新機能を提案する場合は、以下を含めてください：

1. **解決したい問題**: なぜこの機能が必要か
2. **提案する解決策**: 具体的な実装案
3. **代替案**: 検討した他のアプローチ
4. **使用例**: この機能をどう使うか

### Pull Request

#### 開発環境のセットアップ

```bash
# リポジトリをフォーク
git clone https://github.com/YOUR_USERNAME/python-uv-template.git
cd python-uv-template

# uvをインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係をインストール
make install

# pre-commitフックをインストール
pre-commit install
```

#### ブランチ戦略

1. メインブランチから新しいブランチを作成：
   ```bash
   git checkout -b feature/your-feature-name
   # または
   git checkout -b fix/your-bug-fix
   ```

2. 自律修正機能を使いたい場合は `claude/` プレフィックスを使用：
   ```bash
   git checkout -b claude/your-feature-name
   ```

#### 依存関係の管理

このプロジェクトは **uvのネイティブプロジェクト管理機能** で依存関係を管理しています。

**ファイルの役割:**
- `pyproject.toml`: プロジェクトのメタデータと依存関係の定義
- `uv.lock`: uvが自動生成する完全な依存関係ロックファイル（全パッケージのハッシュ値を含む）
- `.python-version`: プロジェクトで使用するPythonバージョン

**新しい依存関係を追加する手順:**

```bash
# 1. pyproject.toml を編集
# [project]
# dependencies = [
#     ...
#     "scikit-learn>=1.3.0",
# ]

# 2. uv.lock を更新
make lock

# 3. ローカル環境に同期
make sync

# 4. 両方のファイルをコミット
git add pyproject.toml uv.lock
git commit -m "Add scikit-learn dependency"
```

**利点:**
- `uv sync` による高速な依存関係インストール（pipより10-100倍高速）
- `uv.lock` による完全な再現性（ハッシュ値検証）
- 不要なパッケージの自動削除
- CI/CDでのビルトインキャッシュによる最適化

#### 開発ワークフロー（TDD）

**重要**: このプロジェクトはテスト駆動開発（TDD）を採用しています。

1. **テストを先に書く**:
   ```python
   # tests/test_new_feature.py
   def test_new_feature():
       result = new_feature(input_data)
       assert result == expected_output
   ```

2. **テストが失敗することを確認**:
   ```bash
   pytest tests/test_new_feature.py
   ```

3. **最小限の実装でテストを通す**:
   ```python
   # src/module.py
   def new_feature(data):
       # 実装
       return result
   ```

4. **テストが通ることを確認**:
   ```bash
   pytest tests/test_new_feature.py
   ```

5. **リファクタリング**: コードを改善しながらテストが通ることを確認

6. **全てのテストを実行**:
   ```bash
   make test
   ```

#### コーディング規約

- **PEP 8**: Pythonの標準スタイルガイドに従う
- **型ヒント**: すべての関数に型アノテーションを追加
  ```python
  def add(a: int, b: int) -> int:
      return a + b
  ```

- **Docstring**: NumPyまたはGoogleスタイルのdocstringを使用
  ```python
  def function(param1: str, param2: int) -> bool:
      """Brief description.

      Args:
          param1: Description of param1
          param2: Description of param2

      Returns:
          Description of return value

      Raises:
          ValueError: When invalid input is provided
      """
      pass
  ```

- **テストカバレッジ**: 80%以上を維持
  ```bash
  make test-cov
  ```

#### コミットメッセージ

明確で説明的なコミットメッセージを書いてください：

```
簡潔なタイトル（50文字以内）

- 詳細な変更内容を箇条書きで
- なぜこの変更が必要かを説明
- 関連するIssue番号があれば記載

Closes #123
```

良い例：
```
Add validation for division by zero

- Add ValueError when denominator is zero
- Update docstring to document the exception
- Add test cases for edge cases

Closes #45
```

悪い例：
```
fix bug
```

#### チェックリスト

Pull Requestを提出する前に、以下を確認してください：

- [ ] テストを先に書いた（TDD）
- [ ] すべてのテストが通過する (`make test`)
- [ ] コードがフォーマットされている (`make format`)
- [ ] リンターエラーがない (`make lint`)
- [ ] 型チェックが通る (`make type-check`)
- [ ] 型ヒントを追加した
- [ ] Docstringを追加した
- [ ] ドキュメントを更新した（必要な場合）
- [ ] カバレッジが維持/向上している

#### CIチェック

すべてのPull Requestは以下のCIチェックを通過する必要があります：

- pytest: すべてのテストが通過
- ruff: コードスタイルチェック
- mypy: 型チェック

ローカルで全てのCIチェックを実行：
```bash
make ci
```

#### Claude Codeを使う

Claude Codeに作業を依頼することもできます：

1. Issueを作成し、`@claude` をメンション
2. 詳細な要件を記載
3. Claudeが自動的に実装してPRを作成

```markdown
@claude

新しいデータ処理関数を実装してください。

要件:
- CSVファイルを読み込んで欠損値を処理
- テストを先に書いてください（TDD）
- 型ヒントとdocstringを含めてください
```

## プロジェクト構造

```
python-uv-template/
├── .github/
│   ├── workflows/        # GitHub Actions
│   └── ISSUE_TEMPLATE/   # Issueテンプレート
├── docs/                 # ドキュメント（Sphinx）
├── examples/             # Jupyter notebook例
├── src/                  # ソースコード
├── tests/                # テストコード
├── benchmarks/           # ベンチマーク
├── scripts/              # ユーティリティスクリプト
├── Makefile              # よく使うコマンド
├── pyproject.toml        # プロジェクト設定
└── requirements.txt      # 依存関係
```

## 質問やヘルプ

質問がある場合は：

1. 既存のIssueやドキュメントを検索
2. 新しいIssueを作成（質問タグ付き）
3. `@claude` をメンションしてClaudeに質問

## ライセンス

このプロジェクトに貢献することで、あなたの貢献がプロジェクトと同じライセンスの下でライセンスされることに同意したものとみなされます。

## 謝辞

すべての貢献者に感謝します！
