# Elias Memory Log - Auth Sprint Final
- **Backend:** Switched from Basic/Session to **DRF Token Authentication** for stateless login.
- **Auth:** Implemented `login` and `logout` actions in `AuthViewSet`.
- **Security:** Differentiated between "Invalid Credentials" (401) and "Inactive Account" (403) for better UX.
- **Migrations:** Applied `authtoken` migrations to the database.
- **Verification:** Confirmed auth lifecycle (Signup -> Confirm -> Login -> Logout) via `verify_auth.py`.
