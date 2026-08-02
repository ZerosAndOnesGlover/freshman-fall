# CS 101: Lecture 35 (Week 11, Lecture 2)
## Decidability and the Halting Problem

---

## 0. Where This Is Going

Tuesday built the model: a Turing machine, and the Church–Turing thesis that says proving something
impossible *for that model* proves it impossible for **every program in every language forever**.

Today we use it. We prove that a specific, precisely stated, obviously useful problem has **no
solution** — not "no efficient solution", not "no solution yet". None, ever.

The proof is short. It fits on a slide. It is also one of the most consequential results in the
history of the field, and it explains why your compiler warns instead of proves.

---

## 1. Decision Problems and Decidability

To be precise about "solvable" we narrow to **decision problems** — questions with a yes/no answer.

- *Is n prime?* — decision problem
- *Does this list contain duplicates?* — decision problem
- *Does this program halt on this input?* — decision problem

A decision problem is a **language**: the set of inputs whose answer is *yes*. "Is n prime?" is the
language {2, 3, 5, 7, 11, …}. Deciding the problem means recognising membership in the set.

> **Definition.** A language L is **decidable** if some Turing machine M exists such that for
> **every** input w, M halts and correctly answers whether w ∈ L.
>
> M must **always halt**. A machine that answers correctly but sometimes runs forever does not
> decide L.

That "always halts" clause is where all the difficulty lives. Weakening it gives:

> **Definition.** A language L is **recognisable** (or *semi-decidable*) if some TM accepts every
> w ∈ L, and for w ∉ L either rejects or **runs forever**.

A recogniser can say *yes*; it just may never get around to saying *no*. Hold on to this
distinction — it is the punchline in §5, and it is the difference between a test suite and a proof.

---

## 2. The Problem

> **HALT** = { ⟨M, w⟩ : M is a Turing machine that halts on input w }

In Python terms: a function `halts(f, x)` that returns `True` if calling `f(x)` would eventually
finish, and `False` if it would loop forever. It must return — no crashing, no hanging, no "maybe".

This would be extraordinarily useful. No more infinite loops in production. Your editor would flag
non-termination as you typed. A grader could check that a student's program finishes before running
it.

**Theorem (Turing, 1936).** HALT is undecidable.

---

## 3. The Proof

Suppose, for contradiction, that HALT is decidable. Then some program `halts(f, x)` exists that
always halts and always answers correctly.

Using it, build this program:

```python
def halts(f, x):
    """Assumed to exist: returns True iff f(x) eventually finishes."""
    ...

def paradox(f):
    if halts(f, f):        # does f halt when given itself as input?
        while True:        # ...then deliberately loop forever
            pass
    else:
        return             # ...then deliberately halt
```

`paradox` is a perfectly ordinary program. If `halts` exists, `paradox` can be written — it is
three lines of standard control flow, nothing exotic.

Now run it on itself:

```python
paradox(paradox)
```

Ask the only question that matters: **does this halt?**

**Case 1 — suppose it halts.** Then `halts(paradox, paradox)` returned `True` (that is the only
branch that can be taken for the call to have been evaluated that way). But look at what the code
does when `halts` returns `True`: it enters `while True: pass` and **never halts**. So it does not
halt. Contradiction.

**Case 2 — suppose it does not halt.** Then `halts(paradox, paradox)` returned `False`. But when
`halts` returns `False`, the function immediately hits `return` and **halts**. So it does halt.
Contradiction.

Both cases are contradictory, and they are exhaustive — `paradox(paradox)` either halts or it does
not, there is no third option. The only assumption we made was that `halts` exists.

Therefore **`halts` does not exist**. HALT is undecidable. ∎

### What the proof actually did

It did not find a hard program that `halts` gets wrong. It showed that the *existence* of `halts`
lets you construct a program on which `halts` must be wrong. The construction is the proof.

The engine is **self-reference**: a program taking its own description as input. That is available
only because Turing showed (L34, §5) that a machine can be encoded as data. Universality is not a
convenience here — it is the mechanism.

> **Note on the framing.** Some texts phrase this as "run `halts` on `paradox`" and stop. That is
> incomplete: the contradiction requires feeding `paradox` **itself**, so that the question `halts`
> is answering and the behaviour `paradox` exhibits are about the same computation. Self-application
> is the load-bearing step.

---

## 4. Diagonalization: The Same Proof, Seen Whole

The `paradox` argument is Cantor's **diagonalization** in disguise, and seeing it that way explains
*why* it works rather than just that it does.

Programs are finite strings over a finite alphabet, so they can be **enumerated**: P₀, P₁, P₂, …
Every program appears somewhere in the list. Inputs can be numbered too.

Build an infinite table where T[i][j] = 1 if program Pᵢ halts on input j, else 0.

A concrete finite corner of it:

|  | j=0 | j=1 | j=2 | j=3 | (behaviour) |
|---|---|---|---|---|---|
| **P₀** | **1** | 1 | 1 | 1 | halts on everything |
| **P₁** | 0 | **0** | 0 | 0 | halts on nothing |
| **P₂** | 1 | 0 | **1** | 0 | halts iff input is even |
| **P₃** | 0 | 1 | 0 | **1** | halts iff input is odd |

