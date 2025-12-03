# ローカルでのGitHub Actionsテスト

このドキュメントでは、`act`を使用してGitHub Actionsワークフローをローカルマシンでテストする方法を説明します。

## 目次

- [概要](#概要)
- [前提条件](#前提条件)
- [初期セットアップ](#初期セットアップ)
- [ワークフローの実行方法](#ワークフローの実行方法)
- [トラブルシューティング](#トラブルシューティング)
- [AI Agentとの統合](#ai-agentとの統合)

## 概要

`act`を使用することで、以下のメリットがあります：

- **高速な開発サイクル**: GitHub ActionsにプッシュせずにローカルでCI/CDをテスト
- **コスト削減**: GitHub Actionsの実行時間を節約
- **デバッグの容易さ**: ローカル環境でステップバイステップでデバッグ可能
- **オフライン開発**: インターネット接続なしでワークフローをテスト

## 前提条件

以下をインストールしてください：

### 1. Dockerのインストール

```bash
# macOS (Homebrew)
brew install --cask docker

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Fedora/RHEL
sudo dnf install docker docker-compose

# Dockerデーモンの起動
sudo systemctl start docker
sudo systemctl enable docker

# 現在のユーザーをdockerグループに追加（再ログイン必要）
sudo usermod -aG docker $USER
```

### 2. actのインストール

```bash
# macOS (Homebrew)
brew install act

# Linux (curl)
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows (Chocolatey)
choco install act-cli

# または、GitHub Releasesから直接ダウンロード
# https://github.com/nektos/act/releases
```

### 3. インストールの確認

```bash
# Dockerの確認
docker --version
docker ps

# actの確認
act --version
```

## 初期セットアップ

### 1. シークレットファイルのセットアップ

```bash
# サンプルファイルをコピー
cp .secrets.example .secrets

# エディタで開いて実際の値を設定
nano .secrets  # または vim, code, etc.
```

`.secrets`ファイルに以下を設定：

```bash
# Anthropic API Key (Claude Code用)
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here

# GitHub Token (オプション: Claude Codeが必要な場合)
GITHUB_TOKEN=ghp_your-github-token-here

# PyPI Token (オプション: リリースワークフロー用)
PYPI_API_TOKEN=pypi-your-token-here
```

**重要**: `.secrets`ファイルはGitにコミットしないでください（`.gitignore`に含まれています）

### 2. 環境変数ファイルのセットアップ（オプション）

```bash
# サンプルファイルをコピー
cp .github/workflows/.env.local.example .github/workflows/.env.local

# 必要に応じてカスタマイズ
nano .github/workflows/.env.local
```

### 3. actの設定確認

`.actrc`ファイルがプロジェクトルートに作成されており、以下の設定が含まれています：

- 使用するDockerイメージ: `catthehacker/ubuntu:act-latest`
- シークレットファイル: `.secrets`
- 環境変数ファイル: `.github/workflows/.env.local`

## ワークフローの実行方法

### 利用可能なワークフロー

このプロジェクトには以下のワークフローがあります：

1. **CI** (`ci.yml`) - テスト、リンター、型チェック、セキュリティチェック
2. **Auto-fix** (`auto-fix.yml`) - CI失敗時の自動修正（Claude Code）
3. **Claude Code** (`claude-code.yml`) - Issueでの@claudeメンション対応
4. **Release** (`release.yml`) - タグベースの自動リリース
5. **Docs** (`docs.yml`) - ドキュメントのビルド
6. **Benchmark** (`benchmark.yml`) - パフォーマンステスト

### 基本的な使い方

#### 1. 利用可能なワークフローをリスト表示

```bash
act -l
```

#### 2. CIワークフローを実行（最も一般的）

```bash
# 完全なCIワークフローを実行
act -j test

# または、pushイベントをシミュレート
act push
```

#### 3. 特定のイベントをトリガー

```bash
# プルリクエストイベント
act pull_request

# タグプッシュ（リリース）
act -e .github/workflows/test-events/tag-push.json
```

#### 4. ドライラン（実行せずに確認）

```bash
act -n
```

#### 5. 詳細ログ付きで実行

```bash
act -v
```

#### 6. 特定のジョブのみ実行

```bash
# CI jobのみ
act -j test

# 複数のジョブを指定
act -j test -j lint
```

### 高度な使い方

#### イベントペイロードをカスタマイズ

```bash
# カスタムイベントペイロードを使用
act -e my-custom-event.json
```

`my-custom-event.json`の例：

```json
{
  "push": {
    "ref": "refs/heads/main",
    "repository": {
      "name": "python-uv-template",
      "owner": {
        "login": "yuzuponikemi"
      }
    }
  }
}
```

#### 特定の環境変数を上書き

```bash
# コマンドラインで環境変数を設定
act -e PYTHON_VERSION=3.12
```

#### コンテナを再利用（高速化）

```bash
# コンテナを再利用して実行時間を短縮
act --reuse
```

#### 対話的にデバッグ

```bash
# 失敗したステップで停止し、シェルに入る
act -b
```

### ワークフロー別の実行例

#### CIワークフロー（推奨）

```bash
# ローカルブランチでCIを実行
act push -j test

# 特定のPythonバージョンでテスト（環境変数で指定）
act push -j test -e PYTHON_VERSION=3.11
```

#### ドキュメントビルド

```bash
# ドキュメントをビルド
act -W .github/workflows/docs.yml
```

#### ベンチマーク

```bash
# ベンチマークを実行
act -W .github/workflows/benchmark.yml
```

## トラブルシューティング

### よくある問題と解決策

#### 1. "Error: Container failed to start"

**原因**: Dockerが起動していない、またはユーザーがdockerグループに属していない

**解決策**:
```bash
# Dockerを起動
sudo systemctl start docker

# 現在のユーザーをdockerグループに追加
sudo usermod -aG docker $USER

# 再ログインまたはログアウト/ログイン
```

#### 2. "Secret not found"

**原因**: `.secrets`ファイルが正しく設定されていない

**解決策**:
```bash
# .secretsファイルを作成
cp .secrets.example .secrets

# 実際のシークレットを設定
nano .secrets
```

#### 3. "Image not found"

**原因**: 必要なDockerイメージがダウンロードされていない

**解決策**:
```bash
# イメージを手動でプル
docker pull catthehacker/ubuntu:act-latest
```

#### 4. ワークフローが特定のステップで失敗する

**解決策**:
```bash
# 詳細ログを有効にして再実行
act -v

# または、特定のステップまで実行してデバッグモードに入る
act -b
```

#### 5. メモリ不足エラー

**原因**: Dockerに割り当てられたメモリが不足

**解決策**:
```bash
# Docker Desktopの設定でメモリを増やす（macOS/Windows）
# または、システムのスワップを増やす（Linux）

# 軽量イメージを使用（.actrcで設定）
-P ubuntu-latest=node:16-buster-slim
```

### デバッグのヒント

#### ログファイルの確認

```bash
# actのログをファイルに保存
act -v 2>&1 | tee act-debug.log
```

#### コンテナ内部に入る

```bash
# 実行中のコンテナを確認
docker ps

# コンテナ内に入る
docker exec -it <container-id> /bin/bash
```

#### actの設定を確認

```bash
# 現在の設定を表示
cat .actrc

# 使用されるイメージを確認
act -l
```

## AI Agentとの統合

このプロジェクトはClaudeやGitHub Copilotなどのコーディングエージェントと連携するように設計されています。

### 推奨ワークフロー

1. **ローカル開発**: AIエージェントがコードを変更
2. **ローカルテスト**: `act`でCIを実行してエラーを検出
3. **修正**: AIエージェントがエラーを修正
4. **再テスト**: `act`で再度テスト
5. **コミット**: すべてのチェックが通ったらコミット・プッシュ

### AIエージェント用コマンド

エージェントが使用できる基本コマンド：

```bash
# CIを実行（テスト、リンター、型チェック）
make ci-local

# または直接actを実行
act push -j test

# 特定のチェックのみ実行
act push -j test --env ACT_TEST_ONLY=true
```

**注意**: エージェント用のマスタープロンプトは`.claude/prompts/AGENT_MASTER_PROMPT.md`に記載されています。

### CI統合のベストプラクティス

#### 1. コミット前に常にローカルCIを実行

```bash
# pre-commitフックに追加（オプション）
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
echo "Running local CI checks with act..."
act push -j test --quiet
if [ $? -ne 0 ]; then
    echo "CI checks failed. Push aborted."
    exit 1
fi
EOF

chmod +x .git/hooks/pre-push
```

#### 2. Makefileを使った統合

`Makefile`に以下のターゲットが既に含まれています：

```makefile
.PHONY: ci-local
ci-local:
	@echo "Running CI locally with act..."
	act push -j test
```

使用方法：
```bash
make ci-local
```

#### 3. エージェントプロンプトでの使用

エージェントに以下のように指示できます：

```
変更を加えたら、必ず以下のコマンドでローカルCIをテストしてください：
```bash
make ci-local
```

すべてのチェックが通ることを確認してから、コミット・プッシュしてください。
```

## 参考リンク

- [act公式ドキュメント](https://github.com/nektos/act)
- [GitHub Actions公式ドキュメント](https://docs.github.com/en/actions)
- [Docker公式ドキュメント](https://docs.docker.com/)

## サポート

問題が発生した場合は、以下を確認してください：

1. `act --version`でactのバージョンが最新か
2. `docker ps`でDockerが正常に動作しているか
3. `.secrets`ファイルが正しく設定されているか
4. `.actrc`ファイルが存在するか

それでも解決しない場合は、Issueを作成してください。
