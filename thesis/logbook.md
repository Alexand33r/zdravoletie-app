# Internship Logbook — Zdravoletie / Fontys University of Applied Sciences

**Student:** Alexander Tanev  
**Programme:** BSc Applied Mathematics, Data Science major  
**Company:** Zdravoletie, Burgas, Bulgaria  
**Company supervisor:** Kostadin Galchin  
**Educational supervisor:** Peter P.A.L. van Alem  
**Period:** February 9 – June 22, 2026  
**Oral defence:** July 3 and July 7, 2026

---

## Week 1 — February 9–15

**Technical work:** Attended the project kickoff at Zdravoletie and familiarised myself with the Anovator body scanning platform. Explored the Anovator web interface to understand what data fields were available per scan session. Began mapping the available variables — body composition metrics, impedance readings, postural risk scores, joint angles, and the bodyAge score — against the project objective.

**Decisions made:** Began mapping available variables against the project objective. No target variable decision was made at this stage — the initial focus was on understanding the data structure and the business context.

**Communication:** Kickoff meeting with Kostadin Galchin at Zdravoletie. Discussed the clinic's use of the Anovator system in advising clients and the practical value of understanding which biometric measurements drive the bodyAge score. There were no formal onboarding procedures — Galchin confirmed full autonomy on the technical direction from the outset, which meant the research scope and methodology would be self-determined. The first week was spent getting familiar with the data formats, understanding the business context, and aligning on the end goals rather than receiving structured guidance.

**Challenges:** The Anovator web interface does not expose a public API. Understanding how to extract records programmatically — or whether manual export was the only option — required more time than expected and became the first independent problem to solve without technical support from the company side.

---

## Week 2 — February 16–22

**Technical work:** Began systematic data extraction from the Anovator web interface. Identified 158 individual scan records drawn from 53 unique clients, spanning sessions from 2022 to 2024. Set up the initial project repository and notebook structure. Began loading and inspecting records for completeness.

**Decisions made:** Confirmed the decision to automate data extraction rather than process each record manually. With 162 scan links delivered via email, manually visiting each URL and copying data into a spreadsheet was not a viable approach. Decided to treat the 158 records as a cross-sectional dataset rather than a longitudinal one, given that most clients had only two or three sessions and the time gaps between sessions were irregular.

**Communication:** Brief update to Kostadin Galchin on data volume and extraction approach. Confirmed that all 53 clients had consented to their data being used for research purposes as part of the clinic's standard intake practice.

**Challenges:** Some scan sessions had inconsistent variable formats across different years — column naming was not standardised across export files, requiring manual cross-referencing to align records into a consistent dataset. Additionally, the Anovator platform had no public API, so the extraction method had to be reverse-engineered from the URL structure of the scan links.

**Technical approach — data extraction:** Receiving 162 Anovator scan links by email, I identified that manually processing each one was inefficient and error-prone. Applying the same analytical thinking I use in modelling — finding the most systematic path through a problem — I wrote a Google Apps Script to scan my Gmail inbox for Anovator links automatically and export them to a Google Sheet, which was then saved as Anovator_Links.xlsx. This became the input for the subsequent API-based extraction pipeline. The decision to automate this step from the outset established a reproducible data collection process and avoided the transcription errors that manual copying would have introduced.


---

## Week 3 — February 23 – March 1

**Technical work:** Completed the initial data audit. The most significant finding was a systematic discrepancy in segmental fat measurements: for a subset of records, the sum of limb fat segments (left arm, right arm, left leg, right leg, trunk fat) did not match the Anovator-reported total body fat figure, with differences of up to approximately 13 kg. Documented this discrepancy as a data quality issue and began initial exploratory data analysis, including distribution plots for all key variables and the age gap target.

