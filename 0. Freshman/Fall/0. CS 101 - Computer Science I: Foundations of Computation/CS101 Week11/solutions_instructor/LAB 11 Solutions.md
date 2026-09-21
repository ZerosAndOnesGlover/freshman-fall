# CS 101 · Lab 11 Solutions (Instructor)
## Building a Turing Machine

**Reference implementation:** `tm_lab_solution.py` — verified **11/11 tests passing**.


> Lab sat Tuesday 15 December 2026 (moved from Thursday of Week 11, which clashed with the PHYS 141 lab).
> Revised 2026-09-21: the universal-machine part and the bonus challenges were removed to fit 110 minutes.
---

## Marking Summary

| Component | Weight |
|---|---|
| Tests passing (11) | 60% |
| `answers.md` written responses | 40% |

Within the written portion, weight **4.5, 5.3, 5.4** most heavily — they are the exercises that
reveal whether the week's central idea landed. A student can reach 11/11 by pattern-matching the
lecture tables; only the written answers show understanding.

---

## Part 1

**1.1** Two entries:

```python
{("q0", "1"): ("q0", "1", "R"),
 ("q0", BLANK): ("qa", "1", "S")}
```

*Marking:* accept any equivalent state names. Deduct if the blank transition writes `1` but moves
right and then accepts in a separate state — that is correct but a step slower; note it, don't
penalise.

**1.2** The tape is *potentially* infinite, not *actually* infinite. Any halting computation touches
only finitely many cells, so the simulator appends blanks on demand and is faithful to every
computation it completes. It is unfaithful only in that it can exhaust real memory — a limitation of
the simulator, not of the model.

---

## Part 2

**2.1** See `tm_lab_solution.py`:

```python
def step(self, tape, head, state):
    # Invariant: on entry AND on return, head is a valid index into tape.
    while head >= len(tape):
        tape.append(self.blank)
    next_state, write, move = self.transitions[(state, tape[head])]
    tape[head] = write
    if move == "R":
        head += 1
    elif move == "L":
        head = max(0, head - 1)   # one-way-infinite tape: clamp at the left edge
    while head >= len(tape):
        tape.append(self.blank)
    return tape, head, next_state
```

The `KeyError` requirement needs no code — indexing a dict with a missing key raises it. Students who
wrote an explicit `if key not in self.transitions: raise KeyError(...)` are also correct.

**2.2** All three choices are defensible; the tests require clamping.

- **Clamp (stay put)** — simplest; matches the standard one-way-infinite definition in Sipser.
- **Crash** — arguably the most honest, since the machine has done something undefined.
- **Extend leftward** — gives a two-way-infinite tape.

**The key insight, and what to mark for:** the choice does **not** change what the machine can
compute. A two-way-infinite tape is simulable on a one-way tape (fold it: interleave the two halves
into odd and even cells), so the models are equivalent in power. Students who say "extending left is
more powerful" have missed the point — give partial credit only.

**2.3** The invariant is: **on entry and on return, `head` is a valid index into `tape`.**

It must be enforced in **two** places — before the lookup (in case a caller passes a head past the
end) and after the move (because moving right off the end invalidates it). Enforcing it only at the
top is the most common bug, and it surfaces as an `IndexError` on the *next* call, far from the
cause.

*This is the exercise most likely to catch a student who copied without understanding.* The starter's
test `step extends tape with blank` fails exactly on this mistake.

---

## Part 3

**3.1**

```python
def run(self, input_string, max_steps=10_000, trace=False):
    tape = list(input_string) or [self.blank]
    head, state, steps = 0, self.start, 0
    while steps < max_steps:
        if state == self.accept:
            return ("accept", "".join(tape).rstrip(self.blank), steps)
        if state == self.reject:
            return ("reject", "".join(tape).rstrip(self.blank), steps)
        try:
            tape, head, state = self.step(tape, head, state)
        except KeyError:
            return ("stuck", "".join(tape).rstrip(self.blank), steps)
        steps += 1
    return ("timeout", "".join(tape).rstrip(self.blank), steps)
```

Two details worth a mark each: the `or [self.blank]` handles empty input, and checking halting states
*before* stepping means a machine already in its accept state accepts in 0 steps.

**3.2** The simulator cannot detect the loop and report it because **that is the halting problem**
(L35). A general "is this machine going to loop forever?" detector is precisely the decider Turing
proved cannot exist. `max_steps` is not a lazy shortcut — it is the **resource bound** escape hatch
from L36 §4, and it is the only option available.

*Mark for:* naming the halting problem explicitly. A student who says "it's hard" or "it would take
too long" has missed it — this is not a performance issue.

**3.3**

- **`stuck`** — no transition is defined for the current (state, symbol). The machine **halts**, in a
  non-accepting state. This is a legitimate rejection.
- **`timeout`** — the machine was still running when the budget ran out. It has **not halted**, and
  we do not know whether it ever will.

**`stuck` is the halt.** Conflating them is a real bug: `timeout` means "no answer", `stuck` means
"the answer is no". A grader that treats timeout as rejection will mark correct-but-slow machines
wrong — which is exactly the soundness failure discussed in L36 Ex 4.

