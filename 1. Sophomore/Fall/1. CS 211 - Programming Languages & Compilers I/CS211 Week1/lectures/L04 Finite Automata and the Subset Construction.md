# CS 211 · Programming Languages & Compilers I
## Week 1 · Lecture 2 of 2
### Finite Automata and the Subset Construction

*“The machine is supplied with a "tape"... running through it, and divided into sections (called "squares") each capable of bearing a "symbol".”* — Alan Turing, "On Computable Numbers" (1936)

---

**Reading:** Dragon §3.6–3.9 · **Next:** Week 2, L05 — recursive descent, and grammars that fight back

**Coursework:** 📝 **PS 0** due Fri this week 17:00 · 🔬 **Lab 1** Fri this week 14:00–15:50 · 📊 **Quiz 2** Tue of Week 2 · 📝 **PS 2** released Wed of Week 2, due Fri of Week 3 17:00

---

## 1. The Claim

Lecture 3 asserted that tokens are a *regular* language and that this is why the lexer is a separate phase. **This lecture is the proof, and it is constructive** — meaning it is also the implementation.

The chain is:

$$\text{regular expression} \;\longrightarrow\; \text{NFA} \;\longrightarrow\; \text{DFA} \;\longrightarrow\; \text{minimal DFA} \;\longrightarrow\; \text{a table}$$

**Every arrow is an algorithm you can run**, and the last object is a two-dimensional array indexed by state and character. That is what `flex` produces, and it is why a lexer costs a handful of instructions per input byte.

---

## 2. Two Machines

A **finite automaton** is a five-tuple $(Q, \Sigma, \delta, q_0, F)$: states, alphabet, transition function, start state, accepting states. **The only memory it has is which state it is in.** That is the entire content of the word "finite".

**A DFA** has $\delta : Q \times \Sigma \to Q$. Exactly one next state. Running it is a loop:

```python
state = start
for ch in text:
    state = table[state][ch]
return state in accepting
```

**One array lookup per character. No backtracking, no stack, no allocation.**

**An NFA** has $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to \mathcal{P}(Q)$ — a *set* of next states, and $\varepsilon$-transitions that consume no input. It can be in several states at once.

**NFAs are easy to build and awkward to run. DFAs are the reverse.** The subset construction converts one into the other, and that is the whole of §4.

---

## 3. Thompson's Construction: Regex → NFA

Each regex operator becomes a small NFA fragment with exactly one start and one accept state. Because the shape is uniform, the fragments compose.

| Regex | Fragment |
|---|---|
| $a$ | `(start) --a--> (accept)` |
| $rs$ | accept of $r$ gets an $\varepsilon$ to start of $s$ |
| $r \mid s$ | new start with $\varepsilon$ to both; both accepts get $\varepsilon$ to a new accept |
| $r^*$ | new start with $\varepsilon$ to $r$'s start and to a new accept; $r$'s accept loops back |

**Each operator adds at most two states**, so the NFA has **$O(n)$ states for a regex of length $n$**. That linearity is the point — and it is why building the NFA is never the expensive step.

**Measured**, for Cyan's `IDENT` over a reduced six-symbol alphabet:

```
IDENT = [a-c_][a-c_01]*
  NFA states : 38
  DFA states : 11
  minimal    : 3
```

**38 states down to 3.** The NFA is generated mechanically and is full of $\varepsilon$-transitions that exist only to make the composition uniform; the minimal DFA is what an experienced person would have drawn by hand — *start*, *seen at least one identifier character*, *dead*.

---

## 4. The Subset Construction: NFA → DFA

**The idea in one sentence: a DFA state is the *set* of NFA states you could currently be in.**

Two operations:

**$\varepsilon$-closure($S$)** — all states reachable from $S$ by $\varepsilon$-transitions alone, including $S$.

**move($S, c$)** — all states reachable from any state in $S$ by consuming exactly $c$.

Then:

```
start  = ε-closure({ nfa.start })
δ(S,c) = ε-closure( move(S, c) )
accept = { S : nfa.accept ∈ S }
```