Read the **diagonal** — T[0][0], T[1][1], T[2][2], T[3][3] — bolded above: `1, 0, 1, 1`.

Now define a new program D that **flips the diagonal**:

> D(j) = loop forever if T[j][j] = 1, else halt.

D's halting behaviour is `0, 1, 0, 0` — the complement. So:

- D differs from P₀ on input 0 (P₀ halts, D does not)
- D differs from P₁ on input 1 (P₁ does not halt, D does)
- D differs from P₂ on input 2, from P₃ on input 3, …
- **D differs from Pᵢ on input i, for every i.**

So D is not in the list. But the list contains *every* program, and D is a program — we just
described it in one line. Contradiction.

The escape hatch is the assumption that let us build D: computing T[j][j] requires deciding whether
Pⱼ halts on j. **That** is what cannot exist. D is exactly `paradox`, written as a table.

This is the same argument Cantor used in 1891 to prove the reals are uncountable, and Gödel used in
1931 for the incompleteness theorems. Turing's contribution was seeing that it applies to *machines*.

### A counting sanity check

There are **countably many** programs — each is a finite string, and finite strings over a finite
alphabet can be listed. But there are **uncountably many** languages over {0,1} (a language is an
arbitrary subset of all strings, and the set of subsets of a countable set is uncountable, again by
diagonalization).

Countably many programs, uncountably many problems. **Almost every problem is undecidable**, purely
by counting. The halting problem is not a freak — it is a named member of the overwhelming majority.
What is remarkable is that we can decide *anything*.

---

## 5. Recognisable but Not Decidable

HALT is undecidable. But it **is** recognisable, and the machine is one you could write today:

```python
def recognise_halt(f, x):
    """Accepts iff f(x) halts. Runs forever iff it doesn't."""
    f(x)          # just... run it
    return True   # only reached if f(x) finished
```

If `f(x)` halts, this returns `True` — correct. If `f(x)` runs forever, this runs forever — it never
gives a wrong answer, it just never gives one. That is exactly semi-decidability.

**So the yes-instances are confirmable and the no-instances are not.** You can prove a program halts
by running it. You can never conclude it loops forever by running it, no matter how long you wait —
at every moment, "it might finish next step" remains live.

This is the formal shape of a thing you already knew from Week 7: **testing shows the presence of
bugs, never their absence.** Now you know it is not a failure of diligence. It is a theorem.

---

## 6. Why Your Tools Work Anyway

Given all this, how does `gcc -Wall` warn about unreachable code? How does `mypy` check types? How
do linters detect infinite loops?

Because a useful checker needs only **two** of these three properties, and the theorem forbids only
all three at once:

- **Sound** — never reports a bug that isn't there (no false positives)
- **Complete** — reports every bug that is there (no false negatives)
- **Total** — always terminates with an answer

Every real tool drops one, deliberately:

| Tool | Drops | In practice |
|---|---|---|
| `gcc -Wall`, `clang` | completeness | Catches common patterns; misses real bugs silently |
| `mypy`, type checkers | completeness | Unannotated code is simply not checked |
| Termination checkers | totality | Answer is "yes / no / **don't know**" |
| Strict verifiers (Coq, Agda) | completeness | Reject some correct programs; you must prove it |
| An over-eager linter | soundness | Warns about code that is actually fine |

Notice that **"don't know" is a legitimate third answer**, and it is how most static analysis
escapes the theorem. Undecidability forbids a *total* decider; it does not forbid a tool that
solves the easy 95% and says so when it is stuck.

The `-Werror` you have been compiling with all term is an engineering choice sitting directly on top
of this result: the compiler cannot find all your bugs, so you promote the ones it *can* find to
hard failures.

---

## 7. Summary

| Idea | Takeaway |
|---|---|
| Decidable | A TM that **always halts** and always answers correctly |
| Recognisable | Accepts yes-instances; may run forever on no-instances |
| HALT | { ⟨M,w⟩ : M halts on w } — **undecidable** |
| The proof | Assume `halts`; build `paradox`; run it on itself; both cases contradict |
| Engine | Self-reference, available because programs are data (universality) |
| Diagonalization | D flips the diagonal, so D differs from every Pᵢ — yet D is a program |
| Counting | Countably many programs, uncountably many problems ⟹ almost all undecidable |
| HALT is recognisable | Just run it — proves yes, never proves no |
| Testing ⟹ presence, not absence | A theorem, not a discipline problem |
| Sound / complete / total | Pick two; every real analyser drops one on purpose |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Suppose someone claims `halts` exists and hands you an implementation. You run
`paradox(paradox)` and it prints nothing and never returns. What exactly did their `halts` return,
and what does that prove about their implementation?

**2. (Explain.)** A student says: "The halting problem only applies to weird self-referential
programs. My program isn't self-referential, so a checker could handle it." Explain what is right
and what is wrong about this.

**3. (Build.)** Write the recogniser for HALT in Python and explain, precisely, which of the three
properties (sound / complete / total) it has and which it lacks.

