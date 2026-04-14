"""
Generates and caches Executive Advocacy Summaries for all buildings.

Runs on every deploy via render_build.sh. Summaries are stored as JSON
on Building.cached_executive_summary, keyed by language code (e.g. "en", "es").
The advocacy_summary API endpoint serves directly from this cache — no live
Gemini calls happen in the request/response cycle.

Usage:
    uv run python manage.py generate_summaries
    uv run python manage.py generate_summaries --lang en
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from buildings_app.logic import ConsensusManager
from buildings_app.models import Building
from orchestration.supervisor import Supervisor

LANGUAGES = ["en", "es"]


class Command(BaseCommand):
    help = "Pre-generates and caches Executive Advocacy Summaries for all buildings."

    def add_arguments(self, parser):  # type: ignore[override]
        parser.add_argument(
            "--lang",
            type=str,
            default=None,
            help="Only generate for this language code (e.g. 'en'). Defaults to all languages.",
        )

    def handle(self, *args: object, **options: object) -> None:
        langs = [options["lang"]] if options["lang"] else LANGUAGES
        buildings = Building.objects.all()

        if not buildings.exists():
            self.stdout.write("No buildings in database — skipping summary generation.")
            return

        supervisor = Supervisor()
        manager = ConsensusManager()

        for building in buildings:
            self.stdout.write(
                f"  Generating summaries for {building.address} (BIN {building.bin})..."
            )
            cache = building.cached_executive_summary or {}

            reports = building.reports.order_by("-reported_at")[:20]
            logs = building.advocacy_logs.order_by("-created_at")[:20]

            for lang in langs:
                context = {
                    "bin": building.bin,
                    "address": building.address,
                    "verified_status": manager.get_verified_status(building),
                    "loss_of_service": manager.get_loss_of_service_percentage(building),
                    "lang": lang,
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
                        cache[lang] = summary.model_dump()
                        self.stdout.write(self.style.SUCCESS(f"    [{lang}] OK"))
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"    [{lang}] Supervisor returned no result — skipping."
                            )
                        )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"    [{lang}] Failed: {e}"))

            building.cached_executive_summary = cache
            building.summary_last_generated = timezone.now()
            building.save(
                update_fields=["cached_executive_summary", "summary_last_generated"]
            )

        self.stdout.write(self.style.SUCCESS("Summary generation complete."))
