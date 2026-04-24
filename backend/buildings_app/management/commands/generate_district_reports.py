"""
Automates the full advocacy pipeline for a specific NYC Council District.
1. Syncs all-time historical SODA reports for the district.
2. Generates/Updates AI advocacy summaries for all buildings in the district.
3. Outputs a district-level health summary.

Usage:
    uv run python manage.py generate_district_reports --district 17
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from buildings_app.logic import ConsensusManager
from buildings_app.models import Building, CouncilDistrict
from orchestration.supervisor import Supervisor
from services.soda import SODAService


class Command(BaseCommand):
    help = "Generates a full advocacy report package for a council district."

    def add_arguments(self, parser):
        parser.add_argument(
            "--district", type=str, required=True, help="Council District ID (e.g. 17)."
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerate all summaries even if they exist.",
        )

    def handle(self, *args, **options):
        district_id = options["district"]
        force = options["force"]

        try:
            district = CouncilDistrict.objects.get(district_id=district_id)
        except CouncilDistrict.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"District {district_id} not found in database.")
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"🚀 Starting advocacy report generation for District {district_id} ({district.member_name})..."
            )
        )

        # 1. Historical SODA Sync
        self.stdout.write("--- Step 1: Syncing Historical SODA Data (All-Time) ---")
        soda = SODAService()
        reports = soda.get_recent_outages(hours=0, district_id=district_id)

        if reports:
            manager = ConsensusManager()
            synced_count = manager.sync_citywide_soda_reports(
                reports, target_district=district_id
            )
            self.stdout.write(
                self.style.SUCCESS(f"✅ Synced {synced_count} new historical reports.")
            )
        else:
            self.stdout.write("No reports found for this district.")

        # 2. Summary Generation
        self.stdout.write("--- Step 2: Generating AI Advocacy Summaries ---")
        buildings = Building.objects.filter(city_council_district=district_id)

        if not buildings.exists():
            self.stdout.write(
                self.style.WARNING(
                    "No buildings found for this district in the database."
                )
            )
            return

        supervisor = Supervisor()
        manager = ConsensusManager()

        skipped_nominal = 0
        for building in buildings:
            # Dual-window filter: only generate summaries for chronic offenders.
            # 1+ complaints in last 12 months AND 3+ in last 3 years.
            counts = manager.get_chronic_offender_data(building)
            if counts is None:
                skipped_nominal += 1
                if building.cached_executive_summary and not force:
                    continue
                # Write a programmatic nominal summary without calling Gemini.
                from orchestration.schemas import ExecutiveSummary

                nominal = ExecutiveSummary(
                    headline="No recent complaint activity recorded.",
                    risk_level="Nominal",
                    historical_patterns="No elevator issues detected in the current analysis window.",
                    community_sentiment="No tenant reports on record for the current period.",
                    legal_standing="No active violations or complaints requiring intervention.",
                    recommended_action="No action required. Residents may submit reports through the platform if issues arise.",
                    confidence_score=1.0,
                )
                building.cached_executive_summary = {"en": nominal.model_dump()}
                building.summary_last_generated = timezone.now()
                building.save(
                    update_fields=["cached_executive_summary", "summary_last_generated"]
                )
                continue

            if building.cached_executive_summary and not force:
                self.stdout.write(
                    f"  Skipping {building.address} (Summary already exists)."
                )
                continue

            self.stdout.write(f"  Generating summary for {building.address}...")

            # Context for Gemini
            reports = building.reports.order_by("-reported_at")[:20]
            logs = building.advocacy_logs.order_by("-created_at")[:20]

            context = {
                "bin": building.bin,
                "address": building.address,
                "verified_status": manager.get_verified_status(building),
                "loss_of_service": manager.get_loss_of_service_percentage(building),
                "complaints_12mo": counts["complaints_12mo"],
                "complaints_3yr": counts["complaints_3yr"],
                "lang": "en",
                "reports": [
                    {"status": r.status, "reported_at": str(r.reported_at)}
                    for r in reports
                ],
                "logs": [
                    {
                        "description": log.description,
                        "sr_number": log.sr_number,
                        "created_at": str(log.created_at),
                    }
                    for log in logs
                ],
            }

            try:
                summary = supervisor.analyze(context)
                if summary:
                    building.cached_executive_summary = {"en": summary.model_dump()}
                    building.summary_last_generated = timezone.now()
                    building.save(
                        update_fields=[
                            "cached_executive_summary",
                            "summary_last_generated",
                        ]
                    )
                    self.stdout.write(self.style.SUCCESS("    OK"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"    Failed: {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"--- Phase 2 Complete: District {district_id} is ready for advocacy. "
                f"({skipped_nominal} buildings assigned nominal status without Gemini.) ---"
            )
        )
