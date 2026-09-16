# CS 212 · Reading Guide · Week 5

---

## Required — and one of them is a whole book

| # | What | Length | Why |
|---|---|---|---|
| 1 | **Beck, *Test-Driven Development by Example*, Part I** | ~100 small pages | **Read it in one sitting, this week.** Type the money example as you go. The rhythm does not transmit by summary and this is the only assigned reading in the course that must be *done* rather than read |
| 2 | **Fowler, *"Mocks Aren't Stubs"*** (2007, martinfowler.com) | ~25 min | The five doubles, and the state-versus-interaction distinction that L18 §1 turns on |
| 3 | **Sommerville Ch. 8 §8.1–8.3** | ~20 pages | The conventional account: levels, test cases, regression |

**Beck is the priority.** If you read one thing this week, read it — and read it with a terminal open.

---

## Recommended

| What | Why |
|---|---|
| **Fowler, *"TestPyramid"*** and **Dodds, *"The Testing Trophy"*** | Ten minutes together. Read them as two positions on **where your complexity lives**, which is L16 §3's framing |
| **Feathers, *Working Effectively with Legacy Code*, Ch. 1–2** | *"Legacy code is code without tests."* The seam vocabulary, which Week 9 uses |
| **Meszaros, *xUnit Test Patterns*** — Test Double chapter, and Obscure Test | Where the five names come from; and the best catalogue of test smells anywhere |
| **Fucci et al., *"An External Replication on the Effects of Test-Driven Development"*** (ESEM 2016) | The study L17 §3 leans on. **Read it if you intend to argue with the lecture** — and A 5 has no question requiring agreement |

---

## Do Not Bother This Week

**BDD tooling documentation** — Cucumber, `behave`, `pytest-bdd`. L18 §3 recommends the phrasing and not the tooling, and reading the tooling docs will make it tempting. **If you want to argue for it, read them and argue in the paper; otherwise skip.**

**Any "100% coverage" blog post.** Week 6 handles coverage properly and several of the common claims are wrong in ways that are easier to unlearn if you have not learned them.

---

## On Reading Beck

*TDD by Example* is a strange book to read and people bounce off it. Three things that help:

1. **It is a transcript, not an argument.** Beck writes what he types, including the wrong turns. **The wrong turns are the content** — they show what a small step looks like when you are unsure.
2. **Part I's money example gets tedious around chapter 8.** Push through. The tedium *is* the demonstration: he is showing that the steps stay small even when the problem gets less interesting, which is exactly where people abandon the discipline.
3. **Type it.** Reading TDD is like reading about swimming. The book is short specifically so that typing it is feasible in an evening.

**Part II (the xUnit framework, test-driven in Python) is optional and is the best part of the book** if you have the time — he builds a testing framework using the framework he is building, which is a genuinely good piece of writing.

---

## A Note on the Evidence, Before You Read the Advocacy

L17 §3 rates the evidence for test-first as weak and mixed, and the strongest replication attributes the benefit to **small uniform steps**, not to ordering. **Beck's book does not claim otherwise** — it is a description of a practice, not a study — but much of the secondary literature does.

**Read Beck for the practice. Do not read the secondary literature for the evidence.** If you want the evidence, read Fucci and Santos, and notice how much smaller the claims are than the blog posts.

---

*CS 212 · Week 5 · Reading Guide*
