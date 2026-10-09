# CS 211 · Programming Languages & Compilers I
## Week 2 · Lecture 2 of 2
### Bottom-Up Parsing, and What Bison Is Telling You

*“There will always be things we wish to say in our programs that in all known languages can only be said poorly.”* — Alan Perlis, "Epigrams on Programming" (1982), #26

---

**Reading:** Dragon §4.5–4.7 · **Next:** Week 3, L07 — the symbol table and what a name means

**Coursework:** 📝 **PS 1** due Fri this week 17:00 · 🔬 **Lab 2** Fri this week 14:00–15:50 · 📊 **Quiz 3** Tue of Week 3 · 📝 **PS 3** released Wed of Week 3, due Fri of Week 4 17:00 · 📘 **Midterm 1** Wed of Week 4 20:00–21:15

---

## 1. The Other Direction

Recursive descent starts at the root and guesses downward. **Bottom-up parsing starts at the leaves and builds upward**, and it never guesses — it waits until it has seen enough.

The mechanism is a **stack** and two actions:

| Action | Meaning |
|---|---|
| **Shift** | Push the next input token onto the stack |
| **Reduce** | The top of the stack matches a production's right-hand side. Pop it, push the left-hand side |

**Parsing `n + n * n`** with `E ::= E+T | T`, `T ::= T*F | F`, `F ::= n`:

| Stack | Input | Action |
|---|---|---|
| | `n + n * n $` | shift |
| `n` | `+ n * n $` | reduce `F → n` |
| `F` | `+ n * n $` | reduce `T → F` |
| `T` | `+ n * n $` | reduce `E → T` |
| `E` | `+ n * n $` | shift |
| `E +` | `n * n $` | shift |
| `E + n` | `* n $` | reduce `F → n` |
| `E + F` | `* n $` | reduce `T → F` |
| `E + T` | `* n $` | **shift** — *not* reduce `E → E+T` |
| `E + T *` | `n $` | shift |
| `E + T * n` | `$` | reduce `F → n` |
| `E + T * F` | `$` | reduce `T → T*F` |
| `E + T` | `$` | reduce `E → E+T` |
| `E` | `$` | **accept** |

**Look at row 9.** The stack holds `E + T`, which is exactly the right-hand side of `E → E+T`. **It could reduce. It must not** — the `*` coming up means the `T` is not finished. **Knowing when not to reduce is the whole problem**, and it is what the tables in §3 encode.

> **This produces a *rightmost* derivation, in reverse.** Each reduction is a derivation step read
> backwards, and the steps come out in the order that reverses a rightmost derivation. L02 §3
> promised both derivations give the same tree; this is the algorithm for the other one.

**And notice what did not happen: left recursion caused no trouble at all.** `E → E+T` was reduced without complaint. **Bottom-up parsers handle left recursion natively** — they never call themselves, so there is nothing to recurse infinitely. That is their first real advantage over L05.

---

## 2. Items and the LR(0) Automaton

**How does the parser know whether to shift or reduce?** It tracks, for every production it might be in the middle of, *how far in it is*.

An **item** is a production with a dot marking the position:

```
E → E · + T        "I have an E; if I see +, this could be it"
E → E + T ·        "I have the whole thing; I could reduce"
```

**A parser state is a set of items** — everything that might be true at once. And here is the key fact:

> **The set of reachable item-sets is finite, so the states form a finite automaton.**

That automaton — the **LR(0) automaton** — is the parser's brain. It runs over the *stack*, not the input. **The stack contents plus the automaton's state tell you what is reduceable**, and because the stack is unbounded, the combination has the power a plain DFA lacked in L04 §7.

**Two kinds of conflict can appear in a state:**

| Conflict | Means |
|---|---|
| **shift/reduce** | One item says reduce, another says shift the same token |
| **reduce/reduce** | Two different items both say reduce |

---

## 3. SLR, LALR, and Why bison Uses the Middle One

