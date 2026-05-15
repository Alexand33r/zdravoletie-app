# Internship Logbook — Zdravoletie / Fontys University of Applied Sciences

**Student:** Alexander Tanev  
**Programme:** BSc Applied Mathematics, Data Science major  
**Company:** Zdravoletie, Varna, Bulgaria  
**Company supervisor:** Kostadin Galchin  
**Educational supervisor:** Peter Alem  
**Period:** February 9 – June 27, 2026  
**Oral defence:** July 4–5, 2026

---

## Week 1 — February 9–15

**Technical work:** Attended the project kickoff at Zdravoletie and familiarised myself with the Anovator body scanning platform. Explored the Anovator web interface to understand what data fields were available per scan session. Began mapping the available variables — body composition metrics, impedance readings, postural risk scores, joint angles, and the bodyAge score — against the project objective.

**Decisions made:** Decided that the primary target variable should be the age gap (bodyAge minus chronological age) rather than bodyAge directly. The motivation was to remove the trivially predictable chronological age component from the learning problem and focus modelling effort on the physiological deviation the Anovator formula computes.

**Communication:** Kickoff meeting with Kostadin Galchin at Zdravoletie. Discussed the clinic's use of the Anovator system in advising clients and the practical value of understanding which biometric measurements drive the bodyAge score. There were no formal onboarding procedures — Galchin confirmed full autonomy on the technical direction from the outset, which meant the research scope and methodology would be self-determined. The first week was spent getting familiar with the data formats, understanding the business context, and aligning on the end goals rather than receiving structured guidance.

**Challenges:** The Anovator web interface does not expose a public API. Understanding how to extract records programmatically — or whether manual export was the only option — required more time than expected and became the first independent problem to solve without technical support from the company side.

---

## Week 2 — February 16–22

**Technical work:** Began systematic data extraction from the Anovator web interface. Identified 158 individual scan records drawn from 53 unique clients, spanning sessions from 2022 to 2024. Set up the initial project repository and notebook structure. Began loading and inspecting records for completeness.

**Decisions made:** Confirmed the decision to extract records manually from the Anovator interface, as no automation path was available. Decided to treat the 158 records as a cross-sectional dataset rather than a longitudinal one, given that most clients had only two or three sessions and the time gaps between sessions were irregular.

**Communication:** Brief update to Kostadin Galchin on data volume. Confirmed that all 53 clients had consented to their data being used for research purposes as part of the clinic's standard practice.

**Challenges:** Some scan sessions had inconsistent variable formats across different years — column naming was not standardised across the export files, requiring manual cross-referencing to align records into a consistent dataset.

**[ALEXANDER TO FILL]:** Whether the data extraction process involved any specific technical tools or scripts, and whether Galchin was involved in identifying which client records to include. - Yes the data extraction invloved As a mathematican, I am used thinking outside the box and trying to find the most optimal and efficient way of running/doing things, so when I saw the format of links i received and the number of it (162), I really didn’t want to have to manually go to each link save them somewhere and then put in a excel table for later data scraping usage. So in order to extract the links from my Gmail and save them to an Excel file, I used Google Apps Scirpt. The idea is this script will scan my inbox fot the specific Anovator links, and paste them into a Google Sheet. Here is a step-by-step of how I did it with some AI suggestions.
I had to create a new Google Sheet file (Anovator Links)
Inside the file, go to Extensions > Apps Script
In the Script, used a code:
Save and run the code
Check the Excel output for validation 
This step created an Excel file - Anovator_Links.xlsx,


---

## Week 3 — February 23 – March 1

**Technical work:** Completed the initial data audit. The most significant finding was a systematic discrepancy in segmental fat measurements: for a subset of records, the sum of limb fat segments (left arm, right arm, left leg, right leg, trunk fat) did not match the Anovator-reported total body fat figure, with differences up to approximately 13 kg. Documented this discrepancy as a data quality issue. Began initial exploratory data analysis, including distribution plots for all key variables and the age gap target.

