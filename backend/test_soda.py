import os
from pathlib import Path

import requests
from dotenv import load_dotenv


def run_soda_smoke_test():
    root_dir = Path(__file__).resolve().parent.parent
    load_dotenv(root_dir / ".env")
    token = os.getenv("SODA_APP_TOKEN")

    if not token:
        print("⏭️  Skipping SODA test: No SODA_APP_TOKEN found in environment.")
        return

    url = "https://data.cityofnewyork.us/resource/kqwi-7ncn.json"
    params = {"$limit": 5, "$$app_token": token}

    print(f"Testing SODA Token: {token[:4]}...{token[-4:]}")
    try:
        r = requests.get(url, params=params)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("✅ SODA SUCCESS!")
            print(f"Data: {len(r.json())} records received.")
        else:
            print(f"❌ SODA FAILED: {r.text}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_soda_smoke_test()
