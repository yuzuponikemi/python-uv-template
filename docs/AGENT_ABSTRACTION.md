# コーディングエージェント抽象化レイヤー

このドキュメントでは、複数のAIコーディングエージェントを統一インターフェースで利用できる抽象化レイヤーについて説明します。

## 概要

このテンプレートは、複数のコーディングエージェントをサポートしています：

- **Claude Code** (Anthropic)
- **Gemini** (Google)
- **Codex/GPT** (OpenAI)
- **SWE-agent** (オープンソース)

抽象化レイヤーにより、エージェントを簡単に切り替えることができ、各エージェントの特性を活かした開発が可能です。

## エージェントの選択

### 設定ファイルによる選択

`.agent-config.yml` ファイルでデフォルトのエージェントを設定できます：

```yaml
agent:
  type: claude_code  # claude_code, gemini, codex, swe_agent
  model: claude-sonnet-4-5-20250929
  max_tokens: 4096
  temperature: 0.7
```

### 環境変数による選択

環境変数でエージェントを指定することもできます：

```bash
export CODING_AGENT_TYPE=gemini
export CODING_AGENT_MODEL=gemini-2.0-flash-exp
```

## エージェント比較

| エージェント | 強み | 推奨用途 |
|------------|------|---------|
| **Claude Code** | TDD、研究ソフトウェア、GitHub統合 | 研究プロジェクト、自動CI修正 |
| **Gemini** | 高速、長コンテキスト、マルチモーダル | 大規模コードベース、画像処理 |
| **Codex/GPT** | 汎用性、関数呼び出し | 一般的な開発タスク |
| **SWE-agent** | 自律デバッグ、オープンソース | バグ修正、リポジトリナビゲーション |

## Python APIの使用

### 基本的な使い方

```python
from src.agent_abstraction import AgentFactory, AgentType

# エージェントを作成
agent = AgentFactory.create_agent(
    agent_type=AgentType.CLAUDE_CODE,
    api_key="your_api_key",
    model="claude-sonnet-4-5-20250929"
)

# タスクを処理
response = agent.process_task(
    task="新しいデータ処理関数を実装してください",
    context={"issue_number": 123}
)

print(response.message)
print(response.changes)
```

### 設定ファイルから読み込み

```python
from src.agent_abstraction import ConfigLoader, AgentFactory

# 設定を読み込む
config = ConfigLoader.load_from_file(".agent-config.yml")

# エージェントを作成
agent = AgentFactory.create_from_config(config)

# CI エラーを修正
response = agent.fix_ci_errors(
    error_logs={
        "pytest": "test_calculator.py::test_add FAILED",
        "mypy": "error: Incompatible types in assignment"
    },
    branch="main"
)
```

### コードレビュー

```python
# Git diffをレビュー
diff = """
--- a/src/calculator.py
+++ b/src/calculator.py
@@ -1,5 +1,8 @@
 def add(a, b):
-    return a + b
+    return a + b + 1  # Bug!
"""

response = agent.review_code(
    diff=diff,
    context={"pr_number": 456}
)

print(response.message)
```

## GitHub Actionsでの使用

### 自動トリガー

Issue や PR で `@claude` または `@ai` とメンションすると、設定されたエージェントが自動的に実行されます：

```markdown
新しい機能を実装してください @claude

要件:
- CSVファイルを読み込む
- データを正規化する
- 結果をプロットする
```

### エージェントの切り替え

一時的に別のエージェントを使用したい場合は、`.agent-config.yml` を編集してコミットします：

```bash
# Gemini に切り替え
sed -i 's/type: claude_code/type: gemini/' .agent-config.yml
git add .agent-config.yml
git commit -m "Switch to Gemini agent"
git push
```

次回の `@ai` メンションから Gemini が使用されます。

## エージェント固有の機能

### Claude Code

```python
from src.agent_abstraction import ClaudeCodeAgent, AgentConfig, AgentType

config = AgentConfig(
    agent_type=AgentType.CLAUDE_CODE,
    api_key="your_key",
    custom_settings={
        "tdd_mode": True,
        "research_software_mode": True
    }
)

agent = ClaudeCodeAgent(config)
capabilities = agent.get_capabilities()
# {
#     "github_integration": True,
#     "auto_fix_ci": True,
#     "tdd_support": True,
#     "research_software": True
# }
```

### Gemini

```python
from src.agent_abstraction import GeminiAgent, AgentConfig, AgentType

config = AgentConfig(
    agent_type=AgentType.GEMINI,
    api_key="your_key",
    model="gemini-2.0-flash-exp",
    custom_settings={
        "multimodal": True
    }
)

agent = GeminiAgent(config)
# 長いコンテキストに対応
# マルチモーダル入力をサポート
```

### SWE-agent

```python
from src.agent_abstraction import SWEAgent, AgentConfig, AgentType

config = AgentConfig(
    agent_type=AgentType.SWE_AGENT,
    api_key="your_key",
    custom_settings={
        "autonomous_mode": True,
        "backend": "openai"
    }
)

agent = SWEAgent(config)
# 自律的なデバッグ
# リポジトリナビゲーション
```

## カスタムエージェントの追加

新しいエージェントを追加することもできます：

```python
from src.agent_abstraction import BaseAgent, AgentConfig, AgentFactory, AgentType

class MyCustomAgent(BaseAgent):
    def _validate_config(self):
        # 設定を検証
        pass

    def process_task(self, task, context=None):
        # タスクを処理
        pass

    def fix_ci_errors(self, error_logs, branch):
        # CI エラーを修正
        pass

    def review_code(self, diff, context=None):
        # コードをレビュー
        pass

# カスタムエージェントを登録
AgentFactory.register_agent(
    AgentType.CUSTOM,  # 新しいタイプを定義
    MyCustomAgent
)
```

## トラブルシューティング

### API キーが見つからない

```bash
# .env ファイルに API キーを設定
cp .env.example .env
# .env を編集して API キーを追加
```

### エージェントが応答しない

1. GitHub Secrets に API キーが設定されているか確認
2. `.agent-config.yml` の設定を確認
3. GitHub Actions のログを確認

### 型エラーが発生する

```bash
# 型スタブをインストール
pip install types-PyYAML
```

## まとめ

抽象化レイヤーにより：

- ✅ 複数のエージェントを統一インターフェースで利用
- ✅ 簡単なエージェント切り替え
- ✅ 各エージェントの特性を活かした開発
- ✅ カスタムエージェントの追加が可能

詳細は各エージェントのドキュメントを参照してください。
