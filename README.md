# BTC–QQQ Pairs / Spread Analysis (Kalman Hedge Ratio + Adaptive Z-Score)

A compact research project to reinforce quantitative time-series knowledge by analyzing the relationship between **BTC-USD** and **QQQ** across **prices** and **returns** using a pairs/spread modeling approach.

## What to look at

- Full write-up: `PROJECT_BRIEF.md`
- Reproducible notebook: `notebook/analysis_pairs.ipynb`
- Core utilities: `src/core.py`

## Figures 

![spread and beta](Output/Spread_and_beta.png)
![z_score](Output/z_score.png)

## Quick run

Create a virtual environment and install the project in editable mode:

### 1) Install
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -U pip
pip install -e ".[research]"
```

## Repository structure

Cross_assets_pair_analyzer

```text
.
├── pyproject.toml
├── README.md
├── PROJECT_BRIEF.md
├── src/
│   ├── __init__.py
│   └── core.py
├── notebook/
│   └── analysis_pairs.ipynb
├── scripts/
│   └── download_data.py
└── Output/
    ├── beta_spread.png
    └── zscore.png
```


## Usage (in a notebook)

```python
import src.core as core

closes = core.load_and_prepare_closes("data/raw/prices.csv", align="inner")
log_prices = core.compute_log_prices(closes)

k = core.kalman_hedge_ratio(log_prices, "BTC-USD", "QQQ")
z = core.zscore_ewm(k["spread"], span=60)
```

## Reproducible demo

If you want the notebook to run out-of-the-box, you can download a small dataset locally:

```bash
pip install -e ".[research]"
python scripts/download_data.py --tickers BTC-USD QQQ --start 2024-01-01 --end 2025-01-01
```

This will write `data/raw/prices.csv` (excluded from git by default).



