# CS 211 · Programming Languages & Compilers I
## Week 0 · Lecture 2 of 2
### Grammars, Derivations, and Ambiguity

---

**Reading:** Dragon §2.2, §4.2–4.3 · **Next:** Week 1, L03 — from grammar to a working lexer

---

## 1. A Finite Rulebook for an Infinite Language

There are infinitely many valid Cyan programs and you cannot list them. **You can list the rules that generate them**, and that finite list is a *grammar*.

Formally, a **context-free grammar** is a four-tuple $G = (N, \Sigma, P, S)$:

| | | Example |
|---|---|---|
| $N$ | **Non-terminals** — the structural categories | `expr`, `stmt`, `block` |
| $\Sigma$ | **Terminals** — the tokens the lexer will hand you | `+`, `if`, `(`, an integer literal |
| $P$ | **Productions** — rules of the form $A \to \alpha$ | `expr → expr + term` |
| $S$ | **The start symbol**, one of the non-terminals | `program` |

**The language $L(G)$ is the set of terminal strings derivable from $S$.** That is the definition, and it is worth reading twice: the grammar does not *check* strings, it *generates* them. Parsing — deciding whether a given string is in $L(G)$, and if so how — is the inverse problem, and it is Week 2.

**Why "context-free"?** Because a production may fire wherever its non-terminal appears, regardless of what surrounds it. `expr → expr + term` applies to *every* `expr`, with no clause about the neighbours. Context-*sensitive* grammars allow rules like $\alpha A \beta \to \alpha \gamma \beta$ — "rewrite $A$ as $\gamma$, but only between $\alpha$ and $\beta$." Programming languages do not use those, for a reason §8 gets to.

---

## 2. BNF and EBNF

**Backus–Naur Form** is the notation, invented for ALGOL 60 by John Backus and Peter Naur — the first time anyone wrote a language's syntax down formally rather than in prose and examples.

```bnf
<expr> ::= <expr> "+" <term> | <term>
<term> ::= <term> "*" <factor> | <factor>
<factor> ::= NUMBER | "(" <expr> ")"
```

**EBNF** adds three shorthands, and they matter mostly for readability:

| Notation | Means | Longhand BNF |
|---|---|---|
| `{ X }` | zero or more `X` | `L ::= L X \| ε` |
| `[ X ]` | optional `X` | `O ::= X \| ε` |
| `( X \| Y )` | grouping | a fresh non-terminal |

**EBNF adds no power.** Anything you can write in EBNF you can write in BNF with more non-terminals; the languages describable are exactly the same. It is sugar, and this course writes EBNF because a grammar you can read is a grammar whose bugs you can see.

---

## 3. Derivations — and Why They Are Not the Interesting Object

A **derivation** is a sequence of rule applications from $S$ to a terminal string. For `n + n * n`:

**Leftmost** (always expand the leftmost non-terminal):

```
expr ⇒ expr + term ⇒ term + term ⇒ factor + term ⇒ n + term
     ⇒ n + term * factor ⇒ n + factor * factor ⇒ n + n * factor ⇒ n + n * n
```

**Rightmost** (always the rightmost):

```
expr ⇒ expr + term ⇒ expr + term * factor ⇒ expr + term * n
     ⇒ expr + factor * n ⇒ expr + n * n ⇒ term + n * n ⇒ factor + n * n ⇒ n + n * n
```

**Different sequences. Same tree.** And the tree is what matters — the order in which you happened to expand non-terminals is an artefact of how you walked, not a fact about the program.

> **This distinction becomes load-bearing in Week 2.** Top-down parsers (recursive descent) build a
> *leftmost* derivation; bottom-up parsers (LR) build a *rightmost* one in reverse. They are
> different algorithms producing the same tree, which is why you can swap one for the other without
> the rest of the compiler noticing.

**A parse tree** records every non-terminal: `expr`, `term`, `factor`, all of it. **An AST** keeps only what carries meaning. The parse tree for `n + n * n` has ten nodes; the AST has five. Phase 3 from L01 is exactly the step that throws the other five away.

---

## 4. Ambiguity, Counted

**A grammar is ambiguous if some string in its language has more than one parse tree.**