**Decisions made:** Two decisions were made this week, both consequential for the rest of the project. First, decided to retain records with fat segment discrepancies rather than exclude them — the pattern was consistent with rounding behaviour in the Anovator platform rather than extraction errors, and exclusion would have reduced an already small dataset without methodological justification. Second, and more significantly, decided to abandon the hardware Score as the modelling target. Initial analysis revealed that 85% of all scans receive a Score of 98/100 — a ceiling effect so severe that no regression model could meaningfully differentiate between clients. This finding redirected the entire project toward the age gap (bodyAge minus chronological age) as the primary target, a variable with a continuous range and genuine discriminative power.

**Communication:** Discussed the Score ceiling effect with Kostadin Galchin and proposed switching the modelling target to the age gap. Galchin agreed with the rationale and confirmed the change in direction. This was the first significant technical decision that required justifying an analytical finding to a non-technical stakeholder — explaining why a metric the company had been using was statistically unusable required framing the argument around practical consultant value rather than statistical theory.

**Challenges:** Determining whether the fat segment discrepancy was a data extraction error or a property of the Anovator system's own computation required careful comparison of multiple records and cross-checking field definitions in the Anovator documentation. The answer — that Anovator uses non-linear internal formulas — would later become a central motivation for the reverse-engineering framing of the thesis.
---

## Week 4 — March 2–8

**Technical work:** Built the feature engineering pipeline. Computed five derived features: sex binary encoding, muscle-to-fat ratio, upper-to-lower body muscle ratio, trunk-to-limb fat ratio (all three with a 0.1 additive constant in the denominator to prevent division by zero), and aggregated_postural_index as the arithmetic mean of six individual postural risk scores. Identified five features with missingness above 88% and two features using -1 as a sentinel value for missing data: sportSafeRisk (37% missing) and sportLevel (70% missing).

**Decisions made:** Chose median imputation using the training fold median over mean or constant-value imputation — feature distributions were skewed and median imputation is more robust to outliers. Decided to retain the five near-constant features and the two sentinel-encoded features rather than drop them, documenting both as acknowledged limitations. This decision was made consciously: dropping features purely on missingness grounds without understanding their clinical meaning risked discarding potentially relevant signal, while retaining them with documented caveats is the more defensible methodological position.

**Communication:** Presented the proposed feature selection to Kostadin Galchin — specifically which variables would be excluded from the final model and the analytical reasoning behind each exclusion. Galchin reviewed the list and agreed with the proposed removals. This interaction was characteristic of the communication pattern established early in the project: analytical decisions were made independently, then explained to the company supervisor in accessible terms for validation rather than guidance. Galchin's role was to confirm that the exclusions made practical sense from a clinic perspective, not to direct the technical methodology.

**Challenges:** Determining the final feature set required iterative analysis — not all Anovator output fields could be used as model inputs, and some carried no meaningful information across most records. Without domain expertise in exercise physiology or bioimpedance measurement, feature selection decisions had to be grounded entirely in statistical evidence rather than clinical knowledge, which is a limitation acknowledged in the thesis methodology.
---

## Week 5 — March 9–15

**Technical work:** Built the Health_Pipeline.ipynb production model notebook. Ran an initial model comparison across the five target regressors (Ridge, SVR, RandomForest, GradientBoosting, HistGradientBoosting) on the full feature set. Observed an R² of 0.98 for the top-performing models on the training-based evaluation. Began building Data_Gen.ipynb for Gaussian Mixture Model synthetic data generation.

**Decisions made:** Selected the five model families to span linear (Ridge), kernel (SVR), and ensemble (RandomForest, GradientBoosting, HistGradientBoosting) approaches — a deliberate choice to cover the methodological spectrum rather than converging prematurely on one family. Decided against including neural networks on the grounds that 158 records is below the data scale at which meaningful neural training is feasible. No hyperparameter search was conducted at this stage; the focus was on establishing baselines before committing to an evaluation protocol.

**Communication:** No supervisor communication this week. The work was entirely technical and self-directed. The R² of 0.98 result was not shared at this stage — it was treated as an intermediate milestone requiring further verification rather than a finding to report.

