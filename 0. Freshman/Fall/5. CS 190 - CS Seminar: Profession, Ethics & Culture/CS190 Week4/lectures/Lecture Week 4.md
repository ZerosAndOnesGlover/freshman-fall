# CS 190 · CS Seminar: Profession, Ethics & Culture
## Lecture · Week 4: Algorithmic Bias
### Case Studies in Hiring, Lending, and Facial Recognition

**Date:** Wednesday 21 October 2026 · 13:00–13:50 · Week 4

---

## 1. Why "Bias" Is a Harder Word Than It Sounds

Every engineer has heard the phrase "algorithmic bias" by the time they reach this seminar, usually as a vague gesture toward "AI being unfair." This week's goal is to replace that vague gesture with a precise technical and ethical vocabulary — because the word "bias" is doing at least three different jobs in common usage, and conflating them produces bad engineering and bad ethics.

**Statistical bias** is a technical term: an estimator is biased if its expected value differs systematically from the true value it's estimating. This is a property of an algorithm relative to a ground truth, and it is measurable.

**Social bias** refers to systematic disadvantage or advantage correlated with group membership (race, gender, age, disability, etc.), regardless of whether any individual decision-maker intended it. This is a property of an outcome relative to a normative standard of fairness, and normative standards are contested.

**Cognitive bias** refers to a systematic deviation from rational judgment in human decision-making — the kind studied in psychology (anchoring, confirmation bias, availability heuristic). This is a property of human reasoning, but it matters here because human-generated training data encodes human cognitive biases, which algorithms then learn and reproduce.

Algorithmic bias, as this week's topic, sits at the intersection: it is when a computational system exhibits social bias — systematically disadvantaging a group — often (but not always) as a downstream consequence of statistical properties of its training data, its objective function, or its deployment context. Understanding *which mechanism* produced a given instance of bias is a prerequisite to understanding how to fix it — a system that is biased because of skewed training data needs a different remedy than one biased because of a poorly chosen objective function.

---

## 2. The Core Technical Mechanisms

### 2.1 Biased Training Data

The most commonly cited mechanism, and the most intuitive: if the data used to train a model reflects historical patterns of discrimination, a model trained to find patterns in that data will learn — and often amplify — those patterns, even without any protected attribute (race, gender) explicitly included as an input feature.

**Historical hiring data** trained on a company's past hiring decisions will encode whatever bias existed in those past decisions. If a company historically hired mostly men for engineering roles — for whatever combination of societal and discriminatory reasons — a resume-screening model trained on "successful hire" as the label will learn to associate "successful hire" with features correlated with being male, even without gender as an input.

**Historical lending data** trained on past loan approval and default outcomes will encode whatever bias existed in past lending decisions, including redlining-era discriminatory patterns whose effects persist in geographic and demographic proxies decades after the explicit discriminatory policy ended.

### 2.2 Proxy Variables

Even when a protected attribute is explicitly excluded from a model's input features — a common and legally required practice in the US for lending decisions ("fair lending" laws prohibit using race as an input) — the model can still learn to discriminate through **proxy variables**: features that are not the protected attribute itself but are strongly correlated with it.

ZIP code is the canonical example. US residential patterns remain significantly racially segregated as a legacy of historical redlining and other discriminatory housing policies. A lending model that uses ZIP code as a feature — a seemingly neutral piece of geographic information relevant to property values and local economic conditions — can reconstruct much of the predictive power that race would have provided directly, without race ever appearing as an input. This is sometimes called "redlining by algorithm."

The technical challenge this creates: **removing the protected attribute from the input features does not guarantee the model is not discriminating.** This is counterintuitive to many engineers' first instinct ("we didn't include race, so we can't be biased on race") and is one of the most important things to understand this week.

### 2.3 Objective Function Mismatch

Sometimes bias emerges not from data or proxies but from *what the model is being optimized to predict*. A hiring model trained to predict "will this person be rated highly by their manager after one year" is not actually predicting job performance — it's predicting manager approval, which can itself be shaped by biased manager judgment, unequal access to mentorship and advancement opportunities, and workplace culture factors unrelated to the candidate's actual capability. Optimizing for a biased proxy label produces a biased model even with perfectly representative, unbiased input data.

### 2.4 Non-Representative Sampling

If a training dataset underrepresents a demographic group, model performance for that group tends to be worse — not because of any discriminatory pattern in the relevant subset of the data, but simply because there is less data to learn from. This is the primary mechanism behind the facial recognition case study below, and it's mechanically distinct from (though it can compound with) proxy variable and objective function issues.

---

## 3. Case Study: Hiring — Amazon's Resume Screening Tool (2014–2017, discontinued)

### 3.1 What Happened

Amazon built an internal machine learning tool to screen resumes, trained on ten years of resumes submitted to the company, using the pattern of who was actually hired as the training signal. Because the tech industry — and Amazon specifically — had historically hired predominantly men for technical roles, the model learned to systematically downgrade resumes containing the word "women's" (as in "women's chess club captain") and to penalize graduates of two all-women's colleges. The model had, in effect, independently rediscovered gender as a predictive feature and learned to select against it, despite gender never being an explicit input.

