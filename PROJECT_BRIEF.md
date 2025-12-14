# PROJECT_BRIEF — BTC–QQQ Pairs / Spread Analysis

## Goal
Reinforce quantitative time-series knowledge by conducting an analytical study of the relationship between **BTC-USD** and **QQQ** in both **prices** and **returns**, using a pairs/spread modeling framework.

## Approach

### 1) Data handling and alignment
- Load close prices from a yfinance-style CSV.
- Align series using `align="inner"` to keep only timestamps where both assets have observed prices.

### 2) Modeling framework (log-price space)
Define:
- \(Y_t\): BTC-USD close price
- \(X_t\): QQQ close price
- \(y_t=log(Y_t)\), \(x_t=log(X_t)\)

Model:
\[
y_t = alpha_t + beta_t x_t + varepsilon_t
\]

Interpretation:
- \(beta_t\): hedge ratio (elasticity in log space)
- \(varepsilon_t\): spread (residual), expected to be more stationary than prices

### 3) Time-varying hedge ratio (Kalman filter)
Estimate \(alpha_t\) and \(beta_t\) using a simple Kalman filter state-space model. This allows the relationship to adapt over time rather than assuming a constant hedge ratio across all regimes.

### 4) Spread normalization and signals
Compute an adaptive z-score:
\[
z_t = frac{varepsilon_t - mu_t}{sigma_t}
\]
where \(mu_t\) and \(sigma_t\) are exponentially weighted estimates controlled by `ZSPAN`.

Define signal events:
- Entry when \(|z| > 2\)
- Exit when \(|z| > 0.5\)

Summarize signal behavior via:
- events per 1000 bars
- percent of time in extreme regimes (\(|z| > 2\))
- duration distribution (mean/median/p90)
- LONG vs SHORT counts

### 5) Diagnostics

![spread and beta](Output/Spread_and_beta.png)
![z_score](Output/z_score.png)

Validate spread behavior with:
- **ADF** (unit root test) and **KPSS** (stationarity test)
- **Half-life** estimate for mean reversion speed
- **Autocorrelation** at multiple lags to characterize dynamics

## Key findings (from the notebook run)
- The spread residual is strongly consistent with stationarity (ADF rejects unit root; KPSS does not reject stationarity).
- Mean reversion is fast (half-life on the order of ~1–2 daily bars).
- Extreme z-score events occur at a moderate frequency and typically resolve within a few bars (parameter-dependent).

- These conclusions suggest that the model could be profitable in practice, as it fulfils the main requirements for a mean reversion strategy based on the spread. 

## What this project demonstrates

- Time-series analysis and preprocessing  
- Relative-value modeling between two assets  
- Dynamic parameter estimation (regime awareness)  
- Signal standardization and event-based analysis  
- Statistical validation of assumptions  
- Robustness/sensitivity checks  
- Reproducible, well-documented research workflow  

### Notes and limitations

This repository focuses on analysis and diagnostics. A production-grade trading system would additionally require:

- transaction costs and slippage modeling

- position sizing and risk constraints (e.g., beta- or volatility-neutral sizing)

- walk-forward validation and regime filters

- execution assumptions consistent with the target venue and frequency