# Competency Portfolio

**Student:** Alexander Tanev
**Student number:** 4878248
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

The context of this internship made professional self-direction unavoidable rather than merely desirable. Zdravoletie is a health and rehabilitation clinic; its staff are trained physiotherapists, fitness professionals, and wellness advisors, not data scientists. The company supervisor, Kostadin Galchin, could speak authoritatively to the clinical purpose of the Anovator bodyAge score and to how practitioners use it in advising clients, but the entire technical direction of the project, including the framing of the research question, the design of the experimental protocol, and the selection of algorithms and evaluation criteria, was necessarily self-determined. There was no in-house technical mentor, no data science team to consult, and no established analytical framework to inherit. Working within this environment required treating professional autonomy not as a privilege to enjoy but as a methodological responsibility: every design choice made without peer review had to be documented carefully and defensible on its own terms.

The strategy adopted in response was to use documentation as a substitute for the external scrutiny that a technical team would ordinarily provide. Every significant decision was recorded in the weekly logbook with the reasoning behind it at the time it was made: the choice of the age gap as the prediction target, the GroupShuffleSplit grouping strategy, the selection of GMM synthesis over generative adversarial alternatives, and the application of Bonferroni rather than less conservative multiple comparison corrections. The record served two functions: it created an audit trail that Peter Alem could review during supervision, and it forced each decision to be articulated explicitly rather than left as an implicit assumption embedded in code.

Communication with Galchin required a consistent translation effort. Progress updates were provided in Bulgarian to eliminate the language barrier, and the framing was shifted from technical findings to practical implications: not which algorithm achieved the lowest mean absolute error, but what the surrogate model could tell a practitioner about which biometric measurements most strongly predict a client's bodyAge deviation. The Streamlit dashboard was designed with Galchin's perspective as the primary constraint; every visualisation and label is oriented toward clinical interpretation rather than statistical detail. Adapting communication in this way was itself a learning process. Early updates over-indexed on methodological detail; by mid-project, the updates had been restructured to lead with clinical implications and relegate technical qualifications to a separate section for those who wanted them.

---

### 1.2 Flexibility in Stakeholder Interactions — Three Moments

**Beginning of the internship:**

The internship began through a mutual connection who identified an alignment between my background in data analysis and Zdravoletie's need for independent research on their Anovator biometric data. The initial meeting with Kostadin Galchin was exploratory rather than directive; he had no specific technical request, only a broader goal: to use the data he had collected to give clients better, evidence-based advice on longevity and health risk. Early discussions ranged widely, including the possibility of incorporating publicly available Bulgarian national health data, but we converged on a more focused scope appropriate to the graduation internship constraints. The first significant decision I proposed was to shift the modelling target away from the Anovator hardware Score, which initial analysis showed to be effectively constant across 85% of clients, toward the age gap (the difference between bodyAge and chronological age). I explained this to Galchin not in statistical terms but in practical ones: the Score told consultants almost nothing useful, while the age gap offered a continuous, sensitive measure that could actually differentiate between clients and track progress over time. Galchin accepted this framing and from that point confirmed full autonomy on the technical direction, with his role being to validate that the research stayed aligned with what would genuinely benefit the business. That working pattern defined the rest of the internship: independent analytical decision-making on my side, accessible communication and directional confirmation on his.

**Middle of the internship — midterm review with Peter Alem:**

