# AI Agent Master Instructions

このファイルは、**Claude**、**GitHub Copilot**、その他のAIコーディングエージェントがこのリポジトリで作業する際の共通ルールを定義します。

## 📋 重要な参照先

**詳細なガイドライン**: [`.claude/prompts/AGENT_MASTER_PROMPT.md`](.claude/prompts/AGENT_MASTER_PROMPT.md)

すべてのAIエージェントは、作業を開始する前に上記のマスタープロンプトを必ず確認してください。

## 🚀 クイックスタート

### Pull Request作成の厳格なルール

**最重要**: このリポジトリでPull Requestを作成する際は、以下の品質チェックを必ず経てください。

```bash
# 推奨: gh pr-strict エイリアスを使用
gh pr-strict

# または手動で実行
ruff format . && ruff check --fix . && mypy . && act push -q && gh pr create
```

#### AIエージェントへの指示

ユーザーから「PRを作成して」と依頼された際は：

1. ✅ **まず品質チェックを実行**
   - `ruff format .` - コード整形
   - `ruff check --fix .` - Lint修正
   - `mypy .` - 型チェック
   - `act push -q` - ローカルCI実行

2. ✅ **すべて成功した場合のみPR作成**
   - `gh pr-strict` を使用（推奨）
   - または `gh pr create`

3. ❌ **やってはいけないこと**
   - 単純に `gh pr create` を実行すること
   - 品質チェックをスキップすること

### 開発フロー（TDD）

```bash
# 1. テストを先に書く
nano tests/test_new_feature.py

# 2. テストが失敗することを確認
pytest tests/test_new_feature.py -v

# 3. 最小限の実装
nano src/your_module.py

# 4. ローカルCIを実行
make ci-local

# 5. すべて成功したらコミット
git add . && git commit -m "feat: Add new feature with tests"

# 6. プッシュ
git push -u origin your-branch-name

# 7. PR作成（厳格版）
gh pr-strict
```

## 📚 ドキュメント構造

```
.
├── AGENTMASTER.md                          # このファイル（簡易版）
├── .claude/
│   ├── hooks/
│   │   └── sessionStart.sh                 # セッション開始時の自動読み込み
│   ├── prompts/AGENT_MASTER_PROMPT.md      # 詳細なマスタープロンプト
│   └── settings.json                       # Claude Code設定
├── .github/copilot-instructions.md         # GitHub Copilot固有の設定
├── docs/
│   ├── GH_PR_STRICT_SETUP.md               # gh pr-strict エイリアス設定
│   └── HOOKS.md                            # フック設定ガイド
├── LOCAL_TESTING.md                        # ローカルテストガイド
├── ARCHITECTURE.md                         # プロジェクト構造
└── CONTRIBUTING.md                         # 貢献ガイド
```

## 🔄 自動読み込み（SessionStartフック）

**このファイルは自動的に読み込まれます！**

`.claude/hooks/sessionStart.sh` により、Claudeのセッション開始時にこのAGENTMASTER.mdが自動的に読み込まれます。

つまり、**毎回「AGENTMASTER.mdを読んで」と指示する必要はありません**。Claudeは常にこのルールを認識した状態で作業を開始します。

### フックの仕組み

- **トリガー**: Claude Codeセッション開始時
- **動作**: AGENTMASTER.mdの内容をClaudeのコンテキストに追加
- **効果**: PR作成ルール、開発フロー、品質チェックを常に認識

詳細は [`docs/HOOKS.md`](docs/HOOKS.md) を参照してください。

## ⚡ よく使うコマンド

```bash
# すべてのCIチェック（最も重要）
make ci-local

# テスト実行
make test

# コード整形
make format

# Lint実行
make lint

# 型チェック
make typecheck

# セキュリティチェック
make security
```

## 🎯 核となる原則

1. **TDD（テスト駆動開発）** - テストを先に書く
2. **品質チェック必須** - PR作成前に必ず `make ci-local` を実行
3. **型ヒント必須** - すべての関数に型ヒントを追加
4. **Docstring必須** - NumPyまたはGoogle styleで記述
5. **過剰な抽象化を避ける** - 必要最小限のコードを書く

## 🔧 GitHub CLIエイリアス設定

`gh pr-strict` エイリアスの設定方法は [`docs/GH_PR_STRICT_SETUP.md`](docs/GH_PR_STRICT_SETUP.md) を参照してください。

## 📖 詳細情報

すべての詳細なガイドライン、ベストプラクティス、トラブルシューティング情報は以下を参照：

👉 [`.claude/prompts/AGENT_MASTER_PROMPT.md`](.claude/prompts/AGENT_MASTER_PROMPT.md)

---

**Note**: このファイルは簡易リファレンスです。詳細な指示は必ずマスタープロンプトを確認してください。