**Decisions made:** Decided to retain records with fat segment discrepancies rather than exclude them. The discrepancy appeared in a minority of records and was consistent with potential rounding behaviour in the Anovator platform rather than extraction errors. Excluding records based on this criterion would have reduced an already small dataset without a methodologically justified basis.

**Communication:** [ALEXANDER TO FILL: any communication this week with supervisors.] - Just the communication of switching the target varuable for the model, the company supervsour agreed on this. 

**Challenges:** Determining whether the fat segment discrepancy was a data extraction error or a property of the Anovator system's own computation required careful comparison of multiple records and cross-checking field definitions in the Anovator documentation.

**[ALEXANDER TO FILL]:** Any additional findings from the data audit that stood out, and whether the fat segment discrepancy was discussed with Galchin. - Yes we found that the intital idea to make a model with the target vriable - Score was a bad idea, as no mathemtiac model, calculations or anything could come close to be able to precisly predict this metric basically: Zdravoletie uses body scanners to help clients optimise their health. However, the standard reports from the hardware often provide a ”Health Score” that is nearly identical
for everyone. My initial analysis showed that 85% of scans receive a score of 98/100.
This ”ceiling effect” makes it impossible for consultants to track real progress or identify
early risks. Furthermore, the machine provides these numbers without explaining the
logic behind them

---

## Week 4 — March 2–8

**Technical work:** Built the feature engineering pipeline. Computed five derived features: sex binary encoding, muscle-to-fat ratio, upper-to-lower body muscle ratio, trunk-to-limb fat ratio (all three with a 0.1 additive constant in the denominator to prevent division by zero), and aggregated_postural_index (arithmetic mean of six individual postural risk scores). Identified five features with missingness above 88%: leftVision (94.3%), rightVision (92.4%), bloodMaxPressure (91.8%), bloodMinPressure (91.8%), and restingHeartRate (88.6%). Identified two features using -1 as a sentinel value for missing data: sportSafeRisk (37% missing) and sportLevel (70% missing).

**Decisions made:** Chose median imputation using the training fold median over mean or constant-value imputation. The feature distributions were skewed and median imputation is more robust to outliers. Decided to retain the five near-constant features and the two sentinel-encoded features for consistency with the production model artifact being built in Health_Pipeline.ipynb, and to document both as limitations.

**Communication:** [ALEXANDER TO FILL: any communication this week with supervisors.] - Again just presenting the features whihc would be removed for the final model chosen. 

**Challenges:** Determining the final feature set required iterative analysis — not all Anovator output fields could be used as model inputs, and some fields carried no information across most records.

**[ALEXANDER TO FILL]:** Whether any domain guidance from Galchin or external sources influenced which features to include. - Not really, from my analysis i shoewd to kostadin which features would be removed as they had no impact or little impact for the final model and he agreed with them.

---

## Week 5 — March 9–15

**Technical work:** Built the Health_Pipeline.ipynb production model notebook. Ran an initial model comparison across the five target regressors (Ridge, SVR, RandomForest, GradientBoosting, HistGradientBoosting) on the full feature set. Observed an R² of 0.98 for the top-performing models on the training-based evaluation. Began building Data_Gen.ipynb for Gaussian Mixture Model synthetic data generation.

**Decisions made:** Selected the five model families to span linear (Ridge), kernel (SVR), and ensemble (RandomForest, GradientBoosting, HistGradientBoosting) approaches. Decided against including neural networks on the grounds that 158 records is below the data scale at which meaningful neural training is feasible. No hyperparameter search was conducted at this stage; the focus was on establishing baselines.

**Communication:** [ALEXANDER TO FILL: any communication this week with supervisors.] - No communication fot this week.

**Challenges:** The R² of 0.98 was surprising given the dataset size. At this stage it was interpreted as a strong initial result. The evaluation protocol at this point was not fully specified — the circular benchmarking issue that would later be identified had not yet been noticed.

