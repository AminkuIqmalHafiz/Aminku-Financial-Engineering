# Quantitative Tail Risk Terminal (Kurtosis Scanner)

## Overview
The Tail Risk Terminal is a Python-based command-line interface (CLI) designed to measure the non-normality of asset returns. By calculating the Excess Kurtosis of an asset over a rolling 1-year window, this engine detects "Fat Tails" (Leptokurtic distributions) to identify when standard mathematical pricing models are underestimating extreme market moves.

## The Quantitative Edge
Standard derivatives pricing (like Black-Scholes) assumes market returns follow a normal distribution. In reality, financial markets experience extreme, violent outliers far more often than a normal bell curve predicts. 

This engine measures that exact discrepancy:
* **High Kurtosis (> 2.0):** The asset has a high probability of extreme outlier moves. Options premiums may be mathematically underpricing this "fat tail" risk.
* **Low Kurtosis (< 0.5):** The asset trades in a highly controlled, predictable range.

## Features
* **Live Statistical Polling:** Automatically pulls 1 year of daily closing data via the `yfinance` API to ensure a statistically significant sample size.
* **Instant Volatility & Kurtosis Metrics:** Calculates both annualized volatility and Fisher's Excess Kurtosis dynamically.

## Requirements
Ensure you have the required quantitative data libraries installed:
```bash
pip install yfinance pandas numpy