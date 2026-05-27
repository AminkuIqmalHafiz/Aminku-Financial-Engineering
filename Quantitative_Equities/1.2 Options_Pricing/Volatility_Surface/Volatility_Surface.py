import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
from datetime import datetime
import warnings

# Suppress pandas warnings for a clean terminal
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    try:
        print("\n" + "="*50)
        print("INSTITUTIONAL 3D VOLATILITY SURFACE (TURBO)")
        print("="*50)

        # ==========================================
        # 1. DATA EXTRACTION
        # ==========================================
        # Defaulting to USO for the Petroleum Engineering macro edge
        ticker_symbol = input("\n[?] Enter Ticker Symbol (e.g., USO, SPY) [Default: USO]: ").strip().upper()
        if not ticker_symbol:
            ticker_symbol = "USO"
        
        print(f"[>] Locking onto {ticker_symbol}... Pulling live options data.")

        ticker = yf.Ticker(ticker_symbol)
        try:
            current_price = ticker.fast_info['lastPrice']
        except Exception:
            raise ValueError(f"Could not fetch data for {ticker_symbol}. Check the ticker.")

        expirations = ticker.options
        data = []

        print("[>] Processing nearest 10 expiration dates...")
        
        # Loop through the next 10 expiration dates
        for exp in expirations[:10]:
            opt = ticker.option_chain(exp)
            
            exp_date = datetime.strptime(exp, '%Y-%m-%d')
            dte = (exp_date - datetime.now()).days
            if dte <= 0: dte = 1 
                
            # OTM Calls (Right side of the bowl)
            calls = opt.calls[(opt.calls['strike'] > current_price) & 
                              (opt.calls['strike'] < current_price * 1.30)]
            for index, row in calls.iterrows():
                if row['impliedVolatility'] > 0.01:
                    data.append({
                        'Strike': row['strike'],
                        'DTE': dte,
                        'IV': row['impliedVolatility']
                    })
                    
            # OTM Puts (Left side of the bowl)
            puts = opt.puts[(opt.puts['strike'] < current_price) & 
                            (opt.puts['strike'] > current_price * 0.70)]
            for index, row in puts.iterrows():
                if row['impliedVolatility'] > 0.01:
                    data.append({
                        'Strike': row['strike'],
                        'DTE': dte,
                        'IV': row['impliedVolatility']
                    })

        df = pd.DataFrame(data)

        if df.empty:
            raise ValueError("No options data found. The market might be closed or the ticker is invalid.")

        # ==========================================
        # 2. THE INTERPOLATION & SMOOTHING ENGINE
        # ==========================================
        print("[>] Interpolating missing data to construct a continuous 3D layer...")

        # Create a perfectly spaced mathematical grid (100x100 resolution)
        strike_grid = np.linspace(df['Strike'].min(), df['Strike'].max(), 100)
        dte_grid = np.linspace(df['DTE'].min(), df['DTE'].max(), 100)
        X, Y = np.meshgrid(strike_grid, dte_grid)

        # Extract the scattered real data points
        points = df[['Strike', 'DTE']].values
        values = df['IV'].values

        # Step 1: Linear interpolation for the main structure
        Z = griddata(points, values, (X, Y), method='linear')

        # Step 2: Nearest-neighbor fallback to patch the jagged outer edges
        Z_nearest = griddata(points, values, (X, Y), method='nearest')
        Z[np.isnan(Z)] = Z_nearest[np.isnan(Z)]

        # Step 3: Gaussian Smoothing (The "Sandpaper")
        print("[>] Applying Gaussian filter to smooth market noise...")
        Z = gaussian_filter(Z, sigma=1.5) 

        # ==========================================
        # 3. RENDER THE 3D SURFACE
        # ==========================================
        print("[>] Rendering the Convexity Desk 3D Surface...")

        fig = go.Figure()

        # Build the solid, smoothed surface layer with the Turbo upgrade
        fig.add_trace(go.Surface(
            x=X, 
            y=Y, 
            z=Z,
            colorscale='Turbo', # The thermal camera scroll-stopper
            opacity=0.95,
            contours_z=dict(show=True, usecolormap=True, highlightcolor="white", project_z=True), # Topographic map lines
            name='Vol Surface'
        ))

        # Add a visual anchor line showing exactly where the current spot price is
        fig.add_trace(go.Scatter3d(
            x=[current_price, current_price],
            y=[df['DTE'].min(), df['DTE'].max()],
            z=[np.nanmin(Z), np.nanmax(Z)], 
            mode='lines',
            line=dict(color='white', width=5, dash='dash'),
            name='Current Spot Price'
        ))

        fig.update_layout(
            title=f'{ticker_symbol} 3D Volatility Surface',
            scene=dict(
                xaxis_title='Strike Price ($)',
                yaxis_title='Days to Expiration (DTE)',
                zaxis_title='Implied Volatility (IV)',
                camera=dict(eye=dict(x=1.5, y=-1.5, z=0.5)) 
            ),
            template="plotly_dark",
            margin=dict(l=0, r=0, b=0, t=40)
        )

        fig.show()
        print("\n[✓] OPERATION SUCCESSFUL. 3D Surface opened in browser.")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n[!!!] CRITICAL ERROR ENCOUNTERED: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("="*50)
        input("Press ENTER to exit the program...")