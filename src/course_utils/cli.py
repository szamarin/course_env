"""CLI helper (`uv run lab`) for discovering and launching course marimo notebooks."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from course_utils.paths import get_modules_dir, get_repo_root, list_lessons


def _format_lesson_label(notebook_path: Path) -> str:
    """Format `modules/<module>/<lesson>/notebook.py` as `<module>/<lesson>`."""
    modules_dir = get_modules_dir()
    try:
        rel = notebook_path.relative_to(modules_dir)
        return str(rel.parent.as_posix())
    except ValueError:
        return str(notebook_path)


def _print_lessons(lessons: list[Path]) -> None:
    if not lessons:
        print("No lessons found under modules/*/*/notebook.py.")
        return

    print("\nAvailable Course Labs:")
    print("-" * 60)
    for idx, nb in enumerate(lessons, start=1):
        label = _format_lesson_label(nb)
        print(f"  [{idx}] {label:<38} ({nb.relative_to(get_repo_root())})")
    print("-" * 60)


def _launch_marimo(target: Path, *, run_mode: bool = False) -> int:
    subcommand = "run" if run_mode else "edit"
    cmd = [sys.executable, "-m", "marimo", subcommand, str(target)]
    print(f"Launching: marimo {subcommand} {target.relative_to(get_repo_root())}")
    return subprocess.call(cmd, cwd=get_repo_root())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="lab",
        description="Discover and launch interactive marimo course labs.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="Optional lesson number (e.g. '1') or substring filter (e.g. '00_welcome' or 'intro').",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all available modules and lessons and exit.",
    )
    parser.add_argument(
        "-r",
        "--run",
        action="store_true",
        help="Launch the notebook in read-only app mode (`marimo run`) instead of editor mode (`marimo edit`).",
    )
    parser.add_argument(
        "-b",
        "--browse",
        action="store_true",
        help="Open the marimo directory browser at the top-level `modules/` folder.",
    )

    args = parser.parse_args(argv)
    lessons = list_lessons()

    if args.list:
        _print_lessons(lessons)
        return 0

    if args.browse:
        return _launch_marimo(get_modules_dir(), run_mode=args.run)

    if args.target:
        # Check if numeric index (1-based)
        if args.target.isdigit():
            idx = int(args.target)
            if 1 <= idx <= len(lessons):
                return _launch_marimo(lessons[idx - 1], run_mode=args.run)
            print(f"Error: Lesson index {idx} is out of range (1..{len(lessons)}).", file=sys.stderr)
            _print_lessons(lessons)
            return 1

        # Otherwise substring match against `<module>/<lesson>`
        query = args.target.lower()
        matches = [
            nb for nb in lessons if query in _format_lesson_label(nb).lower()
        ]
        if len(matches) == 1:
            return _launch_marimo(matches[0], run_mode=args.run)
        if len(matches) > 1:
            print(f"Multiple lessons match '{args.target}':", file=sys.stderr)
            _print_lessons(matches)
            return 1

        print(f"No lesson matching '{args.target}' found.", file=sys.stderr)
        _print_lessons(lessons)
        return 1

    # Interactive prompt when no target is provided
    _print_lessons(lessons)
    if not lessons:
        return 1

    if not sys.stdin.isatty():
        return 0

    print("Enter a lesson number to launch, 'b' to browse all modules, or 'q' to quit:")
    try:
        choice = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return 0

    if not choice or choice.lower() in {"q", "quit", "exit"}:
        return 0
    if choice.lower() in {"b", "browse"}:
        return _launch_marimo(get_modules_dir(), run_mode=args.run)
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(lessons):
            return _launch_marimo(lessons[idx - 1], run_mode=args.run)

    print(f"Unrecognized selection: '{choice}'", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
