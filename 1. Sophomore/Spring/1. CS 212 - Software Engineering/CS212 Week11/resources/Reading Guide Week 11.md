# CS 212 · Reading Guide · Week 11

---

## Required

| # | What | Length | Why |
|---|---|---|---|
| 1 | **Cunningham, *"The WyCash Portfolio Management System"*** (OOPSLA 1992) | **2 pages** | **The original debt metaphor**, and nothing like what the phrase now means. Two pages, and reading them will change how you use the word |
| 2 | **Fowler, *"TechnicalDebtQuadrant"*** (2009) | 5 min | The two axes. A 11 Q2 requires you to place every register item in one |
| 3 | **Tornhill, *Your Code as a Crime Scene*, Ch. 3–4** | ~35 pages | Where hotspot analysis and change coupling come from. **Ch. 4 on change coupling is the part nobody else teaches** |
| 4 | **Procida, *Diátaxis*** (diataxis.fr) | ~20 min | The four kinds of documentation and their different half-lives. **The site is itself an example of what it describes** |

**About ninety minutes.** Read Cunningham first; it is two pages and it reframes the rest.

---

## Recommended

| What | Why |
|---|---|
| **Cunningham's 2009 video interview on the debt metaphor** (~5 min, on YouTube as *"Ward Explains Debt Metaphor"*) | **He says, in his own words, that he never meant "bad code".** Worth five minutes before you use the phrase again |
| **Inozemtseva & Holmes (2014)** — re-read the methodology | You read it in Week 6. **Read it again as a case study in Goodhart's law**, which is what it is |
| **Tornhill, *Software Design X-Rays*** (2018), Ch. 2 and 9 | The same method at organisational scale; **Ch. 9 on knowledge distribution is where the bus-factor analysis comes from** |
| **Google, *"Software Engineering at Google"*** (2020), Ch. 1–3 | The best available writing on engineering *at scale over time*. **Ch. 1's "Hyrum's law" and "shifting left" are both course material** |
| **Nygard on ADRs** — re-read (W3) | Two pages, and it reads differently now that you have superseded one |
| **Ousterhout, *A Philosophy of Software Design*** (2018), Ch. 12–13 | On comments, and it is the best-argued case against *Clean Code*'s position — which is the one this course takes (syllabus §7.2) |

---

## Read Cunningham First, and Notice Three Things

**Two pages, and the phrase you think you know is not in them.**

1. **The debt is taken on *deliberately*, to ship sooner.** It is a financing decision — *"a little debt speeds development"* — not an accident and not a synonym for bad code.
2. **The thing owed is *understanding*.** Cunningham's later clarification is explicit: the debt is that the code **does not yet reflect what you now know about the domain.** Repaying it means bringing the code into line with your current understanding — which is **W9's comprehension refactoring**, not a cleanup sprint.
3. **The interest is continuous and is the thing that matters** — *"every minute spent on not-quite-right code counts as interest."* Which is why L34 §3 says the principal is nearly irrelevant.

**Then notice what the phrase has become**, and that the drift matters: calling mess "debt" is **how mess gets excused**, because debt sounds like a decision somebody made on purpose.

**This is the third time this term** that a term's originator has publicly disowned what it became — **the Agile Manifesto's signatories** (W0 L03 §3), **Fielding on REST** (W10's reading guide), and now Cunningham. **That pattern is worth noticing on its own**, because it tells you something about how this field transmits ideas: the memorable name travels and the caveats do not.

---

## On Tornhill, and Why Chapter 4 Is the Valuable One

Hotspot analysis — change frequency × complexity — is now reasonably well known, and you could get it from L35 §3 alone.

**Change coupling is not**, and it is the chapter worth reading properly. **It finds coupling that exists in no import graph**: two files that change together in 112 of 891 commits while neither references the other. That coupling is real, it is in the *domain*, and **no static analyser, type checker or architecture test can see it** — only the history can.

**Which makes it the empirical version of W2 L07 §7's rule** — *couple what changes together, decouple what changes apart.* Week 2 gave you the rule and told you the evidence was in the `git log`. **This is how you actually read it**, and A 11 Q1(b) asks you to.

---

## A Note on What This Week Is Evidence For

**Mixed, and worth separating:**

| Claim | Evidence |
|---|---|
| Goodhart's law applies to software metrics | **Strong**, in the sense that every instance is well documented — coverage (Inozemtseva & Holmes), velocity, deployment frequency |
| Hotspots predict where defects and effort concentrate | **Moderate.** Tornhill's case studies are real and numerous; they are not controlled studies |
| Cyclomatic complexity predicts defects | **Weak**, and largely explained by size — the same confound as coverage's |
| The maintainability index means anything | **Essentially none.** A 1991 formula with arbitrary weights, fitted to C |
| Documentation close to the code survives longer | **No studies. A structural argument** — code is executed and cannot silently become false; prose is not and does |

**The last row is worth dwelling on**, because it is the shape of most of this week: **an argument from mechanism rather than from measurement.** That is weaker than a study and it is not worthless — a mechanism you can state and check is better than a correlation you cannot explain. **But say which kind of claim you are making**, and A 11 Q4(c) asks you to do exactly that about the maintainability index.

---

*CS 212 · Week 11 · Reading Guide*
