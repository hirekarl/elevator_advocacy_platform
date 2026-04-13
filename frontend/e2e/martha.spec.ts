import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const MOCK_BIN = '1234567';
const BASE_API_URL = 'http://localhost:8000/api';

test.describe("Martha's Journey (Vulnerable User UX)", () => {

  // Force mobile viewport to ensure consistent layout and that BuildingDetail is visible
  // rather than being pushed aside by Auth forms on large screens.
  test.use({ viewport: { width: 375, height: 667 } });

  // Global mocks for every test to avoid hanging on non-critical API calls
  test.beforeEach(async ({ page }) => {
    await page.route(`${BASE_API_URL}/buildings/${MOCK_BIN}/advocacy_script/`, async route => {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ headline: 'Mock Script', script: 'Mock content', legal_reference: 'Mock law' }) });
    });
    await page.route(`${BASE_API_URL}/buildings/${MOCK_BIN}/advocacy_summary/`, async route => {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ risk_level: 'Low', historical_patterns: 'Mock history', community_sentiment: 'Mock sentiment', legal_standing: 'Mock legal', recommended_action: 'Mock action', confidence_score: 0.9 }) });
    });
  });

  test('Scenario 1: Critical Outage (DOWN) - Should show emergency block and call 311', async ({ page }) => {
    // Mock the building API response for a DOWN status
    await page.route(`${BASE_API_URL}/buildings/${MOCK_BIN}/`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          bin: MOCK_BIN,
          address: '123 MARTHA ST',
          borough: 'Manhattan',
          verified_status: 'DOWN',
          recent_reports: [],
          loss_of_service_30d: 15,
          failure_risk: { risk_score: 85 }
        }),
      });
    });

    // Go to the building detail page
    await page.goto(`/building/${MOCK_BIN}`);

    // Martha should see the "NOT WORKING" alert block immediately
    const emergencyBlock = page.getByRole('alert').filter({ hasText: 'Elevator is NOT WORKING' });
    await expect(emergencyBlock).toBeVisible();

    // Accessibility Audit for the emergency state
    // Focus on the main content area to avoid violations in hidden modals or auth forms
    const accessibilityScanResults = await new AxeBuilder({ page })
      .include('#main-content')
      .analyze();
    expect(accessibilityScanResults.violations).toEqual([]);

    // She should see the "Call 311 Now" button clearly
    // Use first() to get the one in the emergency block
    const call311Button = page.getByRole('link', { name: /Call 311 Now/i }).first();
    await expect(call311Button).toBeVisible();
    await expect(call311Button).toHaveAttribute('href', 'tel:311');

    // She should see the "Alert a Neighbor" button
    const alertNeighborButton = page.getByRole('link', { name: /Send Text Alert to a Neighbor/i });
    await expect(alertNeighborButton).toBeVisible();
    await expect(alertNeighborButton).toHaveAttribute('href', /sms:/);
  });

  test('Scenario 2: Auth Friction - Clicking "Not Working" while logged out should trigger auth modal', async ({ page }) => {
    // Mock the building API response for an UP status
    await page.route(`${BASE_API_URL}/buildings/${MOCK_BIN}/`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          bin: MOCK_BIN,
          address: '123 MARTHA ST',
          borough: 'Manhattan',
          verified_status: 'UP',
          recent_reports: []
        }),
      });
    });

    // Ensure we are logged out (clear localStorage)
    await page.addInitScript(() => {
      window.localStorage.clear();
    });

    await page.goto(`/building/${MOCK_BIN}`);
    await page.waitForLoadState('networkidle');

    // Martha tries to report the elevator is "Not Working"
    // Using a more robust selector that doesn't rely on strict role name matching
    // which was failing due to rendering artifacts like the "<" in the debug output.
    const reportButton = page.locator('button', { hasText: 'Not Working' });
    await expect(reportButton).toBeVisible();
    await reportButton.click();

    // The Auth Modal should pop up immediately
    const authModal = page.getByRole('dialog', { name: /Sign in or create account/i });
    await expect(authModal).toBeVisible();
    
    const authHeading = authModal.getByRole('heading', { name: /Sign In/i });
    await expect(authHeading).toBeVisible();
    
    // Ensure no passive toast is shown
    const toast = page.locator('.toast');
    await expect(toast).not.toBeVisible();
  });

  test('Scenario 3: Unverified Status - Should show neighbor verification prompt', async ({ page }) => {
    // Mock the building API response for an UNVERIFIED status
    await page.route(`${BASE_API_URL}/buildings/${MOCK_BIN}/`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          bin: MOCK_BIN,
          address: '123 MARTHA ST',
          borough: 'Manhattan',
          verified_status: 'UNVERIFIED',
          recent_reports: []
        }),
      });
    });

    await page.goto(`/building/${MOCK_BIN}`);

    // Martha should see the warning alert
    const unverifiedAlert = page.locator('.alert-warning', { hasText: 'Elevator Status Not Yet Confirmed' });
    await expect(unverifiedAlert).toBeVisible();
    await expect(unverifiedAlert).toContainText('One neighbor has reported this');
  });

});
