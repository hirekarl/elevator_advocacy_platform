import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta
from typing import Any, Dict, List, Optional

import requests
from django.core.cache import cache
from django.utils import timezone


class SODAService:
    """
    Service wrapper for the NYC SODA API (Dataset kqwi-7ncn).
    Fetches elevator-specific complaints.
    """

    BASE_URL = "https://data.cityofnewyork.us/resource/kqwi-7ncn.json"

    def __init__(self, app_token: Optional[str] = None):
        self.app_token = app_token or os.getenv("SODA_APP_TOKEN")

    def get_elevator_complaints(
        self, bin: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Fetches complaints for a specific BIN, filtered by elevator-related categories.
        """
        # Active category codes as of 2018: '6S' (elevator complaints) and '6M' (elevator/escalator).  # noqa: E501
        # Codes '81' (retired 2007) and '63' (retired 2016) must not be used for current data.  # noqa: E501
        where_clause = f"bin='{bin}' AND complaint_category IN ('6S', '6M')"

        params: Dict[str, Any] = {
            "$where": where_clause,
            "$limit": limit,
            "$$app_token": self.app_token,
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
            return []
        except requests.RequestException as e:
            print(f"SODA Error: {e}")
            return []

    def get_recent_outages(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Fetches all elevator-related outages across NYC from the last N hours.
        If hours=0, fetches the absolute most recent N outages regardless of time.
        """
        # SODA floating timestamp format: YYYY-MM-DDTHH:MM:SS
        if hours > 0:
            limit_date = (timezone.now() - timedelta(hours=hours)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
            where_clause = (
                f"complaint_category IN ('6S', '6M') AND date_entered > '{limit_date}'"
            )
            params: Dict[str, Any] = {
                "$where": where_clause,
                "$$app_token": self.app_token,
            }
        else:
            where_clause = "complaint_category IN ('6S', '6M')"
            params = {
                "$where": where_clause,
                "$order": "date_entered DESC",
                "$limit": 1000,
                "$$app_token": self.app_token,
            }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
            return []
        except requests.RequestException as e:
            print(f"SODA Sync Error: {e}")
            return []

    def get_city_stats(self) -> Dict[str, Any]:
        """
        Returns aggregated city-wide elevator complaint statistics from SODA.

        Makes three parallel queries:
          - Borough breakdown for the last 12 months (count + percentage of total)
          - Top 15 buildings by complaint volume in the last 12 months
          - Monthly complaint counts for the current calendar year (all 12 months)

        Returns:
            A dict with the following shape::

                {
                    "total_complaints_12mo": int,
                    "borough_breakdown": [
                        {"name": str, "count": int, "pct": float}, ...
                    ],   # sorted by count descending
                    "top_buildings": [
                        {"address": str, "borough": str, "count": int}, ...
                    ],   # up to 15 entries
                    "monthly_current_year": [
                        {"month": str, "count": int}, ...
                    ],   # exactly 12 entries, Jan–Dec
                }

            On any SODA error the affected list is empty and total_complaints_12mo
            is 0 — the caller receives a partial (gracefully degraded) response
            rather than a 500.
        """
        CACHE_KEY = "city_stats_v1"
        CACHE_TTL = 60 * 60 * 6  # 6 hours

        cached: Optional[Dict[str, Any]] = cache.get(CACHE_KEY)
        if cached is not None:
            return cached

        BOROUGH_MAP: Dict[str, str] = {
            "1": "Manhattan",
            "2": "Bronx",
            "3": "Brooklyn",
            "4": "Queens",
            "5": "Staten Island",
        }
        MONTH_NAMES: List[str] = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]

        now = timezone.now()
        current_year = now.year
        prev_year = current_year - 1

        category_filter = "complaint_category IN ('6S','6M')"
        # date_entered is stored as MM/DD/YYYY text in this SODA dataset.
        # ISO datetime comparisons return 0 results; LIKE year-suffix patterns work.
        two_year_filter = (
            f"(date_entered LIKE '%/{current_year}'"
            f" OR date_entered LIKE '%/{prev_year}')"
        )

        def _query_borough_breakdown() -> List[Dict[str, Any]]:
            params: Dict[str, Any] = {
                "$select": "community_board, count(*) AS cnt",
                "$where": f"{category_filter} AND {two_year_filter}",
                "$group": "community_board",
                "$limit": 500,
                "$$app_token": self.app_token,
            }
            resp = requests.get(self.BASE_URL, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, list) else []

        def _query_top_buildings() -> List[Dict[str, Any]]:
            params: Dict[str, Any] = {
                "$select": (
                    "house_number, house_street, community_board, bin,"
                    " count(*) AS complaint_count"
                ),
                "$where": f"{category_filter} AND {two_year_filter}",
                "$group": "house_number, house_street, community_board, bin",
                "$order": "complaint_count DESC",
                "$limit": 15,
                "$$app_token": self.app_token,
            }
            resp = requests.get(self.BASE_URL, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, list) else []

        def _query_monthly() -> List[Dict[str, Any]]:
            # Fetch individual date_entered values for current year, group in Python.
            # date_extract_m() does not work on MM/DD/YYYY text fields.
            params: Dict[str, Any] = {
                "$select": "date_entered",
                "$where": (
                    f"{category_filter} AND date_entered LIKE '%/{current_year}'"
                ),
                "$limit": 50000,
                "$$app_token": self.app_token,
            }
            resp = requests.get(self.BASE_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, list) else []

        # Run all three queries in parallel.
        raw_borough: List[Dict[str, Any]] = []
        raw_top: List[Dict[str, Any]] = []
        raw_monthly: List[Dict[str, Any]] = []

        futures_map = {}
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures_map[pool.submit(_query_borough_breakdown)] = "borough"
            futures_map[pool.submit(_query_top_buildings)] = "top"
            futures_map[pool.submit(_query_monthly)] = "monthly"

            for future in as_completed(futures_map):
                key = futures_map[future]
                try:
                    query_result: List[Dict[str, Any]] = future.result()
                except Exception as exc:
                    print(f"SODA city_stats [{key}] error: {exc}")
                    query_result = []
                if key == "borough":
                    raw_borough = query_result
                elif key == "top":
                    raw_top = query_result
                else:
                    raw_monthly = query_result

        # --- Process borough breakdown ---
        borough_totals: Dict[str, int] = {}
        for row in raw_borough:
            cb: str = str(row.get("community_board", ""))
            first_char = cb[0] if cb else ""
            borough_name = BOROUGH_MAP.get(first_char, "Unknown")
            borough_totals[borough_name] = borough_totals.get(borough_name, 0) + int(
                row.get("cnt", 0)
            )

        total_12mo: int = sum(borough_totals.values())
        borough_breakdown: List[Dict[str, Any]] = sorted(
            [
                {
                    "name": name,
                    "count": count,
                    "pct": round(count / total_12mo * 100, 1) if total_12mo else 0.0,
                }
                for name, count in borough_totals.items()
            ],
            key=lambda d: d["count"],
            reverse=True,
        )

        # --- Process top buildings ---
        top_buildings: List[Dict[str, Any]] = []
        for row in raw_top:
            house_num = row.get("house_number", "")
            street = row.get("house_street", "")
            address = (
                f"{house_num} {street}".strip() if house_num or street else "Unknown"
            )
            cb = str(row.get("community_board", ""))
            borough_name = BOROUGH_MAP.get(cb[0] if cb else "", "Unknown")
            top_buildings.append(
                {
                    "address": address,
                    "borough": borough_name,
                    "count": int(row.get("complaint_count", 0)),
                    "bin": str(row.get("bin", "")).strip(),
                    "council_district": None,
                    "rep_name": None,
                }
            )

        # --- Enrich top buildings with council district data ---
        use_mock = os.getenv("USE_MOCK_GEOCLIENT", "False").strip().lower() == "true"

        if not use_mock:
            from buildings_app.models import CouncilDistrict
            from services.geoclient import GeoclientService

            def _lookup_district(index: int, bin_val: str) -> tuple[int, Optional[str]]:
                """Return (index, council_district_str) for a given BIN."""
                try:
                    geo_response = GeoclientService().get_address_details(bin_val)
                    district: Optional[str] = geo_response.get("bin", {}).get(
                        "cityCouncilDistrict"
                    )
                    if not district:
                        district = geo_response.get("address", {}).get(
                            "cityCouncilDistrict"
                        )
                    return (index, str(district).strip() if district else None)
                except Exception as exc:
                    print(f"Geoclient district lookup error for BIN {bin_val}: {exc}")
                    return (index, None)

            district_futures: dict[Any, int] = {}
            with ThreadPoolExecutor(max_workers=5) as geo_pool:
                for idx, building in enumerate(top_buildings):
                    bin_val = building.get("bin", "")
                    if bin_val:
                        fut = geo_pool.submit(_lookup_district, idx, bin_val)
                        district_futures[fut] = idx

                for fut in as_completed(district_futures):
                    try:
                        result_idx, council_district = fut.result()
                        top_buildings[result_idx]["council_district"] = council_district
                    except Exception as exc:
                        print(f"Geoclient future error: {exc}")

            # Resolve rep names from CouncilDistrict model (one query per building, ≤15)
            for building in top_buildings:
                district_id = building.get("council_district")
                if district_id:
                    try:
                        district_obj = CouncilDistrict.objects.get(
                            district_id=district_id
                        )
                        building["rep_name"] = district_obj.member_name
                    except CouncilDistrict.DoesNotExist:
                        building["rep_name"] = None

        # --- Process monthly breakdown ---
        # Each row has a date_entered string in MM/DD/YYYY format; extract month index.
        monthly_counts: Dict[int, int] = {}
        for row in raw_monthly:
            try:
                date_str = str(row.get("date_entered", ""))
                month_num = int(date_str.split("/")[0])
                if 1 <= month_num <= 12:
                    monthly_counts[month_num] = monthly_counts.get(month_num, 0) + 1
            except (IndexError, ValueError):
                continue

        monthly_current_year: List[Dict[str, Any]] = [
            {"month": MONTH_NAMES[i], "count": monthly_counts.get(i + 1, 0)}
            for i in range(12)
        ]

        stats: Dict[str, Any] = {
            "total_complaints_12mo": total_12mo,
            "borough_breakdown": borough_breakdown,
            "top_buildings": top_buildings,
            "monthly_current_year": monthly_current_year,
        }
        cache.set(CACHE_KEY, stats, CACHE_TTL)
        return stats