**[ALEXANDER TO FILL]:** Whether the R²=0.98 result was shared with anyone at this stage, and whether it prompted any immediate scepticism. - This result wasnot communicated with anyone, at this stage it was just a milestone which had to be later verifed/evlauted using the appropiate metrices. 

---

## Week 6 — March 16–22

**Technical work:** Built Benchmarkinig.ipynb with hyperparameter optimisation for the five models. The optimised models continued to show R² near 0.98 on the evaluation set. Generated the 1000-record GMM synthetic dataset in Data_Gen.ipynb using a five-component full-covariance GMM fitted to the 158 real records. Pseudo-labelled the synthetic records using the production model output. Began writing the interim report.

**Decisions made:** Selected five GMM components based on the approximate number of distinguishable body composition profiles in the dataset. Decided to use the production model (trained on all 158 records) as the pseudo-label source for the synthetic data, establishing a teacher-student distillation design.

**Communication:** [ALEXANDER TO FILL: any communication this week with supervisors.] - A short presneration of results and tehcnieques, with the feedback of having to be more clear and inshifhtful when presenting to buisness owenrs/stake holdeers with no so technical background and understanding.

**Challenges:** Writing the methodology section of the interim report was difficult because the project framing at this stage centred on "predicting biological age" — a framing that would later be identified as incorrect at the midterm review. The R²=0.98 result dominated the preliminary results section.

**[ALEXANDER TO FILL]:** Any specific feedback from Galchin on the synthetic data approach or the preliminary results. - No feedback from Galchin on the approaches or technique used, just his overall encourgement to conutnie doing my work and trying to rpesent understnable and clear results for buisness oweners. 

---

## Week 7 — March 23–29

**Technical work:** Continued writing the interim report. Drafted sections covering the project background, data collection procedure, feature engineering decisions, model selection rationale, and preliminary results. Produced visualisations: feature importance plots, correlation heatmaps, and initial model performance comparisons.

**Decisions made:** Structured the interim report around the biological age prediction framing that was current at the time — presenting bodyAge as a proxy for clinical biological age and framing the model performance in those terms. This framing would later be corrected following midterm feedback.

**Communication:** [ALEXANDER TO FILL: any meetings or updates with Peter Alem or Galchin during this week, and the channel through which the interim report was being prepared.]

**Challenges:** [ALEXANDER TO FILL: any specific writing difficulties, or challenges producing visualisations that were clear to a non-technical audience.]

**[ALEXANDER TO FILL]:** Whether there was an interim check-in with Peter Alem before the formal midterm that might have given early warning of the framing issue.

---

## Week 8 — March 30 – April 5

**Technical work:** Completed the interim report. Compiled results, finalisaed figures, and wrote the conclusion section of the interim document. Prepared the midterm presentation alongside the report, covering the project context, methodology, and R²=0.98 finding as the headline result.

**Decisions made:** Decided to present the R²=0.98 result as the primary performance finding while acknowledging the small dataset size as a limitation. In retrospect this was the point at which deeper investigation of the evaluation protocol would have uncovered the circular benchmarking issue, but it was not prioritised at this stage.

**Communication:** Submitted the interim report. [ALEXANDER TO FILL: submission date, submission channel, whether Galchin reviewed the interim report before submission.]

**Challenges:** Condensing several weeks of exploratory work into a coherent narrative for an academic audience required significant editing. The biological age framing created some difficulty in explaining why R²=0.98 did not imply clinical validity.

**[ALEXANDER TO FILL]:** Any Fontys-specific requirements for the interim report format or submission process, and whether there were any initial reactions from either supervisor upon submission.

---

## Week 9 — April 6–12

**Technical work:** Finalised and delivered the midterm presentation to Peter Alem. Received substantive feedback during the session. Began investigating the R²=0.98 result following the feedback.

**Decisions made:** Made the immediate decision after the midterm to halt new development pending resolution of the two issues raised: the framing problem (predicting biological age vs. reverse-engineering a proprietary score) and the suspicious performance result. Prioritised the R² investigation before any further modelling.

