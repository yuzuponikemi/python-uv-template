コントリビューション
====================

このプロジェクトへの貢献を歓迎します！

開発プロセス
------------

1. リポジトリをフォーク
2. 新しいブランチを作成 (``git checkout -b feature/amazing-feature``)
3. テストを書く（TDD）
4. 変更をコミット (``git commit -m 'Add amazing feature'``)
5. ブランチをプッシュ (``git push origin feature/amazing-feature``)
6. Pull Requestを作成

コーディング規約
----------------

* PEP 8に準拠
* すべての関数に型ヒントを追加
* NumPy/Google スタイルのdocstringを使用
* テストカバレッジ80%以上を維持

テスト駆動開発
--------------

新しい機能を追加する際は、必ずテストを先に書いてください::

    # 1. テストを書く
    def test_new_feature():
        result = new_feature(input_data)
        assert result == expected_output

    # 2. テストが失敗することを確認
    pytest tests/test_module.py::test_new_feature

    # 3. 最小限の実装でテストを通す
    def new_feature(data):
        # 実装
        return result

    # 4. リファクタリング
    # コードを改善しながらテストが通ることを確認

コミットメッセージ
------------------

明確で説明的なコミットメッセージを書いてください::

    # Good
    Add validation for division by zero

    # Bad
    fix bug

詳細は `CONTRIBUTING.md` を参照してください。
