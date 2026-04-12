import os
from datetime import timedelta
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Building, ElevatorReport
from services.geoclient import GeoclientService
from services.geoclient_mock import MockGeoclientService
from typing import Optional, List, Dict, Any

class ConsensusManager:
    """
    Logic engine for the 2-hour consensus window and data synchronization.
    """

    CONSENSUS_WINDOW_MINUTES = 120

    def __init__(self, geoclient: Optional[Any] = None):
        if geoclient:
            self.geoclient = geoclient
        elif os.getenv("USE_MOCK_GEOCLIENT", "False") == "True":
            self.geoclient = MockGeoclientService()
        else:
            self.geoclient = GeoclientService()

    def get_or_create_building(self, house_number: str, street: str, borough: str) -> Optional[Building]:
        """
        Backward compatibility for legacy calls.
        """
        building, _ = self.get_or_create_building_with_status(house_number, street, borough)
        return building

    def get_or_create_building_with_status(self, house_number: str, street: str, borough: str) -> tuple[Optional[Building], bool]:
        """
        Retrieves a building by BIN, creating it via Geoclient if it doesn't exist.
        Returns a tuple (Building, created).
        """
        geo_data = self.geoclient.get_bin_with_coordinates(house_number, street, borough)
        bin_id = geo_data.get('bin')
        
        if not bin_id:
            return None, False

        building, created = Building.objects.get_or_create(
            bin=bin_id,
            defaults={
                'address': f"{house_number} {street}",
                'borough': borough,
                'latitude': geo_data.get('latitude'),
                'longitude': geo_data.get('longitude')
            }
        )
        return building, created

    def report_status(self, building: Building, user: User, status: str) -> ElevatorReport:
        """
        Logs a new user report and triggers the consensus check.
        """
        return ElevatorReport.objects.create(
            building=building,
            user=user,
            status=status
        )

    def get_verified_status(self, building: Building) -> str:
        """
        Determines the current consensus status for a building's elevators.
        Status is 'Verified' if:
        1. 2+ independent users report the same status within 2 hours.
        2. Any official SODA report is logged within the window.
        """
        window_start = timezone.now() - timedelta(minutes=self.CONSENSUS_WINDOW_MINUTES)
        
        # Check for official reports first
        official_report = ElevatorReport.objects.filter(
            building=building,
            is_official=True,
            reported_at__gte=window_start
        ).last()
        
        if official_report:
            return official_report.status

        # Aggregate user reports within the window
        reports = ElevatorReport.objects.filter(
            building=building,
            is_official=False,
            reported_at__gte=window_start
        ).values('status').annotate(
            unique_users=Count('user_id', distinct=True),
            last_reported=Count('reported_at')
        ).order_by('-last_reported')

        for report in reports:
            if report['unique_users'] >= 2:
                return report['status']

        return "UNVERIFIED"

    def get_loss_of_service_percentage(self, building: Building, days: int = 30) -> float:
        """
        Calculates the Loss of Service % = (Total Down Time / Total Period Time) * 100.
        Uses a rolling window of N days.
        """
        now = timezone.now()
        start_date = now - timedelta(days=days)
        total_period_seconds = days * 24 * 60 * 60

        down_reports = ElevatorReport.objects.filter(
            building=building,
            status='DOWN',
            reported_at__gte=start_date
        )

        if not down_reports.exists():
            return 0.0

        unique_outages = down_reports.values('reported_at').distinct().count()
        total_down_seconds = unique_outages * (self.CONSENSUS_WINDOW_MINUTES * 60)
        
        percentage = (total_down_seconds / total_period_seconds) * 100
        return round(min(percentage, 100.0), 2)

    def sync_soda_reports(self, building: Building, soda_reports: List[Dict[str, Any]]):
        """
        Synchronizes official SODA reports into our local database.
        """
        for report in soda_reports:
            status = 'DOWN'
            unique_key = report.get('unique_key')
            
            ElevatorReport.objects.get_or_create(
                soda_unique_key=unique_key,
                defaults={
                    'building': building,
                    'user': None,
                    'status': status,
                    'is_official': True,
                    'reported_at': report.get('created_date', timezone.now())
                }
            )
