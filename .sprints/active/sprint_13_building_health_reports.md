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
- [ ] Ensure `risk_level` logic is strictly grounded in both LoS % and current verified status.

## Narrative Reference (Grounding Data)
- **Bronx Heat Wave (2025)**: Lethal isolation due to elevator failure.
- **Aleksandra & Valeriy (Surfside Gardens)**: 47 outages/year; "imprisonment" for seniors with disabilities.
- **Sherwood Village (Queens)**: 100-year-old resident trapped for 30+ days.
