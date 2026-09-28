# PROG 202 · Problem Set 2 · Solutions
## Higher-Order Functions, Folds, and What They Cost
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Released:** Week 2 Wednesday · **Due:** Week 3 Friday 17:00 · **100 points** · **15 parts, ~3 hours**

**What this paper is testing.** Q1 is type-reading and it should be quick. Q2 is the mechanics of folds
and carries the most marks. **Q3 and Q4 are measurements and they are the paper** — 42 of the 100 marks
depend on numbers off their own machine, and a student who has not run anything cannot fake Q3(a)'s
eight cells or Q4(c)'s ratios. Q5 is `sched`.

**Timing:** Q1 25 min, Q2 45 min, Q3 40 min, Q4 40 min, Q5 30 min.

**Allow ±15% on timings** and ±5% on residency; the 44,328-byte figure should be exact.

---

## Q1: Reading Higher-Order Types (18)

### (a) [7]

| Expression | Type |
|---|---|
| `map map` | `[a -> b] -> [[a] -> [b]]` |
| `zipWith const` | `[c] -> [b] -> [c]` |
| `uncurry (+)` | `Num c => (c, c) -> c` |
| `filter . (==)` | `Eq a => a -> [a] -> [a]` |
| `(.) . (.)` | `(b -> c) -> (a1 -> a2 -> b) -> a1 -> a2 -> c` |

[1 each, 2 for the "useful" judgement.]

**The two useful ones are `uncurry (+)` and `filter . (==)`.** `uncurry (+)` is what you hand to
`map` after a `zip`; `filter . (==) x` keeps the elements equal to `x`, which is a real if
unmemorable thing to want.

**`zipWith const` is `take`-to-the-length-of-the-second-list**, which is a cute trick and not
something to write. **`(.) . (.)` composes a one-argument function onto a two-argument one** and is
the canonical example of a point-free expression nobody should commit — worth saying so, since L05 §4
makes the same point with prose.

**`map map` catches people:** `map` has two arguments, so `map map` is `map` *partially applied to
`map`*, i.e. a function taking a **list of functions** and giving a list of functions.

### (b) [5]

- `add :: Int -> (Int -> Int)`. [1]
- `add 3 :: Int -> Int`; `add 3 4 :: Int`. [1]
- **`map (add 3)` needs no lambda because `add 3` already *is* a one-argument function** — `add` never
  took two arguments; `->` is right-associative and application is left-associative, so `add 3 4` is
  `(add 3) 4`. [2] **Require the words "returns a function" or an equivalent.**
- Something of type `[Int] -> [Int]` adding 3, without `add`, a lambda or a helper: **`map (+ 3)`**. [1]
  *(`map (3 +)` is equally fine.)*

### (c) [6]

- **`(- 1) :: Num a => a`.** It is **negative one**, not a section. [2]
- `map (- 1) [1,2,3]` **does not compile**: it tries to use the number −1 as a function. Measured: [1]

  ```
  neg2.hs:2:20: error:
      • No instance for (Num (Int -> b0))
  ```

  *Accept any report of a `Num (… -> …)` error; the exact wording shifts with the numeric context and
  a second "ambiguous type variable" error usually comes with it.*
- Two correct ways: **`subtract 1`** and **`(+ (-1))`**. Also accept `(\x -> x - 1)` if they note it is
  a lambda, and `flip (-) 1`. [2]
- **The irregularity:** `-` is the only symbol that is both a binary operator and a prefix negation, so
  `(- x)` is parsed as negation and cannot be a left section. Every other operator has a working left
  section. [1]

---

## Q2: Writing Folds (22)

### (a) [8]

```haskell
myMap    f = foldr (\x acc -> f x : acc) []
myFilter p = foldr (\x acc -> if p x then x : acc else acc) []
myLength   = foldr (\_ n -> 1 + n) 0
myReverse  = foldr (\x acc -> acc ++ [x]) []      -- O(n^2)
myReverse' = foldl' (flip (:)) []                 -- O(n)
```

[4 for the four `foldr`s, 1 for the `foldl'` reverse.]

**The measurement [3], and it is the point of the question:**

