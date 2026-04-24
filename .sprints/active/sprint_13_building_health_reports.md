# Sprint 13: Building Health Reports & Resident Dashboard

## Objective
Transition building advocacy data from passive "lazy-load" to an active, event-driven "Health" system that grounds data in human stakes.

## Phase 1: Backend Automation
- [ ] Create `buildings_app/signals.py` to trigger report refreshes on critical status transitions.
- [ ] Implement `ConsensusManager.get_district_benchmarks()` for comparative analysis.
- [ ] Refactor summary generation into an asynchronous `@task`.

## Phase 2: Resident Dashboard (Frontend)
- [ ] Scaffold `DashboardView.tsx` as the home for authenticated residents.
- [ ] Build `HealthGauge` component (Visualizing `risk_level`).
- [ ] Implement `LoSTrendCard` using historical data points.
- [ ] Add `QuickAdvocacy` card with 311 script integration.

## Phase 3: AI Synthesis Refinement
- [ ] Update `Supervisor` context to include district-wide benchmarking data.
- [ ] Inject "Human Stakes" narratives (Heat Wave, Senior Isolation) into high-risk prompts.
- [x] **Partial** — Hard NOMINAL gate in `Supervisor.analyze()` ensures zero-activity buildings are never escalated (shipped 2026-04-24 as part of advocacy pipeline sprint). Remaining gap: buildings with 1–3 complaints can still receive "Critical" AI language if the Gemini prompt amplifies them. A calibrated LoS threshold table (0% = Nominal, 0–0.5% = Moderate, etc.) is the fix — deferred.

## Narrative Reference (Grounding Data)
- **Bronx Heat Wave (2025)**: Lethal isolation due to elevator failure.
- **Aleksandra & Valeriy (Surfside Gardens)**: 47 outages/year; "imprisonment" for seniors with disabilities.
- **Sherwood Village (Queens)**: 100-year-old resident trapped for 30+ days.