**Challenges:** The R² of 0.98 was higher than expected given the dataset size. At the time it was interpreted cautiously as a strong preliminary result pending proper evaluation. In retrospect this was the point at which a more experienced research environment — with a technical supervisor or peer reviewer — might have flagged the result as suspicious immediately. The circular benchmarking issue that produced this inflated metric had not yet been identified. This week illustrates a structural limitation of the internship: without a technical peer to challenge interim results, flawed findings can persist longer than they should before being caught through self-review.

---

## Week 6 — March 16–22

**Technical work:** Built Benchmarking.ipynb with hyperparameter optimisation for the five models. The optimised models continued to show R² near 0.98 on the evaluation set. Generated the 1,000-record GMM synthetic dataset in Data_Gen.ipynb using a five-component full-covariance GMM fitted to the 158 real records. Pseudo-labelled the synthetic records using the production model output, establishing a teacher-student distillation design. Began writing the interim report.

**Decisions made:** Selected five GMM components based on the approximate number of distinguishable body composition profiles observable in the dataset — a pragmatic choice made without formal BIC/AIC component selection, which is acknowledged as a limitation in the final thesis. Decided to use the production model trained on all 158 records as the pseudo-label source for the synthetic data. At this stage the circular dependency this created — the teacher model being the same model later benchmarked against the pseudo-labels — had not yet been identified.

**Communication:** Presented a progress summary to Kostadin Galchin covering the synthetic data generation approach and preliminary results. The feedback received was significant: Galchin noted that the presentation was too technical and not sufficiently clear for a business owner or non-specialist audience. This was direct and useful feedback, even if brief. It prompted reflection on the gap between technical rigour and communicative accessibility — a theme that would run through the rest of the internship and became the basis for the professionalisation learning objective. Galchin's overall response was encouraging, with the emphasis that results should be framed around what they mean for clients and consultants rather than how they were computed.

**Challenges:** Writing the methodology section of the interim report was difficult because the project framing at this stage centred on "predicting biological age" — a framing that would later be identified as incorrect at the midterm review. The R²=0.98 result dominated the preliminary results section and was presented with more confidence than the evaluation protocol warranted. In hindsight, this week marked the peak of the project's most significant methodological error: a compelling-looking result built on a flawed benchmarking design, written into a formal document before the flaw was caught.
---

## Week 7 — March 23–29

**Technical work:** Continued writing the interim report. Drafted sections covering the project background, data collection procedure, feature engineering decisions, model selection rationale, and preliminary results. Produced visualisations: feature importance plots, correlation heatmaps, and initial model performance comparisons. Began formatting the document in LaTeX for a more structured and professional academic output.

**Decisions made:** Structured the interim report around the biological age prediction framing that was current at the time — presenting bodyAge as a proxy for clinical biological age and framing the model performance accordingly. This framing reflected the understanding of the project at that point and would later be corrected following midterm feedback. The decision to use LaTeX rather than a word processor was made independently, motivated by the need for proper equation formatting, consistent figure referencing, and a document structure appropriate for an academic submission.

**Communication:** No formal updates to either Peter P.A.L. van Alem or Kostadin Galchin this week. The focus was entirely on writing. There was no interim check-in with Peter P.A.L. van Alem before the formal midterm — the expectations for the interim presentation had been established in a previous conversation and were understood to be indicative rather than graded. This absence of an intermediate feedback loop meant the biological age framing in the report went unchallenged until the midterm itself. In retrospect, proactively sharing a draft section with the educational supervisor earlier would have been a better approach and is something I would do differently in a future research project.

**Challenges:** The primary challenge this week was not technical but presentational — producing visualisations and written sections that were rigorous enough for an academic audience while remaining accessible to a non-specialist reader. Working in LaTeX added a layer of formatting overhead but produced a significantly more professional output than a standard word processor would have allowed. The biological age framing, while internally consistent at this stage, introduced a conceptual tension that was not yet visible: the model was learning to approximate Anovator's proprietary formula, not predicting clinical biological age in any validated sense.

