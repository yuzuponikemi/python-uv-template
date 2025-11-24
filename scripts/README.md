# スクリプト

このフォルダには、データ処理やユーティリティ用のスクリプトが含まれています。

## 利用可能なスクリプト

### process_data.py

CSVファイルを読み込んでデータを処理するサンプルスクリプト。

**機能:**
- CSVファイルの読み込み
- 欠損値の処理（平均値で埋める）
- 数値列の正規化（標準化）
- 処理結果の保存

**使用方法:**

```bash
# 基本的な使用方法
python scripts/process_data.py input.csv output.csv

# デバッグログを表示
python scripts/process_data.py input.csv output.csv --log-level DEBUG

# ヘルプを表示
python scripts/process_data.py --help
```

**例:**

```bash
# サンプルデータを作成
echo "name,value,category
item1,10.5,A
item2,,B
item3,15.7,A" > sample.csv

# データ処理を実行
python scripts/process_data.py sample.csv processed.csv

# 結果を確認
cat processed.csv
```

## 新しいスクリプトを追加する場合

1. **Shebangを追加**: `#!/usr/bin/env python`
2. **Docstringを記載**: スクリプトの目的と使用方法を明確に
3. **型ヒントを使用**: すべての関数に型アノテーションを追加
4. **ロギングを実装**: `logging` モジュールを使用
5. **エラーハンドリング**: 適切な例外処理を実装
6. **引数パーサー**: `argparse` を使用してCLI引数を処理
7. **テストを追加**: `tests/test_scripts.py` にテストを追加
8. **このREADMEを更新**: 使用方法を記載

## ベストプラクティス

### 再現性の確保

```python
import random
import numpy as np

# ランダムシードを固定
random.seed(42)
np.random.seed(42)
```

### 進捗表示

長時間実行されるスクリプトには進捗表示を追加：

```python
from tqdm import tqdm

for item in tqdm(items, desc="Processing"):
    process(item)
```

### 設定ファイルの使用

複雑な設定は外部ファイルに：

```python
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)
```

### ドライラン機能

```python
parser.add_argument("--dry-run", action="store_true",
                   help="Dry run without saving")
```

## 実行権限

スクリプトに実行権限を付与する場合：

```bash
chmod +x scripts/process_data.py
./scripts/process_data.py input.csv output.csv
```
