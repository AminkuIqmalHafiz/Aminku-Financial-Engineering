import math

def risk_neutral_binomial_pricer(S_current, strike, up_price, down_price, risk_free_rate, time_years):
    """
    Calculates the exact, arbitrage-free price of a Call Option using the 
    Risk-Neutral Measure (Q), completely ignoring real-world market predictions.
    """
    print("--- INITIATING RISK-NEUTRAL PRICING ALGORITHM ---")
    
    # 1. Calculate the movement ratios based on the discrete inputs
    up_factor = up_price / S_current
    down_factor = down_price / S_current
    
    # 2. THE GIRSANOV HACK: Calculate the Q-Probability (q)
    # Notice we do NOT ask for the user's expected return. We force the expected
    # growth to equal the risk-free rate to create our Equivalent Martingale Measure.
    q = (math.exp(risk_free_rate * time_years) - down_factor) / (up_factor - down_factor)
    print(f"Risk-Neutral Probability (Q-Measure): {q * 100:.2f}%")
    
    # 3. Calculate the payouts in both future realities
    payoff_up = max(0, up_price - strike)
    payoff_down = max(0, down_price - strike)
    
    # 4. Calculate the Expected Payoff under Measure Q
    expected_payoff_Q = (q * payoff_up) + ((1 - q) * payoff_down)
    print(f"Expected Future Payoff under Q: ${expected_payoff_Q:.2f}")
    
    # 5. Discount the Q-payoff back to today using continuous compounding
    option_price_today = math.exp(-risk_free_rate * time_years) * expected_payoff_Q
    
    return option_price_today

# --- RUNNING THE CODE ---
# Using the exact parameters from our previous example
S0 = 100      # Current Stock Price
K = 100       # Strike Price
U = 120       # Up-State Price
D = 90        # Down-State Price
r = 0.05      # 5% Risk-Free Rate
T = 1.0       # 1 Year to expiration

fair_value = risk_neutral_binomial_pricer(S0, K, U, D, r, T)
print(f"ARBITRAGE-FREE CALL OPTION PRICE: ${fair_value:.2f}")