LR(0) alone reduces whenever an item's dot reaches the end — with no lookahead, so it conflicts constantly. The variants differ in **how much lookahead they use to decide whether to reduce**:

| | Reduce $A \to \alpha$ when the next token is… | Table size | Power |
|---|---|---|---|
| **LR(0)** | always | small | very weak |
| **SLR(1)** | in FOLLOW($A$) | small | weak |
| **LALR(1)** | in a *context-specific* lookahead set | **small** | **strong enough** |
| **LR(1)** | in a lookahead computed per item-with-context | **large** | strongest |

**LR(1) is the powerful one and its tables are enormous** — states can number in the tens of thousands for a real language. **LALR(1) merges LR(1) states that differ only in lookahead**, recovering LR(0)'s state count while keeping nearly all the power.

**That merge is why `bison` uses LALR(1)**, and it is almost free: the merge can introduce reduce/reduce conflicts that pure LR(1) would not have, but for real programming-language grammars it essentially never does.

**The containment is strict:** LL(1) ⊂ SLR(1) ⊂ LALR(1) ⊂ LR(1). **Every LL(1) grammar is LALR(1); the converse fails badly** — which is the second advantage of bottom-up parsing. The left-recursive expression grammar that was *not* LL(1) in L05 §4 is LALR(1) without modification.

---

## 4. What bison Actually Reports

Give bison the ambiguous dangling-else grammar:

```
%token IF E S ELSE
%%
stmt : IF E stmt
     | IF E stmt ELSE stmt
     | S
     ;
```

```
$ bison -Wall -o dangling.c dangling.y
dangling.y: warning: 1 shift/reduce conflict [-Wconflicts-sr]
dangling.y: note: rerun with option '-Wcounterexamples' to generate conflict counterexamples
```

**One shift/reduce conflict.** *(Measured, bison 3.8.2.)* Ask where:

```
$ bison -Wall --report=all -o dangling.c dangling.y
```

```
State 6

    1 stmt: IF E stmt •  [$end, ELSE]
    2     | IF E stmt • ELSE stmt

    ELSE  shift, and go to state 7

    ELSE      [reduce using rule 1 (stmt)]
    $default  reduce using rule 1 (stmt)
```

**Read that carefully, because reading it is the skill.**

- Two items. The dot is at the end of rule 1 — **reduce is possible.** The dot is before `ELSE` in rule 2 — **shift is possible.**
- `ELSE shift, and go to state 7` — **bison chose shift.**
- `ELSE [reduce using rule 1]` — **the square brackets mean this action was disabled.** That is bison telling you which alternative it discarded.

### The counterexample

```
$ bison -Wcounterexamples -o dangling.c dangling.y
```

```
warning: shift/reduce conflict on token ELSE [-Wcounterexamples]
  Example: IF E IF E stmt • ELSE stmt
  Shift derivation
    stmt
    ↳ 1: IF E stmt
              ↳ 2: IF E stmt • ELSE stmt
  Reduce derivation
    stmt
    ↳ 2: IF E stmt             ELSE stmt
              ↳ 1: IF E stmt •
```

**This is the dangling else, drawn as two trees.** In the shift derivation the `ELSE` sits inside the *inner* `stmt` — it binds to the inner `if`. In the reduce derivation the inner `if` closes first and the `ELSE` belongs to the *outer* one.

> **`-Wcounterexamples` is the single most useful bison flag and almost nobody knows it exists.**
> Before it, diagnosing a conflict meant reading item sets by hand. Now the tool shows you the two
> programs that parse differently. **Use it every time.**

### bison's default resolution

**Shift wins.** That is bison's rule for every shift/reduce conflict, and here it means *the `else` binds to the nearest unmatched `if`* — **C's rule**, and exactly the behaviour gcc demonstrated in L02 §6 when it printed nothing and warned `-Wdangling-else`.

