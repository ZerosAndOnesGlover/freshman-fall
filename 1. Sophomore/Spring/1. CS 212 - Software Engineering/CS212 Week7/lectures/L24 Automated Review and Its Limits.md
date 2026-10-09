# CS 212 · Software Engineering
## Week 7 · Lecture 3 of 3
### Automated Review, and Its Limits

*“Mechanical rules are never a substitute for clarity of thought.”* — Brian Kernighan & P. J. Plauger, *Software Tools* (1976)

---

**Sat:** Thursday of Week 7, 10:00–10:50, TH 200 · **Reading:** ruff and mypy documentation — the rule selection pages · **Next:** Week 8, CI/CD

**Coursework:** 📝 **Assignment 6** due Fri this week 17:00 · 📊 **Quiz 8** Tue of Week 8 · 📝 **Assignment 8** released Wed of Week 8 17:00, due Fri of Week 9 17:00
**⚠️ Spring Break follows this week. A 7 is due Friday 27 March**, after the break.

---

## 1. The Principle, Restated as a Budget

L23 §3 said it as a rule: **if a machine can check it, a human must not.** Here is the version with a number attached.

**A reviewer has under an hour of useful attention** (L22 §4). Call it 40 productive minutes. **Every minute spent on something a tool could have caught is a minute not spent on the concurrency question**, and the concurrency question is the one that took `roomsvc` four months.

**So automation is not about rigour. It is about reallocating a fixed budget** from checks that are mechanical to checks that require a person who understands the domain.

| What a machine is better at | What only a person can do |
|---|---|
| Consistency — the same rule, every time, no fatigue | **Is this the right thing to build?** |
| Breadth — every file, not the ones in the diff | **Is the responsibility in the right place?** |
| Things with a syntactic definition | **Would the registrar actually want this?** |
| Not being socially awkward about it | **Is this comprehensible to somebody else?** |

**The fourth row on the left is under-rated.** A linter rejecting your unused import is not a colleague implying you are careless. **Moving a rule into a tool removes the interpersonal cost of enforcing it entirely**, which is why L23 §6's *"they keep making the same mistake"* is answered by a config file rather than a conversation.

---

## 2. The Layers, Cheapest First

Five layers. **Adopt them in this order**, because each is cheaper and more certain than the next.

| Layer | Tool | Catches | False positives |
|---|---|---|---|
| **1. Formatting** | `ruff format` | Nothing. **It ends an argument** | None — there is no judgement to get wrong |
| **2. Linting** | `ruff check` | Unused imports, shadowed names, **mutable default arguments**, bare `except`, unreachable code | Low, and configurable |
| **3. Type checking** | `mypy --strict` | Whole classes of defect: `None` where a value was assumed, wrong argument types, **unhandled union members** | Low once configured; high while you are configuring |
| **4. Security / pattern scanning** | `bandit`, `semgrep`, `pip-audit` | Hard-coded secrets, SQL built by string concatenation, known-vulnerable dependencies | **Moderate to high** |
| **5. Custom rules** | Your own `ast` checks | **Your architecture** (W3 L11 §1), your conventions, your invariants about the code | Zero, because you wrote them |

**Layer 1 is worth thirty seconds of explanation** because teams argue about it. **The value of a formatter is not the formatting — it is the removal of the topic from human conversation.** `ruff format` on every commit means nobody ever writes a review comment about a line break again, which reclaims a share of that 40-minute budget permanently.

**Layer 5 is the one nobody does and it is the highest-value.** A generic linter does not know that your domain package must not import `sqlalchemy`. **Twelve lines of `ast` do** (W3 L11 §1), and you already wrote it in A 3.

---

## 3. What Type Checking Actually Buys

**The most under-used of the five in Python, and the evidence is decent.**

```python
# before: passes every lint, fails in production
def confirm(hold_id: str, repo) -> Booking:
    hold = repo.get(hold_id)          # -> Hold | None
    return repo.mark_confirmed(hold.id)   # AttributeError when the hold is gone
```

