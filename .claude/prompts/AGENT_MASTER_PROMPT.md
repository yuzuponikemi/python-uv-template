# AI Coding Agent Master Prompt

このプロンプトは、Claude、GitHub Copilot、その他のコーディングエージェントがこのプロジェクトで作業する際の統一的なガイドラインです。

## プロジェクト概要

- **プロジェクト名**: python-uv-template
- **目的**: Python研究用ソフトウェア開発のテンプレート
- **開発方針**: テスト駆動開発（TDD）、再現性、科学的正確性

## 核となる原則

### 1. テスト駆動開発（TDD）

- **常にテストを先に書く**: 新機能の実装前に、必ず失敗するテストを作成
- **Red-Green-Refactorサイクル**:
  1. Red: 失敗するテストを書く
  2. Green: テストを通すための最小限のコードを書く
  3. Refactor: コードを改善（テストは常にグリーン）
- **高いカバレッジを維持**: 80%以上のテストカバレッジを目指す
- **エッジケースをテスト**: ゼロ、無限大、NaN、空配列などのエッジケースを必ずテスト

### 2. コード品質

- **型ヒントの使用**: すべての関数シグネチャに型ヒントを追加
- **PEP 8準拠**: ruffによるリンターチェックを満たす
- **包括的なdocstring**: NumPyまたはGoogle styleでdocstringを記述
- **関数の単一責任**: 各関数は1つの明確な責任を持つ
- **説明的な変数名**: 意味が明確で理解しやすい変数名を使用

### 3. 再現性（研究ソフトウェアにおいて重要）

- **依存関係の固定**: 依存関係は正確なバージョンでピン留め
- **環境のドキュメント化**: セットアップ手順を明確に文書化
- **uvによる管理**: 依存関係管理にはuvを使用
- **ランダムシードの設定**: 確率的プロセスには必ずシードを設定
- **データ処理手順の文書化**: 前処理ステップを詳細に文書化

### 4. 科学的正確性

- **数値精度と安定性**: 浮動小数点演算の精度問題を考慮
- **エッジケーステスト**: ゼロ除算、オーバーフロー、アンダーフローなどをテスト
- **アルゴリズムの文書化**: 学術論文やアルゴリズムの参照を含める
- **ベンチマーク検証**: 既知のベンチマークや解析解と比較検証
- **計算複雑性の文書化**: パフォーマンス特性を明記

### 5. ドキュメント

- **使用例を含むREADME**: 明確な使用例をREADMEに記載
- **計算複雑性の記述**: 関連する箇所では計算量を記載
- **論文・アルゴリズムの参照**: 実装したアルゴリズムの出典を明記
- **複雑なワークフローのnotebook**: Jupyter notebookで実例を提供

## ローカル開発フロー

### 変更を加える前に

1. **現在のブランチを確認**:
   ```bash
   git branch
   ```

2. **必要に応じてブランチを作成**:
   ```bash
   git checkout -b claude/feature-name
   ```

### コード変更時の標準フロー

1. **テストを先に書く（TDD）**:
   ```bash
   # tests/ディレクトリに新しいテストを作成
   nano tests/test_new_feature.py
   ```

2. **テストが失敗することを確認**:
   ```bash
   pytest tests/test_new_feature.py -v
   ```

3. **最小限のコードで実装**:
   ```bash
   nano src/your_module.py
   ```

4. **ローカルでCIを実行**（重要！）:
   ```bash
   make ci-local
   ```

   または直接actを使用:
   ```bash
   act push -j test
   ```

5. **すべてのチェックが通ることを確認**:
   - pre-commit hooks
   - ruff linter
   - ruff formatter
   - mypy type checker
   - bandit security check
   - pytest with coverage

6. **失敗があれば修正し、再度ローカルCIを実行**

7. **すべてのチェックが通ったらコミット**:
   ```bash
   git add .
   git commit -m "Add new feature with tests"
   ```

8. **プッシュ前に最終チェック**（オプション）:
   ```bash
   make ci-local
   ```

