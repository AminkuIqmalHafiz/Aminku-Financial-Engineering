import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from scipy.optimize import brentq
import warnings

# Suppress pandas chained assignment warnings for clean terminal output
warnings.filterwarnings('ignore')

# ==========================================
# 1. QUANTITATIVE MATH (BLACK-SCHOLES)
# ==========================================
def calculate_d1_d2(S, K, T, r, sigma):
    T = max(T, 1e-5)
    sigma = max(sigma, 1e-5)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

def bs_call_price(S, K, T, r, sigma):
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def calculate_gamma(S, K, T, r, sigma):
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    T = max(T, 1e-5)
    sigma = max(sigma, 1e-5)
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))

def calculate_vega(S, K, T, r, sigma):
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    T = max(T, 1e-5)
    return (S * norm.pdf(d1) * np.sqrt(T)) / 100 

def implied_volatility(market_price, S, K, T, r):
    objective_function = lambda sigma: bs_call_price(S, K, T, r, sigma) - market_price
    try:
        return brentq(objective_function, 0.01, 3.0) 
    except ValueError:
        return np.nan 

# ==========================================
# 2. DATA EXTRACTION & PROCESSING
# ==========================================
def fetch_options_chain(ticker_symbol, risk_free_rate=0.05):
    print(f"[>] Establishing connection to Yahoo Finance API for {ticker_symbol}...")
    tk = yf.Ticker(ticker_symbol)
    
    try:
        spot_price = tk.history(period="1d")['Close'].iloc[-1]
    except Exception:
        print("[!] FATAL ERROR: Could not fetch Spot Price. Check ticker symbol or internet connection.")
        return None, None

    print(f"[>] Live Spot Price secured: ${spot_price:.2f}")
    
    expirations = tk.options
    if not expirations:
        print("[!] FATAL ERROR: No options chain found for this ticker.")
        return None, None

    target_expirations = expirations[:6] 
    print(f"[>] Processing nearest {len(target_expirations)} expiration dates...")
    
    master_chain = []
    
    for exp in target_expirations:
        opt = tk.option_chain(exp)
        calls = opt.calls
        
        # Filter: Only look at strikes +/- 10% from the current spot price
        calls = calls[(calls['strike'] >= spot_price * 0.90) & (calls['strike'] <= spot_price * 1.10)]
        
        days_to_exp = (pd.to_datetime(exp) - pd.Timestamp.today().normalize()).days
        T = max(days_to_exp / 365.0, 1e-5)
        
        for _, row in calls.iterrows():
            K = row['strike']
            market_price = row['lastPrice']
            
            iv = implied_volatility(market_price, spot_price, K, T, risk_free_rate)
            
            if not np.isnan(iv):
                gamma = calculate_gamma(spot_price, K, T, risk_free_rate, iv)
                vega = calculate_vega(spot_price, K, T, risk_free_rate, iv)
                
                master_chain.append({
                    'Expiration': exp,
                    'Days to Expiry': days_to_exp,
                    'Strike': K,
                    'Implied Volatility': iv,
                    'Gamma': gamma,
                    'Vega': vega
                })
                
    return pd.DataFrame(master_chain), spot_price

# ==========================================
# 3. EXECUTION & RENDERING
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("⚡ INSTITUTIONAL OPTIONS RADAR: TERMINAL EDITION ⚡")
    print("="*50)
    
    # User Input
    ticker = input("\n[?] Enter Ticker Symbol (e.g., SPY): ").upper()
    if not ticker:
        ticker = "SPY"
        print(f"[*] Defaulting to {ticker}")
        
    RISK_FREE_RATE = 0.05
    
    # Run Engine
    df, spot = fetch_options_chain(ticker, RISK_FREE_RATE)
    
    if df is not None and not df.empty:
        print("[>] Data extraction and Black-Scholes processing complete.")
        print("[>] Formatting matrices...")
        
        df['Strike'] = df['Strike'].round(1)
        
        gamma_pivot = df.pivot_table(values='Gamma', index='Strike', columns='Days to Expiry', aggfunc='mean')
        vega_pivot = df.pivot_table(values='Vega', index='Strike', columns='Days to Expiry', aggfunc='mean')

        # --- Render Gamma ---
        print("[>] Rendering Gamma Concentration Heatmap...")
        fig_gamma = go.Figure(data=go.Heatmap(
            z=gamma_pivot.values, x=gamma_pivot.columns, y=gamma_pivot.index,
            colorscale='Inferno', hoverongaps=False
        ))
        fig_gamma.add_hline(y=spot, line_dash="dash", line_color="white", annotation_text="Current Spot Price")
        fig_gamma.update_layout(
            title=f"Gamma Concentration (Acceleration Risk) | {ticker} Spot: ${spot:.2f}",
            xaxis_title="Days to Expiration", yaxis_title="Strike Price ($)",
            template="plotly_dark", height=800, width=1000
        )
        # fig.show() opens the interactive chart in your default web browser
        fig_gamma.show() 

        # --- Render Vega ---
        print("[>] Rendering Vega Concentration Heatmap...")
        fig_vega = go.Figure(data=go.Heatmap(
            z=vega_pivot.values, x=vega_pivot.columns, y=vega_pivot.index,
            colorscale='Viridis', hoverongaps=False
        ))
        fig_vega.add_hline(y=spot, line_dash="dash", line_color="white", annotation_text="Current Spot Price")
        fig_vega.update_layout(
            title=f"Vega Concentration (Volatility Risk) | {ticker} Spot: ${spot:.2f}",
            xaxis_title="Days to Expiration", yaxis_title="Strike Price ($)",
            template="plotly_dark", height=800, width=1000
        )
        fig_vega.show()
        
        print("\n[✓] OPERATION SUCCESSFUL. Heatmaps opened in browser.")
        print("="*50 + "\n")
    else:
        print("\n[!] OPERATION FAILED. Matrix could not be built.\n")