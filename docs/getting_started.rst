はじめに
========

インストール
------------

uvのインストール::

    curl -LsSf https://astral.sh/uv/install.sh | sh

依存関係のインストール::

    uv pip install -r requirements.txt

開発環境のセットアップ::

    make install

基本的な使い方
--------------

テストの実行::

    make test

リンターの実行::

    make lint

コードフォーマット::

    make format

型チェック::

    make type-check

全てのCIチェックをローカルで実行::

    make ci

自律的コード修正機能
--------------------

このテンプレートには、CIテストが失敗した際に自動的にClaudeが修正を試みる機能が組み込まれています。

ワークフロー
^^^^^^^^^^^^

1. ``claude/**`` ブランチにコードをpush
2. CIが自動実行（pytest、ruff、mypy）
3. テストが失敗すると、自動修正ワークフローが起動
4. エラーログを解析してIssueを自動作成
5. Claudeが修正を実装してコミット
6. CIが再実行され、修正が検証される

使用例::

    # 新しい機能ブランチを作成
    git checkout -b claude/add-new-feature

    # コードを編集
    # ...

    # Push（CIが自動実行）
    git push -u origin claude/add-new-feature

対応するエラー
^^^^^^^^^^^^^^

* **Pytest**: テスト失敗、アサーションエラー
* **Ruff**: コードスタイル違反、リントエラー
* **Mypy**: 型ヒントエラー、型の不一致
