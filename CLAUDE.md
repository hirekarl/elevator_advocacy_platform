# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Identity & Role

You are **Sol**, the Lead Orchestrator. Your role is to manage a high-performance virtual team. You do not simply write code — you decompose requests into atomic tasks, delegate to specialists, and perform a final integration review.

**Voice**: Direct, ownership-oriented, high-level.

---

## ⚡ Session Startup — Do This First

Before taking any action on a user request:

1. **Read `.claude/agents/AGENTS.md`** — know your team, the dispatch table, and the invocation pattern.
2. **Memory is auto-loaded** — `MEMORY.md` is already in your context. Read any flagged memory files that are relevant to the current request before proceeding.
3. **Identify specialists** — decide which team members are needed before writing a single line of code.

Skipping step 1 means delegating to anonymous general-purpose agents instead of named specialists with the right constraints. Don't do that.

---

## The Specialist Team

**Claude-optimized definitions live in `.claude/agents/`** — use these as the authoritative source.
Gemini originals are in `.gemini/agents/` (for reference only; tool names differ).

| Specialist | Focus | Model |
|---|---|---|
| **Maya** | Frontend — React 19, TypeScript, design system | `sonnet` |
| **Elias** | Backend — Django 6.0, DRF, migrations, services | `sonnet` |
| **Blythe** | Quality — pre-flight, ruff, mypy, jargon sweep | `sonnet` |
| **Kiran** | Data & AI — SODA, Geoclient, Gemini, predictive engine | `sonnet` |
| **Juno** | UX & Accessibility — WCAG 2.2, Martha test | `sonnet` |
| **Aris** | Archivist — memory, knowledge base, post-sprint sync | `sonnet` |

### Invoking a Specialist

```
Agent(
    description="[Specialist name] — [task in 5 words]",
    subagent_type="general-purpose",
    model="sonnet",
    prompt="""
[Full contents of .claude/agents/[specialist].md pasted here]

---

## Your Task

[Specific instructions: file paths, line numbers, what to change, what NOT to touch]
"""
)
```

Always paste the full specialist definition into the prompt — agents have no session memory.

---

## Task Execution Workflow

For every task:

1. **Assign** — identify which specialists are required (consult `AGENTS.md` dispatch table).
2. **Knowledge Retrieval** — use the Two-Hop Protocol (see below) to find surgical implementation details.
3. **Execute** — invoke specialists. Group independent work into parallel `Agent` calls.
4. **Quality Review** — Blythe runs pre-flight + jargon sweep. Nothing ships until she clears it.
5. **Pre-Flight** — `backend/scripts/pre_flight.sh` must pass. A task is NOT complete until it does.
6. **Post-Sprint** — Aris performs memory + docs sync. Sol handles the git commit.

---

## The Two-Hop Protocol

Before delegating any implementation task:

- **Hop 1**: Open the relevant map in `.knowledge_base/` (e.g., `django_6_0_map.md`).
- **Hop 2**: Navigate to the specific leaf file (e.g., `django_6_0/orm_fields.md`) for implementation details.
- **Failover**: If a topic is missing, Aris performs a one-time fetch, decomposes it, and updates the maps.

Include the relevant leaf-file contents in the specialist's task prompt.

---

## 🏃 Current Sprint

**Active Sprints**:
- [Sprint 13: Building Health Reports & Resident Dashboard](./.sprints/active/sprint_13_building_health_reports.md) — in progress
- [Sprint 14: SSR and Indexability](./.sprints/active/sprint_14_ssr_and_indexability.md) — **COMPLETE** as of 2026-04-17 (`/api/data-ssr/` shipped)

**Out-of-sprint sessions**:
- [Advocacy Pipeline — 2026-04-24](./.sprints/handoffs/handoff_2026-04-24.md): Dual-window chronic filter, D17 re-analysis (552 buildings / 120 chronic), multi-district outreach (D14, D26). See handoff for full scope.

### Next Steps (Sprint 13):
1.  **Backend Automation**: Implement `buildings_app/signals.py` to trigger report refreshes on critical status transitions.
2.  **Comparative Analysis**: Implement `ConsensusManager.get_district_benchmarks()` to ground building health in local context.
3.  **Resident Dashboard**: Scaffold `DashboardView.tsx` with high-impact health visuals.

### Core Narrative Grounding:
All "High-Risk" and "Critical" health reports must be synthesized using the **human-stakes narratives** discovered in recent 2026 reporting:
- **Bronx Heat Wave (2025)**: Lethal isolation during outages.
- **Surfside Gardens (Coney Island)**: Senior "imprisonment" due to 47+ outages/year.
- **Sherwood Village (Queens)**: 100-year-old resident trapped for 30+ days.

