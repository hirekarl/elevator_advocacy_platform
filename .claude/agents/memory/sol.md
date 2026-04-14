# Sol Memory Log - CI & Type-Safety Resolution (2026-04-13)

- **Strategy:** Conducted a full system-wide audit to resolve GitHub Actions CI failures.
- **Backend (Django 6.0):** 
    - Resolved 80+ Mypy errors. 
    - Mandatory: Use `django-stubs-ext.monkeypatch()` in `settings.py` to support runtime generics (e.g., `admin.ModelAdmin[Building]`).
    - Standardized return type annotations and explicit generic arguments in serializers and views.
    - Verified all backend tests (Pytest) and Ruff linting pass.
    - **CI Fix:** Renamed standalone test scripts (`test_soda.py`, `test_ai_orchestration.py`) to prevent `pytest` from incorrectly identifying them as unit tests, which was causing failures in credential-less CI environments.
- **Frontend (React 19):**
    - Cleared ESLint warnings in `BuildingDetail.tsx`.
    - Verified `tsc` and `vite build` pass.
- **Validation:** 
    - Full `pre_flight.sh` success in the backend.
    - 10/10 unit tests passed.
    - 3/3 Playwright tests passed in the frontend.
- **State:** The codebase is now structurally sound and CI-ready.
- **Key Lesson:** Django 6.0 and Mypy require `django-stubs` with runtime monkeypatching to handle modern generic patterns in `admin.py` and `views.py`. Ensure smoke tests/standalone scripts don't use `test_` prefix if they rely on external API keys not present in CI.
