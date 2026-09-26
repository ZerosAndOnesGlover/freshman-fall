# CS 101 · Problem Set 11 Solutions (Instructor)
## Computability and Undecidability

**Reference code:** `ps11_solution.py` — verified **11/11 tests passing**.
**Total: 100 points + 10 bonus**

---

*(Revised 2026-09-26: the set no longer asks A1(a), A3(b), B2 or B3 — Lab 11 writes the recogniser — so
those answers below can be ignored. Renumbered: A1(b)–(c) → A1(a)–(b), A3(c) → A3(b), B4 → B2, B5 → B3.
Marks: A1 4/4, A2 2/4/4, A3 4/6, A4 8/4/4, A5 9/9, B1 18, B2 12, B3 4 + 4.)*

## Part A: Written Questions (62 points)

### A1: Models and Their Limits (10 points)

**(a)** *(4 pts — 2 for the tuple, 2 for the roles)*

A TM is **(Q, Σ, Γ, δ, q₀, q_accept, q_reject)**:

| Component | Role |
|---|---|
| Q | finite set of states — the machine's fixed memory |
| Σ | input alphabet (excludes the blank) |
| Γ | tape alphabet, Σ ⊆ Γ, includes the blank |
| δ: Q × Γ → Q × Γ × {L,R} | the transition function — **the machine itself** |
| q₀ | start state |
| q_accept, q_reject | halting states |

Full marks require noting that δ *is* the machine; the rest is bookkeeping.

**(b)** *(3 pts)* The claim is **wrong**: a two-head machine is **equivalent in power**. A one-head
machine simulates it by storing both head positions as marked symbols on the tape and sweeping
between them. Anything the two-head machine computes, the one-head machine computes.

What it buys is **speed** — a polynomial factor, no more. This is the L34 §4 distinction: model
variations change complexity, not computability. *(2 of the 3 points are for naming that
distinction.)*

**(c)** *(3 pts)* **Can:** strings with an even number of `1`s (or any regular language). **Cannot:**
`aⁿbⁿ`, or equal numbers of `0`s and `1`s.

The separating property: **whether recognition requires unbounded counting**. A finite automaton has
finitely many states and no external storage, so it can distinguish only finitely many counts; by
pigeonhole, two different prefixes collide and it cannot tell them apart thereafter.

---

### A2: The Church–Turing Thesis (8 points)

**(a)** *(2 pts)* Any function computable by *any* effective procedure is computable by a Turing
machine.

**(b)** *(3 pts)* "Effective procedure" is an **informal** notion with no mathematical definition. A
proof requires two formal objects to relate; here one side is intuitive. The thesis asserts that the
formal notion correctly captures the informal one — evidenced by every independent attempt
(λ-calculus, recursive functions, register machines, real hardware) landing on the same class, but
evidence is not proof.

**(c)** *(3 pts)* The confusion is **computability vs complexity**. Quantum computers compute exactly
the same class of functions; they are conjectured faster on certain problems (factoring), which is a
statement about *resources*, not *possibility*. A quantum computer cannot decide the halting problem.

A genuine refutation would be a **physically realisable procedure computing a function no TM can** —
a working hypercomputer. Nothing has come close.

*Marking:* full marks require naming the complexity/computability distinction explicitly. "Quantum
isn't that powerful" without the distinction is worth 1.

---

### A3: Decidable, Recognisable, Neither (10 points)

**(a)** *(3 pts)* **Decidable:** a TM exists that, on every input, **halts** and answers correctly.
**Recognisable:** a TM exists that accepts every string in L, but on strings not in L may reject *or
run forever*.

The difference is the **halting guarantee on no-instances**.

**(b)** *(3 pts)*

```python
def recognise_halt(f, x):
    f(x)
    return True
```

It lacks **totality**. It is sound (a `True` return is always correct) and catches every halting
computation eventually; it simply never returns on non-halting ones.

**(c)** *(4 pts)* Suppose you have a recogniser R for L and a recogniser R' for its complement. Run
**both at once**, interleaving their steps (dovetailing).

Every input is in either L or its complement, so **exactly one** of the two recognisers is guaranteed
to accept eventually. Whichever accepts first tells you the answer, and you halt. Since one is always
guaranteed to accept, this procedure **always terminates** — which is exactly a decider.

