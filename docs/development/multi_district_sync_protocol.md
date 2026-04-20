# Technical Protocol: Multi-District Historical Sync & AI Reporting

## Objective
To provide a scalable, automated pipeline for generating policymaker-facing reports for any of the 51 NYC City Council Districts, identifying high-risk buildings and providing full historical context.

## The Multi-District Workflow
The system uses a model-driven approach to resolve geographic boundaries and ingest data:

1.  **District Discovery**: The `CouncilDistrict` model stores borough mappings (including multi-borough districts like District 8 and 34).
2.  **BIN Pre-filtering**: Using `SODAService.get_district_bins()`, the system resolves all Building Identification Numbers (BINs) for a district via MapPLUTO (`64uk-42ks`) and Footprints (`5zhs-2jue`).
3.  **Targeted Ingestion**: SODA complaints are filtered by these BINs *before* geocoding, reducing API overhead by >80%.
4.  **Historical Ingestion**: All-time reports are captured using pagination and include retired categories ('81', '63').
5.  **AI Synthesis**: The `generate_district_reports` command triggers parallel AI summary generation for every building in the district.

## Core Commands
### 1. Sync & Summarize a District
```bash
uv run python manage.py generate_district_reports --district [ID]
```
This is the "One-Button" command for advocacy. It performs the sync and generates AI summaries.

### 2. City-wide Sync (Targeted)
```bash
uv run python manage.py sync_soda_citywide --hours [N] --district [ID]
```

## System Standards
- **Rate Limiting**: 200ms delay between NYC Open Data calls.
- **Pagination**: 5,000 record batches with `$offset`.
- **Identity**: `complaint_number` is the primary key for official reports to prevent duplicates.

## Verification Protocol
To verify a new district:
1.  Run `generate_district_reports --district [ID]`.
2.  Check `GET /api/districts/[ID]/report/` for aggregated LOS metrics.
3.  Inspect the "Top Offenders" list for owner data accuracy.

---
**Last Updated**: April 20, 2026
**Framework Version**: 2.0 (Generalized)
