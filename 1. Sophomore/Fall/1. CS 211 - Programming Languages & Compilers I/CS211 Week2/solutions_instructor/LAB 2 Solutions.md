# CS 211 · Lab 2 · Solutions and Checkoff Notes
## Instructor Only

---

**Lab 2 is unmarked.** These notes exist so the checkoff is consistent.

> **Every count below was measured** with bison 3.8.2 and Python 3.14.2 against the shipped starter
> files. **Q13 is the checkoff that matters** — a student who leaves believing Cyan's grammar is
> ambiguous has missed the week.

---

## Part 1 — FIRST, FOLLOW, and LL(1)

### Q1 — The four conflicts

```
E on 'n': ('E', '+', 'T')  vs  ('T',)
E on '(': ('E', '+', 'T')  vs  ('T',)
T on 'n': ('T', '*', 'F')  vs  ('F',)
T on '(': ('T', '*', 'F')  vs  ('F',)
```

**The shape, in one sentence:** the left-recursive production and the base production have **identical FIRST sets**, because `E + T` begins with an `E`, which begins with a `T` — so one token of lookahead cannot choose between them.

**Accept** any phrasing of "the two alternatives start with the same tokens because the recursive one starts with the non-terminal itself".

### Q2 — Thirteen entries

FIRST/FOLLOW give:

| | FIRST | FOLLOW |
|---|---|---|
| `E` | `(`, `n` | `$`, `)` |
| `E'` | `+`, ε | `$`, `)` |
| `T` | `(`, `n` | `$`, `)`, `+` |
| `T'` | `*`, ε | `$`, `)`, `+` |
| `F` | `(`, `n` | `$`, `)`, `*`, `+` |

**Entries: E 2, E' 3 (`+` plus `$` and `)` for ε), T 2, T' 3, F 3 → 13.** *(Measured.)*

**The likely wrong prediction is 10** — one entry per production. The extra three come from **ε-productions, which get an entry for every token in FOLLOW**, not one entry.

### Q3 — Where the extra `+` comes from

**Three steps, and the student should be able to name all three.**

1. **`E → T E'`** puts `E'` immediately after `T`, so **FIRST(`E'`) ⊆ FOLLOW(`T`)**. FIRST(`E'`) = `{+, ε}`, so **`+` ∈ FOLLOW(`T`)**.
2. **`T → F T'`** ends with `T'`, so **FOLLOW(`T`) ⊆ FOLLOW(`T'`)**.
3. Therefore **`+` ∈ FOLLOW(`T'`)**.

**Why `E'` does not get it:** `E'` appears last in both `E → T E'` and `E' → + T E'`, so FOLLOW(`E'`) = FOLLOW(`E`) = `{$, )}` and nothing contributes a `+`. **The asymmetry is the interesting part** — `T'` inherits a `+` because a `T` can be followed by `+`, while an `E` never can.

**This question is harder than it looks.** Walk it through at the bench if more than a couple of students stall; the fixed-point flavour of FOLLOW is the thing that has not landed, and it returns in Week 4's dataflow analysis.

### Q4 — Chained comparison

**Left-recursive: NOT LL(1), 2 conflicts** (`E` on `n`, `A` on `n`). **After elimination: LL(1), 8 entries.** *(Measured.)*

### Q5 — Grammar or code?

**The grammar.** `The Cyan Language Reference` §3 writes

```ebnf
cmp_expr ::= add_expr [ ( "==" | ... ) add_expr ]
```

with `[ ... ]` — **optional, not repeated**. So `n cmp n cmp n` has **zero** parse trees; it is a syntax error by the grammar, verified in L02 §9.

**`parser.py` additionally raises a *friendly* error** rather than a generic parse failure, which is a code-level improvement to the message — not a different rule. **Accept a student who says "both": the grammar forbids it and the code improves the diagnosis.**

---

## Part 2 — The Dangling Else, Three Ways

### Q6 — Left-factored, still not LL(1)

```
S' on 'else': ('else', 'S')  vs  ('ε',)
```

**Why factoring did not help:** `else` is in **both** FIRST(`else S`) and FOLLOW(`S'`). Left factoring removes a *shared prefix*; this conflict is not about a shared prefix, it is about a genuine choice of where the `else` attaches. **The language is ambiguous, so no presentation of it is LL(1).**

### Q7 — bison's count

**1 shift/reduce conflict.**

### Q8 — The brackets

```
    ELSE  shift, and go to state 7
    ELSE      [reduce using rule 1 (stmt)]
```

**Square brackets mark the action bison *disabled*.** It kept the **shift**.

**Students often read the brackets as "also does this".** They mean the opposite — it is the road not taken, printed so you can see what the resolution cost.

### Q9 — The two derivations

- **Shift derivation:** the `ELSE` is inside the inner `stmt` → **binds to the inner (nearest) `if`.**
- **Reduce derivation:** the inner `if` reduces first → **binds to the outer `if`.**

**bison chose shift → nearest `if` → C's rule.**

### Q10 — One decision, four vocabularies

The decision: **an `else` attaches to the nearest unmatched `if`.**

| Tool | How it says so |
|---|---|
| **gcc** | Runs the program: prints nothing, and warns `-Wdangling-else` |
| **LL(1) table** | Conflict at `S'` on `else`; resolve by taking `else S` over ε |
| **bison** | Shift/reduce conflict in state 6; shift wins, reduce shown in brackets |
| **Cyan** | Does not arise — `block` requires braces, so there is no unbraced statement to attach to |

