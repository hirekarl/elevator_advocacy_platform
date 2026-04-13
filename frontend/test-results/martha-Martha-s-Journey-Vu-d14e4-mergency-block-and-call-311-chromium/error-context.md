# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: martha.spec.ts >> Martha's Journey (Vulnerable User UX) >> Scenario 1: Critical Outage (DOWN) - Should show emergency block and call 311
- Location: e2e\martha.spec.ts:23:3

# Error details

```
Error: expect(received).toEqual(expected) // deep equality

- Expected  -   1
+ Received  + 202

- Array []
+ Array [
+   Object {
+     "description": "Ensure the order of headings is semantically correct",
+     "help": "Heading levels should only increase by one",
+     "helpUrl": "https://dequeuniversity.com/rules/axe/4.11/heading-order?application=playwright",
+     "id": "heading-order",
+     "impact": "moderate",
+     "nodes": Array [
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": null,
+             "id": "heading-order",
+             "impact": "moderate",
+             "message": "Heading order invalid",
+             "relatedNodes": Array [],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Heading order invalid",
+         "html": "<h4 class=\"mb-4 fw-bold\">Sign In</h4>",
+         "impact": "moderate",
+         "none": Array [],
+         "target": Array [
+           "h4",
+         ],
+       },
+     ],
+     "tags": Array [
+       "cat.semantics",
+       "best-practice",
+     ],
+   },
+   Object {
+     "description": "Ensure every form element has a label",
+     "help": "Form elements must have labels",
+     "helpUrl": "https://dequeuniversity.com/rules/axe/4.11/label?application=playwright",
+     "id": "label",
+     "impact": "critical",
+     "nodes": Array [
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": null,
+             "id": "implicit-label",
+             "impact": "critical",
+             "message": "Element does not have an implicit (wrapped) <label>",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "explicit-label",
+             "impact": "critical",
+             "message": "Element does not have an explicit <label>",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "aria-label",
+             "impact": "critical",
+             "message": "aria-label attribute does not exist or is empty",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "aria-labelledby",
+             "impact": "critical",
+             "message": "aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": Object {
+               "messageKey": "noAttr",
+             },
+             "id": "non-empty-title",
+             "impact": "critical",
+             "message": "Element has no title attribute",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": Object {
+               "messageKey": "noAttr",
+             },
+             "id": "non-empty-placeholder",
+             "impact": "critical",
+             "message": "Element has no placeholder attribute",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "presentational-role",
+             "impact": "critical",
+             "message": "Element's default semantics were not overridden with role=\"none\" or role=\"presentation\"",
+             "relatedNodes": Array [],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Element does not have an implicit (wrapped) <label>
+   Element does not have an explicit <label>
+   aria-label attribute does not exist or is empty
+   aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
+   Element has no title attribute
+   Element has no placeholder attribute
+   Element's default semantics were not overridden with role=\"none\" or role=\"presentation\"",
+         "html": "<input required=\"\" class=\"form-control\" type=\"text\" value=\"\">",
+         "impact": "critical",
+         "none": Array [],
+         "target": Array [
+           "input[type=\"text\"]",
+         ],
+       },
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": null,
+             "id": "implicit-label",
+             "impact": "critical",
+             "message": "Element does not have an implicit (wrapped) <label>",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "explicit-label",
+             "impact": "critical",
+             "message": "Element does not have an explicit <label>",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "aria-label",
+             "impact": "critical",
+             "message": "aria-label attribute does not exist or is empty",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "aria-labelledby",
+             "impact": "critical",
+             "message": "aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": Object {
+               "messageKey": "noAttr",
+             },
+             "id": "non-empty-title",
+             "impact": "critical",
+             "message": "Element has no title attribute",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": Object {
+               "messageKey": "noAttr",
+             },
+             "id": "non-empty-placeholder",
+             "impact": "critical",
+             "message": "Element has no placeholder attribute",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "presentational-role",
+             "impact": "critical",
+             "message": "Element's default semantics were not overridden with role=\"none\" or role=\"presentation\"",
+             "relatedNodes": Array [],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Element does not have an implicit (wrapped) <label>
+   Element does not have an explicit <label>
+   aria-label attribute does not exist or is empty
+   aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
+   Element has no title attribute
+   Element has no placeholder attribute
+   Element's default semantics were not overridden with role=\"none\" or role=\"presentation\"",
+         "html": "<input required=\"\" class=\"form-control\" type=\"password\" value=\"\">",
+         "impact": "critical",
+         "none": Array [],
+         "target": Array [
+           "input[type=\"password\"]",
+         ],
+       },
+     ],
+     "tags": Array [
+       "cat.forms",
+       "wcag2a",
+       "wcag412",
+       "section508",
+       "section508.22.n",
+       "TTv5",
+       "TT5.c",
+       "EN-301-549",
+       "EN-9.4.1.2",
+       "ACT",
+       "RGAAv4",
+       "RGAA-11.1.1",
+     ],
+   },
+ ]
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner:
    - heading "Elevator Advocacy Platform" [level=1] [ref=e4]
  - link "Skip to main content" [ref=e5] [cursor=pointer]:
    - /url: "#main-content"
  - navigation "How to use Elevator Advocacy" [ref=e6]:
    - generic [ref=e7]:
      - link "Elevator Advocacy" [ref=e8] [cursor=pointer]:
        - /url: /
        - generic [ref=e9]: 🏢
        - text: Elevator Advocacy
      - generic [ref=e10]:
        - button "How to Use" [ref=e11] [cursor=pointer]: ❓ How to Use
        - button "toggle_language" [ref=e12] [cursor=pointer]: 🌐 ES
        - button "Log In" [ref=e13] [cursor=pointer]
  - main [ref=e14]:
    - generic [ref=e15]:
      - button "Find Your Building" [ref=e16] [cursor=pointer]:
        - generic [ref=e17]: ←
        - text: Find Your Building
      - generic [ref=e18]:
        - generic [ref=e20]:
          - alert [ref=e21]:
            - heading "Elevator is NOT WORKING" [level=2] [ref=e22]
            - paragraph [ref=e23]: Use the buttons below to call for help or alert someone who can assist you.
            - link "Call 311 Now — 212-639-9675" [ref=e24] [cursor=pointer]:
              - /url: tel:311
              - text: 📞Call 311 Now — 212-639-9675
            - link "Send Text Alert to a Neighbor" [ref=e25] [cursor=pointer]:
              - /url: sms:?body=123%20MARTHA%20ST%3A%20The%20elevator%20at%20this%20building%20may%20not%20be%20working.%20Can%20you%20check%20on%20your%20neighbor%20or%20call%20311%3F
              - text: 💬Send Text Alert to a Neighbor
          - generic [ref=e26]:
            - status [ref=e27]:
              - generic [ref=e28]: Elevator is NOT WORKING
            - generic [ref=e29]:
              - generic [ref=e31]:
                - heading "123 MARTHA ST" [level=2] [ref=e32]
                - paragraph [ref=e33]: Manhattan • BIN 1234567
              - generic [ref=e34]:
                - heading "Is the elevator working right now?" [level=2] [ref=e35]
                - generic [ref=e36]:
                  - button "Back in Service / Working" [ref=e38] [cursor=pointer]:
                    - generic [ref=e40]: ✅
                    - generic [ref=e41]: Working
                  - button "Out of Service / Inoperative" [ref=e43] [cursor=pointer]:
                    - generic [ref=e45]: ❌
                    - generic [ref=e46]: Not Working
                  - button "Slow or Faulty Operation" [ref=e48] [cursor=pointer]:
                    - generic [ref=e50]: ⚠️
                    - generic [ref=e51]: Moving Slowly
                - paragraph [ref=e52]: Tap a button above to tell your neighbors what you see at the elevator. This helps track real-time service for everyone.
                - paragraph [ref=e53]: Reports from two different neighbors within 2 hours confirm the status.
                - generic [ref=e54]:
                  - heading "Emergency Reports" [level=3] [ref=e55]: 🚨 Emergency Reports
                  - generic [ref=e56]:
                    - button "Entrapment (People inside)" [ref=e58] [cursor=pointer]:
                      - generic [ref=e59]: 🆘
                      - generic [ref=e60]: People Trapped Inside
                    - button "Unsafe (Doors/Leveling)" [ref=e62] [cursor=pointer]:
                      - generic [ref=e63]: ⚠️
                      - generic [ref=e64]: Unsafe Conditions
                  - paragraph [ref=e65]: Only use for active emergencies. These reports are flagged as urgent.
                - generic [ref=e66]:
                  - generic [ref=e67]: Sign in to submit a report and help your neighbors.
                  - button "Sign In" [ref=e68] [cursor=pointer]
          - generic [ref=e69]:
            - generic [ref=e71]:
              - heading "Loss of Service (30 Days)" [level=2] [ref=e72]
              - generic [ref=e73]:
                - generic [ref=e74]: 85%
                - generic [ref=e75]: Uptime (30d)
              - progressbar "123 MARTHA ST" [ref=e77]
            - generic [ref=e79]:
              - heading "Maintenance Forecast" [level=2] [ref=e80]
              - generic [ref=e81]:
                - generic [ref=e82]: 85%
                - generic [ref=e83]: Risk Level
              - progressbar "123 MARTHA ST" [ref=e85]
          - generic [ref=e86]:
            - heading "AI Executive Summary" [level=2] [ref=e88]: 🧠 AI Executive Summary
            - generic [ref=e90]:
              - status "Synthesizing worker reports..." [ref=e91]
              - paragraph [ref=e92]: Synthesizing worker reports...
          - heading "Advocacy Center" [level=2] [ref=e93]:
            - generic [ref=e94]: 📢
            - text: Advocacy Center
          - link "Call 311 Now — 212-639-9675" [ref=e95] [cursor=pointer]:
            - /url: tel:311
            - generic [ref=e96]:
              - generic [ref=e97]: 📞 Call 311 Now
              - text: Free NYC helpline — available 24/7
            - generic [ref=e98]:
              - generic [ref=e99]: 212-639-9675
              - text: or dial 311
          - generic [ref=e102]:
            - status "Generating custom advocacy strategy..." [ref=e103]
            - generic [ref=e104]: Generating custom advocacy strategy...
          - generic [ref=e105]:
            - heading "Advocacy Paper Trail" [level=2] [ref=e107]: 📜 Advocacy Paper Trail
            - generic [ref=e109]:
              - generic [ref=e110]:
                - heading "My Personal Trail" [level=3] [ref=e111]
                - alert [ref=e112]: No personal logs. Tap + to add a 311 SR#.
              - generic [ref=e113]:
                - heading "Tenant Community Reports" [level=3] [ref=e114]
                - generic [ref=e116]: No community reports.
              - generic [ref=e117]:
                - heading "Official DOB History" [level=3] [ref=e118]
                - generic [ref=e120]: No official DOB data.
          - generic [ref=e123]:
            - generic [ref=e124]:
              - heading "Help Your Neighbors Advocate" [level=2] [ref=e125]
              - paragraph [ref=e126]: Provide hard data to elected officials or building management to demand better service.
            - generic [ref=e127]:
              - button "Copy Summary" [ref=e128] [cursor=pointer]
              - generic [ref=e129]:
                - link "Share building status via WhatsApp" [ref=e130] [cursor=pointer]:
                  - /url: https://wa.me/?text=Elevator%20Advocacy%20Report%3A%20123%20MARTHA%20ST%0A-%2030-Day%20Service%20Loss%3A%2015%25%0A-%20Current%20Status%3A%20DOWN
                  - text: Share via WhatsApp
                - link "Email building status to a representative" [ref=e131] [cursor=pointer]:
                  - /url: mailto:?subject=Elevator%20Issue%3A%20123%20MARTHA%20ST&body=Elevator%20Advocacy%20Report%3A%20123%20MARTHA%20ST%0A-%2030-Day%20Service%20Loss%3A%2015%25%0A-%20Current%20Status%3A%20DOWN
                  - text: Email Representative
          - generic [ref=e132]:
            - heading "Public Media & Local News" [level=2] [ref=e133]: 📰 Public Media & Local News
            - button "Refresh Public Media & Local News" [ref=e134] [cursor=pointer]: Refresh
          - alert [ref=e137]: No media mentions found.
        - generic [ref=e139]:
          - generic [ref=e141]:
            - heading "Sign In" [level=4] [ref=e142]
            - generic [ref=e143]:
              - generic [ref=e144]:
                - generic [ref=e145]: Username
                - textbox [ref=e146]
              - generic [ref=e147]:
                - generic [ref=e148]: Password
                - textbox [ref=e149]
              - button "Log In" [ref=e150] [cursor=pointer]
              - button "Don't have an account? Sign up" [ref=e152] [cursor=pointer]
          - generic [ref=e153]:
            - heading "Building Feed" [level=5] [ref=e154]
            - alert [ref=e155]: No recent tenant activity.
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | import AxeBuilder from '@axe-core/playwright';
  3   | 
  4   | const MOCK_BIN = '1234567';
  5   | const BASE_API_URL = 'http://localhost:8000/api';
  6   | 
  7   | test.describe("Martha's Journey (Vulnerable User UX)", () => {
  8   | 
  9   |   // Force mobile viewport to ensure consistent layout and that BuildingDetail is visible
  10  |   // rather than being pushed aside by Auth forms on large screens.
  11  |   test.use({ viewport: { width: 375, height: 667 } });
  12  | 
  13  |   // Global mocks for every test to avoid hanging on non-critical API calls
  14  |   test.beforeEach(async ({ page }) => {
  15  |     await page.route(`${BASE_API_URL}/buildings/${MOCK_BIN}/advocacy_script/`, async route => {
  16  |       await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ headline: 'Mock Script', script: 'Mock content', legal_reference: 'Mock law' }) });
  17  |     });
  18  |     await page.route(`${BASE_API_URL}/buildings/${MOCK_BIN}/advocacy_summary/`, async route => {
  19  |       await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ risk_level: 'Low', historical_patterns: 'Mock history', community_sentiment: 'Mock sentiment', legal_standing: 'Mock legal', recommended_action: 'Mock action', confidence_score: 0.9 }) });
  20  |     });
  21  |   });
  22  | 
  23  |   test('Scenario 1: Critical Outage (DOWN) - Should show emergency block and call 311', async ({ page }) => {
  24  |     // Mock the building API response for a DOWN status
  25  |     await page.route(`${BASE_API_URL}/buildings/${MOCK_BIN}/`, async route => {
  26  |       await route.fulfill({
  27  |         status: 200,
  28  |         contentType: 'application/json',
  29  |         body: JSON.stringify({
  30  |           bin: MOCK_BIN,
  31  |           address: '123 MARTHA ST',
  32  |           borough: 'Manhattan',
  33  |           verified_status: 'DOWN',
  34  |           recent_reports: [],
  35  |           loss_of_service_30d: 15,
  36  |           failure_risk: { risk_score: 85 }
  37  |         }),
  38  |       });
  39  |     });
  40  | 
  41  |     // Go to the building detail page
  42  |     await page.goto(`/building/${MOCK_BIN}`);
  43  | 
  44  |     // Martha should see the "NOT WORKING" alert block immediately
  45  |     const emergencyBlock = page.getByRole('alert').filter({ hasText: 'Elevator is NOT WORKING' });
  46  |     await expect(emergencyBlock).toBeVisible();
  47  | 
  48  |     // Accessibility Audit for the emergency state
  49  |     // Focus on the main content area to avoid violations in hidden modals or auth forms
  50  |     const accessibilityScanResults = await new AxeBuilder({ page })
  51  |       .include('#main-content')
  52  |       .analyze();
> 53  |     expect(accessibilityScanResults.violations).toEqual([]);
      |                                                 ^ Error: expect(received).toEqual(expected) // deep equality
  54  | 
  55  |     // She should see the "Call 311 Now" button clearly
  56  |     // Use first() to get the one in the emergency block
  57  |     const call311Button = page.getByRole('link', { name: /Call 311 Now/i }).first();
  58  |     await expect(call311Button).toBeVisible();
  59  |     await expect(call311Button).toHaveAttribute('href', 'tel:311');
  60  | 
  61  |     // She should see the "Alert a Neighbor" button
  62  |     const alertNeighborButton = page.getByRole('link', { name: /Send Text Alert to a Neighbor/i });
  63  |     await expect(alertNeighborButton).toBeVisible();
  64  |     await expect(alertNeighborButton).toHaveAttribute('href', /sms:/);
  65  |   });
  66  | 
  67  |   test('Scenario 2: Auth Friction - Clicking "Not Working" while logged out should trigger auth modal', async ({ page }) => {
  68  |     // Mock the building API response for an UP status
  69  |     await page.route(`${BASE_API_URL}/buildings/${MOCK_BIN}/`, async route => {
  70  |       await route.fulfill({
  71  |         status: 200,
  72  |         contentType: 'application/json',
  73  |         body: JSON.stringify({
  74  |           bin: MOCK_BIN,
  75  |           address: '123 MARTHA ST',
  76  |           borough: 'Manhattan',
  77  |           verified_status: 'UP',
  78  |           recent_reports: []
  79  |         }),
  80  |       });
  81  |     });
  82  | 
  83  |     // Ensure we are logged out (clear localStorage)
  84  |     await page.addInitScript(() => {
  85  |       window.localStorage.clear();
  86  |     });
  87  | 
  88  |     await page.goto(`/building/${MOCK_BIN}`);
  89  |     await page.waitForLoadState('networkidle');
  90  | 
  91  |     // Martha tries to report the elevator is "Not Working"
  92  |     // Using a more robust selector that doesn't rely on strict role name matching
  93  |     // which was failing due to rendering artifacts like the "<" in the debug output.
  94  |     const reportButton = page.locator('button', { hasText: 'Not Working' });
  95  |     await expect(reportButton).toBeVisible();
  96  |     await reportButton.click();
  97  | 
  98  |     // The Auth Modal should pop up immediately
  99  |     const authModal = page.getByRole('dialog', { name: /Sign in or create account/i });
  100 |     await expect(authModal).toBeVisible();
  101 |     
  102 |     const authHeading = authModal.getByRole('heading', { name: /Sign In/i });
  103 |     await expect(authHeading).toBeVisible();
  104 |     
  105 |     // Ensure no passive toast is shown
  106 |     const toast = page.locator('.toast');
  107 |     await expect(toast).not.toBeVisible();
  108 |   });
  109 | 
  110 |   test('Scenario 3: Unverified Status - Should show neighbor verification prompt', async ({ page }) => {
  111 |     // Mock the building API response for an UNVERIFIED status
  112 |     await page.route(`${BASE_API_URL}/buildings/${MOCK_BIN}/`, async route => {
  113 |       await route.fulfill({
  114 |         status: 200,
  115 |         contentType: 'application/json',
  116 |         body: JSON.stringify({
  117 |           bin: MOCK_BIN,
  118 |           address: '123 MARTHA ST',
  119 |           borough: 'Manhattan',
  120 |           verified_status: 'UNVERIFIED',
  121 |           recent_reports: []
  122 |         }),
  123 |       });
  124 |     });
  125 | 
  126 |     await page.goto(`/building/${MOCK_BIN}`);
  127 | 
  128 |     // Martha should see the warning alert
  129 |     const unverifiedAlert = page.locator('.alert-warning', { hasText: 'Elevator Status Not Yet Confirmed' });
  130 |     await expect(unverifiedAlert).toBeVisible();
  131 |     await expect(unverifiedAlert).toContainText('One neighbor has reported this');
  132 |   });
  133 | 
  134 | });
  135 | 
```