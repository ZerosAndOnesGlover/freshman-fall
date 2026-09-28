# PROG 202 · Problem Set 3 · Solutions
## Laziness: Thunks, WHNF, Space Leaks, and Infinite Lists
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Released:** Week 3 Wednesday · **Due:** Week 4 Friday 17:00 · **100 points** · **15 parts, ~3 hours**

**What this paper is testing.** Whether *weak head normal form* has become a working tool rather than a
phrase. Q1 defines it, Q2 charges 727 MB for not knowing it, Q3 makes them explain three measurements
they took on trust in Week 2, Q4 is Hughes, and **Q5(b) is the question that decides whether they will
write a leak next year** — it is the case `-O2` does not repair.

**Timing:** Q1 30 min, Q2 45 min, Q3 25 min, Q4 40 min, Q5 40 min.

**Allow ±5% on residency; the 44,328-byte figure should be exact.** Timings ±15%.

---

## Q1: Weak Head Normal Form (20)

### (a) [8]

```
p = (_,_)
()
p = (_,_)          <- the marked one
2
p = (2,_)
()
xs = _ : _
()
j = Just _
```

[1 per line, 8 total.] **The second `:sprint p` is the one they get wrong** and it is worth 2 of the 8.

**The definition wanted:** *a value is in weak head normal form when its **outermost constructor** is
known.* `(1+1, 2+2)` has a known outermost constructor — the pair — from the moment it is written, so
`seq` has no work to do. **Do not accept "seq evaluates one level"** without "outermost constructor"; the
vaguer phrasing is what produces the 727 MB in Q2.

### (b) [6]

| | | why |
|---|---|---|
| 1. `seq undefined ()` | **throws** | ⊥ has no outermost constructor; reaching WHNF *is* the failing evaluation |
| 2. `seq (undefined, 2) ()` | **succeeds** | the pair constructor is known without either field |
| 3. `seq (1 : undefined) ()` | **succeeds** | `(:)` is the outermost constructor |
| 4. `deepseq (1, undefined) ()` | **throws** | `deepseq` reaches normal form, so it enters both fields |
| 5. `seq (Acc undefined 3) ()` | **throws** | — |

[1 each.]

**Number 5 [1 of the 6 is for the explanation]:** a **strict field forces its argument when the
constructor is applied**, so `Acc undefined 3` cannot be constructed at all — its WHNF is ⊥. In 2 the
pair's WHNF is reachable without its fields; in 5 the constructor's own strictness makes it not.
**That is the entire reason strict fields exist**, and Lab 3 §3c is it being useful.

### (c) [6]

- **`length` forces the spine and never the elements** (W0 L02 §4), so the three thunks are counted and
  never entered. An error that is never demanded does not happen. [2]
- **Something that throws:** `sum [x, x, x]`, `print x`, `x `seq` ()`, `head [x]`. [2]
- **Throws at `-O0` and not `-O2`, or an argument that none exists [2].** No expected answer. The honest
  position, and full marks for it: **it is the wrong way round.** `-O2`'s strictness analysis makes GHC
  force things *earlier*, so the realistic asymmetry is an expression that throws at `-O2` and not at
  `-O0` — e.g. a `foldl` whose accumulator contains an `error` in a branch the final answer does not
  need. Give full marks for a student who reasons to that and reports that they could not produce the
  direction the question asked for; give full marks also for one who produces either direction with
  evidence. **Deduct only for an unsupported assertion.**

---

## Q2: The Leak (22)

### (a) [10]

| | `-O0` allocated | `-O0` residency | `-O2` allocated | `-O2` residency |
|---|---:|---:|---:|---:|
| `two` | 880,110,352 | **244,955,536** | 720,109,696 | **289,026,592** |
| `lazy` | 2,505,464,496 | **726,571,008** | 160,109,640 | **44,328** |
| `bang` | 1,840,142,944 | 60,280 | 160,109,576 | 44,328 |
| `strict` | 1,280,143,312 | 60,272 | **109,944** | **44,328** |

[7 for the sixteen cells.]