### 3.2 Why This Matters Technically

This case is instructive precisely because Amazon's engineers reportedly attempted to correct the specific gendered terms the model was found to penalize — and the model found *other* correlates of gender to discriminate on instead. This illustrates a crucial and general point: patching individual proxy variables after detection is a whack-a-mole strategy against a model that will continue to find new proxies as long as the underlying training signal (historical hiring patterns) encodes the bias. The problem was not a bug in the model; the model was functioning exactly as designed — finding statistical patterns in the training data. The bias was in the data, and no amount of feature engineering downstream fixes a fundamentally biased training signal.

Amazon ultimately discontinued the tool rather than attempting further fixes, reportedly because engineers could not guarantee the model wasn't finding new discriminatory proxies faster than they could identify and remove them.

### 3.3 The Deeper Lesson

"Predict who will be hired" and "predict who is a good candidate" are not the same target, even though they're often treated as interchangeable. The former is a prediction about a human decision process that may itself be biased; the latter is what the company actually wants but cannot directly measure, because "quality of candidate" isn't observed until after a hiring decision has already filtered the population. This is a form of **selection bias**: you only observe performance data for people who were hired, and the hiring decision itself was influenced by the very bias you're trying to detect.

---

## 4. Case Study: Lending — Credit Scoring and the Fair Lending Legal Framework

### 4.1 The Legal Backdrop

The US Equal Credit Opportunity Act (ECOA, 1974) and the Fair Housing Act (1968) prohibit discrimination in lending based on protected characteristics including race, color, religion, national origin, sex, marital status, and age. These laws predate modern machine learning by decades and were written with human loan officers in mind — the legal framework is being adapted, imperfectly, to algorithmic decision-making.

### 4.2 Disparate Treatment vs. Disparate Impact

US anti-discrimination law recognizes two distinct theories of discrimination, and the distinction matters enormously for algorithmic systems:

**Disparate treatment** is intentional discrimination — explicitly using a protected characteristic (or a deliberate proxy for one) as a basis for decisions. This is the easier case to identify and the easier case to defend against by design: don't use race, don't use deliberate proxies for race.

**Disparate impact** is discrimination that results from a facially neutral policy or practice that has a disproportionate adverse effect on a protected group, *regardless of intent*. This is the harder case, and the one most relevant to algorithmic systems trained on historical data: a lending model can have zero discriminatory intent anywhere in its design and still produce disparate impact through the proxy variable mechanism described in Section 2.2.

US courts have generally held that disparate impact liability applies to algorithmic lending decisions, meaning that "we didn't intend to discriminate, and race wasn't an input" is not, by itself, a legal defense if the outcomes are demonstrably disparate and the lender cannot show the practice is justified by legitimate business necessity with no less discriminatory alternative available.

### 4.3 The Technical-Legal Tension: Fairness Through Unawareness Doesn't Work

The most naive fairness intervention — "fairness through unawareness," simply excluding protected attributes from the model's inputs — is precisely the approach that fails against disparate impact claims, because of the proxy variable problem. This creates a genuine technical challenge: how do you build a model that doesn't discriminate on a protected attribute when you're not allowed to use that attribute as an input in the first place (which would often be needed to actively correct for its influence)?

This is not a solved problem. Approaches include: auditing models for disparate impact using protected attribute data collected *separately* from the model's training pipeline (common in practice — lenders collect demographic data for compliance monitoring even though the model doesn't use it as a feature); adversarial debiasing techniques that penalize a model during training for being predictive of a protected attribute even indirectly; and post-processing techniques that adjust model outputs to equalize specific fairness metrics across groups. Each of these approaches has tradeoffs, and none is universally accepted as sufficient — a genuinely unresolved area of active research and litigation.

---

## 5. Case Study: Facial Recognition — Gender Shades (Buolamwini & Gebru, 2018)

### 5.1 The Study

Joy Buolamwini and Timnit Gebru's "Gender Shades" study (2018) evaluated three commercial facial analysis systems (from IBM, Microsoft, and Face++) on their ability to classify gender from facial images, using a dataset deliberately constructed to be balanced across skin tone and gender (the "Pilot Parliaments Benchmark," using images of parliamentarians from countries selected for demographic diversity).

The results: all three systems performed well on lighter-skinned male faces (error rates under 1%) and dramatically worse on darker-skinned female faces (error rates up to 34.7% for one system). The gap wasn't marginal — it was an order of magnitude difference in reliability, concentrated specifically at the intersection of two attributes (dark skin *and* female), a pattern the study's methodology was specifically designed to detect (see intersectionality, below).

### 5.2 The Mechanism: Non-Representative Training Data

Unlike the hiring and lending cases, Gender Shades' primary mechanism was not proxy variables or objective function mismatch — it was straightforward underrepresentation. The benchmark datasets commonly used to train and evaluate facial recognition systems at the time were disproportionately composed of lighter-skinned faces (some analyses found benchmark datasets over 75% male and over 80% lighter-skinned). A model trained predominantly on one demographic learns features that generalize well within that demographic and poorly outside it — this is a straightforward statistical learning phenomenon, not evidence of any discriminatory intent in the modeling process.

