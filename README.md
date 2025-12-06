# python-uv-template

Python研究用ソフトウェア開発のテンプレートリポジトリです。テスト駆動開発（TDD）をベースに、再現性と品質を重視しています。

## 特徴

- **uv** による高速な依存関係管理
- **テスト駆動開発** を前提とした構成
- **Claude Code** による自動化されたコード支援
- **包括的なCI/CD** パイプライン
  - Python 3.11でのテスト（マルチバージョンテストはオプション）
  - 依存関係キャッシュによる高速化（2〜3倍速）
  - セキュリティチェック（Bandit）
  - カバレッジレポート（GitHub Actions Artifacts）
  - pre-commitフック自動実行
- **自動依存関係更新**（Dependabot）
- **自動リリース**（タグベース）
- **ドキュメント自動ビルド**（GitHub Pages対応、Publicリポジトリ向け）
- **ベンチマーク自動実行**
- **低コスト運用**: Private repositoryでも完全無料で利用可能
- 研究用ソフトウェアに最適化された設定

## Claude Code の使い方

このテンプレートには、GitHub上で `@claude` とメンションするだけでAIアシスタントが作業を支援するワークフローが含まれています。

### セットアップ

1. このテンプレートから新しいリポジトリを作成
2. リポジトリの Settings > Secrets and variables > Actions で `ANTHROPIC_API_KEY` を設定
3. Issue や Pull Request で `@claude` とメンションして使用開始

### 使用例

**Issue でのタスク依頼:**
```
新しいデータ処理関数を実装してください @claude

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
この関数のパフォーマンスを最適化して、ベンチマークテストも追加してください @claude
```

### Claudeが従う原則

1. **テスト駆動開発**: 実装前にテストを書きます
2. **型安全性**: すべての関数に型ヒントを追加
3. **再現性**: 依存関係を厳密に管理
4. **科学的正確性**: 数値計算の精度とエッジケースをテスト
5. **ドキュメント**: 論文・アルゴリズムの参照を含む詳細なdocstring

## 自律的コード修正機能

このテンプレートには、CIテストが失敗した際に自動的にClaudeが修正を試みる機能が組み込まれています。

### 仕組み

1. **CI ワークフロー** (`ci.yml`): `claude/**` ブランチにpushすると自動的にテスト・リンター・型チェックを実行
2. **自動修正ワークフロー** (`auto-fix.yml`): CIが失敗した場合、自動的に実行され：
   - エラーログを収集・分析
   - 修正用のIssueを自動作成し、`@claude` をメンション
   - Claudeがエラーを解析して修正を実装
   - 修正を同じブランチにコミット

### 動作例

```bash
# 1. 新しい機能ブランチを作成（claude/ プレフィックスが必要）
git checkout -b claude/add-new-feature

# 2. コードを編集してpush
git add .
git commit -m "Add new feature"
git push -u origin claude/add-new-feature

# 3. CIが自動実行される
# 4. もしテストが失敗したら、Claudeが自動的に修正Issueを作成
# 5. Claudeが修正を実装してコミット
# 6. CIが再実行され、修正が検証される
```

### 対応するエラータイプ

- **Pytest**: テスト失敗、アサーションエラー
- **Ruff**: コードスタイル違反、リントエラー
- **Mypy**: 型ヒントエラー、型の不一致

### 注意点

- 自動修正機能は `claude/**` ブランチでのみ動作します
- 複雑なエラーの場合、Claudeは修正方針を提示して人間のレビューを求めることがあります
- `ANTHROPIC_API_KEY` が正しく設定されていることを確認してください

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

## ローカルでのCIテスト（act）

このプロジェクトは`act`を使用してGitHub Actionsワークフローをローカルで実行できます。

### セットアップ

```bash
# 1. actとDockerをインストール（macOS）
brew install act docker

# 2. act設定ファイルをセットアップ
make act-setup

# 3. .secretsファイルを編集（必要に応じて）
nano .secrets
```

### 使い方

```bash
# ローカルでCIを実行（GitHub Actionsと同じ環境）
make ci-local

# または直接actコマンドを使用
act push -j test

# 詳細ログ付きで実行
act -v
```

**メリット**:
- プッシュ前にローカルでCIをテスト
- 高速な開発サイクル
- GitHub Actionsの実行時間を節約
- オフラインでのテストが可能

詳細は以下を参照してください：
- [LOCAL_TESTING.md](LOCAL_TESTING.md) - actの詳細なセットアップとトラブルシューティング
- [.github/workflows/README.md](.github/workflows/README.md) - 各ワークフローのローカルテスト方法

## 依存関係の管理

このプロジェクトは **uv** のネイティブプロジェクト管理機能を採用しています。

### ファイルの役割

- **`pyproject.toml`**: プロジェクトのメタデータと依存関係の定義
- **`uv.lock`**: uvが自動生成する完全な依存関係ロックファイル（全パッケージの正確なバージョンとハッシュ値）
- **`.python-version`**: プロジェクトで使用するPythonバージョン

### 依存関係を追加する場合