- **The `lazy` sentence [1]:** *`foldl'` forces its accumulator to weak head normal form, and the
  accumulator is a pair — so each step confirms the pair constructor and leaves both components as
  thunks.*
- **The `two` row [1]: retention.** `xs` is named and two traversals need it, so evaluated cells stay
  *reachable*. **No `seq` can fix it because nothing is unevaluated** — the problem is reachability, not
  laziness.
- **Where the 160 MB went [1]:** into **the pairs themselves.** `bang` still allocates a fresh
  `(Int, Int)` tuple per element — plus two boxed `Int`s — and only the *thunks* were removed.
  `data Acc = Acc !Int !Int` lets GHC unbox the fields and keep the whole accumulator in registers, so
  there is nothing to allocate at all: **110 KB total.**

### (b) [6]

- **No, it is not gone. [2]** The 44 KB is an optimisation GHC is permitted to make, not part of the
  program's meaning; the `-O0` column is the proof. A small change — an accumulator only conditionally
  demanded — defeats the analysis at any level and looks identical.
- **Strictness analysis.** [1]
- **The code-review sentence [3].** Anything with force. The best ones:
  *"This is correct only because the optimiser noticed something; write the strictness down so the next
  reader doesn't have to check `-ddump-simpl`."* Or: *"It is 727 MB at `-O0`, and `-O0` is what our test
  suite builds with."* Or: *"`Data.Map.Lazy` is the same bug and `-O2` does not fix that one"* — which is
  Q5(b) and is the strongest answer available.

### (c) [6]

| | residency | time |
|---|---:|---:|
| bang-pattern fix, `./stats lazy` | 234,075,256 | 1.510 s |
| bang-pattern fix, `./stats strict` | **44,328** | 0.028 s |
| strict-fields fix, `./stats lazy` | **44,328** | 0.027 s |
| strict-fields fix, `./stats strict` | 44,328 | 0.027 s |

[3 for the four numbers. The third row is the marked one.]

- **A strict field forces its argument when the constructor is applied** [2], so every `Stats a b c d e`
  anywhere in the program is strict — including the `step` nobody edited. The strictness moved from the
  call site to the type.
- **Where bangs are the only option [1]:** **when you do not own the type.** A library's type, a
  generated module, or a type another module relies on being lazy. `Data.Map.Lazy` is the canonical
  case, which is Q5(b).

---

## Q3: Folds, Explained (18)

### (a) [7]

**After three steps at `-O0`:** the accumulator is the unevaluated `((0 + 1) + 2) + 3` — a chain of three
thunks, each pointing at the previous. [3]

**Strictness analysis** [2]. **What it proves:** *if this function's result is demanded, then this
argument is certainly demanded too.* For `foldl (+)` that holds — the final `print` forces the
accumulator, which forces the last `+`, which forces its left argument, transitively to the start — so
GHC may evaluate as it goes without changing the program's meaning.

**`foldl'` is 44 KB at both levels [2]** because it contains an explicit `seq`: the strictness is in the
program, not in an optimisation, so nothing has to be proved.

### (b) [6]

`foldr (+) 0 [1,2,3]` = `1 + (2 + (3 + 0))`. [1]

**Why the whole structure must exist first [2]:** to compute the outermost `+` you need its right
operand, which is another `+`, whose right operand is another — so the recursion descends to the end of
the list **before any addition can be performed.** At ten million elements that is ten million suspended
applications, and this time they are on the **evaluation stack** rather than in a thunk chain.

**Same problem as (a)? [3] — No.** Both are "too much pending work", and what is held differs:

| | what is held | why `-O2` can/cannot help |
|---|---|---|
| `foldl` | a **thunk chain in the heap**, one link per element | **Can:** the accumulator is provably demanded, so force it as you go |
| `foldr` | the **stack of suspended `+` frames**, one per element | **Cannot:** the recursion genuinely must reach the end before the first addition. The order of work is the problem |

**Full marks require "no" plus the distinction.** A student who says "yes, both are laziness" has the
week's main confusion.

### (c) [5]

