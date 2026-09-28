# PROG 202 · Lab 1 · Solutions
## Algebraic Data Types, and Making the Bug Unwriteable
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Session:** Wednesday of Week 2, 13:00–14:50, BH 215 · **Unmarked**, checked off in the session.

**What the session is really for.** Not `data` syntax — they can read that. It is for the **hierarchy
in L04 §3**: which defect each tool catches, and the fact that the tools run out before the defects
do. A student who leaves able to say *"the type stopped eleven, the smart constructor stopped the
twelfth, and the export list is what makes the smart constructor mean anything"* has had the session.

**Timing.** §0 8 · §1 12 · §2 18 · §3 25 · §4 12 · §5 15 · §6 12 · checkoff 8 = **110 minutes.**
§3 overruns; §6 is the one to cut, because PS 1 Q3 covers it with marks.

**The complete solution** is `SchedSol.hs` in this directory. Do not hand it out; §5's export-list
question stops working once they have seen it.

---

## §0 — Setup

**One failure to expect:** `make` before they have done anything, producing eight `error "TODO"` type
errors at once and a wall of red. Say at the start that the skeleton is *meant* not to build, and that
TODOs 1–3 must be done together — the type errors from a missing `Day` cascade into everything.

**Suggest they do TODO 1, 2, 3 and then `:l Sched.hs` in GHCi**, before touching TODOs 4–8. The module
will load with `error` stubs in it, and they can inspect types.

---

## §1 — `Day` and `Kind`

```haskell
data Day  = Mon | Tue | Wed | Thu | Fri  deriving (Show, Eq, Ord, Enum, Bounded)
data Kind = LEC | LAB | REC | SEM        deriving (Show, Eq, Ord, Enum, Bounded)
```

**Answers.**

*Where did `Mon < Tue` come from?* **Declaration order.** `deriving Ord` orders constructors by the
order they appear in the `data` declaration, left to right. Nobody wrote a comparison.

*A type where that would be a bug.* Anything whose constructors have a natural order that is not the
one you happened to type. The examples that land:

- `data Severity = Debug | Error | Info | Warning` listed carelessly — `Error < Info` is now true and
  every log filter is wrong.
- `data Suit = Clubs | Diamonds | Hearts | Spades` is right for bridge and wrong for any game that
  ranks them differently.
- **A type where no order is meaningful at all**, e.g. `data Colour = Red | Green | Blue`. Deriving
  `Ord` there does not give a wrong order; it invites code that *depends* on an order that means
  nothing. That is the better answer and a few will find it.

*Why `Session` does not derive `Ord`:* there is no obvious answer to "which of two sessions comes
first" — by day? by start time? by course code? Deriving it would silently pick *field order*, which is
`course` first, alphabetically. **Ask the room what `sort` would then do to the timetable.** It sorts
by course name, which nobody wants.

---

## §2 — `Course`, `Minutes`, `Session`

```haskell
newtype Course = Course String
  deriving (Eq, Ord)

instance Show Course where
  show (Course c) = c

newtype Minutes = Minutes Int
  deriving (Eq, Ord)

instance Show Minutes where
  show (Minutes t) = pad (t `div` 60) ++ ":" ++ pad (t `mod` 60)
    where pad n = if n < 10 then '0' : show n else show n

data Session = Session
  { course :: Course
  , kind   :: Kind
  , day    :: Day
  , start  :: Minutes
  , end    :: Minutes
  } deriving (Eq, Show)
```

**Note what is derived and what is not.** `Eq` and `Ord` are derived on both newtypes — `Ord` on
`Minutes` is what `overlaps` uses, and deriving it is right because `Int`'s order *is* the meaning.
`Show` is hand-written on both, and that is a deliberate convention violation flagged in the sheet.

**The point to make aloud at `:t course`:** five functions appeared from a record declaration. They are
ordinary functions — `course :: Session -> Course` — not a special member-access syntax, which is why
`map course ts` works and why `sortOn start` will work in Week 2.

**Common mistakes:**

- **`data` instead of `newtype`**, usually because they copied `Session`'s shape. Accept it; point out
  it is a heap box per value for no benefit, and that `newtype`'s restriction (exactly one constructor,
  exactly one field) is what lets GHC erase it.
- **Deriving `Show` and then wondering why the output says `Minutes 660`.** Half the room. This is the
  moment to say what `Show` is *for*.
- **Trying `deriving newtype`.** `GeneralizedNewtypeDeriving` is not on and they do not need it.

---

## §3 — The Module Body

