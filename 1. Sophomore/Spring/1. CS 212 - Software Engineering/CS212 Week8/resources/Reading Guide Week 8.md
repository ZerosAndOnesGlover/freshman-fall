# CS 212 · Reading Guide · Week 8

---

## Required

| # | What | Length | Why |
|---|---|---|---|
| 1 | **Fowler, *"Continuous Integration"*** (2006, martinfowler.com) | ~30 min | **The definition, in which no tool appears.** Read the ten practices and notice which five do the work |
| 2 | **SEC, *Administrative Proceeding File 3-15570*** (Knight Capital, 2013) | **12 pages** | **Read it.** It is a readable legal document about a deployment, it names all five failures, and every one has a cheap mechanical answer. The best forty minutes in this week |
| 3 | **The Twelve-Factor App** — factors **III (Config)**, **V (Build/release/run)** and **X (Dev/prod parity)** | ~10 min | Three short pages. Factor V is L26 §6's "build once, promote the same artefact" |
| 4 | **Docker docs** — "Best practices for writing Dockerfiles" | ~20 min | Layer caching and multi-stage builds, which are 14 of A 8's marks |

**About ninety minutes.** Read the SEC filing even if you read nothing else.

---

## Recommended

| What | Why |
|---|---|
| **Forsgren, Humble & Kim, *Accelerate*** (2018), Ch. 1–3 | The four DORA metrics and the batch-size argument. **Read Ch. 2 for the methodology**, because A 8 does not ask you to trust it and L25 §6 names two caveats |
| **Fowler, *"FeatureToggle"*** and **"BranchByAbstraction"** | Two bliki entries, ten minutes together. The second is Week 9's technique arriving early |
| **Humble & Farley, *Continuous Delivery*** (2010), Ch. 5 | Where the deployment-pipeline pattern comes from. Dated on tooling, correct on shape |
| **Nygard, *Release It!*, 2nd ed.**, Ch. 4–5 | Failure modes in production, and the stability patterns. **The best book on this list if you only read one** |
| **GitHub Actions docs** — caching, service containers, `concurrency` | The three features that account for most of A 8 Q1's time savings |

---

## Read the SEC Filing Properly

**Forty minutes, and it will change how you think about deployment more than any lecture can.**

It is not a technical document; it is a regulator establishing what happened. **Which makes it unusually good for this purpose**, because it records the *organisational* facts that a post-mortem written by engineers would omit.

**Read for these specifically:**

1. **§15–17: the deployment.** A technician copying code to eight servers over a week. **Note that there was no verification step at all** — not a weak one, none — and that this was normal practice.
2. **§18: the flag.** The new code repurposed a flag that previously activated **Power Peg**, dead for eight years and never removed. **Note that removing dead code was nobody's job.**
3. **§21–24: the alerts.** System emails fired at **08:01**, ninety-seven minutes before the market opened, mentioning Power Peg. **Nobody knew what they meant, so nobody acted.** This is the clearest real-world instance of L27 §6's rule that an alert must say what to do.
4. **§30 onwards: the 45 minutes.** Note how long it took to work out *which* server, and why: they had no way to ask what each host was running.

**Then ask the question A 8 Q5(b) asks:** which of the five would your pipeline now catch? **The SHA-verification step in L27 §4 is nine lines of YAML, and it is the direct answer to the first and fourth.**

---

## A Note on the Evidence, Which Is Unusually Good Here

W0 L02 §8 rated CI's evidence **strong**, and this is the week where that rating pays off. **The reason it is strong is that the outcomes are countable without asking anyone's opinion**: how often you deployed, how long a change took, how often it broke, how long recovery took. No survey of feelings, no proxy for quality.

**Two caveats, and A 8 does not require you to accept the findings:**

- **The DORA data is self-reported and self-selected** — the respondents are people who answer DevOps surveys.
- **It is correlational.** Organisations that deploy well may simply be well-run, and the causal arrow is not established.

**What makes it persuasive anyway is the mechanism**, and it is the same mechanism you have now met three times: **batch size.** Small deploys are easier to diagnose and revert; small pull requests get better reviews (W7 L22 §4); small TDD steps are where the benefit actually lies (W5 L17 §3). **Three practices, three literatures, one underlying reason** — which is a stronger form of evidence than any one study.

---

*CS 212 · Week 8 · Reading Guide*
