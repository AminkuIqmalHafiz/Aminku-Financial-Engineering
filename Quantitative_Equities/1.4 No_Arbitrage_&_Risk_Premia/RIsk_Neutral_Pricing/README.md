 
# Risk-Neutral Pricer

## File Overview
This script is a standalone discrete-time options pricing engine utilizing the **Risk-Neutral Pricing Framework**. It proves that derivative fair value is strictly a function of volatility and the risk-free rate, entirely independent of subjective real-world market predictions.

## Mathematical Architecture
This engine calculates the **Equivalent Martingale Measure (Measure Q)**. By applying the logic of Girsanov's Theorem, it mathematically forces the expected growth rate of the underlying asset to equal the risk-free rate. 
* **Synthetic Probability:** Dynamically calculates the $Q$-probability ($q$) required to ensure the underlying binomial lattice acts as a perfect Martingale.
* **Continuous Discounting:** Applies exponential compounding ($e^{-rT}$) to discount expected future payoffs back to their absolute Present Value.

## Execution
Run the script directly via terminal. The engine will output the calculated Risk-Neutral Probability, the Expected Future Payoff under Measure Q, and the final Arbitrage-Free Option Price.
```bash
python risk_neutral_pricer.py
```

## Dependencies
* Python 3.x
* `math` (Standard Library)
```

***
