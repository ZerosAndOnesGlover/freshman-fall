# CS 101 · Week 10: Files, I/O, and Error Handling

---

## Contents

```
CS101_Week10/
│
├── README.md                                    ← You are here
│
├── lectures/
│   ├── L31 Files and the IO Boundary.md         ← Wed: the file abstraction, what each mode does
│   │                                                 to an existing file, context managers,
│   │                                                 streaming vs slurping, encoding as an
│   │                                                 explicit decision, the counting trap
│   ├── L32 Exceptions and Error Handling.md     ← Thu: exceptions as control flow, the hierarchy
│   │                                                 and clause ordering, try/except/else/finally,
│   │                                                 EAFP vs LBYL and TOCTOU, raising well
│   └── L33 Structured Formats and Robust IO.md  ← Fri: csv and json properly, pathlib, atomic
│                                                     writes, defensive reading of real files
│
├── lab/
│   ├── LAB 10 Robust File Handling.md           ← Tue 8 Dec (W11): reproduce the truncation hazard and defeat
│   │                                                 it, measure encoding damage, establish
│   │                                                 exception ordering,
│   │                                                 build a defensive CSV loader
│   └── io_lab_starter.py                        ← Lab starter — mode table, truncation, encoding
│                                                     and ordering demos ready to run; the rest TODO
│
├── assignments/
│   ├── QUIZ 10 Week 10 Wednesday.md             ← In-class quiz (covers Week 9)
│   ├── MIDTERM 2 Review and Practice Exam.md    ← Covers Weeks 6-9, with full answer key
│   ├── PS 10 Files IO and Error Handling.md     ← Problem Set 10 (due Fri 11 Dec, 17:00)
│   └── ps10_starter.py                          ← Scaffold with a 14-test self-check suite
│
├── resources/
│   └── Reading Guide Week 10.md                 ← 4 REPL sessions, mode + exception + atomic-write
│                                                     reference cards, 10-question self-test
│
└── solutions_instructor/
    └── LAB 10 Solutions.md                      ← Verified outputs, expected answers, marking notes
```

---

## Week 10 at a Glance

**Theme:** Your programs start touching the outside world, which can refuse. This week is about
persisting data without losing it, and failing in ways that can be diagnosed.

| Day | Event | Topic |
|-----|-------|-------|
| Wed 2 Dec | Lecture 31 + Quiz 10 | Files, modes, context managers, encoding, streaming |
| Thu 3 Dec | Lecture 32 | Exceptions, the hierarchy, EAFP vs LBYL, raising well |
| Fri 4 Dec | Lecture 33 + PS10 released | csv/json, pathlib, atomic writes, defensive parsing |
| Tue 8 Dec (W11) | Lab 10 (graded) | Modes and truncation, encoding, exception mechanics, a defensive CSV loader |
| — | **Midterm 2** | Covers Weeks 6–9 |

**📌 Midterm 2 does not cover Week 10.** This week's material appears on the final.

---

## Your To-Do List

### Before Wednesday
- [ ] Review Week 9 — Quiz 10 covers strings, encoding, search cost, regex
- [ ] **Start the Midterm 2 practice exam** — closed-book and timed

### Wednesday
- [ ] Quiz 10 (10 min — covers Week 9)
- [ ] Notes for L31
- [ ] REPL Session A (what the modes do)

### Before Thursday
- [ ] Read the Errors and Exceptions tutorial §8.3–§8.6
- [ ] REPL Session B (encoding is a decision)

### Thursday
- [ ] Notes for L32
- [ ] REPL Sessions C and D (exception mechanics; EAFP measured)

### Friday
- [ ] Notes for L33
- [ ] PS10 released — read it completely

### Tuesday 8 December Lab, Week 11 (Required, Graded)
- [ ] Mode table; truncation reproduced; `atomic_write` proven to protect the original
- [ ] Encoding damage measured and explained
- [ ] Both exception orderings recorded; `BaseException` point made
- [ ] Defensive CSV loader handling all three defects
- [ ] TA checkoff

### Weekend
- [ ] Start PS10 — at minimum A1–A3 (written) and B1–B3 (code)

---

## The Central Ideas of Week 10

