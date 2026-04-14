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
