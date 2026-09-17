# CS 212 · Reading Guide · Week 9

---

## Required

| # | What | Length | Why |
|---|---|---|---|
| 1 | **Fowler, *Refactoring*, 2nd ed., Ch. 1** | ~40 pages | **The worked example.** He refactors a small program step by step, running the tests constantly. **Type it.** Like Beck's book in Week 5, the rhythm does not transmit by summary |
| 2 | **Fowler, *Refactoring*, Ch. 2** | ~20 pages | The definition, the two hats, when and when not. §2.7 on performance is worth reading twice |
| 3 | **Fowler, *Refactoring*, Ch. 3** — the smells | ~25 pages | All twenty-four. **Read the names and the symptoms; skip the detailed cures until you need one** |
| 4 | **Fowler, *"BranchByAbstraction"*** and **"StranglerFigApplication"** | ~15 min | Two bliki entries, and L30 is built on them |

**About two hours, most of it Chapter 1 — and Chapter 1 should be typed rather than read.**

---

## Recommended

| What | Why |
|---|---|
| **Feathers, *Working Effectively with Legacy Code*** (2004), Ch. 1–4 and Ch. 13 | *"Legacy code is code without tests."* **Ch. 13 is characterisation testing**, which is L28 §3's source, and Ch. 4's seam vocabulary is worth having |
| **Spolsky, *"Things You Should Never Do, Part I"*** (2000) | Ten minutes on why Netscape's rewrite lost the market. **L30 §5's caveat matters too** — read it critically |
| **Metz, *"The Wrong Abstraction"*** (2016) | You read it in Week 2. **Read it again now**, because it reads differently once you have refactored something you did not write |
| **Fowler, *"OpportunisticRefactoring"*** and **"PreparatoryRefactoring"** | Two short entries. *"Make the change easy, then make the easy change"* |
| **Tornhill, *Your Code as a Crime Scene*** (2015), Ch. 3–4 | Where the hotspot method comes from — change frequency × complexity. **Week 11 does this properly** |

---

## How to Read Chapter 1

**It is the best chapter in the book and people skim it, which wastes it.**

1. **Open an editor.** Type the starting program — it is short.
2. **Do each refactoring yourself before reading his version.** You will sometimes choose differently, and noticing *that* is the value.
3. **Run the tests after every single step**, as he does. **The point of the chapter is the frequency, not the destination** — he runs them dozens of times, and the fact that this feels excessive is what he is teaching.
4. **Note where he stops.** He does not make it perfect. There is a paragraph near the end about having gone far enough, and it is the chapter's actual lesson.

**If you only have forty minutes**, type the first third and read the rest. **If you have none this
week**, read §2.1–2.3 and come back to Chapter 1 before the final exam — **one of the three essay
options is reliably about refactoring.**

---

## On the 2nd Edition Being JavaScript

The 1999 first edition is Java; the 2018 second edition is JavaScript. **Neither is Python and it does
not matter.**

**What you need from the book is the catalogue and the discipline**, both of which are
language-independent. The mechanics sections occasionally do something a Python programmer would not —
`Extract Function` is fiddlier in JavaScript, and several entries work around the absence of features
Python has — **and the smells and the rhythm transfer unchanged.**

**One place the language genuinely matters**, and L29 §5 makes the point: **automated refactoring is
weaker in Python than in a statically-typed language.** A symbol-aware rename misses
`getattr(obj, name)`, a template variable, a column name in a migration, a JSON key. **Rename with the
tool, then `grep` for the old name as a string.** Every time.

---

## A Note About A 9

**A 9 is on `roomsvc`, not on `slot`**, and that is deliberate: refactoring is only hard when the code
is not yours, the author cannot be asked, and **14% of commits reference an issue** so the reasoning is
gone for the other 86%.

**Which means the reading that pays most this week is Feathers Ch. 13**, not Fowler's catalogue. The
catalogue tells you what to do once you can safely do it. **Feathers tells you how to get to the point
where you can** — and for `confirm_booking`, with eleven tests against ninety-four paths, that is the
binding constraint.

---

*CS 212 · Week 9 · Reading Guide*
