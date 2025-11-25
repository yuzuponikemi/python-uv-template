# python-uv-template

Python研究用ソフトウェア開発のテンプレートリポジトリです。テスト駆動開発（TDD）をベースに、再現性と品質を重視しています。

## 特徴

- **uv** による高速な依存関係管理
- **テスト駆動開発** を前提とした構成
- **複数のAIコーディングエージェント** をサポート（Claude Code、Gemini、Codex、SWE-agent）
- **エージェント抽象化レイヤー** により簡単なエージェント切り替えが可能
- 研究用ソフトウェアに最適化された設定

## AIコーディングエージェントの使い方

このテンプレートは、複数のAIコーディングエージェントをサポートしています。GitHub上で `@claude` や `@ai` とメンションするだけで、設定されたエージェントが作業を支援します。

### サポートされているエージェント

| エージェント | 特徴 | API Key |
|------------|------|---------|
| **Claude Code** (デフォルト) | TDD、研究ソフトウェア、GitHub統合 | `ANTHROPIC_API_KEY` |
| **Gemini** | 高速、長コンテキスト、マルチモーダル | `GOOGLE_API_KEY` |
| **Codex/GPT** | 汎用性、関数呼び出し | `OPENAI_API_KEY` |
| **SWE-agent** | 自律デバッグ、オープンソース | `OPENAI_API_KEY` |

### セットアップ

1. このテンプレートから新しいリポジトリを作成
2. `.agent-config.yml` で使用するエージェントを選択（デフォルトは Claude Code）
3. リポジトリの Settings > Secrets and variables > Actions で必要な API Key を設定
4. Issue や Pull Request で `@claude` または `@ai` とメンションして使用開始

### エージェントの選択

`.agent-config.yml` ファイルでエージェントを変更できます：

```yaml
agent:
  type: gemini  # claude_code, gemini, codex, swe_agent
  model: gemini-2.0-flash-exp
```

詳細は [エージェント抽象化ドキュメント](docs/AGENT_ABSTRACTION.md) を参照してください。

### 使用例

**Issue でのタスク依頼:**
```
新しいデータ処理関数を実装してください @ai

要件:
- CSVファイルを読み込んで欠損値を処理
- テストを先に書いてください（TDD）
- 型ヒントとdocstringを含めてください
```

**Pull Request でのレビュー依頼:**
```
この実装をレビューして、テストカバレッジを改善してください @claude
```

**コードの改善依頼:**
```
この関数のパフォーマンスを最適化して、ベンチマークテストも追加してください @ai
```

### コーディングエージェントが従う原則

すべてのエージェントは以下の原則に従います：

1. **テスト駆動開発**: 実装前にテストを書きます
2. **型安全性**: すべての関数に型ヒントを追加
3. **再現性**: 依存関係を厳密に管理
4. **科学的正確性**: 数値計算の精度とエッジケースをテスト
5. **ドキュメント**: 論文・アルゴリズムの参照を含む詳細なdocstring

## 自律的コード修正機能

このテンプレートには、CIテストが失敗した際に自動的にエージェントが修正を試みる機能が組み込まれています。

### 仕組み

1. **CI ワークフロー** (`ci.yml`): `claude/**` または `ai/**` ブランチにpushすると自動的にテスト・リンター・型チェックを実行
2. **自動修正ワークフロー** (`auto-fix.yml`): CIが失敗した場合、自動的に実行され：
   - エラーログを収集・分析
   - 修正用のIssueを自動作成し、エージェントをメンション
   - エージェントがエラーを解析して修正を実装
   - 修正を同じブランチにコミット

### 動作例

```bash
# 1. 新しい機能ブランチを作成（claude/ または ai/ プレフィックスが必要）
git checkout -b ai/add-new-feature

# 2. コードを編集してpush
git add .
git commit -m "Add new feature"
git push -u origin ai/add-new-feature

# 3. CIが自動実行される
# 4. もしテストが失敗したら、エージェントが自動的に修正Issueを作成
# 5. エージェントが修正を実装してコミット
# 6. CIが再実行され、修正が検証される
```

### 対応するエラータイプ

- **Pytest**: テスト失敗、アサーションエラー
- **Ruff**: コードスタイル違反、リントエラー
- **Mypy**: 型ヒントエラー、型の不一致

### 注意点

- 自動修正機能は `claude/**` または `ai/**` ブランチでのみ動作します
- 複雑なエラーの場合、エージェントは修正方針を提示して人間のレビューを求めることがあります
- 使用するエージェントに対応する API Key が正しく設定されていることを確認してください
- エージェントの選択は `.agent-config.yml` で設定できます

## 開発環境のセットアップ

```bash
# uvのインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
make install

# テストの実行
make test

# リンターの実行
make lint

# フォーマッターの実行
make format

# 全てのCIチェック
make ci
```

## 依存関係の管理

このプロジェクトは **uv** による依存関係の固定管理を採用しています。

### ファイルの役割

- **`requirements.in`**: 人間が編集するトップレベルの依存関係
- **`requirements.txt`**: uvが自動生成する完全な依存関係リスト（全バージョン固定）

### 依存関係を追加する場合

1. `requirements.in` を編集して依存関係を追加
2. `make compile` を実行して `requirements.txt` を更新
3. 変更をコミット（両方のファイルをコミット）

```bash
# requirements.in に新しいパッケージを追加
echo "scikit-learn>=1.3.0" >> requirements.in

# requirements.txt を更新
make compile

# インストール
make install
```

**注意**: CIが自動的に `requirements.txt` を最新化してコミットします。