```haskell
mkSession c k d s e
  | s >= e    = Left (show c ++ " " ++ show k ++ " " ++ show d ++
                      ": starts at " ++ show s ++ " and ends at " ++ show e)
  | otherwise = Right (Session c k d s e)

duration t = b - a
  where Minutes a = start t
        Minutes b = end t

overlaps a b = day a == day b && start a < end b && start b < end a

inWindow (Window d s e) t = day t == d && start t < e && s < end t
```

**`duration` is where `-Wall` will bite them**, and instructively: `where Minutes a = start t` is a
pattern binding on a single-constructor type, so it is total and GHC is silent. If they write it over a
*multi*-constructor type the same shape triggers `-Wincomplete-uni-patterns`, which **`-Wall` does
include on 9.4.7**. Worth saying: older advice that you must add that flag by hand is out of date.

**`overlaps` should now read better than the Week 0 version**, and asking them to compare the two lines
side by side is worth thirty seconds:

```haskell
-- Week 0
overlaps (_, _, d1, s1, e1) (_, _, d2, s2, e2) = d1 == d2 && s1 < e2 && s2 < e1
-- Week 1
overlaps a b = day a == day b && start a < end b && start b < end a
```

**The Week 0 version cannot be read without counting the underscores.** That is the argument for
records, and it is not about safety.

### `timetable` and `traverse id`

```haskell
timetable = traverse id
  (  [ mkSession (Course "MATH 251") LEC d (hm  8  0) (hm  8 50) | d <- [Mon, Tue, Thu] ]
  ++ … )
```

**What to say about `traverse id` and no more:** it takes a list of `Either String Session` and gives
an `Either String [Session]` — **all of them, or the first failure.** Do not explain `Traversable`; do
not say "applicative". Collect their one-sentence guesses and **write the good ones on the board**;
Week 6 L20 opens by returning to them, and having them in the students' own words is worth more than a
correct definition in Week 1.

**Expected output:**

```
sessions         : 17
contact minutes  : 1070
clashes          :
lunch collisions :
  PROG 202 LEC Tue 11:00-12:15
  PROG 202 LEC Thu 11:00-12:15
minutes per day  : [(Mon,175),(Tue,285),(Wed,260),(Thu,175),(Fri,175)]
```

**Insist on the identical 17 / 1070 / 0 / 2.** A rewrite that changes the answers has a bug in it, and
saying so is worth more than the rewrite.

**The per-day answer:** 175 + 285 + 260 + 175 + 175 = **1,070** ✓. Tuesday is heaviest at 285 minutes
(MATH 251 50, CS 212 50, PROG 202 75, CS 202 lab 110). The 09:00-exam question has no right answer;
listen for whoever says **Wednesday**, because Wednesday's 09:00 is already CS 202's lecture.

---

## §4 — The Hole the Types Left

```
$ python3 orderings.py tuple middle
design: tuple    120 tried, 12 accepted, 11 wrong
design: middle   120 tried,  2 accepted,  1 wrong  -> [(0, 1, 2, 4, 3)]
```

**Each design really does invoke `ghc` 120 times and takes about a minute.** Start it running at the
beginning of §4 and talk over it.

**`(0, 1, 2, 4, 3)` is `start` and `end` swapped** — positions 3 and 4 exchanged. It is the only wrong
ordering left because it is the only pair of fields still sharing a type.

**The smart constructor catching it:**

```
$ ./sched
rejected: PROG 202 LEC Thu: starts at 12:15 and ends at 11:00
```

**Point out that the whole timetable was rejected, not just the bad session.** That is `traverse`, and
for a file of static data it is right — a timetable with one impossible session is not a timetable with
sixteen good ones. Ask what you would want instead if the sessions came from a form a user filled in,
and leave the question open; it is Week 6's.

**Answers.** *Why not `strict` (a newtype per field, zero wrong orderings)?* Two costs, and they should
give code:

- **Every arithmetic use needs unwrapping, and one of them stops compiling.** `duration` becomes two
  pattern matches on two *different* types, and `start a < end b` in `overlaps` **does not compile at
  all** — measured:

  ```
  strictcmp.hs:5:26: error:
      • Couldn't match expected type ‘Start’ with actual type ‘End’
      • In the second argument of ‘(<)’, namely ‘end b’
  ```

  There is no `Ord` across two types, so you add a conversion — and the moment you do, the two are
  comparable again and the protection you paid for is gone. **Show this at the board if anyone argues
  for `strict`;** it is the whole argument in four lines.