The midterm review, delivered in the first week of April, was the most professionally demanding interaction of the project. At that point the project was structured around a biological age prediction framing and reporting an R² of 0.98 as its headline result, both of which Peter Alem identified as serious problems. The biological age framing was factually incorrect: the study had access to no clinical ground truth of the kind that biological age research requires, and presenting the Anovator bodyAge score as equivalent to a clinically validated biological age measure would expose any performance claim to immediate methodological challenge. The R² of 0.98 was implausible given the dataset size and the known noise in the target variable, and indicated a methodological error rather than a strong result. Receiving this feedback required a specific kind of flexibility: the inclination to defend work already completed had to be set aside quickly in favour of a diagnostic response. The immediate decision was to halt new development and trace the source of the artefact before doing anything else. That investigation identified circular benchmarking as the source of the inflated R², a structural design error in which synthetic records pseudo-labelled by a model trained on all real data were then used to evaluate that same model. The framing correction and the full eleven-bug audit that followed were direct products of treating the midterm feedback as a methodological signal rather than a criticism to be managed.

**End of the internship:**

[ALEXANDER TO FILL — To be written in June 2026. Describe a third significant interaction, either with Peter Alem following submission of chapters for review, or with Kostadin Galchin following the demonstration of the Streamlit dashboard, or another stakeholder moment that reflects professional flexibility. The paragraph should follow the same structure: situation, flexible response, outcome. Approximately 200 words.]

---

### 1.3 Communication Forms Used

Five distinct communication forms were used across the project. Each was chosen to match the audience, the purpose, and the constraints of the professional relationship it served.

**Bulgarian-language progress documents (audience: Kostadin Galchin).** Written updates in Bulgarian were provided to Galchin at regular intervals throughout the project. The choice of Bulgarian was deliberate and practical: Galchin is a fluent Bulgarian speaker, and conducting all communication in English would have introduced an unnecessary barrier to clear understanding of the project's clinical relevance. These documents were structured around practical implications rather than methodological detail; each update described what the current analysis could say about which biometric measurements drive the bodyAge score and what that might mean for advising practice. Technical qualifications and statistical caveats were present but subordinate to the clinical framing. The form was appropriate because Galchin needed to stay informed of progress and validate that the project remained practically relevant to the clinic's needs, not to evaluate the statistical choices.

**Interim report in English (audience: Peter Alem).** The interim report, submitted at the end of Week 8, was the primary communication with the educational supervisor before the midterm. It was written in English in academic register and structured to demonstrate methodological rigour: it covered the research question, the data collection procedure, the feature engineering rationale, and the preliminary results. The form was required by the Fontys assessment structure and appropriate for an academic audience that needed to evaluate the soundness of the research design. The report was the instrument through which Peter Alem identified the framing and methodology issues that were subsequently corrected.

**Midterm oral presentation (audience: Peter Alem).** The midterm presentation was delivered in person to Peter Alem in the first week of April. The oral form was appropriate because it enabled a live exchange: the presentation of findings could be immediately followed by structured feedback, and the dialogue allowed the framing and R² concerns to be communicated directly rather than through written comments on a document. The interactive format made it possible to clarify the source of the concerns in real time and agree on the direction for the corrective work.

**Streamlit dashboard (audience: Zdravoletie practitioners; secondary audience: academic assessors).** The Streamlit application is a communication artefact as much as a technical one. It translates the analytical outputs of the research, including surrogate model predictions, SHAP feature importance, and population comparison statistics, into a form accessible to a clinical audience with no data science background. The form was chosen because Galchin needed a working tool, not a report, and because a deployed application demonstrating practical usability was a more convincing deliverable than a static visualisation document. The About page, written in plain language and addressed directly to a health professional audience, reinforces the communication function of the tool. The application is also publicly accessible, which allowed it to serve as evidence of product delivery in discussions with both supervisors.

**Written thesis (audience: academic examining committee).** The graduation report is the primary formal communication of the project's scientific contribution. It is written in English in full academic prose, structured according to the conventions of applied machine learning research: introduction establishing the research question and framing, related work situating the study in the literature, methodology documenting the experimental design and protocol, results reporting all findings with confidence intervals and significance test outcomes, discussion interpreting the findings and their limitations, and conclusion summarising the answers to the sub-questions and identifying future work. The form was appropriate because the audience, Peter Alem and the examining committee at Fontys, required a complete and verifiable account of the research, not a summary or a practical tool.

