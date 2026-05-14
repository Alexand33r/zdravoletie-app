# Competency Portfolio

**Student:** Alexander Tanev
**Student number:** [ALEXANDER TO FILL]
**Programme:** BSc Applied Mathematics, Data Science major
**Institution:** Fontys University of Applied Sciences
**Company:** Zdravoletie Health and Rehabilitation Centre, Varna, Bulgaria
**Company supervisor:** Kostadin Galchin
**Educational supervisor:** Peter Alem
**Project period:** February 9 – June 27, 2026
**Oral defence:** July 4–5, 2026

---

## Part 1 — Professionalisation Competency

### 1.1 Learning Strategy and Approach

The context of this internship made professional self-direction unavoidable rather than merely desirable. Zdravoletie is a health and rehabilitation clinic; its staff are trained physiotherapists, fitness professionals, and wellness advisors, not data scientists. The company supervisor, Kostadin Galchin, could speak authoritatively to the clinical purpose of the Anovator bodyAge score and to how practitioners use it in advising clients, but the entire technical direction of the project — the framing of the research question, the design of the experimental protocol, the selection of algorithms and evaluation criteria — was necessarily self-determined. There was no in-house technical mentor, no data science team to consult, and no established analytical framework to inherit. Working within this environment required treating professional autonomy not as a privilege to enjoy but as a methodological responsibility: every design choice made without peer review had to be documented carefully and defensible on its own terms.

The strategy adopted in response was to use documentation as a substitute for the external scrutiny that a technical team would ordinarily provide. Every significant decision — the choice of the age gap as the prediction target, the GroupShuffleSplit grouping strategy, the selection of GMM synthesis over generative adversarial alternatives, the application of Bonferroni rather than less conservative multiple comparison corrections — was recorded in the weekly logbook with the reasoning behind it at the time it was made. This record served two functions: it created an audit trail that Peter Alem could review during supervision, and it forced each decision to be articulated explicitly rather than left as an implicit assumption embedded in code.

Communication with Galchin required a consistent translation effort. Progress updates were provided in Bulgarian to eliminate the language barrier, and the framing was shifted from technical findings to practical implications: not which algorithm achieved the lowest mean absolute error, but what the surrogate model could tell a practitioner about which biometric measurements most strongly predict a client's bodyAge deviation. The Streamlit dashboard was designed with Galchin's perspective as the primary constraint — every visualisation and label is oriented toward clinical interpretation rather than statistical detail. Adapting communication in this way was itself a learning process. Early updates over-indexed on methodological detail; by mid-project, the updates had been restructured to lead with clinical implications and relegate technical qualifications to a separate section for those who wanted them.

---

### 1.2 Flexibility in Stakeholder Interactions — Three Moments

**Beginning of the internship:**

