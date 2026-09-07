# CS 211 · Lab 0
## Grammars, Derivations, and the Shape of Cyan

---

**Week 0 · Friday 14:00–15:50 · BH 220** — the Friday that closes the ten-day Week 0.
**Unmarked.** The TA checks your work off in the session. [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second unexcused absence.
**Bring:** the Week 0 lectures, and [[The Cyan Language Reference]].

> **CS 211's lab does not lag.** Lab *N* covers Week *N* and is sat on the **Friday of Week *N***,
> after both of that week's lectures. CS 201's lab, in the same term, works the other way. Do not
> carry the habit across — see the syllabus, *"The lab does not run a week behind"*.

**Starter file:** `cfg_count.py`, in this folder.

---

## Why This Lab Exists

Two reasons, and the first is administrative: **you need six tools working before Week 1**, and finding out in Week 1 that `bison` is missing costs you a problem set.

The second is the real one. Lecture 2 asserted that a grammar can admit 58,786 parse trees for a twelve-operand expression. **You are going to watch that happen**, then fix it, then break Cyan's own grammar and watch the counter catch you. By the end you will have used the ambiguity checker three times, which is roughly how many times you will need it in Week 2 when bison starts complaining.

---

## Part 1 — The Toolchain (20 minutes)

Everything below is preinstalled in BH 220. **If you are on your own machine, run this first**, because Week 1 opens with `flex` and Week 3 with `ghc`.

```bash
sudo apt install -y flex bison llvm clang ghc cabal-install swi-prolog-nox
```

### 1.1 Check every tool

```bash
for c in python3 gcc flex bison ghc clang opt lli swipl java; do
    printf "%-8s " "$c"
    command -v $c >/dev/null 2>&1 && $c --version 2>&1 | head -1 || echo "MISSING"
done
```

**Every line must print a version.** Record them — versions matter when a lecture quotes a number and your machine disagrees.

| Tool | Needed from | What it is for |
|---|---|---|
| `python3` | Week 1 | `cyanc` itself is written in Python |
| `flex` | Week 1 | generated lexers, to compare against your hand-written DFA |
| `bison` | Week 2 | generated LALR(1) parsers |
| `ghc` | Week 3 | Haskell, for type inference |
| `clang` `opt` `lli` | Week 4 | LLVM IR — reading, optimising, running |
| `gcc` | Week 6 | the garbage collector |
| `java` | Week 6 | a real generational collector to profile |
| `swipl` | today | one Prolog query, in Part 2 |

> **`opt` and `lli` may be installed under versioned names** — `opt-18`, `lli-18` — with no
> unsuffixed symlink. If `command -v opt` fails but `command -v opt-18` succeeds, that is fine;
> note it, because Week 4's commands will need the suffix on your machine.

### 1.2 Four paradigms, four commands

Lecture 1 §3 claimed all four of these produce `Ada, Grace`. Check it.

**Imperative and functional:**

```bash
python3 -c "
people = [('Ada', 36), ('Alan', 24), ('Grace', 45)]
out = []
for n, a in people:
    if a > 30: out.append(n)
print('imperative ->', sorted(out))
print('functional ->', sorted(n for n, a in people if a > 30))"
```

**Declarative:**

```bash
sqlite3 :memory: <<'EOF'
CREATE TABLE person(name TEXT, age INT);
INSERT INTO person VALUES('Ada',36),('Alan',24),('Grace',45);
SELECT name FROM person WHERE age > 30 ORDER BY name;
EOF
```

**Logic:**

```bash
cat > people.pl <<'EOF'
person(ada, 36).
person(alan, 24).
person(grace, 45).
older_than(N, X) :- person(N, A), A > X.
EOF
swipl -q -g "forall(older_than(N,30), (write(N), nl))" -t halt people.pl
```

**Q1.** All four produce the same names. **Rank the four by how much of the *method* you had to write**, and say for each what you gave up in exchange. One sentence each.

---

## Part 2 — Derivations by Hand (20 minutes)

No computer for this part. Use the stratified grammar from Lecture 2 §5:

```bnf
E ::= E "+" T | T
T ::= T "*" F | F
F ::= n | "(" E ")"
```

**Q2.** Write the **leftmost** derivation of `n * n + n`. Every line, no skipping.

**Q3.** Write the **rightmost** derivation of the same string.

**Q4.** Draw the parse tree. **You should have drawn it once**, even though Q2 and Q3 produced different sequences. State in one sentence why that had to be true.

**Q5.** Draw the **AST** for the same string — the tree with the `E`, `T` and `F` nodes removed and only the operators and operands kept. How many nodes did the parse tree have, and how many does the AST have?

> **Q5 is the whole of phase 3 from Lecture 1 §5**, done by hand on one small input. In Week 2 you
> will write the code that does it, and it will be about fifteen lines.

---

## Part 3 — Watching Ambiguity Explode (20 minutes)

```bash
python3 cfg_count.py
```

**Q6.** Record the counts for 3, 6, 9 and 12 operands under the ambiguous grammar. They are the Catalan numbers. **Confirm the ratio:** divide each by its predecessor. The ratio approaches 4 — check whether it looks like it is heading there.

**Q7.** The demonstration ends by claiming *"both grammars generate exactly the same language."* The five rejected strings are evidence but not proof. **Give a string that would disprove it if the counter returned a non-zero count for one grammar and zero for the other**, and check your string. Did you manage to find a difference?

**Q8.** `( n + n ) * n` gets **one** parse tree even under the *ambiguous* grammar. Explain why, in terms of what the parentheses do to the available derivations.

### 3.1 Now break it yourself

Open `cfg_count.py` and add a third operator to the ambiguous grammar:

```python
AMBIGUOUS = {
    'E': [('E', '+', 'E'), ('E', '*', 'E'), ('E', '^', 'E'),
          ('n',), ('(', 'E', ')')],
}
```

**Q9.** Count the trees for `n + n * n ^ n`. Before you run it, **write down your prediction**. Then run it. Were you right?

---

## Part 4 — Fixing an Ambiguous Grammar (25 minutes)

Here is a grammar for a small boolean expression language. **It is ambiguous.**

```python
BOOL_AMBIGUOUS = {
    'B': [('B', 'or', 'B'), ('B', 'and', 'B'), ('not', 'B'),
          ('t',), ('f',), ('(', 'B', ')')],
}
```

**Q10.** Using the counter, find the number of parse trees for `t or f and t` and for `not t and f`. Show that both are greater than 1.

**Q11.** **Stratify it.** Write `BOOL_FIXED` with one non-terminal per precedence level, so that:

- `and` binds **tighter** than `or`
- `not` binds **tighter** than both
- `or` and `and` are both **left**-associative

**Q12.** Verify your grammar with the counter. It must give **exactly 1** for all of these:

```
t
not t
t or f
t and f
t or f and t
not t and f
t or f or t or f
not not t
( t or f ) and t
not ( t or f )
```

and **exactly 0** for all of these:

```
t or
or t
t t
not
( t
t and and f
```

**Do not move on until all sixteen pass.** If one fails, the counter is telling you something true about your grammar.

**Q13.** Your `not` rule is right-recursive — `N ::= "not" N | …` — and you were not told to make it left-recursive. **Why can a prefix operator not be left-recursive?** Answer in one sentence.

---

## Part 5 — Extending Cyan (25 minutes)

Cyan has no exponentiation. You are going to add one, and it has to obey two rules that pull in opposite directions:

- **`**` binds tighter than `*`** — so `2 * 3 ** 2` is `2 * (3 ** 2)` = 18
- **`**` is right-associative** — so `2 ** 3 ** 2` is `2 ** (3 ** 2)` = 512, not `(2 ** 3) ** 2` = 64

**Q14.** Where in the precedence ladder does the new non-terminal go? Write out the modified region of the grammar — you should be changing `mul_expr` and adding one rule.

**Q15.** Encode the whole Cyan expression grammar with your addition and verify with the counter. Every one of these must give exactly 1:

```
n mulop n pow n
n pow n pow n
n pow n mulop n
- n pow n
( n pow n ) pow n
n addop n pow n mulop n
```

**Q16.** Now the part that catches people. `- n pow n` — does your grammar parse it as `(-n) ** n` or `-(n ** n)`? **Check which one you got.** Python chose one of these and it surprises people every year:

```bash
python3 -c "print(-2 ** 2)"
```

Which did Python choose? Does your Cyan grammar agree? **If they disagree, that is a design decision, not a bug** — say which you think is better and why.

---

## Before You Leave

The TA checks:

- [ ] **Part 1** — every tool printed a version; all four paradigm programs ran
- [ ] **Part 2** — two derivations, one parse tree, one AST, on paper
- [ ] **Part 3** — Catalan counts recorded, Q9 prediction written down *before* running
- [ ] **Part 4** — `BOOL_FIXED` passing all sixteen checks, shown running
- [ ] **Part 5** — `**` added, six expressions at exactly 1, Q16 answered

**Keep `BOOL_FIXED` and your extended Cyan grammar.** Week 2 asks you to write a recursive descent parser, and a stratified grammar is the thing you turn directly into functions — one function per non-terminal. The work you did in Parts 4 and 5 is the design step of that parser, done early.

---

## If You Finish Early

**The dangling else, hands on.** Encode C's statement grammar:

```python
STMT = {
    'S': [('if', 'e', 'S'), ('if', 'e', 'S', 'else', 'S'), ('s',)],
}
```

Count the trees for `if e if e s else s`. Then work out what a *third* nested `if` does to the count — predict first, then check. Then encode Cyan's braced version and confirm it gives 1.

---

*Next: Week 1 — Lab 1 builds a lexer twice, once by hand as a DFA and once with `flex`, and compares them on the same input.*
