#!/usr/bin/env bash
# ==============================================================================
# Course Environment Setup Script (macOS & Linux)
# Does NOT require Python to be pre-installed. Bootstraps uv, installs a
# managed Python 3.12 runtime, creates .venv, and installs all dependencies.
# ==============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

PYTHON_VERSION="3.12"

echo "============================================================"
echo "  Course Lab Environment Setup (macOS / Linux)"
echo "============================================================"

# 1. Ensure common user binary paths are on PATH
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

# 2. Check for uv; install if missing
if ! command -v uv >/dev/null 2>&1; then
    echo "[1/4] 'uv' not found. Installing uv..."
    if command -v curl >/dev/null 2>&1; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif command -v wget >/dev/null 2>&1; then
        wget -qO- https://astral.sh/uv/install.sh | sh
    else
        echo "Error: Neither 'curl' nor 'wget' is installed. Please install curl or wget and re-run." >&2
        exit 1
    fi
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
else
    echo "[1/4] Found uv: $(uv --version)"
fi

# Verify uv is now callable
if ! command -v uv >/dev/null 2>&1; then
    echo "Error: uv installation succeeded, but 'uv' could not be found on PATH." >&2
    exit 1
fi

# 3. Install managed Python 3.12 via uv (no system Python required)
echo "[2/4] Ensuring Python ${PYTHON_VERSION} is installed via uv..."
uv python install "${PYTHON_VERSION}"

# 4. Create .venv and sync dependencies from pyproject.toml
echo "[3/4] Creating .venv and syncing course dependencies..."
uv sync --python "${PYTHON_VERSION}"

# 5. Create local .env from .env.example if not already present
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  -> Created local .env from .env.example"
fi

# 6. Verify installation
echo "[4/4] Verifying marimo and course_utils installation..."
MARIMO_VER="$(uv run marimo --version)"
uv run python -c "import course_utils; print(f'  -> course_utils loaded from: {course_utils.__file__}')"
echo "  -> marimo version: ${MARIMO_VER}"

echo ""
echo "============================================================"
echo "  Setup Complete!"
echo "============================================================"
echo "Next steps:"
echo "  • List all lessons:       uv run lab --list"
echo "  • Interactive launcher:   uv run lab"
echo "  • Open a lesson directly: uv run lab 00_welcome"
echo "  • Browse modules in UI:   uv run marimo edit modules"
echo "============================================================"
