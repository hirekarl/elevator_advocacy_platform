import os
import django
from datetime import timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from buildings_app.models import Building, ElevatorReport
from buildings_app.ai_logic import PredictiveEngine
from django.contrib.auth.models import User

def test_predictive_engine():
    # 1. Setup a test building and user
    user, _ = User.objects.get_or_create(username="test_kiran")
    building, _ = Building.objects.get_or_create(
        bin="1234567",
        defaults={"address": "123 Test St", "borough": "MANHATTAN"}
    )

    # 2. Clear existing reports for clean test
    ElevatorReport.objects.filter(building=building).delete()

    # 3. Scenario A: Low Risk (No reports)
    risk_low = PredictiveEngine.calculate_failure_risk(building)
    print(f"Low Risk Scenario: {risk_low}")
    assert risk_low['risk_score'] == 0
    assert risk_low['confidence'] == 0

    # 4. Scenario B: High Risk (Recent failure spike)
    now = timezone.now()
    for i in range(5):
        ElevatorReport.objects.create(
            building=building,
            user=user,
            status='DOWN',
            reported_at=now - timedelta(days=i)
        )

    risk_high = PredictiveEngine.calculate_failure_risk(building)
    print(f"High Risk Scenario: {risk_high}")
    assert risk_high['risk_score'] > 50
    assert risk_high['confidence'] < 100 # Low volume overall

    # 5. Scenario C: Historical Consistency (High Confidence)
    for i in range(20):
        ElevatorReport.objects.create(
            building=building,
            user=user,
            status='DOWN',
            reported_at=now - timedelta(days=i*7) # Weekly historical failure
        )
    
    risk_conf = PredictiveEngine.calculate_failure_risk(building)
    print(f"High Confidence Scenario: {risk_conf}")
    assert risk_conf['confidence'] == 100

    print("\n✅ Predictive Engine verification successful!")

if __name__ == "__main__":
    test_predictive_engine()