1. `pyproject.toml` の `dependencies` または `[project.optional-dependencies]` セクションを編集
2. `make lock` を実行して `uv.lock` を更新
3. `make sync` でローカル環境に反映
4. 変更をコミット（`pyproject.toml` と `uv.lock` の両方）

```bash
# pyproject.toml に新しいパッケージを追加
# dependencies = [
#     ...
#     "scikit-learn>=1.3.0",
# ]

# uv.lock を更新
make lock

# ローカル環境に同期
make sync
```

### uvの恩恵

- **高速インストール**: `uv sync` は依存関係を並列ダウンロード・インストール（pipより10-100倍高速）
- **正確な再現性**: `uv.lock` がすべてのパッケージのハッシュ値を含むため、完全に同一の環境を再現
- **自動クリーンアップ**: `uv sync` は不要になったパッケージを自動削除
- **ビルトインキャッシュ**: CI/CDで自動的に最適化されたキャッシュを使用

## CI/CDパイプライン

このテンプレートには、プロダクショングレードのCI/CDパイプラインが組み込まれています。

### CI（継続的インテグレーション）

**トリガー**: `main`, `master`, `develop`, `claude/**` ブランチへのプッシュ、またはPR作成時

**実行内容**:
- **テスト**: Python 3.11でテスト実行（デフォルト）
  - マルチバージョンテスト（3.9, 3.10, 3.11, 3.12）も利用可能（ci.ymlで設定）
- **依存関係キャッシュ**: uv、pip、pre-commitのキャッシュで高速化（2〜3倍速）
- **品質チェック**:
  - Pre-commitフック（trailing-whitespace, YAML/TOML構文など）
  - Ruff（リンター＋フォーマッター）
  - Mypy（型チェック）
  - Bandit（セキュリティチェック）
- **テスト実行**: pytest with カバレッジ測定
- **カバレッジレポート**: GitHub Actions Artifactsとして保存（30日間）

**コスト**:
- Private repository: GitHub Actionsの無料枠内（月2,000分）
- Public repository: 完全無料

### Dependabot（自動依存関係更新）

**スケジュール**: 毎週月曜日 9:00 (JST)

**監視対象**:
- Python依存関係（`requirements.txt`, `requirements-dev.txt`）
- GitHub Actions
- pre-commitフック

**自動PR作成**: パッチ更新とマイナー更新をグループ化してPR作成

### リリース自動化

**トリガー**: `v*.*.*` 形式のタグプッシュ（例：`v1.0.0`, `v2.1.3`）

**実行内容**:
1. パッケージビルド（wheel + sdist）
2. 前回のタグからの変更履歴を自動生成
3. GitHub Releasesに自動公開
4. ビルド成果物をReleasesに添付

**リリース手順**:
```bash
# バージョンを上げる
git tag v1.0.0
git push origin v1.0.0

# 自動的にGitHub Releasesが作成されます
```

**PyPI公開**（オプション）:
- `.github/workflows/release.yml` の `if: false` を `if: true` に変更
- リポジトリシークレットに `PYPI_API_TOKEN` を追加

### ドキュメント自動ビルド

**トリガー**: `main`/`master` ブランチへのプッシュ、またはPR作成時

**実行内容**:
1. Sphinxドキュメントをビルド
2. GitHub Actions Artifactsとして保存（30日間）

**GitHub Pages デプロイ（オプション）**:
- Public repositoryまたはGitHub Pro以上のPrivate repository向け
- `.github/workflows/docs.yml` のコメント部分を有効化
- リポジトリ Settings > Pages > Source を "GitHub Actions" に設定
- ドキュメントが `https://<username>.github.io/<repo>/` で公開されます

**コスト**:
- Artifactsのみ: 無料
- GitHub Pages: Public repoは無料、Private repoはGitHub Pro必要（月$4〜）

### ベンチマーク自動実行

**トリガー**: `main`/`master` ブランチへのプッシュ、またはPR作成時

**実行内容**:
1. `benchmarks/` ディレクトリのベンチマークを実行
2. 結果をJSON形式で保存
3. PR時は前回の結果と比較（パフォーマンス劣化検出）
4. 結果をArtifactとして90日間保存

**ベンチマーク追加方法**:
```python
# benchmarks/test_performance.py
import pytest

def test_my_function_performance(benchmark):
    result = benchmark(my_function, arg1, arg2)
    assert result is not None
```

## バッジ

READMEに以下のバッジを追加すると、プロジェクトの状態を可視化できます：

```markdown
![CI](https://github.com/yuzuponikemi/python-uv-template/workflows/CI/badge.svg)
![Documentation](https://github.com/yuzuponikemi/python-uv-template/workflows/Documentation/badge.svg)
![Benchmark](https://github.com/yuzuponikemi/python-uv-template/workflows/Benchmark/badge.svg)
```

**カバレッジバッジ（オプション）**:
カバレッジレポートをGitHub Actions Artifactsで保存していますが、バッジ表示には別途サービスが必要です。
- Public repository: [Codecov](https://codecov.io/)（無料）や[Coveralls](https://coveralls.io/)（無料）を利用可能
- Private repository: 有料プランが必要（月$10〜）