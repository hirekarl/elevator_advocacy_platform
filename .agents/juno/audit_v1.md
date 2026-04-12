# UI/UX & Accessibility Audit Report (v1.0)
**Auditor:** Juno (UI/UX & Accessibility Specialist)
**Date:** 2025-03-24
**Scope:** `frontend/src/components/BuildingDetail.tsx`, `frontend/src/App.tsx`

---

## 1. Audit Findings

### BuildingDetail.tsx
- **Visual Feedback:** The use of `animate-pulse` for unverified status and pending reports aligns with the project's "Pulse amber icons" requirement. However, the `Badge` for `UNVERIFIED` uses `bg="warning"`, which often has low contrast against white or light backgrounds.
- **Empty States:** Excellent implementation of "intentional empty states" for reports and news articles, avoiding raw 0s as per `GEMINI.md`.
- **Interaction Debt:** Use of browser `alert()` for "Script copied" and "Data sync started" disrupts the user flow and feels dated.
- **Hardcoded URLs:** API endpoints are hardcoded to `localhost:8000`, which will fail in production.
- **Typography:** `opacity-75` is applied to white text in the Advocacy Center. This likely fails WCAG AA contrast requirements (4.5:1).

### App.tsx
- **Navigation UX:** The "Back to Search" button is functionally a `Button` but styled as a link. This is acceptable, but it lacks a keyboard shortcut or clear focus state in some browsers.
- **State Integrity:** The `useOptimistic` hook implementation for reports provides excellent "Syncing..." feedback.
- **Decorative Elements:** The building emoji (`🏢`) in the Navbar is treated as text, which might be read aloud by screen readers without context.

---

## 2. Plausible User Story Outcomes

- **The "High-Stress Tenant":** A user trying to report a broken elevator at 6:00 PM. They see the "Syncing..." state immediately after submitting, which reduces anxiety that the report didn't go through. *Outcome: Positive UX.*
- **The "Low-Vision Advocate":** A user using a screen reader to copy the 311 script. The "Copy Script" button does not announce what it is copying or that the copy was successful (due to the `alert`). *Outcome: Poor Accessibility.*
- **The "Home Searcher":** A user looking for their building. The "Set as Home Building" button provides clear utility, but the subsequent `alert` is jarring. *Outcome: Mixed UX.*

---

## 3. WCAG Gaps (Level AA)

- **1.1.1 Non-text Content (A):** Emojis (📢, ⚖️, 🏢) lack `role="img"` and `aria-label`.
- **1.4.3 Contrast (Minimum) (AA):** `text-muted` on `bg-light` and `opacity-75` on `text-white` fail the 4.5:1 ratio.
- **2.4.4 Link Purpose (In Context) (A):** "Read Article" links are repetitive. Screen reader users navigating by links will hear "Read Article" multiple times without knowing which article it refers to.
- **4.1.2 Name, Role, Value (A):** The "Refresh Media History" button doesn't indicate its loading state to screen readers while the background sync is occurring.

---

## 4. Actionable Recommendations

### For Maya (Frontend Specialist)
- **Accessibility Fix (ARIA):** 
  - Wrap emojis in `span` tags: `<span role="img" aria-label="Building Icon">🏢</span>`.
  - Update "Read Article" links: `<a href={article.url} aria-label={`Read article: ${article.title} (opens in new window)`} ...>`.
  - Add `aria-live="polite"` to the `Building Feed` container to announce new optimistic reports.
- **UX Fix (Feedback):** Replace all instances of `alert()` with a modern Toast notification system (e.g., `react-bootstrap/Toast` or `react-hot-toast`).
- **Contrast Fix:** Increase contrast for `text-muted` by moving from `#6c757d` to a slightly darker shade (e.g., `#595959`). Remove `opacity-75` from critical information text.
- **Refactor:** Extract the `http://localhost:8000` base URL into an environment variable (`VITE_API_URL`).

### For Elias (Backend Architect)
- **API Consistency:** Ensure all POST actions (like `refresh_news` or `set_primary_building`) return a structured `detail` message that the frontend can display in a Toast, rather than just a status code.
- **Consensus Metrics:** Provide a `verification_countdown` in the building detail payload so Maya can show "Verified in X mins" rather than just a generic "Unverified" pulse.

---
*End of Audit Report v1.0*
