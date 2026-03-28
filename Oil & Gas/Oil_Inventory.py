import requests
from datetime import datetime

def fetch_cushing_storage_v2():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] SYSTEM: Connecting to U.S. EIA Data API (v2 Pipeline)...")
    
    # Insert your active API key here
    api_key = "INSERT_API_KEY_HERE" 
    url = "https://api.eia.gov/v2/petroleum/stoc/wstk/data/"
    
    # Parameters to pull the last TWO weeks of data
    params = {
        "api_key": api_key,
        "frequency": "weekly",
        "data[0]": "value",
        "facets[series][]": "W_EPC0_SAX_YCUOK_MBBL",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": 0,
        "length": 2 
    }
    
    # The maximum operational limit for Cushing storage
    MAX_CAPACITY_K_BBL = 76000 
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Extract THIS week (Index 0 is the newest data)
        latest_week = data['response']['data'][0]
        current_date = latest_week['period']
        current_bbl_k = float(latest_week['value'])
        
        # Extract LAST week (Index 1 is the previous week)
        prev_week = data['response']['data'][1]
        prev_bbl_k = float(prev_week['value'])
        
        # The Math: Flow Momentum and Capacity Limits
        wow_change = current_bbl_k - prev_bbl_k
        capacity_utilization = (current_bbl_k / MAX_CAPACITY_K_BBL) * 100
        
        # Adds a "+" sign if the change is positive for a cleaner terminal look
        change_symbol = "+" if wow_change > 0 else ""
        
        # --- TERMINAL DASHBOARD OUTPUT ---
        print("\n" + "=" * 55)
        print("CUSHING (WTI) PHYSICAL STORAGE INVENTORY REPORT")
        print("=" * 55)
        print(f"RECORD DATE       : {current_date}")
        print(f"CURRENT INVENTORY : {current_bbl_k:,.0f}k Barrels")
        print(f"WEEK-OVER-WEEK    : {change_symbol}{wow_change:,.0f}k Barrels")
        print(f"UTILIZATION RATE  : {capacity_utilization:.2f}%")
        print("-" * 55)
        
        # --- ULTIMATE MARKET LOGIC (Absolute + Momentum) ---
        
        # 1. Structural Risk (The Capacity Percentage)
        if capacity_utilization > 80:
            print("[ALERT] CRITICAL INVENTORY. Tanks near maximum capacity.")
            print("[STRATEGY] Contango squeeze risk. Do not go long physical.")
        elif capacity_utilization < 30:
            print("[ALERT] INVENTORY DEPLETION. Tanks running dry.")
            print("[STRATEGY] Backwardation risk. Watch for violent upside gamma.")
        else:
            print("[STATUS] INVENTORY NOMINAL. Storage flowing normally.")
            
        # 2. Flow Momentum (The Week-Over-Week Delta)
        if wow_change > 0:
            print("[FLOW] BUILDING: Tanks are filling up. Supply > Demand.")
        elif wow_change < 0:
            print("[FLOW] DRAWING: Tanks are draining. Demand > Supply.")
        else:
            print("[FLOW] STAGNANT: Zero net change in physical inventory.")
            
        print("=" * 55 + "\n")

    except Exception as e:
         print(f"[{timestamp}] ERROR: API connection failed. Exception: {e}")

if __name__ == "__main__":
    fetch_cushing_storage_v2()