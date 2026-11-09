"""Path resolution helpers for course modules, lessons, and local assets."""

from __future__ import annotations

from pathlib import Path


def get_repo_root() -> Path:
    """Return the absolute path to the repository root directory."""
    # src/course_utils/paths.py -> src/course_utils -> src -> repo_root
    return Path(__file__).resolve().parents[2]


def get_modules_dir() -> Path:
    """Return the absolute path to the top-level `modules/` directory."""
    return get_repo_root() / "modules"


def get_lesson_dir(notebook_file: str | Path) -> Path:
    """Return the directory containing the given notebook file (`__file__`)."""
    return Path(notebook_file).resolve().parent


def get_asset_path(
    notebook_file: str | Path,
    asset_name: str,
    *,
    must_exist: bool = True,
) -> Path:
    """Resolve an asset inside `<lesson_dir>/assets/<asset_name>`.

    Parameters
    ----------
    notebook_file:
        Pass `__file__` from inside a marimo notebook.
    asset_name:
        Relative file path inside the lesson's `assets/` directory.
    must_exist:
        If True (default), raises `FileNotFoundError` when the asset is missing.
    """
    lesson_dir = get_lesson_dir(notebook_file)
    asset_path = lesson_dir / "assets" / asset_name
    if must_exist and not asset_path.exists():
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found at expected path: {asset_path}"
        )
    return asset_path


def list_lessons() -> list[Path]:
    """Return a sorted list of all lesson `notebook.py` files under `modules/`."""
    modules_dir = get_modules_dir()
    if not modules_dir.exists():
        return []
    return sorted(modules_dir.glob("*/*/notebook.py"))
