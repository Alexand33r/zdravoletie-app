# Plan of Approach

---

| Field | Value |
|---|---|
| Project title | Reverse-Engineering and Analysis of a Proprietary Health Score from Raw Biometric Inputs |
| Author | Alexander Tanev |
| Student number | [ALEXANDER TO FILL] |
| Programme | BSc Applied Mathematics, Data Science major |
| Institution | Fontys University of Applied Sciences |
| Company | Zdravoletie Health and Rehabilitation Centre, Varna, Bulgaria |
| Company supervisor | Kostadin Galchin |
| Educational supervisor | Peter Alem |
| Document version | 1.0 |
| Date | May 14, 2026 |
| Project period | February 9 – June 27, 2026 |
| Hard freeze | June 22, 2026 |
| Oral defence | July 4–5, 2026 |

---

## Table of Contents

1. Introduction
2. Project Definition
   - 2.1 Background
   - 2.2 Problem Description
   - 2.3 Assignment
   - 2.4 Project Result and Deliverables
   - 2.5 User Requirements
   - 2.6 Project Boundaries
3. Phasing
4. Project Control
5. Budget and Planning
6. Risk Analysis
7. Closing

---

## 1. Introduction

### 1.1 Document Purpose

This Plan of Approach describes the design, execution, and management of the graduation internship project carried out at Zdravoletie Health and Rehabilitation Centre, Varna, Bulgaria, as a partial fulfilment of the requirements for the degree of Bachelor of Applied Mathematics, Data Science major, at Fontys University of Applied Sciences. The document establishes the project's scope, phasing, planning, and risk profile for review by both the educational supervisor and the company supervisor. It serves as the binding reference for project management decisions throughout the internship period and as evidence of structured project planning in the competency portfolio.

### 1.2 Company Background

Zdravoletie is a health and rehabilitation centre based in Varna, Bulgaria, offering physiotherapy, dietary advising, and personalised wellness consultations. The centre operates an Anovator body scanning system, a proprietary platform that records biometric measurements across four modalities: anthropometric and metabolic measurements (including body mass, BMI, segmental fat and muscle mass, visceral fat index, and metabolic age), bioelectrical impedance analysis (phase angle and impedance values at 20 kHz and 100 kHz), postural camera imaging (generating a six-dimensional postural risk score), and joint angle measurement. From these inputs the Anovator system computes a composite score called bodyAge — an estimated biological age expressed in years — using a proprietary and undisclosed computational formula. Practitioners at Zdravoletie use the bodyAge score and its component measurements to advise clients on dietary, exercise, and physiotherapy interventions. The centre is supervised on the company side by Kostadin Galchin, who confirmed full technical autonomy for the student at project inception.

### 1.3 Document Overview

Section 2 defines the project, beginning with the technical and clinical background that motivates the research, then stating the problem, formulating the assignment in SMART terms, listing the five deliverables, presenting the MoSCoW-categorised user requirements, and defining the project boundaries. Section 3 describes the project phasing using an adapted V-model structure. Section 4 specifies the project control measures for each phase across the five TOKIO dimensions. Section 5 summarises the budget and planning, referencing the Gantt chart and milestone list. Section 6 presents the risk analysis. Section 7 offers a brief closing reflection.

---

## 2. Project Definition

### 2.1 Background

The Anovator bodyAge score is computed from a set of biometric inputs using a formula that Anovator does not disclose to its clients or to the practitioners who administer it. A client informed that their bodyAge is five years above their chronological age has received a clinically weighted statement, but neither that client nor the attending practitioner at Zdravoletie can determine which of the recorded biometric measurements contributed most to the result, how large each measurement's influence was, or which targeted interventions would produce a measurable change in the next scan. The formula is, from the practitioner's perspective, a black box: inputs enter, a score emerges, and the internal mapping is invisible.

This opacity has direct consequences in the advising context. Zdravoletie practitioners decide among dietary, exercise, and physiotherapy interventions partly on the basis of where the bodyAge score is and how it has changed between sessions. Without visibility into the relative weight the formula assigns to body composition, bioimpedance, postural risk, and joint mobility, these decisions rely on intuition about what the formula rewards rather than on direct evidence. The same opacity limits the ability to detect systematic issues — for example, whether the formula assigns weight to metrics that are structurally difficult to change, or whether it produces asymmetric outputs across demographic subgroups.