**Full marks for connecting all four.** The most common gap is not seeing that Cyan's answer is a *fourth* position — avoiding the question rather than answering it.

---

## Part 3 — Cyan's Own Conflict

### Q11 — The report

```
cyan.y: warning: 2 reduce/reduce conflicts [-Wconflicts-rr]
cyan.y: warning: reduce/reduce conflict on tokens '[', '.' [-Wcounterexamples]
```

**Two reduce/reduce conflicts, on `[` and `.`.** *(Measured.)*

**Note:** bison also emits `warning: empty rule without %empty` for `program : /* empty */`. **That is style, not a conflict** — students who report three warnings should be asked to distinguish them.

### Q12 — The two statements

```
First:   ... '{' IDENT • '[' expr ']' '=' expr ';' '}'
Second:  ... '{' IDENT • '[' expr ']' cmpop add_e ';' '}'
```

The first is an **assignment** (`x[i] = ...`); the second an **expression statement** (`x[i] < y;`).

**They diverge at the token after `]`** — `=` versus `cmpop`. **How many tokens after the ambiguity point?** The dot sits after `IDENT`; the distinguishing token comes after `[ expr ]`, and **`expr` is arbitrarily long**. So the answer is *unboundedly many* — which is exactly why one token of lookahead cannot do it.

**That "unbounded" is the point.** A student who answers "four" has counted the shortest case and missed why no LR($k$) for fixed $k$ helps either.

### Q13 — **Is the grammar ambiguous?**

**No.**

L02 §9 verified mechanically: **23 valid programs each parse to exactly one tree; 9 malformed ones to zero.** If the grammar were ambiguous some program would have two trees, and none does.

**What bison is reporting:** that the grammar is **not LALR(1)** — it cannot build a deterministic table with one token of lookahead. That is a decidable question about a *parsing method*.

**What bison is not reporting, and cannot:** that the grammar is ambiguous. **Ambiguity of a CFG is undecidable** (L02 §8), so no tool answers it in general. bison checks a *sufficient* condition for determinism; failing it means "could not prove", not "disproved".

**Checkoff standard.** The student must say all three of:
1. **No, it is not ambiguous**, and cite the Week 0 verification.
2. **bison decides LALR(1)-ness**, not ambiguity.
3. **The two questions are different**, and the second is undecidable.

**A student missing (3) is close enough to pass.** A student who says "yes, ambiguous" must be walked back through Week 0's counter before moving on — this is the one thing in Lab 2 worth stopping for.

### Q14 — The fix

```
assign_stmt : expr '=' expr ';' ;
```

and delete the `lvalue` rule.

```
$ bison -Wall -o cyan2_par.c cyan2.y ; echo "exit $?"
exit 0
```

**Zero conflicts.** *(Measured.)*

### Q15 — What rejects `3 = 4;` now

**Semantic analysis — Week 3** — or a shape check in the parser immediately after building the node, which is what `parser.py` does.

A good error message: **`line 1: left-hand side of '=' is not assignable`**, ideally naming what was found (`an integer literal`).

**Against a parse failure**, which would say something like `syntax error, unexpected '=', expecting ';'` — technically true, and it tells the programmer nothing about what they did wrong.

**This is the trade:** the grammatical version catches it earlier with a worse message; the shape check catches it later with a better one.

### Q16 — Is the reference wrong?

**No.** A language specification states what the language *is*, as precisely and readably as possible. **`lvalue` says exactly what may appear left of `=`, in the same formalism as everything else in the document** — a reader needs no separate prose rule.

An implementation is constrained by its **parsing technology**. bison cannot compile that rule into an LALR(1) table, so the generated parser encodes the same rule differently. **Two encodings of one language.**

**Accept any answer making the specification/implementation distinction.** **Do not accept** "the reference should be changed to match bison" — that is letting a tool limitation rewrite the language definition, and the whole point of §5 is that it does not have to.

---

## Part 4 — Precedence Declarations

### Q17

**Flat ambiguous grammar: 4 shift/reduce conflicts.** *(Measured.)*

```
%left '+'
%left '*'
```

**With the declarations: 0 conflicts, exit 0.** *(Measured.)* The grammar is textually unchanged — still `expr : expr '+' expr | expr '*' expr | INT`.

**If a student declares operators the grammar lacks** (`%left '+' '-'` with no `-` rule), bison warns `useless precedence and associativity for '-'`. **Harmless**, and worth pointing out as evidence for Q18.

### Q18 — Why Cyan stratifies instead

**Because `The Cyan Language Reference` is read by people who are not running bison.** A student implementing `parser.py` by hand gets the precedence from the grammar's structure directly — one non-terminal per level, which is one function per level. **A `%left` table is a bison feature and means nothing to a recursive descent parser.**

**Also accept:** the structural form keeps precedence in one place rather than two, so the two cannot drift — and Q17's `-Wprecedence` warning is a small example of exactly that drift being possible.

---

## Checkoff Summary

| Part | Minimum to pass |
|---|---|
| **1** | Four conflicts recorded; Q3's `+` traced through at least one step of the chain |
| **2** | All four tools run; Q8's brackets understood correctly |
| **3** | **Q13 answered with points 1 and 2**; bison exiting 0 after the Q14 fix |
| **4** | 4 conflicts before, 0 after |

**If a student is short on time, cut Part 1's Q3 and Part 4 entirely.** Do not cut Q13.

---

*CS 211 · Lab 2 Solutions · Instructor Only*
