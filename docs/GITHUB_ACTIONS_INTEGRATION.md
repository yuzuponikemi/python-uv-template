# GitHub Actions統合ガイド

このドキュメントでは、各エージェントをGitHub Actionsで使用するための設定手順を説明します。

## 目次

1. [共通設定](#1-共通設定)
2. [Claude Code](#2-claude-code)
3. [Google Gemini](#3-google-gemini)
4. [GitHub Copilot](#4-github-copilot)
5. [SWE-agent](#5-swe-agent)
6. [複数エージェントの併用](#6-複数エージェントの併用)

---

## 1. 共通設定

### 1.1 リポジトリSecretsの設定

すべてのエージェントで必要な手順:

1. GitHubリポジトリを開く
2. **Settings** > **Secrets and variables** > **Actions**
3. **New repository secret** をクリック

### 1.2 基本ワークフロー構造

`.github/workflows/coding-agent.yml` は自動的にエージェントを検出します:

```yaml
name: Coding Agent

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]
  pull_request_review:
    types: [submitted]

jobs:
  detect-agent:
    runs-on: ubuntu-latest
    outputs:
      agent_type: ${{ steps.config.outputs.agent_type }}
    steps:
      - uses: actions/checkout@v5
      - name: Read agent configuration
        id: config
        run: |
          AGENT_TYPE=$(grep -A 1 '^agent:' .agent-config.yml | grep 'type:' | awk '{print $2}')
          echo "agent_type=${AGENT_TYPE}" >> $GITHUB_OUTPUT
```

---

## 2. Claude Code

### 2.1 Secretsの設定

**必須:**
- `ANTHROPIC_API_KEY`: Anthropic APIキー

### 2.2 ワークフロー設定

既存の `.github/workflows/claude-code.yml` または `.github/workflows/coding-agent.yml` を使用:

```yaml
claude-code:
  needs: detect-agent
  if: needs.detect-agent.outputs.agent_type == 'claude_code'
  runs-on: ubuntu-latest
  permissions:
    contents: write
    pull-requests: write
    issues: write
    id-token: write
    actions: read
  steps:
    - uses: actions/checkout@v5

    - name: Run Claude Code
      uses: anthropics/claude-code-action@v1
      with:
        anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
        claude_args: |
          --allowedTools "Bash(uv *),Bash(pytest*),Bash(ruff*),Bash(mypy*)"
          --system-prompt "You are assisting with research software development..."
```

### 2.3 使用方法

Issue/PRで `@claude` とメンション:

```markdown
新しいデータ処理関数を実装してください @claude

要件:
- TDDで実装
- 型ヒント付き
```

---

## 3. Google Gemini

### 3.1 Secretsの設定

**必須:**
- `GOOGLE_API_KEY`: Google AI Studio APIキー

### 3.2 カスタムワークフローの作成

`.github/workflows/gemini-agent.yml`:

```yaml
name: Gemini Agent

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  gemini-agent:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@ai')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@ai'))
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install google-generativeai pyyaml
          pip install -r requirements.txt

      - name: Load configuration
        id: config
        run: |
          python - <<'EOF'
          import yaml
          import os

          with open('.agent-config.yml') as f:
              config = yaml.safe_load(f)

          model = config.get('gemini', {}).get('model', 'gemini-2.0-flash-exp')
          print(f"model={model}")

          with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
              f.write(f"model={model}\n")
          EOF

      - name: Run Gemini Agent
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python - <<'EOF'
          import os
          import json
          from pathlib import Path
          from src.agent_abstraction import AgentFactory, AgentType

          # Get task from issue/PR comment
          event_path = os.environ['GITHUB_EVENT_PATH']
          with open(event_path) as f:
              event = json.load(f)

          if 'comment' in event:
              task = event['comment']['body']
          elif 'issue' in event:
              task = event['issue']['body']
          else:
              print("No task found")
              exit(0)

          # Create agent
          agent = AgentFactory.create_agent(
              agent_type=AgentType.GEMINI,
              api_key=os.environ['GOOGLE_API_KEY'],
              model="${{ steps.config.outputs.model }}"
          )

          # Process task
          response = agent.process_task(task)

          # Post result as comment
          print(response.message)

          # TODO: Post comment to GitHub using gh CLI
          EOF

      - name: Post result to GitHub
        if: always()
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Use gh CLI to post comment
          gh issue comment ${{ github.event.issue.number }} \
            --body "Gemini agent completed. See workflow logs for details."
```

### 3.3 簡易版: Pythonスクリプト使用

`.github/workflows/gemini-simple.yml`:

```yaml
name: Gemini Agent (Simple)

on:
  workflow_dispatch:
    inputs:
      task:
        description: 'Task to perform'
        required: true

jobs:
  run-gemini:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install google-generativeai
          pip install -r requirements.txt

      - name: Run Gemini
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
        run: |
          python scripts/run_gemini_agent.py "${{ inputs.task }}"
```

`scripts/run_gemini_agent.py`:

```python
#!/usr/bin/env python3
"""Run Gemini agent from GitHub Actions."""

import os
import sys
from src.agent_abstraction import AgentFactory, AgentType

def main():
    if len(sys.argv) < 2:
        print("Usage: run_gemini_agent.py <task>")
        sys.exit(1)

    task = sys.argv[1]

    # Create agent
    agent = AgentFactory.create_agent(
        agent_type=AgentType.GEMINI,
        api_key=os.environ['GOOGLE_API_KEY'],
        model="gemini-2.0-flash-exp"
    )

    # Process task
    response = agent.process_task(task)

    print("=" * 60)
    print("GEMINI AGENT RESPONSE")
    print("=" * 60)
    print(response.message)
    print("=" * 60)
    print(f"Success: {response.success}")
    print(f"Changes: {response.changes}")

if __name__ == "__main__":
    main()
```

---

## 4. GitHub Copilot

### 4.1 Secretsの設定

**必須:**
- `OPENAI_API_KEY`: OpenAI APIキー（Copilot backend）

または GitHub Copilot for Business を使用している場合:
- `COPILOT_TOKEN`: GitHub Copilot トークン

### 4.2 ワークフロー設定

`.github/workflows/copilot-agent.yml`:

```yaml
name: Copilot Agent

on:
  issue_comment:
    types: [created]
  workflow_dispatch:
    inputs:
      task:
        description: 'Task description'
        required: true

jobs:
  copilot-agent:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install openai
          pip install -r requirements.txt

      - name: Run Copilot Agent
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/run_copilot_agent.py
```

`scripts/run_copilot_agent.py`:

```python
#!/usr/bin/env python3
"""Run Copilot agent from GitHub Actions."""

import os
import json
from pathlib import Path
from src.agent_abstraction import AgentFactory, AgentType

def main():
    # Load event data
    event_path = os.environ.get('GITHUB_EVENT_PATH')
    if event_path and Path(event_path).exists():
        with open(event_path) as f:
            event = json.load(f)

        # Extract task from comment
        task = event.get('comment', {}).get('body', '')
        if not task or '@copilot' not in task.lower():
            print("No @copilot mention found")
            return
    else:
        # Fallback to workflow dispatch input
        task = os.environ.get('INPUT_TASK', '')

    if not task:
        print("No task provided")
        return

    # Create agent
    agent = AgentFactory.create_agent(
        agent_type=AgentType.COPILOT,
        api_key=os.environ['OPENAI_API_KEY'],
        model="gpt-4-turbo"
    )

    # Process task
    response = agent.process_task(task)

    print("=" * 60)
    print("COPILOT AGENT RESPONSE")
    print("=" * 60)
    print(response.message)

if __name__ == "__main__":
    main()
```

---

## 5. SWE-agent

### 5.1 Secretsの設定

**必須:**
- `OPENAI_API_KEY`: OpenAI APIキー（推奨）

または:
- `ANTHROPIC_API_KEY`: Anthropic APIキー

### 5.2 Dockerベースワークフロー

`.github/workflows/swe-agent.yml`:

```yaml
name: SWE-agent

on:
  workflow_dispatch:
    inputs:
      issue_url:
        description: 'GitHub issue URL to fix'
        required: true
  issue_comment:
    types: [created]

jobs:
  swe-agent:
    if: |
      github.event_name == 'workflow_dispatch' ||
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@swe'))
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: Set up Docker
        uses: docker/setup-buildx-action@v3

      - name: Pull SWE-agent Docker image
        run: |
          docker pull sweagent/swe-agent:latest

      - name: Run SWE-agent
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Get issue URL
          if [ "${{ github.event_name }}" == "workflow_dispatch" ]; then
            ISSUE_URL="${{ inputs.issue_url }}"
          else
            ISSUE_URL="${{ github.event.issue.html_url }}"
          fi

          echo "Processing issue: $ISSUE_URL"

          # Run SWE-agent in Docker
          docker run \
            -e OPENAI_API_KEY=$OPENAI_API_KEY \
            -e GITHUB_TOKEN=$GITHUB_TOKEN \
            -v $(pwd):/workspace \
            sweagent/swe-agent:latest \
            python run.py \
              --model gpt-4-turbo \
              --data_path $ISSUE_URL \
              --repo_path /workspace \
              --config_file config/default.yaml \
              --output_dir /workspace/swe_agent_output

      - name: Commit changes
        if: success()
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

          if [ -n "$(git status --porcelain)" ]; then
            git add .
            git commit -m "SWE-agent: Auto-fix from issue"
            git push
          else
            echo "No changes to commit"
          fi

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: swe-agent-results
          path: swe_agent_output/
```

### 5.3 Python統合版

`.github/workflows/swe-agent-python.yml`:

```yaml
name: SWE-agent (Python)

on:
  workflow_dispatch:
    inputs:
      task:
        description: 'Task description'
        required: true

jobs:
  run-swe-agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install SWE-agent
        run: |
          git clone https://github.com/princeton-nlp/SWE-agent.git /tmp/swe-agent
          pip install -e /tmp/swe-agent

      - name: Install project dependencies
        run: pip install -r requirements.txt

      - name: Run SWE-agent
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python scripts/run_swe_agent.py "${{ inputs.task }}"
```

`scripts/run_swe_agent.py`:

```python
#!/usr/bin/env python3
"""Run SWE-agent from GitHub Actions."""

import os
import sys
from pathlib import Path
from src.agent_abstraction import AgentFactory, AgentType

def main():
    if len(sys.argv) < 2:
        print("Usage: run_swe_agent.py <task>")
        sys.exit(1)

    task = sys.argv[1]

    # Create agent
    agent = AgentFactory.create_agent(
        agent_type=AgentType.SWE_AGENT,
        api_key=os.environ['OPENAI_API_KEY'],
        model="gpt-4-turbo",
        swe_agent_path="/tmp/swe-agent"
    )

    # Process task
    response = agent.process_task(
        task=task,
        context={"repo_path": Path.cwd()}
    )

    print("=" * 60)
    print("SWE-AGENT RESPONSE")
    print("=" * 60)
    print(response.message)
    print("=" * 60)

    if response.changes:
        print("Changes made:")
        for change in response.changes:
            print(f"  - {change}")

if __name__ == "__main__":
    main()
```

---

## 6. 複数エージェントの併用

### 6.1 エージェント別トリガー

複数のエージェントを同時に使用する場合の設定:

`.agent-config.yml`:

```yaml
# Primary agent
agent:
  type: claude_code
  model: claude-sonnet-4-5-20250929

# Agent-specific triggers
triggers:
  claude: "@claude"
  gemini: "@gemini"
  copilot: "@copilot"
  swe: "@swe"

# Each agent's configuration
claude_code:
  tdd_mode: true

gemini:
  model: gemini-2.0-flash-exp

copilot:
  model: gpt-4-turbo

swe_agent:
  model: gpt-4-turbo
  swe_agent_path: "/tmp/swe-agent"
```

### 6.2 統合ワークフロー

`.github/workflows/multi-agent.yml`:

```yaml
name: Multi-Agent Support

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  detect-mention:
    runs-on: ubuntu-latest
    outputs:
      claude: ${{ steps.check.outputs.claude }}
      gemini: ${{ steps.check.outputs.gemini }}
      copilot: ${{ steps.check.outputs.copilot }}
      swe: ${{ steps.check.outputs.swe }}
    steps:
      - name: Check mentions
        id: check
        run: |
          BODY="${{ github.event.comment.body }}"
          echo "claude=$([[ $BODY =~ @claude ]] && echo 'true' || echo 'false')" >> $GITHUB_OUTPUT
          echo "gemini=$([[ $BODY =~ @gemini ]] && echo 'true' || echo 'false')" >> $GITHUB_OUTPUT
          echo "copilot=$([[ $BODY =~ @copilot ]] && echo 'true' || echo 'false')" >> $GITHUB_OUTPUT
          echo "swe=$([[ $BODY =~ @swe ]] && echo 'true' || echo 'false')" >> $GITHUB_OUTPUT

  claude-agent:
    needs: detect-mention
    if: needs.detect-mention.outputs.claude == 'true'
    uses: ./.github/workflows/claude-code.yml
    secrets: inherit

  gemini-agent:
    needs: detect-mention
    if: needs.detect-mention.outputs.gemini == 'true'
    uses: ./.github/workflows/gemini-agent.yml
    secrets: inherit

  copilot-agent:
    needs: detect-mention
    if: needs.detect-mention.outputs.copilot == 'true'
    uses: ./.github/workflows/copilot-agent.yml
    secrets: inherit

  swe-agent-job:
    needs: detect-mention
    if: needs.detect-mention.outputs.swe == 'true'
    uses: ./.github/workflows/swe-agent.yml
    secrets: inherit
```

### 6.3 使用例

Issue/PRコメントで複数のエージェントを呼び出し:

```markdown
このバグを修正してください

@swe まず自動的にバグを特定して修正を試みてください
@claude 修正後、コードレビューとテストの追加をお願いします
@gemini 最終的なドキュメントを作成してください
```

---

## トラブルシューティング

### よくある問題

**1. APIキーが認識されない**
- Secretsが正しく設定されているか確認
- ワークフローで正しく参照されているか確認
- Secrets名のタイポをチェック

**2. ワークフローがトリガーされない**
- ブランチ制限を確認
- トリガー条件（`if`）を確認
- GitHubアクションのログを確認

**3. エージェントがタイムアウトする**
- `timeout-minutes` を増やす
- タスクを小さく分割
- より高速なモデルを使用

**4. 権限エラー**
- ワークフローの `permissions` を確認
- リポジトリ設定でGitHub Actionsの権限を確認

### デバッグ方法

ワークフローにデバッグステップを追加:

```yaml
- name: Debug information
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Actor: ${{ github.actor }}"
    echo "Repository: ${{ github.repository }}"
    cat $GITHUB_EVENT_PATH
```

---

## まとめ

各エージェントのGitHub Actions統合:

| エージェント | 難易度 | 必要なもの | 推奨ケース |
|------------|-------|----------|-----------|
| Claude Code | ⭐ 簡単 | APIキーのみ | 即座に使用可能 |
| Gemini | ⭐⭐ 中 | Python script | カスタマイズ可能 |
| Copilot | ⭐⭐ 中 | OpenAI API | 既存OpenAI統合 |
| SWE-agent | ⭐⭐⭐ 難 | Docker/Python | 複雑なバグ修正 |

詳細は各エージェントの公式ドキュメントも参照してください。