**1. `open(path, "w")` destroys the file at open time.**
Before you write a byte. A crash, exception, or power loss between the open and the completed write
leaves you with neither the old version nor the new. Verified: the file reads back as `''`.

**2. The fix is write-elsewhere-then-rename.**
Temp file **in the target's directory**, `fsync` before renaming, `os.replace` (not `os.rename`),
cleanup under `BaseException`. Each of those four defends against a different failure — wrong
filesystem, power loss, wrong platform, wrong signal.

**3. Encoding is a decision you are making whether or not you notice.**
Omit `encoding=` and the locale decides — `UTF-8` here, possibly `cp1252` elsewhere. The same code
then reads the same file differently on different machines.

**4. Silent corruption is worse than a crash.**
`errors="replace"` turns `'café 日本語'` into `'caf�� ���������'` and raises **nothing**. The
exception stops you where the problem is; the replacement propagates it into everything downstream.

**5. Exceptions are a channel for failure that cannot be ignored.**
Unlike C's return codes, which a caller can silently drop. Order clauses **specific → general**, or
the broad one makes the rest unreachable — Python will not warn you.

**6. `except:` catches Ctrl-C.**
`KeyboardInterrupt` and `SystemExit` derive from `BaseException`, not `Exception`. A bare `except`
makes a long-running program un-interruptible.

**7. Checking before doing does not make it safe.**
Between `os.path.exists(p)` and `open(p)`, the file can vanish. That is **TOCTOU**, and the check
only makes the failure rarer — which makes it harder to reproduce, not less likely to matter.

**8. Exceptions are cheap to try and expensive to raise.**
Measured: EAFP beat LBYL on hits (18.6 vs 25.9 ms) and lost badly on misses (52.7 vs 14.8 ms). Ask
forgiveness when failure is rare; check first when it is routine — unless a race is possible, where
correctness decides.

---

## Quick Self-Check

Without notes:

1. Which modes truncate, and at what moment?
2. Give the four requirements of a correct atomic write, and what each prevents.
3. Why must `encoding=` be explicit?
4. What does `errors="replace"` produce, and why is it worse than an exception?
5. Give the execution order of `try`/`except`/`else`/`finally`, both cases.
6. Why is `except OSError` before `except FileNotFoundError` a bug Python won't warn about?
7. Name two things `except:` catches that `except Exception:` does not.
8. What does `raise X from e` preserve?
9. What is TOCTOU? Which style avoids it?
10. A CSV row is missing a column. Which exception does `int(row["score"])` raise, and why not
    `ValueError`?

*(Answers: 1. `w` and `w+`, at `open()`. 2. temp in the target's directory (cross-filesystem
atomicity), `fsync` before rename (power loss), `os.replace` (Windows), `BaseException` cleanup
(Ctrl-C leaking temp files). 3. otherwise the locale decides and differs per machine. 4. U+FFFD
replacements — silent and irreversible, so corruption propagates. 5. success try→else→finally;
failure try→except→finally. 6. `FileNotFoundError` is a subclass, so the broad clause matches first;
unreachability is undecidable in general. 7. `KeyboardInterrupt`, `SystemExit`. 8. `__cause__` —
the original exception and its traceback. 9. time-of-check to time-of-use; **EAFP**. 10. `TypeError`
— `DictReader` fills the missing field with `None`, and `int(None)` is a type error, not a bad
value.)*

---

## Techniques Introduced This Week

| Technique | Guarantee | Key Idea |
|---|---|---|
| `with open(...)` | closes even on exception | Context manager, not manual `close()` |
| Explicit `encoding=` | reproducible across machines | The locale is not a decision |
| Streaming iteration | O(1) memory | `for line in f`, never `.read()` on big files |
| `try`/`except`/`else` | small guarded region | Only the risky call goes in `try` |
| `raise ... from e` | keeps the diagnosis | Otherwise the cause is lost |
| Custom exception hierarchy | callers choose granularity | Base per subsystem, specific subclasses |
| `atomic_write` | all-or-nothing update | Temp + `fsync` + `os.replace` |
| Defensive row parsing | one bad row skips one row | Count and log; never `except: pass` |

---

*CS 101 · Week 10 · © CSE Department*