---

### 1.4 Growth Through Reflection — Three Reflection Reports

**Reflection Report 1 — February 2026 (beginning of internship):**

At the start of the internship I was confident in my technical, analytical, and mathematical abilities. The modelling work itself did not feel intimidating; I had a solid foundation in machine learning and statistics and trusted my ability to work through technical problems independently. The uncertainty lay elsewhere.
Professionally, I was aware of gaps I had not yet fully addressed. Communication had never been a natural strength; I tended to present technical work in technical terms without translating it into what it meant for the person I was talking to. Reliability and consistency in a professional context, rather than an academic one, were also areas I knew needed development. The prospect of working without a technical supervisor felt like both a relief and a risk at the same time. On one side, there would be no pressure to present, explain, and justify every decision constantly. On the other, those pressures are exactly what develop professional skills, and avoiding them meant I would have to create that pressure for myself.
I did not have a clear research question going in. Peter Alem had advised that this was normal; research directions shift once you engage with the real data and the real constraints. I accepted that, though I had some quiet concern about whether the project scope would be substantial enough for a graduation thesis. I committed to staying consistent and letting the work develop, while acknowledging that the professional side of the internship would require as much effort as the technical side. 

**Reflection Report 2 — April 2026 (after midterm feedback):**

The midterm feedback confronted me with a gap between the confidence I had developed in the preceding weeks and the actual rigour of the work I had produced. I had become increasingly convinced that the R²=0.98 result was a genuine finding and had begun to think of the project as technically strong. Peter Alem's feedback at the midterm was precise and uncomfortable: the framing was wrong, the result was an artefact, and the two problems were connected. My immediate reaction was to want to contextualise and qualify rather than to fully accept the critique; I recall thinking that the result was perhaps inflated but not entirely without signal, and that the framing issue was more a matter of presentation than substance. Both of those instincts were wrong, and working through the audit over the following two weeks confirmed that they were wrong. The R² was entirely artefactual. The framing correction was not cosmetic; it changed what claims the thesis was permitted to make. What I learned from this process was less about the specific bugs than about the cost of self-serving interpretation of early results. I had read the 0.98 figure as confirmation rather than as a prompt for scrutiny. Going forward I changed how I read my own results: the first question on encountering a surprising finding became "what could be wrong here" rather than "how strong is this." That shift is visible in how the discussion chapter treats all three experiments; every result, including the statistically significant ones, is examined for alternative explanations before an interpretation is advanced.

**Reflection Report 3 — June 2026 (end of internship):**

[ALEXANDER TO FILL — To be written in June 2026 after the final submission. Write approximately 200 words reflecting on your development across the full project period. Consider: how your professional self-direction improved from February to June, whether your communication with Galchin became more effective over time, how you now feel about the quality of the thesis and dashboard relative to your initial expectations, and what you would do differently. Include an honest assessment of what still feels unfinished or uncertain. Write in first person.]

---

### 1.5 Sources for Professionalisation Competency

Schön, D. A. (1983). *The Reflective Practitioner: How Professionals Think in Action*. Basic Books.

Schön's foundational account of reflection-in-action and reflection-on-action, meaning the capacity of practitioners to think critically about their own practice while doing it and after the fact, directly informs the three reflection reports in Section 1.4, particularly the midterm reflection on the project reframing: recognising and correcting a flawed framing in response to expert feedback is a textbook instance of the reflective competence Schön describes.

Nisbet, M. C., & Scheufele, D. A. (2009). What's next for science communication? Promising directions and lingering distractions. *American Journal of Botany*, 96(10), 1767–1778. https://doi.org/10.3732/ajb.0900041

This paper analyses the challenge of translating scientific findings for non-specialist audiences and identifies stakeholder-oriented framing as a key strategy, directly applicable to the challenge of communicating a machine learning research project to a clinical company supervisor with no statistical background.

