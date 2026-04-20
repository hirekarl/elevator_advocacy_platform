# NYC Tenant Elevator Advocacy Platform - Project Specification

## 1. Context & Tech Standards
- **Role**: You are a Senior Lead Developer bootstrapping a full-stack advocacy tool.
- **Python Standard**: Django 6.0, `uv` for environment/dependency management, PEP-8, full type-hints (`mypy`), Google-style docstrings, and `ruff` for formatting[cite: 2, 134, 145, 146].
- **Frontend Standard**: React 19, Vite, TypeScript, using `use` and `useOptimistic` hooks.
- **Architecture**: Monorepo with decoupled services. Prioritize "decoupling + deduplication".

## 2. Monorepo Structure
- `/backend`: Django 6 + DRF. Core apps: `buildings` (logic), `services` (API wrappers), `orchestration` (AI agents).
- `/frontend`: React 19 + Vite + TypeScript.
- `/docker-compose.yml`: Local dev orchestration.

## 3. Core Features & Logic
- **Data Pipeline**: Resolve address to BIN via NYC Geoclient API. Query elevator complaints from NYC Open Data (SODA) using SoQL.
- **Verification Engine**: "Second-logged observation" rule. Requires a verification from a different user within a 2-hour window to update the canonical elevator status. Includes a `verification_countdown` for transparency.
- **Multi-Agent Analysis**: A Supervisor-Worker system (Gemini 2.5 Flash).
    - **SODAResearcher**: Aggregates history from SODA API.
    - **CommunityReporter**: Aggregates local tenant logs.
    - **AdvocacyStrategist (Implemented)**: Maps data against NYC housing law to suggest specific legal/organizing next steps and generates 311 scripts.
- **Advocacy Reporting Framework**: Model-driven district mapping for automated advocacy.
    - **District-Borough Mapping**: `CouncilDistrict` model maps all 51 districts to borough codes (supporting multi-borough districts).
    - **Pre-filtered Ingestion**: High-performance pipeline resolves all BINs for a district via MapPLUTO/Footprints *before* SODA syncing to reduce geocoding overhead by >80%.
    - **Historical Context**: captures all-time reports including retired SODA categories ('81', '63').
- **ROI/Metrics**: AI calculates a "Loss of Service" metric (e.g., % of time down over 30 days).

## 4. API & Integration Needs
- NYC Developer Portal (Geoclient API).
- NYC Open Data App Token (SODA API).
- LLM Provider (LangChain/OpenAI) for agentic analysis.
