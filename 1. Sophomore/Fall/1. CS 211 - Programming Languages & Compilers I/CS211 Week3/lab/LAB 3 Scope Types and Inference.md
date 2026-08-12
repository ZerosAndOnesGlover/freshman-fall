# CS 211 · Lab 3
## Scope, Types, and Inference

---

**Week 3 · Friday 14:00–15:50 · BH 220** — after both of this week's lectures.
**Unmarked.** The TA checks your work off in the session.
**Starter files:** `typecheck.py`, `hm.py`, `scopes.cy`, plus `lexer.py` and `parser.py` from Weeks 1–2.

> **Midterm 1 is announced this week** and covers Weeks 0–3. It is sat in **Week 4**. The revision
> guide arrives with Week 4's materials; this lab is the last new front-end content before it.

---

## Why This Lab Exists

L07 gave you a type checker that annotates, and L08 gave you one that infers. **They are not the same kind of thing at all**, and this lab is about feeling the difference rather than being told it.

You will watch a scope chain resolve a name three levels up, watch a type error land on the exact column of the offending operator, and then watch Hindley-Milner derive a type nobody wrote — and fail on an expression that looks perfectly reasonable.

---

## Part 1 — Scope Chains (25 minutes)

```bash
python3 typecheck.py scopes.cy
```

`scopes.cy` declares **three** variables named `a`, at three nesting depths, in each of two functions.

**Q1.** Read `shadow`. **For each use of `a` and `b`, say which declaration it resolves to** and at what depth. The `return a;` at the end is the one to think about.

**Q1b. Now read `shadow_bug`, which type-checks and never terminates.**

The `while` tests the depth-2 `a`. The body's first line is `let a = a - 1;` — which **declares a new depth-3 `a`** rather than assigning to the depth-2 one, so nothing the loop tests ever changes.

- **Which single character would you change** to make it terminate?
- **The type checker passes it without a murmur.** Say why — what kind of property is termination, and is any type system in this course going to catch it?
- Cyan permits shadowing. **Rust warns on exactly this pattern and Java forbids it for locals.** Given this example, which do you think is right?

**Q2.** Find `Scope.lookup` in `typecheck.py`. It is six lines. **Explain how shadowing falls out of it** without shadowing being implemented anywhere.

**Q3.** Change `lookup` to walk to the **last** match instead of the first — keep walking after a hit, and return the outermost binding. Rerun on `scopes.cy`.

- **Does it still type-check?**
- **Has any value changed?** Add a `return` that would expose the difference, and demonstrate it.
- **Restore the original afterwards.**

**Q4.** Cyan has **no bare block statement** — `{ let a = 2; }` on its own is a *parse* error, not a scope error. Confirm it:

```bash
echo 'fn f() { { let a = 2; } }' | python3 parser.py
```

**Where does scope nesting come from, then?** Name the two constructs that open one, and connect this back to L02 §6's mandatory braces.

---

## Part 2 — Errors With Positions (25 minutes)

Save this as `bad.cy` exactly as written, line breaks included:

```cyan
fn f() -> int {
  let x = 1;
  return x
    + true;
}
```

```bash
python3 typecheck.py bad.cy
```

**Q5.** The error names a line and a column. **Which line and column, and what is at that position?** Note that the statement began on line 3.

**Q6.** Open `parser.py` and find where the `Binary` node gets its position. **Which token does it take it from** — the left operand, the operator, or the right operand? **Why is that the right choice** for this error message?

**Q7.** Now break it. In `parser.py`, make `Node.__init__` ignore the `line` and `col` arguments and store `0` instead. Rerun on `bad.cy`.

**How much worse is the message?** Then answer: **could the type checker recover the position from anywhere else?** The tokens still exist while the parser runs — but do they still exist when the checker does?

**Restore `parser.py` afterwards.**

**Q8.** Write **three** Cyan programs, each triggering a different message from L07 §5's table of eighteen. **For each, predict the line and column before running it.**

