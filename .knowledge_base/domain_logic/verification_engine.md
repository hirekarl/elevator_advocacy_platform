# Verification Engine (Consensus Model)

## Core Rule
Status updates (UP/DOWN) remain **unverified** until:
1.  A second observation is logged by a **different** `user_id` for the same `elevator_id` within a rolling **2-hour window**.
2.  **OR** an official SODA report (`is_official=True`) is logged within the same window.

## Implementation Logic
- **Official Bypass:** SODA reports from NYC Open Data are considered pre-verified and immediately update the canonical status.
- **Unverified State:** Displayed with pulse amber icons in the UI.
- **Verification Countdown:** A timer showing the remaining time in the 2-hour window before the observation expires.
- **Transition to Verified:** Once a second unique user logs a matching status within the window, the status becomes **canonical**.
- **Expiration:** If no verification occurs within 2 hours, the unverified log is archived or ignored for canonical status calculations.

## Database Pattern (Django)
```python
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

def get_verified_status(building):
    window_start = timezone.now() - timedelta(hours=2)

    # 1. Check for official reports (SODA)
    official = ElevatorReport.objects.filter(
        building=building, is_official=True, reported_at__gte=window_start
    ).last()
    if official: return official.status

    # 2. Check for 2+ unique user reports
    reports = ElevatorReport.objects.filter(
        building=building, is_official=False, reported_at__gte=window_start
    ).values("status").annotate(
        unique_users=Count("user_id", distinct=True)
    )

    for r in reports:
        if r["unique_users"] >= 2: return r["status"]

    return "UNVERIFIED"
```