9. **リモートにプッシュ**:
   ```bash
   git push -u origin claude/feature-name
   ```

### Pull Request作成フロー（厳格版）

**重要**: Pull Requestを作成する際は、必ず以下の品質チェックを経てから作成してください。

#### gh pr-strict エイリアスの使用

このリポジトリでは、`gh pr-strict` カスタムエイリアスを推奨します。これは以下のチェックを自動で実行します：

1. `ruff format .` - コード整形
2. `ruff check --fix .` - Lint修正
3. `mypy .` - 型チェック
4. `act push -q` - ローカルでのGitHub Actions実行
5. すべて成功した場合のみ `gh pr create` を実行

#### PR作成時のルール

- **通常の `gh pr create` は使用しない**: 単純に `gh pr create` を実行するのではなく、必ず品質チェックを経ること
- **AIエージェントへの指示**: ユーザーから「PRを作って」と依頼された際は：
  1. まず `ruff`, `mypy`, `act` が通る状態かを確認
  2. 必要に応じてコードを修正
  3. 最終的に `gh pr-strict` コマンドの使用を推奨または実行
- **コード修正の前提**: すべてのコード修正は、これらのLinterやCIが通ることを前提とする

#### 手動でのPR作成フロー（gh pr-strictが使えない場合）

```bash
# 1. コード整形
ruff format .

# 2. Lint修正
ruff check --fix .

# 3. 型チェック
mypy .

# 4. ローカルCI実行
act push -q

# 5. すべて成功したらPR作成
gh pr create --title "タイトル" --body "説明"
```

エイリアスの設定方法は `docs/GH_PR_STRICT_SETUP.md` を参照してください。

### よく使うコマンド

```bash
# 依存関係のインストール
make install

# テストの実行
make test

# リンターの実行
make lint

# フォーマッターの実行
make format

# 型チェック
make typecheck

# セキュリティチェック
make security

# 全てのCIチェック（ローカル）
make ci-local

# 依存関係の更新
make compile

# カバレッジレポートの表示
make coverage
```

## act（ローカルCI）の使い方

### 基本的な使い方

```bash
# CIワークフロー全体を実行
act push -j test

# 詳細ログ付きで実行
act -v

# ドライラン（実行せずに確認）
act -n

# 特定のワークフローのみ実行
act -W .github/workflows/ci.yml
```

### トラブルシューティング

失敗した場合:

1. **詳細ログを確認**:
   ```bash
   act -v 2>&1 | tee act-debug.log
   ```

2. **Dockerが起動しているか確認**:
   ```bash
   docker ps
   ```

3. **シークレットが設定されているか確認**:
   ```bash
   cat .secrets
   ```

詳細は `LOCAL_TESTING.md` を参照してください。

## コミットメッセージのガイドライン

### フォーマット

```
<type>: <subject>

<body>

<footer>
```

### Type

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの動作に影響しない変更（フォーマット等）
- `refactor`: リファクタリング
- `perf`: パフォーマンス改善
- `test`: テストの追加・修正
- `chore`: ビルドプロセスやツールの変更

### 例

```
feat: Add numerical integration module with trapezoid rule

- Implement trapezoid rule for 1D integration
- Add comprehensive tests including edge cases
- Include performance benchmarks
- Document algorithm complexity (O(n))

Closes #123
```

## エラーハンドリングのベストプラクティス

### やるべきこと

- **システム境界で検証**: ユーザー入力や外部APIからのデータを検証
- **意味のあるエラーメッセージ**: 何が問題か、どう修正できるかを明示
- **カスタム例外の使用**: ドメイン固有の例外を定義

### やるべきでないこと

- **過度なエラーハンドリング**: 起こりえないケースのための防御的プログラミング
- **内部コードへの不信**: フレームワークや標準ライブラリの保証を信頼
- **try-exceptの乱用**: 予期される例外のみをキャッチ

## 依存関係の管理

### 新しい依存関係を追加

1. **requirements.inを編集**:
   ```bash
   echo "scikit-learn>=1.3.0" >> requirements.in
   ```

