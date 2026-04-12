import os
from typing import Optional, Dict, Any
import requests
from django.conf import settings

class GeoclientService:
    """
    Service wrapper for the NYC Geoclient v2 API.
    Maps street addresses to Building Identification Numbers (BIN).
    """

    BASE_URL = "https://api.nyc.gov/geo/geoclient/v2/address.json"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NYC_API_KEY")

    def get_bin(self, house_number: str, street: str, borough: str) -> Optional[str]:
        """
        Geocodes a street address and returns the Building Identification Number (BIN).
        """
        params = {
            "houseNumber": house_number,
            "street": street,
            "borough": borough,
            "subscription-key": self.api_key  # Fallback for some NYC API versions
        }
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key
        }

        try:
            response = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # The Geoclient response structure for v2/address.json
            return data.get('address', {}).get('buildingIdentificationNumber')
        except (requests.RequestException, KeyError) as e:
            # TODO: Integrate with Blythe's logging system
            print(f"Geoclient Error: {e}")
            return None

    def get_address_details(self, bin: str) -> Dict[str, Any]:
        """
        Retrieves full address details from a BIN.
        """
        bin_url = f"https://api.nyc.gov/geo/geoclient/v2/bin/{bin}.json"
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        
        try:
            response = requests.get(bin_url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return {}
