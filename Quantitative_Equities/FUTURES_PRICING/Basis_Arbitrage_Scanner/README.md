***

# Basis Arbitrage Engine

## Overview
The Basis Arbitrage Engine is a Python-based quantitative scanner designed to detect real-time mathematical mispricings between the equity spot market and the futures term structure. By applying continuous compounding to the Cost-of-Carry model, it acts as a radar for structural inefficiencies, identifying when the "Law of One Price" temporarily breaks.

## Features
* **Live Data Ingestion:** Pings live market data via the `yfinance` API to track the immediate spread between the Spot ETF and the Front-Month Futures contract.
* **Fair-Value Math Engine:** Utilizes `numpy` to calculate the exact theoretical price of a derivative based on risk-free interest rates and continuous dividend yields.
* **Algorithmic Signal Routing:** Automatically subtracts theoretical fair value from the live market price to generate explicit, directional "Cash & Carry" or "Reverse Cash & Carry" execution signals based on predefined transaction-cost thresholds.

## The Engineering Thesis
Retail trading attempts to predict the future direction of an asset. Quantitative institutional trading ignores direction entirely, focusing instead on structural mispricings. 

The theoretical price of a futures contract is strictly governed by the Cost-of-Carry equation:

$$F_0 = S_0 e^{(r-q)T}$$

If the live market price deviates from this mathematical reality, the market is inefficient. This terminal allows the user to mathematically prove when a futures contract is overpriced or underpriced, signaling a risk-free arbitrage opportunity before high-frequency algorithms close the gap.

## Requirements
`pip install yfinance numpy`

## Usage
Run the script to execute a live scan. The engine defaults to scanning the spread between the SPY ETF (Spot) and the E-Mini S&P 500 Futures (`ES=F`), adjusting for the 10x multiplier scale.

```bash
python Basis_Arbitrage_Scanner.py
```