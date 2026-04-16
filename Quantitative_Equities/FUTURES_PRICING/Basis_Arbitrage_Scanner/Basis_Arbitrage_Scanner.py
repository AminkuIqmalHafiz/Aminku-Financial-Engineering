import yfinance as yf
import numpy as np
from datetime import datetime

def fetch_live_price(ticker):
    """Pulls the most recent closing price for a given ticker."""
    data = yf.Ticker(ticker)
    # Get the last available daily close
    todays_data = data.history(period="1d")
    return todays_data['Close'].iloc[0]

def calculate_theoretical_future(S0, r, q, T):
    """Applies the continuous Cost-of-Carry formula."""
    # F0 = S0 * e^((r - q) * T) --- we learn today (10 April 26')
    F0 = S0 * np.exp((r - q) * T)
    return F0

def run_arbitrage_scanner():
    print("---INITIATING ARBITRAGE SCANNER ---")
    
    # 1. Define our Parameters 
    spot_ticker = "SPY"
    futures_ticker = "ES=F"  # E-Mini S&P 500 Front-Month Future
    
    r = 0.053  # Risk-free rate (e.g., 5.3% Treasury Bill rate)
    q = 0.013  # SPY continuous dividend yield (approx 1.3%)
    T = 0.25   # Time to maturity in years (Assume 3 months,too much can be huge)
    
    # 2. Fetch Live Market Data
    print(f"Pulling live data for {spot_ticker} and {futures_ticker}...")
    S0 = fetch_live_price(spot_ticker)
    F_market = fetch_live_price(futures_ticker)
    
    # ES=F is priced based on the S&P 500 index (SPX), which is ~10x SPY.
    # We jacked the SPY by 10 times so we can have better comparison with its futures.
    S0_scaled = S0 * 10 
    
    # 3. Calculate Theoretical Fair Value
    F0_theoretical = calculate_theoretical_future(S0_scaled, r, q, T)
    
    # 4. Calculate the Mispricing (Spooky spooky edge)
    mispricing = F_market - F0_theoretical
    
    # 5. Output the Results
    print("\n--- MARKET DATA ---")
    print(f"Live Spot Price (Scaled):  ${S0_scaled:.2f}")
    print(f"Live Futures Price:        ${F_market:.2f}")
    print(f"Theoretical Fair Value:    ${F0_theoretical:.2f}")
    print(f"Absolute Mispricing:       ${mispricing:.2f}")
    
    print("\n--- TRADING SIGNAL ---")
    # 6.Define an arbitrary threshold.
    arbitrage_threshold = 2.00  
    
    if mispricing > arbitrage_threshold:
        print("SIGNAL: Futures are OVERPRICED.")
        print("ACTION: Execute Cash & Carry.")
        print("-> Short the Future, Borrow Cash, Buy the Spot.")
    elif mispricing < -arbitrage_threshold:
        print("SIGNAL: Futures are UNDERPRICED.")
        print("ACTION: Execute Reverse Cash & Carry.")
        print("-> Long the Future, Short the Spot, Invest Cash at risk-free rate.")
    else:
        print("SIGNAL: Market is perfectly priced.")
        print("ACTION: No arbitrage opportunity exists. Do nothing.")

# Run 
if __name__ == "__main__":
    run_arbitrage_scanner()