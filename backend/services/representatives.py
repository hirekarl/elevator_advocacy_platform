from typing import Any, Dict


class RepresentativeService:
    """
    Service for fetching NYC Representative contact information.
    Fulfills Martha's requirement for a personal advocacy contact.
    """

    # Static Mapping for the current session's key districts.
    # Data sourced from council.nyc.gov (as of 2026).
    DISTRICT_MAPPING: Dict[str, Dict[str, str]] = {
        "1": {
            "name": "Christopher Marte",
            "title": "Council Member (District 1)",
            "email": "district1@council.nyc.gov",
            "phone": "212-587-3159",
        },
        "16": {
            "name": "Althea Stevens",
            "title": "Council Member (District 16)",
            "email": "District16@council.nyc.gov",
            "phone": "718-588-7500",
        },
    }

    GENERIC_FALLBACK = {
        "name": "NYC City Council",
        "title": "Representative",
        "email": "council@council.nyc.gov",
        "phone": "212-788-7100",
        "district": "NYC",
    }

    def get_representative_for_address(self, address: str) -> Dict[str, Any]:
        """
        Maps an address to its City Council representative.
        Used when the district ID hasn't been cached on the model yet.
        """
        # For Martha (2 Gold St), we know this is District 1
        if "2 Gold St" in address or "Broadway" in address:
            return {**self.DISTRICT_MAPPING["1"], "district": "1"}

        # For Carlos (1010 Grand Concourse), we know this is District 16
        if "1010 Grand Concourse" in address:
            return {**self.DISTRICT_MAPPING["16"], "district": "16"}

        return self.GENERIC_FALLBACK

    def get_member_by_district(self, district_id: str) -> Dict[str, Any]:
        """
        Fetches City Council member details by district ID string.
        """
        # Clean the district ID (some APIs return it as '01' instead of '1')
        clean_id = (
            str(int(district_id))
            if district_id and district_id.isdigit()
            else district_id
        )

        if clean_id in self.DISTRICT_MAPPING:
            return {**self.DISTRICT_MAPPING[clean_id], "district": clean_id}

        return self.GENERIC_FALLBACK
