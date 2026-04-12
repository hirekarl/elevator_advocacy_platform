from typing import Any, Dict, Optional

from orchestration.base import WorkerAgent
from orchestration.schemas import AdvocacyStrategyResult


class AdvocacyStrategist(WorkerAgent[AdvocacyStrategyResult]):
    """
    Sol's Worker: Maps data against NYC housing law to suggest specific
    legal/organizing next steps and generates dynamic 311 scripts.
    """

    def analyze(self, context: Dict[str, Any]) -> Optional[AdvocacyStrategyResult]:
        """
        Analyzes the building's current situation and provides a strategic advocacy plan.
        Context should include 'address', 'verified_status', 'loss_of_service', and 'lang'.
        """
        address = context.get("address", "this building")
        status = context.get("verified_status", "UNKNOWN")
        loss_of_service = context.get("loss_of_service", 0.0)
        lang = context.get("lang", "en")

        prompt = (
            f"You are a Senior Lead Advocacy Strategist. A tenant is inquiring about elevator issues at {address}.\n\n"
            f"CURRENT VERIFIED STATUS: {status}\n"
            f"LOSS OF SERVICE (30D): {loss_of_service}%\n"
            f"LANGUAGE: {lang}\n\n"
            f"INSTRUCTIONS:\n"
            f"1. If the CURRENT STATUS is 'UP', 'NOMINAL', or 'UNVERIFIED' with 0% Loss of Service, provide a PROACTIVE maintenance and monitoring strategy. Do NOT label it an emergency.\n"
            f"2. If the STATUS is 'DOWN', 'TRAPPED', 'UNSAFE', or Loss of Service is > 10%, provide an URGENT advocacy strategy citing NYC Housing Maintenance Code (§27-2005).\n"
            f"3. Generate a professional reporting script in {lang}.\n"
            f"4. Provide 2-3 specific 'next steps'.\n"
            f"5. Provide a high-impact headline appropriate to the actual severity."
        )

        return self._call_gemini(prompt, AdvocacyStrategyResult)