### 5.3 Intersectionality: Why Aggregate Accuracy Metrics Hide the Problem

A critical methodological point from this study, with implications far beyond facial recognition: **reporting a single aggregate accuracy number for a system hides subgroup performance disparities.** A system that is 95% accurate "on average" can be 99% accurate on the majority group and 60% accurate on an intersectional minority (a group defined by *combination* of attributes — dark skin *and* female, not either alone), and the aggregate number will never reveal this. Buolamwini and Gebru's methodological contribution was as much about *how to measure* fairness (disaggregated, intersectional analysis) as about the specific finding.

This has become a standard practice recommendation across the field: any fairness evaluation must report performance broken down by relevant subgroups and their intersections, not just in aggregate. This is now referenced in the ACM Code's emphasis (principle 1.4) on fairness and is a direct, actionable engineering practice you should carry into any system you build that makes decisions about people.

### 5.4 Consequences and Response

The study had substantial real-world impact: IBM announced it would stop selling general-purpose facial recognition technology (2020), citing concerns about mass surveillance and racial profiling; Microsoft called for federal regulation of facial recognition; several US cities (San Francisco, Boston, and others) passed municipal bans on government use of facial recognition technology, citing this and related research directly. This is a case where a specific piece of rigorous technical research had a measurable, traceable influence on both corporate policy and municipal law — worth noting as a counterexample to any cynicism about whether technical ethics research "does anything."

---

## 6. Fairness Definitions: Why "Just Make It Fair" Is Not an Instruction

A recurring frustration among engineers new to this material: "fairness" seems like it should be a single, checkable property, but the fairness literature defines *multiple, mathematically incompatible* notions of fairness, and satisfying one can mean violating another.

**Demographic parity (statistical parity):** The proportion of positive outcomes (loan approvals, hires, etc.) should be equal across groups. If 40% of group A's applicants are approved, 40% of group B's applicants should be approved too.

**Equalized odds:** The true positive rate and false positive rate should be equal across groups — i.e., among people who *should* receive a positive outcome, the model should be equally likely to correctly identify them regardless of group, and the same for people who should not.

**Predictive parity (calibration):** Among people the model predicts will receive a positive outcome, the actual rate of positive outcomes should be equal across groups — the model's confidence scores should mean the same thing regardless of group.

### 6.1 The Impossibility Result

A landmark theoretical result (Kleinberg, Mullainathan, Raghavan, 2016; Chouldechova, 2017) proves that **when base rates differ between groups** (i.e., when the true underlying rate of the outcome you're predicting genuinely differs across groups, for whatever reason — including reasons rooted in historical discrimination that a single model cannot undo), **demographic parity, equalized odds, and predictive parity cannot all be satisfied simultaneously**, except in special cases (a perfect predictor, or equal base rates).

This is not an engineering failure to be fixed with a better algorithm. It is a mathematical theorem. It means that **choosing a fairness metric is an ethical and political choice, not a purely technical one** — different fairness definitions encode different values about what a fair outcome means, and you cannot have all of them at once when base rates differ. An engineer who says "we made the model fair" without specifying *which* fairness definition they used, and why that one rather than another, has not actually said anything precise.

### 6.2 Practical Implication

This is why algorithmic fairness work increasingly emphasizes that the choice of fairness metric must be made explicitly, with stakeholder input, and documented — not defaulted to by whichever metric the engineering team happened to optimize for. It also means that claims of "bias-free AI" should be treated with the same skepticism you'd apply to a claim of a general-purpose optimal solution to a provably multi-objective problem — because that is, formally, what it is.

---

## 7. What This Means for You as a Future Engineer

Several concrete, actionable takeaways from this week, independent of which career path (Section 3 of Week 0's careers sheet) you pursue:

1. **Excluding a protected attribute from your model's inputs is necessary but not sufficient** to avoid discrimination on that attribute. You must actively check for proxy variables and disparate impact, using held-out demographic data collected specifically for auditing purposes if necessary.

2. **Aggregate accuracy metrics are close to meaningless for systems that affect people.** Always disaggregate performance by relevant subgroups and their intersections before deploying a system that makes decisions about individuals.

3. **"We didn't intend to discriminate" is a legally and ethically incomplete defense** in a disparate impact framework. Intent is not the only thing that matters; outcomes matter independently.

4. **Fairness metrics conflict with each other by mathematical necessity when base rates differ.** Choosing a fairness definition is a value judgment that should be made explicitly and documented, not left as an implicit default of your training procedure.

5. **The training data is not neutral just because you didn't hand-pick it.** Historical data encodes historical patterns of discrimination whether or not anyone intended it to. "The data says X" is not a value-neutral statement when the data reflects biased human decisions.

---

## Key Terms Introduced This Week

See [[Glossary Week 4]]. New terms: *statistical bias*, *social bias*, *proxy variable*, *selection bias*, *disparate treatment*, *disparate impact*, *fairness through unawareness*, *intersectionality*, *demographic parity*, *equalized odds*, *predictive parity*, *impossibility result (fairness)*.
