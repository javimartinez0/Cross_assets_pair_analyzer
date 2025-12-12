"""scripts/download_data.py

Small convenience script to fetch a minimal dataset for the notebook.

By default it:
- downloads daily data for a short recent window,
- saves to data/raw/prices.csv (excluded from git by default).

Usage
-----
python scripts/download_data.py --tickers BTC-USD QQQ --start 2024-01-01 --end 2025-01-01
"""

from __future__ import annotations

import argparse
from pathlib import Path

import src.core as core


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Download OHLCV data and save a yfinance-style CSV.")
    p.add_argument("--tickers", nargs="+", default=["BTC-USD", "QQQ"], help="Tickers to download.")
    p.add_argument("--start", default="2024-01-01", help="Start date (YYYY-MM-DD).")
    p.add_argument("--end", default="2025-01-01", help="End date (YYYY-MM-DD).")
    p.add_argument("--interval", default="1d", help="Data interval (e.g., 1d, 1h).")

    p.add_argument(
        "--out",
        default="data/raw/prices.csv",
        help="Output CSV path (default: data/raw/prices.csv).",
    )
    p.add_argument(
        "--no-auto-adjust",
        action="store_true",
        help="Disable yfinance auto_adjust.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    df = core.download_data(
        tickers=args.tickers,
        start=args.start,
        end=args.end,
        interval=args.interval,
        save_path=str(out),
        auto_adjust=not args.no_auto_adjust,
    )

    print(f"Saved: {out}")
    print(f"Rows: {len(df)} | Columns: {df.shape[1]}")
    print("Tip: the notebook expects data/raw/prices.csv by default.")


if __name__ == "__main__":
    main()
