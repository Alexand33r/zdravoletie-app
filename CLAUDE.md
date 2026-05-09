# Zdravoletie — Project Instructions for Claude Code

## What this project is

A graduation internship at Zdravoletie for Fontys University of Applied Sciences (BSc Applied Mathematics, Data Science major). Two deliverables matter for grading:
- Graduation Report (60%)
- Competency Portfolio (40%)
Plus an oral defense on July 4-5, 2026. Hard freeze date: June 22, 2026.

The supervisor split: Peter Alem (educational, academic side) and Kostadin Galchin (company side). The academic side carries the grade.

## Thesis framing — locked

This project is NOT "predicting biological age."

It IS: **Reverse-engineering and analyzing a proprietary health score (Anovator's bodyAge) from raw biometric inputs, with comparative evaluation of modeling approaches and synthetic data augmentation.**

This framing is non-negotiable. Every experiment, chart, and chapter must support this framing. If something doesn't fit, it goes in "future work" — not in the main thesis.

## Scope — three experiments only

These three experiments form the core empirical contribution. Do these properly. Do not add more.

### Experiment 1: Model comparison with statistical significance
- Five regressors: RandomForest, Ridge, SVR, GradientBoosting, HistGradientBoosting
- 30 repeated GroupShuffleSplit iterations (grouped by individual name)
- Report MAE, RMSE, R² as mean with 95% confidence intervals
- Paired Wilcoxon signed-rank tests on per-fold scores between every model pair
- Bonferroni correction for multiple comparisons
- Output: a results table, a box plot, a significance matrix

### Experiment 2: Synthetic data ablation
- Three training regimes for each of the five models:
  (a) 158 real records only
  (b) 158 real + 1000 GMM synthetic
  (c) 1000 GMM synthetic only
- All evaluated on held-out real data using the same GroupShuffleSplit protocol
- Same significance testing as Experiment 1
- This experiment justifies or invalidates the entire GMM pipeline. Treat its outcome as an honest finding either way.

### Experiment 3: Feature group ablation
- Four cumulative groups: body composition → + bioimpedance (r20/r100) → + postural risk → + joint angles
- Best-performing model from Experiment 1 only
- Same evaluation protocol, same significance testing
- Output: bar chart of MAE by feature group with confidence intervals

## Out of scope — DO NOT do these

When tempted, stop. Note in `future_work.md` and move on.

- CTGAN, TVAE, or copula synthesis comparisons
- Time-based splits
- Calibration diagrams or Brier scores
- Ordinal encoding experiments
- KNN or MICE imputation comparisons
- Power analysis (acknowledge in limitations only)
- Additional classifiers
- New feature engineering beyond what already exists in Health_Pipeline.ipynb

## Hard engineering rules

- No abbreviations in column names, variable names, or function names
- No emojis anywhere — not in code, comments, markdown, plots, or chat
- Fixed random seed (42) for every stochastic operation, declared in a single `config.py`
- All experiments report mean with 95% CI, never single-split point estimates
- Native scikit-learn and scipy only — no autoML, no exotic libraries
- Every plot has axis labels with units and a clear title
- All file paths are relative to repo root, never absolute
- Bulgarian-language artifacts stay where they are; thesis is in English

## Tone and feedback

- Be direct. Call out bad decisions and flawed methodology explicitly.
- Do not soften criticism. The goal is a defensible thesis, not a comfortable one.
- If a plan I propose is wrong, say so before executing.
- Permission to read and edit any file in the repo without asking.

## Phase plan with dates

- **Phase 1 — Stabilization: May 8-15.** Fix all 11 known bugs. Set up `config.py`, `requirements.txt`, repo-root `make_all.py` to run full pipeline. Add this CLAUDE.md.
- **Phase 2 — Core experiments: May 15 - June 5.** Run Experiments 1, 2, 3 with full statistical rigor. Save all results to `results/` as CSVs and figures.
- **Phase 3 — Product polish: June 5-15.** Streamlit app: file upload, population view, PDF export, deployed to Streamlit Community Cloud.
- **Phase 4 — Writing: June 15-22.** Graduation report and competency portfolio. No new code, no new experiments.
- **Buffer: June 22 - July 4.** Presentation prep only.

If a phase finishes early, do not start the next one's work scope-wise — instead, deepen the current phase's quality.

## Repo conventions

- All notebooks live in repo root for now (do not reorganize without asking)
- Saved models and artifacts go in `models/`
- Generated datasets go in `data/`
- Experimental results (CSVs, figures) go in `results/`
- Thesis writing goes in `thesis/` as markdown files, one per chapter

## What you (Claude Code) should do at session start

1. Read this file fully
2. Check `progress.md` (create if missing) for current status
3. State which phase we're in and what the next concrete task is
4. Confirm the model you're running as
5. Wait for instructions before doing anything

## What you should NEVER do

- Add experiments beyond the three listed above
- Drift back to the "predicting biological age" framing
- Run code that mutates `models/` or `data/` files without explicitly stating what will change
- Remove failed experiment results — failures are findings