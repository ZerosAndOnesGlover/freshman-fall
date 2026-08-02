# CS 101 · Reading Guide, Week 11
## Computability: What Cannot Be Computed

---

## The Week in One Sentence

Every week so far asked how *fast* a problem can be solved; this week asks whether it can be solved
**at all**, and proves that some precisely stated, genuinely useful problems cannot be — by any
program, in any language, on any hardware, ever.

---

## Where This Sits

| Week | Question |
|---|---|
| 6 | How fast is this algorithm? (Big-O) |
| 7–8 | How do I structure data so operations are fast? |
| 9 | What can regular expressions match — and what can't they? |
| 10 | How do I survive the messy boundary with the outside world? |
| **11** | **Which problems can be solved at all?** |

Week 9 left a promissory note. L30 said no regular expression can parse HTML, and that this was a
**theorem** rather than a limitation of Python's `re` module. This week pays it off: L34 proves the
model-level version, and then goes far past it.

---

## Primary Reading

**Sipser, *Introduction to the Theory of Computation*** is the standard text and the one to use.

| Lecture | Read before | Pages |
|---|---|---|
| L34 Models of Computation | Sipser **3.1–3.3**; skim **1.1** for finite automata | ~25 |
| L35 Decidability and the Halting Problem | Sipser **4.1–4.2** | ~15 |
| L36 Reduction and Undecidability | Sipser **5.1, 5.3**; **6.3** for Rice | ~20 |

If you read only one thing, read **Sipser 4.2**. It is four pages and contains the most important
proof in the course.

---

## How to Read This Week

The material is unlike anything else in CS 101. Three pieces of advice:

**1. The proofs are short, and shortness is the difficulty.** Turing's proof fits on half a page.
There is nowhere to hide — if you do not follow a line, you do not follow the proof. Read each
proof three times: once for the shape, once for each step, once to see why no step can be removed.

**2. Do the constructions with a pencil.** Every reduction in L36 is a five-line wrapper. Write each
one out yourself before reading the next paragraph. Reduction proofs are learned by writing, not by
reading — and this is the skill the final will test.

**3. Watch the direction.** The single most common error all week, in homework and on exams, is
reducing in the wrong direction. Before writing anything, say out loud: *"I am assuming a solver for
the NEW problem, and using it to build a solver for HALT."* If HALT is your tool rather than your
conclusion, you have it backwards.

---

## Key Terms

| Term | Meaning |
|---|---|
| **Turing machine** | Finite control + unbounded tape; formally a 7-tuple |
| **δ (transition function)** | `Q × Γ → Q × Γ × {L,R}` — the entire machine |
| **Church–Turing thesis** | Every model of effective computation coincides with TMs |
| **Universal TM** | A machine that simulates any machine given its description |
| **Decidable** | Some TM **always halts** with the correct answer |
| **Recognisable** | Accepts yes-instances; may run forever on no-instances |
| **Diagonalization** | Construct an object differing from every item in a list |
| **HALT** | `{⟨M,w⟩ : M halts on w}` — the canonical undecidable problem |
| **Reduction (A ≤ B)** | A B-solver converts into an A-solver: "A is no harder than B" |
| **Rice's theorem** | Every non-trivial **semantic** property is undecidable |
| **Sound / complete / total** | The three properties no analyser can have at once |

---

## Self-Check Questions

Answer these before Friday. If any is hard, re-read the relevant section.

1. What single feature does a Turing machine have that a finite automaton lacks, and what does that
   feature buy?
2. Why can the Church–Turing thesis not be proved? What would refute it?
3. State the difference between *decidable* and *recognisable* in one sentence, without using the
   word "sometimes".
4. In the `paradox` proof, why must `paradox` be run on **itself**?
5. What does the diagonal of the halting table represent, and what does flipping it produce?
6. Which direction is a correct reduction, and what does the wrong direction actually prove?
7. Name a question about programs that is decidable, and say what makes it so.
8. Why does `gcc -Wall` exist if perfect bug detection is impossible?

---

## Common Misconceptions

**"Undecidable means we haven't found the algorithm yet."** No. It means there is a proof that none
exists. This is the difference between an open problem and a closed one — and P vs NP (a genuinely
open problem) is a different thing entirely, which you will meet in CS 301.

**"It only applies to weird self-referential programs."** Self-reference is how the *first* result is
proved. Rice's theorem then shows essentially **every** behavioural question is undecidable, and the
counting argument in L35 §4 shows that almost all problems are, purely by cardinality.

**"A faster computer / more memory / quantum would help."** Undecidability is not about resources. A
machine with infinite speed and infinite memory still cannot decide halting. Quantum computers
compute the same class of functions; they are a **complexity** story, not a computability one.

**"So static analysis is pointless."** Exactly backwards. Undecidability tells you which *guarantee*
to drop — and every real tool drops one deliberately. Knowing which one a tool dropped is how you
know what its output means.

---

## Looking Ahead

- **CS 301 (Theory of Computation)** — the pumping lemma, context-free languages, the Chomsky
  hierarchy, and P vs NP. Everything this week gestured at, done properly.
- **CS 220 (Compilers)** — why parsers are layered as regex → grammar, which is the practical
  consequence of L34 §2.
- **Week 12** — synthesis, the final exam review, and Project 2.

---

*CS 101 · Week 11 · Reading Guide · © CSE Department*
