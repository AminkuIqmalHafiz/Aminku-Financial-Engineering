# Quantitative Cost-of-Carry Engine (Forward Pricing Model)

## Overview
The Cost-of-Carry Engine is a Python-based quantitative terminal tool designed to calculate the theoretical fair value of forward and futures contracts. Utilizing continuous compounding mathematics, the engine holds an essential line between the spot market and derivatives pricing across both financial equities and physical commodities. 

This tool establishes the mathematical baseline required to identify structural mispricings, regime shifts, and risk-free arbitrage opportunities across the term structure.

## The Quantitative Edge
In derivatives trading, the futures price is entirely dictated by the cost of holding the underlying asset. By mapping these carrying costs, this engine identifies the mathematical structure of the market:

* **Contango (Forward Premium):** When the theoretical forward price ($F_0$) is strictly greater than the spot price ($S_0$). The market is actively pricing in the cost of financing and physical storage. The term structure slopes upward.
* **Backwardation (Forward Discount):** When the theoretical forward price ($F_0$) is strictly less than the spot price ($S_0$). Driven by high convenience yields (scarcity), physical traders will pay a massive premium for immediate delivery. The term structure slopes downward.
* **Arbitrage Detection:** If the actual traded futures price deviates from this engine's theoretical calculation, a pure "Cash-and-Carry" or "Reverse Cash-and-Carry" arbitrage opportunity exists.

## Features
* **Dual-Asset Architecture:** You can choose your preferable pricing equation based on the asset class. Financial assets (Equities, FX) strictly process interest and dividend yields, while Consumption assets (Crude Oil, Agriculture) inhibit physical storage costs and convenience yields properties.
* **Continuous Compounding Math:** Utilizes the continuous model $F_0 = S_0 \cdot e^{(r+u-q)T}$ for institutional-grade accuracy over discrete pricing models.
* **Algorithmic Regime Detection:** Automatically compares the calculated forward price against the spot price to declare the current market regime (Contango vs. Backwardation).
* **Terminal Dashboard:** Formatted for high-contrast, rapid CLI reading mimicking institutional desk infrastructure.

## Requirements
This script utilizes Python's standard utility libraries. No external packages or API keys are required.
* `math`
* `os`
* `datetime`

## Setup & Execution
1. Save the script as `cost_of_carry_engine.py` within your primary quantitative directory.
2. Run the scanner via your terminal:
   ```bash
   python cost_of_carry_engine.py