---

## Part 2 — Learning Objective

### 2.1 The Learning Objective

The learning objective for this internship is to strengthen my ability to communicate analytical results clearly and effectively to non-technical stakeholders and to translate data-driven insights into actionable recommendations.

This will be achieved by regularly presenting intermediate results to the company supervisor, discussing assumptions, limitations, and implications of the models, and adapting my communication style based on stakeholder feedback. Active participation in feedback discussions will be used to improve clarity, alignment, and professional interaction.

Progress will be measured by the quality and consistency of stakeholder feedback, the level of alignment between analytical outcomes and stakeholder expectations, and the ability to independently lead result discussions and decision-oriented conversations.

---

### 2.2 Reason for This Learning Objective

The learning objective was chosen in recognition of a professional gap that this particular project was well positioned to expose. Technical analytical work, designing experiments, running models, and interpreting statistical outputs, takes place in a constrained and legible environment where quality criteria are relatively clear: results are reproducible or they are not, methods are appropriate to the data or they are not, claims are supported by evidence or they are not. Communicating that work to stakeholders who do not share the same technical vocabulary is a different kind of challenge, and one that a data scientist working in a professional advisory context cannot avoid.

The specific structure of this internship made this gap especially salient. Kostadin Galchin, the company supervisor, is a health and fitness professional who uses the Anovator system daily and has direct opinions about what the bodyAge score means to clients and practitioners. He does not, however, have a background in statistical modelling. Conveying to him what it means for a Wilcoxon test comparison to be inconclusive, or why a mean absolute error of 2.43 years is simultaneously the best available result and an honest acknowledgement of the limits of what 53 individuals can establish, required a translation effort easy to underestimate. The same challenge applied to the Streamlit dashboard: every design decision about what to show, how to label it, and what to leave out was a communication decision as much as a technical one. The learning objective was chosen because this internship presented a concentrated version of the challenge that defines professional data science work at the boundary between analysis and decision-making: being useful to people who need your results but cannot evaluate your methods.

---

### 2.3 How the Learning Objective Was Worked On

Progress toward the learning objective was made through a set of concrete actions that spanned the full project period. The earliest and most sustained action was the practice of writing regular progress updates in Bulgarian for Galchin. Each update required explicitly asking: what does this finding mean for a practitioner advising clients on diet and exercise, and how can I explain it without requiring the reader to have any statistical background? The question had no obvious answer at the start of the project. Trying to answer it repeatedly, watching whether Galchin's responses indicated it had landed, was the main vehicle for improvement.

The midterm presentation was a second, more concentrated opportunity. Preparing a twenty-minute oral account of the project for Peter Alem forced a decision about which elements were essential and which were internal scaffolding that the audience did not need. The feedback that the biological age framing was wrong was, in retrospect, partly a communication failure: the framing had been adopted without sufficiently interrogating whether it was defensible to a careful academic listener, not just familiar within the project.

Building the Streamlit dashboard shifted the communication work into a design register. The constraints were tighter there; every label, tooltip, and page title either communicated something useful to a health professional or it did not, and there was no prose available to compensate for a poorly chosen visualisation. Writing the About page required a plain-language account of the tool's limitations that could be understood by someone who had never heard of mean absolute error. Completing that page was one of the clearest tests of whether the learning objective had been achieved in practice.

---

### 2.4 Scale Question — Three Measurements

The scale question measures the degree to which the student can effectively communicate technical analytical findings to non-technical stakeholders, on a scale of 1 (unable to adapt communication to audience) to 10 (consistently communicates complex findings clearly and accessibly across all audience types).

**Start of internship — February 2026:**

