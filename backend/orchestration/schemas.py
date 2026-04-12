from typing import List

from pydantic import BaseModel, Field


class SODAResearchResult(BaseModel):
    """Schema for the SODAResearcher's analysis of historical NYC Open Data."""

    historical_summary: str = Field(
        description="A concise summary of historical elevator issues at this building."
    )
    pattern_detected: str = Field(
        description="Any recurring patterns (e.g., 'Failure every summer', 'Quick fixes that fail again')."
    )
    total_incidents_found: int = Field(
        description="Count of incidents identified in the historical record."
    )
    reliability_rating: float = Field(
        description="0.0 to 1.0 rating of the building's historical elevator reliability."
    )


class CommunitySentimentResult(BaseModel):
    """Schema for the CommunityReporter's analysis of local tenant logs."""

    sentiment_summary: str = Field(
        description="Summary of tenant frustration and momentum."
    )
    urgent_reports_found: int = Field(
        description="Number of P0/P1 emergency reports in the local logs."
    )
    advocacy_momentum: str = Field(
        description="Description of how active the tenant association or group is."
    )
    key_complaints: List[str] = Field(
        description="List of specific recurring complaints from residents."
    )


class AdvocacyStrategyResult(BaseModel):
    """Schema for the AdvocacyStrategist's legal and strategic advice."""

    headline: str
    script: str = Field(description="The 311 or management call script.")
    legal_reference: str = Field(
        description="Specific NYC Housing Code or Law being cited."
    )
    next_steps: List[str] = Field(
        description="Actionable steps for the tenant to take next."
    )


class ExecutiveSummary(BaseModel):
    """The final synthesized report from the Supervisor."""

    headline: str
    risk_level: str  # Critical, High, Moderate, Nominal
    historical_patterns: str
    community_sentiment: str
    legal_standing: str
    recommended_action: str
    confidence_score: float
