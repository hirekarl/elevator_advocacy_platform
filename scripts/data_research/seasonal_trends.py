"""
seasonal_trends.py — The Summer Spike

Narrative: "NYC elevator complaints spike 33% in July. Summer is the worst
time to be in a building with a history of failures."

Shows monthly complaint counts by year and each month's deviation from the
annual average. The July premium is consistent across every year since 2018.

Usage:
    python seasonal_trends.py
    python seasonal_trends.py --year 2024
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

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# date_entered is MM/DD/YYYY text — use LIKE month patterns
MONTH_PREFIXES = ["01/", "02/", "03/", "04/", "05/", "06/",
                  "07/", "08/", "09/", "10/", "11/", "12/"]


def fetch_month_count(month_prefix: str, year: int) -> int:
    """Fetch complaint count for one month via LIKE pattern."""
    qs = (
        f"$select=count(*) AS cnt"
        f"&$where=complaint_category IN ('6S','6M')"
        f" AND date_entered LIKE '{month_prefix}%/{year}'"
    )
    if APP_TOKEN:
        qs += f"&$$app_token={APP_TOKEN}"
    resp = requests.get(SODA_URL + "?" + qs, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return int(data[0].get("cnt", 0)) if data else 0


def print_year(year: int, monthly: dict[int, int]) -> None:
    total = sum(monthly.values())
    avg = total / 12 if total else 0
    print(f"\n  {year}  (annual avg: {avg:.0f}/month, total: {total:,})")
    print("  " + "-" * 58)
    for m in range(1, 13):
        count = monthly.get(m, 0)
        delta = ((count - avg) / avg * 100) if avg else 0
        bar = "█" * (count // 20)
        marker = f"{'▲' if delta > 5 else ('▼' if delta < -5 else ' ')}{abs(delta):4.0f}%"
        print(f"  {MONTHS[m-1]:3s}  {count:5d}  {marker}  {bar}")


def print_averages(data: dict[int, dict[int, int]]) -> None:
    monthly_totals: dict[int, list[int]] = {m: [] for m in range(1, 13)}
    for yearly in data.values():
        for m, count in yearly.items():
            if count > 0:
                monthly_totals[m].append(count)

    avgs = {m: sum(v) / len(v) for m, v in monthly_totals.items() if v}
    overall_avg = sum(avgs.values()) / len(avgs) if avgs else 0

    print("\n  AVERAGE BY MONTH (all years in range)")
    print("  " + "-" * 58)
    for m in range(1, 13):
        avg = avgs.get(m, 0)
        delta = ((avg - overall_avg) / overall_avg * 100) if overall_avg else 0
        bar = "█" * int(avg // 20)
        marker = f"{'▲' if delta > 5 else ('▼' if delta < -5 else ' ')}{abs(delta):4.0f}%"
        print(f"  {MONTHS[m-1]:3s}  {avg:6.0f}  {marker}  {bar}")
    print(f"\n  Overall monthly average: {overall_avg:.0f} complaints")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, help="Show a single year only")
    args = parser.parse_args()

    if not APP_TOKEN:
        print("Warning: SODA_APP_TOKEN not set — set it in your shell or .env file.")
        print("  export SODA_APP_TOKEN=<your_token>")
        sys.exit(1)

    years = [args.year] if args.year else list(range(2018, 2026))

    print(f"\n{'='*62}")
    print("  NYC ELEVATOR COMPLAINTS — MONTHLY BREAKDOWN")
    print(f"  Dataset: kqwi-7ncn | Codes: 6S, 6M | Source: NYC Open Data")
    print(f"{'='*62}")
    print(f"  Fetching {len(years) * 12} monthly counts — one moment...")

    all_data: dict[int, dict[int, int]] = {}

    for year in years:
        sys.stdout.write(f"  {year}: ")
        sys.stdout.flush()
        monthly: dict[int, int] = {}
        for m_idx, prefix in enumerate(MONTH_PREFIXES, 1):
            try:
                count = fetch_month_count(prefix, year)
                monthly[m_idx] = count
                sys.stdout.write(".")
                sys.stdout.flush()
            except requests.RequestException as e:
                print(f"\n  Error fetching {MONTHS[m_idx-1]} {year}: {e}")
                monthly[m_idx] = 0
        print()
        all_data[year] = monthly

    for year in years:
        print_year(year, all_data[year])

    if not args.year and len(years) > 1:
        print_averages(all_data)

    print()


if __name__ == "__main__":
    main()
