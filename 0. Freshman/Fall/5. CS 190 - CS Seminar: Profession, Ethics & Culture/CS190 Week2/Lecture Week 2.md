# CS 190 · CS Seminar: Profession, Ethics & Culture
## Lecture · Week 2: How Software Gets Built
### Agile, Open Source, and Research Labs

**Date:** Wednesday 2 September 2026 · 13:00–13:50 · Week 2

---

## 1. Why This Week Exists in an Ethics Seminar

CS 190 is primarily an ethics and professional culture course, so it might seem odd to spend a week on software development process. The reason: the ethical questions this seminar raises in later weeks — about algorithmic bias, privacy, AI safety, responsible disclosure — do not arise in a vacuum. They arise inside specific institutional contexts: a startup running two-week sprints, a company with a monorepo and 2,000 engineers, an open-source project governed by a foundation, a university research lab trying to publish before a competitor does. The context shapes which ethical pressures are felt, which ones are invisible, and which ones are structurally incentivized against.

If you do not understand how software is actually built, you will reason about software ethics in the abstract — and abstract ethical reasoning produces conclusions that don't survive contact with real organizational dynamics. This week gives you the organizational context you need for the rest of the semester.

---

## 2. The Problem Software Development Is Trying to Solve

Before discussing *methods*, it's worth naming the underlying problem all methods are responding to.

Building software is unusual as an engineering discipline in the following sense: the "material" — logic and abstraction — is infinitely malleable. You can change a software system far more radically than you can change a bridge or a building. This sounds like a gift, and in some ways it is. But it creates a specific failure mode that doesn't afflict civil or mechanical engineering as severely: **requirements change during construction**, and construction is slow enough that by the time something is built, what was needed has evolved.

Additionally, software systems are complex in the technical sense: emergent behavior arises from the interaction of components that individually behave simply. A system of 10 components with 10 interactions each has 100 interaction paths. At 100 components each with 100 interactions, it has 10,000. No human can hold this in their head. Coordination across the people building the system adds another layer of complexity on top of the system itself.

Every software development methodology is, at bottom, an attempt to manage these two problems: **changing requirements** and **coordination complexity**. Where they differ is in their assumptions about which of these problems is more fundamental, and which tradeoffs are acceptable.

---

## 3. Waterfall: The Method Most Developers Have Never Used But Always Criticize

### 3.1 What Waterfall Actually Said

"Waterfall" development — the sequential model where you complete Requirements, then Design, then Implementation, then Testing, then Deployment in order — is widely blamed for software project failures and widely held to be the alternative against which Agile defines itself. It is worth understanding what it actually claimed before accepting the critique.

Winston Royce's 1970 paper "Managing the Development of Large Software Systems" is the document from which "waterfall" derives, and it is routinely misread. Royce did describe the sequential phases — but he explicitly argued that executing them in strict sequence without feedback is *risky and should be avoided*. He recommended iteration between phases. The rigid sequential waterfall that became the software industry's punching bag was a distortion of what Royce wrote.

The waterfall model, even in its rigid form, reflects a reasonable engineering intuition: the cost of fixing a mistake rises as you proceed through development. A requirements error caught before design is cheap to fix; caught after deployment, it may require rebuilding the system. The waterfall's logic was: front-load the thinking to prevent late and expensive rework.

### 3.2 Where Waterfall Fails

The problem is that its central assumption — that requirements can be completely and correctly specified upfront — is empirically false for most software systems. Users often do not know what they want until they see something that's almost right. The market changes between the specification and the delivery. Regulatory requirements evolve. Competitors release features that redefine what "good" means.

When requirements change mid-project under a waterfall model, the entire preceding work product (requirements documents, design documents, partially built systems) may be partially invalidated. The rigidity that was meant to prevent rework creates the conditions for massive rework.

---

## 4. Agile: The Reaction

### 4.1 The Agile Manifesto (2001)

In February 2001, seventeen software practitioners met in Snowbird, Utah, and produced a document called the Agile Manifesto. It is short enough to quote in full:

> We are uncovering better ways of developing software by doing it and helping others do it. Through this work we have come to value:
>
> **Individuals and interactions** over processes and tools
> **Working software** over comprehensive documentation
> **Customer collaboration** over contract negotiation
> **Responding to change** over following a plan
>
> That is, while there is value in the items on the right, we value the items on the left more.

