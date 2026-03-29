import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import os

# --- ANSI COLOR CODES (The Bloomberg Aesthetic) ---
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def calculate_fat_tails(ticker_symbol):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{CYAN}[{timestamp}] SYSTEM: Initializing Kurtosis Engine for {ticker_symbol}...{RESET}\n")
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # Pull 1 year of daily closing prices to get a solid statistical sample
        history = ticker.history(period="1y")
        if history.empty:
            print(f"{RED}[ERROR] Ticker '{ticker_symbol}' not found. Check spelling.{RESET}")
            return
            
        # The Math: Calculate daily percentage returns and find the Excess Kurtosis
        history['Returns'] = history['Close'].pct_change()
        history = history.dropna()
        
        # Pandas .kurt() automatically calculates Excess Kurtosis (Fisher's definition, baseline 0)
        excess_kurtosis = history['Returns'].kurt()
        volatility = history['Returns'].std() * np.sqrt(252) * 100 # Annualized Volatility
        
        # --- THE BULLETPROOF BLOOMBERG UI ---
        header = f"TAIL RISK & KURTOSIS REPORT : {ticker_symbol}"
        kurt_str = f"EXCESS KURTOSIS    : {excess_kurtosis:.2f}"
        vol_str = f"ANNUAL VOLATILITY  : {volatility:.2f}%"
        
        print(f"{BOLD}{YELLOW}╔══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}{YELLOW}║  {header:<60}║{RESET}")
        print(f"{BOLD}{YELLOW}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {kurt_str:<60}{BOLD}{YELLOW}║{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {vol_str:<60}{BOLD}{YELLOW}║{RESET}")
        print(f"{BOLD}{YELLOW}╠══════════════════════════════════════════════════════════════╣{RESET}")
        
        # The Edge Logic for Fat Tails
        if excess_kurtosis > 2.0:
            status_text = "[STATUS] EXTREME FAT TAILS (Leptokurtic)"
            edge_text   = "[EDGE]   High risk of violent, unpredictable price swings."
            strat_text  = "[STRAT]  Options are likely underpricing extreme outlier moves."
            color = RED
        elif excess_kurtosis > 0.5:
            status_text = "[STATUS] MODERATE FAT TAILS"
            edge_text   = "[EDGE]   Standard risk. Occasional outlier moves expected."
            strat_text  = "[STRAT]  Proceed with standard risk management."
            color = YELLOW
        else:
            status_text = "[STATUS] NORMAL DISTRIBUTION (Platykurtic / Mesokurtic)"
            edge_text   = "[EDGE]   Price action is highly predictable and contained."
            strat_text  = "[STRAT]  Standard mathematical models are reliable here."
            color = GREEN
            
        print(f"{BOLD}{YELLOW}║{RESET}  {color}{status_text:<60}{RESET}{BOLD}{YELLOW}║{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {color}{edge_text:<60}{RESET}{BOLD}{YELLOW}║{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {color}{strat_text:<60}{RESET}{BOLD}{YELLOW}║{RESET}")
        print(f"{BOLD}{YELLOW}╚══════════════════════════════════════════════════════════════╝{RESET}\n")

    except Exception as e:
        print(f"{RED}[ERROR] Engine failed. Details: {e}{RESET}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{BOLD}{CYAN}=== QUANTITATIVE TAIL RISK TERMINAL ==={RESET}")
    user_input = input(f"Enter Ticker Symbol (e.g., SPY, QQQ, TSLA): ").upper()
    calculate_fat_tails(user_input)