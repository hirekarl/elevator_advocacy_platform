from typing import Any, Optional

import requests

COUNCIL_DISTRICTS_URL = "https://data.cityofnewyork.us/resource/872g-cjhh.json"


def district_from_coordinates(lat: float, lon: float) -> Optional[str]:
    """
    Returns the NYC Council district number for a lat/lon via a
    point-in-polygon spatial query against NYC Open Data (no API key needed).
    """
    try:
        response = requests.get(
            COUNCIL_DISTRICTS_URL,
            params={
                "$where": f"intersects(the_geom, 'POINT ({lon} {lat})')",
                "$select": "coundist",
                "$limit": "1",
            },
            timeout=5,
        )
        response.raise_for_status()
        results = response.json()
        if results:
            return str(results[0].get("coundist"))
    except Exception:
        pass
    return None


class GeoSearchService:
    """
    Geocoder backed by the NYC Planning Labs GeoSearch API.

    No authentication required. Primary geocoder for address → BIN resolution.
    Also performs a council district spatial lookup from the returned coordinates.

    Reference: https://geosearch.planninglabs.nyc/v2
    """

    BASE_URL = "https://geosearch.planninglabs.nyc/v2/search"

    # GeoSearch uses Pelias borough names; map our app's values to its expectation.
    BOROUGH_ALIASES: dict[str, str] = {
        "manhattan": "manhattan",
        "brooklyn": "brooklyn",
        "queens": "queens",
        "bronx": "bronx",
        "the bronx": "bronx",
        "staten island": "staten island",
        "staten_island": "staten island",
    }

    def get_bin_with_coordinates(
        self, house_number: str, street: str, borough: str
    ) -> dict[str, Any]:
        """
        Geocodes a street address and returns the BIN and lat/lon.

        Builds a free-text query from the address components and hits the
        GeoSearch `/search` endpoint, then extracts the BIN from the PAD
        addendum on the first result.
        """
        borough_key = self.BOROUGH_ALIASES.get(borough.lower(), borough.lower())
        borough_display = borough_key.title()
        query = f"{house_number} {street}, {borough_display}, NY"

        try:
            response = requests.get(
                self.BASE_URL,
                params={"text": query, "size": "1"},
                timeout=10,
            )
            response.raise_for_status()
            features = response.json().get("features", [])

            if not features:
                return {}

            feature = features[0]
            props = feature.get("properties", {})
            coords = feature.get("geometry", {}).get("coordinates", [])
            bin_id = props.get("addendum", {}).get("pad", {}).get("bin")

            if not bin_id or not coords:
                return {}

            returned_borough = self.BOROUGH_ALIASES.get(
                props.get("borough", "").lower(), props.get("borough", "").lower()
            )
            if returned_borough and returned_borough != borough_key:
                print(
                    f"GeoSearch borough mismatch: requested '{borough}', "
                    f"got '{props.get('borough')}' — rejecting result."
                )
                return {}

            council_district = district_from_coordinates(coords[1], coords[0])

            return {
                "bin": str(bin_id),
                "latitude": str(coords[1]),
                "longitude": str(coords[0]),
                "city_council_district": council_district,
            }

        except (requests.RequestException, KeyError, IndexError) as exc:
            print(f"GeoSearch Error: {exc}")
            return {}

    def get_address_details(self, bin_id: str) -> dict[str, Any]:
        """
        GeoSearch does not support BIN-based reverse lookup, so this returns
        an empty dict. The field is only used by ancillary tooling, not the
        core request flow.
        """
        return {}
