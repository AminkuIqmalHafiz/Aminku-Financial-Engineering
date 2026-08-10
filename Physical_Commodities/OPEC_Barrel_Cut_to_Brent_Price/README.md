***

# OPEC Macro Event Analyzer

### Overview
The OPEC Macro Event Analyzer is a Python script simulation designed to measure and visualize the structural price impact of historical OPEC production cuts. By analyzing Brent Crude prices the month before and the month after a major announcement, the script calculates the percentage change and renders a clear visual thesis of market reaction.

### Features
* **Zero-API Architecture:** Utilizes hardcoded dictionary arrays for immediate execution, completely bypassing external API rate limits or authentication walls.
* **Vectorized Math:** Leverages `pandas` to instantly calculate absolute price deltas and percentage changes across the entire dataset simultaneously.
* **Conditional Visual Rendering:** Uses `matplotlib` list comprehensions to dynamically color-code the output chart (Green for bullish price action, Red for bearish/failed cuts).
* **Terminal Diagnostics:** Prints a clean DataFrame to the console for quick numerical auditing before launching the visualization.

### The Engineering Thesis
In macro petroleum trading, not all production cuts are treated equally by the market. Some cuts (like the historic COVID-19 intervention) trigger massive bullish reversals, while others (like the November 2022 cut) fail to halt a broader macroeconomic terms. This tool isolates specific historical events to quickly identify whether the market hyped by the news, follow-up perfectly with the change, or simply ignored the it due to broader demand disruption.

### Installation & Requirements
This script requires the standard Python data science stack (pandas) and visualizer (matplotlib) .

```bash
# Install the required dependencies
pip install pandas matplotlib

# Clone the repository and navigate to the directory
git clone https://github.com/yourusername/OPEC-Event-Analyzer.git
cd OPEC-Event-Analyzer
```

### Usage
Run the script natively in your terminal. The numerical data will print directly to the console, and a Matplotlib window will launch to display the visual bar chart.

```bash
python opec_event_analyzer.py
```

### Sample Output Matrix
```text
            Event  Price_Month_Before  Price_Month_After  Pct_Change
0     Vienna 2016               53.31              54.58    2.382292
1  COVID Cut 2020               18.38              29.38   59.847660
2    Nov 2022 Cut               93.33              80.92  -13.296903
3      Saudi 2023               74.84              80.11    7.041689
```
*(A Matplotlib window will launch automatically to display the conditionally formatted bar chart).*
