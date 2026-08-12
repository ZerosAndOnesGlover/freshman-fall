# CS 211 · Lab 2
## Reading a Conflict Report

---

**Week 2 · Friday 14:00–15:50 · BH 220** — after both of this week's lectures.
**Unmarked.** The TA checks your work off in the session.
**Starter files:** `first_follow.py`, `dangling.y`, `cyan.y`.

> **Last week you built the same phase twice and the two agreed.** This week you build the same
> phase twice and **they disagree about the grammar itself** — bison will reject a grammar that
> `parser.py` parses without complaint, and the grammar is not the thing at fault.

---

## Why This Lab Exists

L06 §5 made a claim that is easy to nod along to and hard to actually believe: **a conflict report does not mean your grammar is ambiguous.**

Today you will see both cases on the same afternoon. The dangling else **is** ambiguous, and bison says so. **Cyan's grammar is not ambiguous — Week 0 proved it mechanically — and bison says so anyway.** Telling those two apart from the report is the skill this lab exists to build, because in Week 11 you will be staring at a conflict of your own with nobody to tell you which kind it is.

---

## Part 1 — FIRST, FOLLOW, and LL(1) (25 minutes)

```bash
python3 first_follow.py
```

The script computes FIRST and FOLLOW and builds an LL(1) table, reporting any conflicts.

**Q1.** Run it. **Record the four conflicts** reported for the left-recursive expression grammar. All four have the same shape — state it in one sentence.

**Q2.** The transformed grammar is LL(1) with a table of **13 entries**. **Count the entries you would expect** from the grammar's five non-terminals before looking, then check. Account for any difference.

**Q3.** FOLLOW(`E'`) is `{$, )}` and FOLLOW(`T'`) is `{$, ), +}`. **Where does the extra `+` come from?** Trace it to the production that puts it there.

### 1.1 Add a rule and watch it break

Cyan's `cmp_expr` is non-associative. Make it left-associative instead — add to `first_follow.py`:

```python
chained = {
    'E':  [('E', 'cmp', 'A'), ('A',)],
    'A':  [('A', '+', 'F'), ('F',)],
    'F':  [('n',)],
}
show("Chained comparison, left-recursive", chained, 'E', {'cmp', '+', 'n'})
```

**Q4.** Is it LL(1)? Now eliminate the left recursion by hand and rerun. **How many entries in the table?**

**Q5.** Cyan rejects `a < b < c` at the parser (L05 §6). **Is that rejection a consequence of the grammar, or an extra check in the code?** Look at `parse_cmp` in Week 1's… — actually, look at `parser.py`, which you are given in PS 2. Answer from `The Cyan Language Reference` §3 instead: which is it?

---

## Part 2 — The Dangling Else, Three Ways (30 minutes)

You have now met this ambiguity three times: gcc's runtime behaviour in Week 0, an LL(1) table conflict in L05 §5, and bison's state 6 in L06 §4. **Reproduce all three.**

### 2.1 As an LL(1) conflict

```bash
python3 first_follow.py | tail -12
```

**Q6.** The **left-factored** version is still not LL(1). **Quote the conflict**, and say in one sentence why left factoring did not help.

### 2.2 As a bison conflict

```bash
bison -Wall -o dangling.c dangling.y
```

**Q7.** How many conflicts, and of what kind?

```bash
bison -Wall --report=all -o dangling.c dangling.y
grep -A8 '^State 6$' dangling.output
```

**Q8.** In the state-6 report, one action appears **in square brackets**. **What do the brackets mean?** Which action did bison keep?

### 2.3 As two trees

```bash
bison -Wcounterexamples -o dangling.c dangling.y
```

**Q9.** bison prints a *shift derivation* and a *reduce derivation*. **For each, say which `if` the `else` attaches to.** Then say which one bison chose, and which language's behaviour that matches.

### 2.4 As a running program

