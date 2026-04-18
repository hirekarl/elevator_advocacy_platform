"""
Backfills city_council_district for any building that was geocoded before
the district spatial lookup was added to GeoSearchService.

Uses a point-in-polygon query against the NYC Open Data council districts
dataset (872g-cjhh) from the building's stored lat/lon. No API key required.

Safe to run repeatedly — only touches buildings with a null city_council_district.
Runs on every deploy via render_build.sh after migrations.

Usage:
    uv run python manage.py backfill_council_districts
"""

from django.core.management.base import BaseCommand

from buildings_app.models import Building
from services.geosearch import district_from_coordinates


class Command(BaseCommand):
    help = "Backfills council district data for buildings missing it."

    def handle(self, *args: object, **options: object) -> None:
        buildings = Building.objects.filter(city_council_district__isnull=True)

        if not buildings.exists():
            self.stdout.write(
                "All buildings already have district data — nothing to do."
            )
            return

        for building in buildings:
            self.stdout.write(
                f"  Backfilling {building.address} (BIN {building.bin})..."
            )

            if not building.latitude or not building.longitude:
                self.stdout.write(
                    self.style.WARNING("    No coordinates on record — skipping.")
                )
                continue

            district = district_from_coordinates(
                float(building.latitude), float(building.longitude)
            )

            if district:
                building.city_council_district = district
                building.save(update_fields=["city_council_district"])
                self.stdout.write(
                    self.style.SUCCESS(f"    District {district} — saved.")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "    Spatial query returned no result — skipping."
                    )
                )

        self.stdout.write(self.style.SUCCESS("District backfill complete."))