**Three views of one fact, now assembled:** gcc's runtime behaviour in Week 0, the LL(1) table conflict in L05 §5, and bison's state 6 here. **Same ambiguity, three different tools, three different vocabularies.**

---

## 5. A Conflict Is Not Necessarily A Bug

**This is the part that costs people days.**

L02 §8 said ambiguity of a CFG is *undecidable*. bison cannot therefore answer "is this grammar ambiguous?" **What it answers is "is this grammar LALR(1)?"** — a decidable question, and a *sufficient* condition.

**So a conflict means one of two very different things:**

| | |
|---|---|
| **The grammar is genuinely ambiguous** | The dangling else. Fix the language or accept the default resolution deliberately |
| **The grammar is unambiguous but not LALR(1)** | The tool could not prove it. Rewrite the grammar; the language is fine |

**"bison reported a conflict" does not mean "my grammar is ambiguous."** It means bison could not prove otherwise with one token of lookahead in a merged automaton. **Reading the counterexample is how you tell the cases apart** — if the two derivations produce trees you would consider equally valid programs, it is real ambiguity; if one of them is nonsense you would never want, it is a tooling limitation.

> **The dangerous habit** is suppressing conflicts with `%expect 1` without reading them. That
> declares "I know about exactly one conflict and have accepted its resolution". **It is a
> reasonable thing to write and a terrible thing to write reflexively**, because it silences the
> next one too.

### Cyan is case 2, and you can prove it

Write `The Cyan Language Reference` grammar as a bison file — the whole thing, declarations, statements and expressions — and run it:

```
$ bison -Wall -Wcounterexamples -o cyan_par.c cyan.y
cyan.y: warning: 2 reduce/reduce conflicts [-Wconflicts-rr]
cyan.y: warning: reduce/reduce conflict on tokens '[', '.' [-Wcounterexamples]
  First example:  ... '{' IDENT • '[' expr ']' '=' expr ';' '}'
  Second example: ... '{' IDENT • '[' expr ']' cmpop add_e ';' '}'
```

*(Measured, bison 3.8.2.)*

**Two reduce/reduce conflicts, on `[` and `.`.** The counterexample says exactly what is wrong: seeing `IDENT` at the start of a statement, the parser must reduce it to **`lvalue`** (if this turns out to be `x[i] = ...`) or to **`prim`** (if it turns out to be the expression statement `x[i] < y;`). **Both start identically and diverge arbitrarily far to the right.**

**Now — is the Cyan grammar ambiguous?**

**No, and this is not an opinion.** L02 §9 verified it mechanically: 23 valid programs each parse to exactly **one** tree, 9 malformed ones to zero. **There is no second tree for bison to be confused between.**

**So this is case 2 exactly.** The grammar is unambiguous; LALR(1) cannot *prove* it with one token of lookahead, because the distinguishing token — the `=` — can be arbitrarily far away. **bison is reporting a limitation of bison.**

**The fix is the one every real compiler uses:** drop `lvalue` from the grammar, let assignment take an `expr` on the left, and check the shape afterwards.

```
assign_stmt : expr '=' expr ';' ;
```

```
$ bison -Wall -o cyan2_par.c cyan2.y
$ echo $?
0
```

**Zero conflicts.** *(Measured.)* And `parser.py` from L05 already does precisely this — it parses an expression, then calls `is_lvalue` before accepting `=`, which is why L05 §6's error message is *"left-hand side of `=` is not assignable"* rather than a parse failure.

> **Three positions on one rule, all defensible.** The *reference grammar* states it structurally,
> which documents the language best. **bison** cannot compile that, so the generated parser states
> it as a shape check. **`parser.py`** does the shape check too, and gets a better error message out
> of it. **The specification and the implementation disagree on purpose**, and the reference is
> still the authority on what Cyan *is*.

---

## 6. Precedence Declarations

For the common case — arithmetic — bison lets you resolve conflicts without touching the grammar:

```
%left  '+' '-'
%left  '*' '/'
%right UMINUS
```

