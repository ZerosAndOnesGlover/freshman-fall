# CS 212 · Reading Guide · Week 1

---

## Required

| # | What | Length | Why |
|---|---|---|---|
| 1 | **Sommerville Ch. 4 §4.1–4.3**, "Requirements Engineering" | ~20 pages | The careful account. Its distinction between user and system requirements is worth having, and its elicitation section is better than most |
| 2 | **Cohn, *User Stories Applied*, Ch. 1–2** | ~25 pages | If the library copy is out, Jeffries' original *"Essential XP: Card, Conversation, Confirmation"* (2001) is two pages and carries the same idea |
| 3 | **Evans, *Domain-Driven Design*, Ch. 2** — "Communication and the Use of Language" | ~15 pages | On ubiquitous language. **The best fifteen pages on why naming is an engineering problem rather than a taste problem** |

**About ninety minutes.** Chapter 2 of Evans is the one to read carefully; the rest can be skimmed for structure.

---

## Recommended

| What | Why |
|---|---|
| **Cockburn, *"Walking Skeleton"*** (alistair.cockburn.us, ~1 page) | The original definition, and shorter than this reading guide |
| **Wake, *"INVEST in Good Stories, and SMART Tasks"*** (2003) | Two pages; the source of the acronym |
| **Cockburn, *Writing Effective Use Cases*, Ch. 1–2** | If you found L06 §1 useful, this is where the format comes from. Skip the rest of the book |
| **Fowler, *"AnemicDomainModel"*** (2003, bliki) | Two pages, and it will make more sense after Week 2 — but read it now so it is in your head when you write `service.py` |

---

## A Warning About *Domain-Driven Design*

Evans' book is 560 pages and is **the most over-applied book on this course's shelf.** Its strategic patterns — bounded contexts, context maps, aggregates — are designed for systems with dozens of developers and multiple teams. **`slot` has five people and one context.** Applying the full apparatus to it produces ceremony, not clarity.

**Read Chapter 2 for the ubiquitous language, and stop.** Come back to the aggregates in Week 3 if your model has grown enough to need them, and to the strategic chapters in Year 3.

---

## On Reading Code, Which A 1 Requires

A 1 Q1(b) asks you to find undocumented invariants in `roomsvc` by reading `models.py` and `bookings.py`. You have not been taught to read a codebase cold. **A method:**

1. **Do not start at the top of the biggest file.** Start at `models.py` — the data tells you what the concepts are, in about ten minutes.
2. **Then read the tests**, not the code. `tests/` tells you what the previous authors believed mattered, and — since coverage is 47% on `bookings.py` — the gaps tell you what they did not.
3. **Then `grep` for the vocabulary.** L06 §2's `grep` is the one to start with. Where a concept has several names, the seams between them are where bugs live.
4. **Only then open `bookings.py`**, and open it at `confirm_booking` (line 291), not at line 1.
5. **Use `git log -S'<string>'`** to find when a line appeared and what its commit message said. On the 14% of commits that reference an issue, this gets you the reason.

**Expect this to take two hours and to be frustrating.** That frustration is the actual subject of this course, and it is the same frustration that turned a fourteen-line fix into four months.

---

*CS 212 · Week 1 · Reading Guide*
