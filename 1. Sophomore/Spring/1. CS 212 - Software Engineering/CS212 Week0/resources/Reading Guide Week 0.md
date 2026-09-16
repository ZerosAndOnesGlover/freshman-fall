# CS 212 · Reading Guide · Week 0

---

**The point of this file** is that the four course books cover Week 0's material with wildly
different value, and two of them should not be opened yet. Read the primary sources instead: they
are shorter than the textbook chapters and this week's material is *about* them.

---

## Read This Week, In This Order

| # | What | Length | Why |
|---|---|---|---|
| 1 | **The Agile Manifesto**, agilemanifesto.org — **both pages** | **4 minutes** | You will be arguing about it on Tuesday. The twelve principles on page two are where the content is, and almost nobody reads them |
| 2 | **Royce (1970)**, *"Managing the Development of Large Software Systems"* | 11 pages | **A 0 Q1 requires it.** Read to the end of page 2 before L02 — that is where the sentence is |
| 3 | **Sommerville Ch. 1**, "Introduction" | ~25 pages | The even-handed textbook account of what the discipline claims to be. §1.1–1.3 |
| 4 | **Sommerville Ch. 2**, "Software Processes" | ~30 pages | Process models, done fairly. **§2.1 and §2.3 only**; skip the rest for now |

**That is the required reading and it is about ninety minutes.** Everything below is optional and at least one item is more valuable than items 3 and 4.

---

## Strongly Recommended, One Evening

| What | Why |
|---|---|
| **Leveson & Turner (1993)**, *"An Investigation of the Therac-25 Accidents"*, IEEE Computer 26(7) | **The best-written failure analysis in the field.** Long, and worth every page. If you read one optional thing this term, this |
| **Lions (1996)**, *Ariane 5 Flight 501 Inquiry Board report* | Nine pages, and the clearest example anywhere of correct code failing because its assumptions moved |
| **Fowler (2018)**, *"The State of Agile Software in 2018"* | Twenty minutes, by a signatory, on what went wrong with the word |
| **Dijkstra (1972)**, *"The Humble Programmer"* | Dated in its particulars, undated in its argument |

---

## Do *Not* Read Yet

| Book | Why not yet | When |
|---|---|---|
| **Fowler, *Refactoring*** | Its value is entirely in applying it to code you already find confusing. Reading the catalogue cold is memorising a list | **Week 9.** Skim the smell names in Week 2 if you like |
| **Beck, *TDD by Example*** | It is a rhythm, not a theory. Read it in one sitting **while doing it**, or it teaches nothing | **Week 5.** One sitting. Type the examples |
| **Martin, *Clean Code*** | Most contested book on the list. **Read it after Weeks 2 and 9**, when you have your own opinions to test it against | **Week 9**, and see the syllabus §7 for where this course disagrees |

---

## On Reading Sommerville

It is comprehensive, fair, and published in 2015. **That last fact matters more in this course than in most.** Its chapters on requirements, process and architecture are as good as anything written. Its treatment of continuous integration, containers and modern deployment describes a world that has moved: Week 8 does almost nothing the book anticipates.

**Use it as: the careful account of the parts that have not changed** — requirements engineering, process models, the sociology of projects — and use the lectures and the free sources for the parts that have.

---

## A Note on How to Read Primary Sources

You will read four this term, starting with Royce. A method that is worth the twenty minutes:

1. **Read the abstract and the conclusion first.** Then decide whether you need the middle.
2. **Find the sentence the paper is known for, and read the paragraph around it.** This is where Royce's reputation comes apart, and it is not the only paper in this field where that is true.
3. **Note what the paper does *not* claim.** Most misuse of research in software engineering is a claim about a broader population than the one studied.
4. **Note the date and ask what was expensive then.** Royce was writing when compiling took hours and a test run took a day. Boehm's 100× curve is partly a fact about 1981's feedback loops (L02 §3).

**A 0 Q4 asks you to do (3) and (4) deliberately.**

---

*CS 212 · Week 0 · Reading Guide*
