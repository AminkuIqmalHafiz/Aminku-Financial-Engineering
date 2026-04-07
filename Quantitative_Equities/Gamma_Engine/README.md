# Quantitative Gamma Engine (GEX Regime Detection)

## Overview
The Gamma Engine is a Python-based quantitative terminal tool designed to locate the Zero-Gamma (Gamma Flip) level for any optionable equity, index, or ETF. By aggregating open interest and implied volatility across the options chain, this script reverse-engineers the hedging obligations of institutional market makers (dealers) to determine the structural volatility regime of the underlying asset.

This tool bridges the gap between derivatives positioning and underlying price action, providing a mathematical edge for anticipating market stability or violent momentum expansions.This only work efficiently when market size of the option > its underlying stock.

## The Quantitative Edge
In modern markets, dealer hedging flows can decide intraday and interday volatility. Market makers must continuously buy or sell the underlying asset to remain delta-neutral. This engine calculates the net Gamma Exposure (GEX) to predict their next move:

* **Positive Gamma Regime (Shock Absorbers ON):** When Spot Price > Zero-Gamma Level. Dealers are long gamma. To hedge, they are forced to *buy* when the price drops and *sell* when the price rises. This creates a mean-reverting environment, suppressing volatility and anchoring the market.
* **Negative Gamma Regime (The Ice Rink):** When Spot Price < Zero-Gamma Level. Dealers are short gamma. To hedge, they are forced to *sell* into dips and *buy* into rips. This creates a momentum-chasing environment, exacerbating price swings and triggering extreme volatility.
* **Zero-Gamma Level (The Flip):** The exact pivot point where market maker behavior shifts from stabilizing to destabilizing. 

## Features
* **Live Options Chain Parsing:** Integrates directly with `yfinance` to pull real-time open interest and implied volatility data for the nearest expiration cycle.
* **Dynamic Strike Filtering:** Automatically isolates the relevant option strikes (±10% of the current spot price) to filter out deep out-of-the-money noise.
* **Algorithmic Regime Detection:** Calculates the absolute minimum difference between Call GEX and Put GEX to pinpoint the exact Gamma Flip level and output the current market regime.
* **Terminal Dashboard:** To look cool like Bloomberg obviously.

## Requirements
Ensure you have the required Python libraries installed:
```bash
pip install yfinance pandas numpy