2. **requirements.txtを更新**:
   ```bash
   make compile
   ```

3. **インストール**:
   ```bash
   make install
   ```

4. **両方のファイルをコミット**:
   ```bash
   git add requirements.in requirements.txt
   git commit -m "chore: Add scikit-learn dependency"
   ```

### 開発用依存関係

開発用の依存関係（テストツールなど）は `requirements-dev.txt` に追加します。

## セキュリティ

- **Banditチェック**: `make security` でセキュリティ脆弱性をスキャン
- **シークレット管理**: `.secrets` ファイルに機密情報を保存（Gitにコミットしない）
- **入力検証**: ユーザー入力は常に検証
- **OWASP Top 10**: コマンドインジェクション、XSS、SQLインジェクション等に注意

## パフォーマンス

### ベンチマーク

パフォーマンスクリティカルなコードには必ずベンチマークを追加:

```python
# benchmarks/test_performance.py
import pytest

def test_my_function_performance(benchmark):
    result = benchmark(my_function, arg1, arg2)
    assert result is not None
```

実行方法:
```bash
pytest benchmarks/ --benchmark-only
```

## コードレビューチェックリスト

変更を提出する前に以下を確認:

- [ ] テストが先に書かれている（TDD）
- [ ] すべてのテストが通る（`make test`）
- [ ] 型ヒントが追加されている
- [ ] Docstringが記述されている
- [ ] リンターチェックが通る（`make lint`）
- [ ] フォーマッターチェックが通る（`make format`）
- [ ] 型チェックが通る（`make typecheck`）
- [ ] セキュリティチェックが通る（`make security`）
- [ ] ローカルCIが通る（`make ci-local`）
- [ ] カバレッジが維持されている（80%以上）
- [ ] ドキュメントが更新されている
- [ ] コミットメッセージが明確

## AI Agent固有のガイドライン

### Claude使用時

- GitHub ActionsでClaudeを使用する場合、`@claude`とメンションしてください
- Issueやプルリクエストのコメントでメンション可能
- 自動修正機能は`claude/**`ブランチでのみ有効

### GitHub Copilot使用時

- インラインコメントでコンテキストを提供
- 関数のdocstringを書いてから実装を書かせる
- テストを先に書いてから実装を生成

### 共通の注意点

- **過剰な抽象化を避ける**: 必要最小限のコードを書く
- **後方互換性のハックを避ける**: 不要なコードは削除
- **未使用コードを削除**: `_unused_var`のような回避策を使わない
- **コメントは最小限に**: コードが自己説明的であることを優先

## トラブルシューティング

### よくある問題

1. **テストが失敗する**:
   - ローカルで `make test` を実行して詳細を確認
   - `pytest -v --tb=long` で詳細なトレースバックを表示

2. **リンターエラー**:
   - `make format` で自動修正
   - `ruff check . --fix` で修正可能なエラーを自動修正

3. **型チェックエラー**:
   - `mypy --ignore-missing-imports` で詳細を確認
   - 型ヒントを追加または修正

4. **ローカルCIが失敗する**:
   - `LOCAL_TESTING.md` のトラブルシューティングセクションを参照
   - Docker が起動しているか確認
   - `.secrets` ファイルが設定されているか確認

## 参考資料

- [プロジェクトREADME](README.md) - プロジェクトの全体像
- [ローカルテストガイド](LOCAL_TESTING.md) - actを使ったローカルCI
- [アーキテクチャ](ARCHITECTURE.md) - プロジェクト構造の詳細
- [貢献ガイド](CONTRIBUTING.md) - コントリビューションの方法

## まとめ

このプロジェクトで作業する際は:

1. **TDDを実践**: テストを先に書く
2. **ローカルCIを実行**: コミット前に `make ci-local`
3. **高品質を維持**: 型ヒント、docstring、テストカバレッジ
4. **再現性を重視**: 依存関係を固定、環境を文書化
5. **科学的正確性**: 数値精度、ベンチマーク、エッジケース

質問がある場合は、既存のドキュメントを参照するか、Issueを作成してください。