| *n* | `foldr` version | `foldl'` version |
|---:|---:|---:|
| 20,000 | **5.10 s** | 0.01 s |
| 40,000 | **25.30 s** | 0.01 s |

**Ratio 4.96 for a doubling — quadratic.** Full marks require identifying the `foldr` version as the
quadratic one **before** measuring, and the reason: `acc ++ [x]` re-walks everything built so far
(L06 §5).

> **Worth a remark on every script: this is Hutton §7.3's own `reverse`.** The textbook presents it as
> the illustrative `foldr`, and it is a performance bug. That is not a criticism of the book — it is
> illustrating `foldr`, not writing a library — but a student who copied it into real code would have
> shipped this.

### (b) [8]

```
foldr (-) 0 [1,2,3] = 1 - (2 - (3 - 0)) = 1 - (2 - 3) = 1 - (-1) = 2
foldl (-) 0 [1,2,3] = ((0 - 1) - 2) - 3 = (-1 - 2) - 3 = -3 - 3   = -6
foldr (:) [] [1,2,3] = 1 : (2 : (3 : [])) = [1,2,3]
foldl (flip (:)) [] [1,2,3] = [3,2,1]
```

[1 each, and **require the steps** for the first two.] The fourth **is `reverse`**, and a student who
names it gets the credit for noticing.

**The universal property [4]:**

- **`foldr (:) [] = id`**: `id [] = []` and `id (x:xs) = x : id xs`, which is the shape with `f = (:)`
  and `z = []`. So by the universal property `id = foldr (:) []`. [2]
- **`sum . map (* 2)` as one `foldr`**: `foldr (\x acc -> 2 * x + acc) 0`. [2] Accept
  `foldr ((+) . (* 2)) 0`, which is the same thing and shows they have read §7.5.

**The general law being used** is `foldr f z . map g = foldr (f . g) z`. A student who states it gets
the marks without the worked example.

### (c) [6]

- **`foldr` is right because its outermost application is the *first* element** — `x1 && (rest)` — and
  `(&&)` ignores its second argument when the first is `False`, so the rest is never examined. [2]
- **Measured:** [2]

  ```
  foldr   False
  foldl   andr: <<loop>>
  foldl'  andr: <<loop>>
  ```

  **Not a hang — `<<loop>>`**, the RTS's blackhole detection from Week 0 L01 §1, because `repeat False`
  is a cyclic structure and the fold re-enters the thunk it is already inside. **Full marks require
  `<<loop>>`**; a student who wrote "hangs" did not run it.
- **An operator where `foldl'` is right and `foldr` is a mistake:** `(+)`, `(*)`, `max`, or any operator
  strict in both arguments. [2] `foldr (+) 0` on ten million elements is the 130 MB row; it cannot
  short-circuit because `+` always needs both sides, so all it does is build the pending chain from the
  wrong end.

---

## Q3: Measuring the Folds (22)

### (a) [10]

| | `-O2` residency | `-O2` time | `-O0` residency | `-O0` time |
|---|---:|---:|---:|---:|
| `foldr (+) 0` | 130,050,736 B | 0.359 s | 446,144,352 B | 1.646 s |
| `foldl (+) 0` | **44,328 B** | 0.004 s | **619,453,488 B** | 3.277 s |
| `foldl' (+) 0` | 44,328 B | 0.004 s | 44,328 B | 0.106 s |
| `sum` | 44,328 B | 0.007 s | 44,328 B | 0.112 s |

[6 for the eight residency/time pairs; allow ±5% on the megabyte figures.]

- **The two rankings [2]:** at `-O2`, `foldl` ≈ `foldl'` ≈ `sum` ≪ `foldr`. At `-O0`,
  `foldl'` ≈ `sum` ≪ `foldr` < `foldl`. **`foldr` and `foldl` swap places.**
- **`foldl'` is unchanged across all four cells [2]**, which is what makes it the right default: it does
  not depend on an optimisation being enabled, and every other row does.

### (b) [6]

- `./folds0 foldl 10000000` **completes**, in 3.277 s, with **619 MB** resident. No exception. [2]
- With `+RTS -K16m`, **both**: [2]

  ```
  folds0: Stack space overflow: current size 33624 bytes.
  ```