## Week 8 — March 30 – April 5

**Technical work:** Completed a working draft of the interim report. Compiled results, finalised figures, and wrote the conclusion section of the interim document. Continued refining the codebase alongside the writing — the two workstreams ran in parallel rather than sequentially. Prepared the structure and slide content for the midterm presentation scheduled for April 22, covering project context, methodology, and the R²=0.98 finding as the headline result.

**Decisions made:** Decided to present the R²=0.98 result as the primary performance finding while acknowledging the small dataset size as a limitation. In retrospect this was the point at which deeper investigation of the evaluation protocol would have uncovered the circular benchmarking issue — the result was too clean for a dataset of 158 records and should have prompted more scrutiny. The decision not to investigate further at this stage is an honest reflection of the limitations of working without a technical peer reviewer.

**Communication:** Shared a summary of findings with Kostadin Galchin — not a formal review of the interim report, but an explanation of what had been built and what the preliminary results showed. The purpose was to keep the company supervisor informed rather than to seek technical validation. Galchin's response was positive and encouraging. The interim report itself was not formally submitted at this stage — the midterm presentation was scheduled for April 22 and the report was still being refined. The Fontys interim deliverables are non-graded, which meant the primary purpose of the presentation was to receive directional feedback from Peter P.A.L. van Alem rather than to meet a formal submission requirement.

**Challenges:** Condensing several weeks of exploratory work into a coherent narrative for an academic audience required significant editing. The biological age framing created a subtle difficulty: explaining why R²=0.98 did not imply clinical validity required careful wording that acknowledged the result's strength while not overclaiming its meaning. This tension — between a technically impressive number and its actual research significance — would become the central issue raised at the midterm three weeks later.

---

## Week 9 — April 6–12

**Technical work:** Reviewed the interim report for internal consistency and accuracy. Refined the midterm presentation slides, ensuring the narrative flowed clearly from project context through methodology to the R²=0.98 headline result. Finalised all figures and ensured the slide deck was self-contained for an academic audience unfamiliar with the Anovator platform.

**Decisions made:** No major methodological decisions this week. The focus was on communication quality — ensuring the interim report and presentation accurately represented the work done without overclaiming on the preliminary results. The interim report was submitted approximately one week before the April 22 presentation date, in line with Fontys guidance. No specific formatting requirements applied beyond standard academic document conventions.

**Communication:** No supervisor communication this week. The interim report had been substantially completed and the presentation was in final preparation. This was an entirely self-directed week — without a technical supervisor to review the submission, the quality check relied entirely on self-review. The biological age framing and the R²=0.98 result were both presented with confidence at this stage, as no external challenge to either had yet been received.

**Challenges:** The primary challenge was one that only became visible in retrospect: preparing a presentation built around a result and a framing that would both be questioned the following week. At the time the preparation felt thorough. In hindsight this week illustrates the risk of self-contained work without peer review — it is possible to be internally consistent and externally wrong simultaneously, and the only way to discover that is through external feedback.

---

## Week 10 — April 13–19

**Technical work:** Conducted final rehearsals of the midterm presentation. Reviewed slide content and narrative against anticipated examiner questions. Made minor refinements to figures and supporting material based on the rehearsal. No new modelling or data work this week — the focus was entirely on preparation for the April 22 review.

**Decisions made:** Confirmed the presentation structure would prioritise the R²=0.98 finding as the headline result while contextualising it within the acknowledged limitation of small dataset size. In hindsight this framing prioritised the most visually impressive number over a more cautious interpretation — a decision that reflected confidence in the result rather than scepticism about the evaluation protocol behind it.

**Communication:** No supervisor communication this week ahead of the scheduled April 22 midterm. The presentation had been self-prepared throughout and would be reviewed externally for the first time at the midterm itself.

