# CS 101 · Lecture 34 (Week 11, Lecture 1)
## Models of Computation: What a Computer Fundamentally Is

---

## 0. A Question the Course Has Been Avoiding

For ten weeks you have asked *how fast* algorithms are. Big-O, recurrences, hash tables,
benchmarks — all of it assumes the problem **can** be solved and asks what it costs.

This week asks the prior question: **which problems can be solved by any program at all?**

That is not a question about Python, or about how much memory you have, or about waiting longer.
There are precisely specified problems that **no program can ever solve**, on any hardware, given
unlimited time. Proving that requires being exact about what "a program" means — which is what
today's lecture builds.

You have already met a small version of this. L30 claimed that no regular expression can parse
HTML, and that this was a **theorem** rather than a limitation of Python's engine. Today we make
that kind of claim precise; Thursday proves a much stronger one.

---

## 1. Why We Need a Model

"No program can do X" is a claim about **every possible program**. You cannot check them one by
one — there are infinitely many. You need a mathematical object that captures *exactly* what
programs can do, so that a proof about the object is a proof about all programs.

The requirements are contradictory-sounding:

- **Simple enough to reason about.** Python has hundreds of features; a proof would drown.
- **Powerful enough to be honest.** If the model is weaker than real computers, "the model can't
  do X" proves nothing about Python.

Alan Turing's 1936 answer satisfies both, and it is startlingly minimal.

---

## 2. Warm-Up: Finite Automata and Their Ceiling

Start with something *too* weak, to see what "too weak" looks like.

A **finite automaton** has a fixed set of states and reads its input once, left to right, with no
memory beyond the current state. That is exactly the power of a regular expression.

Here is one that accepts strings with an even number of `1`s:

| State | read `0` | read `1` | at end |
|---|---|---|---|
| `even` (start) | `even` | `odd` | **accept** |
| `odd` | `odd` | `even` | reject |

Verified on a simulator: `""` accept, `"0"` accept, `"11"` accept, `"1"` reject, `"101"` accept,
`"1111"` accept, `"10101"` reject — matching parity in every case.

### What it cannot do

Consider the language **aⁿbⁿ** — some number of `a`s followed by *the same number* of `b`s:
`ab`, `aabb`, `aaabbb`, …

**No finite automaton can recognise it.** The intuition is a counting argument: to check the `b`s
match, the machine must remember how many `a`s it saw. With `k` states it can distinguish at most
`k` different counts, so feed it `a` repeated `k+1` times and two different prefixes must land in
the same state. From that state the machine cannot tell them apart, so it accepts a string it
should reject. (The formal version is the **pumping lemma**, proved in CS 301.)

**This is precisely L30's claim, now stated properly.** Regular expressions describe regular
languages; matched nesting requires unbounded counting; therefore no regex parses HTML. The
failure was never about backtracking or engine quality — it is a limit on the *model*.

So finite memory is the ceiling. Lift it and see what happens.

---

## 3. The Turing Machine

Turing's model adds exactly one thing: an **unbounded tape** the machine can read, write, and move
along.

**Definition.** A Turing machine is a 7-tuple (Q, Σ, Γ, δ, q₀, q_accept, q_reject) where

- **Q** — a finite set of states
- **Σ** — the input alphabet (blank not included)
- **Γ** — the tape alphabet, Σ ⊆ Γ, including a blank symbol `_`
- **δ: Q × Γ → Q × Γ × {L, R}** — the **transition function**
- **q₀ ∈ Q** — the start state
- **q_accept, q_reject ∈ Q** — halting states

The whole machine is that transition function. It says: *in state q reading symbol s, write symbol
s′, move left or right, and enter state q′.* Nothing else.

The tape is infinite in one direction, initially holding the input followed by blanks. The head
starts at the leftmost cell. The machine runs until it reaches `q_accept` or `q_reject` — or
**forever**, which will matter enormously on Thursday.

### A first machine: unary increment

Represent the number *n* as *n* copies of `1`. To add one, walk right to the first blank and write
a `1`:

| State | Read | Write | Move | Next |
|---|---|---|---|---|
| `q0` | `1` | `1` | R | `q0` |
| `q0` | `_` | `1` | — | **accept** |

Verified: `""` → `"1"`, `"1"` → `"11"`, `"111"` → `"1111"`, `"11111"` → `"111111"` — each in
n+1 steps. Two lines of transition table implement addition.

### The machine that breaks the finite-automaton ceiling

Here is a Turing machine for **aⁿbⁿ**, the language no finite automaton can recognise. The strategy
is to cross off one `a` and one `b` repeatedly:

