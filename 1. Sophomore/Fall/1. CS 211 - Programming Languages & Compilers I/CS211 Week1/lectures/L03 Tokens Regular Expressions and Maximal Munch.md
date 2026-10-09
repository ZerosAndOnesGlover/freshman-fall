# CS 211 · Programming Languages & Compilers I
## Week 1 · Lecture 1 of 2
### Tokens, Regular Expressions, and Maximal Munch

*“Some people, when confronted with a problem, think "I know, I'll use regular expressions." Now they have two problems.”* — Jamie Zawinski, alt.religion.emacs (1997)

---

**Reading:** Dragon §3.1–3.3 · **Next:** L04, finite automata and the subset construction

**Coursework:** 📊 **Quiz 1** today · 📝 **PS 1** released Wed this week, due Fri of Week 2 17:00 · 📝 **PS 0** due Fri this week 17:00 · 🔬 **Lab 1** Fri this week 14:00–15:50

---

## 1. Phase One of Eight

Last week established that a program is a tree. **This week is about the step before the tree exists at all.**

The parser in Week 2 will want to reason about `if`, `IDENT`, `(`, `<=` — structural units. What it is handed is a flat sequence of bytes:

```
i f   n   < =   2   {
```

**The lexer's job is to turn characters into tokens**, and it is the only phase of the compiler that ever looks at an individual character. Everything downstream works on tokens.

A **token** carries three things:

| | Example | Why it is kept |
|---|---|---|
| **A kind** | `IDENT`, `INT`, `KEYWORD`, `OP` | What the parser matches on |
| **The text** ("lexeme") | `fib`, `42`, `<=` | The parser mostly ignores it; later phases need it |
| **A position** | line 7, column 12 | **Error messages.** This is the only reason it exists |

**That third field is not optional.** A compiler that can say *"line 7: undefined variable `fbi`"* is a usable tool; one that says *"undefined variable"* is not. Position is captured here, in the lexer, and threaded through every later phase — and it is the single most common thing students forget to carry, usually discovering it in Week 3 when the type checker has an error to report and nowhere to point.

---

## 2. Why This Is a Separate Phase

You could, in principle, fold lexing into parsing. Nobody does. Three reasons, in ascending order of importance:

**1. Simplicity.** The parser's grammar would have to spell out that an identifier is a letter followed by letters-or-digits, at every point an identifier can appear. Separating them means the grammar says `IDENT` and moves on.

**2. Speed.** The lexer is the only phase that touches every byte. It is worth making fast, and it can be made fast precisely because — as §4 will show — it needs no stack and no backtracking.

**3. It is provably enough.** This is the real reason. **Tokens are a regular language, and the tree is not.** Those are different classes of formal power, and the phase split falls exactly on that boundary — which is why it is a clean split rather than an arbitrary one.

> **The split has a cost, and you should know it.** Because the lexer runs first and knows nothing
> about syntax, it cannot use context to disambiguate. C's famous `a * b;` — is that a
> multiplication or a declaration of `b` as a pointer to `a`? — cannot be settled by the lexer, and
> the workaround real C compilers use is a feedback channel from the parser back into the lexer,
> universally called *"the lexer hack"*. Cyan avoids it by having no typedefs.

---

## 3. Regular Expressions Are a Specification, Not a Library

The `re` module you have used in Python is a tool. **What we mean here is the formal object**, which is smaller and better behaved.

A regular expression over an alphabet $\Sigma$ is built from exactly four things:

| Form | Means | Cyan example |
|---|---|---|
| $a$ | the single character $a$ | `+` |
| $r s$ | $r$ followed by $s$ | `->` |
| $r \mid s$ | $r$ or $s$ | `true|false` |
| $r^*$ | zero or more $r$ | `[0-9]*` |

**That is the whole language.** `r+` is $rr^*$, `r?` is $r \mid \varepsilon$, `[a-z]` is a union of twenty-six alternatives. **They are abbreviations and add no power** — exactly as EBNF adds no power to BNF.

