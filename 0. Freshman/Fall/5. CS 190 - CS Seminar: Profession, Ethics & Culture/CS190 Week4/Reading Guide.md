# Reading Guide: Week 4

---

## Required Reading

### 1. Buolamwini, J. & Gebru, T. — "Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification" (*Proceedings of Machine Learning Research*, 2018)
**~15 pages. Free at proceedings.mlr.press (search "Gender Shades").**

The primary source for this week's central case study. Read the full paper, including the methodology section — the way the benchmark dataset was constructed is as important as the headline results. Pay attention to how the authors define and measure "intersectional" accuracy, not just per-attribute accuracy.

**Guiding questions:**
- The paper's methodology deliberately constructs a balanced benchmark dataset rather than using an existing one. Why does this matter? What would have been lost if they had used an existing, unbalanced benchmark instead?
- The paper reports results per company (IBM, Microsoft, Face++) rather than anonymizing them. What are the ethical considerations in naming specific commercial products in a critical academic paper? Do you think this was the right call?

### 2. Dastin, J. — "Amazon scraps secret AI recruiting tool that showed bias against women" (Reuters, 2018)
**~5 pages. Free at reuters.com (search title).**

The primary journalistic account of the Amazon hiring case study. Note this is journalism, not a peer-reviewed technical paper — read it with an eye toward what claims are sourced and how, since Amazon's internal tool and its failure were never published in a technical paper by Amazon itself.

**Guiding question:**
- The article is based on anonymous sources with knowledge of the project, since Amazon did not publish the tool's failure publicly. What does this tell you about how bias failures in industry are typically discovered and reported — and what failures might never come to public light because no journalist obtains sourcing?

### 3. Kleinberg, J., Mullainathan, S., Raghavan, M. — "Inherent Trade-Offs in the Fair Determination of Risk Scores" (2016)
**~10 pages (read Sections 1–3; the later sections are more mathematically technical than required). Free at arxiv.org (search title).**

The original impossibility result paper. This is a theoretical computer science paper — you do not need to follow every proof step, but you should understand the informal statement of the theorem and why it holds. This connects directly to CS 101/MATH 151's emphasis on formal proof as a tool for settling questions that intuition alone cannot.

**Guiding question:**
- The paper's result is often summarized as "you can't have it all" regarding fairness definitions. State, in your own words and without equations, what specific tradeoff the theorem establishes, and under what condition (base rate equality) the tradeoff disappears.

---

## Optional / Enrichment Reading

### 4. Angwin, J., Larson, J., Mattu, S., Kirchner, L. — "Machine Bias" (ProPublica, 2016)
**Free at propublica.org.** The COMPAS recidivism-scoring investigation — a different domain (criminal justice risk assessment) than this week's three case studies, useful if you want a fourth example, and one that directly illustrates the equalized-odds-vs-predictive-parity conflict in a real, contested case (Northpointe, the tool's vendor, disputed ProPublica's framing using a different fairness metric — a real-world instance of the impossibility result in action).

### 5. Barocas, S., Hardt, M., Narayanan, A. — *Fairness and Machine Learning*, Chapter 1
**Free online at fairmlbook.org.** The standard technical reference text for algorithmic fairness. Chapter 1 gives a broader technical taxonomy of bias mechanisms than this week's lecture covers, if you want to go deeper.
