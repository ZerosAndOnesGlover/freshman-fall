# CS 212 · Software Engineering
## Week 8 · Lecture 1 of 3
### Continuous Integration — the Practice, and the Server

*“Optimism is an occupational hazard of programming: feedback is the treatment.”* — Kent Beck, *Extreme Programming Explained* (2000)

---

**Sat:** Tuesday of Week 8, 10:00–10:50, TH 200 · **⚠️ Quiz 8 in the first ten minutes** — covers Week 7 · **Reading:** Fowler, *"Continuous Integration"* (2006) · **Next:** L26, Docker

**Coursework:** 📊 **Quiz 8** today · 📝 **Assignment 8** released Wed this week 17:00, due Fri of Week 9 17:00 · 📝 **Assignment 7** due Fri this week 17:00
**First week back from Spring Break.** A 7 is due Friday 27 March.

---

## 1. CI Is a Practice, Not a Server

**The most common error in this entire course is thinking you have CI because you have GitHub Actions.**

Fowler's definition (2006), and note that no tool appears in it:

> *"Continuous Integration is a software development practice where members of a team integrate their
> work frequently, usually each person integrates at least daily — leading to multiple integrations
> per day. Each integration is verified by an automated build (including test) to detect integration
> errors as quickly as possible."*

**The load-bearing words are "integrate" and "daily".** The automated build is the *verification*; the practice is **merging your work into the shared trunk, at least once a day.**

**A team with a green pipeline and four branches that have not merged for a fortnight does not have continuous integration.** It has automated testing and deferred integration — which is the arrangement that produces the April crisis, and which every previous cohort's retrospectives describe.

> **The test, and you can apply it to your own team today:**
> **`git log --oneline main --since='7 days ago' | wc -l`**, and **how old is your oldest open branch?**
> If the first number is under five for a four-person team, or the second is over three days, **you
> are not doing CI**, whatever the badge says.

---

## 2. What the Practice Requires

Fowler lists ten practices. **Five do the work.**

| Practice | Why it is load-bearing |
|---|---|
| **Maintain a single source repository** | One trunk. `main` is the thing being integrated *into* |
| **Everyone commits to the mainline every day** | **The practice itself.** Everything else supports it |
| **Automate the build** | So that "it works" is a machine's claim, not a person's |
| **Make the build self-testing** | A build that compiles and does not test tells you nothing |
| **Keep the build fast** | §4. This is the constraint that decides whether the practice survives |

**And the one that is cultural rather than technical, and matters more than it sounds:**

> **Fix a broken build immediately.** A red trunk blocks everybody. **A team that tolerates a red
> `main` for a day has learned that red means nothing** — which is precisely the flaky-test failure
> from W5 L18 §5, and it kills CI the same way.

---

## 3. Trunk-Based Development, and the Branch Problem

**The tension every team hits:** you want to integrate daily, and your feature is not finished.

**Long-lived feature branches are the obvious answer and the wrong one.** The cost is not the merge conflict — it is **semantic** drift: your branch and `main` both changed the same concept in incompatible ways, and `git` merges them cleanly. **A clean merge is not a correct merge**, and a fortnight of divergence produces exactly the failures nobody tests for.

**Three techniques let you merge unfinished work**, in increasing order of power:

### 1. Merge it, but do not route to it

The cheapest, and enough for most of `slot`:

```python
# the new code exists on main, is tested, and nothing calls it yet
def suggest_next_free_slots(resource, slot, repo): ...
```

**Integrated, tested, dead.** No flag needed, because nothing reaches it.

### 2. Feature flags

```python
if settings.ENABLE_RECURRING:
    return expand_recurrence(rule)
return [single_booking(rule)]
```

**And the Knight Capital warning applies directly** (W0 L01 §3). Their $440M was a **repurposed flag** whose old meaning had lived in the codebase for eight years, on a server that had not been updated. Two rules follow, and both are cheap:

- **Delete the flag when the feature ships.** A flag is temporary scaffolding; **put an issue on the board with a date when you add one.**
- **Never reuse a flag name.** Ever. The name is retired with the flag.

### 3. Branch by abstraction

For changes too large to flag — swapping a persistence layer, restructuring a module. **Week 9 covers it properly**, because it is a refactoring technique: introduce an abstraction over the old thing, add the new implementation behind it, migrate callers, delete the old. **Every step is on `main` and every step is green.**

> **What to actually do on `slot`:** technique 1 for almost everything, technique 2 for the two or
> three changes that must be reachable but incomplete, **and a merge to `main` at least every two
> days per person.** If a branch has been open a week, it is too big, and it was too big when you
> started it.

---

## 4. Build Speed Is the Constraint That Decides Everything

**Not a nicety.** Every other property of CI depends on it, and the mechanism is behavioural rather than technical.

| Pipeline time | What the team does |
|---|---|
| **Under 2 minutes** | Waits for it. Sees the result while still holding the context |
| **2–10 minutes** | Starts something else. Comes back. **Context switch cost paid per push** |
| **10–30 minutes** | Stops watching. Finds out it is red an hour later, having built on top of the failure |
| **Over 30 minutes** | **Batches pushes to avoid the wait** — which is deferred integration, which is the thing CI exists to prevent. **The pipeline has become the obstacle to the practice** |

**The last row is the failure that eats itself**, and it is why "keep the build fast" is on Fowler's list at all.

**Where the time goes, and what to do — in order of payoff:**

| Cause | Fix |
|---|---|
| **Container and dependency setup on every run** | **Cache aggressively.** `actions/cache` on the dependency lockfile hash. Usually the single biggest win |
| Tests that sleep | Wait for conditions (W5 L16 §6). **`sleep` is the most common avoidable second in any pipeline** |
| Starting Postgres per test module | **Session-scoped**, with the rollback fixture. 9 s once, not 9 s × 12 |
| Serial stages | **Parallelise.** Lint, type-check and unit tests have no dependency on each other |
| Everything running on every push | **Split the pipeline.** §5 |

