import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import os

# --- Colour for The Bloomberg Aesthetic---
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def calculate_gamma_flip(ticker_symbol):
    # Clears the terminal before running for a clean screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{CYAN}[{timestamp}] SYSTEM: Initializing Gamma Engine for {ticker_symbol}...{RESET}")
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # Adding a quick check to make sure the ticker actually exists
        history = ticker.history(period="1d")
        if history.empty:
            print(f"{RED}[ERROR] Ticker '{ticker_symbol}' not found. Check spelling.{RESET}")
            return
            
        spot_price = history['Close'].iloc[-1]
        
        expirations = ticker.options
        next_exp = expirations[0] 
        print(f"{CYAN}[{timestamp}] INFO: Processing options chain for {next_exp}...{RESET}\n")
        
        chain = ticker.option_chain(next_exp)
        calls = chain.calls
        puts = chain.puts
        
        strike_min = spot_price * 0.90
        strike_max = spot_price * 1.10
        
        calls = calls[(calls['strike'] >= strike_min) & (calls['strike'] <= strike_max)]
        puts = puts[(puts['strike'] >= strike_min) & (puts['strike'] <= strike_max)]
        
        calls['Call_GEX'] = calls['openInterest'] * calls['impliedVolatility']
        puts['Put_GEX'] = puts['openInterest'] * puts['impliedVolatility'] * -1 
        
        gex_profile = pd.merge(calls[['strike', 'Call_GEX']], puts[['strike', 'Put_GEX']], on='strike', how='outer').fillna(0)
        gex_profile['Net_GEX'] = gex_profile['Call_GEX'] + gex_profile['Put_GEX']
        
        absolute_zero_diff = gex_profile['Net_GEX'].abs().idxmin()
        gamma_flip_strike = gex_profile.loc[absolute_zero_diff, 'strike']
        
        # --- THE BLOOMBERG UI DASHBOARD ---
        header = f"INSTITUTIONAL GAMMA EXPOSURE (GEX) REPORT : {ticker_symbol}"
        spot_str = f"CURRENT SPOT PRICE : ${spot_price:.2f}"
        gamma_str = f"ZERO GAMMA LEVEL   : ${gamma_flip_strike:.2f}"
        
        print(f"{BOLD}{YELLOW}╔══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}{YELLOW}║  {header:<60}║{RESET}")
        print(f"{BOLD}{YELLOW}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {spot_str:<60}{BOLD}{YELLOW}║{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {gamma_str:<60}{BOLD}{YELLOW}║{RESET}")
        print(f"{BOLD}{YELLOW}╠══════════════════════════════════════════════════════════════╣{RESET}")
        
        # The Edge Logic
        if spot_price > gamma_flip_strike:
            distance = spot_price - gamma_flip_strike
            status_text = "[STATUS] POSITIVE GAMMA REGIME (Shock Absorbers ON)"
            edge_text   = "[EDGE]   Market is stable. Dealers buying dips."
            room_text   = f"[ROOM]   Buffer to flip: ${distance:.2f}"
            color = GREEN
        else:
            distance = gamma_flip_strike - spot_price
            status_text = "[STATUS] NEGATIVE GAMMA REGIME (Ice Rink ON)"
            edge_text   = "[EDGE]   Dealers selling dips. Expect massive swings."
            room_text   = f"[ROOM]   Distance to safety: ${distance:.2f}"
            color = RED
            
        print(f"{BOLD}{YELLOW}║{RESET}  {color}{status_text:<60}{RESET}{BOLD}{YELLOW}║{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {color}{edge_text:<60}{RESET}{BOLD}{YELLOW}║{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {color}{room_text:<60}{RESET}{BOLD}{YELLOW}║{RESET}")
            
        print(f"{BOLD}{YELLOW}╚══════════════════════════════════════════════════════════════╝{RESET}\n")

    except Exception as e:
        print(f"{RED}[ERROR] Engine failed. Make sure options exist for this ticker. Details: {e}{RESET}")

if __name__ == "__main__":
    # Clear screen first
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Prompt the user for the ticker
    print(f"{BOLD}{CYAN}=== QUANTITATIVE GEX TERMINAL ==={RESET}")
    user_input = input(f"Enter Ticker Symbol (e.g., SPY, QQQ, TSLA): ").upper()
    
    # Run the engine
    calculate_gamma_flip(user_input)