At the start of the internship I would honestly rate myself a 3 out of 10 on this scale. I had no significant experience presenting analytical findings to non-technical decision-makers, and my previous communication in academic settings had been largely peer-to-peer, with classmates and fellow students where I felt genuinely confident. The specific challenge of communicating upward, to supervisors, managers, or stakeholders, was one I consistently struggled with. In those situations I became overly focused on making a good impression rather than communicating clearly, which had the opposite effect; the anxiety about being judged interfered with the quality of the explanation itself. I was aware of this pattern going into the internship and recognised it as something that needed to change. The Zdravoletie context, a non-technical supervisor who needed accessible, actionable insights rather than statistical detail, was precisely the kind of environment that would force me to address this directly. That awareness was the starting point, but awareness alone does not translate to ability, which is why I rate myself a 3 rather than higher.

**Middle of internship — April 2026:**

5/10. The midterm review with Peter Alem provided direct evidence of progress and its limits simultaneously. On the progress side, the project's practical framing, which involved working in Bulgarian with a non-technical supervisor and structuring updates around clinical implications, had required consistent communication adaptation throughout the preceding weeks, and that practice had produced measurable improvement in how clearly progress could be explained to Galchin. The feedback from Peter Alem indicated, however, that the same improvement had not yet carried into the academic communication register. The midterm presentation and the interim report both over-indexed on technical detail and under-indexed on the implications of the findings: what do these results mean for a practitioner, why does the framing matter for how conclusions are drawn, and what can and cannot be claimed from the evidence available. The 5/10 rating reflects genuine progress in non-technical stakeholder communication but persistent limitation in a second area: disciplined, implication-focused academic communication to a sophisticated technical audience.

**End of internship — June 2026:**

[ALEXANDER TO FILL — Provide your honest self-rating on the 1–10 scale as of June 2026 and write approximately 100 words explaining your reasoning. Reflect on whether the writing of the thesis chapters, the deployment of the dashboard, and the preparation for the oral defence changed your assessment of where you stand. If your self-rating has increased, be specific about what changed. If it has not changed much, be honest about what remains difficult.]

---

### 2.5 Feedback and Feedforward from Three People

**Kostadin Galchin** is the company supervisor at Zdravoletie Health and Rehabilitation Centre in Varna. He is a health and fitness professional with daily operational experience using the Anovator system and has no background in statistical modelling or machine learning.

Feedback: Galchin observed genuine interest and attention to detail in engaging with new subject matter, noting that thorough understanding of the material enabled strong results. He described the working process as smooth and professional, including the communication between them. He noted that the internship demonstrated and developed skills acquired during academic training and expressed that progress was visible and that Alexander is ready for broader and more complex projects. Feedforward: engage with new fields and niches that will be relevant long-term as an investment in the future, broaden general knowledge as a key to progress, and always look for added value in both personal and professional life.

Response: Galchin's feedback affirms what was most valuable about the working structure of this project: being trusted to set the direction and make technical decisions independently created a level of ownership that would not have been possible in a more supervised environment. The self-directed nature of the internship forced me to develop analytical accountability; every design choice was made by one person and had to be defensible on its own terms, without the safety net of a technical peer review process. The feedforward on engaging with new fields resonates directly with what this project demonstrated: the ability to develop functional competence in an unfamiliar domain, such as health informatics and clinical score modelling, is a form of professional capital that compounds over time. I intend to treat breadth of domain knowledge as a deliberate investment rather than an incidental byproduct of whatever project arrives next.

---

**Dani** is a professional colleague from a collaborative project context. He has strong experience in machine learning engineering and software development, and the collaboration involved building a recommendation system.

Feedback: Dani observed strong ML and Python foundations from the start of the collaboration, noting that Alexander applied theoretical and practical knowledge to tackle challenging tasks while building a recommendation system. He highlighted the quality of work and well-documented outcomes as particular strengths. Feedforward: develop the habit of asking for assistance after spending meaningful time on a problem without reaching the desired outcome, and invest in cloud provider knowledge as a long-term career priority.

