# CS 212 · Reading Guide · Week 10

---

## Required

| # | What | Length | Why |
|---|---|---|---|
| 1 | **Fielding (2000)**, *Architectural Styles and the Design of Network-based Software Architectures*, **Ch. 5 only** | ~30 pages | The definition of REST, by its author. **Read it so you can say what REST actually requires** and notice how little of it anyone does |
| 2 | **Richardson & Ruby, *RESTful Web Services*, Ch. 4** — or Fowler's *"Richardson Maturity Model"* (10 min) | ~25 pages / 10 min | **The maturity model.** Fowler's summary is enough if you are short of time |
| 3 | **Stripe, *"APIs as infrastructure: future-proofing Stripe with versioning"*** (stripe.com/blog) | ~15 min | **The version-transformer chain.** L33 §3's machinery, from the people who run it |
| 4 | **RFC 9457**, *Problem Details for HTTP APIs* | ~10 min, skim | The error format. **You are adopting it in A 10 Q2(c); read the members table and stop** |
| 5 | **Protobuf, *"Proto3 Language Guide"*** — the **Updating A Message Type** section only | ~5 min | **Where the field-number rule comes from**, and it is five minutes |

**About ninety minutes if you take Fowler's summary instead of Richardson & Ruby.**

---

## Recommended

| What | Why |
|---|---|
| **Hyrum Wright, *"Hyrum's Law"*** (hyrumslaw.com) | **One sentence and a stick-figure comic.** The most quoted idea in this week and the shortest reading in the course |
| **SemVer 2.0.0** (semver.org) | Ten minutes. Read it and then read L33 §6's two objections |
| **Zdenek Nemec, *"Everything You Know About Versioning Is Wrong"*** | A well-argued case that URL versioning is a mistake. **Read it to have your recommendation attacked** |
| **RFC 8594**, *The Sunset HTTP Header Field* | Two pages. The header A 10 Q4(c) asks for |
| **GraphQL, *"Best Practices"*** and the **DataLoader** README | If you are arguing *for* GraphQL in A 10 Q5, read these first — they are honest about the N+1 problem |
| **Google, *API Improvement Proposals*** (aip.dev) | A large, opinionated, well-reasoned standard. **AIP-180 (backwards compatibility) is the best short statement of L31 §2's table** |

---

## On Reading Fielding

**It is a dissertation and it reads like one.** Read **Chapter 5 only**, and read it for one purpose: **to find out which of the six constraints your API satisfies.**

Three things to notice:

1. **He never mentions JSON, and barely mentions HTTP as a requirement.** REST is a style; HTTP is one implementation of it.
2. **The constraints are justified by *properties they induce*** — scalability from statelessness, evolvability from the uniform interface. **Each one is a trade, and he says what it costs.** That is the same posture this course has taken all term.
3. **HATEOAS is not optional in his account.** It is part of the uniform-interface constraint. **So by Fielding's definition, almost nothing called REST is REST** — which is why L31 §3 recommends saying "Richardson level 2" instead.

**Fielding has been publicly and repeatedly irritated about this**, and his 2008 post *"REST APIs must be hypertext-driven"* is worth five minutes as an example of an author losing control of a term — **which is the same phenomenon as the Agile Manifesto's signatories in W0 L03 §3.** Twice in one course.

---

## A Note on This Week's Evidence

**There is essentially none**, and you should know that going in.

Almost all API design guidance is **argument from experience and from analogy**, not from measurement. There are no controlled studies showing that level 2 APIs are cheaper to maintain than level 0, or that URL versioning outperforms header versioning, or that GraphQL reduces client development time.

**What there is:**

- **Hyrum's law**, which is an observation so consistently reproduced in practice that it functions as a law even without a study.
- **Liskov substitution**, which is a **theorem** — the compatibility rules in L31 §2 follow from it formally rather than empirically.
- **Stripe's and Google's published practice**, which is evidence about what large organisations found necessary, at scale — **weaker than a study, and much stronger than a blog post.**

**So read this week's material as engineering argument and judge it by its reasoning.** The one part that is not a matter of taste is the compatibility table, because it is a theorem — and that is exactly the part A 10 marks hardest.

---

*CS 212 · Week 10 · Reading Guide*
