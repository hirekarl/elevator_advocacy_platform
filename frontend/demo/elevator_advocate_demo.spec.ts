/**
 * ELEVATOR ADVOCATE — Live Demo Recording
 *
 * Building:  1853 Anthony Avenue, Bronx, NY
 * BIN:       2007566  (50 complaints — CRITICAL risk, heat wave narrative, District 15)
 *
 * Story:
 *   Martha lives on the 7th floor at 1853 Anthony Avenue in the Bronx.
 *   Last summer's heat wave made every elevator outage a health emergency.
 *   She opens Elevator Advocate to see the building's full complaint history
 *   before calling 311 — she needs hard dates to make her case.
 *
 * Requires both servers:
 *   cd backend && uv run python manage.py runserver
 *   cd frontend && npm run dev
 *
 * Run:
 *   npx playwright test --config=playwright.demo.config.ts
 */

import { test, expect, type Page } from '@playwright/test';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Smoothly scroll the page by `pixels` over approximately `ms` milliseconds. */
async function smoothScroll(page: Page, pixels: number, ms = 1200) {
  const steps = 30;
  const stepSize = pixels / steps;
  const delay = ms / steps;
  for (let i = 0; i < steps; i++) {
    await page.evaluate((dy: number) => window.scrollBy(0, dy), stepSize);
    await page.waitForTimeout(delay);
  }
}

/** Type into an input one character at a time for a natural typing feel. */
async function typeSlowly(page: Page, selector: string, text: string) {
  await page.locator(selector).click();
  await page.locator(selector).type(text, { delay: 80 });
}

// ---------------------------------------------------------------------------
// Demo
// ---------------------------------------------------------------------------

test('Elevator Advocate — full user demo', async ({ page }) => {
  test.slow(); // triple the default timeout for a deliberate demo pace

  // -------------------------------------------------------------------------
  // ACT 1 — Landing page
  // -------------------------------------------------------------------------

  await page.goto('/');
  await page.waitForSelector('.hero-section');

  // Pause on the hero so viewers can read it.
  await page.waitForTimeout(3000);

  // Scroll slowly past the tagline and into the first advocacy section.
  await smoothScroll(page, 500, 1500);
  await page.waitForTimeout(1500);

  // Continue down through the problem/solution sections.
  await smoothScroll(page, 700, 1800);
  await page.waitForTimeout(1500);

  await smoothScroll(page, 700, 1800);
  await page.waitForTimeout(2000);

  // -------------------------------------------------------------------------
  // ACT 2 — Fill in the search form (visual effect), then navigate by URL
  // -------------------------------------------------------------------------

  // Scroll back to the search form.
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'smooth' }));
  await page.waitForTimeout(1500);

  // Type the address deliberately so viewers see the search experience.
  await typeSlowly(page, '#search-house-number', '1853');
  await page.waitForTimeout(400);
  await typeSlowly(page, '#search-street', 'Anthony Avenue');
  await page.waitForTimeout(400);
  await page.locator('#search-borough').selectOption('Bronx');
  await page.waitForTimeout(1200);

  // Navigate directly to the building by URL — bypasses the geocoder entirely
  // and guarantees we land on BIN 2007566 regardless of API key state.
  await page.goto('/building/2007566');

  // -------------------------------------------------------------------------
  // ACT 3 — Building detail loads
  // -------------------------------------------------------------------------

  await page.waitForSelector('.building-action-center', { timeout: 15000 });

  // Pause on the status header.
  await page.waitForTimeout(3500);

  // Scroll past the quick-report buttons.
  await smoothScroll(page, 280, 1000);
  await page.waitForTimeout(1500);

  // -------------------------------------------------------------------------
  // ACT 4 — Building metrics
  // -------------------------------------------------------------------------

  await smoothScroll(page, 350, 1400);
  await page.waitForTimeout(2500);

  // -------------------------------------------------------------------------
  // ACT 5 — Executive summary (already cached — loads immediately)
  // -------------------------------------------------------------------------

  await smoothScroll(page, 400, 1400);
  await page.waitForTimeout(1000);

  try {
    await page.waitForSelector('text=AI Executive Summary', { timeout: 5000 });
    await page.waitForSelector('text=CRITICAL', { timeout: 10000 });
  } catch {
    // Degrade gracefully if summary is slow.
  }
  await page.waitForTimeout(3000);

  // -------------------------------------------------------------------------
  // ACT 6 — Complaint history
  // -------------------------------------------------------------------------

  await smoothScroll(page, 500, 1600);
  await page.waitForTimeout(1000);

  try {
    await page.waitForSelector('text=Complaint History', { timeout: 5000 });
  } catch { /* continue */ }

  await page.waitForTimeout(2500);

  // Expand to show all complaints.
  const showAll = page.locator('button', { hasText: /show all/i });
  if (await showAll.isVisible()) {
    await showAll.click();
    await page.waitForTimeout(2000);
  }

  // Scroll slowly through the full complaint list.
  await smoothScroll(page, 500, 2500);
  await page.waitForTimeout(2000);

  // -------------------------------------------------------------------------
  // ACT 7 — Advocacy center: 311 call button
  // -------------------------------------------------------------------------

  try {
    await page.waitForSelector('text=Advocacy Center', { timeout: 5000 });
    await page.locator('text=Advocacy Center').first().scrollIntoViewIfNeeded();
  } catch { /* continue */ }
  await page.waitForTimeout(2000);

  const call311 = page.locator('a[href="tel:311"]');
  if (await call311.isVisible()) {
    await call311.scrollIntoViewIfNeeded();
    await page.waitForTimeout(2500);
  }

  // -------------------------------------------------------------------------
  // ACT 8 — Advocacy script
  // -------------------------------------------------------------------------

  await smoothScroll(page, 300, 1000);
  await page.waitForTimeout(1000);

  try {
    await page.waitForSelector(
      'text=/Talking points|What to tell/i',
      { timeout: 8000 }
    );
  } catch { /* script may still be generating */ }

  await page.waitForTimeout(3000);

  // -------------------------------------------------------------------------
  // Closing hold
  // -------------------------------------------------------------------------

  await page.waitForTimeout(3000);

  await expect(page.locator('.building-action-center')).toBeVisible();
});