**Communication:** Midterm presentation to Peter Alem. Two critical points of feedback were raised: (1) the biological age framing was incorrect — the target variable is the Anovator's own proprietary score, not a clinically validated measure of biological ageing, and any claims about predicting biological age would need to be retracted; (2) an R² of 0.98 on a 158-record dataset with this level of noise in the target variable was implausible and indicated a methodological problem. [ALEXANDER TO FILL: the exact setting of the presentation, whether it was in person or remote, and any additional feedback that was given on the report structure or writing.]

**Challenges:** Receiving feedback that the primary result of the project was an artefact of a methodological error was a significant setback. Reconstructing confidence in the project direction required careful thought about what the data could actually support.

**[ALEXANDER TO FILL]:** Personal reaction to the midterm feedback, and whether Galchin was informed of the outcome.

---

## Week 10 — April 13–19

**Technical work:** Identified the circular benchmarking bug. The Benchmarkinig.ipynb notebook was evaluating models on data derived from the same population used to train the production model that generated the pseudo-labels. Because the 1000 synthetic records were pseudo-labelled by a model trained on all 158 real records, and the evaluation then used an overlapping set, the test set was not genuinely held out. This explained R²=0.98. Began tracing the data flow across all eight notebooks to identify all affected evaluations.

**Decisions made:** Decided to reframe the project as reverse-engineering the Anovator bodyAge score rather than predicting clinical biological age. This reframing was both scientifically correct (the ground truth is the Anovator formula's output, not a clinical endpoint) and consistent with the data available. It also resolved the concern Peter Alem raised: the new framing makes no claim about clinical validity.

**Communication:** [ALEXANDER TO FILL: any follow-up communication with Peter Alem after the midterm, and whether the reframing decision was discussed with Galchin.]

**Challenges:** Tracing the circular data flow across multiple notebooks took longer than expected. The bug was not a single-line error but a structural design issue in how synthetic data generation and evaluation had been sequenced.

**[ALEXANDER TO FILL]:** Whether any intermediate findings were shared with supervisors during the investigation, or whether the full findings were held until they were complete.

---

## Week 11 — April 20–26

**Technical work:** Conducted a systematic audit of all eight notebooks. Documented eleven distinct methodological and implementation issues: (1) circular benchmarking in Benchmarkinig.ipynb; (2) feature leakage in Age_Pred.ipynb where correlations were computed on the full dataset before splitting; (3) a NameError in Data_Gen.ipynb when df_real_imputed was referenced before definition; (4) duplicate GMM training where df_synth was re-fitted rather than copied; (5) fillna(0) used where training-set medians should be applied; (6) a Streamlit sidebar number_input call that did not match the API; (7) BMI not recalculated in the simulation flow; (8) the small test set size not flagged at runtime; (9) single cross-validation split in Health_Pipeline.ipynb instead of repeated CV; (10) the preprocess_client_scan function duplicated in three locations (verified consistent — no bug); (11) negative R² values reported without explanation. All eleven were documented before any fix was applied.

**Decisions made:** Decided to complete the full audit before starting fixes to avoid partial corrections that might interact with undiscovered issues. Prioritised fixes by impact on experimental validity, with the circular benchmarking and feature leakage bugs as the highest priority.

**Communication:** [ALEXANDER TO FILL: any updates to supervisors during the audit process.]

**Challenges:** Some bugs interacted with others — fixing the circular benchmarking evaluation protocol changed the baseline against which other results would be interpreted, requiring reconsideration of what "correct" results would look like for the subsequent experiments.

**[ALEXANDER TO FILL]:** Whether the audit findings were surprising in their scope, and whether any of the eleven issues had been previously noticed but set aside.

---

## Week 12 — April 27 – May 3

**Technical work:** Fixed all eleven identified bugs across the relevant notebooks. Built config.py centralising the fixed random seed (42), all file paths, the cross-validation protocol specification, the model registry with hyperparameters, and the feature group definitions. Wrote requirements.txt. Built make_all.py to execute the full eight-notebook pipeline via nbconvert. Created the results/ and thesis/ directories. Wrote future_work.md to log all out-of-scope items formally.

**Decisions made:** Wrote CLAUDE.md to lock the project framing, scope, engineering conventions, and phase plan going forward. This was necessary after the project had been substantially restructured: a single source of truth for project constraints would prevent inadvertent scope creep or framing drift in subsequent work. Fixed random seed 42 declared once in config.py and imported everywhere — no local overrides.

**Communication:** [ALEXANDER TO FILL: any updates to supervisors on the restructuring, and whether Galchin was aware of the scale of the bug-fixing effort.]

**Challenges:** Ensuring that the three copies of the preprocess_client_scan function across different notebooks remained consistent after the bug fixes required careful verification. No automated test suite existed, so consistency had to be checked manually.

**[ALEXANDER TO FILL]:** Whether the scope of the restructuring effort was communicated to Peter Alem at this point, and his response if so.

---

## Week 13 — May 4–10

**Technical work:** Ran all three core experiments with the corrected evaluation protocol. Experiment 1: 30 repeated GroupShuffleSplit folds (grouped by client name, 80/20 split of the 53 individuals), evaluating five models on MAE, RMSE, and R². HistGradientBoosting achieved the lowest mean MAE at 2.43 years (95% CI [2.09, 2.76]); all ten pairwise Wilcoxon signed-rank tests were inconclusive at Bonferroni-corrected alpha = 0.005. Experiment 2: three training regimes (RealOnly, RealPlusSynth, SynthOnly) for all five models. RealPlusSynth produced statistically significant MAE reductions for four models (adjusted p-values 0.000004 to 0.002855); Ridge degraded substantially under SynthOnly (mean MAE 3.23 years versus 2.48 baseline). Experiment 3: cumulative feature group ablation with HistGradientBoosting. G1 (63 features) achieved the lowest mean MAE at 2.39 years; all six group-pair comparisons inconclusive at Bonferroni-corrected alpha = 0.0083. Saved all result tables and figures to results/.

**Decisions made:** The GroupShuffleSplit grouping on client name was essential: without it, records from the same individual would appear in both training and test folds, allowing the model to exploit within-person biometric consistency rather than generalising across individuals. The Bonferroni correction was applied in preference to less conservative alternatives to control the risk of false positive significance claims — the primary error type of concern given the small sample.

**Communication:** [ALEXANDER TO FILL: any mid-week updates to supervisors, or any informal sharing of the preliminary experiment results.]

**Challenges:** All three experiments produced predominantly inconclusive results under the Bonferroni-corrected testing regime. This required careful re-reading of the statistical literature on inconclusive results to ensure they were reported correctly — as genuine statistical indeterminacy rather than evidence of equivalence. The Ridge degradation under SynthOnly was initially puzzling; tracing it to the pseudo-label variance compression took additional analysis.

**[ALEXANDER TO FILL]:** Whether the inconclusive outcomes from Experiment 1 were discussed with either supervisor, and any response.

---

## Week 14 — May 11–17

**Technical work:** Wrote six thesis chapters: Introduction (~995 words establishing context, research question, scope, and practical significance), Related Work (~2,074 words covering biological age literature, synthetic data generation methods, and SHAP in health ML), Methodology (~2,637 words with full protocol documentation and four stated limitations), Results (~1,900 words including the reliability curve subsection, GMM fidelity metric subsection, and all result tables), Discussion (~2,904 words with five discussion points, four limitations addressed, and SHAP feature interpretation), and Conclusion (~1,138 words with sub-question answers and six future work items). Also wrote the Abstract (~303 words) and Ethics chapter (~800 words). Rebuilt the Streamlit dashboard as a five-page application: Individual Report, Upload New Scan, Population View (with age vs. age_gap scatter plot), Export PDF, and About. Deployed to Streamlit Community Cloud. Wrote the plan of approach, Gantt chart, and this logbook.

**Decisions made:** Structured the reliability curve analysis around the Unknown-group composition issue to be transparent about the inflated per-prediction error statistics relative to the fold-level MAE. Reported the GMM fidelity metric (Frobenius norm of the correlation matrix difference = 2.46 over a 79×79 matrix, normalised 0.031 per feature) as a validation step, not as a headline claim. Chose a cumulative additive structure for Experiment 3's feature group ordering based on data collection complexity, with the cheapest measurements (anthropometric) forming the base.

**Communication:** [ALEXANDER TO FILL: any updates to Peter Alem or Galchin this week, and whether the deployed Streamlit dashboard was demonstrated to Galchin.]

**Challenges:** Maintaining narrative consistency across six thesis chapters written in the same period required deliberate cross-referencing. The discussion chapter required care to avoid overstating the significance of inconclusive results or understating what the significant findings from Experiment 2 do establish.

**[ALEXANDER TO FILL]:** Whether the Streamlit deployment was demonstrated to the clinic, and any practical response from Galchin to seeing the working dashboard.

---

## Week 15 — May 18–24 *(Planned)*

**Technical work:** Begin competency portfolio. Draft the section on Research Competency: framing and evidence of the reverse-engineering research question, the experimental design choices, and the evaluation of results. Review all thesis chapters for consistency in terminology and cross-references.

**Communication:** Planned check-in with Peter Alem to confirm the thesis chapter structure and whether any revisions to framing or content are required before the final writing phase.

**[ALEXANDER TO FILL]:** Actual activities and any deviations from plan.

---

## Week 16 — May 25–31 *(Planned)*

**Technical work:** Continue competency portfolio. Draft the section on Professional Development Competency: self-direction in a non-technical company environment, decision-making under uncertainty, and project restructuring in response to academic feedback.

**Communication:** Planned progress update to Galchin. Share the current state of the thesis and portfolio.

**[ALEXANDER TO FILL]:** Actual activities and any deviations from plan.

---

## Week 17 — June 1–7 *(Planned)*

**Technical work:** Continue competency portfolio. Draft remaining competency sections. Begin final review pass on the graduation report for consistency, formatting, and academic register.

**Communication:** Planned progress check with Peter Alem, focusing on the competency portfolio content and whether the evidence base for each competency is sufficient.

**[ALEXANDER TO FILL]:** Actual activities and any deviations from plan.

---

## Week 18 — June 8–14 *(Planned)*

**Technical work:** Complete the competency portfolio first draft. Begin the final editing pass on the graduation report: resolve any remaining inconsistencies across chapters, verify all table and figure numbering, and ensure all cross-references between chapters are correct.

**Communication:** Planned submission of the competency portfolio draft to Peter Alem for review. Planned final update to Galchin.

**[ALEXANDER TO FILL]:** Actual activities and any deviations from plan.

---

## Week 19 — June 15–21 *(Planned)*

**Technical work:** Incorporate any feedback on the competency portfolio and graduation report. Complete all final revisions. Prepare all deliverable files for submission in the format required by Fontys.

**Communication:** Final feedback meeting with Peter Alem before the June 22 hard freeze. Confirm that both deliverables are submission-ready.

**[ALEXANDER TO FILL]:** Actual activities and any deviations from plan.

---

## Week 20 — June 22–27 *(Planned)*

**Technical work:** Submit all deliverables by June 22 hard freeze. Prepare the oral defence presentation: structure the narrative around the three experiments and their findings, address the known limitations proactively, and prepare answers to anticipated examiner questions on the framing, the inconclusive results, and the Ridge exception in Experiment 2.

**Communication:** Final communication with both supervisors confirming submission. Begin rehearsal of the oral defence presentation.

**[ALEXANDER TO FILL]:** Actual activities and any final preparation notes.

---

*Oral defence scheduled for July 4–5, 2026.*
