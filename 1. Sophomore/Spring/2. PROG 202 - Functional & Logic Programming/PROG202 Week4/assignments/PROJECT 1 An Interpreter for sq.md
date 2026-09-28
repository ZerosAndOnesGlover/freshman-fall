# PROG 202 · Project 1
## `sq` — An Interpreter for a Small Query Language

---

**Assigned:** Week 4, Wednesday · **Due:** Week 7, **Friday 17:00** · **Weight: 15% of the course**

**Submit** a tarball `P1_{LastName}_{StudentID}.tar.gz` containing your `Eval.hs`, plus a PDF report
`P1_{LastName}.pdf` of **at most four pages**.

> **You write one file.** `Eval.hs`, about 90 lines. Everything else — the syntax, the values, the
> timetable, the test suite, the runner — is given and must not be changed.
>
> **`make test` runs 27 test cases and prints how many passed.** That number is most of your mark, and
> you can see it from the first minute.
>
> **`ghc -Wall -O2` must be silent** on your submission.

---

## 1. What You Are Building

`sq` is a tiny language for asking questions about the timetable you have been carrying since Week 0.
Written in its intended surface syntax — **which you are not implementing** — a program looks like this:

```
count (filter (\t -> day t == Wed) timetable)
total (map (\t -> duration t) timetable)
let lectures = filter (\t -> kind t == LEC) timetable in count lectures
```

**There is no parser.** `Syntax.hs` gives you the abstract syntax tree and `Tests.hs` writes the
programs directly as `Expr` values, so the first of those three is

```haskell
Count (Filter (Lam "t" (Bin Eq (Field "day" (Var "t")) (DayL Wed))) Table)
```

**Parsing is CS 211's subject and it is deliberately not here.** What is here is everything that happens
*after* the parse: environments, scope, closures, and errors.

Your whole job is one function:

```haskell
eval :: Env -> Expr -> Either Err Value
```

**An environment in, and either an error or a value out.** Nothing mutates, nothing is global, and the
type is the design: every failure is a `Left` that the caller must handle, and an expression's meaning
depends on nothing but its environment.

---

## 2. The Files

| File | Yours? | What it is |
|---|---|---|
| **`Eval.hs`** | **yes** | `eval`, `apply`, and nothing else. Six TODOs |
| `Syntax.hs` | no | `Expr` and `Op`. Fifteen constructors |
| `Value.hs` | no | `Value`, `Env`, `Err`, `render`, and three coercions |
| `Sched.hs` | no | Week 1's timetable, unchanged |
| `Tests.hs` | no | **27 cases with their expected answers.** Read it — it is the specification |
| `Main.hs` | no | The runner |
| `Makefile` | no | `make test`, `make test-phase1`, … |

**`Tests.hs` is the specification and it is readable.** When the prose here and `Tests.hs` disagree,
`Tests.hs` wins; if you find such a disagreement, say so in your report and you will get credit for it.

---

## 3. The Three Phases

**Do them in order.** Each is a checkpoint you can stop at with a working program, and the weeks line up
with the lectures.

### Phase 1 — expressions and the timetable *(Weeks 1–4 material; do it in Week 4–5)*

TODOs 1–4. Literals, variables, `Table`, binary operators, `if`, field access, and the four list
primitives.

**12 of the 27 cases.** `make test-phase1`.

**The two things that are not mechanical:**

- **`filter` and `map` take a function that can fail.** `Data.List.filter` cannot help you, because your
  predicate returns `Either Err Bool` and not `Bool`. Write the recursion by hand. *(Week 5 will show you
  that what you wrote has a name, and Week 6 will show you it is one line.)*
- **`==` must refuse to compare different kinds of value.** `day t == LEC` is a **type error**, not
  `false`. The case is called `mixed-equality` and getting this wrong is the commonest way to lose marks
  in Phase 1.

### Phase 2 — `let` and scope *(Week 5 material; do it in Week 5)*

TODO 5. Three lines, and the test called `let-shadow` pins down which way round `extend` goes.

**4 more, 16 of the 27.** `make test-phase2` shows those four.

### Phase 3 — functions and closures *(do it in Week 6–7)*

TODO 6. `Lam` builds a closure; `App` applies one.

**The remaining 11, and all 27 together.** `make test-phase3`, then `make test`.

