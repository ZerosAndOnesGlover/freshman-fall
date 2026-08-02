# Glossary: Week 4 Additions

---

**Statistical Bias**
In statistics and machine learning, the systematic difference between an estimator's expected value and the true value it is estimating. A technical, measurable property distinct from social or ethical connotations of "bias."

**Social Bias (Algorithmic)**
Systematic disadvantage or advantage in a system's outcomes correlated with membership in a demographic group, regardless of the intent of the system's designers. The primary subject of this week's lecture.

**Proxy Variable**
An input feature that is not itself a protected attribute (race, gender, etc.) but is statistically correlated with one, such that a model can learn to discriminate on the protected attribute indirectly through the proxy, even when the protected attribute is explicitly excluded from the model's inputs. Example: ZIP code as a proxy for race in the US, due to historically segregated residential patterns.

**Selection Bias**
A bias arising because the data available for training or evaluation is not a representative sample of the population of interest, often because the sampling process itself is influenced by the outcome being studied. In the Amazon hiring case: only resumes of people who were hired have observed "success" labels, and the hiring decision itself was shaped by the bias being investigated.

**Objective Function Mismatch**
A source of bias arising when the quantity a model is trained to optimize (the objective/label) is a biased or incomplete proxy for the quantity actually intended to be measured or achieved — e.g., training to predict "manager approval rating" as a stand-in for "job performance," when manager approval is itself shaped by bias.

**Disparate Treatment**
A legal theory of discrimination (US anti-discrimination law) involving intentional differential treatment based on a protected characteristic, or a deliberate proxy for one. Requires proof of discriminatory intent.

**Disparate Impact**
A legal theory of discrimination (US anti-discrimination law) in which a facially neutral policy or practice has a disproportionate adverse effect on a protected group, regardless of intent. Applicable to algorithmic systems even when no protected attribute is used as an input and no discriminatory intent exists in the design process.

**Fairness Through Unawareness**
The (insufficient) practice of attempting to prevent algorithmic discrimination solely by excluding protected attributes from a model's input features. Fails against disparate impact due to the proxy variable mechanism.

**Intersectionality**
A framework (originating in legal scholarship, Kimberlé Crenshaw, 1989) recognizing that individuals who belong to multiple marginalized groups simultaneously (e.g., dark-skinned women) can experience distinct forms of disadvantage not predictable from either group membership alone. In algorithmic fairness evaluation: performance disparities can be concentrated at specific intersections of attributes that are invisible in analyses that consider each attribute separately.

**Demographic Parity (Statistical Parity)**
A fairness criterion requiring that the proportion of positive outcomes be equal across demographic groups, regardless of the actual (ground-truth) distribution of the outcome across those groups.

**Equalized Odds**
A fairness criterion requiring that the true positive rate and false positive rate of a model be equal across demographic groups — i.e., the model's accuracy conditional on the true outcome should not depend on group membership.

**Predictive Parity (Calibration)**
A fairness criterion requiring that, among individuals a model assigns a given predicted outcome or score, the actual rate of that outcome be equal across demographic groups — i.e., the model's predictions should mean the same thing regardless of group.

**Impossibility Result (Fairness)**
A theoretical result (Kleinberg, Mullainathan, Raghavan, 2016; Chouldechova, 2017) proving that when base rates of an outcome differ between groups, demographic parity, equalized odds, and predictive parity cannot all be satisfied simultaneously by any predictor except in degenerate cases (a perfect predictor, or equal base rates). Establishes that choosing among fairness definitions is a value-laden choice, not a purely technical optimization problem.

**Base Rate**
The underlying, true frequency of an outcome in a population or subgroup, prior to any prediction or intervention. Differences in base rates between groups (which may themselves result from historical discrimination) are the condition under which the fairness impossibility result applies.
