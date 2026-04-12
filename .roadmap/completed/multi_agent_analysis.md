# Proposal: Phase 6 — Multi-Agent Analysis (Supervisor-Worker System)

## Objective
To provide tenants and advocates with a deep, AI-synthesized "Executive Building Summary" that combines historical SODA data, real-time tenant logs, and NYC housing law into a single, actionable report.

## The Team (Specialists)
- **Elias (Backend Architect):** Implement the `Agent` and `Supervisor` base classes in `backend/orchestration/`.
- **Kiran (Data & AI):** Build the `SODAResearcher` and `CommunityReporter` worker agents.
- **Maya (Frontend):** Create the "Executive Summary" UI card and implement React 19 `use()` fetching.
- **Blythe (Quality):** Ensure all LLM prompts are optimized and output is structured via `instructor` and Pydantic.

## Architectural Changes

### 1. The Orchestration Layer (`backend/orchestration/`)
- `base.py`: Abstract Base Class `WorkerAgent`.
- `supervisor.py`: The orchestrator that manages worker lifecycles and synthesizes final reports.
- `workers/soda_researcher.py`: Agent specialized in historical SODA SoQL queries.
- `workers/community_reporter.py`: Agent specialized in summarizing local `ElevatorReport` and `AdvocacyLog` data.
- `workers/advocacy_strategist.py`: Transitioned from `ai_logic.py`.

### 2. The Summary Schema
A structured Pydantic model for the final executive output:
```python
class ExecutiveSummary(BaseModel):
    headline: str
    risk_level: str  # Critical, High, Moderate, Nominal
    historical_patterns: str
    community_sentiment: str
    legal_standing: str
    recommended_action: str
    confidence_score: float
```

### 3. API & Frontend
- **Endpoint:** `GET /api/buildings/{bin}/advocacy_summary/`
- **Frontend:** A high-impact "AI Executive Summary" card at the top of the Building Action Center.

## Implementation Plan

### Sprint 8: The Workers (Back-end)
- Implement `SODAResearcher` and `CommunityReporter`.
- Move `AdvocacyStrategist` to the orchestration folder.
- Unit tests for each worker using mock LLM responses.

### Sprint 9: The Supervisor & UI (Full-stack)
- Implement the `Supervisor` synthesis logic.
- Create the DRF endpoint.
- Build the "Executive Summary" React component with "Syncing..." optimistic states.

## Verification Protocol
- All worker agents must return valid Pydantic models.
- The Supervisor must successfully aggregate 3 worker responses into a final summary.
- `./backend/scripts/pre_flight.sh` must pass.
