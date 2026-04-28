# Institutional Options Radar: Gamma & Vega Heatmaps 

## Overview
Retail traders focus on first-order directional risk (Delta). Institutional trading desks focus on non-linear curvature (Gamma) and volatility exposure (Vega/Vanna). 

This repository contains a standalone, terminal-executed Python engine that pulls the live options chain for any given ticker, reverse-engineers the Implied Volatility using a root-finding algorithm, and plots the exact concentration of institutional risk across Strike Prices and Days to Expiration (DTE).

## Core Quantitative Mechanics

### 1. Gamma Concentration
The engine visualizes the non-linear acceleration of risk. As time to expiration approaches zero, Gamma does not decay linearly,it spikes violently into a mathematical singularity right At-The-Money (ATM). This heatmap maps exactly where "Pin Risk" is highest, showing where algorithmic desks will be forced into high-frequency rehedging loops.

### 2. The Vanna Squeeze
By pulling live market data rather than assuming a flat textbook distribution, this tool visually captures the Volatility Skew (the Smirk). 
* Because the market aggressively bids up downside Put options for crash insurance, downside IV is extremely high. 
* Mathematically, higher IV flattens Gamma. Lower IV (on the upside) causes Gamma to spike.
* The resulting heatmap physically proves how Vanna (the cross-sensitivity of Delta to Volatility) mutates the risk curve, creating asymmetrical, highly concentrated whiplash risk on upside strikes.

### 3. Vega Vulnerability
The secondary heatmap maps pure Vega, revealing exactly which strikes and tenors hold the most "fear premium" and are most vulnerable to a macroeconomic Volatility Crush.

## Tech Stack & Architecture
* **Data Ingestion:** `yfinance` (Live spot pricing and options chain extraction).
* **Quantitative Engine:** `scipy.stats`, `scipy.optimize` (Newton-Raphson / Brent's method to extract IV and calculate Black-Scholes partial derivatives).
* **Matrix Visualization:** `plotly` (Renders interactive, browser-based heatmaps directly from the terminal).
* **Data Structuring:** `pandas`, `numpy`.

## Execution
Run the script directly via terminal. The engine operates entirely in the back-end (no web server required) and will automatically render the interactive heatmaps in your default web browser.

```bash
# Install dependencies
pip install yfinance scipy pandas numpy plotly

# Execute the radar
python Vanna


Dashboard Output
Terminal: Logs the real-time spot price, connection status, and matrix construction.

Browser (Plotly): 

Gamma Heatmap: Identifies high-acceleration 0DTE zones.

Vega Heatmap: Identifies premium inflation zones in far-tenor ATM options.

"You cannot manage non-linear risk if you cannot see it. Delta tells you where the move is pointing; Gamma and Vanna tell you when the move is going to spin out."