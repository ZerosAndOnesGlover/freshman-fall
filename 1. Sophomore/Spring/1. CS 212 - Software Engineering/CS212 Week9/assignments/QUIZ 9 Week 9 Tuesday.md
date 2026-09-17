# CS 212 · Quiz 9
## Administered: Tuesday, Week 9 (first 10 minutes of lecture)

**Name:** _________________________________ **Team:** ___________ **Date:** ___________

**Covers Week 8** — continuous integration, Docker, deployment.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.

---

**Q1.** Your team has a green pipeline on every push and four branches that have not merged for two weeks. Do you have continuous integration? Give the two-command test.

&nbsp;

&nbsp;

---

**Q2.** What does a team do when its pipeline takes over 30 minutes, and why is that the worst outcome?

&nbsp;

&nbsp;

---

**Q3.** Which checks belong in the gate and which in the nightly sweep? State the principle.

&nbsp;

&nbsp;

---

**Q4.** DORA finds that deploying more often goes with *lower* change failure rates. What mechanism explains it, and where have you met that mechanism twice before?

&nbsp;

&nbsp;

---

**Q5.** Name three of the five reasons "works on my machine" survives Docker.

&nbsp;

&nbsp;

---

**Q6.** Why must you never rebuild the image for production after testing it?

&nbsp;

&nbsp;

---

**Q7.** Knight Capital deployed to seven of eight servers. Give the nine-lines-of-YAML answer, and what the application must expose for it to work.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **No.** You have automated testing with deferred integration — which is the arrangement that produces the April crisis.

**The test:** `git log --oneline main --since='7 days ago' | wc -l`, and **how old is your oldest open branch.** Under five commits for a four-person team, or a branch older than three days, and you are not doing CI whatever the badge says.

*The load-bearing words in Fowler's definition are **integrate** and **daily**. The build is the verification.*

---

**Q2.** **It batches pushes to avoid the wait.**

**That is deferred integration — caused by the pipeline that exists to prevent it.** The pipeline has become the obstacle to the practice, which is why "keep the build fast" is on Fowler's list of ten at all.

---

**Q3.** **Gate: fast and deterministic** — format, lint, type check, unit and integration tests, the architecture test. **It blocks.**
**Sweep: slow, probabilistic, or dependent on the outside world** — E2E, mutation, dependency audit, order-independence runs. **It does not block.**

**The principle: a slow gate gets bypassed and a flaky gate gets ignored** — and then the real failures are ignored too.

---

**Q4.** **Batch size.** Frequent deployment forces small changes; small changes are easier to review, test, reason about, **and diagnose and revert when they fail.** A weekly release of 200 commits that breaks gives you 200 suspects; one commit gives you one.

**You have met it twice before:** **review size** (W7 — defect density collapses above 200 lines) and **TDD's small steps** (W5 — what the benefit actually tracks). **Three practices, three literatures, one mechanism.**

---

**Q5.** Any three of: **environment variables** (the commonest by far); **volume mounts** — your compose file mounts `./src` and the CI image bakes it in, so **you may have been testing local files rather than the image**; **the build context / `.dockerignore`**; **architecture** — an arm64 laptop build against an amd64 runner; **an unpinned base tag** — `FROM python:3.12` is not a version and it moved last Tuesday.

---

**Q6.** **A rebuild resolves dependencies again.** Between your test run and the production build, a transitive dependency may have published a patch — so **the thing you tested and the thing you deployed are different, and nothing in the pipeline can tell you.**

**Build once, tag with the commit SHA, promote that image.** Never `latest`, or *"what is running in production?"* is unanswerable during an incident.

---

**Q7.** **Assert that every deployment target reports the SHA you just built**, and fail the pipeline if any does not:

```bash
for host in $TARGETS; do
  running=$(curl -fsS "https://$host/health" | jq -r .sha)
  [ "$running" = "$GITHUB_SHA" ] || exit 1
done
```

**The application must expose `/health` returning its own SHA**, baked in at image build — not read from a file and not from a `git` call, because there is no repository in the image.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| **Q1, Q2** | **L25 §1, §4** — and run the two commands on your own repository today |
| Q3 | L25 §5 — A 8 Q2 is marked on exactly this split |
| **Q4** | **L25 §6** — the batch-size mechanism is the most likely final-exam essay |
| Q5, Q6 | L26 §3, §6 |
| **Q7** | **L27 §4** — A 8 Q4(b) requires it, **shown failing** |

**Q1 and Q4 are the ones that recur.** Q1 is a fact about your team you can check in ten seconds and may not like; Q4 is the third appearance of one mechanism and is the kind of connection the final exam rewards.

---

*CS 212 · Week 9 · Quiz 9 · covers Week 8 · ungraded*
