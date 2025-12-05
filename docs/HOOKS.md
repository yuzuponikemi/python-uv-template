# Claude Code Hooks 設定ガイド

このドキュメントでは、このリポジトリで設定されているClaude Codeフックの説明と設定方法を解説します。

## 概要

Claude Codeフックは、特定のイベント（セッション開始、コマンド実行前後など）に自動的に実行されるスクリプトです。このリポジトリでは、セッション開始時にAI Agentのガイドラインを自動読み込みする機能を実装しています。

## 設定されているフック

### 1. SessionStart Hook

**目的**: セッション開始時に `AGENTMASTER.md` を自動的に読み込み、ClaudeにAI Agentのガイドラインを認識させる

**ファイル**: `.claude/hooks/sessionStart.sh`

**動作**:
- セッション開始時に自動実行
- `AGENTMASTER.md` の内容をClaudeのコンテキストに追加
- これにより、ClaudeはPR作成ルール、開発フロー、品質チェックなどを常に認識

**実装内容**:
```bash
#!/bin/bash
# SessionStart Hook - Read AGENTMASTER.md context
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENTMASTER_FILE="$REPO_ROOT/AGENTMASTER.md"

if [ -f "$AGENTMASTER_FILE" ]; then
    echo "📚 Loading AGENTMASTER.md context..."
    cat "$AGENTMASTER_FILE"
    echo "✅ AGENTMASTER.md loaded successfully!"
else
    echo "⚠️  Warning: AGENTMASTER.md not found"
fi
```

## ディレクトリ構造

```
.claude/
├── hooks/
│   └── sessionStart.sh          # セッション開始時のフック
├── prompts/
│   └── AGENT_MASTER_PROMPT.md   # 詳細なAIエージェントガイドライン
└── settings.json                # Claude Code設定ファイル
```

## settings.json 設定

`.claude/settings.json` でフックを有効化しています：

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/sessionStart.sh"
          }
        ]
      }
    ]
  }
}
```

### matcher の値

- `""` (空文字列): すべてのセッション開始時に実行
- `"startup"`: 新規セッション開始時のみ
- `"resume"`: セッション再開時のみ
- `"clear"`: `/clear` コマンド実行時
- `"compact"`: コンパクション時

## フックの種類

Claude Codeは以下のフックタイプをサポートしています：

| フックタイプ | 実行タイミング | 用途例 |
|------------|-------------|--------|
| `SessionStart` | セッション開始時 | コンテキスト読み込み、環境確認 |
| `BeforeCommand` | コマンド実行前 | バリデーション、警告表示 |
| `AfterCommand` | コマンド実行後 | 自動フォーマット、後処理 |
| `Stop` | セッション終了時 | クリーンアップ、状態保存 |

## フックのスコープ

### リポジトリ固有のフック（推奨）

**場所**: `.claude/hooks/`

**特徴**:
- そのリポジトリでのみ有効
- Gitでコミット・共有可能
- チーム全体で統一されたルールを適用

**例**: このリポジトリのsessionStartフック

### グローバルフック（個人設定）

**場所**: `~/.claude/hooks/`

**特徴**:
- すべてのリポジトリで有効
- 個人的な設定に最適
- Gitでは管理されない

**優先順位**: リポジトリ固有のフックが優先されます

## 手動でフックをテストする方法

フックスクリプトは通常のシェルスクリプトとして実行できます：

```bash
# SessionStartフックをテスト
.claude/hooks/sessionStart.sh

# 実行権限を確認
ls -la .claude/hooks/sessionStart.sh

# 実行権限がない場合は付与
chmod +x .claude/hooks/sessionStart.sh
```

## トラブルシューティング

### 問題1: フックが実行されない

**確認事項**:
1. `.claude/settings.json` が正しく設定されているか
   ```bash
   cat .claude/settings.json
   ```

2. フックファイルに実行権限があるか
   ```bash
   ls -la .claude/hooks/sessionStart.sh
   ```

3. フックファイルのパスが正しいか
   ```bash
   # settings.jsonの相対パスが正しいか確認
   ```

**解決策**:
```bash
# 実行権限を付与
chmod +x .claude/hooks/sessionStart.sh

# settings.jsonのsyntaxを確認
python -m json.tool .claude/settings.json
```

### 問題2: AGENTMASTER.mdが見つからない

**確認事項**:
```bash
# ファイルが存在するか確認
ls -la AGENTMASTER.md

# フックスクリプトを手動実行して確認
.claude/hooks/sessionStart.sh
```

**解決策**:
AGENTMASTER.mdがリポジトリのルートに存在することを確認してください。

### 問題3: フックのエラーメッセージが表示される

フックのエラー出力は標準エラー（stderr）に表示されます。デバッグ用に詳細ログを追加：

```bash
#!/bin/bash
set -x  # デバッグモードを有効化
# ... フックの内容 ...
```

## カスタマイズ例

### 例1: 複数のファイルを読み込む

```bash
#!/bin/bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# 複数のドキュメントを読み込み
for file in AGENTMASTER.md CONTRIBUTING.md ARCHITECTURE.md; do
    if [ -f "$REPO_ROOT/$file" ]; then
        echo "=== Loading $file ==="
        cat "$REPO_ROOT/$file"
        echo ""
    fi
done
```

### 例2: 環境情報を表示

```bash
#!/bin/bash
echo "=== Environment Info ==="
echo "Git Branch: $(git branch --show-current)"
echo "Python Version: $(python --version)"
echo "Last Commit: $(git log -1 --oneline)"
echo ""
```

### 例3: 特定の条件でのみ実行

```bash
#!/bin/bash
# mainブランチでは警告を表示
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ]; then
    echo "⚠️  Warning: You are on the main branch!"
    echo "   Consider creating a feature branch."
fi
```

## ベストプラクティス

1. **実行権限を設定**: すべてのフックスクリプトに実行権限を付与
   ```bash
   chmod +x .claude/hooks/*.sh
   ```

2. **絶対パスを使用**: スクリプト内では絶対パスを使用
   ```bash
   REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
   ```

3. **エラーハンドリング**: ファイルの存在確認を必ず行う
   ```bash
   if [ -f "$FILE" ]; then
       # 処理
   else
       echo "Warning: $FILE not found"
   fi
   ```

4. **出力を明確に**: ユーザーが理解しやすいメッセージを表示
   ```bash
   echo "📚 Loading context..."
   echo "✅ Done!"
   ```

5. **素早く実行**: フックは頻繁に実行されるため、重い処理は避ける

6. **Gitで管理**: リポジトリ固有のフックは必ずGitでコミット

## 関連ドキュメント

- [AGENTMASTER.md](../AGENTMASTER.md) - AIエージェント共通ルール
- [.claude/prompts/AGENT_MASTER_PROMPT.md](../.claude/prompts/AGENT_MASTER_PROMPT.md) - 詳細なガイドライン
- [Claude Code公式ドキュメント - Hooks](https://code.claude.com/docs/en/hooks)
- [GitHub - claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)

## まとめ

SessionStartフックにより：

✅ セッション開始時に自動的にAGENTMASTER.mdが読み込まれる
✅ ClaudeはPR作成ルールを常に認識
✅ 開発フローとベストプラクティスが自動的に適用される
✅ チーム全体で統一されたAI Agent体験

これにより、「AGENTMASTER.mdを読んで」と毎回指示する必要がなくなり、Claudeが常にプロジェクトのルールを理解した状態で作業できます！
