
```markdown
# Variance Risk Premium Harvester

## File Overview
This script is a structural alpha-generation simulator. It mathematically models institutional volatility-selling strategies designed to harvest the **Variance Risk Premium (VRP)**. 

## Quantitative Mechanics
The engine exploits the spread between market fear and physical reality:
* **Implied Volatility (Measure Q):** Simulates the extraction of inflated premiums by selling an At-The-Money (ATM) straddle during periods of macroeconomic panic.
* **Realized Volatility (Measure P):** Utilizes stochastic path generation to simulate the actual physical movement of the underlying asset over a 30-day continuous period.
* **Tail Risk Settlement:** Calculates the net-settlement at expiration, demonstrating the structural profitability of short-volatility strategies while accurately modeling the rare, catastrophic losses associated with unhedged tail risk.

## Execution
Run the script directly via terminal. Because the script utilizes stochastic Monte Carlo-style path generation, every run is unique. Execute it multiple times to observe the distribution of structural wins versus tail-risk losses.
```bash
python vrp_harvester.py
Dependencies
Python 3.x

numpy (Vectorized Math & Normal Distribution Generation)