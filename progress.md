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
- [x] Deploy to Streamlit Community Cloud — live at https://zdravoletie-app-r59gvphlkih7549cgipbgt.streamlit.app/

## Phase 4 — Writing (June 15-22)

- [x] thesis/introduction.md   (~995 words — context, research question, scope/out-of-scope, practical significance)
- [x] thesis/related_work.md   (~2074 words — biological age lit, synthetic data gen, SHAP in health ML)
- [x] thesis/methodology.md   (~2637 words — full draft with 4 limitations, protocol, all 3 experiments)
- [x] thesis/results.md       (~1900 words — §4.2.3 reliability curve added, §4.3.1 GMM fidelity metric added, tables renumbered 4.1–4.7)
- [x] thesis/discussion.md    (~2904 words — 5 discussion points, all 4 limitations addressed, §5.4 SHAP interpretation)
- [x] thesis/conclusion.md    (~1138 words — findings summary, 3 sub-question answers, limitations cross-ref, 6 future work items)
- [x] thesis/abstract.md    (~303 words — research question, three experiments, Ridge exception, G1=G4, sample size caveat)
- [x] thesis/ethics.md      (~800 words — GDPR classification, consent assumptions, data handling, production requirements)
- [x] pages/0_About.py      (static About page: tool purpose, age gap vs clinical age, known limitations)
- [x] pages/3_Population_View.py — age vs age_gap scatter plot added below histogram (active_age from session_state)
- [x] main.tex hardcoded Section~3.9 references fixed to \ref{sec:limitations} (lines 904, 971); hyperref moved after natbib
- [x] thesis/PoA_full.tex created — standalone LaTeX PoA with MoSCoW table, TOKIO tables, risk matrix longtable, Gantt longtable; microtype fix applied; compiles cleanly (18 pages)
- [x] thesis/presentation_outline.md created — 10-slide, 15-min defence outline with examiner Q&A per slide
- [x] thesis/main.tex restructured to Fontys 7-chapter format (Steps 1–3, 2026-05-28)
- [x] thesis/main.tex: listings package added; 5 Python code snippets inserted in Ch 5 (GroupShuffleSplit, imputation, GMM, Wilcoxon) and Ch 4 (SHAP); compiles cleanly (39 pages, 2026-05-28)
      - Ch 1 Summary, Ch 2 Reason for and Relevance, Ch 3 Research Questions + Product Description
      - Ch 4 Theoretical Framework, Ch 5 Research Method (Section 3.10 added), Ch 6 Results and Conclusions
      - Ch 7 Discussion and Recommendations (Ridge/G1=G4/Wilcoxon expanded; Recommendations section)
      - Full 4-step compile clean: pdflatex/bibtex/pdflatex/pdflatex all exit 0 — 38 pages
- [ ] Competency portfolio — personal fills (student number, reflection paragraphs) — human only
