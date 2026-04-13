# Sprint 10: Martha Mode — Vulnerable User UX

**Status:** ✅ COMPLETED
**Date:** 2026-04-13
**Lead:** Sol (Orchestrator)
**Team:** Juno (Audit), Maya (Implementation), Blythe (Validation)
**North Star:** Martha — 70yo, walker, possible early-stage dementia, physically stranded if elevator is down.

---

## Post-Remediation Note
Initial implementation introduced 8 TypeScript errors (`TS2448`, `TS2454`) due to hook ordering. These were resolved via a remediation pass on 2026-04-13.

## Problem Statement

The app was audited from the perspective of Martha's three jobs when her elevator breaks:
1. Tell her neighbors
2. Call 311
3. Let her daughter know she's stranded

**Juno's Audit Findings:**

| # | Finding | Severity |
|---|---|---|
| 1 | Call 311 is buried in Zone 3 (Advocacy Center), below the fold | Critical |
| 2 | Tapping a report button while logged out shows a passive toast, not the auth modal — Martha gives up | Critical |
| 3 | Status banner is small-text, all-caps technical jargon ("VERIFICATION PENDING (47m)") | High |
| 4 | `opacity-75` on white text in advocacy section fails WCAG AA 4.5:1 contrast | High |
| 5 | Quick Report button labels use `small` CSS class — too small for low-vision users | Medium |
| 6 | Verification explainer speaks to advocates ("Two neighbors within 2 hours"), not Martha | Medium |
| 7 | No "alert a neighbor/daughter" shortcut when elevator is DOWN | Medium |
| 8 | No plain-language status headline for DOWN/TRAPPED/UNSAFE/UNVERIFIED states | High |

---

## Implementation Plan

### Maya: Frontend

- [x] Add `getStatusLabel()` helper — human-readable status in plain English/Spanish
- [x] Emergency block: when DOWN/TRAPPED/UNSAFE, show a high-contrast alert ABOVE Zone 1 with:
  - Large plain-language status ("Elevator is NOT WORKING")
  - Tap-to-call 311 button (full-width, large)
  - "Alert a Neighbor" SMS pre-populated link
- [x] UNVERIFIED block: when UNVERIFIED, show amber alert with plain-language neighbor prompt
- [x] Rewrite status ribbon: larger text, plain language, uses `getStatusLabel()`
- [x] `handleReport`: if not logged in, trigger `onShowAuth()` immediately (not passive toast)
- [x] Quick Report button labels: remove `small` class, use cleaner label text
- [x] Remove `opacity-75` from Call 311 section description spans
- [x] Update `verification_explainer` i18n string to plain English
- [x] **REMEDIATION**: Fix `useCallback` ordering in `App.tsx` and `BuildingDetail.tsx`

### Blythe: Validation

- [x] All new i18n keys present in both EN and ES
- [x] No `opacity-75` on critical information text
- [x] `npm run build` (TSC) pass
- [x] Pre-flight passes

---

## Success Criteria

1. A logged-out user clicking "Not Working" immediately sees the auth modal.
2. When a building's status is DOWN, the first thing visible (above all else) is a large Call 311 button.
3. The status ribbon text is in plain English, not technical codes.
4. Pre-flight (`./backend/scripts/pre_flight.sh`) passes 100%.
