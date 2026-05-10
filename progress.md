# Progress Tracker

## Phase 1 — Stabilization (May 8-15)

### Bug fixes (11 total)
- [x] 1. Circular benchmarking — Part 2 (real-data validation) added to Benchmarkinig.ipynb
- [x] 2. Feature leakage in Age_Pred.ipynb — correlations now computed on training split only
- [x] 3. df_real_imputed NameError in Data_Gen.ipynb — resolved in prior session
- [x] 4. Duplicate GMM training in Data_Gen.ipynb — replaced with df_synth.copy()
- [x] 5. fillna(0) for health metrics — training-set medians used in all three locations
- [x] 6. Streamlit sidebar bug — st.sidebar.number_input used correctly
- [x] 7. BMI not recalculated in simulation — fixed in WI_IS.ipynb and zdravoletie_app.py
- [x] 8. Small test set warning — printed at runtime in Age_Pred.ipynb split cell
- [x] 9. Single cross-validation split — 10-fold repeated CV cell added to Health_Pipeline.ipynb
- [x] 10. preprocess_client_scan duplicated — all three copies verified consistent, no bug
- [x] 11. Negative R² unexplained — explanatory note added to Age_Pred.ipynb

### Scaffolding
- [x] CLAUDE.md written
- [x] config.py — RANDOM_SEED, all paths, CV protocol, model registry, feature groups
- [x] requirements.txt
- [x] make_all.py — runs full 8-notebook pipeline via nbconvert
- [x] results/ directory created
- [x] thesis/ directory created
- [x] future_work.md — out-of-scope items logged
- [x] progress.md — this file

## Phase 2 — Core experiments (May 15 - June 5)

- [x] Experiment 1: five-model comparison (30x GroupShuffleSplit, MAE/RMSE/R2 with 95% CI, Wilcoxon + Bonferroni)
      Best model: HistGradientBoosting (MAE 2.43). No pairs significant at Bonferroni alpha=0.005 — all inconclusive.
- [x] Experiment 2: synthetic data ablation (real-only vs real+synthetic vs synthetic-only)
      RealPlusSynth significantly beats RealOnly for 4/5 models (RF, SVR, GB, HGB). Ridge degrades on SynthOnly.
- [x] Experiment 3: feature group ablation (anthropometric+metabolic -> +bioimpedance -> +postural risk -> +joint angles)
      No group transitions significant. G1 (63 features) has lowest mean MAE; adding groups adds no significant signal.

## Phase 3 — Product polish (June 5-15)

- [x] Streamlit: multi-page app rebuilt (zdravoletie_app.py + pages/)
      - app_utils.py: shared load/predict/visualise/PDF utilities
      - pages/1_Individual_Report.py: client selection by name, simulation sliders, SHAP bar chart
      - pages/2_Upload_New_Scan.py: CSV upload, column validation, prediction, risk/protective factors
      - pages/3_Population_View.py: histogram with client marked, percentile stats
      - pages/4_Export_PDF.py: matplotlib PDF download (46 KB, one-page report)
- [ ] Deploy to Streamlit Community Cloud (see deployment checklist below)

## Phase 4 — Writing (June 15-22)

- [x] thesis/introduction.md   (~995 words — context, research question, scope/out-of-scope, practical significance)
- [x] thesis/related_work.md   (~2074 words — biological age lit, synthetic data gen, SHAP in health ML)
- [x] thesis/methodology.md   (~2637 words — full draft with 4 limitations, protocol, all 3 experiments)
- [x] thesis/results.md       (~1759 words — all tables with exact numbers, R2 caveat, significance tables)
- [x] thesis/discussion.md    (~2904 words — 5 discussion points, all 4 limitations addressed)
- [x] thesis/conclusion.md    (~1138 words — findings summary, 3 sub-question answers, limitations cross-ref, 6 future work items)
- [x] thesis/abstract.md    (~303 words — research question, three experiments, Ridge exception, G1=G4, sample size caveat)
- [x] thesis/ethics.md      (~800 words — GDPR classification, consent assumptions, data handling, production requirements)
- [x] pages/0_About.py      (static About page: tool purpose, age gap vs clinical age, known limitations)
- [ ] Competency portfolio
