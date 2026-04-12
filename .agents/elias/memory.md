# Elias Memory Log - Auth & Superuser Final
- **Backend:** Switched from Basic/Session to **DRF Token Authentication** for stateless login.
- **Auth:** Implemented `login` and `logout` actions in `AuthViewSet`.
- **Identity-Agnostic Login:** Updated login logic to support both `username` and `email` resolution via `Q` objects.
- **Security:** Differentiated between "Invalid Credentials" (401) and "Inactive Account" (403) for better UX.
- **Superuser:** Fixed admin authentication by resetting credentials and verifying `is_active` status.
- **Migrations:** Applied `authtoken` migrations to the database.
