# CS 212 · Software Engineering
## Week 8 · Lecture 3 of 3
### Deployment, and How to Fail Safely

*“When you get in situations where you cannot afford to make a mistake, it's very hard to do the right thing. So if you're trying to do the right thing, the right thing might be to eliminate the cost of making a mistake rather than try to guess what's right.”* — Ward Cunningham, "A Conversation with Ward Cunningham", Artima (2003)

---

**Sat:** Thursday of Week 8, 10:00–10:50, TH 200 · **Reading:** SEC, *Administrative Proceeding 3-15570* (Knight Capital) — 12 pages · **Next:** Week 9, refactoring

**Coursework:** 📝 **Assignment 7** due Fri this week 17:00 · 📊 **Quiz 9** Tue of Week 9 · 📝 **Assignment 9** released Wed of Week 9 17:00, due Fri of Week 10 17:00

---

## 1. Continuous Delivery Is Not Continuous Deployment

Two terms, constantly conflated, and the distinction is where the engineering is.

| | |
|---|---|
| **Continuous delivery** | **Every commit that passes the pipeline is *releasable*.** A human decides when to release |
| **Continuous deployment** | Every commit that passes the pipeline **is released**, automatically |

**Continuous delivery is the engineering achievement.** It requires that the artefact is built, tested, and promotable without manual work — which is everything in L26 §6. **Continuous deployment is then a policy choice on top of it**, and it is sometimes the wrong one: a regulated release, a coordinated launch, or a customer who must be told.

> **`slot` should reach continuous delivery and need not reach continuous deployment.** A 8 asks for
> a pipeline that produces a promotable, SHA-tagged image and deploys it to a staging environment on
> every merge. **Whether a human presses a button after that is a decision, and you should make it
> deliberately and record it.**

---

## 2. Knight Capital, Properly

**W0 L01 §3 gave you the summary. Here is the mechanism, because it is the most instructive deployment failure on record and the SEC filing is twelve readable pages.**

**1 August 2012.** Knight Capital deployed a new order router to its eight production servers, over the preceding week.

| What happened | |
|---|---|
| **Seven servers received the new code.** The eighth did not | A **manual** deployment, performed by a person, with no verification step |
| The new code **reused a flag** that, in the old code, had activated a routine called **Power Peg** | Power Peg had been **dead for eight years** and was not removed |
| On the eighth server, the flag switched on Power Peg | Which sent orders **without counting fills** — so it kept buying, indefinitely |
| At 09:30 the market opened. In **45 minutes**: ~4 million executions, 397 million shares | **$460M gross loss.** The firm was acquired within months |
| **Alerts fired at 08:01** — 97 minutes before the open — and were not treated as blocking | The email said "Power Peg disabled" and nobody knew what that meant |

**Five distinct failures, and every one has a cheap mechanical answer:**

| Failure | The answer |
|---|---|
| Manual deployment to eight hosts | **Automated deployment with verification** — §4 |
| Dead code retained for eight years | **Delete dead code.** It is not free; it is a loaded gun |
| A feature flag repurposed | **Never reuse a flag name; delete the flag when the feature ships** (L25 §3) |
| No automated check that all hosts ran the same build | **Assert the deployed SHA on every target** — §4 |
| Alerts that fired and were not actionable | **An alert nobody can act on is noise.** §6 |

> **The sentence to take:** *"individuals and interactions over processes and tools"* is the wrong
> instruction for deployment (W0 L03 §2). **Deployment is vigilance, not judgement**, and vigilance
> belongs to a machine.

---

## 3. Environments, and What Each Is For

| Environment | Purpose | The honest truth about it |
|---|---|---|
| **Local** | Fast feedback while writing | Differs from production in ways you cannot enumerate |
| **CI** | The gate | Ephemeral, clean, and **therefore not like production either** |
| **Staging** | The last check before real users | **It is never really like production** — different data volume, no real traffic, stubbed third parties. Useful, and do not over-trust it |
| **Production** | Real users, real data, real consequences | The only environment whose behaviour is ground truth |

**The uncomfortable conclusion, and it is the modern consensus:** since staging cannot be made faithful, **the answer is not a better staging environment — it is making production failures cheap and fast to detect.** That is §5 and §6, and it is why "test in production" is a serious engineering position rather than recklessness, *provided* the mechanisms exist.

**For `slot`, be proportionate.** You have no production. **What you should have is a staging deploy on every merge to `main`, from the SHA-tagged image, with migrations run as a separate step and a smoke test afterwards.** That is the whole of A 8's deployment requirement and it is achievable in an afternoon.

---

## 4. Deployment Verification: the Answer to the Eighth Server

**The cheapest, highest-value thing in this lecture.**

```yaml
- name: Deploy
  run: ./deploy.sh ${{ github.sha }}

- name: Verify every target runs this build      # ← the Knight Capital step
  run: |
    for host in $TARGETS; do
      running=$(curl -fsS "https://$host/health" | jq -r .sha)
      if [ "$running" != "${{ github.sha }}" ]; then
        echo "::error::$host is running $running, expected ${{ github.sha }}"
        exit 1
      fi
    done
```

**Which requires the application to expose what it is:**

```python
@app.get("/health")
def health():
    return {"status": "ok",
            "sha": os.environ["GIT_SHA"],        # baked in at image build
            "started_at": STARTED_AT.isoformat()}
```

