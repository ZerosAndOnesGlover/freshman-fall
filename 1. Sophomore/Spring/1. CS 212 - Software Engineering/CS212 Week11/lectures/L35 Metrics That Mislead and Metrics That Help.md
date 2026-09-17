# CS 212 · Software Engineering
## Week 11 · Lecture 2 of 3
### Metrics That Mislead, and Metrics That Help

---

**Sat:** Wednesday of Week 11, 10:00–10:50, TH 200 · **Reading:** Tornhill, *Your Code as a Crime Scene*, Ch. 3–4 · **Next:** L36, documentation
**A 11 is released after this lecture**, Wednesday 17:00.

---

## 1. Goodhart's Law, for the Fifth Time

> **When a measure becomes a target, it ceases to be a good measure.**

**You have now met this five times in eleven weeks**, and it is worth putting them in one place, because the pattern is the lesson:

| Week | The measure | What happens when it becomes a target |
|---|---|---|
| **W6** | Line coverage | Test the trivial modules, `# pragma: no cover` the hard ones, write assertionless tests |
| **W7** | Review comments | Comment on naming to look thorough; **fourteen nits read as a rejection** |
| **W8** | Deployment frequency | Split one change into six deploys |
| **W10** | Endpoints deprecated | Mark things deprecated and never remove them — **seventeen of them** |
| **W11** | Any of the below | §2 |

**The mechanism is always the same**, and it is not dishonesty: **every measure is a proxy for something you actually want, and optimising a proxy diverges from the goal exactly where the proxy is weakest.** People find that divergence because they are competent, not because they are cheating.

**So the rule for every metric in this lecture:**

> **Measure it, read it, act on individual findings — and never set a target on it.** The only
> legitimate target-shaped use is a **ratchet**: *this may not get worse*, which has no reward for
> gaming because there is no prize for exceeding it.

---

## 2. The Metrics That Mislead

### Lines of code

**As productivity: uniquely bad**, because the better outcome usually has fewer lines. **Deleting `roomsvc`'s 380-line plugin directory is one of the most valuable changes available, and it scores −380.**

**As a size proxy for normalisation: fine and necessary.** *"Defects per thousand lines"* and *"this module is 25% of the codebase"* are legitimate. **The number is not the problem; the reward is.**

### Cyclomatic complexity

**McCabe, 1976** — independent paths through a function. `confirm_booking` is **94**.

**What it is good for:** a **threshold alarm**. Anything over ~10 is worth a look; over 30 is nearly always a real problem. **It also tells you the minimum number of test cases for full branch coverage**, which is a genuinely useful fact.

**What it is bad for:** comparison and targeting. A 200-line function of straight-line code scores low and may be awful; a 12-line dispatch table scores high and is fine. **And the target-shaped failure is specific and common** — splitting one complex function into five that must be read together reduces the number and improves nothing, which is W2 L07 §1's argument arriving as a metric.

### The maintainability index

`roomsvc/bookings.py` scores **11.42** out of 100.

**It is a formula** combining Halstead volume, cyclomatic complexity and lines of code, calibrated at HP in 1991. **Three honest problems:** the weights are arbitrary and were fitted to 1991 C code; Halstead volume is barely meaningful for modern languages; and **a single number cannot be acted on** — there is no such thing as fixing the maintainability index.

**Use it as a smell, exactly like the others**: 11 out of 100 says *look here*. It does not say what to do.

### Velocity and story points

**Not in the Scrum Guide as a requirement, and the most abused number in the field** (W0 L02 §7). Points are made up, so **the moment velocity is compared across teams or used to judge performance, it inflates** — costlessly and invisibly.