*Marking:* the key insight is running both simultaneously, and that termination is guaranteed because
one of them must accept. Students who say "run R first, then R'" have missed it — R might never
return, and you would never start R'. Award 2 for the right idea with sequential execution, 4 for
dovetailing.

The contrapositive is the useful form: **HALT is recognisable, so its complement is not.** Otherwise
HALT would be decidable.

---

### A4: The Halting Problem (12 points)

**(a)** *(6 pts — 2 construction, 2 per case)*

Assume `halts(f, x)` exists, always halting and always correct. Then define:

```python
def paradox(f):
    if halts(f, f):
        while True: pass
    else:
        return
```

Run `paradox(paradox)`:

- **If it halts** — then `halts(paradox, paradox)` returned `True`, so the code took the `while True`
  branch and **never halts**. Contradiction.
- **If it does not halt** — then `halts(paradox, paradox)` returned `False`, so the code hit `return`
  and **halts**. Contradiction.

The cases are exhaustive. The only assumption was `halts`, so `halts` does not exist. ∎

*Marking:* both cases must be argued. One case alone is 3/6, not 5/6 — the proof is the exhaustion.

**(b)** *(3 pts)* The contradiction requires that the computation `halts` is **predicting** and the
computation `paradox` is **performing** be the same one. Feeding `paradox` some other function g
gives `halts(g, g)`, and `paradox`'s own behaviour is then unconstrained by that answer — no
contradiction arises, only an ordinary program that does something.

Self-application is what closes the loop. It is available only because programs are data
(universality, L34 §5).

**(c)** *(3 pts)*

| Diagonalization | Halting proof |
|---|---|
| The table T[i][j] | "does program Pᵢ halt on input j" |
| The diagonal T[i][i] | "does Pᵢ halt on **its own description**" |
| The flipped element D | `paradox` — halts exactly when the diagonal says it doesn't |

D differs from every Pᵢ at position i, so D is not in the enumeration — yet D is a program. The
contradiction is the same one; `paradox` is D written as code.

---

### A5: Reduction (12 points)

**(a) ALWAYS-CRASHES** *(6 pts)*

Assume `crashes(f, x)` decides whether `f(x)` raises an exception. Construct:

```python
def halts(f, x):
    def wrapper(_):
        f(x)                 # if this never returns, we never reach the raise
        raise ValueError()   # reached ONLY if f(x) halted
    return crashes(wrapper, None)
```

- **If f(x) halts** — control reaches `raise`, so `wrapper` crashes, `crashes` returns `True`,
  `halts` returns `True`. ✅
- **If f(x) loops forever** — control never reaches `raise`. `wrapper` never crashes (it never
  finishes at all), so `crashes` returns `False` and `halts` returns `False`. ✅

`halts` would be correct on all inputs, contradicting A4. Therefore `crashes` does not exist. ∎

*Marking:* 2 for the construction, 2 per direction. A common slip is assuming `f(x)` itself might
raise — note that if it does, it *halted*, and the answer `True` is still correct. Students who spot
and address this deserve full credit and a comment.

**(b) EMPTY** *(6 pts)*

Assume `is_empty(M)` decides whether M accepts nothing. Construct:

```python
def halts(M, w):
    def wrapper(anything):   # ignores its own input
        M(w)                 # run M on the FIXED w
        return ACCEPT
    return not is_empty(wrapper)
```

`wrapper` ignores its argument, so its behaviour is identical on every input — it either accepts
everything or nothing.

- **If M(w) halts** — `wrapper` reaches `ACCEPT` on **every** input, so its language is Σ\* — not
  empty. `is_empty` returns `False`, `halts` returns `True`. ✅
- **If M(w) loops forever** — `wrapper` never accepts anything, so its language **is** empty.
  `is_empty` returns `True`, `halts` returns `False`. ✅

Contradiction with A4; `is_empty` does not exist. ∎

*Marking:* the **input-ignoring wrapper** is the technique being tested — it converts an
"all inputs" question into a "this one computation" question. Students who reduce backwards (using
`halts` to build `is_empty`) get **at most 1 point** regardless of how well written; the direction is
the whole content of the problem.

---

## Part B: Code (48 points)

All implementations in `ps11_solution.py`, verified 11/11.

### B1: `equal_zeros_ones()` (12 points)

The two structural problems, and their solutions:

**Left-end detection.** The tape is one-way infinite and the simulator **clamps** at position 0, so a
machine sweeping left never bumps into a boundary it can detect — it just spins. The fix is a
**sentinel**: the very first symbol crossed off is marked `Z` instead of `X`. The return sweep runs
left until it reads `Z`, then steps right into the scanning state.