Here is the grammar you would write first, before knowing better:

```bnf
E ::= E "+" E | E "*" E | NUMBER | "(" E ")"
```

It is short, it is obvious, and it is broken. Count the parse trees it admits:

```
$ python3 cfg_count.py
```

```
Additions only:  n + n + ... + n
 operands | ambiguous G | stratified G
        1 |           1 |            1
        2 |           1 |            1
        3 |           2 |            1
        4 |           5 |            1
        5 |          14 |            1
        6 |          42 |            1
        7 |         132 |            1
        8 |         429 |            1
       10 |        4862 |            1
       12 |       58786 |            1
```

**`n + n + n + n + n + n + n + n + n + n + n + n` has 58,786 distinct parse trees.** Those are the **Catalan numbers** $C_{k-1}$ for $k$ operands — the count of ways to bracket a sequence — and they grow roughly as $4^k / k^{1.5}$. A twenty-operand expression has over 1.7 billion.

The mixed-operator cases are where it actually hurts:

```
  n + n * n          ambiguous:   2   stratified: 1
  n * n + n          ambiguous:   2   stratified: 1
  n + n * n + n      ambiguous:   5   stratified: 1
  ( n + n ) * n      ambiguous:   1   stratified: 1
```

**`n + n * n` has two trees**: $(n + n) \times n$ and $n + (n \times n)$. Those evaluate to different numbers. The grammar, as written, does not say which one your language means — so the language does not yet have a meaning.

**Note the parenthesised case: one tree, even under the broken grammar.** Parentheses were never about readability. They are the programmer overriding the grammar's choice, and where the programmer has spoken there is nothing left to be ambiguous about.

---

## 5. The Fix: Stratify by Precedence

You do not fix ambiguity by adding a rule that says "multiplication binds tighter". **You fix it by making the grammar structurally incapable of producing the other tree.**

```bnf
E ::= E "+" T | T          <- one level per precedence tier
T ::= T "*" F | F
F ::= NUMBER | "(" E ")"
```

**Every precedence level gets its own non-terminal, and the tighter-binding one sits lower.** `E` can only ever have `T`s as its operands, and a `T` has already absorbed all the multiplication available — so multiplication is *forced* into the subtree. The tree you want is the only tree there is.

**Associativity comes from which side recurses.** `E ::= E "+" T` is *left*-recursive, so `a + b + c` groups as `(a + b) + c`. Write `E ::= T "+" E` and you would get right-associativity instead.

> **That choice is not cosmetic, as CS 201 Week 1 established.** In floating point, addition is not
> associative: with `a = 1e16, b = -1e16, c = 1.0`, Python gives `(a+b)+c = 1.0` and
> `a+(b+c) = 0.0`. **Your grammar's recursion side decides which answer your language produces.**
> Verified, Python 3.14.2.

The verified result: the stratified grammar gives **exactly one parse tree for every one of those strings**, and rejects exactly the same malformed strings the ambiguous one did:

```
Rejected strings (must be 0 in both):
  n +        ambiguous: 0   stratified: 0
  n n        ambiguous: 0   stratified: 0
  n + + n    ambiguous: 0   stratified: 0
```

**Both grammars generate the identical language.** They differ only in how many trees they admit per string. **Ambiguity is a property of a grammar, not of a language** — a point worth holding onto, because a lot of confusion in Week 2 comes from conflating the two.

---

## 6. The Dangling Else — Ambiguity Stratification Cannot Fix

```bnf
stmt ::= "if" expr stmt | "if" expr stmt "else" stmt | ...
```

Now parse `if a if b s1 else s2`. **Does the `else` belong to the outer `if` or the inner one?** Both parses are legal and no precedence tier separates them, because the conflict is not about precedence at all.

C resolves it by fiat — *the `else` binds to the nearest unmatched `if`* — which is a rule about the parser, not about the grammar. Watch what that costs:

```c
#include <stdio.h>
int main(void) {
    int a = 0, b = 0;
    if (a == 1)
        if (b == 1) printf("inner-then\n");
    else printf("ELSE TAKEN\n");
    printf("done\n");
    return 0;
}
```

