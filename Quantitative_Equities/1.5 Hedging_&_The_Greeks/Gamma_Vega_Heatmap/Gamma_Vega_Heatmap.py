import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from scipy.optimize import brentq
from scipy.interpolate import griddata
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
# 3. INTERPOLATION ENGINE
# ==========================================
def interpolate_surface(pivot_df):
    """
    Takes a sparse pivot table with NaNs and interpolates missing values
    using a 2D meshgrid to create a smooth continuous surface.
    """
    x, y = np.meshgrid(pivot_df.columns, pivot_df.index)
    mask = ~np.isnan(pivot_df.values)
    
    points = np.column_stack((x[mask], y[mask]))
    values = pivot_df.values[mask]
    
    # Step 1: Linear interpolation for smooth inner gradients
    grid_z = griddata(points, values, (x, y), method='linear')
    
    # Step 2: Nearest-neighbor fallback to patch the outer edges
    grid_z_nearest = griddata(points, values, (x, y), method='nearest')
    grid_z[np.isnan(grid_z)] = grid_z_nearest[np.isnan(grid_z)]
    
    return pd.DataFrame(grid_z, index=pivot_df.index, columns=pivot_df.columns)

# ==========================================
# 4. EXECUTION & RENDERING (CRASH-PROOF)
# ==========================================
if __name__ == "__main__":
    try:
        print("\n" + "="*50)
        print("VOLATILITY SURFACE & GREEKS MAPPER")
        print("="*50)
        
        # User Input
        ticker = input("\n[?] Enter Ticker Symbol (e.g., SPY): ").strip().upper()
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
            
            gamma_pivot_raw = df.pivot_table(values='Gamma', index='Strike', columns='Days to Expiry', aggfunc='mean')
            vega_pivot_raw = df.pivot_table(values='Vega', index='Strike', columns='Days to Expiry', aggfunc='mean')

            print("[>] Interpolating missing matrix data to smooth surfaces...")
            gamma_pivot = interpolate_surface(gamma_pivot_raw)
            vega_pivot = interpolate_surface(vega_pivot_raw)

            # --- Render Gamma ---
            print("[>] Rendering Gamma Concentration Heatmap...")
            fig_gamma = go.Figure(data=go.Heatmap(
                z=gamma_pivot.values, x=gamma_pivot.columns, y=gamma_pivot.index,
                colorscale='Inferno', hoverongaps=False
            ))
            fig_gamma.add_hline(y=spot, line_dash="dash", line_color="white", annotation_text="Current Spot Price")
            fig_gamma.update_layout(
                title=f"Gamma Concentration (Acceleration Risk) | {ticker}",
                xaxis_title="Days to Expiration", yaxis_title="Strike Price ($)",
                template="plotly_dark", height=800, width=1000
            )
            fig_gamma.show() 

            # --- Render Vega ---
            print("[>] Rendering Vega Concentration Heatmap...")
            fig_vega = go.Figure(data=go.Heatmap(
                z=vega_pivot.values, x=vega_pivot.columns, y=vega_pivot.index,
                colorscale='Viridis', hoverongaps=False
            ))
            fig_vega.add_hline(y=spot, line_dash="dash", line_color="white", annotation_text="Current Spot Price")
            fig_vega.update_layout(
                title=f"Vega Concentration (Volatility Risk) | {ticker}",
                xaxis_title="Days to Expiration", yaxis_title="Strike Price ($)",
                template="plotly_dark", height=800, width=1000
            )
            fig_vega.show()
            
            print("\n[✓] OPERATION SUCCESSFUL. Heatmaps opened in browser.")
        else:
            print("\n[!] OPERATION FAILED. Matrix could not be built. Yahoo Finance might be blocking the request or missing data.")

    except Exception as e:
        print(f"\n[!!!] CRITICAL ERROR ENCOUNTERED: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # This absolutely guarantees the terminal stays open so you can read what happened!
        print("="*50)
        input("Press ENTER to exit the program...")