Four value statements, each structured as a contrast. Note what the manifesto *doesn't* say: it doesn't say documentation is worthless, or that plans are useless. The "over" formulation is deliberate — it's a prioritization, not an elimination.

The manifesto also produced twelve principles, of which the most important for understanding the philosophy are:

- "Our highest priority is to satisfy the customer through early and continuous delivery of valuable software."
- "Welcome changing requirements, even late in development."
- "Deliver working software frequently, from a couple of weeks to a couple of months, with a preference to the shorter timescale."
- "Working software is the primary measure of progress."

### 4.2 Scrum: The Dominant Agile Implementation

Scrum is the specific Agile framework most commonly used in industry. Its key elements:

**Sprints:** Fixed-duration work cycles, typically 1–2 weeks. At the start of each sprint, the team selects work from the product backlog. At the end, they deliver working software — not a document, not a plan, but something that runs and does something.

**The Product Backlog:** A prioritized list of features, bug fixes, and other work, expressed as "user stories" (short descriptions of functionality from the user's perspective: "As a user, I want to reset my password so that I can regain access to my account if I forget it."). The backlog is never fully complete — it is continuously refined.

**The Sprint Retrospective:** At the end of each sprint, the team reflects on its own process: what went well, what didn't, what to change. This is the Agile feedback loop applied to the development process itself, not just the product.

**Daily Standup:** A brief (~15 minute) daily meeting where each team member answers three questions: what did I do yesterday, what will I do today, what is blocking me. The explicit purpose is coordination and obstacle identification, not status reporting to management.

**The Product Owner and Scrum Master:** The Product Owner represents the business/user perspective and owns the backlog prioritization. The Scrum Master is responsible for protecting the team's process — not a project manager in the traditional sense, but a facilitator who removes impediments.

### 4.3 Kanban: The Alternative

Kanban (from the Japanese manufacturing practice) organizes work as a board of columns (typically: To Do → In Progress → Review → Done), with a key constraint: a **WIP limit** (Work In Progress limit) on each column. The WIP limit prevents the system from taking on more work than it can complete, which surfaces bottlenecks: if the Review column is full, new work cannot be started until reviewing is done — forcing the team to address the bottleneck rather than pile more work in front of it.

Kanban is flow-based rather than iteration-based. There are no fixed sprints; work flows continuously. Teams that do maintenance work (where interruptions are inherent) or operations work (where demand is unpredictable) often prefer Kanban to Scrum for this reason.

### 4.4 The Agile Industrial Complex

A note of honest caution about Agile as it actually manifests in many organizations: there is a large industry of Agile certifications, consultants, and frameworks (SAFe — Scaled Agile Framework — is the most prominent at enterprise scale) that has, in the view of many practitioners, distorted Agile's original intent beyond recognition.

The original Agile Manifesto valued "individuals and interactions over processes and tools." Many large-scale "Agile transformations" have replaced one bureaucratic process (waterfall documentation) with another (SAFe ceremonies, PI planning, portfolio backlogs) while delivering no meaningful improvement in responsiveness or software quality. This is sometimes called "Agile in name only" or, more critically, "cargo-cult Agile" — adopting the rituals without the underlying philosophy.

The ethical dimension here: the velocity and sprint metrics that Agile frameworks generate are routinely used by management to surveil and pressure engineering teams in ways the Agile Manifesto explicitly opposed. "Story points" — originally a relative complexity measure internal to the team — are routinely converted into productivity metrics and compared across teams by management, invalidating their original purpose (Goodhart's Law: when a measure becomes a target, it ceases to be a good measure).

---

## 5. Open Source: Code as Commons

### 5.1 What Open Source Is

Open source software is software whose source code is publicly available and can be inspected, modified, and distributed by anyone, subject to the terms of a license. The Open Source Initiative maintains a formal definition with ten criteria (including free redistribution, access to source code, and no discrimination against persons or fields of endeavor).

This sounds simple but represents a radical departure from the default intellectual property model for software, which treats source code as a trade secret and the compiled binary as the product sold.

### 5.2 A Brief History

**Richard Stallman** (1983) launched the GNU Project with the goal of creating a completely free (as in freedom, not price) Unix-compatible operating system. Stallman's **GNU General Public License (GPL)** (1989) was a legal innovation as much as a technical one: it used copyright law *against itself* — the GPL grants you broad rights to use, modify, and distribute, but requires that any distributed modifications must themselves be GPL-licensed. This "copyleft" provision prevents the commons from being enclosed: you cannot take GPL code, improve it, and release only the binary. Stallman's framing was explicitly political: software freedom as a matter of users' rights.

**Linus Torvalds** (1991) released the Linux kernel under GPL. Combined with the GNU utilities and tools, this produced the GNU/Linux operating system — now the operating system running the majority of the world's servers, every Android device, and most of the cloud infrastructure your programs will run on.

**The Open Source Initiative** (1998) was founded partly in reaction to Stallman's explicitly political framing — some practitioners wanted to make the case for open source on purely practical grounds (better software through community review) rather than ideological ones. The term "open source" was itself a deliberate rebrand away from "free software" to be more palatable to corporate decision-makers.

### 5.3 The Modern Open Source Ecosystem

Today, open source is the dominant model for software infrastructure. The languages you will use in this degree (Python, with its CPython interpreter; even LLVM, the compiler infrastructure underlying Clang and Rust) are open source. The tools (Git, GCC, Valgrind, Docker) are open source. The frameworks (React, TensorFlow, PyTorch, Kubernetes) are open source. Major tech companies — Google, Meta, Microsoft, Amazon — release significant open source projects and employ engineers whose primary job is open source contribution.

### 5.4 License Taxonomy: What the License Actually Means

Open source licenses differ significantly in what they permit. The most important distinction:

**Copyleft licenses (GPL, LGPL, AGPL):** Require that modified versions and derivative works be released under the same license. The "viral" property. Strong GPL: applies to the entire combined work. LGPL: weaker — linking a program to a GPL library doesn't require the program itself to be GPL. AGPL: the "network use" variant — if you run GPL'd software as a web service, the AGPL requires you to provide source to users even if you never distribute a binary.

**Permissive licenses (MIT, BSD, Apache 2.0):** Allow modification and redistribution with few restrictions, including incorporation into proprietary software. MIT is the most permissive common license — essentially "do anything, keep the copyright notice." Apache 2.0 adds an explicit patent grant. BSD comes in variants (2-clause, 3-clause) with minor differences.

**The Business Source License and "source-available" licenses:** A newer category, adopted by companies like HashiCorp and Elastic, that make source code available but restrict certain commercial uses. These are technically *not* open source by the OSI definition, though they are sometimes marketed with open-source-adjacent language. Understanding this distinction matters: MongoDB's SSPL and HashiCorp's BSL were both adopted after the companies became concerned that cloud providers (primarily AWS) were offering their software as a hosted service and capturing revenue that the originating company felt it was owed. This is an active ethical and commercial debate in the industry.

### 5.5 Open Source Sustainability: A Structural Problem

The open source ecosystem has a well-documented sustainability crisis. Critical infrastructure — libraries used by billions of devices and millions of products — is often maintained by one or two individuals working unpaid in their spare time. When that maintenance lapses (the maintainer burns out, moves on, or simply stops), vulnerabilities accumulate and systems that depend on the library become insecure.

**The Heartbleed vulnerability (2014)** in OpenSSL is the canonical case: a critical security flaw in a library securing a large fraction of the world's encrypted web traffic, maintained by a tiny volunteer team with minimal resources, that went undetected for over two years. The aftermath prompted investment in open source security infrastructure (the Linux Foundation's Core Infrastructure Initiative), but the structural problem — high-value infrastructure maintained by volunteers — has not been resolved.

**The xz Utils backdoor (2024)** is the most recent dramatic instance: a sophisticated, multi-year social engineering attack by a malicious actor (operating under the pseudonym Jia Tan) who gradually became a trusted maintainer of xz Utils, then introduced a backdoor in a late-stage release. The attack was caught before widespread deployment by accident — a Microsoft engineer noticed performance anomalies in SSH. The attack demonstrated that the trust model of open source (trust grows with contribution history) is itself an attack surface.

The ethical dimension: companies whose entire business runs on open source infrastructure and who contribute nothing back to its maintenance are free-riding on a commons they did not help build and are not helping sustain. This is a real ethical question about corporate responsibility that has no clean resolution — but it has legislative and policy responses developing in the EU (Cyber Resilience Act) that will affect how software is built and maintained for the next decade.

---

## 6. Research Labs: Where Ideas Start

### 6.1 University Research

University computer science research operates under a publish-or-perish incentive structure. Researchers are primarily evaluated on publications in prestigious venues (conferences like SOSP, OSDI, PLDI, NeurIPS, ICML; journals like JACM, CACM). The primary outputs are ideas and trained researchers, not products.

This creates specific dynamics:
- **Long time horizons.** A project that takes five years to produce a result that matters is viable in academia in a way it is not in industry.
- **Open publication.** By default, university research is public — the paper is the deliverable, and papers are read by everyone.
- **Fundamental work.** Universities are where ideas like neural networks, the internet protocols, functional programming languages, and relational databases were initially developed, often decades before industry found them commercially useful.

The ethical concerns in academic CS research include: conflicts of interest from industry funding (a research lab funded by a tech company may be structurally discouraged from publishing findings harmful to that company); the "dual-use" problem (research into AI capabilities, cryptographic attacks, or security vulnerabilities produces knowledge that can be used both defensively and offensively); and the reproducibility crisis (a significant fraction of ML research papers cannot be reproduced by independent researchers, raising questions about the reliability of the published record).

### 6.2 Industrial Research Labs

Major technology companies operate research divisions whose mandate sits between pure research and product development. The most historically significant: **Bell Labs** (produced the transistor, Unix, C, the laser, information theory — an extraordinary concentration of fundamental innovation made possible by AT&T's regulated monopoly profits funding basic research without immediate commercial pressure). **Xerox PARC** (produced the GUI, the mouse, Ethernet, Smalltalk, laser printing — almost none of which Xerox commercialized). **Microsoft Research, Google Brain/DeepMind, Meta AI, OpenAI** represent the current generation.

Industrial research operates differently from university research: shorter time horizons (typically), closer coupling to products, higher salaries, access to computational resources unavailable to universities, but also more constraints on what can be published and when.

The tension between publication and proprietary advantage is constant: a research lab that publishes its most valuable findings benefits the field (and recruits top researchers, who want to publish) but also benefits competitors. Different companies manage this tradeoff differently — Google has historically published foundational work (Transformer, MapReduce, Bigtable) that competitors then built on; OpenAI has moved progressively toward not publishing its most recent model details, despite "Open" being in its name.

### 6.3 Government and Military Research

DARPA (Defense Advanced Research Projects Agency) funded ARPANET, the precursor to the internet. NSF funds university research across computing. NIST produces cryptographic standards (including AES, SHA-3) used by the entire world. The DoD funds significant cybersecurity and AI research.

Government-funded research raises different ethical questions than private research: Who has access to results? What restrictions exist on dual-use findings? How are classified research programs evaluated if they cannot be publicly reviewed? What is the relationship between a publicly-funded university researcher and a government contract that may constrain publication?

---

## 7. How These Contexts Shape Ethical Outcomes

This is the synthesis the rest of the semester will build on. To make it concrete:

**Algorithmic bias** (Week 4) often emerges not from deliberate malice but from a sprint-based development culture where "fairness testing across demographic groups" is not in the sprint backlog because no one put it there, and nobody asks why it wasn't there.

**Privacy failures** (Week 5) often emerge from open-source dependencies that collect more data than the depending product's team knows, because the dependency's data practices were never reviewed.

**AI safety failures** (Week 6) emerge partly from research incentive structures that reward capability demonstrations and downweight safety analysis, because safety does not yet have a prestigious publication venue equivalent to NeurIPS.

**Responsible disclosure** (Week 8) emerges from the collision of researcher incentives (publish for credit) with vendor incentives (delay disclosure to avoid embarrassment and prepare a patch) with user interests (know about the vulnerability immediately).

Understanding *where* decisions are made — in a sprint planning meeting, a research lab's publication process, a company's legal review of a license, a DARPA program officer's grant decision — is the prerequisite for understanding how those decisions could be made differently.

---

## 8. Key Terms Introduced This Week

See `Glossary Week 2.md`. New terms: *waterfall model*, *Agile Manifesto*, *Scrum*, *Kanban*, *sprint*, *backlog*, *WIP limit*, *open source*, *copyleft*, *permissive license*, *Goodhart's Law*, *dual-use research*, *publish-or-perish*.