Response: The feedforward on asking for help after sustained effort resonates as a fair and accurate observation. My default pattern when blocked is to extend the independent effort, running one more experiment, consulting one more paper, or restructuring the problem, before surfacing the difficulty to a colleague, and there were moments in this project where that instinct extended the timeline unnecessarily rather than serving the work. I recognise this as a genuine development priority rather than a minor stylistic preference, and I intend to treat knowing when to escalate as a deliberate skill to practice in collaborative settings going forward. The cloud provider feedforward is one I accept unreservedly: the trajectory of professional data science work in the next several years will be substantially shaped by cloud infrastructure competency, and the gap between what I understand analytically and what I can deploy at scale in a cloud environment is one I plan to close through structured study and practice.

---

**Alexander Tanev - Alexander's father** is an observer from the home and family environment, without professional involvement in the project.

Feedback: "As a father who observes Alexander closely at home, I can say that since the start of his internship I have noticed a visible change in his maturity and sense of responsibility. He approaches his work seriously and I can see how much effort he puts in, often working late into the evening on his project. If I were to give one piece of advice for his development, it would be to act more quickly and decisively when a situation requires it — he sometimes spends a long time thinking before taking action, and building confidence in his own decisions will serve him well going forward." — Alexander's father, May 2026

Response: The observation about decisiveness is accurate, and I recognise it without qualification. The clearest illustration from this project is the three weeks I spent after first obtaining the R²=0.98 result before the midterm: I had a persistent unease about that figure but continued building on it rather than stopping immediately to investigate, extending both the time wasted and the scope of the necessary correction when the problem was eventually identified. A more decisive response to early doubt, halting development and auditing the data flow on the day the suspicion first arose, would have resolved the issue in hours rather than weeks. That pattern of extended deliberation before acting on a clear signal is one I intend to address directly. The practical change I am working on is to set explicit time limits for uncertainty before committing to a diagnostic action, so that reflection serves decision-making rather than postponing it.

---

### 2.6 Sources for Learning Objective

Spiegelhalter, D., Pearson, M., & Short, I. (2011). Visualizing uncertainty about the future. *Science*, 333(6048), 1393–1400. https://doi.org/10.1126/science.1191181

Spiegelhalter and colleagues analyse how uncertainty in quantitative predictions can and should be communicated to non-specialist audiences, presenting evidence-based recommendations for displaying confidence intervals and probability distributions, directly applicable to the challenge of communicating the model's 95% CI results and 2.43-year MAE to Zdravoletie practitioners who need to act on these outputs without a statistical background.

Davenport, T. H., & Patil, D. J. (2012). Data scientist: The sexiest job of the 21st century. *Harvard Business Review*, 90(10), 70–76.

Davenport and Patil describe the data scientist's role as fundamentally advisory, translating analytical findings into organisational decisions by working at the boundary between technical analysis and non-technical stakeholders, and their characterisation of the required communication competencies maps directly onto the learning objective selected for this portfolio: the challenge of making complex model outputs accessible to a non-technical company supervisor and clinical end users.

---

## Part 3 — Overall Reflection

### 3.1 Approach and Decision-Making

Four decisions shaped the character of this project, and reflecting on each reveals something about how analytical choices interact with professional integrity in research practice.

The first was choosing the age gap (bodyAge minus chronological age) as the prediction target rather than the raw bodyAge score. The reasoning was direct: chronological age is trivially predictable, and including it as a component of the target variable would inflate performance metrics without illuminating the question of interest, which is what the Anovator formula does with the physiological deviation from expected age. The decision was made at the start of Week 1 and logged in the logbook. Alternatives considered were predicting bodyAge directly and predicting a binary indicator of elevated bodyAge. Both were rejected: the first for the reason stated above, the second because it discards continuous variation that the regression framework can exploit. The decision was straightforward technically but important to document; a reader who did not understand it might misinterpret the model's mean absolute error of 2.43 years as a direct error on bodyAge itself.

