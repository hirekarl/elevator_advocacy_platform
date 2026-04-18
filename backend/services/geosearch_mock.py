from typing import Any, Dict


class MockGeoSearchService:
    """
    Mock GeoSearch for testing and local dev without external API calls.

    Returns realistic BIN/coordinate/district data for known addresses.
    Unknown addresses return {} — no phantom hash-based BINs.
    """

    is_mocked = True

    MOCK_DATA: Dict[tuple, Dict[str, Any]] = {
        ("1853", "Anthony Avenue", "Bronx"): {
            "bin": "2007566",
            "latitude": "40.848969",
            "longitude": "-73.908665",
            "city_council_district": "17",
        },
        ("131", "Broome Street", "Manhattan"): {
            "bin": "1003641",
            "latitude": "40.718271",
            "longitude": "-73.998042",
            "city_council_district": "1",
        },
        ("120", "Broadway", "Manhattan"): {
            "bin": "1001145",
            "latitude": "40.707569",
            "longitude": "-74.011348",
            "city_council_district": "1",
        },
        ("1", "City Hall Park", "Manhattan"): {
            "bin": "1000001",
            "latitude": "40.712772",
            "longitude": "-74.006058",
            "city_council_district": "1",
        },
        ("350", "5Th Ave", "Manhattan"): {
            "bin": "1015862",
            "latitude": "40.748433",
            "longitude": "-73.985657",
            "city_council_district": "3",
        },
        ("200", "Eastern Pkwy", "Brooklyn"): {
            "bin": "3028212",
            "latitude": "40.671368",
            "longitude": "-73.963884",
            "city_council_district": "35",
        },
    }

    def get_bin_with_coordinates(
        self, house_number: str, street: str, borough: str
    ) -> Dict[str, Any]:
        key = (house_number.strip(), street.strip().title(), borough.strip().title())
        return dict(self.MOCK_DATA.get(key, {}))

    def get_address_details(self, bin_id: str) -> Dict[str, Any]:
        return {}
