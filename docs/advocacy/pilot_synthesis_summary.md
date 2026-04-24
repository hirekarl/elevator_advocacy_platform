# Executive Summary: Phase 6 Advocacy Pilot & Legislative Coalition

## 1. The "Loss of Service" (LoS) Mandate
The core mission is to convert fragmented NYC Open Data (SODA) into a verified, quantified metric for housing justice.
- **Verification Rule:** A "two-unique-user" consensus window of 120 minutes ensures data integrity [cite: domain_logic/verification_engine.md].
- **The Metric:** LoS % = (Total Down Time / Total Period Time) * 100.
- **Heuristic:** Each verified "DOWN" report is assigned a 120-minute (2-hour) downtime block for calculation [cite: domain_logic/los_metrics.md].

## 2. Identified High-Priority "Hotspots"
Hotspot data comes from two complementary sources:
1. **City-wide SODA analysis** (`scripts/data_research/district_hotspots.py`): active codes `6S` and `6M`, covering 2025–2026. Used to identify top buildings per priority district for initial outreach framing.
2. **D17 database analysis** (full pipeline via `generate_district_reports --district 17`): 552 buildings analyzed against all-time SODA records using the **dual-window chronic filter** (1+ complaints in last 12 months AND 3+ over 3 years). 120 buildings qualified as chronic offenders as of April 24, 2026. Full results in `docs/advocacy/districts/district_17/district_17_data_snapshot.csv`.

⚠️ SODA community board assignments below are inferred from geography. Always confirm exact council district via geocoding before including in a briefing.

**D17 Top 5 (April 24, 2026 — database analysis):**

| Address | Complaints (12mo) | Complaints (3yr) |
| :--- | :--- | :--- |
| **601 East 156 St** | 8 | 24 |
| **303 East 158 St** | 7 | 26 |
| **1068 Franklin Ave** | 6 | 11 |
| **390 East 158 St** | 5 | 36 |
| **1090 Franklin Ave** | 5 | 12 |

**Cross-district hotspots (SODA city-wide analysis, 2025–2026):**

| Address | Borough | District | Council Member | Complaints (12mo) |
| :--- | :--- | :--- | :--- | :--- |
| **341 East 162 St** | Bronx | 16 (CB3) | **Althea Stevens** | 20 |
| **150 Lefferts Ave** | Brooklyn | 35 (CB9) | **Crystal Hudson** | 16 |
| **1150 Tiffany St** | Bronx | 17 (CB2) | **Justin Sanchez** | 12 |
| **2045 Story Ave** | Bronx | 18 (CB9) | **Amanda Farías** | 8 |
| **509 West 155 St** | Manhattan | 10 (CB12) | **Carmen De La Rosa** | 8 |
| **33 Saratoga Ave** | Brooklyn | 42 (CB16) | **Chris Banks** | 8 |

*Note: D14 (Pierina Ana Sanchez) and D26 (Shekar Krishnan) have been added to the priority district list. Run `district_hotspots.py --district pierina_sanchez` and `--district krishnan` for current SODA data. Full database analysis requires running `generate_district_reports` for those districts first.*

## 3. The Outreach Strategy
The strategy expanded from a single-district constituent approach to a multi-district coalition push:

- **Phase 1 (complete):** D17 pilot — Karl as Justin Sanchez’s constituent. Email sent 2026-04-17. Follow-up drafted 2026-04-24 with GitHub repo and CSV data snapshot links.
- **Phase 2 (ready to send):** Pierina Ana Sanchez (D14) — Housing & Buildings Committee Chair. Highest-leverage single contact in the Council. D17 is proof of concept; offer to run D14 analysis. Draft at `docs/advocacy/outreach/councilmember_pierina_sanchez_outreach.md`. *Prerequisite: run `generate_district_reports --district 14` first.*
- **Phase 3 (ready to send):** Shekar Krishnan (D26) — activated by MTA 7-train elevator demonstration (~April 21, 2026). Residential building angle is the complement, not the same fight. Draft at `docs/advocacy/outreach/councilmember_krishnan_outreach.md`. *Prerequisite: run `generate_district_reports --district 26` first.*
- **Coalition Goal:** Sanchez (D17) leads cross-borough Bronx Power Block; Pierina Sanchez (D14) provides committee-level anchor; Krishnan (D26) opens Queens flank.
- **Institutional Partners:** Strategic alignment with **CASA**, **Mothers on the Move (MOM)**, and **Mobilization for Justice (MFJ)**.

## 4. Technical Readiness & Next Steps
- **KB Alignment:** All core logic has been decomposed into the Knowledge Base. Specialists (Elias, Maya, Kiran) are mandated to follow the "Two-Hop Protocol."
- **Development Pivot:** Priority is now shifting to the **Member Dashboard** and **Automated Building Health Reports**.
- **Action Item:** Send the drafted outreach email to Justin Sanchez’s office.