> **`closure-is-not-dynamic` is the case that decides whether you understood this.**
>
> ```
> let k = 1 in
>   let f = \x -> x + k in
>     let k = 100 in f 0
> ```
>
> **The answer is 1, not 100.** `f` captured `k = 1` when it was created. If you apply a function in the
> *caller's* environment instead of the one it captured, **every other test still passes and this one
> fails** — which is why it is in the suite and why you should read it before writing `apply`.
>
> That is the difference between *lexical* and *dynamic* scope, and choosing lexical is the single most
> consequential decision in this project. Your report must say why.

---

## 4. Marking

| | | |
|---|---:|---|
| **Test cases** | **50** | `make test`, pro rata. 27 cases, 50 marks |
| **Error handling** | **15** | Every failure is a `Left` with the *right* `Err`. No `error`, no `undefined`, no partial pattern match in your code |
| **Code quality** | **15** | `-Wall` silent; no pattern-matching on `Value` outside the given coercions; `eval` readable as one `case` |
| **Report** | **20** | §5 |
| **Total** | **100** | |

**Two automatic deductions, stated so they are not a surprise:**

- **Any file other than `Eval.hs` modified: −20.** The suite must run against the given ones.
- **`-Wall` not silent: −5 per distinct warning**, to a maximum of −15. The skeleton starts with
  unused-binding warnings; they disappear as you do the TODOs.

---

## 5. The Report — Four Pages, Twenty Marks

Not a description of your code. **Four questions, five marks each.**

**(a) Lexical scope.** State what `closure-is-not-dynamic` tests and what your `apply` does about it.
Then: **give a program in which dynamic scope would be more convenient**, and say why languages stopped
using it anyway.

**(b) Errors.** `eval` returns `Either Err Value`, so every intermediate step has to be unwrapped and
rewrapped, and your `Filter` and `Map` had to be written by hand because of it.

- **Count the lines of your `Eval.hs` that exist only to move errors around.** Give the number.
- What would the same interpreter look like if a failure were an exception?
- **What would it look like if `eval` returned `Value` and you used `error`?** Name what you would lose,
  precisely — and note that this is what most interpreter tutorials do.

**(c) The environment.** `Env` is `[(Name, Value)]`.

- What is the complexity of a variable lookup, and what is the deepest environment any of the 27 tests
  produces?
- Replace it with `Data.Map` and re-run the suite. **Report the timing of `make test` before and
  after.** *(You will find it makes no measurable difference. Say why, and say what input would change
  that.)*
- `extend` conses. **Say why an immutable environment is the right choice here anyway**, using Week 3's
  measurement of a persistent insert.

**(d) What `sq` cannot do.** Pick **one** and answer properly:

- **Recursion.** `let f = \x -> ... f ... in ...` does not work in `sq`. Say exactly why, from your
  implementation of `Let`, and what minimal change would allow it.
- **Types.** Every error in `sq` is found at run time. Say what a type checker for `sq` would have to
  do, and name the one from Week 1 L03 §5 that you have already met.
- **`total` on a list of sessions.** Why is it a type error, and what would you have to add to the
  language rather than to the interpreter to make `total timetable` mean something sensible?

---

## 6. Practicalities

```bash
mkdir -p "$PROG202/week4/project1"
cd "$PROG202/week4/project1"
cp "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week4/assignments/project1/"* .
make test
```

**`week4/project1/` is submitted work, not `practice/`.** It is where the grader looks.

**Commit as you go**, at least once per phase. A single commit at 16:55 on the Friday of Week 7 is
its own evidence.

> **Plan around the midterm.** The paper is **Thursday of Week 6** and covers Weeks 0–5. **Phases 1 and
> 2 use only material the midterm also covers**, so doing them before it is revision rather than a
> competing demand. Phase 3 needs nothing new — do it after.
>
> **Spring Break is the week after the deadline, not before it.** There is no slack at the end.

**Collaboration:** discuss approaches freely; the code and the report must be yours. Name anyone you
discussed which phase with, at the top of the report. **`Tests.hs` is given to everybody, so comparing
test *results* is not collaboration — comparing `Eval.hs` is.**

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest *problem set* is
dropped; **projects are not.**

---

## 7. What This Feeds

**Project 2**, due in the completion period, asks the same questions of Prolog — and in Week 12 you put
the two side by side. `sq`'s `filter (\t -> day t == Wed) timetable` is one line of Prolog with no
interpreter at all, and **understanding why is the point of the second half of this course.**

**CS 311 next year writes the parser** this project deliberately omits, and then a type checker, and then
a code generator. `Eval.hs` is the stage it starts from.

---

*PROG 202 · Project 1 · assigned Week 4, due Week 7 · © CSE Department*