**Read the indentation.** It says the `else` belongs to `if (a == 1)`, and since `a` is `0`, `ELSE TAKEN` should print.

```
$ gcc -Wall -o dangling dangling.c && ./dangling
dangling.c:4:8: warning: suggest explicit braces to avoid ambiguous 'else' [-Wdangling-else]
done
```

**`ELSE TAKEN` never printed.** The `else` bound to the inner `if (b == 1)`, which is unreachable because `a` is not `1`. The indentation is a lie, and the compiler knows it is a lie — `-Wdangling-else` fires, and it is on by default under `-Wall`.

**Cyan does not have this problem, because Cyan refuses to have it:**

```ebnf
if_stmt ::= "if" expr block [ "else" ( if_stmt | block ) ]
block   ::= "{" { stmt } "}"
```

**The branches are `block`s, so the braces are mandatory.** There is no unbraced statement for an `else` to attach to ambiguously, and the grammar is unambiguous with no side rule. Rust and Go make the same choice. **The cost is that you must type braces around a one-line branch forever** — which is exactly the trade in habit 2, paid in keystrokes and refunded in a class of bug that cannot occur.

---

## 7. Three Languages, Three Answers to `a < b < c`

One more, because it shows the same trade with three different resolutions. Let `a = 1, b = 5, c = 3`. Mathematically the claim "$1 < 5 < 3$" is false.

**C parses it as `(a < b) < c`:**

```
$ gcc -Wall -Wextra -o chain chain.c && ./chain
chain.c:5:46: warning: comparisons like 'X<=Y<=Z' do not have their mathematical meaning [-Wparentheses]
a < b < c  evaluates to 1
  because (a<b) is 1, and 1 < c is 1
```

**C says true.** `a < b` is `1`, and `1 < 3` is true. Internally consistent, mathematically nonsense, and again the compiler warns.

**Python adds a grammar rule for chained comparison:**

```
a < b < c  evaluates to False (chained: a<b AND b<c)
```

**Python says false**, the mathematically right answer, bought with a special production that desugars `a < b < c` into `a < b and b < c` — with `b` evaluated once.

**Cyan makes comparison non-associative and rejects it outright:**

```ebnf
cmp_expr ::= add_expr [ ( "==" | "!=" | "<" | "<=" | ">" | ">=" ) add_expr ]
```

The `[ ... ]` is optional, not repeated — **so `n < n < n` has zero parse trees and is a syntax error.** Verified against the grammar checker: `n cmpop n cmpop n → 0`.

| | Answer | Bought | Paid |
|---|---|---|---|
| **C** | `true` | one uniform rule for all binary operators | a silently wrong result |
| **Python** | `false` | the mathematical meaning | a special case in the grammar |
| **Cyan** | *syntax error* | no wrong answer is expressible | you must write `a < b && b < c` |

**Three defensible designs. No free one.**

---

## 8. What Grammars Cannot Do

CFGs are not powerful enough to describe a programming language — only its *syntax*. None of these can be expressed by any context-free grammar:

- **A variable must be declared before it is used.**
- **A function call must supply the number of arguments the declaration takes.**
- **Both sides of `=` must have compatible types.**

Each requires remembering something from an arbitrarily distant part of the program, and "context-free" is precisely the promise not to do that. **This is not a defect — it is the reason parsing is fast.** A CFG can be parsed in linear time; the context-sensitive languages cannot.

**So the compiler does it in the next phase instead.** Everything on that list is checked in Week 3 by walking the AST with a symbol table. The division of labour is deliberate: the grammar gets the tree shape, and semantic analysis gets everything that needs memory.

**But do not push things across that line too eagerly.** "The left-hand side of an assignment must be assignable" *sounds* like it belongs in semantic analysis. It does not. Write the rule as

```ebnf
assign_stmt ::= lvalue "=" expr ";"
lvalue      ::= IDENT | lvalue "[" expr "]" | lvalue "." IDENT
```

and `3 = 4;` has **zero** parse trees — rejected by the parser, with a syntax error, before any symbol table exists. Write it as `postfix "=" expr ";"` instead and `3 = 4;` parses cleanly and has to be caught later with a worse error message. **The Cyan grammar was written the second way first, and the ambiguity checker in §9 is what caught it.** Deciding which checks the grammar can carry is a real design skill, and the default answer is *more than you would guess*.

