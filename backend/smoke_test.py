import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Set up Django environment
sys.path.append(str(Path(__file__).resolve().parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from buildings_app.logic import ConsensusManager
from services.soda import SODAService


def run_smoke_test():
    # Load .env from project root
    root_dir = Path(__file__).resolve().parent.parent
    load_dotenv(root_dir / ".env")

    # Check for Mock Mode
    mock_mode = os.getenv("USE_MOCK_GEOCODER", "False") == "True"
    print(f"--- 🚀 Initializing Smoke Test (Mock Mode: {mock_mode}) ---")

    manager = ConsensusManager()
    soda = SODAService()

    # 1. Test GeoSearch (120 Broadway, Manhattan)
    print("\n1. Testing GeoSearch (Address -> BIN)...")
    building = manager.get_or_create_building("120", "Broadway", "Manhattan")

    if building:
        print(f"✅ Success! Building for 120 Broadway: {building.bin}")
        bin_id = building.bin
    else:
        print(
            "❌ GeoSearch Failed. Check network connectivity or set USE_MOCK_GEOCODER=True in .env"
        )
        return

    # 2. Test SODA (Check for complaints at this BIN)
    print("\n2. Testing SODA (Elevator Complaints)...")
    complaints = soda.get_elevator_complaints(bin_id)

    print(
        f"✅ Success! Found {len(complaints)} elevator-related records for this building."
    )
    if complaints:
        print(
            f"   Latest Complaint: {complaints[0].get('created_date')} - {complaints[0].get('descriptor')}"
        )

    print("\n--- ✨ Smoke Test Complete: System is Wired! ---")


if __name__ == "__main__":
    run_smoke_test()