- `foldr`: the **first** element — `f x₁ (foldr f z rest)`. `foldl`: the **last**. [2]
- **Hence:** an operator that ignores its second argument stops `foldr` immediately, and `foldl` cannot
  produce anything before reaching an end the list does not have. [2]
- **`<<loop>>` [1]** because `repeat False` is a **cyclic** structure — the RTS blackholes a thunk while
  evaluating it, and the fold re-enters the very thunk it is inside. Week 0 L01 §1. *Blackholing detects
  self-reference, not non-termination, and here the self-reference is real.*

---

## Q4: Infinite Lists (20)

### (a) [7]

The trace [3] — accept any correct form; the marked content is that at each step `zipWith` consumes cells
**already produced**:

```
fibs           = 0 : 1 : zipWith (+) fibs (tail fibs)
have            0 : 1 : …          tail fibs = 1 : …
zipWith gives  (0+1) : …           = 1 : …
fibs           = 0 : 1 : 1 : …     now zipWith has (1, 1)
…              = 0 : 1 : 1 : 2 : 3 : …
```

**`bad` [2]:** not **productive** — its outermost cons is unavailable until `zipWith` produces one, and
`zipWith` needs the outermost cons. `<<loop>>`, measured.

**The recursive function [2]:** `fib n = fib (n-1) + fib (n-2)` is **O(φⁿ)** because nothing is shared;
the list version is **O(n)** additions on `Integer` because each cell is computed once and remembered.
**That sharing is the `let`-bound sharing of L02 §2, and it is guaranteed, not an optimisation.**

### (b) [7]

```
within   1e-12 (sqrts 2)    = 1.414213562373095
relative 1e-12 (sqrts 2)    = 1.414213562373095
sqrt 2 (Prelude)            = 1.4142135623730951
within   1e-12 (sqrts 1e20) = 1.0e10
relative 1e-12 (sqrts 1e20) = 1.0e10
```
[2]

**Why the absolute rule succeeds at 1e20 [2]:** Newton reaches an **exact `Double` fixed point** and then
repeats. `take 12 (drop 30 (sqrts 1e20))` ends in `1.0e10` repeated, and `s !! 40 == s !! 41` is `True`
— measured. So `abs (a - b)` is exactly `0`.

**Accept nothing that appeals to Newton's convergence rate**; the point is that floating-point
iteration stops moving, which is a property of `Double`, and it is why "consecutive values are equal" is
a *different* test from "consecutive values are close".

**The counter-example [3]:** any sequence converging without reaching a fixed point. The clean one:

```haskell
slow = [ 1e12 * (1 + 1 / fromIntegral k) | k <- [1 :: Int ..] ]
```

Successive terms differ by ≈ `1e12/k²`, so the absolute test needs `k > 10¹²` — about a trillion steps.
**`relative 1e-12 slow = 1.0000010001250157e12`**, measured, immediately.

### (c) [6]

| *n* | naive | real |
|---:|---:|---:|
| 2,000 | 0.07 s | 0.02 s |
| 10,000 | 1.51 s | 0.08 s |
| 20,000 | *(theirs)* | *(theirs)* |

[3 for six timings.] Both print `17393` at 2,000 and `104743` at 10,000.

- **A real sieve crosses off multiples by repeated *addition* and never divides** [2]. The two-liner is
  dominated by **`mod`**, testing each survivor against every prime so far — Θ(n²/log n) — against the
  sieve's Θ(n log log n) **additions**.
- **The estimate [1]:** from 1.51 s at 10,000 and a roughly quadratic fit, a minute is around
  *n* ≈ 60,000–70,000. Accept anything in that region with the fit shown.

---

## Q5: `sched` Under a Microscope (20)

### (a) [7]

A mean needs a sum and a count. **`nMinutes` and `nSessions` are already both fields**, so the mean is
computed at the *end*, from two strict `Int`s, and there is no new accumulator at all:

```haskell
meanDuration :: Stats -> Double
meanDuration s = fromIntegral (nMinutes s) / fromIntegral (nSessions s)
```

[4 for a version that stays in constant space; 3 for the explanation.]

