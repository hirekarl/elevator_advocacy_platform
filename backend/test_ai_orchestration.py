import os
import sys

import django
import pytest

# Set up Django environment
sys.path.append(os.path.join(os.getcwd(), "backend"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from buildings_app.logic import ConsensusManager
from buildings_app.models import Building
from orchestration.supervisor import Supervisor
from orchestration.workers.advocacy_strategist import AdvocacyStrategist
from orchestration.workers.community_reporter import CommunityReporter
from orchestration.workers.soda_researcher import SODAResearcher


def print_header(title: str):
    print(f"\n{'=' * 60}")
    print(f"🚀 {title}")
    print(f"{'=' * 60}")


@pytest.mark.django_db
def test_multi_agent_system():
    # 1. Setup Data
    bin_arg = None
    if len(sys.argv) > 1:
        bin_arg = sys.argv[1]

    if bin_arg:
        building = Building.objects.filter(bin=bin_arg).first()
        if not building:
            print(f"❌ Error: Building with BIN {bin_arg} not found.")
            return
    else:
        building = Building.objects.first()

    if not building:
        print(
            "❌ Error: No buildings found in database. Please run sync_soda_complaints first."
        )
        return

    manager = ConsensusManager()

    # Mocking context for the test
    context = {
        "bin": building.bin,
        "address": building.address,
        "verified_status": manager.get_verified_status(building),
        "loss_of_service": manager.get_loss_of_service_percentage(building),
        "lang": "en",
        "reports": [],
        "logs": [],
    }

    print_header(f"Testing AI Orchestration for: {building.address}")

    # 2. Test Individual Workers
    print("\n--- Phase 1: Worker Agent Verification ---")

    workers = [
        ("SODA Researcher", SODAResearcher()),
        ("Community Reporter", CommunityReporter()),
        ("Advocacy Strategist", AdvocacyStrategist()),
    ]

    for name, worker in workers:
        try:
            print(f"🔍 Executing {name}...")
            result = worker.analyze(context)
            if result:
                print(f"✅ {name} Success: {type(result).__name__} returned.")
                # Print specific details to debug
                if hasattr(result, "historical_summary"):
                    print(f"   - Historical Summary: {result.historical_summary}")
                if hasattr(result, "sentiment_summary"):
                    print(f"   - Sentiment Summary: {result.sentiment_summary}")
                if hasattr(result, "headline"):
                    print(f"   - Strategist Headline: {result.headline}")
            else:
                print(f"⚠️ {name} Warning: No result returned (Check GEMINI_API_KEY).")
        except Exception as e:
            print(f"❌ {name} Failed: {e}")

    # 3. Test Supervisor Synthesis
    print("\n--- Phase 2: Supervisor Synthesis (The Lead) ---")
    try:
        supervisor = Supervisor()
        print("🧠 Synthesizing full Executive Summary...")
        summary = supervisor.analyze(context)

        if summary:
            print("✅ Synthesis Complete!")
            print(f"\nHEADLINE: {summary.headline}")
            print(f"RISK LEVEL: {summary.risk_level}")
            print(f"CONFIDENCE: {summary.confidence_score}")
            print(f"RECOMMENDED ACTION: {summary.recommended_action}")
        else:
            print("❌ Supervisor failed to generate a summary.")
    except Exception as e:
        print(f"❌ Supervisor Error: {e}")

    # 4. API Endpoint Check (Optional/Local)
    print("\n--- Phase 3: System Integrity Check ---")
    from rest_framework.test import APIClient

    client = APIClient()
    url = f"/api/buildings/{building.bin}/advocacy_summary/"
    print(f"📡 Testing DRF Action: GET {url}")

    try:
        response = client.get(url)
        if response.status_code == 200:
            print("✅ API Endpoint functional!")
        elif response.status_code == 503:
            print(
                "⚠️ API Service Unavailable (LLM Provider likely down or keys missing)."
            )
        else:
            print(f"❌ API Error: Status {response.status_code}")
    except Exception as e:
        print(f"❌ API Request Failed: {e}")


if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("🛑 STOP: GEMINI_API_KEY is not set in your environment.")
        sys.exit(1)

    test_multi_agent_system()
    print("\n✨ Test script execution finished.")