Work outward from the start set, creating a DFA state for each distinct subset you meet, until nothing new appears.

**Worked, on `(a|b)*a`** — "any string of a's and b's ending in a". The minimal machine is:

| DFA state | Means | on `a` | on `b` |
|---|---|---|---|
| $A$ | last character was not an `a` | $B$ | $A$ |
| $B$ *(accepting)* | last character was an `a` | $B$ | $A$ |

**Two states**, and $B$ means exactly "the last character was an `a`" — the information the language needs, and no more.

**But the subset construction does not hand you two states. It hands you three:**

```
(a|b)*a       NFA 10   DFA 3   minimal 2
```

*(Measured.)* The extra one is the start state: "no input read yet" is a distinct *subset* of NFA states from "just read a `b`", even though no future input can ever tell them apart. **The construction cannot see that; it works subset by subset and has no notion of which distinctions matter.** Collapsing them is §6's job, and this two-versus-three gap is the smallest possible example of why minimisation is a separate step.

---

## 5. The Exponential Blowup, Measured

An NFA with $n$ states has at most $2^n$ subsets, so the DFA can have up to $2^n$ states. **The question is whether that bound is ever reached.** It is.

The standard witness is $(a|b)^*a(a|b)^n$ — *"the character $n+1$ from the end is an `a`"*:

```
   n | NFA | DFA  | minimal | 2^(n+1)
   1 |  16 |    5 |       4 |       4
   2 |  22 |    9 |       8 |       8
   3 |  28 |   17 |      16 |      16
   4 |  34 |   33 |      32 |      32
   5 |  40 |   65 |      64 |      64
   6 |  46 |  129 |     128 |     128
   7 |  52 |  257 |     256 |     256
   8 |  58 |  513 |     512 |     512
```

*(Measured. Thompson construction, subset construction and partition-refinement minimisation, all in Python.)*

**Read the last two columns together — that is the whole lesson.** The NFA grows by six states per increment. **The minimal DFA hits $2^{n+1}$ exactly, at every single $n$.** The theoretical worst case is not a loose bound here; it is attained.

**And minimisation buys you one state.** The constructed DFA has $2^{n+1}+1$ — the extra one being the start state, as in §4 — and minimisation removes precisely that one and stops. **You cannot minimise your way out of an exponential**, because the states are not redundant: they encode genuinely different histories.

**Why it must be so.** To decide whether the character $n+1$ from the end was an `a`, the machine must remember the last $n+1$ characters. There are $2^{n+1}$ distinct histories, and any two of them lead to different futures — so no two can share a state. **The information-theoretic argument is the proof**, and the measurement above is it happening.

> **Why this does not ruin lexing in practice.** Real token specifications are unions of short,
> mostly-disjoint patterns — keywords, identifiers, numbers, operators. Nothing in them requires
> remembering a sliding window of the last $n$ characters. `flex` on Cyan's full token set produces
> a table of a few hundred states, not $2^{58}$. **The exponential is real, reachable, and does not
> arise from anything a language designer would write.**

---

## 6. Minimisation

Two states are **equivalent** if no string distinguishes them — from either, exactly the same set of continuations leads to acceptance. **Merge every equivalence class and the result is the unique smallest DFA for that language.**

The algorithm is partition refinement:

1. Start with two blocks: accepting and non-accepting. *(Add a dead state first, so the DFA is total.)*
2. Split any block whose members disagree — where two states in the block, on the same character, go to different blocks.
3. Repeat until nothing splits.

**"Disagree" is the whole algorithm.** Two states survive in the same block only while no single character has yet told them apart.

**Uniqueness is the strong result here.** For a given regular language there is exactly one minimal DFA up to renaming — so two regular expressions denote the same language *if and only if* their minimal DFAs are isomorphic. **That is a decision procedure for regular-expression equivalence**, and it is why the identifier NFA's 38 states, 11 DFA states and 3 minimal states are three views of one object rather than three different answers.

---

## 7. Why the Parser Cannot Work This Way

Here is the boundary that justifies the whole phase split.

**No finite automaton can recognise balanced parentheses.**

