"""
Backfills city_council_district (and state district fields) for any building
that was created via the GeoSearch fallback, which does not return district data.

Strategy:
  1. Try Geoclient (returns all three district fields).
  2. If Geoclient is unavailable or returns no district, fall back to a
     point-in-polygon query against the NYC Open Data council districts
     dataset (872g-cjhh) using the building's existing lat/lon. This path
     requires no API key and populates city_council_district only.

Safe to run repeatedly — only touches buildings with a null city_council_district.
Runs on every deploy via render_build.sh after migrations.

Usage:
    uv run python manage.py backfill_council_districts
"""

import requests
from django.core.management.base import BaseCommand

from buildings_app.models import Building
from services.geoclient import GeoclientService

COUNCIL_DISTRICTS_URL = "https://data.cityofnewyork.us/resource/872g-cjhh.json"


def _district_from_coordinates(lat: float, lon: float) -> str | None:
    """
    Returns the council district number for a lat/lon point using a
    NYC Open Data spatial query. No API key required.
    """
    try:
        params: dict[str, str] = {
            "$where": f"intersects(the_geom, 'POINT ({lon} {lat})')",
            "$select": "coundist",
            "$limit": "1",
        }
        response = requests.get(
            COUNCIL_DISTRICTS_URL,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        results = response.json()
        if results:
            return str(results[0].get("coundist"))
    except Exception:
        pass
    return None


class Command(BaseCommand):
    help = "Backfills council district data for buildings missing it."

    def handle(self, *args: object, **options: object) -> None:
        buildings = Building.objects.filter(city_council_district__isnull=True)

        if not buildings.exists():
            self.stdout.write(
                "All buildings already have district data — nothing to do."
            )
            return

        geoclient = GeoclientService()

        for building in buildings:
            self.stdout.write(
                f"  Backfilling {building.address} (BIN {building.bin})..."
            )

            district = None

            # --- Path 1: Geoclient (full district data) ---
            parts = building.address.split(" ", 1)
            if len(parts) == 2:
                house_number, street = parts
                try:
                    geo_data = geoclient.get_bin_with_coordinates(
                        house_number, street, building.borough
                    )
                    if geo_data.get("city_council_district"):
                        building.city_council_district = geo_data[
                            "city_council_district"
                        ]
                        building.state_assembly_district = geo_data.get(
                            "state_assembly_district"
                        )
                        building.state_senate_district = geo_data.get(
                            "state_senate_district"
                        )
                        building.save(
                            update_fields=[
                                "city_council_district",
                                "state_assembly_district",
                                "state_senate_district",
                            ]
                        )
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"    District {geo_data['city_council_district']} via Geoclient — saved."
                            )
                        )
                        continue
                except Exception as e:
                    self.stdout.write(
                        f"    Geoclient error: {e} — trying coordinates fallback."
                    )

            # --- Path 2: NYC Open Data spatial query (coordinates fallback) ---
            if building.latitude and building.longitude:
                district = _district_from_coordinates(
                    float(building.latitude), float(building.longitude)
                )
                if district:
                    building.city_council_district = district
                    building.save(update_fields=["city_council_district"])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"    District {district} via coordinates fallback — saved."
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            "    Coordinates fallback returned no result — skipping."
                        )
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "    No coordinates on record and Geoclient unavailable — skipping."
                    )
                )

        self.stdout.write(self.style.SUCCESS("District backfill complete."))
