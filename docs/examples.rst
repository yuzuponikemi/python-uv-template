使用例
======

基本的な計算
------------

計算機モジュールの基本的な使い方::

    from src.calculator import add, subtract, multiply, divide, power

    # 加算
    result = add(10, 5)
    print(f"10 + 5 = {result}")  # 15

    # 減算
    result = subtract(10, 5)
    print(f"10 - 5 = {result}")  # 5

    # 乗算
    result = multiply(10, 5)
    print(f"10 × 5 = {result}")  # 50

    # 除算
    result = divide(10, 5)
    print(f"10 ÷ 5 = {result}")  # 2.0

    # べき乗
    result = power(2, 8)
    print(f"2^8 = {result}")  # 256

エラーハンドリング
------------------

ゼロ除算のエラーハンドリング::

    from src.calculator import divide

    try:
        result = divide(10, 0)
    except ValueError as e:
        print(f"エラー: {e}")  # エラー: Cannot divide by zero

Jupyter Notebook での使用
--------------------------

詳しい使用例は ``examples/`` フォルダのJupyter notebookを参照してください。
