# CS 212 · Assignment 8 — Marking Guidance
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 8.** **Almost every mark is for something that runs**, and the paper says
so. **Open the linked runs before reading the prose.** A described pipeline is worth nothing; a green
run is worth the mark.

**Mark from the repository and the Actions tab**, in this order:
1. `.github/workflows/` — do both workflows exist and are they triggered correctly?
2. The Actions tab — are there green runs, and how long do they take?
3. `Dockerfile` — the five decisions.
4. The registry — are there SHA-tagged images?
5. **Then** the PDF.

**The three discriminators:**

1. **Does the gate actually block?** Check branch protection, or ask. A gate that reports and does not
   block is a report, and about a third of teams do not turn protection on.
2. **Q3(b): did the tests run against the pushed image, or against a fresh build?** Almost everybody
   claims the former and many have the latter. **Read the workflow.**
3. **Q4(b): was the SHA check shown *failing*?** Same test as A 5 Q1(b) and A 3 Q3(a) — a check never
   observed failing is not known to check anything.

**Automatic caps, both stated:** no linked green gate run → 50; a sweep that blocks merges → 75.

**Calibration:** median 68–72. This paper has a wide spread — teams that built the pipeline properly
score 85+, and teams that ran out of time score in the 50s, with little in between.

---

## Team-level fairness note

**One pipeline, several papers.** Read all of a team's papers together, and mark Q1–Q4 on the shared
artefact — **they should receive similar marks for it, because it is the same thing.** Q5(c) is where
they differ, and `git log --format='%an' -- .github/ Dockerfile docker-compose.yml` is the evidence.

**If one student built everything**, that is a finding for the team's retrospective and for the final
report's contribution assessment, **not a reason to fail the other three on Q1–Q4** — but it must be
recorded, and Q5(c) marks it honestly: a student with no commits to the pipeline loses those 4 marks.

---

## Q1: Measure Before You Change Anything (15)

### (a) [6]

| | |
|---|---|
| 3 | Total time and per-step breakdown, **from a linked run** |
| 3 | Where the time goes, ordered |

**Deduct 3** for numbers with no link. **Deduct 2** for a total with no breakdown — the breakdown is
the point of the question.

