import math
import os
from datetime import datetime

# --- ANSI COLOR CODES ---
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def cost_of_carry_terminal():
    # Clear the terminal for a clean UI
    os.system('cls' if os.name == 'nt' else 'clear')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"{BOLD}{CYAN}=== QUANTITATIVE COST-OF-CARRY ENGINE ==={RESET}")
    print(f"{CYAN}[{timestamp}] SYSTEM: Initializing Forward Pricing Model...{RESET}\n")
    
    try:
        # Step 1: Route the logic based on Asset Type
        print(f"{YELLOW}Select Asset Class Architecture:{RESET}")
        print("1. Financial Asset")
        print("2. Consumption Asset (Crude Oil, Ags)")
        
        asset_choice = input(f"\n{BOLD}Enter 1 or 2: {RESET}").strip()
        
        if asset_choice not in ['1', '2']:
            print(f"{RED}[ERROR] Invalid selection. Terminating process.{RESET}")
            return

        # Step 2: Gather Universal Variables
        S0 = float(input(f"Enter Current Spot Price (S0) [e.g., 5000]: "))
        r = float(input(f"Enter Risk-Free Rate (r) as % [e.g., 5.0]: ")) / 100.0
        T = float(input(f"Enter Time to Maturity (T) in years [e.g., 0.5]: "))
        
        # Step 3: Gather Specific Variables
        if asset_choice == '1':
            asset_type = "FINANCIAL"
            q = float(input(f"Enter Dividend Yield (q) as % [e.g., 1.5]: ")) / 100.0
            u = 0.0 # Force storage to zero for financial assets
        else:
            asset_type = "CONSUMPTION"
            q = float(input(f"Enter Convenience Yield (q) as % [e.g., 4.0]: ")) / 100.0
            u = float(input(f"Enter Storage Cost (u) as % [e.g., 2.0]: ")) / 100.0

        # Step 4: The Math (F = S * e^((r + u - q) * T))
        print(f"\n{CYAN}[SYSTEM] Calculating continuous compounding model...{RESET}")
        carry_cost = r + u - q
        F0 = S0 * math.exp(carry_cost * T)
        
        # Step 5: Market Regime Detection
        if F0 > S0:
            regime = "CONTANGO (Forward Premium)"
            regime_color = GREEN
            edge = "Market is pricing in carrying costs. Curve slopes UP."
        elif F0 < S0:
            regime = "BACKWARDATION (Forward Discount)"
            regime_color = RED
            edge = "High convenience/scarcity. Curve slopes DOWN."
        else:
            regime = "FLAT MARKET"
            regime_color = YELLOW
            edge = "Cost of carry is perfectly neutralized."

        # --- THE TERMINAL UI DASHBOARD ---
        header = f"FORWARD PRICING REPORT : {asset_type} ASSET"
        spot_str = f"CURRENT SPOT PRICE (S0) : ${S0:,.2f}"
        fwd_str = f"THEORETICAL FAIR (F0)   : ${F0:,.2f}"
        
        print(f"\n{BOLD}{YELLOW}╔══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}{YELLOW}║  {header:<60}║{RESET}")
        print(f"{BOLD}{YELLOW}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {spot_str:<60}{BOLD}{YELLOW}║{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {fwd_str:<60}{BOLD}{YELLOW}║{RESET}")
        print(f"{BOLD}{YELLOW}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {regime_color}[STATUS] {regime:<50}{RESET}{BOLD}{YELLOW} ║{RESET}")
        print(f"{BOLD}{YELLOW}║{RESET}  {regime_color}[EDGE]   {edge:<50}{RESET}{BOLD}{YELLOW} ║{RESET}")
        print(f"{BOLD}{YELLOW}╚══════════════════════════════════════════════════════════════╝{RESET}\n")

    except ValueError:
        print(f"{RED}[ERROR] Invalid numeric input. Do not include letters or symbols.{RESET}")

if __name__ == "__main__":
    cost_of_carry_terminal()