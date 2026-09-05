# CS 190 · CS Seminar: Profession, Ethics & Culture
## Lecture · Week 6: AI and Society
### Autonomous Weapons, Deepfakes, and LLMs

**Date:** Wednesday 30 September 2026 · 13:00–13:50 · Week 6

---

## 1. Why This Week Is Different From Week 4

Week 4 examined algorithmic bias — cases where a system's *intended* function (screen resumes, score creditworthiness, recognize faces) produces unintended discriminatory harm. This week examines something structurally different: systems whose *intended* function is itself the subject of live ethical dispute, independent of whether they work correctly or fairly. An autonomous weapon that identifies and engages targets with perfect accuracy raises a different set of questions than a biased one. A deepfake that is technically flawless is not less ethically fraught than a crude one — arguably more so. This week asks you to reason about cases where the technology working exactly as intended is itself the problem to be reckoned with, not a side effect of it malfunctioning.

---

## 2. Autonomous Weapons Systems

### 2.1 Definitions and the Spectrum of Autonomy

**Lethal Autonomous Weapons Systems (LAWS)** is the term of art used in international policy discussions (particularly at the UN Convention on Certain Conventional Weapons, CCW) for weapons systems that can select and engage targets without human intervention. The definition matters enormously because "autonomy" is not binary — it describes a spectrum, and where a given system falls on that spectrum changes the ethical and legal analysis substantially.

A useful three-tier framework, commonly used in this literature:

**Human-in-the-loop:** A human must authorize each engagement. The system may identify candidate targets, track them, and recommend engagement, but a human makes the final decision to fire. Most currently deployed systems described as "autonomous weapons" — Israel's Iron Dome, various loitering munitions — actually fall here, with debate over how meaningful the human's role actually is when decisions must be made in seconds.

**Human-on-the-loop:** The system operates autonomously but a human monitors and can intervene or override. The human is a supervisor rather than an approver of each action — meaningful oversight depends on whether the human has enough time, information, and situational awareness to actually exercise the override in practice, which is often doubtful.

**Human-out-of-the-loop (fully autonomous):** The system selects and engages targets with no human review of individual engagement decisions, potentially after only a general mission authorization. This is the tier that generates the most serious ethical and legal controversy, and the tier that current international humanitarian law was not written with in mind.

### 2.2 The Core Ethical Arguments

**The case that autonomous weapons could reduce harm:** Proponents (including some military ethicists) argue that autonomous systems could, in principle, comply with the laws of armed conflict — distinction (targeting only combatants, not civilians) and proportionality (avoiding excessive civilian harm relative to military advantage) — more reliably than human soldiers, who are subject to fear, fatigue, anger, and the psychological pressures of combat that produce war crimes and mistaken targeting. A sufficiently well-designed system, this argument holds, removes a source of human error and human atrocity from war, not just efficiency gains.

**The case against, on accountability grounds:** The central counterargument, articulated forcefully by the Campaign to Stop Killer Robots and by scholars like Peter Asaro, is the **accountability gap**: when an autonomous system makes a lethal targeting error, who is responsible? Not the weapon, which has no moral agency. Not necessarily the human operator, who did not make the specific targeting decision. Possibly the programmer, the military commander who authorized deployment, or the manufacturer — but existing legal and military accountability frameworks (courts-martial, command responsibility doctrine) were built around human decision-makers making discrete decisions, and do not map cleanly onto a distributed responsibility chain involving a learned, probabilistic system whose specific failure mode may not be traceable to any single identifiable design or command decision. This is not a hypothetical problem — it is a real gap in existing accountability structures that international law has not resolved.

**The case against, on human dignity grounds:** A distinct argument, associated with the International Committee of the Red Cross among others, holds that even a perfectly accurate autonomous weapon is ethically objectionable because life-and-death decisions about a specific human being should not be delegated to a machine incapable of genuine moral judgment, empathy, or the capacity to exercise mercy — that something essential to the moral seriousness of taking a human life is lost when the decision is made by an algorithm regardless of its accuracy. This argument does not depend on the system malfunctioning; it holds even for a system that works perfectly.