- **The two sentences [2].** The advice was about **strictness, not direction**: for an operator strict
  in its accumulator, neither fold is safe, and what saves you is forcing as you go. And the
  "stack overflow" describes a default that has changed — GHC's stack lives on the heap and grows to 80%
  of it, so the same bug now presents as 619 MB of heap rather than as a crash.

**The mark is for explaining why `foldr` overflows too.** A student who only says "the stack limit is
bigger now" has half of it.

### (c) [6]

```haskell
foldl  f z (x:xs) = foldl  f (f z x) xs
foldl' f z (x:xs) = let z' = f z x in z' `seq` foldl' f z' xs
```
[2]

- **`seq a b` evaluates `a` to weak head normal form and then returns `b`.** [1]
- **What it does *not* do: evaluate `a` completely.** [1] One constructor deep is all. `seq (1:undefined)
  ()` succeeds; `seq undefined ()` does not. **This is the sentence people get wrong**, and it is why
  `deepseq` exists.
- **Strictness analysis** [2]. Any hypothesis of the form *"`-O2` worked out that the accumulator is
  always eventually needed and evaluated it as it went"* is full marks. **Why it cannot be relied on:**
  it is an optimisation, not a guarantee — their own `-O0` column is the proof, and a slightly different
  program (one where the accumulator is only *sometimes* needed) defeats the analysis at any level.

---

## Q4: `++` and `qsort` (20)

### (a) [7]

| *n* | `left` | `right` |
|---:|---:|---:|
| 10,000 | 1.17 s | 0.01 s |
| 20,000 | 4.93 s | 0.01 s |
| 40,000 | 22.57 s | 0.01 s |

**Ratios 4.2 and 4.6** for doublings — quadratic. [3]

**The definition [2]:**

```haskell
[]     ++ ys = ys
(x:xs) ++ ys = x : (xs ++ ys)
```

**The character is the `xs` in `xs ++ ys`** — the recursion is on the *left* argument only. `ys` is
never inspected, never copied, and appears once in the result, so the cost is `length xs` and nothing
to do with `ys`.

**The fix and its cost [2]:** cons onto the front and `reverse` once at the end — one O(n) pass instead
of n of them. Accept `foldr (:)`, which needs no reversal. Accept `Data.Sequence` with a note that it is
a different structure, or a difference list.

### (b) [7]

| | allocated | maximum residency | time |
|---|---:|---:|---:|
| `qsort` | 2,235,510,768 B | 55,926,624 B | **1.752 s** |
| `Data.List.sort` | 1,562,152,448 B | 47,827,872 B | **3.240 s** |

[4]

**Why faster is not a reason to use it [3]:** because (c) shows the same function taking **19 seconds on
40,000 already-sorted elements** where the library takes 0.194 s on a million. **The average case is
better and the worst case is unusable, and the worst case is the input you actually get** — anything
already sorted, nearly sorted, or sorted by a previous stage.

**Full marks require the appeal to (c).** A student who argues from "stability" alone has a true but
weaker answer; give 2.

### (c) [6]

| *n*, ascending | `qsort` | `Data.List.sort` |
|---:|---:|---:|
| 10,000 | 0.571 s | — |
| 20,000 | 2.714 s | 0.003 s |
| 40,000 | **19.009 s** | — |
| 1,000,000 | *hours* | **0.194 s** |

- **Ratios 4.75 and 7.00** [2] — worse than the 4.0 a pure quadratic gives. **The extra is the
  collector**: the recursion is n deep on sorted input, each level holds a live list, and residency
  climbs with it, so GC time grows on top of the comparison count.
- **Why the library is fast on sorted input [2]:** `Data.List.sort` is a **bottom-up mergesort that
  detects ascending runs first**. An already-sorted list is *one run*, so the first pass finds it and
  there is nothing left to merge — O(n).
- **Two properties of real quicksort it lacks [2]:** it is **not in place** (it allocates two new lists
  at every level), and it **does not choose a pivot** (it takes the head, which is why sorted input is
  the worst case). Also accept: no tail-recursion on the larger partition, and no fallback to insertion
  sort for small partitions.

---

## Q5: `sched`, Folded (18)