**Challenges:** Presentations have not historically been my strongest area, and this one carried additional pressure given the academic context and the presence of a formal evaluator. Significant effort went into ensuring the slides were clear, the content was structured logically, and the delivery was rehearsed sufficiently to handle follow-up questions. Going into the review, some concerns were anticipated — primarily around the depth of the interim report, the level of academic substantiation, and the use of external sources. What was not anticipated was a fundamental challenge to the project framing or a questioning of the headline performance result. The feedback that arrived on April 22 therefore went further than expected in both directions: more directional than anticipated on the framing, and more sceptical than anticipated on the methodology.
---

## Week 11 — April 20–26

**Technical work:** On April 22, delivered the midterm presentation to Peter P.A.L. van Alem. Following the verbal feedback received during the session, immediately began a full systematic audit of all notebooks as a direct response. Identified the circular benchmarking bug as the root cause of the R²=0.98 result: Benchmarking.ipynb was evaluating models on data derived from the same population used to train the production model that generated the pseudo-labels, making the test set not genuinely held out. Traced this data flow across all eight notebooks to identify all affected evaluations. Documented eleven distinct methodological and implementation issues in total before applying any fix.

**Decisions made:** Made the immediate decision after the midterm to halt new development pending resolution of the issues raised. Decided to complete the full audit before starting any fixes to avoid partial corrections that might interact with undiscovered issues. Prioritised fixes by impact on experimental validity, with the circular benchmarking and feature leakage bugs as the highest priority. Also decided immediately to reframe the project as reverse-engineering the Anovator bodyAge score rather than predicting clinical biological age — both scientifically correct and resolving the central concern Peter P.A.L. van Alem raised. This reframing decision was made independently and quickly, which in retrospect reflects a degree of professional maturity: rather than defending the original framing, the feedback was accepted and acted on without delay.

**Communication:** Midterm presentation to Peter P.A.L. van Alem on April 22 — delivered remotely via video call. Two critical points of verbal feedback were raised during the session: first, the biological age framing was incorrect — the target variable is the Anovator's proprietary score, not a clinically validated measure of biological ageing; second, an R² of 0.98 on a 158-record dataset was implausible and indicated a methodological problem. Formal written feedback from Peter P.A.L. van Alem was scheduled for the follow-up meeting on May 12, meaning the audit and reframing work in the weeks that followed was initiated on the basis of the verbal feedback alone, without waiting for the written assessment. Kostadin Galchin was informed of the outcome in broad terms — that the project was being restructured in response to academic feedback — without going into technical detail about the specific bugs identified.

**Challenges:** Receiving feedback that the headline result of the project was an artefact of a methodological error was the most significant setback of the internship. The immediate challenge was not technical but psychological — reconstructing confidence in the project direction and identifying what the data could genuinely support. The decision to treat the feedback as an opportunity to improve the research rather than as a criticism to defend against was a deliberate choice, and one that defined the trajectory of the second half of the internship. Some bugs also interacted with others: fixing the circular benchmarking protocol changed the baseline against which all subsequent results would be interpreted, requiring a full reconsideration of what valid results would look like. The personal reaction to the midterm feedback was initially one of disorientation — the two issues raised were not minor refinements but fundamental challenges to the project's primary result and framing. The response, however, was to treat the feedback as a course correction rather than a failure. None of the eleven issues had been previously identified and set aside; the circular benchmarking design had not been recognised as problematic before the midterm.

---

## Week 12 — April 27 – May 3

**Technical work:** Fixed all eleven identified bugs across the relevant notebooks. Built config.py centralising the fixed random seed (42), all file paths, the cross-validation protocol specification, the model registry with hyperparameters, and the feature group definitions. Wrote requirements.txt and built make_all.py to execute the full eight-notebook pipeline via nbconvert. Created the results/ and thesis/ directories. Wrote future_work.md to log all out-of-scope items formally. Wrote a project constraints document locking the revised framing, scope, engineering conventions, and phase plan — necessary after the restructuring to prevent scope creep or framing drift in subsequent work.

