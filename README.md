# Interactive Course Labs & Workshops

Welcome! This repository contains the hands-on labs and interactive workshops for the course, powered by **[marimo](https://marimo.io/)** reactive Python notebooks and **[uv](https://docs.astral.sh/uv/)** for fast, reproducible environment management.

---

## Quickstart (1-Step Setup)

You do **not** need Python pre-installed on your computer. The setup script for your operating system will automatically install `uv`, download an isolated Python 3.12 runtime, create a local `.venv` virtual environment, and install all course packages.

### macOS & Linux

Open a terminal in the repository root and run:

```bash
./setup.sh
```

### Windows (PowerShell or Command Prompt)

In **PowerShell**, run:

```powershell
.\setup.ps1
```

Or in **Command Prompt** (or by double-clicking in File Explorer):

```cmd
setup.bat
```

---

## Launching Labs

Once setup completes, use `uv run lab` from the repository root to discover and open lessons:

| Action | Command |
| :--- | :--- |
| **Interactive lesson picker** | `uv run lab` |
| **List all available lessons** | `uv run lab --list` |
| **Open a specific lesson by name or number** | `uv run lab 00_welcome` or `uv run lab 1` |
| **Open a lesson in read-only App mode** | `uv run lab 00_welcome --run` |
| **Open the marimo file browser across all modules** | `uv run lab --browse` (or `uv run marimo edit modules`) |

---

## Repository Structure

```text
.
├── pyproject.toml               # Top-level course dependencies & configuration
├── setup.sh                     # macOS / Linux zero-prerequisite setup script
├── setup.ps1                    # Windows PowerShell zero-prerequisite setup script
├── setup.bat                    # Windows CMD / double-click wrapper for setup.ps1
├── src/
│   └── course_utils/            # Shared helper package importable in all notebooks
│       ├── __init__.py
│       ├── paths.py             # get_asset_path(__file__, ...) and path utilities
│       └── cli.py               # Powers the `uv run lab` launcher
└── modules/                     # Course modules and hands-on lessons
    ├── README.md                # Instructor guide for adding new modules/lessons
    └── 00_welcome/
        └── lesson_01_intro/
            ├── README.md
            ├── notebook.py      # Interactive marimo notebook
            └── assets/          # Lesson-specific datasets and media
                └── sample_dataset.csv
```

---

## Updating Your Environment

If the instructor adds new packages or modules during the course, pull the latest changes and re-run the setup script (or run `uv sync`):

```bash
uv sync
```
