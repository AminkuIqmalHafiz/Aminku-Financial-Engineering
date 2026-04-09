## Description
Provide a brief description of the new quantitative model, scanner, or fix included in this PR. What financial engineering problem does it solve?

## Mathematical Framework
- [ ] If adding a new pricing model, the underlying theory (e.g., Black-Scholes, Binomial Lattice) is documented in the PR or linked README.
- [ ] Variables conform to standard financial notation where possible (S0, K, r, T, sigma).

## Pre-Flight Checks
Before requesting a review, please confirm the following:
- [ ] I have tested this code with live market data (e.g., via `yfinance`) and the outputs match theoretical expectations.
- [ ] Edge cases have been handled (e.g., avoiding division by zero if Time to Maturity `T = 0`).
- [ ] Heavy calculations rely on `numpy` or `pandas` rather than standard Python loops.
- [ ] The code runs without throwing syntax or dependency errors.

## Screenshots / Output (If applicable)
Paste a snippet of the terminal output or the data visual showing the engine running successfully.