**4. (Stretch.)** The **Collatz conjecture** says that repeating "n → n/2 if even, 3n+1 if odd"
reaches 1 from every positive n. Verified past 2⁶⁸; unproven. Explain how a working `halts` would
settle it, and what that tells you about why `halts` cannot exist.

### Answers

**1.** If `paradox(paradox)` ran forever, it entered the `while True: pass` branch, which is reached
**only** when `halts(f, f)` returns `True`. So their `halts` returned `True` — it claimed
`paradox(paradox)` halts.

It did not halt. **Their implementation is wrong on this input**, which is exactly what the theorem
guarantees: whatever they wrote, `paradox` built from it is a counterexample. Had it instead
returned immediately, `halts` would have returned `False` while the program demonstrably halted —
wrong in the other direction. There is no third behaviour, so no implementation survives.

**2. What is right:** self-application really is doing the work in the proof, and it is rare in
practice. Also correct in spirit: for *many specific programs*, termination is easy to establish —
a `for` loop over a fixed list obviously terminates, and tools prove this routinely.

**What is wrong** is the conclusion. The theorem says no **single, general** checker handles all
programs. That is compatible with a checker handling any *particular* program, including every
program the student will ever write. But there are two deeper problems with the student's reasoning:

- **Undecidability is not confined to self-reference.** By §4's counting argument, almost all
  problems are undecidable, and §Thursday shows ordinary questions ("does this program ever print
  `hello`?") are too. `paradox` is how we *prove* the first one, not where the difficulty lives.
- **Termination of innocent-looking programs can be open mathematics.** A three-line Collatz loop
  is not self-referential and nobody knows whether it halts for all inputs (see Ex 4).

So the honest statement is: a checker can handle your program, and cannot handle all programs, and
you cannot tell in advance which category a new program falls into.

**3.**

```python
def recognise_halt(f, x):
    f(x)
    return True
```

- **Sound** — ✅ It returns `True` only after `f(x)` has actually finished, so a `True` answer is
  always correct. It never lies.
- **Complete** — ✅ For *yes*-instances. Every `f, x` where `f(x)` halts will eventually cause this
  to return `True`. (It is not complete in the sense of ever reporting *no* — it has no `False`
  branch at all.)
- **Total** — ❌ **This is what it lacks.** When `f(x)` loops forever, so does the recogniser. It
  never terminates, so it is not a decider.

That single missing property is the entire gap between *recognisable* and *decidable*, and the
theorem says it cannot be closed.

*(A practical caveat worth noting: this also inherits `f`'s side effects and can exhaust the stack
or memory. Those are engineering problems; the totality failure is the mathematical one.)*

**4.** Write:

```python
def collatz_loop(n):
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    return True
```

This halts on input n **exactly when** the Collatz sequence from n reaches 1. So a single call
`halts(collatz_loop, n)` settles the conjecture **for that n** — no running required, and it works
even for an n whose sequence would run past the age of the universe.

The conjecture itself is the infinite conjunction "for **every** n", so one call is not enough. But
`halts` gives it to you in two steps: since `halts` is assumed total, `terminates = lambda n: halts(collatz_loop, n)`
is a total, computable test, and

```python
def collatz_search():
    n = 1
    while halts(collatz_loop, n):   # total test, thanks to the assumption
        n += 1
    return n                        # the first counterexample
```

halts **iff a counterexample exists**, i.e. iff Collatz is **false**. One more call —
`halts(collatz_search, None)` — returns the answer.

> **Why the second step is needed.** You cannot write `collatz_search` without `halts`. Being a
> counterexample means the sequence *never* reaches 1, and no finite computation confirms "never" —
> running the loop can establish that n is fine, never that it isn't. So the counterexample test is
> not itself decidable; it becomes decidable only because we assumed `halts`. Contrast **Goldbach**
> ("every even n > 2 is a sum of two primes"), where a counterexample *is* finitely checkable —
> just try all p < n/2, a loop that always terminates. There, `goldbach_search` needs no `halts` at
> all, and `halts(goldbach_search, None)` settles it in a single call.

**What this tells you:** `halts` would be a universal mathematics machine. Any conjecture of the
form "no counterexample exists" — Goldbach, twin primes, and with the extra step above, Collatz —
reduces to a termination question by writing a program that searches for a counterexample and halts
when it finds one.

If `halts` existed, all of them would fall out of a function call. That it does not exist is, in
hindsight, not surprising at all. (Verified for individual values: collatz(27) halts after 111
steps, collatz(97) after 118, collatz(871) after 178 — the *general* claim is what is open.)

---

## Reading

- **Sipser, Ch. 4.2** — the halting problem and diagonalization (primary)
- **Sipser, Ch. 4.1** — decidable languages, for §1
- **Turing (1936), §8** — the original argument, in Turing's own framing
- **Hofstadter, *Gödel, Escher, Bach*, Ch. XIII** — optional; self-reference as a unifying theme

---

*CS 101 · Week 11 · Lecture 35 (Thu) · © CSE Department*