The second was choosing GMM synthesis over CTGAN, TVAE, or copula alternatives. The reasoning was data-scale: 158 records falls below the regime in which GAN architectures train reliably, and the instability of GAN training at small data scales would make results from such a comparison unreliable and hard to interpret. The GMM was not the most powerful generative approach available; it was the most appropriate one given the constraint. What this decision taught me is that in applied research, the right method is not the most sophisticated method but the most honest method for the available data. Choosing a simpler approach because it is defensible is preferable to choosing a complex approach because it looks more advanced.

The third was applying Bonferroni correction rather than a less conservative multiple comparisons procedure. The Benjamini-Hochberg procedure, for example, would have produced more significant results across all three experiments. The decision to apply Bonferroni reflected a prior about the primary risk in this context: a false positive claim that one algorithm or training regime significantly outperforms another, when the data cannot actually certify that, would misrepresent the project's contribution. The consequence was that the majority of comparisons were reported as inconclusive, which was harder to present but more honest.

The fourth decision, reframing the project after the midterm, was the most difficult and ultimately the most formative. The original biological age framing was not merely a presentation choice; it was a substantive claim that the Anovator score constituted clinical ground truth of the kind studied in the biological age literature. Abandoning it required accepting that weeks of work had been built on an incorrect premise. The lesson was about the distinction between investing effort in an approach and being correct about that approach, and about the importance of treating expert feedback as evidence rather than as an obstacle.

---

### 3.2 Collaboration and Communication

This project was largely self-directed, and that condition had real advantages and real disadvantages worth examining. The advantage was full ownership of every analytical decision: no technical manager to negotiate with, no conflicting priorities to balance, no institutional inertia to overcome. Every choice about experimental design, evaluation protocol, and statistical framing was made by one person, based on explicit reasoning logged at the time. That ownership produced a kind of analytical coherence that is harder to achieve when a research direction is negotiated across a team.

The disadvantage was the absence of peer review for those same decisions. In a team environment, a proposed evaluation protocol would be read and questioned by a colleague before the first line of code was written. The circular benchmarking error that produced the R²=0.98 artefact, the most significant methodological mistake in the project, persisted for several weeks precisely because no one else read the data flow across the notebooks and asked why the evaluation set overlapped with the pseudo-label source. Peter Alem's midterm question, which surfaced the problem, was the external review that should have happened earlier. That experience is the clearest evidence of what peer review actually provides that solo work cannot replicate through documentation alone.

Communication with Galchin improved significantly over the project period. The initial updates were too dense and the clinical implications too buried. By mid-project, the structure had been inverted: implications first, methods as supporting context. The dashboard is the fullest realisation of that approach; it shows the SHAP chart and the risk/protective factor labels before it mentions the model architecture, and the About page addresses a practitioner rather than a researcher. Whether this translation succeeded is partly a question of evidence that Galchin's feedback will answer.

---

### 3.3 Evidence of Development

The following artefacts support the competency and learning objective claims made in this portfolio. All files are included in the graduation submission package.

**Midterm presentation slides (April 2026)**
The slide deck prepared for the April 22 midterm presentation with Peter Alem demonstrates the state of technical communication at the midpoint of the internship. The slides show how findings were structured for an academic audience at that stage, including the biological age framing and the R²=0.98 result that were later challenged. As a before-and-after reference point alongside the reframed thesis, the presentation illustrates the development in both framing accuracy and communicative clarity across the internship period.

**Interim report (March–April 2026) — I_Internship.pdf**
The interim report represents the state of technical communication at the midpoint of the internship. It is evidence of both capability and limitation: the document shows how to structure a research narrative for an academic audience, but also reflects the biological age framing error and the uncritical presentation of the R²=0.98 result. As a before-and-after reference point it is more useful than a document that shows only success.

