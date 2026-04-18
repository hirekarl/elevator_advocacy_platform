import { defineConfig, devices } from '@playwright/test';

/**
 * Demo recording config — separate from the accessibility test suite.
 *
 * Requires both servers running before you start:
 *   cd backend && uv run python manage.py runserver
 *   cd frontend && npm run dev
 *
 * Run with:
 *   npx playwright test --config=playwright.demo.config.ts
 *
 * Video files land in frontend/demo/recordings/.
 */
export default defineConfig({
  testDir: './demo',
  fullyParallel: false,
  retries: 0,
  workers: 1,
  reporter: [['dot']],
  use: {
    baseURL: 'http://localhost:5173',
    viewport: { width: 1920, height: 1080 },
    video: 'on',
    launchOptions: {
      slowMo: 40,
      headless: false,
    },
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  outputDir: './demo/recordings',
});