- **It does not scale.** Five fields, five newtypes, five `Show` instances. A twelve-field record gets
  twelve, and people stop doing it by Thursday, and then the *inconsistency* is worse than either
  design.

The second cost is the one that decides it. **The right answer to "which would you ship" is `middle`
plus `mkSession`**, and a student who says `strict` should be asked to write `overlaps` for it at the
board.

---

## §5 — The Module Boundary

```
$ make break
Break.hs:14:7: error:
    • Illegal term-level use of the type constructor or class ‘Session’
    • imported from ‘Sched’ at Break.hs:11:1-12
    • Perhaps use variable ‘mkSession’ (imported from Sched)
```

**This is the best error message in the week and most of the room will misread it.** They expect
*"Session is not in scope"* or *"not exported"*. Instead GHC says **you have used a type name where a
value is wanted** — because `Session` the *type* is exported and in scope, and `Session` the
*constructor* is not. The two live in separate namespaces (L03 §2), and the export list let exactly one
of them through.

**And it suggests `mkSession`.** Worth pointing at.

**Answers.**

1. Covered above. Require the words "two namespaces" or an equivalent.
2. `Session (..)` exports the constructor too. `make break` now **compiles**, and

   ```
   $ ./break
   PROG 202 LEC Tue 12:15-11:00
   $ echo $?
   0
   ```

   **A session that ends before it starts, rendered perfectly happily, exit status 0.** Nothing
   crashes. That is the point: the bad value simply exists now, and it will produce a wrong answer
   somewhere later and further away. **Make them run it** — the absence of a crash is the lesson.

   **Two details worth ten seconds each.** `Session (..)` also exports the five field accessors, which
   the list already names, so GHC emits three `-Wduplicate-exports` warnings — **the "fix" is not even
   clean.** And `render bad` still works, because `render` never had any reason to care; a smart
   constructor protects the *making* of values, never their use.
3. **The sentence wanted:** *"The check in `mkSession` only helps if there is no other way to make a
   `Session`, and the export list is the only thing that makes that true."* Accept any phrasing with
   both halves. **Reject "because `mkSession` validates the input"** — that is the thing they already
   believed and it is what the exercise disproves.

> **If one thing is said in this session, it is this.** A validation function is a *convention* until
> a module boundary makes it a *guarantee*. This generalises to every language with a visibility
> modifier, and it is the transferable half of Lab 1.

---

## §6 — Exhaustiveness

Both warnings from `exhaustive.hs` are in L04 §2; read them out rather than paraphrasing, because the
`...` at the end of the `String` one is the punchline.

**(a)** GHC names the fourth case: `Patterns of type ‘Kind’ not matched: SEM`.

**(b)** This is the part to spend time on.

```haskell
firstSession :: [Session] -> Session
firstSession ts = head ts
```

**`-Wall` says nothing.** `./sched` on an empty list gives `Prelude.head: empty list`.

*Why can GHC check one and not the other?* Because **exhaustiveness is a property of a pattern match,
and there is no pattern match here.** `head` is an ordinary function whose own definition is
incomplete, and that incompleteness was checked once, inside `base`, where it was written deliberately.
By the time you call it, the type `[Session] -> Session` is a **lie the compiler has no way to
detect** — it promises a `Session` for every list, including the empty one.

*The fix:*

```haskell
firstSession :: [Session] -> Maybe Session
firstSession = listToMaybe
```

**The fix is in the type.** Once it admits the empty case, every caller is forced to handle it — which
is L03 §3, and the reason `Maybe` exists.

**Listen for the student who says "just check for `[]` first".** That works and it is the worse answer:
it fixes this call site and leaves the next one. Ask them how they would find the next one.

---

## Checkoff

Six items. **Be strict about two:**

- §5 question 3 must be *spoken*, and must contain both halves. This is the session's thesis.
- The `traverse id` sentence must be *written down and kept*. Week 6 L20 asks for it back, and the
  exercise only works if they wrote it before they knew.

---

## After the Session

**PS 1 is due the Friday of Week 2** and repeats §4, §5 and §6 with marks attached. Students who
finished §6 have done Q3(c).

**Quiz 2 is the Tuesday of Week 2** and covers Week 1 — the counting, the `type`/`newtype`/`data`
distinction, and the exhaustiveness measurement.

**Week 2 removes the recursion.** Several students will have written `duration` and `pairs` with
explicit recursion rather than comprehensions; do not correct it, note who, and let L05 do it.

---

*PROG 202 · Week 1 · Lab 1 Solutions · INSTRUCTOR ONLY · © CSE Department*