---

## Part 3 — Inference (35 minutes)

```bash
python3 hm.py
```

**Q9.** Record the inferred types for all six expressions in the first block. **For `\f -> \x -> f (f x)`, explain in one sentence** what forces `f`'s argument and result types to be the same.

**Q10.** The last block prints a trace for `\x -> x + 1`:

```
assign x : t0
unify(t0, int)
unify(int, int)
```

**Write the equivalent trace by hand** for `\x -> if x <= 0 then 1 else x`. You should get five or six steps.

### 3.1 Cross-check against GHC

```bash
cat > t.hs <<'EOF'
i     = \x -> x
twice = \f -> \x -> f (f x)
comp  = \f -> \g -> \x -> f (g x)
EOF
for n in i twice comp; do echo ":t $n" | ghci -v0 t.hs; done
```

**Q11.** **Do the types match `hm.py`'s?** They will differ in variable *names*. **Why is that difference not a disagreement?** Refer to the principal type theorem.

### 3.2 The occurs check

**Q12.** `\x -> x x` fails. **Quote the error**, then write out the equation it could not solve. Why is there no finite type satisfying it?

**Q13.** Comment out the `occurs()` guard in `hm.py`'s `unify` and rerun. **Describe what happens** — and be ready to interrupt it.

**Restore it afterwards.**

### 3.3 Let-polymorphism, and a trap

**Q14.** The output shows four lines under *let-polymorphism*. Two are marked `[both OK]`.

- **Which pair demonstrates the effect**, and what is the error on the failing one?
- **Why does the `id (id 1)` pair not demonstrate it?** This is the trap — say precisely what is different about how `id` is used there.

**Q15.** In `\f -> (f 1, f True)` — imagine Cyan had tuples — `f` is **lambda-bound**, so HM refuses. **Is that a limitation or a deliberate choice?** One sentence, referring to what generalising lambda-bound variables would cost. *(L08 §6 names the system where it is allowed.)*

---

## Part 4 — Where Haskell Is Not HM (10 minutes)

```bash
echo 'bad = 1 + True' > e.hs
ghc -fno-code e.hs 2>&1 | head -5
```

**Q16.** GHC says `No instance for (Num Bool)`. **`hm.py` says `cannot unify bool with int`.**

**These are different kinds of error.** Say what GHC's message implies about the type of the literal `1` in Haskell, and why that is not simply `Int`.

**Q17.** L08 §7 calls this "the seam". **What is bolted onto HM here**, and which week takes it up?

---

## Before You Leave

The TA checks:

- [ ] **Part 1** — Q1's four resolutions; Q3's modified `lookup` demonstrated **and reverted**
- [ ] **Part 2** — Q5's line and column; Q7 run **and reverted**, with the recoverability question answered
- [ ] **Part 3** — six inferred types; Q11's GHC cross-check; **Q14's trap explained correctly**
- [ ] **Part 4** — Q16 distinguishing a class error from a unification error

**Q14 is the checkoff that matters.** A student who thinks `id (id 1)` demonstrates let-polymorphism has not understood what generalisation buys.

---

## If You Finish Early

**Add a type rule to Cyan.** `The Cyan Language Reference` §4 says `+` on two `string`s concatenates. **Add `*` on a `string` and an `int`** — `"ab" * 3` giving `"ababab"` — to `typecheck.py`.

Then answer the design question: **`3 * "ab"` — legal or not?** Implement your choice, and say what Python does and why.

**Harder:** make `typecheck.py` report **more than one error per run** instead of stopping at the first. What must change about `err()`, and what new problem appears once one error's type is unknown? *(This is the error-recovery trade from Week 1 L03 §6, one phase up.)*

---

*Next: Week 4 — the front end is done. The typed tree becomes three-address code and a control-flow graph, which is the form a compiler actually optimises. Midterm 1 sits this week and covers Weeks 0–3.*
