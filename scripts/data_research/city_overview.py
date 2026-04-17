"""
city_overview.py — The Scale of the Problem

Narrative: "This isn't a District 17 problem. It's a city-wide failure of
accountability — and the data proves it."

Shows the top buildings city-wide, a borough-level breakdown, and headline
stats. Use this for Pursuit demos, press pitches, or any audience that needs
to understand the full scope before you narrow to a specific district.

Usage:
    python city_overview.py                  # last 12 months (2025-2026)
    python city_overview.py --years 2024     # single year
    python city_overview.py --years 2023 2024 2025   # multi-year
    python city_overview.py --top 50         # expand the leaderboard
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

BOROUGH_FROM_CB = {
    "1": "Manhattan",
    "2": "Bronx",
    "3": "Brooklyn",
    "4": "Queens",
    "5": "Staten Island",
}


def build_year_filter(years: list[int]) -> str:
    clauses = [f"date_entered LIKE '%/{y}'" for y in years]
    return "(" + " OR ".join(clauses) + ")"


def fetch_top_buildings(year_filter: str, top_n: int) -> list[dict]:
    qs = (
        f"$select=house_number,house_street,community_board,count(*) AS complaint_count"
        f"&$where=complaint_category IN ('6S','6M') AND {year_filter}"
        f"&$group=house_number,house_street,community_board"
        f"&$order=complaint_count DESC"
        f"&$limit={top_n}"
    )
    if APP_TOKEN:
        qs += f"&$$app_token={APP_TOKEN}"
    resp = requests.get(SODA_URL + "?" + qs, timeout=20)
    resp.raise_for_status()
    return resp.json()


def fetch_borough_totals(year_filter: str) -> dict[str, int]:
    qs = (
        f"$select=community_board,count(*) AS cnt"
        f"&$where=complaint_category IN ('6S','6M') AND {year_filter}"
        f"&$group=community_board"
        f"&$order=cnt DESC"
        f"&$limit=500"
    )
    if APP_TOKEN:
        qs += f"&$$app_token={APP_TOKEN}"
    resp = requests.get(SODA_URL + "?" + qs, timeout=20)
    resp.raise_for_status()

    totals: dict[str, int] = {}
    for rec in resp.json():
        cb = rec.get("community_board", "")
        borough = BOROUGH_FROM_CB.get(cb[0], "Unknown") if cb else "Unknown"
        totals[borough] = totals.get(borough, 0) + int(rec.get("cnt", 0))
    return totals


def fetch_total(year_filter: str) -> int:
    qs = (
        f"$select=count(*) AS total"
        f"&$where=complaint_category IN ('6S','6M') AND {year_filter}"
    )
    if APP_TOKEN:
        qs += f"&$$app_token={APP_TOKEN}"
    resp = requests.get(SODA_URL + "?" + qs, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return int(data[0].get("total", 0)) if data else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--years", nargs="+", type=int, default=[2025, 2026],
                        help="Years to include (default: 2025 2026)")
    parser.add_argument("--top", type=int, default=25,
                        help="Number of top buildings to show (default: 25)")
    args = parser.parse_args()

    if not APP_TOKEN:
        print("Warning: SODA_APP_TOKEN not set.")
        print("  export SODA_APP_TOKEN=<your_token>")
        sys.exit(1)

    year_filter = build_year_filter(args.years)
    year_label = " + ".join(str(y) for y in sorted(args.years))

    print(f"\nFetching city-wide data for {year_label}...")

    try:
        total = fetch_total(year_filter)
        borough_totals = fetch_borough_totals(year_filter)
        top_buildings = fetch_top_buildings(year_filter, args.top)
    except requests.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\n{'='*64}")
    print("  NYC ELEVATOR COMPLAINTS — CITY-WIDE OVERVIEW")
    print(f"  Years: {year_label} | Codes: 6S, 6M | Source: NYC Open Data")
    print(f"{'='*64}")

    print(f"\n  Total complaints in period: {total:,}")

    print(f"\n  COMPLAINTS BY BOROUGH")
    print("  " + "-" * 46)
    max_b = max(borough_totals.values(), default=1)
    for borough in ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]:
        count = borough_totals.get(borough, 0)
        pct = (count / total * 100) if total else 0
        bar = "█" * (count * 28 // max_b)
        print(f"  {borough:<16}  {count:6,}  ({pct:4.1f}%)  {bar}")

    print(f"\n  TOP {args.top} BUILDINGS CITY-WIDE")
    print("  " + "-" * 62)
    print(f"  {'Rank':<5}  {'Address':<38}  {'Borough':<11}  {'CB':<5}  {'#':>4}")
    print("  " + "-" * 62)
    for i, b in enumerate(top_buildings, 1):
        cb = b.get("community_board", "")
        borough = BOROUGH_FROM_CB.get(cb[0], "?")[:10] if cb else "?"
        addr = (b.get("house_number", "") + " " + b.get("house_street", ""))[:37]
        count = b.get("complaint_count", "0")
        print(f"  {i:<5}  {addr:<38}  {borough:<11}  {cb:<5}  {count:>4}")

    if top_buildings:
        top = top_buildings[0]
        top_addr = top.get("house_number", "") + " " + top.get("house_street", "")
        top_cb = top.get("community_board", "")
        top_borough = BOROUGH_FROM_CB.get(top_cb[0], "?") if top_cb else "?"
        print(f"\n  Most-complained building: {top_addr}, {top_borough}")
        print(f"  {top.get('complaint_count')} complaints in this period.")

    print(f"\n  Community board format: first digit = borough")
    print(f"  (1=Manhattan 2=Bronx 3=Brooklyn 4=Queens 5=Staten Island)")
    print()


if __name__ == "__main__":
    main()
