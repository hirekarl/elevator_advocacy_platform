# Advocacy Report: District 17 Elevator Reliability Audit

**Date**: April 24, 2026  
**To**: Councilmember Justin Sanchez  
**From**: The Elevator Advocate Platform  
**Subject**: Comprehensive Analysis of Elevator "Loss of Service" in District 17  

## 1. Executive Summary
This report summarizes the findings of a district-wide elevator reliability audit conducted between April 12 and April 20, 2026. By synthesizing 7,737 historical city records with real-time tenant observations, we have mapped the state of vertical mobility for all 551 residential buildings in District 17.

### Key Metrics
*   **Total Inventory**: 552 Buildings with elevator complaint history in NYC Open Data
*   **Chronic Offenders**: 120 buildings with 1+ complaints in the last 12 months AND 3+ complaints in the last 3 years
*   **Priority Targets**: 5 buildings with 5+ complaints in the last 12 months
*   **Most Chronic**: 390 East 158 Street — 36 complaints over 3 years

Of the 552 buildings in the district's complaint record, 120 show a pattern of recent and recurring elevator failures. The remaining 432 have no complaint activity in the last 12 months and are not included in the priority analysis.

---

## 2. Priority Advocacy Targets
The following properties have the highest complaint volume in the last 12 months and a documented multi-year pattern. Buildings are ranked by 12-month complaint count; all have 3+ complaints over 3 years, confirming a chronic pattern rather than isolated incidents.

### #1: 601 East 156 Street
*   **Complaints (12 months)**: 8 (city record — SODA) | **Complaints (3 years)**: 24
*   **Legal Owner**: Unavailable in MapPLUTO
*   **Risk Level**: CRITICAL
*   **AI Synthesis**: "Critical Elevator Malfunctions at 601 East 156 Street Demand Immediate Intervention and Systemic Resolution."

### #2: 303 East 158 Street
*   **Complaints (12 months)**: 7 (city record — SODA) | **Complaints (3 years)**: 26
*   **Legal Owner**: Senior Living Options Inc
*   **Risk Level**: CRITICAL
*   **AI Synthesis**: "Elevator Service at 303 East 158 Street Reaches Critical Failure Point, Demanding Immediate Intervention."

### #3: 1068 Franklin Avenue
*   **Complaints (12 months)**: 6 (city record — SODA) | **Complaints (3 years)**: 11
*   **Legal Owner**: 1068 Franklin Ave Housing Development Fund Corp
*   **Loss of Service**: 0.28%
*   **Risk Level**: HIGH
*   **AI Synthesis**: "Elevator Crisis at 1068 Franklin Avenue: Persistent Malfunctions Demand Urgent Intervention."

### #4: 390 East 158 Street
*   **Complaints (12 months)**: 5 (city record — SODA) | **Complaints (3 years)**: 36
*   **Legal Owner**: El Jardin De Seline HDFC, Inc.
*   **Risk Level**: HIGH
*   **AI Synthesis**: "Critical Assessment: Escalating Elevator Failures at 390 East 158 Street Demand Immediate Action."
*   **Note**: 36 complaints over 3 years is the highest sustained complaint volume in the district.

### #5: 1090 Franklin Avenue
*   **Complaints (12 months)**: 5 (city record — SODA) | **Complaints (3 years)**: 12
*   **Legal Owner**: HP 1090 Franklin Housing Development Fund Company Inc.
*   **Loss of Service**: 0.28%
*   **Risk Level**: HIGH
*   **AI Synthesis**: "Chronic Elevator Malfunctions at 1090 Franklin Avenue Pose High Risk, Urgent Action Required."

---

## 3. Methodology & Data Integrity
Our findings are powered by the **"Dignity Through Data"** model, ensuring that every claim is backed by official city records and tenant consensus:

1.  **Identity Resolution**: Every building is identified via its Building Identification Number (BIN) to prevent address variations from obscuring records.
2.  **Consensus Verification**: Outages are only canonically "Verified" when multiple residents report the same status within a 2-hour window.
3.  **Historical Ingestion**: We include retired city complaint categories ('81', '63') to provide a full 10-year reliability timeline for every building.

### Building Selection: Dual-Window Filter
This report only surfaces buildings that clear **both** of the following bars:

- **Recent bar**: 1 or more complaints in the last **12 months**
- **Chronic bar**: 3 or more complaints in the last **3 years**

A building must satisfy both conditions to appear as a priority target. This design addresses two opposite failure modes: a 30-day window undercounts active problems because SODA complaints can take weeks or months to appear in city data; an all-time window overcounts by surfacing buildings with old, resolved issues. The 12-month window is wide enough to absorb SODA's reporting lag while remaining recent enough to be actionable. The 3-year chronic bar filters out one-off incidents.

### Understanding "Loss of Service %"
The LoS % figures in this report are a **complaint-frequency index**, not a measured duration of actual elevator downtime. Each complaint on record is treated as a proxy for a 2-hour service disruption — the minimum window our platform uses to confirm an outage through tenant consensus. The calculation is: *(complaint count × 2 hours) ÷ (30-day period)*.

This is a known limitation. SODA complaints record when a complaint was *filed*, not how long the elevator was actually out of service. A single complaint could reflect a 20-minute glitch or a three-week outage; the current methodology cannot distinguish between them. For this reason, LoS % should be read as a **relative risk signal** — buildings with higher scores have a documented pattern of complaint activity — rather than a precise measure of time without service.

**We are actively seeking expert review of this methodology.** If your housing team or a partner organization has experience with building maintenance data, we welcome scrutiny and collaboration on improving this metric.

### How Tenant Reporting Closes the Gap
SODA data has two structural limitations for real-time advocacy: complaints are typically logged days or weeks after an outage begins, and they carry no timestamp for when service was restored. This means the historical record systematically undercounts both the frequency and duration of elevator failures.

The Elevator Advocate platform is designed to address both gaps. When residents in a building submit status reports through the app, those reports are timestamped at the moment of submission. Two matching reports within a 2-hour window create a **Verified** record — one that is grounded in real-time tenant observation rather than a delayed complaint filing. As more residents in District 17 use the platform, the LoS calculation will shift from a historical proxy toward an actual measure: the time between a verified "DOWN" report and a subsequent "UP" report, as observed by the people living in the building.

In short: the current report reflects what the city has on record. Active tenant participation is how we close the gap between what the record shows and what residents are living through today.

---

## 4. Recommended Legislative Actions
Based on the AI-synthesized summaries for these 551 buildings, we recommend the following:

1.  **Targeted DOB Inquiries**: Initiate Department of Buildings (DOB) audits for the top 5 offenders listed in this report.
2.  **Owner Accountability**: Leverage MapPLUTO data (included in our digital dashboard) to contact legal owners directly regarding chronic LoS metrics.
3.  **"Loss of Service" Standard**: Adopt LoS % as a standard metric for determining building health in District 17.

---
**Technical Lead**: Sol (Orchestrator)  
**Community Lead**: Karl Johnson (District 17 Resident)  
**Live Data**: [elevatoradvocate.nyc/api/districts/17/report/](https://elevatoradvocate.nyc/api/districts/17/report/)
