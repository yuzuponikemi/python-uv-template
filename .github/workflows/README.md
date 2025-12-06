# GitHub Actions ワークフローのローカルテスト

このディレクトリのすべてのワークフローは [act](https://github.com/nektos/act) を使用してローカルでテスト可能です。

## actのインストール

### macOS (Homebrew)
```bash
brew install act
```

### Linux
```bash
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

### Windows (Chocolatey)
```bash
choco install act-cli
```

詳細は [act公式ドキュメント](https://github.com/nektos/act#installation) を参照してください。

## 基本的な使い方

### すべてのワークフローを実行
```bash
act
```

### 特定のイベントでトリガー
```bash
act push              # push イベント
act pull_request      # pull_request イベント
act workflow_dispatch # 手動トリガー
```

### 特定のジョブのみ実行
```bash
act -j test           # CI の test ジョブのみ
act -j benchmark      # Benchmark の benchmark ジョブのみ
act -j build          # Documentation の build ジョブのみ
```

### Apple Silicon (M1/M2/M3) Macの場合
```bash
act --container-architecture linux/amd64
```

## ワークフロー別のテスト方法

### 1. CI (`ci.yml`)
**推奨度: ⭐⭐⭐⭐⭐ (完全にローカルテスト可能)**

```bash
# push イベントでテスト
act push

# pull_request イベントでテスト
act pull_request

# 手動トリガーでテスト
act workflow_dispatch
```

**機能:**
- ✅ 依存関係のインストール
- ✅ pre-commit フック
- ✅ ruff linter/formatter
- ✅ mypy 型チェック
- ✅ bandit セキュリティチェック
- ✅ pytest カバレッジ
- ✅ アーティファクトのアップロード

### 2. Benchmark (`benchmark.yml`)
**推奨度: ⭐⭐⭐⭐☆ (ほぼ完全にローカルテスト可能)**

```bash
# push イベントでテスト
act push

# pull_request イベントでテスト
act pull_request

# 手動トリガーでテスト
act workflow_dispatch
```

**機能:**
- ✅ ベンチマーク実行
- ✅ 結果のJSON出力
- ✅ アーティファクトのアップロード
- ⚠️ PRコメント (ACT環境ではスキップ)
- ⚠️ キャッシュ比較 (ACT環境では制限あり)

### 3. Documentation (`docs.yml`)
**推奨度: ⭐⭐⭐⭐⭐ (完全にローカルテスト可能)**

```bash
# push イベントでテスト
act push

# 手動トリガーでテスト
act workflow_dispatch

# build ジョブのみ実行
act -j build
```

**機能:**
- ✅ Sphinxドキュメントのビルド
- ✅ アーティファクトのアップロード
- ❌ GitHub Pagesへのデプロイ (本番環境のみ)

### 4. Auto-fix (`auto-fix.yml`)
**推奨度: ⭐⭐☆☆☆ (限定的なローカルテスト)**

```bash
# 手動トリガーでテスト (simulate_failure=true)
act workflow_dispatch -e .github/workflows/test-events/auto-fix.json
```

**注意:**
- `workflow_run` イベントは act でサポートされていないため、`workflow_dispatch` でテスト
- ❌ GitHub Issue作成 (ACT環境ではスキップ)
- ❌ アーティファクトのダウンロード (workflow_run からのみ)
- ✅ エラーコンテキストの準備

**テスト用イベントファイル作成:**
```bash
mkdir -p .github/workflows/test-events
cat > .github/workflows/test-events/auto-fix.json <<EOF
{
  "inputs": {
    "simulate_failure": "true"
  }
}
EOF
```

### 5. Release (`release.yml`)
**推奨度: ⭐⭐⭐⭐☆ (ビルドとテストは可能)**

```bash
# 手動トリガーでテスト
act workflow_dispatch

# タグpushイベントでテスト (イベントファイルが必要)
act push -e .github/workflows/test-events/release.json
```

**機能:**
- ✅ パッケージビルド
- ✅ Changelogの生成
- ✅ dist/ ディレクトリへの出力
- ❌ GitHub Release作成 (ACT環境ではスキップ)
- ❌ PyPI公開 (ACT環境ではスキップ)

**テスト用イベントファイル作成:**
```bash
cat > .github/workflows/test-events/release.json <<EOF
{
  "ref": "refs/tags/v0.0.0-test",
  "repository": {
    "name": "python-uv-template",
    "owner": {
      "name": "test-user"
    }
  }
}
EOF
```

### 6. Claude Code (`claude-code.yml`)
**推奨度: ⭐☆☆☆☆ (ローカルテスト不推奨)**

このワークフローは以下の理由でローカルテストが困難です:
- GitHub webhook イベント (`issue_comment` など) に依存
- `ANTHROPIC_API_KEY` シークレットが必要
- `claude-code-action` が GitHub API へのアクセスを必要とする

**代替案:**
- CI ワークフローをローカルでテストする (Claude が修正する対象)
- auto-fix ワークフローで生成されるエラーコンテキストを確認

## 高度な使い方

### ドライラン（実行せずに確認）
```bash
act -n
```

### 特定のワークフローファイルのみ実行
```bash
act -W .github/workflows/ci.yml
```

### デバッグモード
```bash
act -v
```

### シークレットの設定
```bash
# .secretsファイルを作成
cat > .secrets <<EOF
ANTHROPIC_API_KEY=your_api_key_here
GITHUB_TOKEN=your_github_token
EOF

# シークレットを使って実行
act --secret-file .secrets
```

**重要:** `.secrets` ファイルは `.gitignore` に追加してコミットしないでください！

### 環境変数の設定
```bash
# .env ファイルを作成
cat > .env <<EOF
PYTHONHASHSEED=0
NUMBA_CACHE_DIR=/tmp/numba_cache
EOF

# 環境変数を使って実行
act --env-file .env
```

### Dockerイメージの選択

デフォルトでは、act は小さなDockerイメージを使用しますが、GitHub Actionsの環境に近いイメージを使うこともできます:

```bash
# Medium サイズ (推奨)
act -P ubuntu-latest=catthehacker/ubuntu:act-latest

# Large サイズ (GitHub Actions に最も近い)
act -P ubuntu-latest=catthehacker/ubuntu:full-latest
```

## トラブルシューティング

### act が `ACT` 環境変数を設定しない場合
一部の古いバージョンの act では `ACT` 環境変数が設定されないことがあります。最新版にアップデートしてください:

```bash
brew upgrade act  # macOS
```

### Dockerのディスク容量不足
```bash
# 未使用のDockerリソースをクリーンアップ
docker system prune -a
```

### パーミッションエラー
```bash
# Linux/macOS でDocker権限が必要な場合
sudo act
```

### Apple Silicon での実行エラー
```bash
# x86_64 アーキテクチャを明示的に指定
act --container-architecture linux/amd64
```

## ベストプラクティス

1. **頻繁にローカルテストする**: プッシュする前にローカルでCIを実行
2. **特定のジョブをテスト**: `-j` オプションで高速に特定部分をテスト
3. **ドライランで確認**: `-n` で何が実行されるか事前確認
4. **シークレットは安全に**: `.secrets` ファイルを `.gitignore` に追加

## 参考リンク

- [LOCAL_TESTING.md](../../LOCAL_TESTING.md) - actの詳細なセットアップガイドとトラブルシューティング
- [act 公式ドキュメント](https://github.com/nektos/act)
- [act のトラブルシューティング](https://github.com/nektos/act/blob/master/TROUBLESHOOTING.md)
- [GitHub Actions ドキュメント](https://docs.github.com/ja/actions)

## ACT環境でスキップされる機能

以下の機能は ACT 環境（`ACT` 環境変数が設定されている）では自動的にスキップされます:

- GitHub Issue/PR へのコメント作成
- GitHub Release の作成
- PyPI への公開
- workflow_run イベント からのアーティファクトダウンロード
- GitHub API を使用する actions/github-script

これらの機能をテストするには、実際のGitHub Actions環境を使用してください。
