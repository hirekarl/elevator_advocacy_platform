# Metrics: Loss of Service (LoS)

## Definition
The percentage of time an elevator was inoperative over a specific period (typically 30 days).

## Formula
**Loss of Service %** = `(Total Down Time / Total Period Time) * 100`

## Implementation Heuristic (Django 6.0)
Since reports are discrete events, the system assigns a fixed **120-minute (2-hour) duration** to each unique "DOWN" observation to calculate total downtime.

```python
def get_loss_of_service_percentage(building, days=30):
    now = timezone.now()
    start_date = now - timedelta(days=days)
    total_period_seconds = days * 24 * 60 * 60

    down_reports = ElevatorReport.objects.filter(
        building=building, status="DOWN", reported_at__gte=start_date
    )

    if not down_reports.exists(): return 0.0

    # Each unique report timestamp represents a 2-hour window
    unique_outages = down_reports.values("reported_at").distinct().count()
    total_down_seconds = unique_outages * (120 * 60)

    percentage = (total_down_seconds / total_period_seconds) * 100
    return round(min(percentage, 100.0), 2)
```

## AI Forecasting (Kiran)
- **Forecast vs. Actual:** AI predicts maintenance failures based on historical SODA data and compares them to real-time verification logs.
- **Metric Goal:** Identify buildings with >10% Loss of Service for targeted advocacy.
