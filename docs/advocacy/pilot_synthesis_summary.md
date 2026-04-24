# Executive Summary: Advocacy Pilot & Legislative Coalition

**Last updated:** April 24, 2026

## 1. The "Loss of Service" (LoS) Mandate

The core mission is to convert fragmented NYC Open Data (SODA) into a verified, quantified metric for housing justice.

- **Verification Rule:** A "two-unique-user" consensus window of 120 minutes ensures data integrity.
- **The Metric:** LoS % = (Total Down Time / Total Period Time) × 100.
- **Heuristic:** Each SODA complaint is treated as a proxy for a 2-hour service disruption — the minimum window used to confirm an outage through tenant consensus.
- **Known limitation:** LoS % is a complaint-frequency index, not a measured duration. SODA complaints record when a complaint was filed, not how long the elevator was down. Present as a relative risk signal, not a precise figure.

---

## 2. District Analysis Status

All analyses use the **dual-window chronic filter**: 1+ complaints in the last 12 months AND 3+ complaints in the last 3 years. Non-chronic buildings receive a programmatic NOMINAL summary without calling Gemini.

### D17 — Justin Sanchez (Bronx) — COMPLETE

- **552 buildings** analyzed; **120 chronic offenders** (22%); 432 nominal
- Full report: `docs/advocacy/districts/district_17/district_17_final_report.md`
- CSV: `docs/advocacy/districts/district_17/district_17_data_snapshot.csv`

| Address | Complaints (12mo) | Complaints (3yr) |
|:---|:---|:---|
| **601 East 156 St** | 8 | 24 |
| **303 East 158 St** | 7 | 26 |
| **1068 Franklin Ave** | 6 | 11 |
| **390 East 158 St** | 5 | 36 |
| **1090 Franklin Ave** | 5 | 12 |

*Note: 1150 Tiffany St (cited in original April 17 outreach) was corrected — 3 complaints (12mo) / 7 (3yr), not 12.*

### D14 — Pierina Ana Sanchez (Bronx) — COMPLETE

- **671 buildings** analyzed; **154 chronic offenders** (23%); 517 nominal
- Top address: **2240 Walton Avenue** — 12 complaints (12mo) / 26 complaints (3yr)
- Full report: `docs/advocacy/districts/district_14/district_14_final_report.md`
- CSV: `docs/advocacy/districts/district_14/district_14_data_snapshot.csv`

### D27 — Dr. Nantasha Williams (Queens) — COMPLETE

- **231 buildings** analyzed; **37 chronic offenders** (16%); 194 nominal
- Top address: **89-20 161 Street** — 6 complaints (12mo) / 34 complaints (3yr)
- Active safety complaint on record as of March 2026: **169-28 110 Road**
- Full report: `docs/advocacy/districts/district_27/district_27_final_report.md`
- CSV: `docs/advocacy/districts/district_27/district_27_data_snapshot.csv`

| Address | Complaints (12mo) | Complaints (3yr) | Risk |
|:---|:---|:---|:---|
| **89-20 161 St** | 6 | 34 | CRITICAL |
| **90-10 149 St** | 6 | 12 | HIGH |
| **147-40 Archer Ave** | 6 | 7 | HIGH |
| **90-10 150 St** | 5 | 12 | CRITICAL |
| **169-28 110 Rd** | 4 | 16 | CRITICAL |

### D26 — Julie Won (Queens) — DATA ONLY, NOT IN ACTIVE OUTREACH

- **524 buildings** analyzed; **37 chronic offenders** (7%); 487 nominal
- Analysis run April 24, 2026. Julie Won is not on Housing & Buildings Committee.
- Not in current outreach plan. Data available in database if needed.

---

## 3. Outreach Strategy & Status

All outreach materials live under `docs/advocacy/outreach/`. See `TRACKER.md` for live status.

### Phase 1 — D17 constituent engagement (IN PROGRESS)

- Original email sent **2026-04-17** to Justin Sanchez's office.
- **Kevin Collado (Community Liaison) responded 2026-04-24** — invited to a virtual intro meeting.
- **Meeting scheduled: Thursday, May 7, 2026.**
- Follow-up email superseded by meeting. Meeting brief, notes template, and follow-up template at `contacts/d17_justin_sanchez/`.
- **Primary ask at meeting:** warm introduction to Pierina Ana Sanchez's office (D14).
- Justin Sanchez is NOT on Housing & Buildings; outreach framed as constituent engagement.

### Phase 2 — D14 committee pitch (ON HOLD — pending May 7)

- Highest-leverage contact: Pierina Ana Sanchez chairs Housing & Buildings Committee.
- Draft complete at `contacts/d14_pierina_sanchez/outreach.md`. All data in hand.
- **On hold:** primary ask on May 7 is a warm intro from Justin Sanchez's office. Cold-emailing before that burns the intro. Send after May 7 — use warm intro if offered, else send cold.

### Phase 3 — D27 Queens committee pitch (SENT — April 24, 2026)

- **Dr. Nantasha Williams** — the only Queens member on the Housing & Buildings Committee.
- Replaces Shekar Krishnan (D25 — wrong district, no committee jurisdiction).
- Email sent April 24, 2026. Awaiting response.
- Draft on file at `contacts/d27_nantasha_williams/outreach.md`.

### Sent

- **LinkedIn post** — sent April 24, 2026
- **Twitter/X thread** — sent April 24, 2026

### Coalition — not yet contacted

Reach out after D14 and D27 are in motion. All are Housing & Buildings Committee members:

| Priority | Member | District | Role |
|:---|:---|:---|:---|
| 4 | Yusef Salaam | D9 (Harlem/West Bronx) | H&B member |
| 5 | Shaun Abreu | D7 (Upper Manhattan) | H&B member + Transportation Chair |
| 6 | Oswald Feliz | D15 (Bronx) | H&B member |
| 7 | Kevin C. Riley | D12 (Norwood/Fordham) | H&B member + Land Use Chair |

---

## 4. Technical Readiness

- **Pre-flight:** `bash backend/scripts/pre_flight.sh` — ruff format + lint, mypy, Django check, pytest. Must pass before every backend commit. Pre-commit hooks installed as of April 24, 2026.
- **export_district_csv:** Fixed April 24, 2026 to sort chronic-first (12mo desc, 3yr desc) rather than alphabetically. Use `--output` with an absolute path.
- **District commands:** `generate_district_reports --district <id>` (full pipeline); `export_district_csv --district <id> --output <path>` (CSV snapshot).
- **Sprint 13 in progress:** Building Health Reports and Resident Dashboard. See `.sprints/active/sprint_13_building_health_reports.md`.
- **Pursuit internal email:** Drafted and gitignored at `contacts/pursuit/internal_email.md`. Send after May 7 with meeting outcome framing.