**One number for calibration.** `roomsvc`'s suite is **94 seconds** and its pipeline is **6 minutes 40**, of which **4 minutes 10 is installing dependencies with no cache.** The tests are not the problem; the setup is. **Check yours before optimising anything.**

---

## 5. The Two-Speed Pipeline

**You cannot run everything on every push, and you should not try.** Split by cost and by what a failure means.

```yaml
on: [push, pull_request]        # ← the gate. Must be fast. Must block.
  - ruff format --check
  - ruff check
  - mypy src/slot/domain
  - pytest tests/unit tests/integration        # target: under 3 minutes total
  - pytest tests/test_architecture.py          # W3's import rule

on: schedule (nightly)          # ← the sweep. Slow. Must NOT block.
  - pytest tests/e2e
  - pytest -m contract                          # real external services
  - mutmut run --paths-to-mutate src/slot/domain
  - pip-audit
  - pytest -p randomly (5 seeds)                # order-independence
```

**The split follows one principle:** **the gate contains only checks that are fast and deterministic. Everything probabilistic, slow, or dependent on the outside world goes in the sweep.**

**Why this is not a compromise but the right design** — and it is L24 §7's rule arriving in a pipeline:

- **A gate that is slow gets bypassed.** Someone adds `[skip ci]`, or merges without waiting.
- **A gate that is flaky gets ignored**, and then the real failures are ignored too.
- **A gate that depends on an external service fails when that service does**, which teaches the team that red means "try again".

**The sweep's results must be *seen*, or it is theatre.** Post the nightly result somewhere the team reads — an issue that gets updated, a message, a badge. **A nightly mutation run whose output nobody opens is worse than none**, because it creates the belief that the tests are being checked.

---

## 6. What the Evidence Says

**This is one of the better-evidenced areas in the course** (W0 L02 §8 rated it *strong*), and the reason is that the outcomes are measurable without asking anyone's opinion.

**The DORA programme** (Forsgren, Humble & Kim, *Accelerate*, 2018; annual State of DevOps reports), across roughly 2,000 organisations, identifies **four key metrics**:

| Metric | What it measures |
|---|---|
| **Deployment frequency** | How often you release |
| **Lead time for changes** | Commit → running in production |
| **Change failure rate** | Share of deployments causing a degradation |
| **Time to restore service** | How long recovery takes |

**The counter-intuitive finding, and it is the one worth carrying:** the first two and the last two **move together**. Organisations that deploy more often have **lower** change failure rates and recover faster.

**The obvious model says the opposite** — deploy more, break more. **The mechanism that resolves it is batch size.** Frequent deployment forces small changes; small changes are easier to review, easier to test, easier to reason about, and — critically — **easier to diagnose and revert when they fail.** A weekly release of 200 commits that breaks gives you 200 suspects. A deploy of one commit gives you one.

**Two honest caveats**, because the DORA data is survey-based:

1. **Self-reported, and self-selected.** The respondents are people who answer DevOps surveys.
2. **Correlational.** Organisations that deploy well may be well-run in general, and the causal arrow is not established by this data.

**It is still the strongest evidence in this course**, because the effect is large, replicated annually, and the batch-size mechanism is independently plausible — it is the same mechanism as W7's size effects on review and W5's small steps in TDD. **Three different practices, one underlying reason.**

---

## 7. What to Do on Your Project

**This fortnight, and A 8 requires most of it.**

1. **Measure your pipeline.** Total time, and time per step. **Do this before optimising anything** — it is usually the dependency install.
2. **Cache dependencies** keyed on the lockfile hash. Often minutes.
3. **Split the pipeline** into a gate and a nightly sweep, per §5.
4. **Put the architecture test in the gate.** You wrote it in A 3.
5. **Put the mutation run in the sweep**, with the result posted somewhere you will see it.
6. **Measure your integration frequency**, honestly: commits to `main` per person per week, and the age of your oldest branch. **Report it in A 8 whatever it says.**

---

## 8. Summary

- **CI is a practice, not a server.** The load-bearing words are *integrate* and *daily*; the build is the verification. **A green pipeline with four fortnight-old branches is not CI** — check `git log main --since='7 days ago'` and your oldest branch's age.
- **Five of Fowler's ten practices do the work**, and the cultural one — **fix a broken build immediately** — matters most, because a tolerated red trunk teaches the team that red means nothing.
- **Long-lived branches cost semantic drift, not merge conflicts.** A clean merge is not a correct merge. **Merge unfinished work** three ways: unrouted code, feature flags, or branch by abstraction.
- **Knight Capital was a repurposed flag on an un-updated server.** Delete flags when the feature ships; **never reuse a flag name.**
- **Build speed decides everything**, because over 30 minutes a team **batches pushes to avoid the wait** — deferred integration, caused by the pipeline meant to prevent it. `roomsvc`: 94 s of tests inside a 6:40 pipeline, **4:10 of it uncached dependency install.**
- **Two-speed pipeline:** the gate is fast and deterministic and blocks; the sweep is slow and probabilistic and does not. **A sweep nobody reads is worse than none.**
- **DORA, ~2,000 organisations: deployment frequency and lead time move *with* low failure rates and fast recovery**, and the mechanism is **batch size** — the same mechanism as review size and TDD's small steps. Survey-based and correlational, and still the strongest evidence here.

**Next:** L26 — Docker: what a container actually is, why "works on my machine" survives it anyway, and the image you should be shipping.

---

*CS 212 · Week 8 · L25 · © CSE Department*
