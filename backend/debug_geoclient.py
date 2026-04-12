import os
import requests
from pathlib import Path
from dotenv import load_dotenv

def debug_geoclient():
    root_dir = Path(__file__).resolve().parent.parent
    load_dotenv(root_dir / ".env")
    key = os.getenv("NYC_API_KEY")
    
    url = "https://api.nyc.gov/geo/geoclient/v2/address.json"
    params = {"houseNumber": "120", "street": "Broadway", "borough": "Manhattan"}
    
    print(f"Testing key: {key[:4]}...{key[-4:]}")
    
    # 1. Standard Azure Header
    print("\nAttempt 1: Header 'Ocp-Apim-Subscription-Key'")
    try:
        r = requests.get(url, params=params, headers={"Ocp-Apim-Subscription-Key": key})
        print(f"Status: {r.status_code}")
        if r.status_code == 200: print("✅ SUCCESS!")
    except Exception as e: print(f"Error: {e}")

    # 2. Lowercase Azure Header
    print("\nAttempt 2: Header 'ocp-apim-subscription-key'")
    try:
        r = requests.get(url, params=params, headers={"ocp-apim-subscription-key": key})
        print(f"Status: {r.status_code}")
        if r.status_code == 200: print("✅ SUCCESS!")
    except Exception as e: print(f"Error: {e}")

    # 3. Query Param 'subscription-key'
    print("\nAttempt 3: Query Param 'subscription-key'")
    p_with_key = params.copy()
    p_with_key["subscription-key"] = key
    try:
        r = requests.get(url, params=p_with_key)
        print(f"Status: {r.status_code}")
        if r.status_code == 200: print("✅ SUCCESS!")
    except Exception as e: print(f"Error: {e}")

    # 4. Header 'X-API-Key'
    print("\nAttempt 4: Header 'X-API-Key'")
    try:
        r = requests.get(url, params=params, headers={"X-API-Key": key})
        print(f"Status: {r.status_code}")
        if r.status_code == 200: print("✅ SUCCESS!")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    debug_geoclient()
