# Sprint 11: Martha's Journey — Playwright E2E Tests

**Status:** 🏗️ IN PROGRESS
**Date:** 2026-04-13
**Lead:** Sol (Orchestrator)
**Team:** Juno (Audit), Maya (Implementation), Blythe (Validation), Aris (Archivist)
**North Star:** Martha's experience must be verifiable and regression-proof.

---

## Objectives

1. **Verify Critical Outage Flow**: Ensure the "Emergency Block" (Call 311 / Alert Neighbor) is the first thing Martha sees when an elevator is DOWN.
2. **Verify Auth Friction**: Ensure clicking "Not Working" while logged out immediately triggers the auth modal.
3. **Verify Plain Language**: Ensure status labels are human-readable (e.g., "NOT WORKING" instead of "DOWN").
4. **Accessibility Audit**: Use Playwright's accessibility tools to confirm WCAG 2.2 compliance for the Martha Mode components.

## Scenarios (Martha's Journey)

### Scenario 1: The Stranded Resident (Critical Outage)
- **Goal**: Report an outage and get help.
- **Flow**: 
  1. Martha navigates to her building page.
  2. The API returns status `DOWN`.
  3. Martha sees the large red "NOT WORKING" alert block at the top.
  4. Martha sees the "Call 311 Now" button.
  5. Martha sees the "Alert a Neighbor" SMS link.

### Scenario 2: The Good Neighbor (Logged-out Reporting)
- **Goal**: Report a new outage.
- **Flow**:
  1. Martha (logged out) navigates to her building page.
  2. Martha clicks the "Not Working" button in the Quick Report section.
  3. **Assertion**: The Login/Signup modal appears immediately.
  4. **Assertion**: No passive toast was shown instead of the modal.

### Scenario 3: The Skeptic (Unverified Status)
- **Goal**: Verify a neighbor's report.
- **Flow**:
  1. Martha navigates to a building with status `UNVERIFIED`.
  2. Martha sees the amber "Waiting for verification" alert.
  3. Martha sees the plain-language prompt to verify.

---

## Implementation Plan

### Maya: Frontend (Playwright)
- [ ] Install Playwright in `frontend/`.
- [ ] Configure `playwright.config.ts` for Vite dev server.
- [ ] Implement `e2e/martha.spec.ts` with mocked API responses.
- [ ] Integrate `@axe-core/playwright` for accessibility checks.

### Juno: UX & Accessibility
- [ ] Review test assertions for "Martha-friendliness" (e.g., button sizes, contrast).

### Blythe: Quality & Standards
- [ ] Ensure tests use semantic roles and data-testid where necessary.
- [ ] Confirm no "AI smell" in test descriptions.

---

## Success Criteria
1. All three Martha scenarios pass in headless mode.
2. Accessibility audit passes for the Building Detail page in various states (UP/DOWN/UNVERIFIED).
3. `npm run test:e2e` command added to `frontend/package.json`.
