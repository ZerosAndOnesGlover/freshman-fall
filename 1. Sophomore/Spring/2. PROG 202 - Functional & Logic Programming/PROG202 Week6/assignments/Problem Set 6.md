# PROG 202 · Problem Set 6
## Applicatives, Monad Transformers, and Functional Error Handling

---

**Released:** Week 6, Wednesday · **Due:** Week 7, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS6_{LastName}_{StudentID}.pdf`, plus your `.hs` files in a tarball
`PS6_{LastName}.tar.gz`

> **About three hours.** Five questions, fifteen parts.
>
> **⚠️ Project 1 is due the same day, Friday of Week 7 at 17:00.** Both are deadlines and neither moves. **Do
> Project 1 first if you are behind**: it is worth 15% and this is worth about 3%. Q5 of this paper is
> Project 1's report question (c), so doing that part twice is not wasted.
>
> **Every `.hs` file compiles clean under `ghc -Wall -O2`.**

---

### Q1: `<*>` Against `>>=` (20 points)

**(a) [7]** For each, say whether it is **applicative** or **monadic**, using L13 §7's test — *"is any
`<-`-bound name used in a later statement's arguments?"* — and give the `<$>`/`<*>` form where one exists.

1. Look up two keys in a map and add them.
2. Look up a key, then use its value as the next key.
3. Validate five independent fields of a form.
4. Read a config file, then open the file it names.
5. Run two independent `IO` actions and pair their results.

**(b) [6]** `<*>` and `>>=` differ in one structural way.

- Give both types, and say which argument of each is a *function of the previous result*.
- **Hence explain why `Either` reports one error out of three**, and why that is not a bug.
- Give the one-sentence reason an applicative *can* run both sides when a monad cannot.

**(c) [7]** `:t` each and say what it does: `liftA2`, `sequenceA`, `traverse`, `<*`, `*>`, `<$`.

Then: `traverse`'s constraint is `Applicative f`, **not `Monad f`.** Give **two** consequences of that
choice, one about error reporting and one about evaluation order. *(The second is Week 7's.)*

---

### Q2: An Applicative That Is Not a Monad (22 points)

**(a) [8]** Write the `Validation` applicative — the `newtype`, `Functor`, and `Applicative` — and use it to
validate a `Session` with three independent checks.

- Report the output for a session with **three** things wrong, and for a good one.
- Report the same three checks over `Either`. **One error against three.**
- **Why does the instance need `Semigroup e`?** Say what breaks without it.

**(b) [8]** Now write the `Monad` instance for `Validation`.

- **It compiles.** Report that it does, with `-Wall`.
- Report `(+) <$> l1 <*> l2` and `((+) <$> l1) \`ap\` l2` for two `Left`s. They differ.
- **Name the law that is broken**, state it, and say why the standard library therefore provides no `Monad`
  instance for validation.
- Give the `Monad` instance that **does** satisfy the law, and say what it costs.

**(c) [6]** `traverse validateSession sessions`.

- Run it over `Either` and over `Validation` on a list with **two** bad sessions. Report both.
- **The traversal is the same function.** Say what changed.
- Hence: complete the sentence *"the choice of applicative chooses …"* and give one more example of a
  strategy you could choose this way.

---

### Q3: The Order of the Stack (20 points)

**(a) [8]** Build `resources/order.hs` and report both lines.

- Give the type of `runStateT` and of `runExceptT`, and **derive from the types alone** which stack keeps the
  state.
- **State the rule** in one sentence.
- The `step` function is byte-identical in both stacks. **Say what warned you.**

**(b) [6]** Add a `WriterT [String]` log to each of the two stacks.

- Report where you put it in each, and what each gives for a run that fails halfway.
- **For the log to survive the failure, where must it go?**
- Hence generalise the rule to a stack of four layers.

**(c) [6]** Weeks 3–6 have now shown you three silent type-level choices that decide a runtime property.

- Name all three, **with their measurements.**
- For each, say what — if anything — would have warned you.
- **One of the three is different in kind from the other two.** Say which and why.

---

### Q4: `Stack` (20 points)

From your Lab 6 `Stack.hs`.

**(a) [8]** Report `make test` at 13/13, and your `loadSession`.

- Confirm you used `asks dayStart` and that `Config` is **not** an argument.
- **You wrote no `lift`.** Explain why, naming the three classes involved.
- **That is also why the wrong stack order compiled.** Explain the connection in two sentences.

**(b) [6]** The skeleton shipped with the wrong order and 7 of 13 failing.

- Report the shape every failure had.
- **Explain, from the type of `runExceptT (runStateT …)`**, why `runApp` had to invent a `Trace`.
- Give the one-line change to `App` and the one to `runApp`.

**(c) [6]** `loadAll` short-circuits and `validateAll` accumulates, and **they perform the same
validations.**

- Which of the two could have been written the other way, and which could not? Justify both.
- `validateAll` takes a `Config` argument where `loadAll` uses `asks`. **Say why it has to.**
- Suppose the requirement changed to *"report every bad row, but stop after ten"*. Which of the two would you
  start from, and what would you add?

---

### Q5: Where Project 1 Would Go (18 points)

This is Project 1's report question (c), extended. **The same answer counts for both.**

**(a) [6]** Write the type `eval` would need if the interpreter also counted steps and had a read-only
environment.

- Give the type, with all three layers.
- **Justify the order of each layer in one sentence.**
- Say which layer `Env` is, and why it is not a `State`.

**(b) [6]** Project 1's `Env` is `[(Name, Value)]`.

- Replace it with `Data.Map` and re-run `make test`. Report the timing before and after.
- **It makes no measurable difference.** Say why, and give an input that would change that.
- `extend` conses. Using Week 3's persistent-insert measurement, **say why an immutable environment is right
  here anyway.**

**(c) [6]** `sq` has no recursion: `let f = \x -> … f … in …` does not work.

- **Explain exactly why**, from your implementation of `Let`.
- Give the minimal change that would allow it, and say what it costs.
- **Name the Week 3 concept** that makes that change possible in Haskell but not in a strict language.

---

## Marks

| Q | Topic | Parts | Points |
|---|---|---:|---:|
| 1 | `<*>` against `>>=` | 3 | 20 |
| 2 | An applicative that is not a monad | 3 | 22 |
| 3 | The order of the stack | 3 | 20 |
| 4 | `Stack` | 3 | 20 |
| 5 | Where Project 1 would go | 3 | 18 |
| | **Total** | **15** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of
the term is dropped** — and **Project 1, due the same day, is not a problem set.**

---

*PROG 202 · Week 6 · PS 6 · © CSE Department*