**Decisions made:** Decided to complete all infrastructure work before running any new experiments. The rationale was that running experiments on an unstable codebase — even with correct evaluation protocols — would produce results that could not be reliably reproduced. Fixed random seed 42 declared once in config.py and imported everywhere with no local overrides, ensuring full reproducibility across all subsequent experiment runs.

**Communication:** Updated Kostadin Galchin on the restructuring in broad terms — that a systematic review had identified issues in the initial evaluation approach and that the project was now on a corrected footing. Galchin was supportive, though the technical specifics of the bug-fixing effort were not something he could meaningfully evaluate given his non-technical background. No meeting with Peter P.A.L. van Alem this week — the bi-weekly schedule meant the next check-in was not due until the May 12 meeting, at which point the formal written midterm feedback would also be shared.

**Challenges:** Ensuring that the three copies of the preprocess_client_scan function across different notebooks remained consistent after the bug fixes required careful manual verification. No automated test suite existed, so consistency had to be checked by reading and comparing the implementations directly. This was time-consuming but necessary — an inconsistency between the training pipeline and the inference pipeline would have introduced a data leakage equivalent at prediction time.
---

## Week 13 — May 4–10

**Technical work:** Ran all three core experiments with the corrected evaluation protocol. Experiment 1: 30 repeated GroupShuffleSplit folds grouped by client name, evaluating five models on MAE, RMSE, and R². HistGradientBoosting achieved the lowest mean MAE at 2.43 years (95% CI [2.09, 2.76]); all ten pairwise Wilcoxon signed-rank tests were inconclusive at Bonferroni-corrected alpha = 0.005. Experiment 2: three training regimes across all five models — RealPlusSynth produced statistically significant MAE reductions for four models (adjusted p-values 0.000004 to 0.002855); Ridge degraded substantially under SynthOnly (mean MAE 3.23 years versus 2.48 baseline). Experiment 3: cumulative feature group ablation with HistGradientBoosting — G1 (63 features) achieved the lowest mean MAE at 2.39 years; all six group-pair comparisons inconclusive at Bonferroni-corrected alpha = 0.0083. All result tables and figures saved to results/.

**Decisions made:** The GroupShuffleSplit grouping on client name was essential — without it, records from the same individual would appear in both training and test folds, allowing the model to exploit within-person biometric consistency rather than generalising across individuals. The Bonferroni correction was applied in preference to less conservative alternatives to control the risk of false positive significance claims, which is the primary error type of concern given the small sample size. Both decisions reflect the influence of the midterm feedback: the corrected evaluation protocol was a direct product of the circular benchmarking investigation, and the conservative statistical threshold was chosen precisely because overclaiming had already cost the project three weeks of rework.

**Communication:** No supervisor communication this week. The work was entirely technical and self-directed. The meeting with Peter P.A.L. van Alem carrying the formal written midterm feedback was scheduled for the following week — May 12 — so the experiments were run and results interpreted independently before any external review. This was a deliberate choice: having complete results ready before the May 12 meeting would allow a more substantive discussion of the findings rather than a progress update. The inconclusive outcomes from Experiment 1 were not discussed with either supervisor at this stage. The interpretation — that inconclusive results under a conservative threshold represent genuine statistical indeterminacy rather than model equivalence — was worked out independently through the statistical literature before being written into the thesis.

**Challenges:** All three experiments produced predominantly inconclusive results under the Bonferroni-corrected testing regime. This required careful engagement with the statistical literature to ensure the results were characterised correctly — inconclusive under a conservative threshold is not the same as evidence of equivalence, and that distinction needed to be stated clearly in the thesis. The Ridge degradation under SynthOnly was initially puzzling and required additional analysis to trace to pseudo-label variance compression — the synthetic labels had lower variance than the real targets, which compressed the signal Ridge relies on while leaving tree-based models largely unaffected. Interpreting and writing up these results independently, without a technical supervisor to validate the reasoning, required a higher degree of confidence in the statistical methodology than had been needed at any earlier point in the project.
---