```console
$ mypy --strict src/slot/
src/slot/app/confirm.py:4: error: Item "None" of "Hold | None" has no
    attribute "id"  [union-attr]
```

**That is a real defect** — the hold expired between the request and the confirm, which is W1 L06 §1's extension 5a — **found by a tool, in a second, with no test.**

**The evidence, such as it is:**

| Finding | Source |
|---|---|
| Type annotations reduce the time to fix type-related defects and to understand unfamiliar code | Hanenberg et al.; Endrikat et al. (2014) — small controlled studies, consistent direction |
| **Roughly 15% of public bugs in untyped JavaScript projects would have been prevented by type annotations** | Gao, Bird & Barr, *"To Type or Not to Type"* (ICSE 2017) — **the most-cited number here, and it is about JavaScript, not Python** |
| Gradual typing adoption in large Python codebases catches a meaningful class of `None`-related errors | Dropbox and Instagram engineering reports — **industrial reports, not studies** |

**Be careful with the 15%.** It is a good study, it used real bugs from real repositories, and **it is about a language whose type coercion rules are notoriously permissive.** Python is stricter at runtime, so the transferable figure is probably lower. **Quoting it as a Python number is the same error as quoting Fagan's 60% about pull requests** (L22 §1).

> **The practical recommendation, which does not depend on the number:** turn on `mypy` in a
> **ratchet**, not all at once. `--strict` on your domain package, ordinary mode elsewhere,
> and never decreasing. **`--strict` on a 4,000-line project you have already written will produce
> 300 errors and get switched off**, which is the same failure mode as adding the architecture test
> in Week 9 (W3 L11 §5).

---

## 4. Where the Scanners Earn and Where They Waste

**Layer 4 has the worst signal-to-noise ratio of the five**, and it still earns a place for two specific things.

**Genuinely worth it:**

| | |
|---|---|
| **Dependency vulnerability scanning** | `pip-audit` against the lockfile. Nearly zero false positives — a CVE either applies to your version or it does not. **Cheap, mechanical, and it is the class of problem behind Heartbleed's blast radius** |
| **Secret detection** | A committed credential is unrecoverable — rotating is the only fix, and `git` remembers forever. **A pre-commit hook here is worth more than any review comment** |
| **A small number of targeted `semgrep` rules** | *"No f-string inside `execute()`"*. **You write the rule because you had the bug** |

**Mostly a waste:**

- **A general-purpose scanner's full rule set on a term project.** `bandit` will flag your `assert` statements, your `random` usage in tests, and every `subprocess` call. **The finding-to-noise ratio is bad enough that people learn to ignore the output**, which is exactly the flaky-test failure from W5 L18 §5 in a new costume.
- **Anything whose output nobody reads.** A scanner reporting 200 findings weekly into a channel nobody opens is worse than no scanner, because it creates the belief that security is handled.

> **The rule for layer 4: adopt rules you can name a reason for, and turn the rest off.** Three
> rules that fire twice a term and are always right beat two hundred that fire constantly. **A 7
> Q4 asks you to do exactly this pruning.**

---

## 5. What No Tool Can Check

**The list matters because the whole point of §1 was to free attention for these.** Every item is something a reviewer must look at, because nothing else will.

| Invisible to every tool | Why |
|---|---|
| **Whether the requirement is right** | A perfect implementation of the wrong rule passes every check. W1 L04 §5's `roomsvc` issue #812 |
| **Whether the responsibility is in the right place** | Nothing can tell you that a pricing rule in a route handler is misplaced — only that it type-checks |
| **Whether an abstraction has a second case** | W2 L08 §7's question is about the future, and tools see only the present |
| **Whether the code is comprehensible** | The defining test — *can someone who did not write this change it?* — has no automated form |
| **Whether the tests assert anything meaningful** | **Mutation testing gets closest** (W6 L21) and still cannot tell you the assertions are about the right things |
| **Whether the concurrency is safe** | Type checkers, linters and mutation testing are all syntactic. **The VNC 101 race passes all three** |
| **Whether this was worth building** | W0 L02 §5's 45% |

