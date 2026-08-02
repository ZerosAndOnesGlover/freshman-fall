# CS 101 · Lecture 37 (Week 12, Lecture 1)
## Synthesis: The Whole Stack

---

## 0. What You Actually Learned

Twelve weeks ago you wrote `print("Hello, world")` and were told the machine underneath was a
device that manipulates bits according to stored instructions.

Since then you have written sorting algorithms, analysed their growth, built hash tables, parsed
text with regular expressions, survived corrupt files, and proved that certain programs cannot
exist. It can feel like eleven unrelated topics.

It is not. It is **one idea applied eleven times**, and today's lecture is about seeing that.

---

## 1. The Idea

> **Every week of this course built a layer that hides the layer below it, and every week showed
> you where that layer leaks.**

That is the whole of computer science in one sentence. A layer of abstraction gives you a simpler
model to think in. It also lies to you in specific, learnable ways, and knowing exactly where it
lies is the difference between using a tool and understanding it.

Here is the course as a stack:

| Week | The abstraction you were given | Where it leaks |
|---|---|---|
| 1 | Numbers and text are just values | `0.1 + 0.2 != 0.3`; floats are not reals |
| 2 | Control flow is a straight story | Off-by-one, unreachable branches, short-circuit evaluation |
| 3 | Functions are independent black boxes | Shared mutable defaults; the call stack is finite |
| 4 | Recursion is self-reference that just works | Stack depth is bounded; naive recursion recomputes |
| 5 | Sorting is a thing you call | Which sort matters; stability matters; input shape matters |
| 6 | Performance is "how long it took" | Constants hide asymptotics; asymptotics hide constants |
| 7 | A list holds your data | `insert(0, x)` is Θ(n); contiguity has a price |
| 8 | Lookup is instant | Only with a good hash and a sane load factor |
| 9 | A string is a sequence of characters | Code points vs bytes vs graphemes; regex cannot count |
| 10 | Files hold your data reliably | Truncation at open, partial writes, encoding, crashes |
| 11 | Programs solve problems | Some problems have no program |

**Read the right-hand column top to bottom.** That is what you actually know now, and it is what
distinguishes you from someone who has merely learned Python syntax.

---

## 2. Four Threads That Ran Through Everything

### Thread 1: Representation determines cost

You met this in Week 1 with floats and it never went away.

- A **list** is contiguous, so indexing is Θ(1) and front-insertion is Θ(n) (W7)
- A **hash table** trades space and ordering for Θ(1) average lookup (W8)
- A **string** is immutable, so `s += c` in a loop is Θ(n²) (W9)
- A **Turing machine's tape** is unbounded, which is exactly why it can count and a finite automaton
  cannot (W11)

The recurring question — *what does this structure make cheap, and what does it make expensive?* —
is the single most transferable question in the course.

### Thread 2: The boundary is where things break

Inside your program, values behave. At every boundary, they do not.

- **Week 1** — the boundary between real numbers and their float representation
- **Week 9** — the boundary between text and bytes
- **Week 10** — the boundary between your process and the filesystem
- **Week 10** — the boundary between your assumptions and the actual data

`atomic_write` is the purest example: four separate requirements, each defending against a different
way the boundary betrays you (wrong directory, unflushed buffer, Windows semantics, Ctrl-C).

### Thread 3: Measure, don't assume

You were wrong about performance at least once this term, and the measurement told you.

- The `s += c` benchmark that looked linear because CPython resizes in place when the refcount is 1
- The hash table that had a fine load factor and terrible distribution
- Bubble sort that beat merge sort on n = 10

Big-O is a statement about **growth**, not about your input. Both facts matter and neither replaces
the other.

### Thread 4: Some limits are absolute

Weeks 1–10 taught you to make things faster. Week 11 taught you that some things are not slow —
they are impossible, and no amount of engineering changes that.

Knowing which is which is the most senior skill in the list.

---

## 3. Worked Synthesis: One Problem, Every Week

To see the threads together, take one concrete task and walk down the stack.

> **"Find the 10 most frequent words in a 2 GB log file."**

**Week 10 — the boundary.** You cannot `read()` 2 GB into memory comfortably, and the file may have
encoding errors. Stream it line by line, specify the encoding explicitly, decide your policy for
malformed lines before you meet one.

```python
with open(path, encoding="utf-8", errors="replace") as f:
    for line in f: ...
```

**Week 9 — text.** "Word" needs defining. Case folding, punctuation, Unicode normalisation. A regex
handles tokenising (`\w+`) but cannot handle nesting — and you do not need nesting here, which is
exactly the judgement L30 asked for.

**Week 8 — counting.** A dict gives Θ(1) average increment. Doing this with a list of
`(word, count)` pairs and a linear scan would be Θ(n·k) and is the classic beginner mistake.

**Week 6 — the analysis.** Counting is Θ(n) in the number of words. Sorting all k distinct words to
find the top 10 is Θ(k log k).

**Week 7 — the better structure.** You do not need a full sort. A **heap** of size 10 gives
Θ(k log 10) = Θ(k). For k = 500,000 distinct words that is a real difference, and it is the same
"what does this structure make cheap" question as always.

**Week 3 — structure.** Three functions — tokenise, count, top-k — each testable alone. Not one
80-line block.

**Week 11 — the limit.** "Is my tokeniser correct for all inputs?" is not decidable in general. You
test, you assert, you handle the boundary. You do not prove.

One task. Seven weeks of the course, all load-bearing.

---

## 4. What "Knowing How to Program" Actually Means

At the start of term, the plausible answer was "knowing the syntax." You now have a better one.

**1. You can choose a representation.** Given a problem, you can ask what operations dominate and
pick a structure that makes those cheap. This is most of practical performance work.

