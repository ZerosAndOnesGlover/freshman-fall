# PROG 101 · Lab 12 Solutions (Instructor)
## Refactor, Test, Debug

---

## Part 1: Read Before You Change (4 pts)

**This part is marked on evidence of having read before editing**, which is why it is worth 4 points
for producing no code.

| Criterion | Points |
|---|---|
| Recorded **observed** behaviour from running it, not a guess | 1 |
| Identified entry point, inputs and outputs | 1 |
| Identified the data structures **before** the functions | 1 |
| Three-sentence summary that is accurate | 1 |

**The tell** for a student who skipped ahead: the summary describes what the refactored code does
rather than the original, or mentions module names that only exist after Part 2.

Lecture 1's ordering — run it, find the entry point, read the data structures, then the functions —
is the transferable skill here. The data structures constrain everything that can be done to them,
so reading them first makes the functions predictable.

---

## Part 2: Refactor (6 pts)

No single correct decomposition. Mark the **interfaces**, not conformance to a model.

| Criterion | Points |
|---|---|
| At least two modules with headers; headers hold declarations only | 2 |
| Everything not in a header is `static` | 1 |
| Three renames with reasons drawn from Lecture 1's rules | 1 |
| Nesting reduced via guard clauses | 1 |
| **Byte-identical output** proven with `diff` | 1 |

**The byte-identical constraint is the heart of the exercise.** Refactoring by definition preserves
behaviour; a student whose output differs has either introduced a bug or made an unrequested
"improvement". Both are worth stopping for — in industry the second causes as much trouble as the
first, because it hides in a diff labelled "refactor".

Expected `diff` evidence:

```bash
./tally_orig data.txt > orig.out
./tally      data.txt > new.out
diff orig.out new.out && echo IDENTICAL
```

**Common defects:** a function body left in a header (`multiple definition` at link — Week 10);
missing include guards; a header that only compiles when included after something else.

---

## Part 3: Test (5 pts)

Reference `check.h` is Lecture 2's. Verified output shape:

```
  test_tally.c:23: FAIL: count_words("") == 0 (got 1 vs 0)
9 checks, 1 failed
```

| Criterion | Points |
|---|---|
| `CHECK` reports file, line and condition text | 1 |
| `do { } while (0)`; safe in unbraced `if`/`else` | 1 |
| Suite covers n = 0, n = 1, malformed input, one boundary | 2 |
| `make test` **returns non-zero** on failure | 1 |

**`make test` must fail the build.** A target that prints failures and exits 0 is worth nothing in
CI, and this is the most common miss. Check by breaking a test deliberately and running
`make test; echo $?`.

**n = 0 is the case students omit** and the one most likely to find a real bug in their own
refactored code.

---

## Part 4: Measure and Debug (5 pts)

### 4A — Coverage (2 pts)

Expected output shape:

```
File 'tally.c'
Lines executed:87.50% of 8

        2:    4:    if (n < 0)      return -1;
       1*:    5:    else if (n == 0) return 0;
        1:    6:    else if (n < 10) return 1;
    #####:    7:    else             return 2;
```

Mark on whether the student **acted on** the `#####` lines — wrote a test or gave a defensible
reason it is unreachable. Reporting the percentage alone is worth 0 of the 2; the percentage is not
the deliverable.

Legitimately unreachable lines exist: a `default:` covering an enum whose values are all handled, or
an allocation-failure branch with no injection mechanism. Accept those with the reasoning.

### 4B — The three bugs (3 pts)

| Defect | Expected first tool | Why that one | Output |
|---|---|---|---|
| **Crash** | GDB `bt` | Gives the line **and the argument values** | `#0 … (p=0x0) at buggy.c:N` |
| **Leak** | Valgrind `--leak-check=full` | Only Valgrind reports the allocation site of a lost block | `N bytes in 1 blocks are definitely lost` |
| **Wrong answer, no crash** | **Tests + `gcov`** | **No sanitizer will fire** — it is a logic error, not a memory error | The untested branch |

**The third is the marking point, as the lab warns.** Students reach for sanitizers reflexively; a
logic error produces no sanitizer output at all, and running ASan, UBSan and Valgrind in turn wastes
the session. Matching tool to symptom — rather than running everything — is the skill.

*Award the full 3 only where each tool choice is justified by the symptom. A student who found all
three bugs by running every tool has fixed the code without learning the lesson; give 2 and say so.*

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| Part 1 summary describes the refactored design | Edited before reading | −2; the ordering is the exercise |
| Output differs after refactoring | A bug, or an unrequested change | −1 and require it fixed; explain why this matters |
| `make test` exits 0 on failure | Status not propagated | −1 |
| Coverage reported as a percentage only | Missed the point of `#####` | −2 |
| All three bugs found by running every tool | No diagnostic reasoning | −1, with feedback |
| Framework built on `assert` | Would silently pass under `-DNDEBUG` | −2, explain the silent-pass failure |

---

*PROG 101 · Week 12 · Lab 12 Solutions · Instructor copy — do not distribute*
