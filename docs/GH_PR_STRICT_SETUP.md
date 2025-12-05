# GitHub CLI `gh pr-strict` エイリアス設定ガイド

このガイドでは、Pull Request作成時に品質チェックを強制する `gh pr-strict` カスタムエイリアスの設定方法を説明します。

## 概要

`gh pr-strict` エイリアスは、Pull Requestを作成する前に以下のチェックを自動で実行します：

1. **`ruff format .`** - コード整形
2. **`ruff check --fix .`** - Lint修正
3. **`mypy .`** - 型チェック
4. **`act push -q`** - ローカルでのGitHub Actions実行
5. **すべて成功した場合のみ `gh pr create`** を実行

これにより、品質基準を満たさないPRが作成されることを防ぎます。

## 前提条件

以下のツールがインストールされている必要があります：

- [GitHub CLI (`gh`)](https://cli.github.com/)
- [ruff](https://docs.astral.sh/ruff/)
- [mypy](https://mypy.readthedocs.io/)
- [act](https://github.com/nektos/act)

このリポジトリでは、これらは `requirements-dev.txt` に含まれています：

```bash
make install
```

## エイリアス設定方法

### 方法1: GitHub CLI コマンドで設定（推奨）

最も簡単な方法は、`gh alias set` コマンドを使用することです：

```bash
gh alias set pr-strict '!f() {
  echo "🔍 Running quality checks..."

  # Step 1: Code formatting
  echo "📝 Formatting code with ruff..."
  ruff format . || { echo "❌ Formatting failed"; return 1; }

  # Step 2: Linting with auto-fix
  echo "🔧 Linting code with ruff..."
  ruff check --fix . || { echo "❌ Linting failed"; return 1; }

  # Step 3: Type checking
  echo "🔍 Type checking with mypy..."
  mypy . || { echo "❌ Type checking failed"; return 1; }

  # Step 4: Local CI
  echo "🚀 Running local CI with act..."
  act push -q || { echo "❌ Local CI failed"; return 1; }

  # Step 5: Create PR if all checks pass
  echo "✅ All checks passed! Creating PR..."
  gh pr create "$@"
}; f'
```

### 方法2: 設定ファイルを直接編集

GitHub CLIの設定ファイルを直接編集することもできます：

1. 設定ファイルを開く：
   ```bash
   nano ~/.config/gh/config.yml
   ```

2. `aliases:` セクションに以下を追加：
   ```yaml
   aliases:
       pr-strict: '!f() { echo "🔍 Running quality checks..."; echo "📝 Formatting code with ruff..."; ruff format . || { echo "❌ Formatting failed"; return 1; }; echo "🔧 Linting code with ruff..."; ruff check --fix . || { echo "❌ Linting failed"; return 1; }; echo "🔍 Type checking with mypy..."; mypy . || { echo "❌ Type checking failed"; return 1; }; echo "🚀 Running local CI with act..."; act push -q || { echo "❌ Local CI failed"; return 1; }; echo "✅ All checks passed! Creating PR..."; gh pr create "$@"; }; f'
   ```

3. ファイルを保存して閉じる（`Ctrl+O` → `Enter` → `Ctrl+X`）

## 使用方法

### 基本的な使い方

```bash
# インタラクティブモードでPR作成
gh pr-strict

# タイトルと本文を指定してPR作成
gh pr-strict --title "feat: Add new feature" --body "Description of changes"

# ドラフトPRとして作成
gh pr-strict --draft

# 特定のベースブランチに対してPR作成
gh pr-strict --base main
```

### すべてのオプション

`gh pr-strict` は `gh pr create` と同じオプションをすべて使用できます：

```bash
gh pr-strict --title "Title" \
             --body "Description" \
             --draft \
             --base main \
             --head feature-branch \
             --reviewer @username \
             --assignee @me \
             --label bug,enhancement \
             --milestone "v1.0"
```

利用可能なオプションの完全なリストは以下で確認できます：
```bash
gh pr create --help
```

## トラブルシューティング

### 問題1: エイリアスが見つからない

```bash
gh: Unknown command 'pr-strict'
```

**解決策**:
```bash
# エイリアスが正しく設定されているか確認
gh alias list

# 設定されていない場合は再度設定
gh alias set pr-strict '!f() { ... }; f'
```

### 問題2: ruff/mypy/actが見つからない

```bash
command not found: ruff
```

**解決策**:
```bash
# 開発用依存関係をインストール
make install

# または直接インストール
pip install ruff mypy
```

actのインストール方法は[公式ドキュメント](https://github.com/nektos/act#installation)を参照してください。

### 問題3: ローカルCIが失敗する

```bash
❌ Local CI failed
```

**解決策**:
1. 詳細なログを確認：
   ```bash
   act push -v
   ```

2. Dockerが起動しているか確認：
   ```bash
   docker ps
   ```

3. 詳細なトラブルシューティングは [`LOCAL_TESTING.md`](../LOCAL_TESTING.md) を参照

### 問題4: エイリアスをスキップしてPRを作成したい

緊急時やデバッグ目的で品質チェックをスキップしたい場合：

```bash
# 通常のgh pr createを使用（非推奨）
gh pr create --title "Emergency fix" --body "Bypassing checks"
```

⚠️ **注意**: これは緊急時のみにしてください。通常は必ず `gh pr-strict` を使用してください。

## エイリアスの確認

設定したエイリアスの内容を確認：

```bash
gh alias list
```

特定のエイリアスの詳細を表示：

```bash
gh alias list pr-strict
```

## エイリアスの削除

エイリアスが不要になった場合：

```bash
gh alias delete pr-strict
```

## カスタマイズ

エイリアスの動作をカスタマイズすることもできます：

### 例1: actのチェックをスキップ

```bash
gh alias set pr-strict-no-act '!f() {
  ruff format . && ruff check --fix . && mypy . && gh pr create "$@"
}; f'
```

### 例2: テストも実行

```bash
gh alias set pr-strict-with-tests '!f() {
  ruff format . && ruff check --fix . && mypy . && pytest && act push -q && gh pr create "$@"
}; f'
```

### 例3: カバレッジチェックも含める

```bash
gh alias set pr-strict-coverage '!f() {
  ruff format . && ruff check --fix . && mypy . && pytest --cov=src --cov-report=term-missing --cov-fail-under=80 && act push -q && gh pr create "$@"
}; f'
```

## 関連ドキュメント

- [GitHub CLI公式ドキュメント](https://cli.github.com/manual/)
- [GitHub CLI エイリアス](https://cli.github.com/manual/gh_alias)
- [ruff公式ドキュメント](https://docs.astral.sh/ruff/)
- [mypy公式ドキュメント](https://mypy.readthedocs.io/)
- [act公式ドキュメント](https://github.com/nektos/act)
- [ローカルテストガイド](../LOCAL_TESTING.md)
- [AIエージェントマスタープロンプト](../.claude/prompts/AGENT_MASTER_PROMPT.md)

## まとめ

`gh pr-strict` エイリアスを使用することで：

✅ コード品質が自動的に保証される
✅ CI/CDの失敗が減る
✅ レビュワーの負担が軽減される
✅ チーム全体のコード品質が向上する

このリポジトリでPull Requestを作成する際は、必ず `gh pr-strict` を使用してください！