## Week 14 — May 11–17

**Technical work:** Wrote all six thesis chapters covering the full research narrative: introduction establishing context and research question, related work covering biological age literature, synthetic data generation methods, and SHAP in health ML, methodology with full protocol documentation and four stated limitations, results including the reliability curve subsection and GMM fidelity metric, discussion with five discussion points and SHAP feature interpretation, and conclusion with direct sub-question answers and future work items. Also wrote the abstract and ethics chapter. Rebuilt the Streamlit dashboard as a five-page application — Individual Report, Upload New Scan, Population View with age vs. age gap scatter plot, Export PDF, and About — and deployed it to Streamlit Community Cloud. Produced the plan of approach, Gantt chart, and this logbook.

**Decisions made:** Structured the reliability curve analysis to be transparent about inflated per-prediction error statistics relative to fold-level MAE. Reported the GMM fidelity metric as a validation step rather than a headline claim. Chose a cumulative additive structure for Experiment 3's feature group ordering based on data collection complexity, with anthropometric measurements forming the base group. The Streamlit application was not demonstrated to Galchin this week. The decision was to wait until the application had been further refined before presenting it externally, ensuring the first demonstration to the clinic would reflect a validated and polished product.

**Communication:** Bi-weekly meeting with Peter P.A.L. van Alem on May 12 — the session carrying the formal written midterm feedback. The discussion covered his assessment of progress so far and the areas requiring improvement. Two points were emphasised: first, the report needed to be substantially more theoretical and mathematically grounded, reflecting the added value expected from an Applied Mathematics student rather than a general ICT student; second, the interim report at four pages was too brief and the final thesis would need significantly more depth and academic substance. Both points were taken as clear direction for the thesis writing that followed immediately after this meeting. The feedback was constructive and gave a concrete target for the remainder of the internship.

**Challenges:** Writing six thesis chapters in a single week while simultaneously rebuilding and deploying the Streamlit application required careful prioritisation. Maintaining narrative consistency across chapters written in rapid succession required deliberate cross-referencing — claims in the results chapter needed to align precisely with the protocol described in the methodology, and the discussion needed to interpret only what the results actually showed without overstating the significance of inconclusive findings.
---

## Week 15 — May 18–24 

**Technical work:** Continued filling the competency portfolio sections. Reviewed thesis chapters for consistency in terminology and cross-references. Carried out small remaining technical tasks on the Streamlit application.

**Communication:** Meeting with Kostadin Galchin to discuss the final stage of the internship. He confirmed satisfaction with progress and outlined the remaining steps before handover. No meeting with Peter P.A.L. van Alem this week. The main priorities for the remaining weeks are completing the final thesis, competency portfolio, and logbook.

**Reflection:** The project is effectively in its closing phase. The shift from technical development to writing and documentation requires a different kind of attention, and I am treating it with the same systematic approach used during the experimental work. The Galchin meeting confirmed that the product is in a state he is satisfied with, which removes the main source of uncertainty about the practical deliverable.

---

## Week 16 — May 25–31 

**Technical work:** Continued competency portfolio drafting. Worked on the professionalisation competency sections: self-direction in a non-technical company environment, decision-making under uncertainty, and the project restructuring that followed midterm feedback.

**Communication:** Update provided to Galchin on the current state of the thesis and portfolio. Final supervision meeting with Peter P.A.L. van Alem for this internship period. He reviewed current progress and directed me to prioritise delivering first drafts of both the final thesis and the competency portfolio so he can provide feedback before the final submission deadline.

**Reflection:** The direction from Peter is clear: the remaining time is for writing and consolidation, not further technical development. Having a concrete external deadline for first drafts adds useful pressure. The main risk at this stage is over-refining sections in isolation rather than completing a full draft that Peter can actually review end to end.