### 2.3 The Existing Legal Framework and Its Gaps

International Humanitarian Law (IHL), primarily the Geneva Conventions and their Additional Protocols, requires that any new weapon be evaluated (Additional Protocol I, Article 36) for compliance with IHL before deployment — including distinction and proportionality. The difficulty: these are legal standards developed for evaluating human judgment applied to specific circumstances, and it is genuinely unclear how to certify, in advance, that a machine learning system will reliably make context-dependent proportionality judgments across the enormous variety of real combat situations it might encounter — situations that, by definition, cannot all be anticipated and tested in advance the way a discrete weapons system (a specific munition with a specific blast radius) can be.

As of this writing, there is no binding international treaty specifically regulating or banning LAWS, despite a decade of discussions at the UN CCW. A coalition of states and NGOs advocates for a preemptive ban; other states (including several with advanced military AI programs) oppose a ban and argue for a framework of "meaningful human control" requirements instead — a framework that itself remains without precise, agreed-upon definition.

---

## 3. Deepfakes

### 3.1 The Technical Mechanism (Briefly)

A deepfake is synthetic media — image, audio, or video — generated or manipulated using deep learning techniques (most commonly generative adversarial networks, GANs, or more recently diffusion models) to depict a person doing or saying something they did not actually do or say, in a way designed to be visually or audibly convincing. You will study the underlying generative model architectures formally in CS 331 (Artificial Intelligence, Year 3); this week's focus is on the societal consequences of the capability, which do not require understanding the underlying architecture in detail, only its output properties: increasingly high fidelity, decreasing cost and technical skill required to produce, and increasingly real-time generation capability (live deepfake video calls are now technically feasible).

### 3.2 Categories of Harm

**Non-consensual intimate imagery (NCII):** The single largest category of deepfake harm by volume is the creation of non-consensual sexual imagery, overwhelmingly targeting women, using their likeness without consent. Multiple studies of deepfake content online have found this category constitutes the substantial majority of deepfake material in circulation — a fact that should reframe any discussion of deepfakes that treats political disinformation as the primary use case. This is a serious, ongoing, and disproportionately gendered harm, and it has prompted specific legislative responses (several US states have criminalized non-consensual deepfake pornography; the UK's Online Safety Act addresses it directly).

**Political disinformation:** Synthetic video or audio of political figures saying things they never said, deployed to influence elections, incite violence, or damage reputations. The threat here is compounded by a second-order effect sometimes called the **liar's dividend** (a term from legal scholars Bobby Chesney and Danielle Citron): as public awareness of deepfakes increases, real, authentic footage of genuine wrongdoing can be dismissed as "probably a deepfake" by the person it implicates, providing a plausible deniability mechanism that did not exist before the technology did. The harm of deepfakes, in this sense, is not limited to the fake content itself — it degrades the evidentiary value of *all* video and audio, including genuine recordings.

**Fraud:** Voice-cloning technology has been used in real, documented cases of fraud — impersonating executives' voices to authorize fraudulent wire transfers (a documented case involved a UK energy firm's CEO being impersonated via AI-generated voice to authorize a $243,000 transfer in 2019), and impersonating family members' voices in "grandparent scam" variants to extract emergency funds from victims who believe they are speaking to a relative in distress.

**Reputational and personal harm beyond NCII:** Fabricated video of ordinary individuals (not just public figures) saying or doing damaging things, used in harassment, workplace disputes, or interpersonal conflict — a category of harm that scales down to affect private individuals with essentially the same technology used against public figures.

### 3.3 Technical and Policy Responses

