import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import platform
    import sys

    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd
    import polars as pl

    from course_utils import get_asset_path

    return alt, get_asset_path, mo, np, pd, pl, platform, sys


@app.cell(hide_code=True)
def _(mo, np, pd, pl, platform, sys):
    mo.md(f"""
    # Welcome to the Interactive Course Lab!

    This notebook is powered by **marimo** and managed by **uv**. Every cell in a marimo notebook is **reactive**: when you interact with a UI widget or modify a variable, all dependent cells automatically update.

    ### Environment Status
    | Component | Version / Details |
    | :--- | :--- |
    | **Python** | `{platform.python_version()}` (`{sys.platform}`) |
    | **marimo** | `{mo.__version__}` |
    | **Polars** | `{pl.__version__}` |
    | **Pandas** | `{pd.__version__}` |
    | **NumPy** | `{np.__version__}` |
    """)
    return


@app.cell
def _(get_asset_path, mo, pl):
    csv_path = get_asset_path(__file__, "sample_dataset.csv")
    df = pl.read_csv(csv_path)

    mo.md(
        f"""
        ## 1. Loading Lesson Assets

        Each lesson has its own `assets/` folder. Using `course_utils.get_asset_path(__file__, "sample_dataset.csv")`, we loaded `{csv_path.name}` ({df.height} rows, {df.width} columns):
        """
    )
    return (df,)


@app.cell
def _(df, mo):
    cohorts = ["All"] + sorted(df["cohort"].unique().to_list())
    cohort_dropdown = mo.ui.dropdown(
        options=cohorts,
        value="All",
        label="Filter by Cohort:",
    )
    min_hours_slider = mo.ui.slider(
        start=0.0,
        stop=10.0,
        step=0.5,
        value=0.0,
        label="Minimum Study Hours:",
    )

    mo.hstack([cohort_dropdown, min_hours_slider], justify="start", gap=2)
    return cohort_dropdown, min_hours_slider


@app.cell
def _(alt, cohort_dropdown, df, min_hours_slider, mo, pl):
    filtered_df = df.filter(pl.col("study_hours") >= min_hours_slider.value)
    if cohort_dropdown.value != "All":
        filtered_df = filtered_df.filter(
            pl.col("cohort") == cohort_dropdown.value
        )

    chart = (
        alt.Chart(filtered_df.to_pandas())
        .mark_circle(size=120)
        .encode(
            x=alt.X("study_hours:Q", title="Study Hours"),
            y=alt.Y(
                "quiz_score:Q",
                title="Quiz Score",
                scale=alt.Scale(domain=[50, 100]),
            ),
            color=alt.Color("cohort:N", title="Cohort"),
            tooltip=[
                "student_id",
                "cohort",
                "study_hours",
                "practice_labs_completed",
                "quiz_score",
            ],
        )
        .properties(
            title="Study Hours vs. Quiz Score",
            width=550,
            height=320,
        )
    )

    mo.vstack(
        [
            mo.md(f"**Showing {filtered_df.height} of {df.height} students**"),
            chart,
            filtered_df,
        ]
    )
    return (filtered_df,)


@app.cell
def _(mo):
    mo.md("""
    ## 2. Hands-On Exercise

    Try computing the average `quiz_score` per `cohort` on `filtered_df` in the cell below using Polars' `group_by` and `agg`!
    """)
    return


@app.cell
def _(filtered_df, pl):
    summary_by_cohort = (
        filtered_df.group_by("cohort")
        .agg(
            pl.len().alias("student_count"),
            pl.col("study_hours").mean().round(2).alias("avg_study_hours"),
            pl.col("quiz_score").mean().round(2).alias("avg_quiz_score"),
        )
        .sort("cohort")
    )
    summary_by_cohort
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
