# CS 101 · Lab 11
## Building a Turing Machine

**Duration:** 3 hours · **Starter:** `tm_lab_starter.py` · **Submit:** your completed file + `answers.md`

---

## Goals

By the end you will have:

- Implemented a working Turing machine simulator from the formal definition
- Built machines for three languages, including one no finite automaton can recognise
- Watched a universal machine simulate another machine
- Confronted the halting problem experimentally, and seen exactly where the experiment fails

The lecture gave you the theory. Today the theory has to run.

---

## Part 0 — Setup (5 minutes)

```bash
cd ~/cs101/week11
python3 tm_lab_starter.py
```

You should see `0/11 tests passing`, with every test reporting `not implemented`. That is the
correct starting state. Your job is to reach 11/11.

Read the whole starter file before writing anything. In particular read the tests — they are the
specification, and they say precisely what each function must do.

---

## Part 1 — Read the Definition Again (15 minutes)

Before coding, translate the formal definition into the data structures in the starter.

A TM is (Q, Σ, Γ, δ, q₀, q_accept, q_reject). In the starter:

| Formal | In code |
|---|---|
| δ | `transitions`, a dict `(state, symbol) -> (next_state, write, move)` |
| q₀ | `self.start` |
| q_accept, q_reject | `self.accept`, `self.reject` |
| Γ's blank | `BLANK`, the string `"_"` |
| The tape | a Python `list` of single-character strings |

**Exercise 1.1.** In `answers.md`, write out the `transitions` dict for the unary-increment machine
from L34 §3 by hand, before implementing anything. It is two entries.

**Exercise 1.2.** The tape is *infinite* but a Python list is not. State, in one sentence, how the
simulator can be faithful to an infinite tape using finite memory.

---

## Part 2 — Implement `step()` (35 minutes)

`step()` performs exactly one transition. Get this right and everything else follows.

It must:

1. Extend the tape with blanks if `head` has run past the right end
2. Look up `(state, tape[head])` in `self.transitions`
3. Write the new symbol, move the head, return the new state
4. Raise `KeyError` if no transition is defined — the machine is **stuck**

**Exercise 2.1.** Implement `step()`. Run the tests; the four Part 2 tests should pass.

**Exercise 2.2 — the edge case that will bite you.** Our tape is infinite in *one* direction only.
What should happen if the machine tries to move left from position 0?

Three defensible answers: crash, stay put, or extend leftward. The tests require **stay put**
(clamp at 0). In `answers.md`, say which you think is the better *modelling* choice and why — and
note whether it changes what the machine can compute.

**Exercise 2.3.** There is a second place blanks may need appending that is easy to miss. After
moving right off the end of the tape, `head` is out of range. If you only extend at the *top* of
`step()`, the tape returned by this call has an invalid `head`.

State the **invariant** your implementation maintains, and where you enforce it. (The reference
solution states: *on entry and on return, `head` is a valid index into `tape`* — and enforces it
both before the lookup and after the move.)

---

## Part 3 — Implement `run()` (30 minutes)

`run()` drives `step()` in a loop and reports what happened.

It returns `(outcome, tape, steps)` where outcome is one of:

| Outcome | Meaning |
|---|---|
| `"accept"` | reached `self.accept` |
| `"reject"` | reached `self.reject` |
| `"stuck"` | no transition defined — a halt, in a non-accepting state |
| `"timeout"` | hit `max_steps` without halting |

**Exercise 3.1.** Implement `run()`. Check the halting states *before* stepping, so a machine
starting in an accept state accepts in 0 steps.

**Exercise 3.2 — why `max_steps` exists.** Delete the `max_steps` guard and run the built-in
infinite-loop machine from the tests. Then restore it.

In `answers.md`, answer precisely: **why can the simulator not simply detect the infinite loop and
report it, instead of giving up after a fixed count?** Name the theorem.

**Exercise 3.3.** `"timeout"` and `"stuck"` are different outcomes, and conflating them is a real
bug. Explain the difference in one sentence each, and say which one is a *halt*.

---

## Part 4 — Build Three Machines (50 minutes)

**Exercise 4.1 — `unary_increment()`.** Return the machine from Exercise 1.1. Two transitions.

**Exercise 4.2 — `even_ones()`.** Accept strings over `{0,1}` with an even number of `1`s.

Two states, and the state *is* the memory: name them `even` and `odd`, and make each one mean "the
number of `1`s seen so far has this parity." When the blank is reached, accept from `even`, reject
from `odd`.

In `answers.md`: this machine never writes anything different from what it reads and never moves
left. What does that tell you about the *class* of this language?

**Exercise 4.3 — `a_n_b_n()`.** Accept exactly `aⁿbⁿ`. This is the one that matters.

The strategy is cross-off-and-repeat: mark the leftmost `a` as `X`, walk right to the leftmost
unmarked `b` and mark it `Y`, walk back, repeat. Accept when no `a`s remain and nothing but `Y`s
follow. The transition table is in L34 §3 — but try to derive it before looking.

Verify it accepts `""`, `"ab"`, `"aabb"`, `"aaabbb"` and rejects `"aab"`, `"abb"`, `"ba"`,
`"aabbb"`, `"abab"`.

**Exercise 4.4.** Run `a_n_b_n()` with `trace=True` on `"aabb"`. You should see 13 steps. Paste the
trace into `answers.md` and annotate which steps constitute one complete "cross off a pair" cycle.