**Nine lines of YAML and three of Python.** Knight Capital's $440M was the absence of exactly this.

**And the smoke test, which is the other half:**

```yaml
- name: Smoke test
  run: |
    curl -fsS "$STAGING/health"
    id=$(curl -fsS -X POST "$STAGING/bookings" -d '{"resource":"TH200","slot":"..."}' | jq -r .id)
    curl -fsS "$STAGING/bookings/$id" | jq -e '.state == "CONFIRMED"'
```

**One booking, end to end, against the deployed thing.** It is the walking skeleton from Week 1, run as a post-deployment check — **which is one reason the skeleton was worth building in January.**

---

## 5. Deployment Strategies

| Strategy | How | Cost |
|---|---|---|
| **Recreate** | Stop the old, start the new | **Downtime.** Fine for `slot` and fine for a great deal of real software |
| **Rolling** | Replace instances a few at a time | **Old and new run simultaneously** — which is exactly why L26 §7's migrations must be backward-compatible |
| **Blue/green** | Two full environments; switch traffic; keep the old one warm | Double the infrastructure. **Rollback is a switch, which is its whole appeal** |
| **Canary** | Route 1% of traffic to the new version; watch; increase | Needs traffic-splitting **and metrics good enough to decide** |

**The property that actually matters is not which strategy — it is how fast you can undo it.**

> **DORA's fourth metric is *time to restore service*, and it is a design property, not a heroism
> property.** Blue/green restores in seconds because the old environment is still running. Recreate
> restores in however long a deploy takes. **A migration that drops a column restores in never.**

**So the question to ask of any deployment, and the one the final viva asks:** **"if this is wrong, how do we get back, and how long does it take?"** If the answer involves a database restore, the change was not deployable.

---

## 6. Observability, Which You Add Before the Incident

**You cannot add logging to a request that has already failed.** Three things, in order of value per minute spent:

**1. A correlation ID on every request.**

```python
@app.middleware("http")
async def correlate(request, call_next):
    rid = request.headers.get("X-Request-ID", str(uuid4()))
    with structlog.contextvars.bound_contextvars(request_id=rid):
        response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response
```

**Every log line from one request now shares an ID.** Without it, reconstructing what happened means correlating by timestamp, which fails exactly when you need it — under load.

**2. Structured logs.** JSON, with fields, not interpolated prose. `grep` works on prose; **queries work on fields**, and *"all failed confirms for resource TH200 in the last hour"* is a query.

**3. Four numbers, and only four to begin with.** Request rate, error rate, latency at p50/p95/p99, and **one domain metric** — for `slot`, confirmed bookings per hour. **The domain metric is the one that catches the failure your technical metrics miss**: a deploy that leaves every endpoint returning 200 while silently rejecting every booking looks perfect on the first three.

**On alerting, one rule that fixes the Knight Capital failure:**

> **An alert must say what to do.** *"Power Peg disabled"* was fired, received, and unactionable. An
> alert that nobody can act on trains everybody to ignore alerts — **which is W5's flaky-test failure
> and W7's noisy-linter failure in a third costume.** Same disease, three times in eight weeks.

---

## 7. What to Build This Fortnight

**A 8 requires items 1–5. Items 6–7 are worth doing anyway.**

1. **The two-speed pipeline** (L25 §5): a fast deterministic gate, a nightly sweep.
2. **A multi-stage Dockerfile**, non-root, dependencies layered before source, base image pinned.
3. **Build once, tag with the SHA**, push to a registry.
4. **Deploy that tag to staging on every merge to `main`**, with **migrations as a separate step.**
5. **Verify the deployment** — the SHA check and a smoke test that books one slot.
6. A correlation ID and structured logs.
7. **A `/health` endpoint that reports its own SHA.**

**And the honest measurement A 8 asks for:** your pipeline's total time, broken down by step, **before and after** you cache the dependency layer.

---

## 8. Summary

- **Continuous delivery — every passing commit is releasable — is the engineering achievement. Continuous deployment is a policy on top of it**, and sometimes the wrong one. `slot` should reach the first.
- **Knight Capital is five failures, each with a cheap mechanical answer:** a manual deploy that reached seven of eight hosts; eight-year-old dead code retained; **a repurposed flag**; no check that all hosts ran the same build; **and an alert that fired 97 minutes early and was unactionable.**
- **Deployment is vigilance, not judgement**, which is why *"individuals over processes"* is the wrong instruction for it.
- **No environment except production is like production**, and staging cannot be made faithful — so the answer is **making production failures cheap to detect and fast to undo**, not a better staging.
- **Deployment verification is nine lines of YAML and three of Python**: assert every target reports the expected SHA, then smoke-test one booking end to end. **That absence cost $440M.**
- **Strategies matter less than reversal time.** DORA's *time to restore* is a design property — blue/green restores in seconds; **a migration that drops a column restores in never.** Ask: *if this is wrong, how do we get back, and how long?*
- **Observability is added before the incident:** a **correlation ID**, structured logs, and **four numbers including one domain metric** — because a deploy can return 200 everywhere while silently rejecting every booking.
- **An alert must say what to do**, or it trains people to ignore alerts. **Third appearance in eight weeks of the same disease** — flaky tests, noisy linters, unactionable alerts.

**Next:** Week 9 — refactoring: Fowler's catalogue, the smells in `roomsvc`, and finally removing the bug this course opened with.

---

*CS 212 · Week 8 · L27 · © CSE Department*
