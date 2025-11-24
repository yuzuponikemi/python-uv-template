#!/usr/bin/env python
"""データ処理スクリプトの例.

このスクリプトは、CSVファイルを読み込んでデータを処理するサンプルです。
研究用途でのデータ処理パイプラインの参考として使用できます。

Usage:
    python scripts/process_data.py input.csv output.csv
    python scripts/process_data.py --help
"""

import argparse
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def setup_logging(log_level: str = "INFO") -> None:
    """ロギングを設定する.

    Args:
        log_level: ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def load_data(input_path: Path) -> pd.DataFrame:
    """CSVファイルからデータを読み込む.

    Args:
        input_path: 入力ファイルのパス

    Returns:
        読み込んだデータフレーム

    Raises:
        FileNotFoundError: ファイルが存在しない場合
        pd.errors.EmptyDataError: ファイルが空の場合
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Loading data from {input_path}")

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    return df


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """データを処理する.

    Args:
        df: 入力データフレーム

    Returns:
        処理後のデータフレーム
    """
    logger = logging.getLogger(__name__)
    logger.info("Processing data")

    # 欠損値の処理
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        logger.warning(f"Found {missing_count} missing values, filling with mean")
        df = df.fillna(df.mean(numeric_only=True))

    # 数値列の正規化（例）
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        logger.info(f"Normalizing {len(numeric_cols)} numeric columns")
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                df[f"{col}_normalized"] = (df[col] - mean) / std

    logger.info("Processing complete")
    return df


def save_data(df: pd.DataFrame, output_path: Path) -> None:
    """処理後のデータを保存する.

    Args:
        df: 保存するデータフレーム
        output_path: 出力ファイルのパス
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Saving data to {output_path}")

    # 出力ディレクトリを作成
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)
    logger.info(f"Saved {len(df)} rows to {output_path}")


def main(
    input_path: Path,
    output_path: Path,
    log_level: str = "INFO",
) -> None:
    """メイン処理.

    Args:
        input_path: 入力ファイルのパス
        output_path: 出力ファイルのパス
        log_level: ログレベル
    """
    setup_logging(log_level)
    logger = logging.getLogger(__name__)

    try:
        # データ読み込み
        df = load_data(input_path)

        # データ処理
        df_processed = process_data(df)

        # データ保存
        save_data(df_processed, output_path)

        logger.info("All operations completed successfully")

    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパースする.

    Returns:
        パース済みの引数
    """
    parser = argparse.ArgumentParser(
        description="Process CSV data with normalization and missing value handling",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input CSV file path",
    )

    parser.add_argument(
        "output",
        type=Path,
        help="Output CSV file path",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(
        input_path=args.input,
        output_path=args.output,
        log_level=args.log_level,
    )
