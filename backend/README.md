# Elevator Advocate - Backend (Django 6.0)

The backend is built with Django 6.0 and Django REST Framework, managed by `uv`.

## Key Features
- **Consensus Engine**: Logic for verifying tenant reports within a 2-hour window.
- **Advocacy Reporting Framework**: Automated, district-wide data ingestion and AI summary generation.
- **Multi-Agent Orchestration**: Supervisor-worker pattern using Gemini 2.5 Flash for news extraction and advocacy synthesis.

## Management Commands

### Advocacy & Ingestion
- `uv run python manage.py generate_district_reports --district [ID]`: The main "One-Button" advocacy command. Syncs all historical SODA data and generates AI summaries for a district.
- `uv run python manage.py sync_soda_citywide --hours [N] --district [ID]`: Targeted city-wide sync.
- `uv run python manage.py sync_soda_complaints`: Fast sync for the last 24 hours (modern codes only).
- `uv run python manage.py generate_summaries`: Regenerate AI summaries for all buildings in the DB.

### Database & Seed
- `uv run python manage.py loaddata buildings_app/fixtures/council_districts.json`: Load/Update NYC Council District metadata.
- `uv run python manage.py seed_pilot_buildings`: Seed the database with high-priority pilot buildings.
- `uv run python manage.py seed_users`: Create test users (Martha, Niece, etc.).

## Development
- **Environment**: Managed by `uv`. Use `uv sync` to install dependencies.
- **Standards**: `ruff check .` for linting, `mypy .` for type-checking.
- **Validation**: Run `./scripts/pre_flight.sh` before every commit.
