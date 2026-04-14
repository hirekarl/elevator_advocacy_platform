#!/usr/bin/env bash
# exit on error
set -o errexit

# Install uv if not present
if ! command -v uv &> /dev/null
then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Clear Render's injected VIRTUAL_ENV so uv resolves the project's own .venv.
unset VIRTUAL_ENV

# Build the backend
cd backend
uv sync --frozen
uv run python manage.py collectstatic --no-input
uv run python manage.py migrate

# Seed initial user accounts if credentials are configured
if [ -n "$SEED_ADMIN_PASSWORD" ] && [ -n "$SEED_USER_PASSWORD" ]; then
    echo "Seeding initial user accounts..."
    uv run python manage.py seed_users
else
    echo "Skipping seed_users — SEED_ADMIN_PASSWORD or SEED_USER_PASSWORD not set."
fi