| State | Read | Write | Move | Next | Meaning |
|---|---|---|---|---|---|
| `q0` | `a` | `X` | R | `q1` | cross off an `a`, go find a `b` |
| `q0` | `Y` | `Y` | R | `q3` | no `a`s left — check nothing but `Y`s remain |
| `q0` | `_` | `_` | — | **accept** | empty input |
| `q1` | `a` | `a` | R | `q1` | skip remaining `a`s |
| `q1` | `Y` | `Y` | R | `q1` | skip crossed-off `b`s |
| `q1` | `b` | `Y` | L | `q2` | cross off a `b`, go back |
| `q2` | `a`, `Y` | same | L | `q2` | walk back left |
| `q2` | `X` | `X` | R | `q0` | found the crossed-off `a`; repeat |
| `q3` | `Y` | `Y` | R | `q3` | skip `Y`s |
| `q3` | `_` | `_` | — | **accept** | all matched |

Verified:

| Input | Result | Steps |
|---|---|---|
| `""` | accept | 1 |
| `"ab"` | accept | 5 |
| `"aabb"` | accept | 13 |
| `"aaabbb"` | accept | 25 |
| `"aab"` | halt (reject) | 7 |
| `"abb"` | halt (reject) | 4 |
| `"aabbb"` | halt (reject) | 12 |

**The tape is doing the counting** that finite memory could not. That single addition — unbounded
storage the machine can revisit — is the entire difference between "cannot count" and "can compute
anything computable".

> **On rejection.** A machine rejects by halting in a non-accepting state. In the table above,
> most rejections happen because δ has no entry for the current (state, symbol) pair — the machine
> gets *stuck*, which is a halt. A fully specified machine would route these to `q_reject`
> explicitly; the shorthand is standard and harmless.

---

## 4. The Church–Turing Thesis

The Turing machine looks absurdly primitive. Yet:

- **λ-calculus** (Church, 1936) — functions and substitution, no machine at all
- **General recursive functions** (Gödel, Herbrand)
- **Register machines**, **cellular automata**, **your laptop**, **Python**

All of these compute **exactly the same set of functions**. Every attempt to define "effectively
computable" has landed on the same class, and each equivalence is a proved theorem, not a
coincidence.

> **Church–Turing thesis.** Any function that can be computed by *any* effective procedure can be
> computed by a Turing machine.

This is **not a theorem** — "effective procedure" is an informal notion, so it cannot be proved. It
is a claim about the adequacy of a definition, and ninety years of failed attempts to exceed it are
the evidence.

**The consequence is what makes this week possible.** Prove that no Turing machine can solve a
problem, and you have proved that **no program in any language on any hardware** can solve it —
past, present, or future. That is the leverage the model buys.

Note what the thesis does *not* say. It says nothing about **speed** — a Turing machine simulating
your laptop is astronomically slower. Computability and complexity are different questions, and
Week 6 answered the second for problems that are computable at all.

---

## 5. Universality: The Machine That Runs Machines

Turing's second insight is the one that built the industry.

A Turing machine can be written down as a finite string — its transition table is just data. So a
machine can be given **another machine's description** as input.

> **The Universal Turing Machine** U takes ⟨M, w⟩ — an encoded machine M and an input w — and
> simulates M running on w.

U does whatever M would do. One fixed machine, capable of any computation, selected by its input.

**That is a stored-program computer.** Before Turing, "computers" were built for a task and rewired
to change it. Universality says you do not need a machine per problem; you need **one** machine and
a description of the problem. Your laptop is a universal machine; an app is the description.

It is also why L01's von Neumann architecture stores instructions and data in the same memory —
because Turing proved that instructions *are* data. And it sets up Thursday: since a machine can
take a machine as input, it can be given **itself**.

---

## 6. Summary

| Idea | Takeaway |
|---|---|
| Impossibility needs a model | "No program can" is a claim about infinitely many programs |
| Finite automata = regular expressions | Fixed memory; cannot recognise `aⁿbⁿ` |
| That is L30's regex boundary, formalised | Matched nesting needs unbounded counting |
| A Turing machine = finite control + unbounded tape | One addition, total change in power |
| δ: Q × Γ → Q × Γ × {L,R} | The entire machine is this function |
| Church–Turing thesis | Every model of effective computation coincides |
| Therefore | "No TM can" ⟹ "no program in any language ever can" |
| Universality | A machine can simulate any machine: the stored-program computer |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Using the unary-increment table from §3, trace the machine on input `"11"`. Give the
tape and head position after each step, and the total step count. Then state the step count for
input of length n.

