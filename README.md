# Pairs / Spread Analysis

This repository showcases a compact, research-oriented pairs/spread analysis workflow.

## What it includes

- Close-price loading from a yfinance-style CSV (MultiIndex header).
- Explicit calendar alignment (important when mixing 24/7 assets with session-based markets).
- Spread construction as an OLS residual in log-price space.
- Time-varying hedge ratio estimation via a lightweight Kalman filter.
- Adaptive z-score using exponentially weighted mean/std.
- Diagnostics helpers (half-life estimate, ADF/KPSS tests if `statsmodels` is installed).

## Installation

Create a virtual environment and install the project in editable mode:

```bash
python -m venv .venv
# Windows:
#   .venv\Scripts\activate
# macOS/Linux:
#   source .venv/bin/activate

pip install -U pip
pip install -e ".[research]"
```

## Usage (in a notebook)

```python
import src.core as core

closes = core.load_and_prepare_closes("data/raw/prices.csv", align="inner")
log_prices = core.compute_log_prices(closes)

k = core.kalman_hedge_ratio(log_prices, "BTC-USD", "QQQ")
z = core.zscore_ewm(k["spread"], span=60)
```

## Notes on calendar alignment

When combining assets with different trading calendars (e.g., BTC vs an ETF), forward-filling
session-market prices across weekends can introduce artificial zero-returns and bias the hedge ratio.
For pairs/spread work, `align="inner"` (common timestamps only) is typically the safest default.

## Reproducible demo

If you want the notebook to run out-of-the-box, you can download a small dataset locally:

```bash
pip install -e ".[research]"
python scripts/download_data.py --tickers BTC-USD QQQ --start 2024-01-01 --end 2025-01-01
```

This will write `data/raw/prices.csv` (excluded from git by default).
