# ベンチマーク

このフォルダには、パフォーマンステストとベンチマークが含まれています。

## 概要

ベンチマークは、コードのパフォーマンスを測定し、リグレッションを検出するために使用されます。
研究用ソフトウェアでは、特に以下の場合に重要です：

- 大規模データセットの処理
- 計算集約的なアルゴリズム
- パフォーマンス最適化後の検証
- 異なる実装の比較

## 使用方法

### 基本的な実行

```bash
# すべてのベンチマークを実行
pytest benchmarks/ -v --benchmark-only

# 特定のベンチマークを実行
pytest benchmarks/benchmark_calculator.py -v --benchmark-only

# 通常のテストとベンチマークを両方実行
pytest benchmarks/ -v
```

### 詳細なレポート

```bash
# 詳細な統計を表示
pytest benchmarks/ --benchmark-verbose

# JSON形式で結果を保存
pytest benchmarks/ --benchmark-json=benchmark_results.json

# 比較用のベースラインを保存
pytest benchmarks/ --benchmark-save=baseline
```

### 結果の比較

```bash
# 以前の結果と比較
pytest benchmarks/ --benchmark-compare

# 特定のベースラインと比較
pytest benchmarks/ --benchmark-compare=baseline
```

## ベンチマークの書き方

### 基本的な構造

```python
import pytest

@pytest.mark.benchmark
def test_benchmark_function(benchmark):
    """Benchmark description."""
    # ベンチマーク対象の関数を実行
    result = benchmark(function_to_test, arg1, arg2)

    # 結果の検証（オプション）
    assert result == expected_value
```

### グループ化

関連するベンチマークをグループ化して比較：

```python
@pytest.mark.benchmark(group="addition")
def test_benchmark_custom_add(benchmark):
    result = benchmark(custom_add, 1, 2)
    assert result == 3

@pytest.mark.benchmark(group="addition")
def test_benchmark_numpy_add(benchmark):
    result = benchmark(np.add, 1, 2)
    assert result == 3
```

### セットアップ/ティアダウン

セットアップコストを除外するには：

```python
def test_benchmark_with_setup(benchmark):
    # セットアップ（測定から除外）
    data = prepare_large_dataset()

    # ベンチマーク実行
    result = benchmark(process_data, data)

    assert len(result) > 0
```

## ベストプラクティス

### 1. 再現性の確保

```python
import random
import numpy as np

@pytest.fixture(scope="session", autouse=True)
def set_random_seed():
    random.seed(42)
    np.random.seed(42)
```

### 2. 適切なデータサイズ

- 小さすぎる：測定誤差が大きい
- 大きすぎる：実行時間が長くなる
- 実際の使用例に近いサイズを選択

```python
# Good: 実際の使用例に近い
data = np.random.rand(10000)

# Bad: 小さすぎる
data = np.random.rand(10)
```

### 3. ウォームアップ

JITコンパイラなどのウォームアップを考慮：

```python
@pytest.mark.benchmark(warmup=True, warmup_iterations=10)
def test_benchmark_jit_function(benchmark):
    result = benchmark(jit_compiled_function, data)
```

### 4. 統計的有意性

複数回実行して統計を取る：

```python
pytest benchmarks/ --benchmark-min-rounds=100
```

## 結果の解釈

### 出力例

```
Name (time in us)              Min        Max       Mean    StdDev    Median
---------------------------------------------------------------------------
test_benchmark_add           1.234      2.345     1.567     0.234     1.456
test_benchmark_multiply      2.345      3.456     2.789     0.345     2.678
```

### 主要な指標

- **Min**: 最小実行時間（理想的なケース）
- **Max**: 最大実行時間（最悪ケース）
- **Mean**: 平均実行時間（典型的なケース）
- **StdDev**: 標準偏差（安定性の指標）
- **Median**: 中央値（外れ値の影響を受けにくい）

### パフォーマンスリグレッションの検出

```bash
# ベースラインを保存
pytest benchmarks/ --benchmark-save=before_optimization

# 最適化を実施

# 比較
pytest benchmarks/ --benchmark-compare=before_optimization
```

改善率が10%以上であれば有意な改善とみなせます。

## CI/CDでの使用

GitHub Actionsで自動的にベンチマークを実行：

```yaml
- name: Run benchmarks
  run: |
    pytest benchmarks/ --benchmark-json=output.json

- name: Store benchmark result
  uses: benchmark-action/github-action-benchmark@v1
  with:
    tool: 'pytest'
    output-file-path: output.json
```

## 追加の依存関係

ベンチマークには以下のパッケージが必要です：

```bash
pip install pytest-benchmark
```

詳細な可視化には：

```bash
pip install pytest-benchmark[histogram]
```