**Why this is not the `lazyPair` bug:** the pair in Q2 was *the accumulator*, forced only to WHNF ten
million times. Here nothing is accumulated for the mean — it is one division on two numbers that are
already strict fields. **A student who instead added a `(Int, Int)` field to `Stats` has reproduced the
bug exactly**, and the marks are for noticing and reporting both numbers.

**Before and after should be identical**: 44,328 bytes, ~0.027 s.

### (b) [7]

```haskell
histS = MS.toList . foldl' (\m t -> MS.insertWith (+) (day t) (duration t) m) MS.empty
histL = ML.toList . foldl' (\m t -> ML.insertWith (+) (day t) (duration t) m) ML.empty
```

**Measured at `-O2`, `stream 100000` (1.7 million sessions):**

| | maximum residency | time |
|---|---:|---:|
| `Data.Map.Strict` | **44,328 B** | 0.060 s |
| `Data.Map.Lazy` | **107,201,136 B** | 0.752 s |

[4 for the two numbers, 3 for the explanation.]

Both print `[(Mon,175000),(Tue,285000),(Wed,260000),(Thu,175000),(Fri,175000)]`.

**This is the most important result on the paper.** `-O2` repaired the lazy *pair* in Q2 and **does not
repair this** — the thunks are values inside a balanced tree, and the strictness analyser cannot see
through a data structure to prove that every value in it will be demanded.

**So: use `Data.Map.Strict` for a counter**, because `insertWith (+)` on a lazy map stores the *unapplied
addition* as the new value, and five keys times 340,000 updates each is five 340,000-link chains. In WHNF
terms: `insertWith` forces the *map* to WHNF — the tree node — and never the value inside it. **Exactly
Q1(a)'s pair, one level deeper, and out of the optimiser's reach.**

**Full marks require the appeal to WHNF.** "Strict is faster" is 1 mark.

### (c) [6]

- **The one-sentence warning [3].** Mark the content, not the prose. It must name the mechanism, not just
  the symptom. Good: *"Every accumulator in the statistics code must be strict in its fields — `foldl'`
  only forces the outermost constructor, so a lazy field builds one thunk per input element; see the
  `!`s in `Stats`."* Bad: *"Careful, this can use a lot of memory."*
- **Which figure for CI [3]: maximum residency.** It is the one that determines whether the program fits
  in the machine, it is roughly deterministic for a given input, and **it is the one that catches a
  retention bug.** *Bytes allocated* is a churn figure — high allocation with low residency is normal and
  fast, because GHC's nursery is a bump allocator — so a threshold on it would fire on healthy code and
  miss the leak. Accept a threshold expressed as a constant (e.g. "under 2 MB for any *n*"), and give
  extra credit for noting that the useful check is that residency is **independent of input size**, which
  is exactly what distinguishes 44 KB from 234 MB.

---

## Marks

| Q | Topic | Parts | Points |
|---|---|---:|---:|
| 1 | Weak head normal form | 3 | 20 |
| 2 | The leak | 3 | 22 |
| 3 | Folds, explained | 3 | 18 |
| 4 | Infinite lists | 3 | 20 |
| 5 | `sched` under a microscope | 3 | 20 |
| | **Total** | **15** | **100** |

---

## What to Watch For Across the Cohort

1. **Q1(a)'s second `:sprint p` predicted as `(2,4)`.** Expected, and fine — the marks reward the
   prediction. What matters is whether their *definition* of WHNF then explains it. If the definition
   still says "one level" rather than "outermost constructor", fix it in the tutorial.
2. **Q3(b) answered "yes, same problem".** The `foldl`/`foldr` distinction — heap chain against
   evaluation stack — is on the midterm, which is two weeks away.
3. **Q2(b) answered "it doesn't matter at `-O2`".** Point them at their own Q5(b), which is the
   counter-example, and note that the midterm covers Weeks 0–5.
4. **Q5(b) answered "strict is faster".** They have the result and not the mechanism, and the mechanism
   is the one thing from this week that will still be useful to them in another language — `insertWith`
   on a lazy map is `defaultdict` with a closure in it.

---

*PROG 202 · Week 3 · PS 3 Solutions · INSTRUCTOR ONLY · © CSE Department*
