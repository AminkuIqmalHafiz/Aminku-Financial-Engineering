# Convexity Desk 

## Overview
Convexity Desk is a Python-based quantitative terminal designed to map interactive 3D options volatility surfaces in real-time. By filtering for Out-Of-The-Money (OTM) derivatives across the term structure, it visualizes the exact mathematical curvature of market fear and institutional hedging.

## Features
* **Live Volatility Mapping:** Pulls live options chain data using the `yfinance` API.
* **Institutional Filtering:** Automatically strips illiquid ITM contracts to map pure Out-Of-The-Money Call and Put convexity.
* **Interactive 3D Surface:** Utilizes `Plotly` to render a fully rotatable 3D surface mapping Strike Price vs. Days to Expiration (DTE) vs. Implied Volatility (IV).

## The Engineering Thesis
Standard retail trading relies on linear, directional bets. Quantitative institutional trading relies on the convex payout of variance sigma^2. This terminal allows the user to visually analyze the "Volatility Smile" and Term Structure to identify spatial mispricings in the derivatives market. 

## Requirements
`pip install yfinance pandas numpy plotly`

## Usage
Run the script and input any valid ticker symbol (e.g., SPY, NVDA, USO) to generate the live 3D surface.