**Exercise 4.5 — the payoff.** In `answers.md`, in a short paragraph: L30 told you no regular
expression can match `aⁿbⁿ` or parse HTML. You have just written a machine that does the first one.
Explain what your machine has that a regex does not, and why that is a statement about *models*
rather than about Python's `re` engine.

---

## Part 5 — The Universal Machine (25 minutes)

L34 §5 claimed a machine can simulate another machine given its description. Your simulator **is**
that claim, in Python.

**Exercise 5.1.** Write a function:

```python
def universal(machine_description, tape_input):
    """machine_description is a (transitions, start, accept, reject) tuple."""
```

that builds a `TuringMachine` from the description and runs it. Three lines.

**Exercise 5.2.** Call `universal()` on the *description* of `a_n_b_n()` with input `"aabb"`.
Confirm you get the same result as calling the machine directly.

**Exercise 5.3.** In `answers.md`: you have just written a program that takes a program as data and
runs it. Name the two things this makes possible — one from L34 (an architecture) and one from L35
(a proof technique).

---

## Part 6 — Meeting the Halting Problem (30 minutes)

Now try to do the impossible, and watch precisely where it fails.

**Exercise 6.1.** Write:

```python
def will_halt(machine, tape_input, budget=10_000):
    """Return True if the machine halts within budget, False otherwise."""
```

using your `run()`. This is easy — write it.

**Exercise 6.2.** `will_halt` is **not** a halting decider. State, in one sentence, exactly what it
gets wrong, and give a machine on which it returns the wrong answer.

**Exercise 6.3 — the experiment.** Try to repair it by raising the budget. Write a loop that
doubles `budget` until the machine halts:

```python
def will_halt_harder(machine, tape_input):
    budget = 1
    while True:
        outcome, _, _ = machine.run(tape_input, max_steps=budget)
        if outcome != "timeout":
            return True
        budget *= 2
```

In `answers.md`: this is *sound* — when it returns, it is right. Which of the three properties from
L35 §6 does it lack, and on which inputs does the failure show up?

**Exercise 6.4.** Connect it to the proof. `will_halt_harder` is exactly the **recogniser** from
L35 §5. Write one sentence explaining why no amount of cleverness in choosing budgets can turn it
into a decider — and be specific about which direction (yes-instances or no-instances) is the
problem.

---

## Part 7 — Checkoff and Submission (10 minutes)

Before submitting, confirm:

- [ ] `python3 tm_lab_starter.py` reports **11/11 tests passing**
- [ ] `step()` states and maintains its head-validity invariant (Ex 2.3)
- [ ] `run()` distinguishes all four outcomes, and checks halting states before stepping
- [ ] All three machines built, `a_n_b_n()` verified on the full accept/reject list
- [ ] `universal()` implemented and demonstrated (Part 5)
- [ ] `answers.md` addresses 1.1, 1.2, 2.2, 2.3, 3.2, 3.3, 4.2, 4.4, 4.5, 5.3, 6.2, 6.3, 6.4
- [ ] No `__pycache__` directory in your submission

**Marking:** 60% tests passing, 40% `answers.md`. The written answers are marked on whether you can
say *why*, not on length. Exercises 4.5, 6.3 and 6.4 carry the most weight — they are the ones that
show whether the week landed.

---

## Reflection Questions

Answer in `answers.md`, a paragraph each:

1. You implemented an infinite tape with a Python list that grows on demand. In what sense is your
   simulator a faithful Turing machine, and in what sense is it not? Does the difference affect
   which languages it can recognise?

2. Your `step()` is about ten lines. The Church–Turing thesis says these ten lines capture
   everything any computer can ever do. What is your honest reaction, and what would it take to
   convince you?

3. Part 6 had you build something that *almost* decides halting. Describe the experience of the gap
   between "works on everything I tried" and "provably cannot work" — and say where else in
   programming you have met that gap.

---

## Bonus Challenges

1. **Binary increment.** A TM that adds 1 to a binary number. Harder than unary — you must handle
   the carry, which means walking right to the end, then processing leftward.

2. **Palindrome checker.** Accept `w` over `{0,1}` iff `w` reads the same backwards. Cross off the
   first and last symbols and repeat.

3. **Step-count growth.** Measure steps for `a_n_b_n()` at n = 1..12 and tabulate. The crossing-off
   strategy walks the tape once per pair, so predict the growth *before* measuring, then check.
   Take **first and second differences** of your step counts — that is the fastest way to identify
   the degree. Fit an exact closed form and verify it on every n you measured. (Compare your Week 6
   techniques.)

4. **A two-tape machine.** Extend the simulator to two tapes. Then re-implement `a_n_b_n()` using
   the second tape as a counter and compare step counts. You have just experienced why multi-tape
   machines are *no more powerful* but can be *polynomially faster* — the computability/complexity
   distinction from L34 §4, made concrete.

5. **Busy beaver.** Among 3-state, 2-symbol machines that halt on a blank tape, the record for
   *most `1`s written* is **6**, and the record for *most steps taken* is **21**. Careful: these are
   **two different machines** — the 6-`1` champion halts in 13 steps, and the 21-step champion writes
   only 4 `1`s. Σ(n) and S(n) are separate functions.

   Search the space (there are few enough to brute-force) and find both champions. Then read why
   BB(5) took until 2024 to settle, and why BB(6) is beyond reach — this is undecidability with a
   number attached: BB grows faster than *any* computable function, which is exactly why no program
   can compute it.

---

*CS 101 · Week 11 · Lab 11 · © CSE Department*