Suppose one could, with $k$ states. Feed it $(^0, (^1, (^2, \dots, (^k$ — that is $k+1$ inputs and only $k$ states, so **two of them land in the same state**: say $(^i$ and $(^j$ with $i \neq j$. The machine now cannot distinguish them, so it accepts $(^i )^i$ if and only if it accepts $(^j )^i$. **The first is balanced and the second is not.** Contradiction.

*(This is the pumping lemma, in the form you will actually use it.)*

**The lexer's job is regular. The parser's job is not.** Cyan has parentheses, braces and brackets, all nestable to any depth, so the parser needs unbounded memory — a **stack**. That is the difference between a finite automaton and a pushdown automaton, and it is precisely the line the phase split follows.

**This is the answer to "why two phases?" from L03 §2**, and it is not a matter of taste. The two jobs sit on opposite sides of a boundary in formal power, so the tools differ: a table for one, a stack for the other.

---

## 8. What `flex` Actually Does

Everything above, then it writes out the table as C.

```bash
$ flex -o cyan_lex.c cyan.l && gcc -o cyanlex cyan_lex.c
```

The generated file contains `yy_nxt` — the transition table — and a driver loop shaped like §2's four lines. **This is why `flex` output is unreadable and fast**: it is a data structure, not a program anyone wrote.

**Two things it adds beyond the theory:**

**Maximal munch needs a *last accepting position*.** A pure DFA answers "is this whole string in the language?" A lexer must answer "what is the longest prefix that is?" — so it runs forward, remembers the most recent accepting state and where it was, and on failure rewinds to it. `x-->y` from L03 §4 is exactly this rewind: at the first `-` it advances hoping for `->`, sees another `-`, and backs up to the single-character match.

**Start conditions** are a second DFA. Cyan's block comments use one — `%x COMMENT` — because "inside a comment" is a mode with entirely different rules. It is still finite state; it is two tables and a mode variable.

---

## 9. What to Take Away

1. **Regex → NFA → DFA → minimal DFA → table.** Every arrow is an algorithm, and the last object is what runs.
2. **Thompson's construction is linear**; a regex of length $n$ gives an NFA of $O(n)$ states.
3. **A DFA state is a set of NFA states.** That one sentence is the subset construction.
4. **The exponential blowup is real and reachable** — 58 NFA states to 513 DFA states, measured — **and minimisation does not rescue you**, because the information genuinely must be remembered.
5. **It does not arise in real token sets**, which is why lexer generators are practical.
6. **The minimal DFA is unique**, which makes regular-expression equivalence decidable.
7. **Finite automata cannot count nesting.** That is a theorem, and it is why parsing is a separate phase with a stack.

---

## Exercises

1. Build the NFA for `(a|b)*abb` by Thompson's construction and count its states. Then run the subset construction by hand. How many DFA states, and how many after minimisation?
2. In §5 the constructed DFA has $2^{n+1}+1$ states and the minimal one has $2^{n+1}$. **Account for the single state that minimisation removes**, and say why no *further* merging is possible.
3. **Prove that the minimal DFA for $(a|b)^*a(a|b)^n$ needs $2^{n+1}$ states**, using the distinguishing-strings argument from §5 rather than by running the construction.
4. Cyan's `IDENT` minimises from 38 states to 3. Draw the 3-state minimal DFA and label what each state means in English.
5. §7 proves no DFA recognises balanced parentheses. **Does any DFA recognise balanced parentheses nested at most 100 deep?** Answer and justify — this is the same question as L03's Exercise 5, and the answer surprises people.
6. Maximal munch needs a rewind. Give a Cyan input where the lexer must back up **more than one character**, or argue that Cyan's token set makes it impossible.
7. Two regular expressions are equivalent iff their minimal DFAs are isomorphic. **Use this to decide** whether `(a|b)*` and `(a*b*)*` denote the same language. Construct both minimal DFAs.

---

*Next week: the parser. The grammar from Week 0 becomes code — one function per non-terminal — and the first thing that happens is that left recursion sends it into an infinite loop.*