**Detection:** An active area of research building classifiers to distinguish synthetic from authentic media, but this is fundamentally an adversarial arms race — detection techniques inform generation techniques designed to evade them (an instance of the same generative adversarial dynamic used to create the content in the first place), meaning detection is unlikely to be a durable solution on its own.

**Provenance and authentication:** An alternative approach, exemplified by the Coalition for Content Provenance and Authenticity (C2PA, backed by Adobe, Microsoft, and others), focuses not on detecting fakes but on cryptographically signing and tracking the provenance of authentic media at the point of capture — shifting the burden from "prove this is fake" to "verify this is authentic," which is a fundamentally different and arguably more tractable engineering problem, though it requires widespread adoption by camera and device manufacturers to be effective and does nothing for the vast existing corpus of unsigned media.

**Legal response:** A patchwork, similar to the privacy law landscape from Week 5 — some jurisdictions have specific deepfake statutes (particularly for NCII and election-related deepfakes within a specified window before voting), but comprehensive frameworks are absent in most jurisdictions, and the same jurisdictional and enforcement challenges that complicate privacy law apply here, compounded by the difficulty of identifying anonymous creators.

---

## 4. Large Language Models and Society

### 4.1 What Changed, Technically, and Why It Matters Here

You will study the technical architecture of large language models formally in CS 331 (attention mechanisms, the Transformer architecture, training via next-token prediction at scale). This week's concern is narrower and more immediate: LLMs represent a capability that is qualitatively different from prior natural language processing systems in ways that create genuinely new categories of societal question, not merely a scaled-up version of old ones.