*This is worth dwelling on in office hours.* Students who do not use a sentinel typically produce a
machine that times out on every input, and the cause is invisible from the outcome.

**Why the partner is always to the right.** The scanning state `q0` starts at the sentinel and moves
right over `X`s only. So when it stops at an unmarked symbol, **everything to its left is already
crossed off**. Any unmatched partner must therefore lie to the right, and scanning rightward is
complete.

Verified: accepts `""`, `"01"`, `"10"`, `"0011"`, `"0101"`, `"1100"`, `"011010"`, `"000111"`;
rejects `"0"`, `"1"`, `"001"`, `"110"`, `"01011"`, `"0001"`.

*Marking:* 10 for the tests, 2 for the invariant comment. A machine that works but does not state the
invariant loses the 2.

### B2: `binary_increment()` (14 points)

Three phases, and the third is where the marks are.

1. **Sentinel** — `qInit` rewrites the leftmost digit as `A` (was `0`) or `B` (was `1`), so the carry
   sweep can recognise the left end.
2. **Carry** — walk right to the blank, then leftward: `1` → `0` and keep carrying; `0` → `1` and
   stop.
3. **Overflow** — reaching the sentinel still carrying means the result is one digit longer. `A`
   (leading 0) simply becomes `1`. `B` (leading 1) becomes `0` and triggers a **right shift**.

The shift is a pair of states `qShift1`/`qShift0` meaning "I am carrying this digit": write the
carried digit into the current cell, pick up whatever was there, move right. On reaching the blank,
write the carried digit and accept.

Trace for `"111"` (the case that exposes every bug):

| Phase | Tape |
|---|---|
| after `qInit` | `B11` |
| after carry sweep | `000` (sentinel `B` consumed, carry still out) |
| after shift | `1000` |

Verified on **all of n = 0..31**.

*Marking:* 8 for carry correctness, 6 for overflow. A machine correct on `"1011"` but producing
`"100"` for `"111"` has the classic clamping bug — it silently loses the overflow digit — and earns
the 8 but not the 6.

### B3: `recognise_halt()` (8 points)

```python
def recognise_halt(machine, tape_input, start_budget=1):
    budget = start_budget
    while True:
        outcome, _, _ = machine.run(tape_input, max_steps=budget)
        if outcome != "timeout":
            return True
        budget *= 2
```

**Written answer:** it lacks **totality**. It is sound (returns `True` only after observing a halt)
and complete on yes-instances (any halting machine has a finite step count, and the budget doubles
without bound, so it is caught eventually). On **no-instances** it never returns.

*Marking:* 5 for code, 3 for correctly identifying totality **and** naming no-instances as where the
failure lives. "It might be slow" is not the answer.

### B4: `build_prints_hello_wrapper()` (8 points)

```python
def build_prints_hello_wrapper(f, x, log):
    def wrapper():
        f(x)
        log.append("hello")
    return wrapper
```

**Written answer:** the construction assumes **PRINTS-HELLO is decidable** and concludes **HALT is
decidable** — since `wrapper` logs `hello` exactly when `f(x)` halts, any PRINTS-HELLO decider
answers HALT. HALT is undecidable, so PRINTS-HELLO is too.

*Marking:* 5 for code, 3 for the explanation — and the explanation must get the **direction** right.
"We use `halts` to check if it prints hello" is backwards and earns 0 of the 3.

### B5: Classification (6 points)

| Question | Answer | Justification |
|---|---|---|
| source contains `'while'` | **decidable** | **Syntactic** — search the text |
| ever *executes* a `while` loop | **undecidable** | **Semantic**, non-trivial — Rice |
| halts within 1000 steps on w | **decidable** | **Resource-bounded** — simulate 1000 steps |
| halts on every input | **undecidable** | Semantic, non-trivial — Rice (this is ALL-HALT) |
| even number of states | **decidable** | **Syntactic** — count them |
| two programs compute the same function | **undecidable** | Semantic, non-trivial — Rice |

*Marking:* 3 for the dict (½ each), 3 for justifications (½ each). A justification must name
**syntactic**, **resource-bounded**, or **Rice/semantic** — "because it's hard" earns nothing.

The first two rows are the pedagogical point: nearly identical English, opposite answers, because one
asks about **text** and the other about **behaviour**.

---

