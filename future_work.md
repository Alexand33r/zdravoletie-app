# Future Work

Items confirmed out of scope for this thesis. Do not implement during Phases 1-3.
Log new items here whenever they arise so they are not forgotten and not acted on.

## Alternative synthetic data generators
- CTGAN, TVAE, or Gaussian copula as replacements or comparisons for the GMM pipeline.
  Rationale for exclusion: would require a separate methodology chapter and is a thesis topic in itself.

## Alternative evaluation strategies
- Time-based train/test splits (train on earlier scan dates, test on later).
  Rationale: the longitudinal structure is real but the dataset has too few individuals (53) to
  make meaningful temporal splits without collapsing the test set.
- Calibration evaluation: reliability diagrams, Brier scores for the binary classification task.
- Power analysis to formally justify N=53 individuals.

## Alternative preprocessing
- Ordinal encoding for postural risk scores (1-5) and bodyShape (0-7).
- KNN imputation or MICE as alternatives to median imputation.

## Additional classifiers
- Logistic regression, SVM classifier, XGBoost for the binary score > 90 task.

## Data expansion
- Scraping reports from additional gyms to reduce single-gym bias and increase N.
- Second-wave scans from existing individuals for a proper longitudinal study.
- Targeted recruitment of female participants (current dataset is 81% male).

## Product extensions
- File upload of a new individual scan in the Streamlit app.
- Population-level comparison view (individual vs. cohort percentile).
- PDF report export.
- Deployed version on Streamlit Community Cloud with authentication.