The key qualitative shifts: **generality** (a single model handles an enormous range of tasks — translation, summarization, code generation, creative writing, tutoring — without task-specific engineering, unlike prior NLP systems that were narrowly built for one task); **fluency** (output is grammatically and stylistically indistinguishable from human writing in most contexts, removing a signal — awkward machine-generated text — that previously helped people identify automated content); and **scale of deployment** (hundreds of millions of people interact with LLM-based systems, embedding them in education, customer service, coding, medicine, and law with a speed of adoption that has outpaced the development of norms, regulation, or even basic empirical understanding of the systems' failure modes).

### 4.2 Misinformation and Hallucination

LLMs generate **hallucinations** — fluent, confident, and false statements presented with the same stylistic register as accurate ones, without any internal signal (to the user) distinguishing reliable from unreliable output. This differs qualitatively from prior misinformation problems: a human-authored false article can be traced to an author with identifiable motives and track record; a hallucinated citation, legal precedent, or medical claim from an LLM has no author in the traditional sense and can be generated at a volume and speed no team of human misinformation writers could match, on any topic, on demand.

This has produced documented real-world harms already: lawyers submitting court filings containing entirely fabricated case citations generated by an LLM and not verified before filing (several documented, sanctioned cases in US courts); students and professionals relying on confidently incorrect factual claims in domains where verification is not straightforward for a non-expert.

### 4.3 Labor and Economic Disruption

LLMs and adjacent AI systems are displacing or transforming labor in ways that echo — but also differ from — historical automation waves (mechanization of agriculture, industrial automation of manufacturing). Two dimensions worth separating carefully, since they are often conflated:

**Task automation vs. job elimination:** Most current evidence suggests LLMs automate specific *tasks* within jobs (drafting routine text, generating boilerplate code, summarizing documents) more often than eliminating entire job categories outright — but the net effect on total employment, wages, and the distribution of which tasks remain valuably human is genuinely disputed among economists, and differs enormously by occupation. Distinguishing "this technology changes what I do" from "this technology eliminates the need for me" is analytically important and frequently blurred in popular discussion.

**Distributional effects:** Historical automation waves have generally increased aggregate productivity while imposing concentrated costs on specific groups of displaced workers, often with a significant time lag before new job categories absorb displaced labor (if they do) — and the transition costs are borne disproportionately by workers, not by the capital owners who benefit from productivity gains. Whether LLM-driven automation follows this historical pattern, follows it faster (due to the breadth of tasks affected simultaneously across many occupations at once, rather than one sector at a time as in prior automation waves), or differs in some other structural way, is an open empirical question with enormous policy stakes — not a settled matter you should treat as resolved in either direction.

### 4.4 Epistemic Effects: Trust, Authorship, and the Information Environment

A less concrete but arguably more foundational concern: LLMs complicate basic questions about authorship, expertise, and trust that underlie how societies establish shared factual understanding. If a substantial fraction of online text, reviews, comments, and even scientific abstracts are LLM-generated (a phenomenon already measurably occurring), the traditional signals humans use to calibrate trust — an identifiable author with a track record, a byline, a institutional affiliation — degrade, without a clear replacement mechanism yet established. This connects directly to the "liar's dividend" dynamic discussed for deepfakes: it is not only that false content becomes easier to produce, but that the erosion of reliable signals of authenticity degrades trust in *all* content, true or false, human or synthetic.

### 4.5 Existential and Long-Term Risk Debates

A distinct and highly contested strand of the AI-and-society conversation concerns long-term or "existential" risk — the concern, associated with researchers including those at leading AI labs' safety teams as well as independent AI safety organizations, that sufficiently advanced AI systems could pose risks to humanity's long-term survival or flourishing that are qualitatively different from (and more severe than) the nearer-term harms discussed above (bias, misinformation, labor disruption).

This is a genuinely contested area within the AI research community itself — serious researchers disagree sharply on the plausibility, timeline, and nature of such risks, and the debate is frequently entangled with commercial and reputational incentives on multiple sides (labs emphasizing risk may benefit from regulatory capture against smaller competitors; labs downplaying risk may be minimizing scrutiny of their commercial products). This seminar takes no institutional position on this debate — it is flagged here because you will encounter it constantly in industry, media, and policy discussions throughout your career, and you should be aware that credentialed, serious people hold sharply divergent views on it, which is itself informative about the current state of the field's understanding of its own trajectory.

---

## 5. A Unifying Analytical Frame for This Week

Across autonomous weapons, deepfakes, and LLMs, notice a recurring structure worth carrying forward as a general analytical tool:

1. **Capability outpaces governance.** In each case, the technical capability has developed and deployed faster than legal, regulatory, or normative frameworks have adapted to govern it. This is not a coincidence specific to AI — it echoes the internet's own history (Week 1, Week 2) — but the pace is faster and the stakes in several of these cases (lethal force, non-consensual imagery, mass-scale misinformation) are higher.

2. **The technology working correctly is sometimes the problem, not a failure mode.** Unlike Week 4's algorithmic bias content, where the goal was to make systems work *better* to reduce harm, several of this week's cases involve systems whose correct, intended function is itself ethically contested — a perfectly accurate autonomous weapon, a perfectly realistic deepfake, a perfectly fluent hallucination.

3. **Accountability structures built for human decision-makers do not map cleanly onto distributed, probabilistic, or synthetic systems.** The accountability gap in autonomous weapons has structural analogues in deepfake harm (anonymous or jurisdictionally distant creators) and LLM hallucination (no traditional "author" to hold accountable for a false claim).

Carry this frame into next week's discussion of intellectual property (Week 7), which will apply many of the same structural questions — capability outpacing law, contested legitimacy of the technology's core function, and unclear accountability — to a different domain.

---

## Position Paper #2

Assigned this week — see `Position Paper 2.md` for the full prompt. Due before the Week 7 seminar.

---

## Key Terms Introduced This Week

See `Glossary Week 6.md`. New terms: *LAWS (Lethal Autonomous Weapons Systems)*, *human-in/on/out-of-the-loop*, *accountability gap*, *distinction and proportionality (IHL)*, *deepfake*, *NCII*, *liar's dividend*, *C2PA / content provenance*, *hallucination (LLM)*, *task automation vs. job elimination*, *existential risk (AI)*.