### (a) [6]

The six bodies are in `ReportSol.hs`. [3 for six correct replacements, no signature changed.]

**`runningTotals` [3]:**

- **The extra element is `scanl`'s starting value**, reported before anything has been added:
  `scanl (+) 0 [1,2,3]` is `[0,1,3,6]`. It is not an off-by-one error.
- On the empty list: **`tail . scanl (+) 0` gives `[]`** (because `scanl (+) 0 []` is `[0]`) and
  **`scanl1 (+)` gives `[]`**. Both correct.
- **`tail . scanl1 (+)` throws** — `tail []`. **This is the combination a student gets by using both
  hints**, it passes `make check` because the timetable is never empty, and catching it is worth the
  mark.

### (b) [6]

- **The tie:** `fst (maximumBy (comparing snd) [(Mon,100),(Tue,100),(Wed,50)])` is **`Tue`**.
  `maximumBy` keeps the **last** maximum. [2]
- **The one-word fix:** `reverse`. `maximumBy (comparing snd) (reverse (histogram ts))` gives **`Mon`**.
  [2] Accept `head (sortOn (negate . snd) …)`, which needs no `reverse` because `sortOn` is stable, and
  `minimumBy (comparing (negate . snd))`, which keeps the first minimum. **Both verified.**
- **The two sentences [2]:** a test that *generates* inputs — including ties — rather than running the
  one real timetable would have found it on the first attempt; that is Week 11. The real timetable
  cannot, because its maximum (Tue, 285) is unique. **Worth noting to them: the timetable does contain
  a three-way tie at 175, for Mon, Thu and Fri — just not at the maximum**, which is a nicely sharp
  illustration that "my data has ties" is not the same as "my data exercises the tie".

### (c) [6]

```haskell
gaps :: Day -> [Session] -> [(Minutes, Minutes)]
gaps d ts = [ (e, s) | (e, s) <- zip (hm 8 0 : map end onDay)
                                     (map start onDay ++ [hm 18 0])
            , e < s ]
  where onDay = sortOn start [ t | t <- ts, day t == d ]
```

[4 for a working version with no explicit recursion.]

**Wednesday:** `[(08:00,09:00),(09:50,10:00),(10:50,13:00),(14:50,15:00),(15:50,18:00)]`

**The `zip` idiom is the thing being taught:** pair "the end of each session, preceded by the day's
start" with "the start of each session, followed by the day's end", and every pair is a candidate gap.
The `e < s` guard drops the zero-length ones.

- **Which fold [1]:** a comprehension, or `foldr` — the result is a list built front to back and it
  streams. `foldl'` would work and gives nothing.
- **A day with no sessions [1]:** `zip [08:00] [18:00]` = `[(08:00, 18:00)]` — **the whole day is one
  gap**, which is right. A student whose version returns `[]` there has a bug and should be told which
  input finds it.

---

## Marks

| Q | Topic | Parts | Points |
|---|---|---:|---:|
| 1 | Reading higher-order types | 3 | 18 |
| 2 | Writing folds | 3 | 22 |
| 3 | Measuring the folds | 3 | 22 |
| 4 | `++` and `qsort` | 3 | 20 |
| 5 | `sched`, folded | 3 | 18 |
| | **Total** | **15** | **100** |

---

## What to Watch For Across the Cohort

1. **Q2(c) answered as "hangs" rather than `<<loop>>`.** They did not run it. This is the paper's
   cheapest test of whether measurements are being taken.
2. **Q3(b) answered as "the stack is bigger now".** Half the answer. The other half — that `foldr`
   overflows too, so direction was never the issue — is the one worth having, and it is what makes
   `foldl'` the rule rather than `foldr`.
3. **Q4(b) arguing that the four-liner is fine because it was faster.** They have not connected (b) to
   (c). Raise it in the tutorial; it is the paper's one genuinely engineering-shaped judgement.
4. **Q2(a) not noticing the quadratic `reverse` is Hutton's own.** Worth pointing out even to students
   who got the measurement, because the transferable lesson is that illustrative code is not library
   code.

---

*PROG 202 · Week 2 · PS 2 Solutions · INSTRUCTOR ONLY · © CSE Department*
