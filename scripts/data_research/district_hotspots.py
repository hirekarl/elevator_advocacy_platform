"""
district_hotspots.py — Worst Buildings Per Priority District

Narrative: "Here are the buildings in your district that have failed their
tenants the most in the last 12 months."

Shows top buildings by complaint count for each of the six priority council
districts, filtered by community board.

Usage:
    python district_hotspots.py                      # all six priority districts
    python district_hotspots.py --district sanchez   # one councilmember
    python district_hotspots.py --years 2024 2025    # custom year range
    python district_hotspots.py --top 15             # more results per district
"""

import argparse
import os
import sys
from pathlib import Path

import requests

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass

SODA_URL = "https://data.cityofnewyork.us/resource/kqwi-7ncn.json"
APP_TOKEN = os.getenv("SODA_APP_TOKEN")

# Community boards covering each priority council district.
# Format: SODA community_board = borough_digit + two-digit CB number.
# CB boundaries don't perfectly match council district boundaries — assignments
# are inferred. Geocode individual addresses to confirm exact district.
PRIORITY_DISTRICTS = [
    {
        "key": "sanchez",
        "councilmember": "Justin Sanchez",
        "district": "D17",
        "borough": "Bronx",
        "community_boards": ["201", "202"],
        "neighborhoods": "Hunts Point, Port Morris, Mott Haven, Longwood",
    },
    {
        "key": "stevens",
        "councilmember": "Althea Stevens",
        "district": "D16",
        "borough": "Bronx",
        "community_boards": ["203"],
        "neighborhoods": "Morrisania, Crotona, Melrose",
    },
    {
        "key": "farias",
        "councilmember": "Amanda Farías",
        "district": "D18",
        "borough": "Bronx",
        "community_boards": ["209"],
        "neighborhoods": "Parkchester, Castle Hill, Soundview",
    },
    {
        "key": "banks",
        "councilmember": "Chris Banks",
        "district": "D42",
        "borough": "Brooklyn",
        "community_boards": ["316", "317"],
        "neighborhoods": "Brownsville, East New York",
    },
    {
        "key": "hudson",
        "councilmember": "Crystal Hudson",
        "district": "D35",
        "borough": "Brooklyn",
        "community_boards": ["308", "309"],
        "neighborhoods": "Crown Heights, Prospect Heights",
    },
    {
        "key": "delarosa",
        "councilmember": "Carmen De La Rosa",
        "district": "D10",
        "borough": "Manhattan",
        "community_boards": ["112"],
        "neighborhoods": "Washington Heights, Inwood",
    },
]


def build_year_filter(years: list[int]) -> str:
    clauses = [f"date_entered LIKE '%/{y}'" for y in years]
    return "(" + " OR ".join(clauses) + ")"


def fetch_top_buildings(community_boards: list[str], year_filter: str, top_n: int) -> list[dict]:
    cb_list = ", ".join(f"'{cb}'" for cb in community_boards)
    qs = (
        f"$select=house_number,house_street,community_board,count(*) AS complaint_count"
        f"&$where=complaint_category IN ('6S','6M')"
        f" AND community_board IN ({cb_list})"
        f" AND {year_filter}"
        f"&$group=house_number,house_street,community_board"
        f"&$order=complaint_count DESC"
        f"&$limit={top_n}"
    )
    if APP_TOKEN:
        qs += f"&$$app_token={APP_TOKEN}"
    resp = requests.get(SODA_URL + "?" + qs, timeout=15)
    resp.raise_for_status()
    return resp.json()


def print_district(district: dict, buildings: list[dict]) -> None:
    cm = district["councilmember"]
    d = district["district"]
    hood = district["neighborhoods"]
    print(f"\n  {cm} ({d}) — {hood}")
    print("  " + "-" * 56)
    if not buildings:
        print("  No complaints found in this area for this period.")
        return
    for i, b in enumerate(buildings, 1):
        addr = (b.get("house_number", "") + " " + b.get("house_street", ""))[:38]
        count = int(b.get("complaint_count", 0))
        bar = "█" * (count // 2)
        print(f"  {i:2d}. {addr:<38}  {count:4d}  {bar}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--district", choices=[d["key"] for d in PRIORITY_DISTRICTS],
                        help="Show only one district by councilmember key")
    parser.add_argument("--years", nargs="+", type=int, default=[2025, 2026],
                        help="Years to include (default: 2025 2026)")
    parser.add_argument("--top", type=int, default=10,
                        help="Results per district (default: 10)")
    args = parser.parse_args()

    if not APP_TOKEN:
        print("SODA_APP_TOKEN not set.")
        print("  export SODA_APP_TOKEN=<your_token>")
        sys.exit(1)

    year_filter = build_year_filter(args.years)
    year_label = " + ".join(str(y) for y in sorted(args.years))

    districts = PRIORITY_DISTRICTS
    if args.district:
        districts = [d for d in PRIORITY_DISTRICTS if d["key"] == args.district]

    print(f"\n{'='*60}")
    print("  ELEVATOR COMPLAINT HOTSPOTS — PRIORITY COUNCIL DISTRICTS")
    print(f"  Years: {year_label} | Codes: 6S, 6M")
    print(f"  ⚠  District assignments inferred from community board geography.")
    print(f"{'='*60}")

    for district in districts:
        try:
            buildings = fetch_top_buildings(
                district["community_boards"], year_filter, args.top
            )
        except requests.RequestException as e:
            print(f"\n  Error fetching {district['district']}: {e}", file=sys.stderr)
            continue
        print_district(district, buildings)

    print()


if __name__ == "__main__":
    main()