**What is deliberately absent:** backreferences. Python's `re` lets you write `(a+)\1`, matching a string followed by a copy of itself. **That is not a regular expression**, it is strictly more powerful, and it is why Python's engine can take exponential time on some patterns while a lexer never can. The formal object has no such trapdoor.

### Cyan's token classes

Straight from `The Cyan Language Reference` §2:

```
IDENT   ::=  [A-Za-z_] [A-Za-z0-9_]*
INT     ::=  [0-9]+
STRING  ::=  " ( [^"\\\n] | \\. )* "
OP      ::=  == | != | <= | >= | && | || | -> | [-+*/%<>!=]
COMMENT ::=  // [^\n]*    |    /* .*? */
```

**Note what is *not* in `INT`.** No sign, no hex, no underscores. `-5` is two tokens, `-` and `5`, and the tree built in Week 2 is what makes it negative. Students routinely add a sign to the `INT` rule and then cannot explain why `3-5` lexes as `3` and `-5` with no operator between them.

---

## 4. Maximal Munch

Given the input `<=`, a lexer could produce `<` and then `=`, or a single `<=`. Both are consistent with the rules. **The tie-break is a rule, not a deduction:**

> **Maximal munch: at each position, take the longest match. If two rules match the same longest
> string, take the one listed first.**

Both halves are needed. The first settles `<=`; the second settles `if`, which matches both the keyword rule and `IDENT` at length two.

**Measured on the two Cyan lexers you will build in Lab 1:**

| Input | Tokens | Why |
|---|---|---|
| `a<=b` | `a` `<=` `b` | longest match at `<` is `<=` |
| `a< =b` | `a` `<` `=` `b` | the space ends the munch |
| `a<<=b` | `a` `<` `<=` `b` | `<<` is not a Cyan operator, so the first `<` stands alone |
| **`x-->y`** | `x` `-` `->` `y` | **look at this one** |
| `ifx` | `IDENT(ifx)` | longest match beats the keyword rule |
| `if x` | `KEYWORD(if)` `IDENT(x)` | the space ends the munch, then rule order picks the keyword |

*(Verified: flex 2.6.4 and the hand-written lexer produce identical output on all six.)*

**`x-->y` is the one to remember.** At the first `-`, the longest match is just `-`, because `--` is not an operator in Cyan. At the second `-`, the longest match is `->`. So a reader who sees `x` decreasing and pointing at `y` gets `x - (-> y)`, which is a syntax error in Week 2 rather than a lex error here. **The lexer is not confused. It applied its rule correctly and produced something the parser will reject** — and that division of labour is the design working, not failing.

> **Keywords are not a separate mechanism.** `if` is an identifier that happens to be reserved. Most
> real lexers do exactly what Cyan's does: match `IDENT`, then look the text up in a keyword set and
> retag it. Writing thirteen separate keyword rules works too, and flex handles it, but the set
> lookup is one line and does not grow.

---

## 5. What the Lexer Throws Away

**Whitespace and comments produce no tokens at all.** They are consumed and discarded, and by the time the parser runs there is no evidence they existed.

This is worth pausing on, because it is a real design decision with real consequences:

- **A code formatter cannot be built on this lexer.** It needs the whitespace. Real formatters (`gofmt`, `black`, `rustfmt`) use a lexer that *preserves* trivia, attaching it to adjacent tokens.
- **Nor can a documentation generator**, which needs the comments.
- **Python cannot do this at all.** Indentation is significant, so Python's lexer must emit `INDENT` and `DEDENT` tokens — which means it must track a stack of indentation levels. **A lexer with a stack is not a finite automaton**, and that is a genuine departure from the theory in L04.

**Cyan discards both**, because Cyan is a compiler and not a formatter. That is the trade: the lexer is simpler and provably regular, and the tooling that needs trivia has to use a different front end.

### Comments do not nest

```
a/* /* */ */b
```

