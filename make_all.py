"""
Runs the Zdravoletie DATA PREPARATION pipeline in dependency order.
Executes all 8 source notebooks via nbconvert --execute --inplace.
Any notebook failure halts the pipeline immediately.

This script covers data scraping through model artifact generation.
The three thesis experiment notebooks (Experiment_1, Experiment_2,
Experiment_3) are intentionally excluded: they are standalone scripts
and must be run separately after this pipeline completes.

Usage:
    python make_all.py               # run all 8 data-prep notebooks
    python make_all.py --skip-scraping   # skip Data_Scraping.ipynb
"""

import subprocess
import sys
import time
from pathlib import Path

NOTEBOOKS_IN_ORDER = [
    "Data_Scraping.ipynb",     # requires live anovator.com access
    "Data_model.ipynb",
    "Age_Pred.ipynb",
    "Health_Pipeline.ipynb",   # produces all model artifacts in models/
    "Data_Gen.ipynb",          # requires models/ artifacts
    "Benchmarkinig.ipynb",     # requires models/ and synthetic data
    "Insight_Generator.ipynb", # requires models/ artifacts
    "WI_IS.ipynb",             # writes zdravoletie_app.py
]

TIMEOUT_SECONDS = 600  # 10 minutes per notebook


def run_notebook(notebook_path: str) -> bool:
    """Execute a notebook in-place. Returns True on success."""
    print(f"\n{'=' * 60}")
    print(f"Running: {notebook_path}")
    print(f"{'=' * 60}")
    start = time.time()

    result = subprocess.run(
        [
            sys.executable, "-m", "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            f"--ExecutePreprocessor.timeout={TIMEOUT_SECONDS}",
            "--ExecutePreprocessor.kernel_name=python3",
            notebook_path,
        ],
        capture_output=True,
        text=True,
    )

    elapsed = time.time() - start

    if result.returncode == 0:
        print(f"  OK  ({elapsed:.0f}s)")
        return True

    print(f"  FAILED  ({elapsed:.0f}s)")
    if result.stderr:
        print(result.stderr[-3000:])
    return False


def main() -> None:
    skip_scraping = "--skip-scraping" in sys.argv

    for notebook in NOTEBOOKS_IN_ORDER:
        if skip_scraping and notebook == "Data_Scraping.ipynb":
            print(f"SKIP  {notebook}  (--skip-scraping)")
            continue

        if not Path(notebook).exists():
            print(f"SKIP  {notebook}  (file not found)")
            continue

        success = run_notebook(notebook)

        if not success:
            print(f"\nPipeline halted at: {notebook}")
            print("Fix the error above, then re-run.")
            sys.exit(1)

    print("\nFull pipeline completed successfully.")


if __name__ == "__main__":
    main()
