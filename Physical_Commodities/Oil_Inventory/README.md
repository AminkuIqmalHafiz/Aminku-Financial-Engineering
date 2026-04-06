# Cushing Physical Storage & Flow Tracker (EIA API v2)

## Overview
The Cushing Storage Tracker is a lightweight, Python-based quantitative terminal tool designed to monitor the physical crude oil inventory at the Cushing, Oklahoma delivery hub. By pulling live data directly from the U.S. Energy Information Administration (EIA) API, this script calculates week-over-week flow momentum and absolute capacity utilization. 

This tool bridges the gap between fundamental physical supply chain data and financial derivative pricing, providing immediate alerts for structural risk in the energy markets.

## The Quantitative Edge
In commodities trading, physical storage constraints dictate the shape of the futures curve. This engine does not just fetch data; it interprets the physical reality to identify potential market regimes:

* **Contango Squeeze Risk (High Utilization):** When tanks approach maximum capacity (> 80%), the market struggles to store excess supply, often forcing the prompt month futures contract to price at a steep discount to later months (Contango). 
* **Backwardation Gamma (Low Utilization):** When tanks run dry (< 30%), physical scarcity dominates. Refiners and physical traders will pay a massive premium for immediate delivery, driving the prompt month higher and creating extreme volatility/backwardation.
* **Flow Momentum:** Tracks the immediate week-over-week delta to identify whether the market is actively in a state of building (Supply > Demand) or drawing (Demand > Supply).

## Features
* **Live EIA v2 API Integration:** Automatically fetches the most recent weekly storage data for Cushing, OK (Series: `W_EPC0_SAX_YCUOK_MBBL`).
* **Automated Capacity Utilization:** Dynamically calculates current inventory against the estimated operational maximum capacity of 76,000,000 barrels.
* **Structural Risk Alerts:** Outputs actionable terminal alerts based on predefined physical threshold parameters.
* **Terminal Dashboard:** Formatted for clean, rapid CLI reading.

## Requirements
Ensure you have the required Python library installed:
```bash
pip install requests
```

## Setup & Execution
1. **Get an API Key:** Register for a free API key at the [U.S. Energy Information Administration (EIA) Open Data Portal](https://www.eia.gov/opendata/).
2. **Configure the Script:** Open the Python script and replace `"INSERT_API_KEY_HERE"` with your actual EIA API key.
3. **Run the Scanner:**
```bash
python cushing_scanner.py
```

## Example Terminal Output
```text
[2026-04-06 14:09:51] SYSTEM: Connecting to U.S. EIA Data API (v2 Pipeline)...

=======================================================
CUSHING (WTI) PHYSICAL STORAGE INVENTORY REPORT
=======================================================
RECORD DATE       : 2026-03-27
CURRENT INVENTORY : 32,500k Barrels
WEEK-OVER-WEEK    : -1,200k Barrels
UTILIZATION RATE  : 42.76%
-------------------------------------------------------
[STATUS] INVENTORY NOMINAL. Storage flowing normally.
[FLOW] DRAWING: Tanks are draining. Demand > Supply.
=======================================================
```

