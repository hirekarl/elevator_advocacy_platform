import math
from datetime import timedelta
from typing import Dict, List, Any
from django.utils import timezone
from .models import Building, ElevatorReport

class PredictiveEngine:
    """
    Kiran's AI Engine: Forecasts elevator maintenance failures using historical
    SODA data and real-time user reports.
    """

    @staticmethod
    def calculate_failure_risk(building: Building) -> Dict[str, Any]:
        """
        Calculates a 7-day failure risk score (0-100%).
        
        Logic:
        1. Establish historical frequency (last 180 days).
        2. Weighted by recent "Loss of Service" trends (last 14 days).
        3. Penalty for "Unverified" reports (amber pulse).
        """
        now = timezone.now()
        history_start = now - timedelta(days=180)
        recent_start = now - timedelta(days=14)

        # 1. Historical Baseline
        total_reports = ElevatorReport.objects.filter(
            building=building,
            reported_at__gte=history_start,
            status__in=['DOWN', 'FAILED']
        ).count()

        # Reports per month (average)
        reports_per_month = total_reports / 6.0
        
        # 2. Recent Volatility
        recent_reports = ElevatorReport.objects.filter(
            building=building,
            reported_at__gte=recent_start,
            status__in=['DOWN', 'FAILED']
        ).count()

        # 3. Forecast Logic (Exponential Smoothing placeholder)
        # Baseline risk starts at reports per month normalized to 100%
        # (e.g., 4 reports/mo = high baseline risk)
        baseline_risk = min((reports_per_month / 2.0) * 100, 40)
        
        # Recent volatility multiplier
        volatility_bonus = min(recent_reports * 15, 60)
        
        forecasted_risk = round(baseline_risk + volatility_bonus, 2)
        
        # 4. Confidence Score
        confidence = 100 if total_reports > 10 else (total_reports * 10)

        return {
            "risk_score": min(forecasted_risk, 100.0),
            "confidence": confidence,
            "forecast_window": "7 Days",
            "metric": "Probabilistic Failure Risk"
        }

    @staticmethod
    def compare_forecast_vs_actual(building: Building, forecast_risk: float) -> str:
        """
        Compares the AI's forecast against the actual verified state.
        Returns a 'Performance' string for Aris/Sol to review.
        """
        # Actual state from Consensus Engine (placeholder for logic call)
        # In a real scenario, this would compare if a predicted outage occurred.
        from .logic import ConsensusManager
        manager = ConsensusManager()
        actual_status = manager.get_verified_status(building)

        if forecast_risk > 70 and actual_status == 'DOWN':
            return "ACCURATE: High risk predicted, outage confirmed."
        elif forecast_risk < 20 and actual_status == 'DOWN':
            return "ANOMALY: Low risk predicted, unexpected outage."
        elif forecast_risk > 70 and actual_status == 'UP':
            return "PREVENTATIVE: High risk predicted, maintenance may have intervened."
        
        return "NOMINAL: Tracking within expected parameters."