```bash
printf '#include <stdio.h>\nint main(void){int a=0,b=0;\nif(a==1)\n if(b==1)printf("x\\n");\nelse printf("y\\n");\nreturn 0;}\n' > d.c
gcc -Wall -o d d.c && ./d
```

**Q10.** It prints nothing and warns. **Connect it to Q9**: bison's choice and gcc's behaviour are the same decision. State the decision once, in the vocabulary of each of the four tools you have now used on it.

---

## Part 3 — Cyan's Own Conflict (35 minutes)

`cyan.y` is `The Cyan Language Reference` grammar written for bison.

```bash
bison -Wall -Wcounterexamples -o cyan_par.c cyan.y
```

**Q11.** **How many conflicts, of what kind, and on which tokens?**

**Q12.** Read the counterexample. It shows two statements that begin identically. **Write out both**, and mark the token at which they finally diverge. **How many tokens after the ambiguity point is it?**

**Q13. The important one.** Week 0 verified mechanically that this grammar gives **exactly one parse tree** to each of 23 valid programs and zero to 9 malformed ones. **So is the grammar ambiguous?**

Answer, and then reconcile the two results. **What exactly is bison reporting, if not ambiguity?**

### 3.1 Fix it

**Q14.** Change `assign_stmt` so that the left-hand side is an `expr` rather than an `lvalue`, and delete the `lvalue` rule. Rerun bison.

```bash
bison -Wall -o cyan2_par.c cyan2.y ; echo "exit $?"
```

**Target: no output, exit 0.**

**Q15.** Your fixed grammar now accepts `3 = 4;`. **Which phase must reject it now?** Write the error message you would want, and compare it against what a parse failure would have said.

**Q16.** `The Cyan Language Reference` still specifies `lvalue`, and it is not going to change. **Is the reference wrong?** Argue in two or three sentences, using the distinction between a language specification and a parser implementation.

---

## Part 4 — Precedence Declarations (10 minutes)

**Q17.** Write a bison grammar for arithmetic using the **flat, ambiguous** rule:

```
expr : expr '+' expr | expr '*' expr | INT ;
```

Run it. **How many conflicts?**

Now add precedence declarations above the `%%`:

```
%left '+'
%left '*'
```

**Rerun. How many conflicts now?** And confirm the grammar is still the flat one — you have resolved the conflicts without stratifying.

> **Declare only operators the grammar actually uses.** Adding `%left '+' '-'` to a grammar with no
> `-` earns `warning: useless precedence and associativity for '-' [-Wprecedence]`. Harmless, and a
> useful reminder that the declaration block and the rules can drift apart — which is §6's whole
> objection to this style.

**Q18.** Cyan uses the stratified form instead (seven levels, L02 §9). **Give one reason the stratified form is better here**, referring to who reads `The Cyan Language Reference`.

---

## Before You Leave

The TA checks:

- [ ] **Part 1** — four conflicts recorded; Q3's `+` traced to its production
- [ ] **Part 2** — all four tools run; Q10 states the single decision in four vocabularies
- [ ] **Part 3** — Cyan's two conflicts found, **Q13 answered correctly**, and `bison` exiting 0 after the fix
- [ ] **Part 4** — conflict counts before and after `%left`

**Q13 is the one that matters.** If a student says the grammar is ambiguous, walk them back through Week 0's verification before letting them move on.

---

## If You Finish Early

**Make bison and `parser.py` disagree about a program.** Both accept Cyan; find a program where one accepts and the other rejects, or where they would build different trees. Start with the places the two implementations differ: the `lvalue` check, comparison chaining, and `else if`.

**Then the harder version:** construct a grammar that is genuinely ambiguous but that bison reports **no** conflict for. *(Hint: bison resolves shift/reduce silently by shifting. What if the ambiguity is resolved by a precedence declaration you wrote?)*

---

*Next: Week 3 — the tree exists and means nothing yet. The symbol table, scope, and the first phase that can reject a program the parser was happy with.*
