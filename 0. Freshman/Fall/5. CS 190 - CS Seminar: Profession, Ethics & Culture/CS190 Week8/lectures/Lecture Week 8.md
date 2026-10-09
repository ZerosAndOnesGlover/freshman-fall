# CS 190 · CS Seminar: Profession, Ethics & Culture
## Lecture · Week 8: Cybersecurity Ethics
### Responsible Disclosure, Hacktivism, and the Law That Governs Both

*“The act of breaking into a computer system has to have the same social stigma as breaking into a neighbor's house. It should not matter that the neighbor's door is unlocked.”* — Ken Thompson, "Reflections on Trusting Trust", Turing Award Lecture (1984)

**Date:** Wednesday 18 November 2026 · 13:00–13:50 · Week 8

**Reading:** *Van Buren v. United States* (2021), majority opinion · ISO/IEC 29147, overview sections · Google Project Zero, "Policy and Disclosure" — [[CS190 Week8/resources/Reading Guide|Reading Guide]]

**Coursework:** 📝 **Prep 8** due today 12:00

---

## 1. The Problem Disclosure Exists to Solve

A researcher finds a flaw in software that millions of people use. What should they do?

The question sounds easy until you notice that **every available option harms someone**.

- **Tell the vendor privately and wait.** Users stay exposed while the vendor works — and some vendors
  do not work. The flaw may already be known to attackers.
- **Publish immediately.** Users learn to protect themselves, but so do attackers, and the vendor has
  no patch ready.
- **Tell nobody.** The flaw persists indefinitely, and anyone else who finds it faces the same choice.
- **Sell it.** To the vendor, to a broker, or to a government. Each has different consequences.

**There is no option that harms no one.** This is what makes disclosure an ethics problem rather than
a procedural one, and it is why the profession has spent thirty years arguing about it without
reaching consensus.

---

## 2. The Vulnerability Lifecycle

To reason about disclosure you need the timeline.

| Stage | What is true |
|---|---|
| **Introduced** | The flaw enters the codebase, usually unnoticed |
| **Discovered** | Someone finds it — researcher, attacker, or vendor. **Nobody knows who was first.** |
| **Disclosed** | The finder tells someone |
| **Patched** | A fix exists |
| **Deployed** | The fix reaches users — often months later, sometimes never |
| **Exploited** | Attackers use it, possibly at any point after discovery |

Two features of this timeline drive everything that follows.

**First, the window between discovery and deployment is where all the risk lives**, and disclosure
policy is essentially an argument about how to manage that window.

**Second, you never know whether you were first.** A researcher who finds a flaw cannot know whether
an attacker found it a year ago. This uncertainty is the strongest argument against indefinite
silence: withholding a vulnerability protects users only if nobody else has it, and that is unknowable.

---

## 3. The Three Disclosure Models

### 3.1 Full disclosure

Publish everything immediately and publicly.

**The argument for it:** users cannot defend themselves against a threat they do not know exists.
Vendors historically ignored quiet reports; publication is the only reliable lever. Secrecy protects
the vendor's reputation, not the user.

**The argument against it:** for the period between publication and patch deployment, you have armed
every attacker and helped no one who cannot act on the information. Most users cannot patch software
themselves.

### 3.2 Coordinated (responsible) disclosure

Tell the vendor privately, agree a timeline, publish after the patch ships.

**This is the current professional norm**, codified in **ISO/IEC 29147** (vulnerability disclosure)
and **ISO/IEC 30111** (vulnerability handling), and operated in practice by CERT/CC, national CSIRTs,
and vendor security teams.

**The unresolved question is the deadline.** Google's Project Zero publishes after **90 days**
regardless of whether a patch exists, on the reasoning that an open-ended embargo gives vendors no
incentive to move. Vendors object that 90 days is arbitrary and sometimes impossible — a flaw in a
CPU or a medical device cannot be fixed on the same schedule as a web application.

> **Note the term "responsible" is contested.** Calling one model responsible implies the others are
> not, which is precisely the point at issue. Many researchers deliberately say **coordinated**
> disclosure to avoid conceding the argument in the vocabulary.

### 3.3 Non-disclosure

Tell nobody, or tell only a paying party.

**Legitimate versions exist**: a researcher may reasonably decide that publishing a flaw in
safety-critical infrastructure with no available patch endangers people. **Commercial versions also
exist**: an exploit brokerage buys vulnerabilities and sells them to governments, and the flaw stays
unpatched by design.

The ethical distinction is not whether money changes hands — bug bounties involve money too — but
**whether the transaction ends with the flaw fixed or preserved**.

---

## 4. What the Ecosystem Has Built

| Mechanism | What it does |
|---|---|
| **CVE** | A public identifier for each vulnerability, so everyone can refer to the same thing |
| **CVSS** | A severity score, imperfect but shared |
| **Bug bounties** | Vendors pay for reports, converting an adversarial relationship into a transactional one |
| **Safe-harbour policies** | A vendor's written promise not to sue researchers acting in good faith |
| **CERT/CC and national CSIRTs** | Neutral coordinators, useful when a flaw spans many vendors |

**Bug bounties changed the landscape substantially**, and mostly for the better. Before them, a
researcher's reward for a careful private report was frequently a legal threat. But they also
introduced distortions: bounty prices are far below what an exploit brokerage pays, and a programme's
scope is set by the vendor, which can exclude the findings the vendor least wants published.

**A safe-harbour policy is not a law.** It is a promise by one company, revocable, and it does not bind
prosecutors.

---

## 5. Two Cases Worth Knowing

### 5.1 Heartbleed (2014)

A flaw in OpenSSL exposed server memory — including private keys — to any client that asked. OpenSSL
underpinned a large fraction of the encrypted web and was maintained by a very small team on almost no
funding.

