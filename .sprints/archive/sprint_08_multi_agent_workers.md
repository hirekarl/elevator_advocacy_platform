# Sprint 8: Multi-Agent Analysis — The Workers (Back-end)

**Date:** 2026-04-12
**Lead:** Sol (Orchestrator)
**Team:** Elias (Backend Architect), Kiran (Data & AI), Blythe (Validation)
**Status:** IN PROGRESS 🏗️

---

## Objective
Establish the core orchestration layer in the backend and implement the first set of specialized worker agents (`SODAResearcher` and `CommunityReporter`) to enable autonomous building analysis.

---

## Elias: Backend Architect Tasks
- [x] Create `backend/orchestration/` directory structure.
- [x] Implement `base.py` with the `WorkerAgent` abstract base class.
- [x] Implement `supervisor.py` (basic skeleton) to manage worker registration.
- [x] Refactor `AdvocacyStrategist` from `buildings_app/ai_logic.py` into `orchestration/workers/advocacy_strategist.py`.

## Kiran: Data & AI Tasks
- [x] Implement `workers/soda_researcher.py`:
    - Specialization: Historical SODA SoQL queries for pattern discovery.
    - Tool: `SODAService`.
- [x] Implement `workers/community_reporter.py`:
    - Specialization: Summarizing local `ElevatorReport` and `AdvocacyLog` data.
    - Logic: Identify tenant momentum and sentiment.

## Blythe: Quality & Standards Tasks
- [x] Define structured Pydantic schemas for worker outputs in `orchestration/schemas.py`.
- [x] Optimize Gemini 1.5 Flash prompts for extraction precision.
- [x] Ensure full type-hinting and Google-style docstrings across all new files.

---

## Success Criteria
1. `backend/orchestration/` contains a functional `WorkerAgent` base class.
2. `SODAResearcher` successfully extracts historical patterns from SODA via Gemini.
3. `CommunityReporter` accurately summarizes tenant activity logs.
4. `./backend/scripts/pre_flight.sh` passes all checks.