**Earlier lines bind looser; `%left` means reduce on a tie, `%right` means shift.** With these, the ambiguous one-line grammar `E : E '+' E | E '*' E | n` parses correctly, conflicts and all resolved.

**This is the stratified grammar from L02 §5, expressed as a table instead of as structure.** Same information, two encodings:

| | Precedence in the grammar | Precedence in a `%left` table |
|---|---|---|
| **Grammar size** | one non-terminal per level — Cyan has seven | one rule, flat |
| **Self-documenting?** | yes — the structure *is* the precedence | no — you must read two places |
| **Works with recursive descent?** | yes | **no** — it is an LR table feature |

**Cyan uses the structural version**, because `The Cyan Language Reference` must be readable by someone with no parser generator, and because L05's hand-written parser needs the levels anyway.

---

## 7. Which One Should You Use?

| | Recursive descent | LALR(1) generator |
|---|---|---|
| Left recursion | **breaks** — needs a loop | **native** |
| Grammar class | LL(1)-ish, with hacks | strictly larger |
| Error messages | **excellent** — you write them | mechanical |
| Debuggability | a stack trace you can read | an item-set report you must learn |
| Grammar changes | edit one function | rerun, re-read conflicts |
| Ambiguity | you will not notice | **reported** |

**The last row is the honest case for bison even if you ship a hand-written parser.** L05's `parser.py` will happily parse an ambiguous grammar — it just silently picks whatever its code order implies, and never tells you the other tree existed. **bison would have told you.**

**What production compilers do:** hand-written recursive descent for the shipping parser, because error messages matter more than anything else on that list — **and a bison grammar kept alongside as a specification and an ambiguity check.** That is not a compromise; it is using each tool for what it is good at.

---

## 8. What to Take Away

1. **Shift and reduce**, over a stack. The hard part is knowing when *not* to reduce.
2. **Items track how far into a production you are**, and the reachable item-sets form a finite automaton running over the stack.
3. **LALR(1) merges LR(1) states** to get LR(0)'s size with nearly LR(1)'s power. That is why bison uses it.
4. **LL(1) ⊂ SLR(1) ⊂ LALR(1) ⊂ LR(1)**, strictly. Left-recursive grammars are fine bottom-up.
5. **Read the conflict report**: bracketed actions are the ones bison disabled, and `-Wcounterexamples` shows you the two derivations.
6. **bison shifts by default**, which for the dangling else means binding to the nearest `if` — gcc's behaviour, reached from a third direction.
7. **A conflict means "not provably LALR(1)", not "ambiguous."** Telling the two apart requires reading, not suppressing.

---

## Exercises

1. Trace `n * n + n` bottom-up as in §1. At which row must the parser *not* reduce, and what tells it so?
2. In the state-6 report, `$default reduce using rule 1` appears alongside the shift. **Explain why both are listed** and what `$default` covers.
3. §5 removed Cyan's two reduce/reduce conflicts by letting `assign_stmt` take an `expr` on the left. **What does the resulting grammar now accept that Cyan does not permit?** Say which phase must reject it, and what the error message should be.
4. Write a grammar that is **unambiguous but not LALR(1)**. *(Hint: needs more than one token of lookahead to decide a reduction.)* Confirm with bison that it conflicts.
5. `%left '+'` versus stratifying the grammar: give one concrete situation where the `%left` version is clearly better, and one where it is clearly worse.
6. §7 claims a hand-written parser "will happily parse an ambiguous grammar and never tell you". **Demonstrate it**: find a change to `parser.py` that makes it accept an ambiguous language, and say which tree it silently picks.
7. bison resolves shift/reduce by shifting. **What would the dangling else do if it resolved by reducing?** Give the resulting binding rule, and name a language that uses it.

---

*Next week: the tree is built, and the compiler still does not know that `x` is an `int` or that `fib` takes one argument. Week 3 is the phase that finds out — and the first one that can reject a program the grammar was perfectly happy with.*
