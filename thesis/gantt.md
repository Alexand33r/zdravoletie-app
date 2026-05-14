# Gantt Chart — Zdravoletie Graduation Project

**Project period:** February 9 – June 27, 2026  
**Hard freeze:** June 22, 2026  
**Oral defence:** July 4–5, 2026

**Status key:** D = Done | I = In progress | P = Planned | (blank) = not scheduled

## Week reference

| Week | Dates |
|------|-------|
| W1 | Feb 9 – Feb 15 |
| W2 | Feb 16 – Feb 22 |
| W3 | Feb 23 – Mar 1 |
| W4 | Mar 2 – Mar 8 |
| W5 | Mar 9 – Mar 15 |
| W6 | Mar 16 – Mar 22 |
| W7 | Mar 23 – Mar 29 |
| W8 | Mar 30 – Apr 5 |
| W9 | Apr 6 – Apr 12 |
| W10 | Apr 13 – Apr 19 |
| W11 | Apr 20 – Apr 26 |
| W12 | Apr 27 – May 3 |
| W13 | May 4 – May 10 |
| W14 | May 11 – May 17 (current) |
| W15 | May 18 – May 24 |
| W16 | May 25 – May 31 |
| W17 | Jun 1 – Jun 7 |
| W18 | Jun 8 – Jun 14 |
| W19 | Jun 15 – Jun 21 |
| W20 | Jun 22 – Jun 27 |

## Schedule

| Work Package | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | W9 | W10 | W11 | W12 | W13 | W14 | W15 | W16 | W17 | W18 | W19 | W20 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Data extraction and audit | D | D | D | D | D | D | D | D | | | | | | | | | | | | |
| Data preparation and modeling | | | | D | D | D | D | D | D | D | D | D | | | | | | | | |
| Experiment 1: model comparison | | | | | | | | | | | | | D | D | | | | | | |
| Experiment 2: synthetic ablation | | | | | | | | | | | | | D | D | | | | | | |
| Experiment 3: feature ablation | | | | | | | | | | | | | D | D | | | | | | |
| Streamlit app development | | | | | | | | | | | | | D | D | D | D | D | D | | |
| Thesis writing | | | | | | | | D | D | D | D | D | D | D | D | D | D | D | D | |
| Competency portfolio | | | | | | | | | | | | | | | | | | P | P | |
| Buffer and presentation prep | | | | | | | | | | | | | | | | | | | | P |

## Notes

Data extraction and audit (W1–W8) covered manual export of Anovator scan records through the web interface, data integrity checks, variable identification, and initial exploratory analysis across all eight source notebooks.

Data preparation and modeling (W4–W12) covered feature engineering, imputation strategy design, the Health_Pipeline.ipynb production model, and the GMM synthetic data generation pipeline in Data_Gen.ipynb, overlapping with data audit as notebook development proceeded iteratively.

Experiments 1, 2, and 3 (W13–W14) were run sequentially within the stabilisation and core experiment phases. Experiment 1 established the model ranking. Experiment 2 evaluated synthetic augmentation. Experiment 3 performed the feature group ablation on the best model from Experiment 1. All statistical testing and figure generation were completed within this window.

Streamlit app development (W13–W18) covered the multi-page application (Individual Report, Upload New Scan, Population View, Export PDF, About), the shared utilities module, SHAP integration, PDF export, and deployment to Streamlit Community Cloud.

Thesis writing (W8–W19) ran in parallel with the experimental work, with chapter drafts produced progressively: introduction and related work during data preparation, methodology during experiments, results and discussion after experiments, and conclusion and abstract during the product polish and extended improvement phases.

Competency portfolio (W18–W19) is the sole remaining deliverable as of W14. It is planned for the June 8–22 window.

Buffer and presentation preparation (W20) is reserved for slide preparation, narrative rehearsal, and any final corrections identified during supervision review.
