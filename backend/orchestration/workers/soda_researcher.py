from typing import Any, Dict, Optional

from orchestration.base import WorkerAgent
from orchestration.schemas import SODAResearchResult
from services.soda import SODAService


class SODAResearcher(WorkerAgent[SODAResearchResult]):
    """
    Kiran's Worker: Specialized in historical SODA SoQL queries and analysis.
    Identifies long-term reliability patterns for a specific building.
    """

    def analyze(self, context: Dict[str, Any]) -> Optional[SODAResearchResult]:
        """
        Analyzes historical SODA data for a building.
        Context must include 'bin'.
        """
        bin_id = context.get("bin")
        if not bin_id:
            return None

        # 1. Fetch historical data from SODA Service
        soda_service = SODAService()
        complaints = soda_service.get_elevator_complaints(bin_id, limit=100)

        if not complaints:
            return SODAResearchResult(
                historical_summary="No historical elevator complaints found in NYC Open Data for this building.",
                pattern_detected="None",
                total_incidents_found=0,
                reliability_rating=1.0,
            )

        # 2. Prepare prompt for Gemini
        complaints_text = "\n".join(
            [
                f"- Date: {c.get('date_entered')}, Category: {c.get('complaint_category')}, "
                f"Status: {c.get('status')}"
                for c in complaints[:30]  # Limit to 30 for context efficiency
            ]
        )

        prompt = (
            f"You are a Senior NYC Housing Investigator. Analyze the following historical elevator complaint "
            f"data for BIN {bin_id} from the NYC Department of Buildings (SODA API):\n\n"
            f"{complaints_text}\n\n"
            f"Identify recurring patterns (e.g., 'Chronic failure every summer', 'Quick fixes that recur within weeks'). "
            f"Provide a concise summary and a reliability rating (0.0 to 1.0)."
        )

        # 3. Call Gemini for structured extraction
        return self._call_gemini(prompt, SODAResearchResult)
