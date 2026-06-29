"""Validate banking CSV row count (Lab 8 pipeline processing step)."""
import argparse
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="/opt/ml/processing/input")
    args = parser.parse_args()
    input_dir = Path(args.input)
    files = list(input_dir.glob("*.csv"))
    if not files:
        raise SystemExit(f"No CSV files in {input_dir}")
    df = pd.read_csv(files[0])
    if len(df) < 10:
        raise SystemExit(f"Validation failed: only {len(df)} rows")
    print(f"VALIDATION_OK rows={len(df)} file={files[0].name}")


if __name__ == "__main__":
    main()