> **One more limit, and it is a strong one: deciding whether an arbitrary CFG is ambiguous is
> *undecidable*.** There is no algorithm that reads a grammar and answers yes or no in general. What
> tools like `bison` do instead is check a *sufficient* condition — is this grammar LALR(1)? — and
> report a conflict if not. A conflict means "I could not prove this unambiguous", which is not the
> same as "this is ambiguous". You will meet that distinction in Week 2, usually at the point where
> bison reports 2 shift/reduce conflicts and you have to work out whether they matter.

---

## 9. The Cyan Expression Grammar

This is the grammar you will implement. It is fixed now and does not change until Week 8 adds generics.

```ebnf
expr     ::= or_expr
or_expr  ::= and_expr { "||" and_expr }
and_expr ::= cmp_expr { "&&" cmp_expr }
cmp_expr ::= add_expr [ ( "==" | "!=" | "<" | "<=" | ">" | ">=" ) add_expr ]
add_expr ::= mul_expr { ( "+" | "-" ) mul_expr }
mul_expr ::= unary { ( "*" | "/" | "%" ) unary }
unary    ::= [ "-" | "!" ] postfix
postfix  ::= primary { "(" [ args ] ")" | "[" expr "]" | "." IDENT }
primary  ::= INT | STRING | "true" | "false" | IDENT | "(" expr ")"
```

**Seven precedence levels, lowest to highest.** Read it top to bottom and it is the precedence table of every C-family language you have used, written as structure instead of as a chart you memorise.

**It is verified unambiguous** — 33 well-formed expressions each parse to exactly one tree, 11 malformed ones to zero, checked mechanically by the same counter that found 58,786 trees in §4. The full listing is in `resources/The Cyan Language Reference.md`, along with the statement and declaration grammar.

---

## 10. What to Take Away

1. **A grammar is a finite generator for an infinite language**, and $L(G)$ is defined by derivation, not by checking.
2. **Derivation order is an artefact; the tree is the object.** Leftmost and rightmost derivations of the same string give the same tree.
3. **Ambiguity is countable and it explodes** — Catalan numbers, 58,786 trees for twelve operands.
4. **You fix ambiguity structurally**, one non-terminal per precedence level, with the recursion side setting associativity.
5. **Ambiguity is a property of the grammar, not the language.** Two grammars can generate the same strings and disagree entirely on trees.
6. **Some ambiguity is not about precedence** — the dangling else is fixed by requiring braces, or lived with via a parser-level rule and a compiler warning.
7. **Grammars cannot express declare-before-use, arity, or type compatibility.** That is Week 3's job, and the split is what keeps parsing linear.

---

## Exercises

1. Give a string with exactly **three** parse trees under `E ::= E "+" E | E "*" E | n`. Draw all three.
2. The Catalan numbers count bracketings. Explain, in one or two sentences, why the *same* count applies to parse trees of `n + n + ... + n`.
3. Rewrite `add_expr` so that `-` becomes **right**-associative. Then evaluate `10 - 3 - 2` under both versions and say which one matches every language you have used.
4. Cyan's `cmp_expr` uses `[ ... ]`, not `{ ... }`. Change it to `{ ... }` and describe precisely which strings become legal, and what tree `a < b < c` would then get.
5. Add an exponentiation operator `**` to the Cyan grammar. It must bind **tighter than `*`** and be **right**-associative, so `2 ** 3 ** 2` is `2 ** (3 ** 2)` = 512. Where in the ladder does its non-terminal go, and which side recurses?
6. The dangling else can also be removed by requiring a closing keyword — `if ... then ... else ... endif`, as Ada and Visual Basic do. Compare that against Cyan's mandatory braces: what does each cost the programmer, and do they buy the same thing?
7. Explain why "every variable is declared before use" cannot be a context-free rule, using the definition of context-freeness from §1 rather than an appeal to intuition.

---

*Next: Week 1 — the lexer. Regular expressions, finite automata, and why the first phase of the compiler is the one phase that provably does not need a stack.*