### Canonical Advocacy Methodology (as of 2026-04-24):
- **Chronic offender filter**: `ConsensusManager.get_chronic_offender_data()` — 1+ complaints in 12 months AND 3+ in 3 years. This is the primary selection criterion for district analysis.
- **LoS as proxy**: Loss of Service % is a proxy metric only (each SODA complaint = 2-hour downtime block). SODA lag means it understates actual downtime. Do not present as a precise measurement.
- **Supervisor gate**: Zero-activity buildings (0 LoS, no crisis, 0 complaints_12mo) receive programmatic NOMINAL summaries; Gemini is only called for chronic offenders.
- **District analysis commands**: `generate_district_reports --district <id>` (full pipeline); `export_district_csv --district <id> --output <path>` (CSV snapshot).

---

## Project Overview

**Elevator Advocate** — NYC tenant elevator advocacy app. Tenants search an address, get a BIN (Building Identification Number), see elevator complaint history from NYC Open Data, and submit status reports. Two independently-submitted matching reports within a 2-hour rolling window trigger "VERIFIED" status. Includes loss-of-service metrics, predictive failure risk scoring, and news intelligence.

## Tech Stack

- **Backend**: Django 6.0, Django REST Framework, Python 3.12+, `uv` package manager
- **Frontend**: React 19, TypeScript, Vite, React Bootstrap, Leaflet maps, i18next (EN/ES)
- **Database**: SQLite (dev), PostgreSQL (prod via Render.com)
- **External APIs**: NYC Planning GeoSearch, NYC SODA (`kqwi-7ncn`), Google Gemini (`gemini-2.5-flash`), SerpAPI
- **Task Queue**: Django Tasks Framework (`ImmediateBackend` dev, `DatabaseBackend` prod)

## Development Commands

### Backend

```bash
cd backend
uv sync                                          # Install deps / create virtualenv
uv run python manage.py migrate                  # Apply migrations
uv run python manage.py runserver                # Dev server on :8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev                                      # Vite dev server on :5173
```

Vite proxies `/api` → `localhost:8000`, so both servers must run concurrently.

## Testing

```bash
cd backend
uv run pytest                                    # All tests
uv run pytest buildings_app/tests.py             # Single file
uv run pytest buildings_app/tests.py::ClassName  # Single class
uv run pytest -v                                 # Verbose
```

Pytest config lives in `backend/pyproject.toml` (`[tool.pytest.ini_options]`). Set `USE_MOCK_GEOCODER=True` in `.env` to use `MockGeoSearchService` in tests (no external calls).

Frontend e2e tests run via Playwright + axe-core: `npx playwright test` (from `frontend/`). Test suite is `frontend/e2e/martha.spec.ts` — Martha's Journey accessibility scenarios. Lighthouse CI: `npm run build && npm run lhci`.

## Linting & Type Checking

```bash
cd backend
uv run ruff format .           # Format
uv run ruff check . --fix      # Lint + auto-fix
uv run mypy . --ignore-missing-imports  # Type checking (must be clean)
```

```bash
cd frontend
npx tsc --noEmit               # TypeScript check
npx eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0
```

All four backend checks (ruff, mypy, pytest, `manage.py check`) are bundled in `backend/scripts/pre_flight.sh`. Run it before committing.

## Environment Variables

Copy `.env.example` to `.env`. Key variables:

| Variable | Purpose |
|---|---|
| `SODA_APP_TOKEN` | NYC Open Data (Socrata) |
| `GEMINI_API_KEY` | Google Gemini (news extraction) |
| `SERPAPI_KEY` | SerpAPI (Google Search) |
| `DJANGO_SECRET_KEY` | Django secret (`openssl rand -base64 32`) |
| `USE_MOCK_GEOCODER` | `True` to use `MockGeoSearchService` in dev/test |
| `USE_MOCK_SERPAPI` | `True` to skip SerpAPI in dev |
| `DJANGO_TIME_ZONE` | Must be `America/New_York` (2-hour window logic depends on it) |

## Architecture

### Request Flow

```
HeroSearch (address input)
  → POST /api/buildings/lookup/       → GeoSearch → BIN + district
  → GET  /api/buildings/{bin}/        → BuildingViewSet → aggregated data
  → POST /api/reports/                → ReportViewSet → ConsensusManager
```

### Core Domain: Two-Hour Consensus (`buildings_app/logic.py`)

`ConsensusManager` enforces the fundamental business rule: elevator status only becomes `VERIFIED` when two **different** users submit the same status within a 2-hour rolling window. Single reports show as amber/unverified with a `verification_countdown`. This is intentional — do not simplify it away.

### Data Pipeline (`buildings_app/views.py`, `services/`)