**Midterm feedback form — Interim_Evaluation_Form_Company_Graduation_Project_A_Tanev_Final.docx**
The written feedback from Peter Alem following the April 22 midterm presentation. The document records the two critical challenges raised, the incorrect framing and the implausible performance result, and documents the communication and methodological gaps that the second half of the internship was designed to address.

**Thesis methodology chapter — thesis/methodology.md**
The methodology chapter communicates a complex experimental protocol, including the GroupShuffleSplit design rationale, Wilcoxon signed-rank testing with Bonferroni correction, and three-regime synthetic data ablation, with precision and without ambiguity. Compared to the interim report, it reflects a substantially higher standard of academic communication and a more honest treatment of limitations.

**Thesis discussion chapter Section 5.4 — SHAP interpretation — thesis/discussion.md**
This section translates SHAP model output into physiological terms accessible to a health professional audience, explaining what high waist circumference SHAP values mean for this population and connecting feature importance to existing understanding of metabolic health risk. It bridges technical model output and domain-relevant interpretation, which is the applied form of the learning objective.

**Streamlit application About page — pages/0_About.py**
The About page of the deployed Streamlit dashboard was written explicitly for a non-technical audience. It explains what the tool does, what the model predicts (an approximation of Anovator's bodyAge score, not clinical biological age), and what the known limitations are, in plain language without statistical jargon. The deliberate framing of limitations rather than capabilities reflects the communication standard developed over the course of the internship.

**Internship logbook — thesis/logbook.md**
The logbook documents decisions, challenges, and reflections across all twenty weeks of the internship. It records the systematic documentation practice adopted to compensate for the absence of peer review in a self-directed research environment. The quality of reflection in later entries, compared to the more descriptive early entries, shows development in analytical self-awareness over the internship period.

---

### 3.4 Areas for Further Development

Three areas of professional capability were exposed as underdeveloped by the experience of this project and are identified here without qualification as directions for continued work.

The first is the communication of statistical uncertainty to non-statisticians. Reporting a mean absolute error of 2.43 years with a 95% confidence interval of [2.09, 2.76] is precise and defensible in academic context. Explaining to a practitioner what it means that the prediction could be off by more than two years on a given client, and what that implies for the weight they should give the score in an advising conversation, is a different and harder task. The Streamlit dashboard addresses this imperfectly, and the limitation section of the About page is necessarily compressed. A more complete treatment would require fluency in communicating uncertainty in health contexts specifically, a field with its own literature and practice standards that this project touched but did not engage with systematically.

The second is working within structured organisational environments. Zdravoletie provided minimal procedural structure, and the flexibility that resulted was both an advantage and a gap in professional experience. The ability to work within a structured organisation, where analytical decisions must be approved, where communication has defined channels, and where timelines are constrained by organisational processes rather than personal planning, is a capability that this internship did not exercise.

The third is domain knowledge in health and physiology. The project required biological interpretation of SHAP feature importance outputs, explaining for example why trunk fat distribution and bioimpedance phase angle appeared among the top predictors in physiological terms, without a biology or physiology background. The interpretations offered in the thesis are grounded in the research literature but would benefit substantially from direct collaboration with a clinician.

The fourth is the discipline of building conceptual understanding and practical skill independently, without offloading execution to automated tools. Feedback from a colleague during this project period raised a concern that over-reliance on AI-assisted code generation can produce working outputs while bypassing the reasoning process that builds durable professional competence; a graduate-level practitioner who consistently reaches for a tool to produce code or documentation rather than writing it by hand risks accumulating a surface familiarity with techniques without the depth needed to diagnose, adapt, or defend them under pressure. That observation is valid and I take it seriously. The correct response is not to refuse useful tools but to be deliberate about when assistance accelerates legitimate work and when it substitutes for understanding that I should be building myself. Writing more code, derivations, and documentation by hand, and tolerating the slower pace that entails, is a necessary discipline at this stage of professional development, and one I will treat as a deliberate practice rather than an occasional choice.
