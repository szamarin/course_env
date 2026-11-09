# Course Modules & Lessons Authoring Guide

All hands-on labs are organized into a two-level hierarchy inside `modules/`:

```text
modules/
└── <module_number>_<module_slug>/
    └── lesson_<number>_<lesson_slug>/
        ├── README.md          # Optional lesson overview / instructions
        ├── notebook.py        # Interactive marimo notebook
        └── assets/            # Datasets, images, and static files for this lesson
```

## Creating a New Lesson

1. **Create the lesson directory and `assets/` subfolder:**
   ```bash
   mkdir -p modules/01_data_wrangling/lesson_01_filtering/assets
   ```

2. **Create or edit the marimo notebook:**
   ```bash
   uv run marimo edit modules/01_data_wrangling/lesson_01_filtering/notebook.py
   ```

3. **Access `course_utils` and lesson-local assets inside `notebook.py`:**
   Even though `course_utils` is installed in `.venv`, adding `src/` relative to `__file__` at the top of the notebook guarantees imports work regardless of how or where the notebook is launched:
   ```python
   from pathlib import Path
   import sys

   _src_dir = str(Path(__file__).resolve().parents[3] / "src")
   if _src_dir not in sys.path:
       sys.path.insert(0, _src_dir)

   from course_utils import get_asset_path
   import polars as pl

   data_path = get_asset_path(__file__, "my_data.csv")
   df = pl.read_csv(data_path)
   ```

4. **Adding new Python packages to the course:**
   All dependencies are managed in the top-level `pyproject.toml`. To add a package:
   ```bash
   uv add scikit-learn
   ```
   Commit both `pyproject.toml` and `uv.lock` so students receive the exact same environment when running `./setup.sh` or `setup.bat` / `.\setup.ps1`.

5. **Validating notebooks:**
   ```bash
   uv run marimo check modules/01_data_wrangling/lesson_01_filtering/notebook.py
   ```