---

## Part 4

**4.1–4.3** See `tm_lab_solution.py`. All three verified against the full accept/reject lists.

**4.2 (written)** The machine never writes a different symbol and never moves left — **it never uses
the tape at all.** All of its memory is in its two states. That means a *finite automaton* could
recognise this language, so it is **regular**. Indeed it is `((0*10*1)*0*)` in regex form.

The point: having a tape does not oblige you to use it. This machine is a Turing machine only
incidentally.

**4.4** Verified trace, 13 steps:

```
   1: 'Xabb' head=1 state=q1
   2: 'Xabb' head=2 state=q1
   3: 'XaYb' head=1 state=q2
   4: 'XaYb' head=0 state=q2
   5: 'XaYb' head=1 state=q0
   6: 'XXYb' head=2 state=q1
   7: 'XXYb' head=3 state=q1
   8: 'XXYY' head=2 state=q2
   9: 'XXYY' head=1 state=q2
  10: 'XXYY' head=2 state=q0
  11: 'XXYY' head=3 state=q3
  12: 'XXYY_' head=4 state=q3
  13: 'XXYY_' head=4 state=qa
('accept', 'XXYY', 13)
```

**The cycles:** steps **1–5** cross off the first pair (`a`→`X` at step 1, `b`→`Y` at step 3, walk
back through steps 4–5). Steps **6–10** cross off the second pair. Steps **11–13** are the final
verification sweep in `q3`, confirming only `Y`s remain before accepting.

*Mark for:* correctly identifying that the return-walk (steps 4–5, 9–10) is part of the cycle. This
is what makes the algorithm quadratic — see bonus 3.

**4.5** The machine has an **unbounded, rewritable, re-readable tape**; a regular expression has only
a fixed number of states. Matching `aⁿbⁿ` requires remembering an unbounded count, and a fixed state
set can only distinguish finitely many counts (L34 §2, the pigeonhole argument).

The crucial phrase to look for: **this is a property of the model, not the implementation.** No
change to Python's `re` module — no optimisation, no new syntax, no faster backtracking — can fix
it, because regular expressions *define* the regular languages and `aⁿbⁿ` is provably not one. That
is why L30's "don't parse HTML with regex" is a theorem rather than style advice.

*Full marks* require distinguishing model from implementation. A student who says "regex is too slow"
or "the engine can't handle nesting" has the conclusion without the reason.

---

## Part 5

**5.1**

```python
def will_halt(machine, tape_input, budget=10_000):
    return machine.run(tape_input, max_steps=budget)[0] != "timeout"
```

**5.2** It returns `False` for machines that **halt, but take more than `budget` steps** — conflating
"did not halt in time" with "does not halt". Any machine exceeding the budget works as a
counterexample; the cleanest is the unary-increment machine on an input of 20,000 `1`s, which halts
in 20,001 steps but is reported as non-halting at the default budget.

*Mark for:* a concrete counterexample, not just the description.

**5.3** It lacks **totality**. It is sound (a `True` return is always correct, since the machine
demonstrably halted) and it is complete on yes-instances (any halting machine is eventually caught,
because the budget doubles without bound and every halting computation has a finite step count).

**The failure is on no-instances:** if the machine never halts, the loop doubles the budget forever
and `will_halt_harder` never returns. It gives a wrong answer to nobody; it simply gives no answer to
some.

**5.4** This is exactly L35 §5's recogniser. No budget schedule fixes it because **the problem is
asymmetric**: halting is witnessed by a finite computation, so running long enough always confirms a
*yes*. Non-halting has no finite witness — at every step, "it might halt on the next one" remains
consistent with everything observed so far, so no finite observation ever establishes *no*.

*Mark for:* explicitly identifying that **no-instances** are the unattainable direction, and that the
reason is the absence of a finite witness. A student who says "you'd have to wait forever" is on the
right track but should be pushed to say *why* waiting never suffices.

---

## Reflection Questions

**1.** Faithful: it implements δ exactly, and any computation it completes is exactly the computation
the formal machine performs. Unfaithful: real memory is finite, so a computation needing more tape
than RAM fails.

**The important half of the answer:** this does **not** change which languages are recognisable *in
principle*, because the limit is on the simulator's resources rather than on the model. It is the
same distinction as L34 §4 — the Church–Turing thesis is about computability, not about resources.
Students who conclude "so my simulator is weaker than a real TM, therefore the theory doesn't apply"
have inverted it.

**2.** Accept any honest reaction. Look for engagement with what would *refute* the thesis — a
physically realisable procedure computing a non-computable function. Reward students who note that
"I can't imagine how X would be done by a TM" is not evidence, since the thesis has survived ninety
years of exactly that intuition being wrong.

**3.** The gap between empirical confidence and proof. Good answers connect to Week 7: a passing test
suite is evidence, never proof, and now they know it is a theorem rather than a gap in diligence.
Other legitimate connections: type systems that reject correct programs, `-Werror` promoting
detectable problems while undetectable ones sail through, benchmarks that fail to expose worst cases.

---

