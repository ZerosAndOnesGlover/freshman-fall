# PROG 202 · Lab 3 · Solutions
## Watching Laziness: Thunks, Space Leaks, and `seq`
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Session:** Wednesday of Week 4, 13:00–14:50, BH 215 · **Unmarked**, checked off in the session.

**What the session is really for.** One sentence: **`seq` forces to weak head normal form, and WHNF of a
constructor is the constructor.** Everything else in the lab is that sentence costing money.

**§3c is the session's thesis** and it is not about laziness at all: moving the `!` from the *use site*
into the *type* fixed a function nobody edited. That is the transferable engineering point — make the
invariant a property of the data, not a rule every caller has to remember — and it is the same argument
as Week 1 §5's export list.

**Timing.** §0 8 · §1 18 · §2 18 · §3 25 · §4 20 · §5 12 · checkoff 8 = **109 minutes.** §4 is the one to
cut if behind (PS 3 Q4 covers it); §3 must not be cut.

**Reference solutions:** `StatsSol.hs` (bang patterns) and `StatsFields.hs` (strict fields).

---

## §1 — `:sprint`

```
ghci> let p = (1+1, 2+2) :: (Int, Int)
ghci> :sprint p
p = (_,_)
ghci> p `seq` ()
()
ghci> :sprint p
p = (_,_)          <- seq did nothing
ghci> fst p
2
ghci> :sprint p
p = (2,_)
```

```
ghci> let xs = map (*2) [1..5] :: [Int]
ghci> xs `seq` ()
ghci> :sprint xs
xs = _ : _         <- one cell, head and tail both thunks
```

```
ghci> import Control.DeepSeq
ghci> let q = (1+1, 2+2) :: (Int, Int)
ghci> q `deepseq` ()
ghci> :sprint q
q = (2,4)
```

**The sentence to extract, and do not accept a paraphrase that omits "outermost":** *`p` was already in
weak head normal form — its outermost constructor was known the moment it was written — so `seq` had
nothing to do and never touched the components.*

**Answers.**

1. **`seq (undefined, 2) ()` succeeds** because the pair constructor is known without evaluating either
   field. **`seq undefined ()` throws** because `undefined` has no outermost constructor at all — it is
   ⊥, and reaching WHNF *is* the evaluation that fails. Consistent: both force to WHNF, and only one of
   them has one.
2. **`length` forces the spine and never the elements** (Week 0 L02 §4). The three `x`s are thunks that
   are counted and never entered, so the `error` is a value that is never demanded.
3. **`seq (Acc undefined 3) ()` throws** — measured. This is the one that surprises them, and it is the
   right surprise: a **strict field forces on construction**, so `Acc undefined 3` cannot be built
   without evaluating `undefined`, and the WHNF of that expression is ⊥. **Contrast with 2:** a plain
   pair's WHNF is reachable without its fields; a strict constructor's is not.

   **This is why §3c works**, and it is worth saying now rather than in §3.

---

## §2 — Reproducing the 727 MB

| | `-O0` allocated | `-O0` residency | `-O2` allocated | `-O2` residency |
|---|---:|---:|---:|---:|
| `two` | 880,110,352 | **244,955,536** | 720,109,696 | **289,026,592** |
| `lazy` | 2,505,464,496 | **726,571,008** | 160,109,640 | **44,328** |
| `bang` | 1,840,142,944 | 60,280 | 160,109,576 | 44,328 |
| `strict` | 1,280,143,312 | 60,272 | **109,944** | **44,328** |

**(a)** *`foldl'` forces its accumulator to weak head normal form, and the accumulator is a pair — so
each step confirms the pair constructor and leaves both components as thunks, building two
ten-million-link chains.*

**(b) Retention**, not strictness. `xs` is named and two traversals need it, so every cell between
`sum`'s cursor and the front stays reachable. **`seq` cannot help because nothing is un-evaluated** —
the problem is that evaluated data is still *reachable*. Only restructuring to one pass removes it, which
is what the other three rows are.

**Note the `-O2` figure is worse than `-O0`** (289 vs 245 MB). Do not over-explain; the honest answer is
that fusion changes the allocation pattern and the collector's high-water mark moves with it. What
matters is that it did not *improve*.

**(c)** **No, the bug is not gone.** Two sentences wanted: the 44 KB is **strictness analysis**, which
is an optimisation GHC is permitted to make and not a guarantee the language gives — the `-O0` column is
the proof that the program's meaning does not include it. And a small change (an accumulator that is
only conditionally demanded) defeats the analysis at any level while looking identical.

**Listen for "so it doesn't matter at `-O2`".** That is the belief §3 exists to break, and Q5(b) of PS 3
breaks it with `Data.Map.Lazy`, which `-O2` does **not** repair.

---

## §3 — The Leak in `Stats.hs`

### 3a

**Five chains, each ten million... no — 1.7 million long**, one per field. Accept "five, one per field,
each as long as the input". The students who say "one chain" have not noticed that `Stats` has five
independent fields.

### 3b

```haskell
stepStrict s t =
  let !a = nSessions s + 1
      !b = nMinutes s + duration t
      !c = nLectures s + (if kind t == LEC then 1 else 0)
      !d = nLabs s + (if kind t == LAB then 1 else 0)
      !e = max (longest s) (duration t)
  in Stats a b c d e
```

```
lazy     234,075,256 bytes maximum residency   1.510 s
strict          44,328 bytes maximum residency   0.028 s
```

**5,280× the memory and 54× the time, for five characters.** Both print
`sessions=1700000 minutes=107000000 lectures=1300000 labs=200000 longest=110`.