**2. You can predict, then measure, then reconcile.** When the measurement disagrees with the
prediction, you now treat that as information rather than noise — the disagreement is where the real
learning is.

**3. You defend the boundary.** You do not trust input, files, encodings, or the assumption that the
last write completed.

**4. You know the difference between hard and impossible.** And you can say precisely why.

**5. You can read a program you did not write.** Which is what almost all professional programming
actually is, and what L39 will spend its time on.

---

## 5. The Honest Inventory

Things this course gave you a **real** foundation in:

- Imperative and recursive problem decomposition
- Complexity analysis and its correct application
- The core data structures and their trade-offs
- Text processing and the encoding boundary
- Defensive I/O and error handling
- The computability boundary

Things you have only **touched**:

- Object-oriented design (used, never studied — CS 102)
- Testing as a discipline (practised, not systematised — CS 210)
- Memory management (met in PROG 101's C, not internalised)
- Concurrency (deliberately avoided — see L38)

Things you have **not** met at all, and should know you have not: networks, databases, operating
systems, compilers, machine learning, security, distributed systems, and human factors. L38 maps
these.

**This inventory is the point.** A course that left you feeling finished would have failed. Knowing
the shape of what you do not know is what lets you learn it deliberately.

---

## 6. Summary

| Idea | Takeaway |
|---|---|
| The course is one idea | Build a layer; find where it leaks |
| Thread 1 | Representation determines cost |
| Thread 2 | Boundaries are where correctness dies |
| Thread 3 | Measure; reconcile with prediction |
| Thread 4 | Some limits are absolute, not engineering problems |
| Synthesis | One realistic task uses seven weeks at once |
| Knowing how to program | Choose representations, defend boundaries, know the limits |
| The inventory | Knowing the shape of your ignorance is the deliverable |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** For each abstraction, name the specific leak from the table in §1, and give one line
of code that exposes it: (a) floats are numbers, (b) a list holds your data, (c) lookup is instant.

**2. (Explain.)** Take the word-frequency problem in §3 and change one requirement: the file is now
50 KB, not 2 GB. State which of the seven decisions change and which do not, and why.

**3. (Build.)** Pick any program you wrote this term. Identify one place where you chose a
representation, and write two sentences on what that choice made cheap and what it made expensive.

**4. (Stretch.)** §4 claims "you can read a program you did not write" is most of professional
programming. If that is true, name three things this course did that build that skill, and one
thing it did not do that would have.

### Answers

**1.**

| | Leak | Exposing line |
|---|---|---|
| **(a)** floats | Finite binary representation; decimals like 0.1 are not exact | `0.1 + 0.2 == 0.3` → `False` |
| **(b)** list | Contiguous storage makes front operations Θ(n) | `lst.insert(0, x)` in a loop — Θ(n²) total |
| **(c)** lookup | Θ(1) is *average*, and assumes a well-distributed hash | A class with `__eq__` but no `__hash__`, or all keys colliding into one bucket |

*Also acceptable for (a):* non-associativity — `(a+b)+c != a+(b+c)` for suitable floats.

**2.** At 50 KB the file fits in memory comfortably, so:

**Changes:**
- **Streaming is no longer necessary.** `f.read()` is fine, and simpler code is better code when
  the constraint is gone.
- **The heap is no longer worth it.** With few distinct words, `sorted(counts.items())[:10]` is
  clearer and the Θ(k log k) vs Θ(k) difference is invisible. Choosing the heap here would be
  optimising a cost you cannot measure.

**Does not change:**
- **The encoding decision.** A 50 KB file can be just as malformed as a 2 GB one. Size has no
  bearing on whether bytes decode.
- **Defining "word".** Tokenising is a correctness question, not a performance one.
- **Using a dict to count.** It is both faster *and* clearer than the list-of-pairs alternative —
  there is no trade-off to make.
- **Decomposition into functions.** Testability does not depend on input size.
- **The undecidability limit.** Still cannot prove the tokeniser correct.

**The lesson:** scale changed the *performance* decisions and left every *correctness* decision
untouched. Students who change the encoding handling because the file got smaller have the two
categories confused.

**3.** Open. Look for a genuine trade-off with both halves named. Strong answers sound like: *"I
used a dict keyed by student ID, which made lookup Θ(1) instead of scanning the list. It made
'find the student with the highest score' worse, because I lost ordering and now have to scan all
values anyway — a sorted structure or a heap would have served both."*

Weak answers name only the benefit. The exercise is specifically about the cost.

**4.** **Three things that built it:**

- **Starter files with test suites.** Every lab and problem set handed you a codebase with a
  contract you had to read before writing — which is exactly the professional situation.
- **Reading the standard library's behaviour rather than guessing.** The encoding, `re`, and file-mode
  material forced you to consult documented semantics.
- **The instrumented-algorithm work** (and Project 2): taking an algorithm you did not write,
  understanding it well enough to observe it, and confirming it matches a predicted cost.

**One thing it did not do:** you never read a **large, unfamiliar, imperfect codebase** — one with
history, inconsistent style, dead code, and decisions whose reasons are not written down. Every
codebase you touched was clean and purpose-built for the lesson. That is the single biggest gap
between this course and the first week of a real job, and it is why L39 spends its time there.

*Also accept:* no code review, no version control history to read, no debugging someone else's bug
report.

---

## Reading

- Re-read your own **Week 6 Big-O notes** alongside your **Week 11 undecidability notes**. The
  contrast between "expensive" and "impossible" is the course's central distinction.
- **Brooks, "No Silver Bullet"** (1986) — on essential vs accidental complexity; short, and the best
  companion to §1
- **Petzold, *Code*** — optional; the bottom of the stack, told well

---

*CS 101 · Week 12 · Lecture 37 (Tue) · © CSE Department*