**Read row six again.** Seven weeks of this course have been circling one bug, and **not one of the five automated layers would have caught it.** A partial unique index would, and a reviewer asking *"can two of these run at once?"* would. **The tools buy you the attention to ask that question; they cannot ask it.**

---

## 6. Wiring It Up

**Concretely, for `slot`, and most of it is one file.**

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "RUF"]   # not "ALL"; ALL is noise
ignore = ["E501"]                                   # the formatter owns line length

[tool.mypy]
python_version = "3.12"
warn_unused_ignores = true
[[tool.mypy.overrides]]                             # the ratchet
module = "slot.domain.*"
strict = true
```

```yaml
# .pre-commit-config.yaml  -- runs before the commit exists
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks: [{id: ruff, args: [--fix]}, {id: ruff-format}]
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks: [{id: detect-secrets}]
```

**Two decisions in there are worth naming:**

1. **`select` is a list, not `"ALL"`.** Enabling every rule produces hundreds of findings, most of which are style preferences with no rationale — exactly the thing L23 §3 says never to comment on. **Automating a bad review comment does not make it a good one.**
2. **`pre-commit` runs layers 1–2 before the commit exists**, so a formatting-only diff never reaches a reviewer. **CI runs all five again**, because a hook can be skipped and a pipeline cannot. Week 8 builds that.

---

## 7. The Shape to Aim At

**Google's mutation-testing practice (W6 L21 §5) is the model for how all of this should feel**, and it generalises to every automated check.

| Principle | In practice |
|---|---|
| **Check the diff, not the world** | Findings on lines the author did not touch are noise. `ruff check --diff`, `diff-cover`, mutants on changed lines only |
| **Surface a few, not all** | A handful of findings as review comments. **A wall of output is read by nobody** |
| **Let humans mark findings useless** | And **use that signal to prune the rule set.** A rule everyone dismisses should be deleted, not tolerated |
| **Never block on a probabilistic check** | Layers 1–3 and 5 can block; **layer 4 reports.** A security scanner that blocks merges gets disabled within a fortnight |

**The last row is the one teams get wrong.** A check that is right 99% of the time can block. A check that is right 60% of the time must advise, **because a gate that is wrong two times in five will be removed** — and then you have neither the gate nor the advice.

---

## 8. Summary

- **Automation is a budget reallocation, not rigour.** A reviewer has ~40 productive minutes; every one spent on a mechanical check is one not spent on the question that took `roomsvc` four months.
- **Moving a rule into a tool removes the interpersonal cost of enforcing it** — which answers L23 §6's recurring-mistake case with a config file rather than a conversation.
- **Five layers, cheapest first:** formatting (**which ends an argument rather than catching anything**), linting, type checking, scanning, **and custom rules — the one nobody does and the highest-value**, because only you know your domain must not import `sqlalchemy`.
- **Type checking finds real defects with no test** — the expired-hold `None` is W1's extension 5a, caught in a second. **The 15% figure is about JavaScript**, and quoting it as a Python number is Fagan's 60% all over again. **Adopt it as a ratchet**; `--strict` on an existing 4,000-line project produces 300 errors and gets switched off.
- **Scanners: dependency audits and secret detection earn their place; a general rule set on a term project does not.** Adopt rules you can name a reason for.
- **No tool can check** whether the requirement is right, whether the responsibility is placed right, whether an abstraction has a second case, whether the code is comprehensible, whether the assertions are about the right things, **whether the concurrency is safe** — the VNC 101 race passes all five layers — **or whether it was worth building.**
- **Aim at: check the diff not the world, surface a few not all, prune rules people dismiss, and never block on a probabilistic check** — because a gate that is wrong two times in five gets removed, and then you have neither the gate nor the advice.

**Next:** Week 8 — CI/CD. Where the five layers stop being a local convention and become a property of the repository, and where Knight Capital's eighth server is finally answered.

---

*CS 212 · Week 7 · L24 · © CSE Department*