**Accept `seq` by hand instead of bangs**, and accept `$!`. A student who writes
`Stats $! a $! b …` has the right idea and the wrong operator precedence; let them find out.

### 3c — the section that matters

```haskell
data Stats = Stats
  { nSessions :: !Int
  , nMinutes  :: !Int
  , nLectures :: !Int
  , nLabs     :: !Int
  , longest   :: !Int
  }
```

```
lazy     44,328 bytes maximum residency   0.027 s
strict   44,328 bytes maximum residency   0.027 s
```

**`step` was not edited and is now strict.** Put both numbers on the board before they run it, and ask
them to predict the `lazy` row. Most will say 234 MB.

**Answers.**

1. **A strict field forces its argument when the constructor is applied.** `Stats a b c d e` now
   evaluates all five before allocating, so every construction anywhere in the program — including in
   `step`, which nobody touched — is strict. **The strictness became a property of the type rather than
   of the call site.** *(This is §1 answer 3 cashing out.)*
2. No expected answer; the good ones say **the type**, because it cannot be forgotten, cannot be
   inconsistent between two constructions, and is visible in the declaration a reader is most likely to
   look at. Accept a defence of the bang-pattern version on the grounds that it is local and does not
   change a shared type.
3. **When you do not own the type** — it comes from a library, or from a generated module, or another
   module depends on its laziness. **`Data.Map.Lazy` is the canonical case**: you cannot add `!` to
   someone else's `Map`, so the fix has to be at the use site (or you switch to `Data.Map.Strict`, which
   is the same fix made by whoever did own the type). PS 3 Q5(b) is this.

---

## §4 — Infinite Lists

### 4a

`take 3 fibs` = `[0,1,1]`. `take 3 bad` = **`<<loop>>`**.

**The sentence:** *`fibs` is **productive** — forcing its first cell requires only the literal `0 :`, so
`zipWith` always has cells already produced to work with. `bad`'s outermost cons is not available until
`zipWith` has produced something, and `zipWith` needs `bad`'s outermost cons.*

### 4b

```
within   1e-12 (sqrts 2)    = 1.414213562373095
relative 1e-12 (sqrts 2)    = 1.414213562373095
sqrt 2 (Prelude)            = 1.4142135623730951
relative 1e-12 (sqrts 1e20) = 1.0e10
within   1e-12 (sqrts 1e20) = 1.0e10
```

**Both rules succeed on `1e20`, and the absolute one has no business doing so.** The reason is a
`Double` fact, not a Newton fact: the iteration reaches an **exact fixed point** and then repeats
forever. Measured — `s !! 40 == s !! 41` is `True`, and printing `take 12 (drop 30 (sqrts 1e20))` shows
`1.0e10` five times in a row. So `abs (a - b)` is exactly `0`, and `0 <= 1e-12`.

**The genuine counter-example** they are asked to construct needs a sequence that converges *without*
reaching a fixed point. The cleanest:

```haskell
slow :: [Double]
slow = [ 1e12 * (1 + 1 / fromIntegral k) | k <- [1 :: Int ..] ]
```

Consecutive terms differ by about `1e12 / k²`, so the absolute test needs `k > 10¹²` — about a trillion
steps, i.e. never. **`relative 1e-12 slow` returns `1.0000010001250157e12`** in no time. Accept anything
with this shape.

**And the point:** *you did not edit `sqrts`.* In a language where the loop owns the convergence test you
would have edited the algorithm to change the stopping rule, and you would have two copies of Newton's
method the first time you needed two rules.

### 4c

`head [...]` gives `(3,4,5)`. **With `last` it never terminates**, because `last` must reach the end of a
list that has none. **The consumer controls termination** — the generator has no opinion, and that is
both the feature and the hazard.

---

## §5 — The Sieve

```
naive  2000: 0.07 s      real  2000: 0.02 s
naive 10000: 1.51 s      real 10000: 0.08 s
```

Both print `17393` and `104743`.

1. **A real sieve crosses off multiples by repeated *addition* and never divides.** The two-liner tests
   every survivor against every prime found so far: Θ(n²/log n) divisions against Θ(n log log n)
   additions.
2. **Nothing in two lines of list comprehension tells you the cost.** Laziness lets you write a
   generator whose complexity is a property of how it is consumed and of what the comprehension does per
   element, neither of which is visible in its shape. **Same answer as §2(b) and §3, third costume** —
   and that repetition is the lab's design, not an accident.

---

## Checkoff

Six items. **Be strict about two:**

- §1's `(_,_)` after `seq` must come with a *spoken* explanation containing the word "outermost".
- §3c must be **demonstrated with `step` unedited**. A student who edited `step` as well has done the
  work and missed the point; make them revert it and re-run.

---

## After the Session

**PS 3 is due the Friday of Week 4.** It repeats §2, §3 and §5 with marks, and **Q5(b) is the one to warn
them about**: `Data.Map.Lazy` as a counter leaks **107 MB at `-O2`** where `Data.Map.Strict` holds 44 KB.
That is the case `-O2` does **not** repair, because the thunks are inside a structure the analyser cannot
see through — and it is the argument for §3c generalised to a library.

**Quiz 4 is the Tuesday of Week 4** and covers this week.

**Week 4 is type classes**, and it finally answers `:t 3`. Tell them that `Foldable t =>` in every `:t`
output for three weeks is about to make sense.

---

*PROG 202 · Week 3 · Lab 3 Solutions · INSTRUCTOR ONLY · © CSE Department*
