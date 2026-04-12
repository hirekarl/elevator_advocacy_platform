from typing import Any, Dict, Optional

from orchestration.base import WorkerAgent
from orchestration.schemas import ExecutiveSummary
from orchestration.workers.advocacy_strategist import AdvocacyStrategist
from orchestration.workers.community_reporter import CommunityReporter
from orchestration.workers.soda_researcher import SODAResearcher


class Supervisor(WorkerAgent[ExecutiveSummary]):
    """
    Sol's Lead Orchestrator: Manages the worker lifecycle and synthesizes
    their individual analyses into a final high-impact Executive Summary.
    """

    def analyze(self, context: Dict[str, Any]) -> Optional[ExecutiveSummary]:
        """
        Executes all worker agents and synthesizes the results.
        Context needs: 'bin', 'address', 'verified_status', 'loss_of_service', 'lang', 'reports', 'logs'.
        """
        # 1. Initialize Workers
        soda_worker = SODAResearcher()
        community_worker = CommunityReporter()
        advocacy_worker = AdvocacyStrategist()

        # 2. Execute Workers
        soda_result = soda_worker.analyze(context)
        community_result = community_worker.analyze(context)
        advocacy_result = advocacy_worker.analyze(context)

        # 3. Prepare Synthesis Prompt
        soda_text = (
            f"Historical Summary: {soda_result.historical_summary}\nPattern: {soda_result.pattern_detected}\nReliability: {soda_result.reliability_rating}"
            if soda_result
            else "No historical data."
        )
        community_text = (
            f"Sentiment: {community_result.sentiment_summary}\nMomentum: {community_result.advocacy_momentum}\nUrgent Reports: {community_result.urgent_reports_found}"
            if community_result
            else "No community data."
        )
        advocacy_text = (
            f"Strategy Headline: {advocacy_result.headline}\nLegal Reference: {advocacy_result.legal_reference}"
            if advocacy_result
            else "No specific strategy."
        )

        prompt = (
            f"You are the Lead Supervisor of an Elevator Advocacy Team. Synthesize the findings of three specialist agents into a final Executive Summary for building {context.get('address')}.\n\n"
            f"SODA RESEARCHER (Historical Data):\n{soda_text}\n\n"
            f"COMMUNITY REPORTER (Local Activity):\n{community_text}\n\n"
            f"ADVOCACY STRATEGIST (Legal Perspective):\n{advocacy_text}\n\n"
            f"SYNTHESIS GUIDELINES:\n"
            f"1. Risk Level must be NOMINAL if there are 0 current reports, 0 historical reports, and 0% loss of service.\n"
            f"2. Risk Level is MODERATE if there are historical issues but the elevator is currently 'UP'.\n"
            f"3. Risk Level is HIGH or CRITICAL only if there is a verified 'DOWN', 'TRAPPED', or 'UNSAFE' status, or high historical failure frequency.\n"
            f"4. Provide a synthesis that is authoritative, actionable, and reflects the ACTUAL severity documented above."
        )

        # 4. Final Synthesis
        return self._call_gemini(prompt, ExecutiveSummary)