**Both lexers tokenise this as `a` `*` `/` `b`.** *(Verified.)* The comment opened at the first `/*` and closed at the **first** `*/`, leaving ` */b` as live code — where `*` and `/` are operators and `b` is an identifier.

**This is what `The Cyan Language Reference` §2 means by "not nested"**, and it is C's behaviour too. Languages that chose otherwise — Rust, Haskell, OCaml — need the lexer to keep a *depth counter*, which is the same departure from finite state that Python's indentation forces. **Nesting comments costs you the regularity of your lexer.** It may well be worth it; it is not free.

---

## 6. When Two Lexers Disagree

In Lab 1 you build Cyan's lexer twice — once by hand and once with `flex` — and run both on the same input. **On every valid program they agree token for token.** *(Verified: 40 tokens on the reference program, identical.)*

They disagree on **invalid** input, and that is where the interesting design question lives:

| Input | `flex` | Hand-written |
|---|---|---|
| `12abc` | `INT(12)` `IDENT(abc)` | **error:** malformed number |
| `"unterminated` | `ERROR(")` `IDENT(unterminated)` | **error:** newline in string literal |
| `a&b` | `IDENT(a)` `ERROR(&)` `IDENT(b)` | **error:** unexpected character `&` |

*(Verified: flex 2.6.4 against the hand-written lexer.)*

**The pattern: flex recovers and continues; the hand-written lexer stops.** Neither is wrong, and the choice is a real one:

- **Recovering** reports every error in one run. A programmer with twenty typos fixes them in one pass rather than twenty compile cycles.
- **Stopping** gives a better message for the first error, and avoids the cascade where one bad character produces forty bogus errors downstream.

**`12abc` is the sharpest case.** flex is not being sloppy — it applied maximal munch faithfully. No rule matches `12abc`, the longest match at position 0 is `12`, and `abc` follows. **The hand-written lexer adds a rule flex was never told about:** a letter immediately after a digit is an error rather than a token boundary. That rule is a deliberate addition, and it is why C and Python both reject `12abc` instead of reading it as two tokens.

---

## 7. What to Take Away

1. **The lexer is the only phase that sees characters**, and the only one that can record source positions. Carry them.
2. **Tokens are a regular language**, and that is *why* the phase split is where it is — L04 proves the "why".
3. **Regular expressions here are the formal four-operator object**, not the library. No backreferences, and therefore no exponential blowup.
4. **Maximal munch, then rule order.** `x-->y` is `x` `-` `->` `y`, and the lexer is right to say so.
5. **Whitespace and comments are discarded**, which makes the lexer simple and makes formatters impossible to build on it.
6. **Nesting comments, or significant indentation, costs you finite state.** Both are defensible; neither is free.
7. **Error recovery is a design axis, not a correctness question.** flex continues, the hand-written lexer stops, and both are defensible.

---

## Exercises

1. Cyan's `INT` rule has no sign. Show the token sequence for `3-5` and for `3 - -5`, and say what builds the negation instead.
2. Give an input on which "longest match" and "first rule listed" disagree, and say which wins.
3. `x-->y` lexes as `x` `-` `->` `y`. **Add one operator to Cyan** that would make the same input lex differently, and give the new token sequence.
4. Python's lexer emits `INDENT` and `DEDENT`. Explain why this makes it not a finite automaton, referring to what a finite automaton can remember.
5. Nesting comments requires a depth counter. **Is a lexer with a bounded counter — say, maximum nesting depth 255 — still a finite automaton?** Answer carefully; the answer is yes, and the reason is worth stating precisely.
6. flex reads `12abc` as two tokens; the hand-written lexer rejects it. **Write the rule flex would need** to reject it too, and say where in the rule list it must go.
7. A compiler with error recovery reports twenty errors, of which nineteen are consequences of the first. Suggest one strategy for suppressing the cascade, and name what your strategy might hide.

---

*Next: L04 — the machine underneath. Why a regular expression can always be turned into a table lookup, why that table can be exponentially large, and why it does not matter in practice.*
