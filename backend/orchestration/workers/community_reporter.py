from typing import Any, Dict, Optional

from orchestration.base import WorkerAgent
from orchestration.schemas import CommunitySentimentResult


class CommunityReporter(WorkerAgent[CommunitySentimentResult]):
    """
    Kiran's Worker: Summarizes local tenant reports and advocacy logs.
    Identifies tenant momentum, key pain points, and current sentiment.
    """

    def analyze(self, context: Dict[str, Any]) -> Optional[CommunitySentimentResult]:
        """
        Analyzes community activity.
        Context should include 'reports' (list of dicts) and 'logs' (list of dicts).
        """
        reports = context.get("reports", [])
        logs = context.get("logs", [])

        if not reports and not logs:
            return CommunitySentimentResult(
                sentiment_summary="No tenant reports or advocacy logs recorded for this building yet.",
                urgent_reports_found=0,
                advocacy_momentum="Dormant",
                key_complaints=["None"],
            )

        # 1. Prepare data text for analysis
        reports_text = "\n".join(
            [
                f"- Status: {r.get('status')}, Time: {r.get('reported_at')}"
                for r in reports[:20]
            ]
        )

        logs_text = "\n".join(
            [
                f"- Action: {log.get('description') or '311 Logged'}, SR#: {log.get('sr_number')}, Time: {log.get('created_at')}"
                for log in logs[:20]
            ]
        )

        urgent_count = sum(
            1 for r in reports if r.get("status") in ["TRAPPED", "UNSAFE", "DOWN"]
        )

        prompt = (
            f"You are a Community Organizer specializing in NYC tenant rights. Analyze the following "
            f"local elevator status reports and tenant advocacy logs for this building:\n\n"
            f"TENANT REPORTS:\n{reports_text}\n\n"
            f"ADVOCACY LOGS (311 entries, etc):\n{logs_text}\n\n"
            f"There are {urgent_count} urgent reports in this period.\n\n"
            f"Identify the current tenant sentiment (e.g., 'Increasingly frustrated', 'Organized but waiting'). "
            f"Evaluate the 'advocacy momentum' (how actively neighbors are reporting/sharing) and list 2-3 key complaints."
        )

        # 2. Call Gemini for structured extraction
        return self._call_gemini(prompt, CommunitySentimentResult)
