# Security Policy

## Supported Versions
Currently, only the `Main` branch is actively supported with security updates. 

## Live Capital Disclaimer
**WARNING:** The quantitative engines, pricer models, and arbitrage scanners in this repository are built for academic, theoretical, and research purposes. Do not connect these engines directly to live brokerage APIs (e.g., Interactive Brokers) with real capital without conducting your own independent audits. The maintainers are not responsible for financial losses due to execution errors, API latency, or mathematical model breakdown.

## Reporting a Vulnerability
If you discover a critical vulnerability—especially one that could cause API key leakage or catastrophic mathematical overflows in the pricing engines—please do NOT open a public issue. 

Instead, please report it via GitHub's private vulnerability reporting feature in the "Security" tab of this repository. We will review the mathematical or code-based vulnerability and deploy a patch.
