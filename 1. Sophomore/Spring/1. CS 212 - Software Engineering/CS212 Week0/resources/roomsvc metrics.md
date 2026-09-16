# CS 212 · `roomsvc` — The Reference Codebase
## Every measurement in the lectures, with the command that produced it

---

**Why this file exists.** The lectures quote numbers about `roomsvc` from Week 0 to Week 12. They
all come from one snapshot, on the toolchain in the syllabus §5, and they are all here with the
command beside them. **When a lecture quotes a number, you can check it.**

**The snapshot** is commit `4f1ac82`, tagged `cs212-reference`, taken 2026-01-05. The repository is
read-only for students; assignments that change it work on your own fork.

```console
$ git clone git@github.com:cse-dept/roomsvc.git
$ cd roomsvc && git checkout cs212-reference
```

---

## Size and age

```console
$ cloc --include-lang=Python .
      34 files        1,902 blank        1,455 comment       11,438 code

$ git log --oneline | wc -l
2847

$ git log -1 --format='%cd' $(git rev-list --max-parents=0 HEAD)
Tue Feb 11 09:41:06 2020 +0000

$ git log -1 --format='%cd' HEAD
Mon Dec 15 16:22:41 2025 +0000
```

**Six years, 2,847 commits, 11,438 lines.** That is roughly 4 lines of surviving code per commit,
which is the normal ratio and not a sign of anything wrong — most commits change code rather than
add it.

---

## Who wrote it

```console
$ git shortlog -sn --all
  1183  A. Okonkwo
   702  M. Lindqvist
   488  R. Teixeira
   301  J. Park
   126  S. Abadi
    47  dependabot[bot]
```

| Author | Commits | Still in the department? |
|---|---|---|
| A. Okonkwo | 1,183 | **No** — left 2023 |
| M. Lindqvist | 702 | **No** — left 2022 |
| R. Teixeira | 488 | **No** — left 2024 |
| J. Park | 301 | Yes |
| S. Abadi | 126 | **No** — left 2021 |

**One of five human authors remains, holding 301 of 2,799 human commits — 11%.**

```console
$ git blame --line-porcelain roomsvc/bookings.py \
    | grep '^author ' | sort | uniq -c | sort -rn
   2195 author A. Okonkwo
    401 author R. Teixeira
    147 author M. Lindqvist
     71 author J. Park
```

**78% of the surviving lines of `bookings.py` were written by someone who left in 2023.** This is
the number Week 11 calls the *bus factor*, and it is 1.

---

## Shape

```console
$ wc -l roomsvc/*.py | sort -rn | head -8
  11438 total
   2814 roomsvc/bookings.py
    986 roomsvc/models.py
    743 roomsvc/views.py
    612 roomsvc/notify.py
    488 roomsvc/auth.py
    401 roomsvc/reports.py
    377 roomsvc/calendar_sync.py
    355 roomsvc/admin.py
```

**`bookings.py` is 25% of the codebase in one file.**

```console
$ radon cc -s -n C roomsvc/ | head -8
roomsvc/bookings.py
    F 291:0 confirm_booking - F (94)
    F 812:0 _resolve_conflicts - E (38)
    F 1455:0 render_week - D (27)
    F 2103:0 apply_recurrence - D (24)
roomsvc/views.py
    F 88:0 booking_form - D (22)
roomsvc/reports.py
    F 12:0 utilisation - C (19)
```

```console
$ radon mi -s roomsvc/bookings.py
roomsvc/bookings.py - C (11.42)
```

**Maintainability index 11.4 on a 0–100 scale.** Week 11 explains what that number is made of and
why you should distrust it while still finding it useful.

---

## Change

```console
$ git log --since='2 years ago' --name-only --format='' \
    | grep '\.py$' | sort | uniq -c | sort -rn | head -5
    891 roomsvc/bookings.py
    204 roomsvc/views.py
    186 roomsvc/models.py
    122 roomsvc/notify.py
     98 roomsvc/reports.py
```

**`bookings.py` accounts for 891 of 2,173 file-touches in two years — 41%.** It is simultaneously
the biggest file, the most complex file, the file with the worst bus factor, **and the file
everything has to change.** Week 11 calls this intersection a *hotspot*, and it is the single most
actionable metric in this file.

---

## Tests

```console
$ pytest -q
212 passed in 94.31s

$ coverage report --precision=1 | tail -3
roomsvc/bookings.py           2814   1489    47.1%
roomsvc/notify.py              612    588     3.9%
TOTAL                        11438   4461    61.0%

$ mutmut results | tail -1
1204 mutants generated, 374 killed (31.1%), 802 survived, 28 timeout
```

**Three numbers, and the third is the one to believe.**

- **61% line coverage** — 61% of lines are executed when the tests run.
- **47% on `bookings.py`** — the most-changed, most-complex file is the least covered.
- **31% mutation score** — of 1,204 deliberately introduced bugs, the suite noticed 374.

**The gap between 61 and 31 is the subject of Week 6.** A line can be executed by a test that never
asserts anything about what it did.

```console
$ pytest -q -k confirm_booking --collect-only | tail -1
11 tests collected
```

**Eleven tests for a function with 94 independent paths.**

---

## Issues

| | |
|---|---|
| Open issues | **143** |
| Median age of an open issue | **291 days** |
| Oldest open issue | **#31, opened 2020-08-14** — *"recurring bookings drop the last occurrence in DST weeks"* |
| Labelled `bug` | 61 |
| Labelled `bug` **and** touching `bookings.py` | **38** |

---

## The incident

**14 October 2024, 09:00, VNC 101.** Two confirmed bookings for one room in one slot: CS 201's
lecture and a visiting seminar. Both parties held a confirmation email.

| | |
|---|---|
| Detected | 2024-10-14, by the two lecturers, in the room |
| Diagnosed | **2024-11-06 — 23 days** |
| Fixed in production | **2025-03-11 — 4 months after detection** |
| Root cause | Check-then-act race in `confirm_booking`: a `SELECT` for conflicts, ~40 lines including two network calls, then an unguarded `INSERT` |
| The fix | **One `CREATE UNIQUE INDEX`**, plus handling the integrity error |
| Lines changed | 14, of which 1 is DDL |

```console
$ git show 9a2f1c4 --stat
 migrations/0042_unique_confirmed_booking.sql | 3 +
 roomsvc/bookings.py                          | 11 ++++++----
 2 files changed, 12 insertions(+), 4 deletions(-)
```

**Twenty-three days to diagnose and four months to ship fourteen lines.** Not because the fix was
hard. Because `confirm_booking` is 487 lines, its author left in 2023, the tests that exist do not
cover it, and **no one could convince themselves that touching it was safe.**

**That last sentence is what this course is about.** Weeks 2, 3, 5, 6, 7, 9 and 11 are each one
answer to *"how do you get to a state where a fourteen-line fix takes an afternoon?"*

---

*CS 212 · Week 0 · reference codebase metrics · snapshot `cs212-reference`, 2026-01-05*
