# ==============================================================================
# Course Environment Setup Script (Windows PowerShell)
# Does NOT require Python to be pre-installed. Bootstraps uv, installs a
# managed Python 3.12 runtime, creates .venv, and installs all dependencies.
# ==============================================================================
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $RepoRoot

$PythonVersion = "3.12"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Course Lab Environment Setup (Windows)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Ensure user-local uv install locations are in PATH for this session
$UserBinPaths = @(
    "$env:USERPROFILE\.local\bin",
    "$env:USERPROFILE\.cargo\bin"
)
foreach ($BinPath in $UserBinPaths) {
    if ((Test-Path $BinPath) -and ($env:Path -notlike "*$BinPath*")) {
        $env:Path = "$BinPath;$env:Path"
    }
}

# 2. Check for uv; install if missing
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[1/4] 'uv' not found. Installing uv..." -ForegroundColor Yellow
    powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"

    foreach ($BinPath in $UserBinPaths) {
        if ((Test-Path $BinPath) -and ($env:Path -notlike "*$BinPath*")) {
            $env:Path = "$BinPath;$env:Path"
        }
    }
} else {
    $UvVer = & uv --version
    Write-Host "[1/4] Found uv: $UvVer" -ForegroundColor Green
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Error "uv installation finished, but 'uv' was not found on PATH. Please restart your terminal and try again."
    exit 1
}

# 3. Install managed Python 3.12 via uv (no system Python required)
Write-Host "[2/4] Ensuring Python $PythonVersion is installed via uv..." -ForegroundColor Yellow
& uv python install $PythonVersion
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 4. Create .venv and sync dependencies from pyproject.toml
Write-Host "[3/4] Creating .venv and syncing course dependencies..." -ForegroundColor Yellow
& uv sync --python $PythonVersion
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 5. Create local .env from .env.example if not already present
if ((Test-Path ".env.example") -and (-not (Test-Path ".env"))) {
    Copy-Item ".env.example" ".env"
    Write-Host "  -> Created local .env from .env.example" -ForegroundColor Green
}

# 6. Verify installation
Write-Host "[4/4] Verifying marimo and course_utils installation..." -ForegroundColor Yellow
$MarimoVer = & uv run marimo --version
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& uv run python -c "import course_utils; print(f'  -> course_utils loaded from: {course_utils.__file__}')"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "  -> marimo version: $MarimoVer" -ForegroundColor Green
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Next steps:"
Write-Host "  * List all lessons:       uv run lab --list"
Write-Host "  * Interactive launcher:   uv run lab"
Write-Host "  * Open a lesson directly: uv run lab 00_welcome"
Write-Host "  * Browse modules in UI:   uv run marimo edit modules"
Write-Host "============================================================" -ForegroundColor Cyan