**What it demonstrated about disclosure:** the coordination was imperfect. Some organisations were
briefed before the public announcement and others were not, and the resulting resentment shaped
subsequent norms about who gets advance notice and on what basis.

**What it demonstrated about the profession:** critical global infrastructure was being maintained by
volunteers, and nobody had noticed until it broke. The Core Infrastructure Initiative followed
directly from it.

### 5.2 Meltdown and Spectre (2018)

Flaws in the speculative-execution behaviour of most modern processors — architectural, not a bug in
any one product, and not fully fixable in software.

**Why it is the hard case for disclosure policy:** the embargo ran for months because fixes required
coordinated changes across chip vendors, operating systems, hypervisors, and cloud providers. A 90-day
deadline would have been actively harmful. The embargo nonetheless leaked before the coordinated date,
which is what embargoes involving hundreds of people tend to do.

**The lesson:** a disclosure policy calibrated for application software does not transfer to hardware.
Reasonable rules produce unreasonable results outside the domain they were designed for.

---

## 6. The Legal Overlay

Ethics does not operate in a vacuum. In the United States the governing statute is the **Computer
Fraud and Abuse Act (CFAA, 1986)**, and its central phrase — accessing a computer "without
authorization" or in a manner that "exceeds authorized access" — was written before the web existed.

**The vagueness was the problem.** For years prosecutors and plaintiffs argued that violating a
website's terms of service constituted exceeding authorised access, which would criminalise an
enormous amount of ordinary behaviour and much legitimate research.

**Van Buren v. United States (2021)** narrowed this considerably. The Supreme Court held that
"exceeds authorized access" refers to obtaining information from areas of a system one is not entitled
to reach — not to misusing information one *is* entitled to access. The decision removed the broadest
reading, though considerable uncertainty remains about scanning, scraping, and testing systems one
does not own.

**Other relevant instruments:**

- **DMCA § 1201** prohibits circumventing access controls. Because security research often requires
  exactly that, the Copyright Office has granted a **security-research exemption** through its
  triennial rulemaking — but it is narrow, conditional, and must be periodically renewed.
- **The US Department of Justice announced a policy in 2022** of declining to prosecute good-faith
  security research under the CFAA. **A charging policy is not a statute**: it binds federal
  prosecutors, not private plaintiffs or other jurisdictions, and a later administration can revise it.
- **Other jurisdictions differ substantially.** The UK's Computer Misuse Act 1990 has no research
  exemption and has been the subject of sustained reform campaigning; several other countries treat
  possession of security tools as an offence.

> **The professional consequence:** a researcher acting entirely ethically may still be acting
> unlawfully, and the two questions must be reasoned about separately. "It was the right thing to do"
> is not a legal defence, and "it was legal" is not an ethical justification.

---

## 7. Hacktivism

**Hacktivism** is the use of computer intrusion or disruption to advance a political cause. It sits
awkwardly in professional ethics because it borrows the moral logic of civil disobedience while using
tools the profession otherwise condemns.

### The case made for it

Civil disobedience has a recognised place in political ethics: deliberately breaking a law to expose
its injustice, **accepting the penalty**, in order to force public attention. On this reading,
defacing a repressive government's website or leaking evidence of wrongdoing is a modern equivalent of
a sit-in.

### The case made against it

Three objections recur, and they are serious.

**Accountability.** Classical civil disobedience is performed openly, and the participant accepts
arrest — that acceptance is what converts law-breaking into moral testimony. Anonymous online action
takes the moral credit without the personal cost.

**Proportionality and collateral damage.** A denial-of-service attack on a government site also
disables services people depend on. A leak intended to expose one wrongdoer routinely exposes
uninvolved individuals whose data happened to be in the same database.

**Epistemic humility.** The hacktivist is judge of their own cause. Every actor believes their cause
is just, including those the profession would not want to endorse — and no mechanism distinguishes
them from the outside.

### Whistleblowing is a different question

Disclosing wrongdoing you encountered **in the course of authorised access** raises genuine ethical
questions about loyalty, harm, and public interest — but it is not the same act as breaking into a
system. Conflating them muddies both. Many jurisdictions have statutory whistleblower protections;
none protect intrusion.

---

## 8. Applying the ACM Code

Week 3's framework is directly applicable, and it does not resolve cleanly — which is the point.

| Principle | What it demands here |
|---|---|
| **1.1** Contribute to society and human well-being | Argues for disclosure — users cannot defend against unknown threats |
| **1.2** Avoid harm | Argues *both ways*: harm from unpatched flaws, harm from armed attackers |
| **1.3** Be honest and trustworthy | Argues against silently sitting on a flaw you reported nowhere |
| **2.8** Access resources only when authorised | Argues against unauthorised testing, even well-intentioned |
| **3.1** Ensure the public good is the central concern | The tie-breaker the Code intends you to reach for |

**Notice that 1.2 and 2.8 pull against each other** in exactly the cases that matter. A code of ethics
is not an algorithm. It supplies the considerations you are obliged to weigh; it does not do the
weighing.

---

## 9. What This Week Asks of You

You will spend a career finding flaws — in your own systems and in other people's. The decisions in
this lecture will be yours to make, usually under time pressure and usually with incomplete
information.

Three things worth settling in advance:

1. **Know your organisation's disclosure policy before you need it.** Reading it during an incident is
   too late.
2. **Distinguish the legal question from the ethical one**, and get advice on the first. They are
   genuinely separate, and conflating them is how well-intentioned people get prosecuted.
3. **Decide now what you would do if your employer asked you to sit on a flaw** that endangered users.
   You will reason better about it today than in the meeting.

---

*Next: Week 9 — Tech Industry Culture: Diversity, Work Culture, Mental Health*