A further structural feature of the available data intensifies the modelling challenge. Analysis of the 158 scan records assembled for this project reveals a ceiling-effect pattern in the bodyAge distribution: the signed difference between bodyAge and chronological age — referred to throughout this document and the thesis as the age gap — has a mean of 0.45 years and a standard deviation of 3.30 years, with the distribution concentrated near zero. This compression limits the variance available for predictive modelling. A naive model that predicts zero for every record would achieve a mean absolute error equal to the mean absolute deviation of the age gap distribution, which forms a practical floor on achievable prediction error. Any trained regressor must consistently and substantially beat this baseline to justify its complexity. The ceiling effect is not an incidental data quality problem; it is a structural property of how the Anovator formula maps biometric inputs to scores, and it bears on the interpretation of all performance figures reported in the study.

### 2.2 Problem Description

The central problem this project addresses is an interpretability gap in a health technology product that is in active clinical use. Zdravoletie's practitioners and clients receive a numeric score without any explanation of how it was computed or which inputs drove it. This gap is not merely a scientific inconvenience: it affects the quality of health advising decisions and prevents meaningful evaluation of whether the scoring formula is calibrated, consistent, or equitable.

A secondary methodological problem emerged during the project's execution. The initial framing of the project treated the bodyAge score as a proxy for clinical biological age — a quantity studied extensively in gerontology, where the ground truth is established against mortality follow-up, morbidity incidence, or validated biomarker panels. This framing was identified as incorrect at the midterm review: the study has access to none of those external health endpoints, and bodyAge is the Anovator formula's own proprietary output, not a clinically validated measure of physiological ageing. Treating it as a clinical ground truth would expose any performance claim to immediate methodological challenge. The correct framing, adopted after the midterm, is score reverse-engineering: the models in this study learn to approximate an opaque computational formula from its inputs, using the formula's own output as the training target. This reframing makes the research question answerable with the data available, eliminates the need for external clinical validation, and produces findings that are honest about what the data can and cannot establish.

The research question that guides the project is: to what extent can machine learning regression models reverse-engineer the Anovator bodyAge score from the raw biometric inputs the system records, and what do the results reveal about the relative informational contribution of different biometric feature groups?

### 2.3 Assignment

The assignment is defined in SMART terms to provide an unambiguous standard against which completion can be assessed.

The project will deliver a scientifically rigorous empirical study of the reverse-engineering problem described above. Specifically, the student will train and evaluate five regression algorithms — Ridge regression, Support Vector Regression with a radial basis function kernel, Random Forest, Gradient Boosting, and Histogram Gradient Boosting — on a dataset of 158 scan records from 53 individuals drawn from the Zdravoletie Anovator platform. All models will be evaluated using 30 repeated cross-validation folds with GroupShuffleSplit grouped by individual identity, preventing within-person data leakage across splits. Performance will be reported as mean MAE, RMSE, and R² with 95% confidence intervals derived from the 30-fold distribution. Pairwise comparisons will be assessed using the Wilcoxon signed-rank test with Bonferroni correction for multiple comparisons. The study will assess three experimental questions: which algorithm best approximates the Anovator formula, whether GMM-based synthetic data augmentation improves approximation quality on real held-out data, and which biometric feature groups carry independent predictive information. The findings will be written up in a thesis-format graduation report and supported by a deployed Streamlit dashboard that makes the surrogate model and its SHAP-based explanations available to Zdravoletie practitioners. All deliverables will be submitted by June 22, 2026.

The assignment is specific because it defines the algorithms, evaluation protocol, dataset, and experimental questions with no ambiguity. It is measurable through the performance metrics, statistical testing, and deliverable completion criteria. It is achievable given the 158-record dataset, the defined experimental scope, and the available tools. It is relevant because it directly addresses the interpretability gap Zdravoletie identified as a practical need. It is time-bound by the June 22 hard freeze and the July 4–5 oral defence.

### 2.4 Project Result and Deliverables

The project produces five distinct deliverables. The graduation report is the primary academic deliverable: a structured thesis of approximately ten thousand words covering introduction, related work, methodology, results, discussion, and conclusion chapters. It documents the research question, experimental design, statistical findings, and their interpretation in the context of the bodyAge reverse-engineering framing. The graduation report carries sixty percent of the final grade.

The Plan of Approach is the project management deliverable: this document. It establishes the scope, phasing, planning, and risk profile of the project in a format conforming to Fontys University guidelines and serves as evidence of structured planning competency in the portfolio.

The competency portfolio is the second graded academic deliverable, carrying forty percent of the final grade. It presents evidence and reflection for each of the Fontys Applied Mathematics graduation competencies, drawing on the project work as the primary evidence base.

The internship logbook documents the student's weekly activities, decisions, and communications across all twenty project weeks. It provides a verifiable record of professional engagement and serves as supporting evidence for the competency portfolio.