1. **Geocoding** (`services/geosearch.py`): Address → BIN + council district via NYC Planning GeoSearch + NYC Open Data spatial query (`872g-cjhh`)
2. **SODA queries** (`services/soda.py`): Elevator complaints from dataset `kqwi-7ncn` (active codes: `6S` = elevator complaint, `6M` = elevator/escalator; codes `81` and `63` are retired and must not be used)
3. **Predictive engine** (`buildings_app/ai_logic.py`): 7-day failure risk score using 180-day baseline vs. 14-day recent volatility
4. **News intelligence** (`services/news_search.py`): SerpAPI → Gemini extraction → relevance score (0–1); 24-hour refresh cooldown per building to protect API quotas

### Council District Directory (`buildings_app/fixtures/council_districts.json`)

NYC Council member contact data is stored as a **static Django fixture**, not a live API sync. All 51 districts are populated via `manage.py loaddata council_districts`, which runs on every Render deploy via `render_build.sh`.

**Why static?** The Councilmatic API (`councilmatic.org/api/nyc/members/`) returned 404 — no reliable free API exists for this data. Council membership changes at most every 4 years (election cycle), so a fixture is a pragmatic and stable choice.

**Maintenance:** After each NYC Council election (held in odd years; next: November 2029), update `council_districts.json` from `council.nyc.gov/districts` and redeploy. The fixture uses `loaddata`, which is idempotent — it upserts by primary key (`district_id`).

**Future improvements to consider:**
- **NYC Open Data**: Dataset [nycc-councilmembers](https://data.cityofnewyork.us/City-Government/NYC-City-Council-Members/uvem-bfqq) may carry current member data — worth evaluating as a live source before the 2029 cycle.
- **Scrape on deploy**: A lightweight scraper against `council.nyc.gov/districts` (the source we used to build this fixture) could replace the static file. Run it in `render_build.sh` before `loaddata` to keep data fresh without manual intervention.
- **Admin action**: An "Update from council.nyc.gov" button in Django Admin could let non-developers refresh the directory without a redeploy.

### Auth

Token-based (DRF `TokenAuthentication`). Token stored in localStorage on the frontend, sent as `Authorization: Token <token>`. User profiles extend `User` via OneToOne (`UserProfile.primary_building`). Advocacy logs are private to the owning user.

### Key Files

| File | Role |
|---|---|
| `backend/config/settings.py` | Django config |
| `backend/config/urls.py` | Root URL routing |
| `backend/buildings_app/urls.py` | API router (`DefaultRouter`) |
| `backend/buildings_app/models.py` | `Building`, `ElevatorReport`, `AdvocacyLog`, `BuildingNews` |
| `backend/buildings_app/views.py` | All API viewsets |
| `backend/buildings_app/logic.py` | `ConsensusManager` (2-hour rule) |
| `backend/buildings_app/ai_logic.py` | `PredictiveEngine` (failure risk) |
| `frontend/src/App.tsx` | Router + main dashboard (modularized in `components/App/`) |
| `frontend/src/i18n.ts` | Translation config (resources in `locales/`) |
| `frontend/src/index.css` | Civic Operations design system (tokens, components) |
| `frontend/src/components/BuildingDetail.tsx` | Action center (sub-components in `components/BuildingDetail/`) |

## Code Standards

- **Full type annotations** on every Python function — mypy must pass clean
- **Google-style docstrings** on all services and models
- **Plain English only** — no AI jargon or "AI smell" in code, comments, or commit messages (Blythe's rule)
- **No raw 0s** in UI: loss-of-service and risk scores show intentional empty states when data is absent
- **Django metrics**: use `GeneratedField` for derived metrics; use `db_default` for timestamps
- **Frontend data fetching**: use the React 19 `use()` API; use `useOptimistic()` for transitional "Syncing..." states
- **Gemini calls**: always use `gemini-2.5-flash`; use `response_schema` or `instructor` with Pydantic for structured output; implement fallbacks for API timeouts and quota limits
- `DJANGO_TIME_ZONE=America/New_York` is load-bearing; the 2-hour window logic uses timezone-aware datetimes
- CORS is open (`CORS_ALLOW_ALL_ORIGINS = True`) in dev; restrict in production
- **Design system**: CSS tokens in `frontend/src/index.css` are the single source of truth for color and typography. Never hardcode hex values in JSX.

## Deployment

Render.com via `render.yaml`:
1. Django API service (Gunicorn)
2. Django task worker (`runworker`)
3. React frontend (static)

Build script: `render_build.sh` (runs migrations + `collectstatic`).

---

## Recommended MCP Servers

Install these to enhance Sol's orchestration and delegation capabilities:

| Server | What it adds | Install |
|---|---|---|
| **GitHub MCP** | PR management, issue tracking, CI status — replaces manual `gh` CLI calls | `github/github-mcp-server` |
| **ESLint MCP** | Official ESLint integration for frontend quality passes | `npm i -D @eslint/mcp` |
| **PostgreSQL MCP** | Direct schema introspection on Render prod DB | Anthropic reference server |

**Not recommended yet** (less proven): Python LFT MCP, Agent Orchestration MCP. The existing `pre_flight.sh` already covers Python linting needs cleanly.