**2. (Explain.)** Why can no finite automaton recognise `aⁿbⁿ`? Give the counting argument, and
state what the Turing machine has that makes it possible.

**3. (Build.)** Give the transition table for a Turing machine over `{0,1}` that accepts exactly
those strings ending in `0`. State your states and say what each one *means*.

**4. (Stretch.)** The Church–Turing thesis cannot be proved. Explain why not, state what would
refute it, and explain why "quantum computers are faster" is not a refutation.

### Answers

**1.** With head position marked `^`:

| Step | Tape | Head | State | Action |
|---|---|---|---|---|
| 0 | `1 1 _` | 0 | `q0` | reads `1`, writes `1`, moves R |
| 1 | `1 1 _` | 1 | `q0` | reads `1`, writes `1`, moves R |
| 2 | `1 1 _` | 2 | `q0` | reads `_`, writes `1`, **accept** |

Final tape `"111"`, **3 steps** — verified. For input of length n the machine takes **n + 1 steps**:
n to walk over the `1`s and one to write the new one. Verified at n = 0, 1, 3, 5 giving 1, 2, 4, 6
steps. *(Counting the accepting transition as a step; some texts count n.)*

**2.** A finite automaton has a fixed number of states, say k, and **no memory other than which
state it is in**. To verify `aⁿbⁿ` it must, on reaching the `b`s, know how many `a`s it saw.

Feed it the k+1 strings `a`, `aa`, …, `a^(k+1)`. Each drives the machine to some state, and there
are only k states, so by the **pigeonhole principle** two different prefixes `a^i` and `a^j` (i ≠ j)
end in the same state. From that state the machine's future behaviour is identical — it cannot
distinguish them. So it treats `a^i b^i` and `a^j b^i` the same, and must either accept both or
reject both. Since exactly one is in the language, the automaton is wrong on one of them. ∎

The Turing machine has an **unbounded tape it can write to and revisit**. It does not need to
*remember* the count in its states — it *records* it on the tape by crossing off matched pairs.
Storage that is external, unbounded, and rewritable is the whole difference.

**3.** The machine only needs to remember the most recent symbol it read, so three states suffice:

- **`qs`** — start state, nothing read yet
- **`q0`** — "the last symbol read was `0`"
- **`q1`** — "the last symbol read was `1`"

| State | Read | Write | Move | Next |
|---|---|---|---|---|
| `qs` (start) | `0` | `0` | R | `q0` |
| `qs` | `1` | `1` | R | `q1` |
| `qs` | `_` | `_` | — | **reject** (empty string) |
| `q0` | `0` | `0` | R | `q0` |
| `q0` | `1` | `1` | R | `q1` |
| `q0` | `_` | `_` | — | **accept** |
| `q1` | `0` | `0` | R | `q0` |
| `q1` | `1` | `1` | R | `q1` |
| `q1` | `_` | `_` | — | **reject** |

The machine never writes anything different from what it reads and never moves left — **all of its
memory is in the state**. That is the signature of a problem a *finite automaton* could already
solve, and it is worth noticing: having a tape does not mean you must use it.

**4.** It cannot be proved because one side of the claim is **informal**. "Effectively computable"
is an intuitive notion about what a human or machine can do by following a finite set of mechanical
rules; it has no mathematical definition. A proof needs two formal objects, and here there is only
one. The thesis asserts that the formal object (Turing computability) correctly captures the
informal one.

**What would refute it:** exhibiting a physically realisable procedure that computes a function no
Turing machine can — a working "hypercomputer", say one that decides the halting problem. That is a
falsifiable claim, and nothing in ninety years has come close.

**Why quantum computing is not a refutation:** quantum computers compute exactly the same
**class of functions** as Turing machines. They are believed to be faster for certain problems —
factoring via Shor's algorithm, most famously — but "faster" is a *complexity* claim, not a
*computability* one. A quantum computer cannot decide the halting problem either. Confusing these
two axes is the single most common misunderstanding of the thesis, and the distinction is exactly
the one between this week and Week 6.

---

## Reading

- **Sipser, *Introduction to the Theory of Computation*, Ch. 3.1–3.3** — Turing machines, the
  formal definition, and variants (primary)
- **Sipser, Ch. 1.1** — finite automata, for §2
- **Turing (1936), "On Computable Numbers"** — the original paper; §1–§6 are surprisingly readable
- **Petzold, *The Annotated Turing*** — optional, and the gentlest route into the original

---

*CS 101 · Week 11 · Lecture 34 (Wed) · © CSE Department*