---

## Week 17 — June 1–7 

**Technical work:** Completed a full UI overhaul of the Streamlit application: expanded SHAP feature label mapping from 18 to 54 entries with human-readable names, implemented colour-coded metric cards across all pages (green for negative age gap, amber for positive), restructured the About page with styled info and warning boxes, and fixed the truncated client name display in Population View. All changes deployed to Streamlit Community Cloud.

**Communication:** Received detailed written feedback from Peter P.A.L. van Alem on both the thesis and competency portfolio. Feedback covered missing mathematical depth, undefined terminology, statistical justification gaps, a missing AI usage declaration, and several structural additions. Submitted revised versions of both documents (thesis v2, 52 pages) addressing all comments, including: mathematical model formulas for all five algorithms, Shapiro-Wilk normality evidence, two TikZ diagrams, Streamlit screenshots in Section 3.2, AI usage appendix, and ethical considerations moved to the competency portfolio.

**Reflection:** This week made the gap between a working project and a defensible research report concrete. The feedback from Peter was precise and extensive — not surface-level corrections but substantive methodological challenges around statistical assumptions, mathematical depth, and traceability of concepts. Working through each point systematically rather than defensively was the right approach. The thesis is now significantly stronger than the version Peter first read.

## Week 18 — June 8–14 

**Technical work:** Completed final editing pass on the graduation report: resolved all remaining inconsistencies, verified table and figure numbering, and confirmed cross-references across chapters. Thesis compiled cleanly at 52 pages. Competency portfolio finalised at 21 pages with ethical considerations appendix added. Both documents pushed to GitHub and sent to Peter P.A.L. van Alem for final review.

**Communication:** Submitted thesis v2 and competency portfolio to Peter alongside a request for an official defense confirmation letter for employer documentation. Awaiting feedback. Closing meeting with Galchin to be scheduled before June 22 to finalise the three provisional sections in the competency portfolio (Reflection Report 3, end-of-internship stakeholder moment, and end-of-internship scale reading).

**Reflection:** The internship is effectively in its closing phase. The main body of technical and written work is complete; what remains is the Galchin meeting, the final portfolio update, and preparation for the July defense. Looking back across the eighteen weeks, the most significant development was not technical but methodological: learning to treat expert feedback as a diagnostic signal rather than a criticism to manage, and building the habit of documenting decisions at the time they are made rather than reconstructing them after the fact.

## Week 19 — June 15–21 *(Actual)*

**Technical work:** Incorporated all feedback from Peter P.A.L. van Alem on the thesis v2: mathematical model formulas for all five algorithms, Shapiro-Wilk normality evidence, two TikZ diagrams, Streamlit screenshots in Section 3.2, AI usage appendix, and ethical considerations moved to the competency portfolio. Thesis compiled cleanly at 52 pages. Conducted full audit of all supporting documents (plan of approach, logbook, competency portfolio) for consistency errors — corrected defence dates, removed duplicate closing paragraph in PoA, fixed week count in portfolio, confirmed all supervisor name and location fixes throughout. Began preparation for July 3 product presentation and July 7 academic defence.

**Communication:** Closing handover with Kostadin Galchin completed via message exchange. Galchin confirmed the tool is useful in practice and expressed interest in further development after graduation. His feedback was used to update the three provisional sections in the competency portfolio. Submitted revised thesis v2 and finalised competency portfolio to Peter P.A.L. van Alem for final review ahead of the June 22 deadline.
**Reflection:** The project is now fully in its closing phase. All experimental work, writing, and document revisions are complete. The Galchin handover confirmed that the communication objective for the internship was met — a non-technical stakeholder found the tool genuinely useful without requiring a technical explanation. The remaining focus is defence preparation: ensuring every methodological decision made over eighteen weeks can be explained clearly and defended under questioning.

---
*Oral defence: July 3, 2026 (product presentation with educational and company supervisor) and July 7, 2026 (academic defence with assessor).*