**Cycle time is the honest alternative**: how long a card takes from *In Progress* to *Done*. **It is measured in hours, cannot be inflated by redefinition, and is the number that actually tells you something** — usually that you started too many things at once (Little's Law, W0 L02 §7).

---

## 3. The One Analysis Worth More Than the Rest

**Hotspots.** Change frequency × complexity — and it is two commands.

```bash
git log --since='2 years ago' --name-only --format='' | grep '\.py$' \
  | sort | uniq -c | sort -rn | head -10
radon cc -s -a roomsvc/ | tail -20
```

| File | Touches | Complexity | Coverage | Hotspot? |
|---|---|---|---|---|
| **`bookings.py`** | **891** | **94 (worst fn)** | **31.8%** | **Yes. This is the whole answer** |
| `views.py` | 204 | 22 | 61% | Secondary |
| `models.py` | 186 | 4 | 95.6% | No — changes often, trivially |
| `legacy_import.py` | **2** | 31 | 0% | **No. Bad and dormant** |

**Why this beats every static measure**: a static analyser ranks `legacy_import.py` alongside `views.py`, because it cannot see that one is touched twice a year and the other twenty times a month. **The `git log` supplies the missing dimension, it requires no judgement, and it is the interest rate from L34 §3 made into a number.**

**Two refinements worth the extra command:**

**Change coupling** — which files change *together*:

```bash
git log --name-only --format='---' | awk '/^---/{...}'   # pairs, counted
```

`bookings.py` and `notify.py` change together in **112 of 891** commits. **They are coupled and neither imports the other** — the coupling is in the domain, and this is the evidence for a boundary being in the wrong place. **Change coupling is the empirical version of W2 L07 §7's "couple what changes together"**, and it is the only way to find a coupling that exists in nobody's import graph.

**Knowledge distribution:**

```bash
git blame --line-porcelain roomsvc/bookings.py | grep '^author ' | sort | uniq -c | sort -rn
```

**78% of `bookings.py`'s surviving lines were written by someone who left in 2023.** A **bus factor of 1** on the file that absorbs 41% of all changes — **which is the single most alarming number in the entire reference codebase**, and no static analyser will ever produce it.

---

## 4. The Four Metrics Worth Tracking on `slot`

**Few, read as trends, never targeted.**

| Metric | Command | Read it as |
|---|---|---|
| **Mutation score, domain package** | `mutmut run --paths-to-mutate src/slot/domain` | **The only one that says whether your tests would notice a regression** (W6) |
| **Pipeline time** | From the Actions tab | **A leading indicator.** Over ~10 min and people stop waiting (W8 L25 §4) |
| **Cycle time** | Board timestamps | Usually says you have too much WIP |
| **Hotspot table** | The two commands in §3 | **Where to spend your remaining effort** |

**And one thing that is not a metric and is worth more than all four: read your own `git log`.**

```bash
git log --oneline --since='1 week ago' main | wc -l    # are you integrating?
git branch --sort=-committerdate --format='%(refname:short) %(committerdate:relative)'
```

**If your oldest branch is a fortnight old, no metric on that table will tell you as much as that one fact** (W8 L25 §1).

---

## 5. Reading a Trend, Not a Score

**Every number in this course is more useful as a first derivative.**

| Score | Trend |
|---|---|
| "68% mutation score" | **"68%, from 51% in Week 6"** — the suite is getting better |
| "Pipeline is 4 minutes" | **"4 minutes, from 90 seconds in Week 8"** — something is wrong and you should find it now |
| "12 items in the debt register" | **"12, and we closed 3 and added 5"** — you are accruing faster than you repay |

**Three properties make trends better:**

1. **A trend is robust to a bad measure.** Even if "68%" is not comparable to another team's 68%, **your own 51 → 68 is comparable to your own 51.**
2. **A trend has a direction, and a direction implies an action.** A score invites a target.
3. **A trend catches the thing scores hide** — which is that the quantity was fine and is now deteriorating, and nobody noticed because it is still above the number someone chose.

> **The final report asks for trends, not scores.** *"Our mutation score went 51 → 68 → 71, and the
> jump in Week 7 was A 6's ten survivors"* is worth far more than *"our mutation score is 71%"*.

---

## 6. What Metrics Cannot See

**Compiled because the final report asks you to be honest about your own project, and because every number in this lecture is silent on all of it.**

| Invisible | Why |
|---|---|
| **Whether you built the right thing** | 45% of features are never used (W0 L02 §5), and no code metric knows which |
| **Whether the requirements are right** | A perfect implementation of the wrong rule measures perfectly |
| **Whether anyone can understand it** | The defining test — *can someone who did not write it change it?* — has no automated form |
| **Whether the team can work together** | Which decides more projects than any metric on this page |
| **Whether the invariant is actually enforced** | Coverage, complexity and mutation score were all silent on the VNC 101 race. **A `\d` in a migration file was the whole answer** |

**The last row is the course's own argument turned on itself.** Eleven weeks of measurement, and **the single most important property of `slot` — that it cannot double-book a room — is verified by one integration test and one line of DDL**, neither of which appears in any metric you will report.

---

## 7. Summary

- **Goodhart's law, for the fifth time in eleven weeks.** The mechanism is never dishonesty: **a measure is a proxy, and optimising a proxy diverges from the goal exactly where the proxy is weakest.** The only legitimate target-shaped use is a **ratchet** — *this may not get worse.*
- **Lines of code as productivity is uniquely bad**, because deleting 380 lines is one of the best changes available and scores −380. **As a size proxy it is fine.**
- **Cyclomatic complexity is a threshold alarm** and tells you the minimum test cases for branch coverage. **Targeting it produces five functions that must be read together.**
- **The maintainability index is a 1991 formula with arbitrary weights** and **cannot be acted on** — `bookings.py` scores 11.4 and there is no such thing as fixing it.
- **Velocity is the most abused number in the field; cycle time is the honest alternative** — measured in hours, not inflatable by redefinition.
- **Hotspots — change frequency × complexity — beat every static measure**, because the `git log` supplies the dimension a static analyser cannot see. **`legacy_import.py` is worse than `views.py` and dormant.**
- **Change coupling finds couplings that exist in nobody's import graph** — `bookings.py` and `notify.py` change together in 112 commits and neither imports the other. **Knowledge distribution finds the bus factor of 1 on the file that absorbs 41% of all change.**
- **Track four things on `slot`**, read as **trends rather than scores** — a trend is robust to a bad measure, implies an action, and catches deterioration that a threshold hides.
- **Metrics cannot see whether you built the right thing, whether anyone understands it, whether the team works — or whether the invariant is enforced.** Eleven weeks of measurement, and the whole answer was one line of DDL.

**Next:** L36 — documentation: what survives, what rots, and why the only documentation that stays true is the kind a machine checks.

---

*CS 212 · Week 11 · L35 · © CSE Department*