The Streamlit dashboard is the practical product deliverable. It is a five-page application deployed to Streamlit Community Cloud that allows Zdravoletie practitioners to retrieve predictions and SHAP-based feature importance explanations for individual clients, upload new scan records for immediate scoring, view population comparison statistics, and export a PDF report. The application makes the analytical outputs of the research accessible to a non-technical clinical audience.

### 2.5 User Requirements

The following requirements have been identified through analysis of the project context and discussions with both supervisors. They are categorised according to the MoSCoW framework (Must have, Should have, Could have, Won't have) and numbered for traceability across project phases.

| ID | Requirement | Category | Stakeholder |
|---|---|---|---|
| R01 | The study must address three research questions — algorithm comparison, synthetic augmentation, and feature group ablation — each with a dedicated experiment and full statistical testing | Must have | Educational supervisor |
| R02 | All experimental results must be reported as mean with 95% confidence interval derived from 30 cross-validation folds; single-split point estimates are not acceptable | Must have | Educational supervisor |
| R03 | Cross-validation splits must be grouped by individual identity so that no client's records appear in both training and test folds | Must have | Educational supervisor |
| R04 | Pairwise model comparisons must be assessed with the Wilcoxon signed-rank test and Bonferroni correction; conclusions must accurately distinguish inconclusive from significant results | Must have | Educational supervisor |
| R05 | The graduation report must be submitted in full by June 22, 2026, covering all thesis chapters with consistent framing of the research as score reverse-engineering | Must have | Educational supervisor / Fontys |
| R06 | The Plan of Approach, logbook, and competency portfolio must be completed and submitted as standalone documents by June 22, 2026 | Must have | Educational supervisor / Fontys |
| R07 | The surrogate model and the SHAP-based feature importance explanations must be accessible to Zdravoletie practitioners through a deployed web interface | Should have | Company supervisor |
| R08 | The dashboard must allow upload of a new scan record in CSV format, with column validation and immediate age gap prediction | Should have | Company supervisor |
| R09 | The competency portfolio must address all required Fontys graduation competencies with concrete evidence from the project | Should have | Educational supervisor |
| R10 | The application must provide a population comparison view showing the current client's position in the full 158-record distribution | Could have | Company supervisor |
| R11 | The application must support export of a single-page PDF report per client for use in advising sessions | Could have | Company supervisor |
| R12 | CTGAN, TVAE, copula-based, or any other alternative synthetic data generation method will not be evaluated | Won't have | — |
| R13 | Clinical validation of the bodyAge score against external health endpoints will not be performed | Won't have | — |
| R14 | Neural network architectures will not be included in the algorithm comparison | Won't have | — |

### 2.6 Project Boundaries

The following items are explicitly outside the scope of this project. They are documented here to prevent scope creep and to provide an honest account of what the study does not claim.

The study does not perform clinical validation of the Anovator bodyAge score. It makes no claim that the score is a valid measure of physiological ageing, that a high age gap is predictive of adverse health outcomes, or that model predictions have diagnostic utility. Any interpretation in clinical terms would require longitudinal health endpoint data that this study does not have access to.

The study does not evaluate alternative synthetic data generation architectures. Generative adversarial networks, variational autoencoders, copula-based synthesis, and related approaches are excluded because the 158-record corpus falls below the data scale at which those architectures train reliably. The decision to use a five-component Gaussian Mixture Model was made on precisely those grounds, and introducing GAN or copula comparisons would expand the scope without adding defensible empirical insight given the available data.

The study does not use time-based cross-validation splits. The dataset is cross-sectional — most clients have two or three sessions spanning irregular intervals — and temporal ordering of train and test partitions would introduce arbitrary gaps in the 53-individual sample rather than improving realism of the evaluation.

The study does not perform imputation comparisons. The median imputation strategy applied uniformly to all training folds was selected for its robustness to skewed distributions and for consistency with the production model artifact that the dashboard depends on. Evaluating KNN, MICE, or constant-value alternatives would expand the scope without addressing the core research question.

The study does not perform hyperparameter optimisation as part of the comparative experiments. Model hyperparameters are fixed as specified in config.py to ensure that observed performance differences reflect algorithm family characteristics rather than optimisation effort. Future work may evaluate tuned configurations, but this is not within the scope of the current project.

No additional experiments beyond the three listed in Section 2.3 will be conducted. Features used are limited to those already defined in Health_Pipeline.ipynb. New feature engineering, ordinal encoding experiments, and power analysis are all out of scope, with the last acknowledged in the limitations section of the thesis.

---

## 3. Phasing

The project phases are structured following an adapted V-model. In the standard V-model, the left arm descends from requirements analysis through system design to implementation, and the right arm ascends from unit testing through integration testing to acceptance. For a research project of this type, this structure translates into a descending arm of increasingly concrete problem definition and data preparation, a bottom implementation phase of experimental execution, and an ascending arm of increasingly comprehensive validation culminating in the oral defence. Six phases are identified. Because the project is substantially complete as of the date of this document, phases are described both in terms of what was planned and what was executed.

---

### Phase 1: Problem Analysis and Framing

**Period:** February 9 – April 19, 2026 (Weeks 1–10)

**What is done:** This phase establishes what the project is actually asking and whether the available data can answer it. It covers the initial orientation to the Anovator system, the identification of the bodyAge target variable, the design of the data extraction procedure, the conduct of the midterm review, and the critical project reframing that followed. The most significant event in this phase was the midterm feedback from the educational supervisor, which identified two fundamental issues: the biological age framing was scientifically incorrect given the available data, and an R² of 0.98 obtained at that stage was implausible and indicated a methodological error. Both issues were resolved by the end of the phase: the framing was corrected to score reverse-engineering, and the source of the R² artefact was traced to circular benchmarking — a structural design error in which synthetic records pseudo-labelled by a model trained on all 158 real records were then used to evaluate that same model.

**How:** The student attended the project kickoff at Zdravoletie, explored the Anovator web interface systematically, and began mapping available variables against the project objective. Preliminary modelling was conducted in Health_Pipeline.ipynb and Benchmarkinig.ipynb using non-rigorous single-split evaluation. Following the midterm review, a systematic audit of all eight notebooks was conducted, documenting eleven distinct methodological and implementation issues before any fixes were applied, to prevent partial corrections from masking undiscovered problems.

**Input:** Anovator web interface; Fontys internship guidelines; preliminary notebook pipeline.

**Output:** Corrected project framing (score reverse-engineering); documented list of eleven bugs; CLAUDE.md establishing the non-negotiable project constraints; config.py establishing the fixed random seed, file paths, cross-validation protocol, model registry, and feature group definitions; requirements.txt; make_all.py; results/ and thesis/ directories; future_work.md.

**Deliverable:** CLAUDE.md (project charter); Phase 1 stabilisation artefacts.

---

### Phase 2: Data Collection and Engineering

**Period:** February 9 – May 3, 2026 (Weeks 1–12, overlapping with Phase 1)

**What is done:** This phase covers the complete data pipeline from raw Anovator export files to a clean, consistently imputed feature matrix ready for experimental use. It includes data extraction, data integrity checks, feature engineering, and the construction of the GMM synthetic data generation pipeline.

**How:** Records were extracted manually from the Anovator web interface, as no programmatic API was available. One hundred and fifty-eight scan records were collected from 53 unique clients spanning sessions from 2022 to 2024. Data integrity checks identified a systematic discrepancy in segmental fat measurements for a subset of records (sum of limb segments not matching reported total body fat, with differences up to approximately 13 kg); the discrepancy was attributed to rounding behaviour in the Anovator platform and the affected records were retained. Feature engineering produced five derived variables: a binary sex encoding, muscle-to-fat ratio, upper-to-lower body muscle ratio, trunk-to-limb fat ratio (all three with a 0.1 additive constant in the denominator to prevent division by zero), and an aggregated postural index (arithmetic mean of six individual postural risk scores). Five features with missingness above 88% and two features using -1 as a sentinel value for missing data were identified and documented as limitations. Imputation was performed using training-fold medians to prevent data leakage. A five-component Gaussian Mixture Model was fitted to the 158 real records to generate 1000 synthetic records; pseudo-labels for the synthetic corpus were generated by the production model trained on all real records, constituting a teacher-student knowledge distillation setup.

**Input:** Anovator web export files; domain knowledge from Kostadin Galchin on the clinical meaning of each variable.

**Output:** Cleaned and imputed dataset (158 real records); 1000-record GMM synthetic dataset with pseudo-labels; documented data quality issues; feature engineering pipeline in Health_Pipeline.ipynb.

**Deliverable:** data/ directory contents; Health_Pipeline.ipynb production model; Data_Gen.ipynb synthetic data notebook.

---

### Phase 3: Modeling and Experimentation

**Period:** May 4–17, 2026 (Weeks 13–14)

**What is done:** This phase executes all three core experiments with the corrected evaluation protocol, generates all result tables and figures, and completes the statistical testing.

**How:** All three experiments use 30 repeated GroupShuffleSplit cross-validation folds grouped by client identity with an 80/20 split of the 53 individuals, a fixed random seed of 42 for all stochastic operations, and Wilcoxon signed-rank testing with Bonferroni correction for all pairwise comparisons. Experiment 1 evaluates five regression algorithms on the full 88-feature set, reporting MAE, RMSE, and R² as mean with 95% confidence intervals. All ten pairwise comparisons are inconclusive at the Bonferroni-corrected significance threshold. HistGradientBoosting achieves the lowest mean MAE at 2.43 years. Experiment 2 evaluates all five models under three training regimes: real data only (158 records), real data augmented with 1000 GMM synthetic records, and synthetic data only. The real-plus-synthetic regime produces statistically significant MAE reductions for four of five models; Ridge regression degrades substantially under the synthetic-only regime, a finding traced to pseudo-label variance compression. Experiment 3 applies a cumulative feature group ablation to HistGradientBoosting, adding body composition, bioimpedance, postural risk, and joint angles in four successive increments. All six group-pair comparisons are inconclusive; the first group (63 features) achieves the lowest mean MAE at 2.39 years.

**Input:** Cleaned dataset from Phase 2; GMM synthetic dataset; experimental design from CLAUDE.md and config.py.

**Output:** Twelve result CSV files; twelve figures (box plots, bar charts, heatmaps, reliability curve, GMM fidelity metric); full significance testing outputs.

**Deliverable:** results/ directory contents; all figures referenced in the graduation report.

---

### Phase 4: Product Development

**Period:** May 4 – June 14, 2026 (Weeks 13–18)

**What is done:** This phase builds the Streamlit dashboard application and deploys it to Streamlit Community Cloud.

**How:** The application is structured as a five-page Streamlit multi-page app. Page 1 (Individual Report) allows a practitioner to select a client by name, view their predicted age gap alongside SHAP-based feature importance, and adjust biometric inputs via sliders to simulate interventions. Page 2 (Upload New Scan) accepts a CSV file from a new scan session, validates column completeness, runs the surrogate model, and displays risk and protective factors derived from SHAP values. Page 3 (Population View) shows the full 158-record age gap histogram with the current client marked by a vertical line, alongside an age versus age gap scatter plot for population context. Page 4 (Export PDF) generates a downloadable single-page matplotlib-based PDF report for use in advising sessions. Page 5 (About) provides a plain-language explanation of the tool's purpose, the distinction between the age gap and clinical biological age, and the known limitations. Shared utilities are centralised in app_utils.py to ensure consistency across pages.

**Input:** Production model from Health_Pipeline.ipynb; SHAP library; Phase 3 results for population statistics.

**Output:** zdravoletie_app.py; pages/ directory (five pages); app_utils.py; deployed application.

**Deliverable:** Live Streamlit application; GitHub repository with deployment configuration.

---

### Phase 5: Validation and Writing

**Period:** March 30 – June 21, 2026 (Weeks 8–19, concurrent with Phases 3 and 4)

**What is done:** This phase produces all written deliverables: the graduation report thesis chapters, the abstract and ethics chapter, the Plan of Approach, the logbook, and the competency portfolio.

**How:** Thesis chapters were written progressively in parallel with the experimental work, with introduction and related work produced during data preparation, methodology during the experiments, and results, discussion, conclusion, abstract, and ethics during and after the product development phase. The academic framing — score reverse-engineering rather than biological age prediction — is applied consistently across all chapters. All cross-references between chapters, table and figure numbering, and citation formats are verified in the final editing pass. The competency portfolio draws on documented evidence from all five phases, with structured reflection on each Fontys Applied Mathematics graduation competency. The logbook records activities, decisions, and communications for each project week.

**Input:** Experimental results from Phase 3; dashboard from Phase 4; all project artefacts; Fontys portfolio guidelines.

**Output:** thesis/ directory (nine chapter files); competency portfolio; this Plan of Approach; logbook.

**Deliverable:** Complete graduation report; competency portfolio; Plan of Approach; logbook — all submission-ready by June 22, 2026.

---

### Phase 6: Delivery and Defence

**Period:** June 22 – July 5, 2026 (Weeks 20 and beyond)

**What is done:** Final submission of all deliverables by the hard freeze date, followed by preparation and delivery of the oral defence presentation.

**How:** All deliverable files are assembled in the format required by Fontys and submitted through the designated submission channel by June 22. The defence presentation is structured around the three experiments and their findings, with proactive treatment of the known limitations — statistical underpowering, pseudo-label variance compression, the sentinel-value encoding of missing sportSafeRisk and sportLevel, and the aggregated_postural_index redundancy. Anticipated examiner questions on the framing correction, the inconclusive Experiment 1 results, and the Ridge exception in Experiment 2 are prepared in advance.

**Input:** All deliverables from Phase 5; final supervisor feedback.

**Output:** Submitted graduation report and portfolio; oral defence presentation.

**Deliverable:** Submission confirmation; oral defence on July 4–5, 2026.

---

## 4. Project Control

Project control is specified for each phase across five dimensions following the TOKIO framework: Time, Organisation, Information, Quality, and Money. For the Money dimension, the notional cost is computed as student hours at a reference rate of €25 per hour.

---

### Phase 1: Problem Analysis and Framing

| Dimension | Measure |
|---|---|
| Time | 80 hours across Weeks 1–10. Milestones: kickoff (W1), initial data audit complete (W3), midterm presentation (W9), all eleven bugs documented (W11). |
| Organisation | Student is solely responsible for all analysis and documentation. Educational supervisor Peter Alem provides the primary checkpoint at the midterm review (W9). Company supervisor Kostadin Galchin confirms data access and clinical context at kickoff. |
| Information | Progress communicated to Peter Alem at the midterm presentation. Decisions logged in the weekly logbook. CLAUDE.md written at phase end to lock project constraints. |
| Quality | All identified issues documented in writing before any fix is applied to prevent partial corrections. Reframing decision explicitly approved through the midterm feedback process. |
| Money | 80 hours × €25/hour = €2,000 (notional) |

---

### Phase 2: Data Collection and Engineering

| Dimension | Measure |
|---|---|
| Time | 160 hours across Weeks 1–12. Milestones: extraction complete (W2), integrity audit complete (W3), feature engineering pipeline complete (W4), production model artifact complete (W5), GMM synthetic dataset complete (W6). |
| Organisation | Student is solely responsible for data extraction, integrity analysis, and pipeline construction. Galchin confirms client consent coverage and provides domain context on variable definitions. |
| Information | Data quality issues documented in the Week 3 logbook entry. Feature engineering decisions recorded in the Week 4 logbook entry. Galchin updated on data volume and consent status at Week 2. |
| Quality | Imputation uses training-fold medians to prevent leakage. Derived features computed with a 0.1 additive denominator constant documented as a fixed decision in config.py. Feature set frozen in Health_Pipeline.ipynb; no changes after Phase 2 without explicit justification. |
| Money | 160 hours × €25/hour = €4,000 (notional) |

---

### Phase 3: Modeling and Experimentation

| Dimension | Measure |
|---|---|
| Time | 80 hours across Weeks 13–14. Milestones: Experiment 1 complete (W13), Experiment 2 complete (W13), Experiment 3 complete (W14), all results saved (W14). |
| Organisation | Student is solely responsible for experimental execution. All experiment parameters (random seed, fold count, alpha threshold) declared in config.py and not modified during execution. |
| Information | Results saved to results/ immediately upon generation. Statistical testing outputs archived alongside figures. Logbook entries for Weeks 13–14 document experimental decisions and unexpected findings. |
| Quality | Fixed random seed 42 for all stochastic operations. GroupShuffleSplit group constraint verified before each experiment run. Bonferroni correction applied consistently; all inconclusive comparisons reported as inconclusive rather than as evidence of equivalence. Failed or unexpected results retained and documented, not discarded. |
| Money | 80 hours × €25/hour = €2,000 (notional) |

---

### Phase 4: Product Development

| Dimension | Measure |
|---|---|
| Time | 100 hours across Weeks 13–18. Milestones: individual report page functional (W14), upload page functional (W14), population view with scatter plot complete (W14), PDF export functional (W14), About page complete (W14), deployment live (W14). |
| Organisation | Student is solely responsible for application development and deployment. Galchin is the primary stakeholder for the practical utility of the dashboard. Educational supervisor is informed of deployment status. |
| Information | Deployment URL communicated to Galchin when live. Application limitations (dependency on 158-record dataset, no real-time Anovator integration) stated plainly on the About page. |
| Quality | Column validation on file upload prevents silent failure from misnamed inputs. SHAP explanations computed fresh per prediction, not cached from training. Dashboard tested end-to-end on the production dataset before deployment. |
| Money | 100 hours × €25/hour = €2,500 (notional) |

---

### Phase 5: Validation and Writing

| Dimension | Measure |
|---|---|
| Time | 140 hours across Weeks 8–19. Milestones: introduction and related work drafts (W8–W12), methodology draft (W13), results draft (W14), discussion and conclusion drafts (W14), abstract and ethics drafts (W14), competency portfolio first draft (W18), final editing pass complete (W19). |
| Organisation | Student is solely responsible for all writing. Peter Alem reviews chapter drafts and the competency portfolio. Feedback incorporated before the June 22 hard freeze. |
| Information | Chapter drafts shared with Peter Alem via the designated submission channel. Feedback documented in the logbook. Cross-references between chapters verified in the final editing pass. |
| Quality | Score reverse-engineering framing applied consistently across all chapters. No single-split point estimates reported; all results cite 95% CI. Limitations acknowledged in the methodology chapter and carried through to discussion and conclusion. All table and figure numbers verified for consistency with in-text references. |
| Money | 140 hours × €25/hour = €3,500 (notional) |

---

### Phase 6: Delivery and Defence

| Dimension | Measure |
|---|---|
| Time | 40 hours across Weeks 19–20 and the defence period. Milestones: all deliverables submitted (June 22), presentation rehearsal complete (July 3), oral defence delivered (July 4–5). |
| Organisation | Student delivers the oral defence. Peter Alem chairs the academic assessment. Fontys processes the final grade. |
| Information | Submission confirmation archived. Defence slide deck shared with Peter Alem before the defence date for any final guidance. |
| Quality | Presentation addresses all three experiments, the midterm reframing, and the four documented limitations explicitly. Anticipated examiner questions on framing, inconclusive results, and the Ridge exception prepared in advance. |
| Money | 40 hours × €25/hour = €1,000 (notional) |

---

## 5. Budget and Planning

### 5.1 Total Hour and Cost Estimate

| Phase | Period | Hours | Notional Cost (€25/hour) |
|---|---|---|---|
| Phase 1: Problem Analysis and Framing | W1–W10 | 80 | €2,000 |
| Phase 2: Data Collection and Engineering | W1–W12 | 160 | €4,000 |
| Phase 3: Modeling and Experimentation | W13–W14 | 80 | €2,000 |
| Phase 4: Product Development | W13–W18 | 100 | €2,500 |
| Phase 5: Validation and Writing | W8–W19 | 140 | €3,500 |
| Phase 6: Delivery and Defence | W19–W20+ | 40 | €1,000 |
| **Total** | **W1–W20** | **600** | **€15,000** |

The notional hourly rate of €25 reflects a standard reference figure for student labour in the Netherlands and does not imply a commercial billing arrangement. Zdravoletie does not pay a fee for the internship; the cost estimate is provided for project management transparency and portfolio assessment purposes only. There are no hardware, software licensing, or infrastructure costs: all computations run on the student's own machine using open-source Python libraries, and the Streamlit Community Cloud deployment is free.

### 5.2 Gantt Chart Reference

The full week-by-week Gantt chart is maintained in thesis/gantt.md. The project spans twenty weeks from February 9 to June 27, 2026. Eight work packages are tracked: data extraction and audit (W1–W8), data preparation and modelling (W4–W12), Experiment 1 (W13–W14), Experiment 2 (W13–W14), Experiment 3 (W13–W14), Streamlit application development (W13–W18), thesis writing (W8–W19), and competency portfolio (W18–W19). A buffer and presentation preparation week is reserved at W20.

### 5.3 Milestones

| Milestone | Target Date | Status |
|---|---|---|
| Project kickoff and data extraction begun | February 9, 2026 | Complete |
| Initial data audit complete | March 1, 2026 | Complete |
| Production model and GMM synthetic dataset complete | March 22, 2026 | Complete |
| Midterm presentation delivered | April 6, 2026 | Complete |
| Project reframing and all eleven bugs fixed | May 3, 2026 | Complete |
| All three experiments complete, results saved | May 17, 2026 | Complete |
| Streamlit application deployed | May 17, 2026 | Complete |
| All thesis chapters complete | May 17, 2026 | Complete |
| Competency portfolio first draft | June 14, 2026 | Planned |
| All deliverables submission-ready | June 21, 2026 | Planned |
| Hard freeze — final submission | June 22, 2026 | Planned |
| Oral defence | July 4–5, 2026 | Planned |

---

## 6. Risk Analysis

The following table presents eight risks identified across the project lifecycle. Each risk is scored on three dimensions: Impact (I) on a scale of 1 to 5 from negligible to critical, Probability (P) on a scale of 1 to 5 from very unlikely to near certain, and Vulnerability (V) on a scale of 1 to 5 from well-mitigated to entirely unmitigated. The Risk Priority score (RP) is computed as I × P × V. Risks are ordered by descending RP.

| # | Risk | I | P | V | RP | Mitigation |
|---|---|:---:|:---:|:---:|:---:|---|
| R1 | Single researcher: no independent verification of implementation decisions, statistical analysis, or thesis writing | 3 | 5 | 3 | 45 | Systematic pre-fix audit completed before any code changes applied. CLAUDE.md written to lock framing, scope, and engineering conventions as an external constraint. All decisions logged in the weekly logbook. |
| R2 | Small dataset size (53 individuals): limits statistical power; most pairwise comparisons will be inconclusive at Bonferroni-corrected thresholds | 4 | 5 | 2 | 40 | Sample size acknowledged as a structural constraint, not a correctable limitation. All inconclusive results reported as inconclusive rather than misrepresented as equivalence. Consistent use of 30 folds and 95% CI reporting ensures honest characterisation. Additional data collection is outside project scope. |
| R3 | Statistical underpowering materialised: Experiment 1 and Experiment 3 produced no significant pairwise comparisons under Bonferroni correction at 30 folds | 4 | 5 | 2 | 40 | Treated as an honest finding. Inconclusive results accurately reported as statistical indeterminacy. Discussion section explains the mechanism — Bonferroni correction combined with limited fold count — and characterises the implications for interpretive confidence. |
| R4 | Reproducibility of scraping step: the Anovator web interface has no public API; data extraction was manual and the interface could change or become inaccessible | 4 | 3 | 2 | 24 | Full 158-record dataset saved to CSV in the data/ directory. Extraction procedure documented in the Week 2 logbook entry. The study does not depend on re-extraction; all experiments run from the saved CSV. |
| R5 | API access dependency resolved through manual extraction only: if additional data were needed, there would be no programmatic path to acquire it | 5 | 4 | 1 | 20 | Risk materialised and accepted at project inception; manual extraction was the only path. The 158-record dataset size was accepted as a fixed constraint and the experimental design was sized accordingly. Pseudo-labelled GMM synthetic data provides augmentation without requiring new real records. |
| R6 | Non-technical company supervisor: Galchin cannot provide methodological guidance on the modelling or statistical analysis; critical decisions must be made and justified by the student alone | 2 | 5 | 2 | 20 | Educational supervisor Peter Alem is the primary source of methodological guidance. Company supervisor role restricted to domain context and data access confirmation. All technical decisions documented in the logbook and thesis. |
| R7 | Deadline risk: June 22 hard freeze missed, resulting in incomplete or late submission | 5 | 2 | 2 | 20 | Gantt chart maintained in thesis/gantt.md. All experimental work, thesis writing, and dashboard development completed by May 17 — five weeks before the freeze. Remaining deliverable (competency portfolio) planned for Weeks 18–19. One-week buffer (W20) reserved before the oral defence. |
| R8 | Scope creep: additional experiments, alternative models, or extended feature engineering added beyond the three experiments defined in CLAUDE.md | 3 | 3 | 2 | 18 | CLAUDE.md explicitly lists all out-of-scope items. Out-of-scope suggestions are redirected to future_work.md rather than acted upon. Phase plan is fixed; no new experiments will be introduced in Phase 5 or Phase 6. |

---

## 7. Closing

This project addresses a clearly bounded and practically motivated problem: the interpretability gap in a proprietary health scoring system actively used by a rehabilitation clinic. The reverse-engineering framing adopted after the midterm review is scientifically honest, technically tractable with the available 158-record dataset, and directly relevant to the advising practice at Zdravoletie. The three experiments deliver structured empirical findings with full statistical accountability. The Streamlit dashboard translates those findings into a form that Zdravoletie practitioners can use without data science expertise. The framing and scope are non-negotiable and documented in CLAUDE.md; all deviations from the defined scope are redirected to future work rather than incorporated mid-project.

The student brings relevant preparation for this assignment. The Applied Mathematics programme with a Data Science major provides direct coverage of the methodological tools used in the study — regression analysis, cross-validation design, hypothesis testing, and probabilistic modelling — as well as the mathematical foundations required to interpret and critique their application. The mid-project structural restructuring, initiated in response to a serious framing error identified at the midterm, demonstrated willingness to revise a central design decision under academic pressure rather than defend a flawed prior commitment. The systematic eleven-bug audit, completed before any code was modified, reflected an engineering discipline appropriate to single-researcher work where no independent verification is available. The project proceeds to final submission and oral defence from a position in which all experimental work and all thesis chapters are complete, and the sole remaining deliverable is the competency portfolio.
