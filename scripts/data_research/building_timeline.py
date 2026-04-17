"""
building_timeline.py — One Building's Full Story

Narrative: "This isn't a one-time problem. Look at the pattern."

Shows every complaint on record for a specific address: date, category, and
annual summary. Use this to spotlight a building in a council briefing, a
press pitch, or as evidence in Housing Court.

Usage:
    python building_timeline.py --number 341 --street "EAST 162 STREET" --cb 203
    python building_timeline.py --number 150 --street "LEFFERTS AVENUE" --cb 309
    python building_timeline.py --number 1016 --street "BRYANT AVENUE" --cb 202
    python building_timeline.py --bin 2034290

Address must use SODA format: uppercase, no house number in --street.
Community board: 3-digit code (borough digit + 2-digit CB, e.g. 203 = Bronx CB3).
"""

import argparse
import os
import sys
from collections import Counter
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
    "1": "Manhattan", "2": "Bronx", "3": "Brooklyn",
    "4": "Queens", "5": "Staten Island",
}

CATEGORY_LABELS = {
    "6S": "Elevator complaint",
    "6M": "Elevator/escalator complaint",
}


def fetch_by_address(house_number: str, house_street: str, cb: str) -> list[dict]:
    qs = (
        f"$where=house_number='{house_number}'"
        f" AND house_street='{house_street.upper()}'"
        f" AND community_board='{cb}'"
        f"&$order=date_entered DESC"
        f"&$limit=1000"
    )
    if APP_TOKEN:
        qs += f"&$$app_token={APP_TOKEN}"
    resp = requests.get(SODA_URL + "?" + qs, timeout=15)
    resp.raise_for_status()
    return resp.json()


def fetch_by_bin(bin_id: str) -> list[dict]:
    qs = (
        f"$where=bin='{bin_id}'"
        f"&$order=date_entered DESC"
        f"&$limit=1000"
    )
    if APP_TOKEN:
        qs += f"&$$app_token={APP_TOKEN}"
    resp = requests.get(SODA_URL + "?" + qs, timeout=15)
    resp.raise_for_status()
    return resp.json()


def parse_year(date_str: str) -> str:
    """Extract year from MM/DD/YYYY format."""
    parts = date_str.split("/")
    return parts[2] if len(parts) == 3 else "?"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--bin", help="Look up by BIN number")
    group.add_argument("--number", help="House number (e.g. 341)")
    parser.add_argument("--street", help='Street name in caps, no house number (e.g. "EAST 162 STREET")')
    parser.add_argument("--cb", help="Community board code (e.g. 203 = Bronx CB3)")
    args = parser.parse_args()

    if args.number and not (args.street and args.cb):
        parser.error("--number requires --street and --cb")

    if not APP_TOKEN:
        print("SODA_APP_TOKEN not set.")
        print("  export SODA_APP_TOKEN=<your_token>")
        sys.exit(1)

    try:
        if args.bin:
            records = fetch_by_bin(args.bin)
            lookup = f"BIN {args.bin}"
        else:
            records = fetch_by_address(args.number, args.street, args.cb)
            lookup = f"{args.number} {args.street.upper()}, CB{args.cb}"
    except requests.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Filter to elevator categories only for the timeline; show all for BIN lookup
    elevator_records = [r for r in records if r.get("complaint_category") in ("6S", "6M")]

    if not elevator_records:
        if records:
            print(f"\nFound {len(records)} total records for {lookup}, but none are elevator complaints (6S/6M).")
        else:
            print(f"\nNo records found for {lookup}.")
            print("Check that house number, street name, and community board are correct.")
        sys.exit(0)

    rec0 = elevator_records[0]
    resolved_addr = rec0.get("house_number", "") + " " + rec0.get("house_street", "")
    resolved_bin = rec0.get("bin", "Unknown")
    cb = rec0.get("community_board", "")
    borough = BOROUGH_FROM_CB.get(cb[0], "?") if cb else "?"

    print(f"\n{'='*62}")
    print(f"  {resolved_addr}, {borough}")
    print(f"  BIN: {resolved_bin}  |  Community Board: CB{cb}")
    print(f"  Elevator complaints (6S/6M) on record: {len(elevator_records)}")
    print(f"{'='*62}")

    # Annual summary
    by_year: Counter = Counter()
    for r in elevator_records:
        by_year[parse_year(r.get("date_entered", ""))] += 1

    print("\n  COMPLAINTS BY YEAR")
    print("  " + "-" * 40)
    for year in sorted(by_year.keys(), reverse=True):
        count = by_year[year]
        bar = "█" * count
        print(f"  {year}  {count:4d}  {bar}")

    # Full timeline
    display_count = min(len(elevator_records), 50)
    print(f"\n  COMPLAINT TIMELINE (most recent {display_count})")
    print("  " + "-" * 54)
    print(f"  {'Date':<14}  {'Code':<4}  {'Category':<32}  {'Status'}")
    print("  " + "-" * 54)
    for r in elevator_records[:50]:
        date = r.get("date_entered", "Unknown")
        code = r.get("complaint_category", "?")
        label = CATEGORY_LABELS.get(code, code)
        status = r.get("status", "")
        print(f"  {date:<14}  {code:<4}  {label:<32}  {status}")

    if len(elevator_records) > 50:
        print(f"  ... and {len(elevator_records) - 50} more")

    # Summary stats
    dates = sorted([r.get("date_entered", "") for r in elevator_records if r.get("date_entered")])
    if dates:
        print(f"\n  Earliest on record: {dates[0]}")
        print(f"  Most recent:        {dates[-1]}")
        recent_3yr = [r for r in elevator_records if parse_year(r.get("date_entered", "")) in ("2023", "2024", "2025")]
        print(f"  Last 3 years (2023–2025): {len(recent_3yr)} complaints")
    print()


if __name__ == "__main__":
    main()