**Expected shape**, for calibration: on an uncached GitHub-hosted runner, a typical `slot` gate is
**2:30–5:00**, of which **60–120 s is dependency install**, 20–40 s is the Postgres service becoming
healthy, and **30–90 s is the actual tests.** A team reporting tests as the dominant cost has either
a genuinely slow suite (worth flagging — W6's mutation run will be unusable) or has misread the run.

### (b) [6]

| | |
|---|---|
| 3 | Before and after, both linked, with the install step's time isolated |
| 3 | **Whether caching was the biggest win available** |

**The second 3 marks reward the honest negative.** Some teams will find caching saves 40 s while the
Postgres healthcheck costs 45 — **and saying so, with the numbers, is the right answer.** Full marks
for *"caching saved 52 s; the bigger win was `concurrency: cancel-in-progress`, which stopped three
superseded runs per push."*

**Deduct 3** for "caching made it faster" with no isolated figure.

### (c) [3]

2 for a target with a justification against L25 §4's table; 1 for it being in the charter. **Accept
any target under 10 minutes with a reason.** A team targeting 30 minutes has not read the table.

---

## Q2: The Two-Speed Pipeline (25)

### (a) [14]

| | |
|---|---|
| 8 | Both workflows exist, correctly triggered, **green**, linked |
| 4 | **The gate blocks** — branch protection, or an equivalent |
| 2 | **The sweep does not block** |

**Check the gate's contents against the specification.** The five required items are: format check,
lint, type check on the domain, unit+integration tests, **and the architecture test from A 3.**
**Deduct 1 per missing item** from the 8.

**The architecture test is the one most often missing**, which is worth noting in feedback: they wrote
it in A 3 for marks and never wired it in, which is exactly W3 L11 §5's warning about adding controls
late.

**On branch protection [4]:** check it directly if you have access; otherwise require a screenshot or
a PR showing a blocked merge. **A team that says "we always wait for green" scores 1 of 4** — that is a
convention, not a control, and it is the same distinction as A 3 Q3(b).

**The sweep's 2 marks:** check the triggers. A "nightly" workflow with `on: [push]` is not a sweep.

### (b) [6]

| | |
|---|---|
| 3 | The principle, correctly stated |
| 3 | **One genuinely uncertain check, classified with reasoning** |

**The principle:** the gate contains only checks that are **fast and deterministic**; anything slow,
probabilistic, or dependent on the outside world goes in the sweep — **because a slow gate gets
bypassed and a flaky gate gets ignored.**

**Good uncertain cases**, with the answers markers should accept:

| Check | Defensible either way? |
|---|---|
| `pip-audit` | **Sweep.** It fires on someone else's schedule, not on your change. A team that gates on it will be blocked by a CVE in a transitive dependency on a Friday |
| Coverage-of-diff | **Either.** Gate is defensible if it only reports; gating on a *threshold* re-introduces Goodhart (W6 L19 §4) |
| Contract tests | **Sweep**, clearly — they hit a real external service |
| One fast E2E smoke journey | **Either.** Gate is defensible if it is under 30 s and deterministic |
| The mutation run | **Sweep.** Mutation time ≈ mutants × suite time |

**Full marks for a defended answer either way.** 0 for restating the principle without applying it.

### (c) [5]

| | |
|---|---|
| 3 | A mechanism that exists — a linked issue, a step summary, a message, a badge |
| 2 | **A named person or a rotation, with a time** |

**The paper is explicit: *"we would check it"* scores 0.** Accept: *"the release manager for the
fortnight (charter §4) looks at the nightly issue at the Monday and Thursday stand-ups; a red sweep
becomes a board card that day."*

**Award the full 5 to any team whose mechanism has already fired** — i.e. the sweep went red and
there is a comment or a card showing somebody responded. **That is the practice working and it should
be praised.**

---

## Q3: The Image (25)

### (a) [12]

**2 each for the five decisions, plus 2 for the size comparison.**

| Decision | What to check | Common failure |
|---|---|---|
| Dependency layers before source | `COPY pyproject.toml` before `COPY src/` | `COPY . .` first, which defeats caching entirely |
| Multi-stage, no build tools in runtime | Two `FROM` lines; runtime has no compiler | A single stage with `--no-cache-dir` and a claim that it is "small" |
| Non-root | `USER` before `CMD` | Missing entirely — **the most common omission** |
| No config baked in | No secrets, no hard-coded URLs; env vars | A `.env` copied in, or `DATABASE_URL` with a working default |
| Healthcheck | `HEALTHCHECK` present and it actually probes | A `HEALTHCHECK` that runs `true` |

**On the size comparison [2]:** expect roughly **1.0–1.3 GB single-stage with build tools → 180–350 MB
multi-stage slim.** Any credible before/after gets the 2. **A team reporting no size change has not
actually removed the build stage from the final image** — check for `COPY --from=`.

**`USER` placement is worth a feedback note.** `USER slot` before the `COPY --from=build` lines means
the copy happens as the unprivileged user and may fail on permissions. Correct order: copy, then
`USER`. **Not a deduction if it works, but say so.**

### (b) [7]

| | |
|---|---|
| 4 | Build once, SHA tag, pushed — **verified in the registry** |
| 3 | **Why rebuilding is dangerous**, concretely |

**The mark for (b)'s first part requires reading the workflow.** The failure to look for: a `test` job
that runs `docker build` and a separate `deploy` job that runs `docker build` again. **That is two
images.** Deduct 2 and explain — it is the exact failure L26 §6 describes.

**The 3 marks for "why":** a rebuild **resolves dependencies again**, and between the test run and the
production build a transitive dependency may have published a patch. **The thing you tested and the
thing you deployed are different, and nothing in the pipeline can tell you.** Accept also: a
non-reproducible base tag; a different builder architecture; a build-time network failure producing a
subtly different image.

**Deduct 3** for "it's slower" — true and not the danger.

### (c) [6]

**First part [3]:** the pin, shown as a diff. Digest or patch version both acceptable.

**Second part [3] — the demonstration.** This is the interesting mark.

| | |
|---|---|
| 3 | A cause **reproduced and fixed**, with output |
| 2 | A cause reproduced but not fixed, or fixed but shown only in prose |
| 1 | A statement of which they checked and how, having failed to reproduce one |
| 0 | Nothing attempted |

**The easiest to reproduce, and what a good answer looks like:** remove `DATABASE_URL` from the
compose file and show the container failing at import; or remove the `volumes:` mount and discover
that the image does not contain the module you have been editing. **The second is the best one and the
most instructive** — several teams will discover they have been testing local files for eight weeks.

---

## Q4: Deploy and Verify (20)

### (a) [8]

| | |
|---|---|
| 5 | A staging deploy on merge to `main`, of the SHA-tagged image |
| 3 | **Migrations as a separate step, and why startup is wrong** |

**Be generous about the target.** Fly.io, Render, a Hetzner box, a self-hosted runner deploying to a
container on a department machine, or even a local target — **the paper says the shape is what is
marked.** A team that deploys to a container on one member's machine via a self-hosted runner has done
the assignment.

**The 3 marks for migrations:** three replicas starting simultaneously means three migration runs
racing; and a failed migration inside a startup path produces a **crash loop** rather than a clear
failure with a stack trace. **Either reason earns it.**

**Deduct 3** if migrations run in an entrypoint script.

### (b) [7]

| | |
|---|---|
| 4 | `/health` reporting a SHA **baked in at build**, not read from a file or a git call |
| 3 | The assertion step, **shown failing** |

**Check the SHA's provenance.** `os.environ["GIT_SHA"]` with `build-args` is right.
`subprocess.run(["git", "rev-parse", "HEAD"])` inside the container is wrong — **there is no git
repository in the image**, and a team that did this and got it working has a `.git` directory in their
image, which is its own finding (deduct 2, and tell them their image contains their history).

**The failing demonstration [3]** must show the pipeline step exiting non-zero on a mismatch. Accept a
deliberate bad tag, a manually-stopped container, or a temporarily hard-coded wrong SHA. **1 of 3 if
only the passing case is shown.**

### (c) [5]

5 for a post-deployment smoke test that **creates and reads back a booking against the deployed
instance**, linked. 3 if it only hits `/health`. **1 if it runs against `localhost` in the CI job
rather than against the deployment** — which is a surprisingly common misread, and worth explaining:
a smoke test that does not touch the deployed thing tests nothing about the deployment.

---

## Q5: Reversal, and Your Part (15)

### (a) [6]

| | |
|---|---|
| 3 | A reversal answer **with a number** |
| 3 | The change that would make it "never", and the discipline that prevents it |

**Expected numbers:** *"redeploy the previous SHA, ~90 seconds, and we have tried it"* is ideal.
*"About a minute"* with no evidence of having tried → 2.

**The "never" answer:** **a migration that drops a column or a table.** The discipline is L26 §7's
expand-and-contract — five deploys to rename a column, each reversible. **Accept also:** a destructive
data backfill, an irreversible external side effect (an email sent, a payment taken), or deleting a
queue.

**Full marks and a note for a team that identifies one they have already shipped.** Several will have
a `DROP COLUMN` in their migration history from Week 4.

### (b) [5]

**1 per failure**, and the paper says **an honest "no" scores more than an unverifiable "yes".**

| Knight Capital failure | What a "yes" must point at |
|---|---|
| Manual deploy, 7 of 8 hosts | An automated deploy in a workflow |
| Dead code retained 8 years | **Almost every team should answer "no" honestly** — nothing in their pipeline detects dead code. `vulture`, or coverage on production traffic, is the answer they do not have |
| Repurposed flag | A flag inventory, a deletion issue per flag, or "we have no flags" — **which is a legitimate yes** |
| No check all hosts ran the same build | **The SHA verification from (b)** |
| Unactionable alert | An alert with a runbook link, or an honest "we have no alerting" |

**Mark the honesty.** A team claiming five yeses, with no dead-code detection and no alerting, scores
2 — and should be told which two they cannot support.

### (c) [4]

| | |
|---|---|
| 2 | A named part, with linked commits |
| 2 | Something learned that they did not expect |

**Check the `git log`.** The paper says it will be read. A student claiming the Dockerfile with no
commits to it **loses these 4 marks** and should be asked about it — gently, because sometimes one
person types while two pair, and **pairing declared in the paper is fine.**

**The "learned" 2 marks are for specificity.** *"I learned CI is fiddly"* → 0. *"I learned that
`depends_on` waits for the container to start, not to be ready, which is why our tests had been
failing about one run in five since Week 5"* → 2, **and it is worth circulating.**

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Before/after timings linked with the install step isolated, and an honest verdict on whether caching was the biggest win. Gate blocks, sweep does not, sweep failures have a named owner and have already fired once. All five Dockerfile decisions with real size figures. Tests run against the pushed image. A "works on my machine" cause reproduced and fixed. SHA check shown failing. Reversal with a number and a tried rollback. Honest verdicts on all five Knight Capital failures |
| **75–89** | Both workflows green and correctly split, blocking configured. Multi-stage image, SHA-tagged, staging deploy with separate migrations, health endpoint and smoke test. Reversal answered |
| **60–74** | One workflow doing everything, or a blocking sweep (capped at 75). Two Dockerfile decisions missing. Deploy without verification. Timings unmeasured or unlinked |
| **45–59** | A workflow that runs tests. No pushed image, no deploy, no verification (capped at 50 without a green gate) |
| **< 45** | Nothing runs |

**Feedback note for every paper:** give them their gate's current time and their target, and say
whether it is on track. **Week 9's refactoring depends entirely on a pipeline people are willing to
wait for** — a team at eight minutes will stop running it during a refactoring, which is exactly when
they need it most.

**Cohort note after marking:** publish the distribution of gate times, anonymised. **It is the single
most motivating number of the term** — teams that see a classmate's pipeline at 90 seconds go and cache
their dependencies that week.

---

*CS 212 · Week 8 · A 8 marking guidance · INSTRUCTOR ONLY*