[ALEXANDER TO FILL — Describe the initial meeting with Kostadin Galchin where the research direction was discussed and you converged on the age gap approach. The paragraph should cover: what the situation was at the start of the project (did Galchin have a specific request or was the direction open?), how you communicated the distinction between predicting the raw bodyAge score and predicting the age gap, what Galchin's response was to this framing, and what the outcome was in terms of the agreed research direction and working relationship. Approximately 200 words.]

**Middle of the internship — midterm review with Peter Alem:**

The midterm review, delivered in the first week of April, was the most professionally demanding interaction of the project. At that point the project was structured around a biological age prediction framing and reporting an R² of 0.98 as its headline result — both of which Peter Alem identified as serious problems. The biological age framing was factually incorrect: the study had access to no clinical ground truth of the kind that biological age research requires, and presenting the Anovator bodyAge score as equivalent to a clinically validated biological age measure would expose any performance claim to immediate methodological challenge. The R² of 0.98 was implausible given the dataset size and the known noise in the target variable, and indicated a methodological error rather than a strong result. Receiving this feedback required a specific kind of flexibility: the inclination to defend work already completed had to be set aside quickly in favour of a diagnostic response. The immediate decision was to halt new development and trace the source of the artefact before doing anything else. That investigation identified circular benchmarking — a structural design error in which synthetic records pseudo-labelled by a model trained on all real data were then used to evaluate that same model — as the source of the inflated R². The framing correction and the full eleven-bug audit that followed were direct products of treating the midterm feedback as a methodological signal rather than a criticism to be managed.

**End of the internship:**

[ALEXANDER TO FILL — To be written in June 2026. Describe a third significant interaction, either with Peter Alem following submission of chapters for review, or with Kostadin Galchin following the demonstration of the Streamlit dashboard, or another stakeholder moment that reflects professional flexibility. The paragraph should follow the same structure: situation, flexible response, outcome. Approximately 200 words.]

---

### 1.3 Communication Forms Used

Five distinct communication forms were used across the project. Each was chosen to match the audience, the purpose, and the constraints of the professional relationship it served.

**Bulgarian-language progress documents (audience: Kostadin Galchin).** Written updates in Bulgarian were provided to Galchin at regular intervals throughout the project. The choice of Bulgarian was deliberate and practical: Galchin is a fluent Bulgarian speaker, and conducting all communication in English would have introduced an unnecessary barrier to clear understanding of the project's clinical relevance. These documents were structured around practical implications rather than methodological detail — each update described what the current analysis could say about which biometric measurements drive the bodyAge score and what that might mean for advising practice. Technical qualifications and statistical caveats were present but subordinate to the clinical framing. The form was appropriate because Galchin needed to stay informed of progress and validate that the project remained practically relevant to the clinic's needs, not to evaluate the statistical choices.

**Interim report in English (audience: Peter Alem).** The interim report, submitted at the end of Week 8, was the primary communication with the educational supervisor before the midterm. It was written in English in academic register and structured to demonstrate methodological rigour: it covered the research question, the data collection procedure, the feature engineering rationale, and the preliminary results. This form was required by the Fontys assessment structure and appropriate for an academic audience that needed to evaluate the soundness of the research design. The report was the instrument through which Peter Alem identified the framing and methodology issues that were subsequently corrected.

**Midterm oral presentation (audience: Peter Alem).** The midterm presentation was delivered in person to Peter Alem in the first week of April. The oral form was appropriate because it enabled a live exchange: the presentation of findings could be immediately followed by structured feedback, and the dialogue allowed the framing and R² concerns to be communicated directly rather than through written comments on a document. The interactive format made it possible to clarify the source of the concerns in real time and agree on the direction for the corrective work.

**Streamlit dashboard (audience: Zdravoletie practitioners; secondary audience: academic assessors).** The Streamlit application is a communication artefact as much as a technical one. It translates the analytical outputs of the research — surrogate model predictions, SHAP feature importance, population comparison statistics — into a form accessible to a clinical audience with no data science background. The form was chosen because Galchin needed a working tool, not a report, and because a deployed application demonstrating practical usability was a more convincing deliverable than a static visualisation document. The About page, written in plain language and addressed directly to a health professional audience, reinforces the communication function of the tool. The application is also publicly accessible, which allowed it to serve as evidence of product delivery in discussions with both supervisors.

**Written thesis (audience: academic examining committee).** The graduation report is the primary formal communication of the project's scientific contribution. It is written in English in full academic prose, structured according to the conventions of applied machine learning research: introduction establishing the research question and framing, related work situating the study in the literature, methodology documenting the experimental design and protocol, results reporting all findings with confidence intervals and significance test outcomes, discussion interpreting the findings and their limitations, and conclusion summarising the answers to the sub-questions and identifying future work. The form was appropriate because the audience — Peter Alem and the examining committee at Fontys — required a complete and verifiable account of the research, not a summary or a practical tool.

---

### 1.4 Growth Through Reflection — Three Reflection Reports

**Reflection Report 1 — February 2026 (beginning of internship):**

[ALEXANDER TO FILL — Write approximately 200 words describing your state at the start of the internship. Consider: your initial confidence level about the technical work, any anxiety or uncertainty about working in an unstructured company environment without a technical supervisor, whether you had a clear idea of what the research question should be, and what your initial assumptions were about the difficulty of the project. Be honest about both confidence and doubt. The reflection should be written in first person and describe your mental state and approach at that time, not an idealised version of it.]

**Reflection Report 2 — April 2026 (after midterm feedback):**

The midterm feedback confronted me with a gap between the confidence I had developed in the preceding weeks and the actual rigour of the work I had produced. I had become increasingly convinced that the R²=0.98 result was a genuine finding and had begun to think of the project as technically strong. Peter Alem's feedback at the midterm was precise and uncomfortable: the framing was wrong, the result was an artefact, and the two problems were connected. My immediate reaction was to want to contextualise and qualify rather than to fully accept the critique — I recall thinking that the result was perhaps inflated but not entirely without signal, and that the framing issue was more a matter of presentation than substance. Both of those instincts were wrong, and working through the audit over the following two weeks confirmed that they were wrong. The R² was entirely artefactual. The framing correction was not cosmetic; it changed what claims the thesis was permitted to make. What I learned from this process was less about the specific bugs than about the cost of self-serving interpretation of early results. I had read the 0.98 figure as confirmation rather than as a prompt for scrutiny. Going forward I changed how I read my own results: the first question on encountering a surprising finding became "what could be wrong here" rather than "how strong is this." That shift is visible in how the discussion chapter treats all three experiments — every result, including the statistically significant ones, is examined for alternative explanations before an interpretation is advanced.

**Reflection Report 3 — June 2026 (end of internship):**

[ALEXANDER TO FILL — To be written in June 2026 after the final submission. Write approximately 200 words reflecting on your development across the full project period. Consider: how your professional self-direction improved from February to June, whether your communication with Galchin became more effective over time, how you now feel about the quality of the thesis and dashboard relative to your initial expectations, and what you would do differently. Include an honest assessment of what still feels unfinished or uncertain. Write in first person.]

---

### 1.5 Sources for Professionalisation Competency

[TWO SOURCES NEEDED — The following are suggested starting points. Search and verify before adding:

1. For science communication to non-technical audiences: consider Nisbet, M.C., & Scheufele, D.A. (2009), "What's next for science communication? Promising directions and lingering distractions," *American Journal of Botany*, 96(10), 1767–1778; or Featherstone, H., & Hendry, J. (2012), *Science Communication in Practice*; or a chapter on stakeholder communication from a professional engineering ethics or practice text.

2. For reflective practice and professional development: consider Schon, D.A. (1983), *The Reflective Practitioner: How Professionals Think in Action*; or Moon, J.A. (2004), *A Handbook of Reflective and Experiential Learning: Theory and Practice*; or Kolb, D.A. (1984), *Experiential Learning: Experience as the Source of Learning and Development*.

Replace these suggestions with the actual sources you choose to use, formatted in APA 7 citation style.]

---

## Part 2 — Learning Objective

### 2.1 The Learning Objective

[ALEXANDER TO FILL — Copy here the exact text of your learning objective as written and submitted to Fontys. Do not paraphrase or rewrite it. If the objective was written in Dutch, reproduce it in Dutch here and provide an English translation directly below it.]

---

### 2.2 Reason for This Learning Objective

The learning objective was chosen in recognition of a professional gap that this particular project was well positioned to expose. Technical analytical work — designing experiments, running models, interpreting statistical outputs — takes place in a constrained and legible environment where quality criteria are relatively clear: results are reproducible or they are not, methods are appropriate to the data or they are not, claims are supported by evidence or they are not. Communicating that work to stakeholders who do not share the same technical vocabulary is a different kind of challenge, and one that a data scientist working in a professional advisory context cannot avoid.

The specific structure of this internship made this gap especially salient. Kostadin Galchin, the company supervisor, is a health and fitness professional who uses the Anovator system daily and has direct opinions about what the bodyAge score means to clients and practitioners. He does not, however, have a background in statistical modelling, and conveying to him what it means for a Wilcoxon test comparison to be inconclusive, or why a mean absolute error of 2.43 years is simultaneously the best available result and an honest acknowledgement of the limits of what 53 individuals can establish, required a translation effort that is easy to underestimate. The same challenge applied to the Streamlit dashboard: every design decision about what to show, how to label it, and what to leave out was a communication decision as much as a technical one. The learning objective was chosen because this internship presented a concentrated version of the challenge that defines professional data science work at the boundary between analysis and decision-making: being useful to people who need your results but cannot evaluate your methods.

---

### 2.3 How the Learning Objective Was Worked On

Progress toward the learning objective was made through a set of concrete actions that spanned the full project period. The earliest and most sustained action was the practice of writing regular progress updates in Bulgarian for Galchin. Each update required explicitly asking: what does this finding mean for a practitioner advising clients on diet and exercise, and how can I explain it without requiring the reader to have any statistical background? This question did not have an obvious answer at the start of the project, and the process of trying to answer it repeatedly — and watching Galchin's responses indicate whether the explanation landed — was the main vehicle for improvement.

The midterm presentation was a second, more concentrated opportunity. Preparing a twenty-minute oral account of the project for Peter Alem forced a decision about which elements were essential and which were internal scaffolding that the audience did not need. The feedback that the biological age framing was wrong was, in retrospect, partly a communication failure: the framing had been adopted without sufficiently interrogating whether it was defensible to a careful academic listener, not just familiar within the project.

Building the Streamlit dashboard shifted the communication work into a design register. The constraints were tighter there — every label, tooltip, and page title either communicated something useful to a health professional or it did not, and there was no prose available to compensate for a poorly chosen visualisation. Writing the About page required a plain-language account of the tool's limitations that could be understood by someone who had never heard of mean absolute error. Completing that page was one of the clearest tests of whether the learning objective had been achieved in practice.

---

### 2.4 Scale Question — Three Measurements

The scale question measures the degree to which the student can effectively communicate technical analytical findings to non-technical stakeholders, on a scale of 1 (unable to adapt communication to audience) to 10 (consistently communicates complex findings clearly and accessibly across all audience types).

**Start of internship — February 2026:**

[ALEXANDER TO FILL — Provide your honest self-rating on the 1–10 scale as of February 2026, and write approximately 100 words explaining your reasoning. Consider: what communication experience you had before this internship, how confident you felt about the specific challenge of a non-technical supervisor, and what your honest assessment was of your ability to make complex statistical findings accessible. Be specific rather than vague.]

**Middle of internship — April 2026:**

5/10. The midterm review with Peter Alem provided direct evidence of progress and its limits simultaneously. On the progress side, the project's practical framing — working in Bulgarian with a non-technical supervisor and structuring updates around clinical implications — had required consistent communication adaptation throughout the preceding weeks, and that practice had produced measurable improvement in how clearly progress could be explained to Galchin. The feedback from Peter Alem indicated, however, that the same improvement had not yet carried into the academic communication register. The midterm presentation and the interim report both over-indexed on technical detail and under-indexed on the implications of the findings: what do these results mean for a practitioner, why does the framing matter for how conclusions are drawn, and what can and cannot be claimed from the evidence available. The 5/10 rating reflects genuine progress in one direction — non-technical stakeholder communication — against persistent limitation in a second: disciplined, implication-focused academic communication to a sophisticated technical audience.

**End of internship — June 2026:**

[ALEXANDER TO FILL — Provide your honest self-rating on the 1–10 scale as of June 2026 and write approximately 100 words explaining your reasoning. Reflect on whether the writing of the thesis chapters, the deployment of the dashboard, and the preparation for the oral defence changed your assessment of where you stand. If your self-rating has increased, be specific about what changed. If it has not changed much, be honest about what remains difficult.]

---

### 2.5 Feedback and Feedforward from Three People

**Peter Alem** is the educational supervisor assigned to this project by Fontys University of Applied Sciences. He has an academic background and is responsible for assessing the scientific rigour and professional quality of the graduation work.

[FEEDBACK TO BE INSERTED — Ask Peter Alem to provide written feedback and feedforward on your learning objective after the thesis is submitted. His feedback should address: whether your academic communication improved over the course of the project, how clearly the thesis conveys findings to an informed reader, and what you should continue to develop. Insert verbatim or paraphrased with attribution once received.]

**Kostadin Galchin** is the company supervisor at Zdravoletie Health and Rehabilitation Centre in Varna. He is a health and fitness professional with daily operational experience using the Anovator system and has no background in statistical modelling or machine learning.

[FEEDBACK TO BE INSERTED — Ask Kostadin Galchin to provide feedback on how well the project's outputs — particularly the Bulgarian-language updates and the Streamlit dashboard — communicated the analytical findings in a form he could understand and act on. His feedback should address: whether the progress updates were clear, whether the dashboard is usable in a clinical setting, and what would have made the communication more effective. Insert verbatim or paraphrased with attribution once received.]

**[ALEXANDER TO FILL — Identify Dani/Bobi: describe their relationship to you (fellow student, peer reviewer, classmate, etc.) and their relevant background. Then insert the feedback and feedforward they provided once received.]**

[FEEDBACK TO BE INSERTED — Ask Dani/Bobi to provide peer feedback on your learning objective. Their feedback should address how effectively you communicated your project and its results in a non-specialist context — for example, if they are a fellow student from a different programme, whether your explanations of the statistical methods and findings were understandable and well-motivated. Insert verbatim or paraphrased with attribution once received.]

---

### 2.6 Sources for Learning Objective

[TWO SOURCES NEEDED — The following are suggested starting points. Search and verify before adding:

1. For data visualisation and communication of quantitative results: consider Cairo, A. (2016), *The Truthful Art: Data, Charts, and Maps for Communication*; or Tufte, E.R. (2001), *The Visual Display of Quantitative Information*; or a peer-reviewed paper on communicating uncertainty in health data to lay audiences, such as Spiegelhalter, D., Pearson, M., & Short, I. (2011), "Visualizing uncertainty about the future," *Science*, 333(6048), 1393–1400.

2. For professional advisory communication in technical fields: consider Kahneman, D. (2011), *Thinking, Fast and Slow* (chapters on expert communication); or Huff, D. (1954), *How to Lie with Statistics* (as a counter-example text); or a practitioner-facing source such as Peng, R.D., & Matsui, E. (2015), *The Art of Data Science*.

Replace these suggestions with the actual sources you choose to use, formatted in APA 7 citation style.]

---

## Part 3 — Overall Reflection

### 3.1 Approach and Decision-Making

Four decisions shaped the character of this project, and reflecting on each reveals something about how analytical choices interact with professional integrity in research practice.

The first was choosing the age gap — bodyAge minus chronological age — as the prediction target rather than the raw bodyAge score. The reasoning was direct: chronological age is trivially predictable, and including it as a component of the target variable would inflate performance metrics without illuminating the question of interest, which is what the Anovator formula does with the physiological deviation from expected age. This decision was made at the start of Week 1 and logged in the logbook. Alternatives considered were predicting bodyAge directly and predicting a binary indicator of elevated bodyAge. Both were rejected: the first for the reason stated above, the second because it discards continuous variation that the regression framework can exploit. The decision was straightforward technically but important to document — a reader who did not understand it might misinterpret the model's mean absolute error of 2.43 years as a direct error on bodyAge itself.

The second was choosing GMM synthesis over CTGAN, TVAE, or copula alternatives. The reasoning was data-scale: 158 records falls below the regime in which GAN architectures train reliably, and the instability of GAN training at small data scales would make results from such a comparison unreliable and hard to interpret. The GMM was not the most powerful generative approach available; it was the most appropriate one given the constraint. What this decision taught me is that in applied research, the right method is not the most sophisticated method but the most honest method for the available data. Choosing a simpler approach because it is defensible is preferable to choosing a complex approach because it looks more advanced.

The third was applying Bonferroni correction rather than a less conservative multiple comparisons procedure. The Benjamini-Hochberg procedure, for example, would have produced more significant results across all three experiments. The decision to apply Bonferroni reflected a prior about the primary risk in this context: a false positive claim that one algorithm or training regime significantly outperforms another, when the data cannot actually certify that, would misrepresent the project's contribution. The consequence was that the majority of comparisons were reported as inconclusive, which was harder to present but more honest.

The fourth decision — reframing the project after the midterm — was the most difficult and ultimately the most formative. The original biological age framing was not merely a presentation choice; it was a substantive claim that the Anovator score constituted clinical ground truth of the kind studied in the biological age literature. Abandoning it required accepting that weeks of work had been built on an incorrect premise. The lesson was about the distinction between investing effort in an approach and being correct about that approach — and about the importance of treating expert feedback as evidence rather than as an obstacle.

---

### 3.2 Collaboration and Communication

This project was largely self-directed, and it is important to be precise about what that meant in practice, because the advantages and disadvantages of that condition were both real. The advantage was full ownership of every analytical decision: no technical manager to negotiate with, no conflicting priorities to balance, no institutional inertia to overcome. Every choice about experimental design, evaluation protocol, and statistical framing was made by one person, based on explicit reasoning logged at the time. That ownership produced a kind of analytical coherence that is harder to achieve when a research direction is negotiated across a team.

The disadvantage was the absence of peer review for those same decisions. In a team environment, a proposed evaluation protocol would be read and questioned by a colleague before the first line of code was written. The circular benchmarking error that produced the R²=0.98 artefact — the most significant methodological mistake in the project — persisted for several weeks precisely because no one else read the data flow across the notebooks and asked why the evaluation set overlapped with the pseudo-label source. Peter Alem's midterm question, which surfaced the problem, was the external review that should have happened earlier. That experience is the clearest evidence of what peer review actually provides that solo work cannot replicate through documentation alone.

Communication with Galchin improved significantly over the project period. The initial updates were too dense and the clinical implications too buried. By mid-project, the structure had been inverted: implications first, methods as supporting context. The dashboard is the fullest realisation of that approach — it shows the SHAP chart and the risk/protective factor labels before it mentions the model architecture, and the About page addresses a practitioner rather than a researcher. Whether this translation succeeded is partly a question of evidence that Galchin's feedback will answer.

---

### 3.3 Evidence of Development

[ALEXANDER TO FILL — This section should list the concrete artefacts that demonstrate your development across the competency and the learning objective. Link to or name the specific files where possible. Suggested evidence to include:

- The Bulgarian-language progress update documents sent to Galchin (provide filenames or dates)
- The interim report (Week 8), as evidence of the state of communication before the midterm
- The midterm feedback form or notes from Peter Alem (if a written record exists)
- The thesis methodology chapter, as evidence of accurate technical communication after the reframing
- The thesis discussion chapter, particularly Section 5.4 (SHAP interpretation), as evidence of translating model outputs into physiological terms accessible to a health professional audience
- The Streamlit About page (pages/0_About.py), as evidence of non-technical communication design
- This logbook (thesis/logbook.md), as evidence of the systematic documentation practice used to compensate for the absence of peer review

Write two or three sentences for each artefact explaining what it demonstrates and how it constitutes evidence of development rather than merely evidence of completion.]

---

### 3.4 Areas for Further Development

Three areas of professional capability were exposed as underdeveloped by the experience of this project and are identified here without qualification as directions for continued work.

The first is the communication of statistical uncertainty to non-statisticians. Reporting a mean absolute error of 2.43 years with a 95% confidence interval of [2.09, 2.76] is precise and defensible in academic context. Explaining to a practitioner what it means that the prediction could be off by more than two years on a given client — and what that implies for the weight they should give the score in an advising conversation — is a different and harder task. The Streamlit dashboard addresses this imperfectly, and the limitation section of the About page is necessarily compressed. A more complete treatment would require fluency in communicating uncertainty in health contexts specifically, a field with its own literature and practice standards that this project touched but did not engage with systematically.

The second is working within structured organisational environments. Zdravoletie provided minimal procedural structure, and the flexibility that resulted was both an advantage and a gap in professional experience. The ability to work within a structured organisation — where analytical decisions must be approved, where communication has defined channels, and where timelines are constrained by organisational processes rather than personal planning — is a capability that this internship did not exercise.

The third is domain knowledge in health and physiology. The project required biological interpretation of SHAP feature importance outputs — explaining, for example, why trunk fat distribution and bioimpedance phase angle appeared among the top predictors in physiological terms — without a biology or physiology background. The interpretations offered in the thesis are grounded in the research literature but would benefit substantially from direct collaboration with a clinician.
