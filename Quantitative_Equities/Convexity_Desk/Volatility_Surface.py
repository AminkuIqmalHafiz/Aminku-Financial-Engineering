import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. Dynamic Ticker Input
ticker_symbol = input("Enter Ticker Symbol (e.g., SPY, NVDA, AAPL): ").upper()
print(f"Locking onto {ticker_symbol}... Pulling live options data.")

ticker = yf.Ticker(ticker_symbol)
try:
    current_price = ticker.fast_info['lastPrice']
except Exception:
    print(f"Could not fetch data for {ticker_symbol}. Check the ticker and try again.")
    exit()

expirations = ticker.options
data = []

# 2. Loop through the next 10 expiration dates
for exp in expirations[:10]:
    opt = ticker.option_chain(exp)
    
    # Calculate exactly how many days until expiration (DTE)
    exp_date = datetime.strptime(exp, '%Y-%m-%d')
    dte = (exp_date - datetime.now()).days
    if dte <= 0: dte = 1 
        
    # 3. Filter for Out-Of-The-Money (OTM) Options to build the Volatility Smile
    
    # OTM Calls (Right side of the bowl: Strikes > Current Price)
    calls = opt.calls[(opt.calls['strike'] > current_price) & 
                      (opt.calls['strike'] < current_price * 1.30)]
    for index, row in calls.iterrows():
        if row['impliedVolatility'] > 0.01: # Filter out broken data
            data.append({
                'Strike': row['strike'],
                'DTE': dte,
                'IV': row['impliedVolatility'],
                'Type': 'Call'
            })
            
    # OTM Puts (Left side of the bowl: Strikes < Current Price)
    puts = opt.puts[(opt.puts['strike'] < current_price) & 
                    (opt.puts['strike'] > current_price * 0.70)]
    for index, row in puts.iterrows():
        if row['impliedVolatility'] > 0.01:
            data.append({
                'Strike': row['strike'],
                'DTE': dte,
                'IV': row['impliedVolatility'],
                'Type': 'Put'
            })

df = pd.DataFrame(data)

if df.empty:
    print("No options data found. The market might be closed or the ticker is invalid.")
    exit()

# 4. Render the Convexity Desk 3D Surface
print("Rendering the 3D Volatility Surface...")

# Split the data so we can color Calls and Puts differently
calls_df = df[df['Type'] == 'Call']
puts_df = df[df['Type'] == 'Put']

fig = go.Figure()

# Plot the Puts (Red dots on the left)
fig.add_trace(go.Scatter3d(
    x=puts_df['Strike'], y=puts_df['DTE'], z=puts_df['IV'],
    mode='markers', name='OTM Puts',
    marker=dict(size=4, color='red', opacity=0.8)
))

# Plot the Calls (Green dots on the right)
fig.add_trace(go.Scatter3d(
    x=calls_df['Strike'], y=calls_df['DTE'], z=calls_df['IV'],
    mode='markers', name='OTM Calls',
    marker=dict(size=4, color='green', opacity=0.8)
))

fig.update_layout(
    title=f'Convexity Desk: {ticker_symbol} 3D Volatility Surface (Spot Price: ${current_price:.2f})',
    scene=dict(
        xaxis_title='Strike Price ($)',
        yaxis_title='Days to Expiration (DTE)',
        zaxis_title='Implied Volatility (IV)'
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

fig.show()