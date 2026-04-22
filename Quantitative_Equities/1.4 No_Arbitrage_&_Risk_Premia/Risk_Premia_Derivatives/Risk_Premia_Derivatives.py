import numpy as np

def harvest_vrp(S_current, implied_vol, realized_vol, days_to_expiry=30):
    """
    Simulates harvesting the Variance Risk Premium (VRP) by acting as an options 
    seller. We sell volatility when IV is high, and profit if RV is lower.
    """
    print("--- INITIATING VRP HARVEST SIMULATION ---")
    print(f"Market Fear (IV): {implied_vol * 100}% | Actual Movement (RV): {realized_vol * 100}%")
    
    # 1. THE SETUP: Sell an At-The-Money (ATM) Straddle
    # We collect premium based on the market's Fear (Implied Volatility).
    # (Simplified approximation formula for ATM straddle premium)
    premium_collected = S_current * 0.8 * implied_vol * np.sqrt(days_to_expiry / 365)
    print(f"Initial Premium Collected (Cash In): ${premium_collected:.2f}")
    
    # 2. THE REALITY: Simulate 30 days of actual market movement using Measure P (RV)
    # We convert annualized RV to daily RV, then generate random daily returns.
    daily_rv = realized_vol / np.sqrt(252) 
    daily_returns = np.random.normal(0, daily_rv, days_to_expiry)
    
    # Calculate the final stock price after 30 days of random movement
    price_path = S_current * np.exp(np.cumsum(daily_returns))
    final_price = price_path[-1]
    
    # 3. THE SETTLEMENT: Calculate how much the stock physically moved
    actual_physical_move = abs(final_price - S_current)
    print(f"Actual Stock Price at Expiry: ${final_price:.2f} (Moved ${actual_physical_move:.2f})")
    
    # 4. THE HARVEST: Did the premium cover the movement?
    net_profit = premium_collected - actual_physical_move
    
    if net_profit > 0:
        print(f"RESULT: VRP HARVESTED SUCCESSFULLY. Net Profit: ${net_profit:.2f}")
    else:
        print(f"RESULT: TAIL RISK HIT. Loss: ${net_profit:.2f}")
        
    return net_profit

# --- RUNNING THE CODE ---
# Scenario: Market expects a 40% crash/rally, but the stock only moves at a 20% rate.
S0 = 100      # Stock Price
IV = 0.40     # 40% Implied Volatility (Fear)
RV = 0.20     # 20% Realized Volatility (Reality)

profit = harvest_vrp(S0, IV, RV)