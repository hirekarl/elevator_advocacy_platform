from typing import Optional, Dict, Any

class MockGeoclientService:
    """
    Mock implementation of the NYC Geoclient v2 API.
    Provides realistic BINs for testing without external API calls.
    """

    # Real NYC Address -> BIN mappings for testing
    MOCK_DATA = {
        ("120", "Broadway", "Manhattan"): "1001145",
        ("1", "City Hall Park", "Manhattan"): "1000001",
        ("350", "5th Ave", "Manhattan"): "1015862", # Empire State Building
        ("200", "Eastern Pkwy", "Brooklyn"): "3028212", # Brooklyn Museum
    }

    def get_bin(self, house_number: str, street: str, borough: str) -> Optional[str]:
        """
        Returns a mock BIN for common addresses, or a deterministic dummy BIN.
        """
        # Normalized lookup
        key = (house_number.strip(), street.strip().title(), borough.strip().title())
        
        if key in self.MOCK_DATA:
            return self.MOCK_DATA[key]
        
        # Deterministic fallback for any NYC-like address
        return f"9{hash(key) % 1000000:06d}"

    def get_address_details(self, bin: str) -> Dict[str, Any]:
        """
        Returns mock address metadata.
        """
        return {
            "address": {
                "buildingIdentificationNumber": bin,
                "houseNumber": "120",
                "street": "Broadway",
                "borough": "Manhattan"
            }
        }
