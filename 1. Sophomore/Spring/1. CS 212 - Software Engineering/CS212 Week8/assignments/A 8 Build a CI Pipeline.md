# CS 212 · Assignment 8
## Build a CI Pipeline: GitHub Actions, Docker, on Every Push

---

**Released:** Week 8, Wednesday 17:00 · **Due:** Week 9, Friday 3 April, 17:00
**Total: 100 points** · Submit a PDF, `A8_{LastName}_{StudentID}.pdf`, plus **the pipeline in your team repository**

> **Almost every mark here is for something that runs.** A described pipeline scores nothing; a
> linked green run scores fully. **Link every run you claim** — a workflow run URL, or a screenshot
> with the run number and timestamp.
>
> **This is a team artefact built by an individual.** Your team has one pipeline; you each write your
> own paper about it, and **you must each own at least one named part of it.** Q5 asks which, and
> `git log .github/` will be checked against your answer.
>
> Collaboration: expected within your team. State who built what.

---

### Q1: Measure Before You Change Anything (15 points)

**(a) [6]** Report your pipeline's **current** total time and **time per step**, from an actual run. Link it. Then say where the time goes, in order.

**(b) [6]** **Cache the dependency layer**, keyed on your lockfile hash. Report the before and after — **total time and the install step's time.** Link both runs.

**L25 §4 measures `roomsvc` at 6:40, of which 4:10 is uncached dependency install.** **[3 of the 6]** are for stating whether your project had the same shape, and **whether caching was the biggest win available** — if something else dominated, say what and why.

**(c) [3]** **Name your pipeline's target time and justify it** against L25 §4's table. Put the target in your charter.

---

### Q2: The Two-Speed Pipeline (25 points)

**(a) [14]** Split into a **gate** (on push and pull request) and a **sweep** (nightly).

**The gate must contain, and must block:** format check, lint, type check on your domain package, unit and integration tests, **and the architecture test from A 3.**

**The sweep must contain, and must not block:** end-to-end tests, the mutation run on your domain, a dependency audit, **and `pytest -p randomly` on at least three seeds.**

| | |
|---|---|
| **8** | Both workflows exist, are correctly triggered, and are green. Link both |
| **4** | The gate's contents are complete and it **blocks** — branch protection on, or an equivalent |
| **2** | The sweep **does not block** |

**(b) [6]** **State the principle behind your split**, and **classify one check you were unsure about**, with your reasoning. *(Good candidates: the contract tests, `pip-audit`, a slow E2E journey, coverage-of-diff.)*

**(c) [5]** **The sweep's results must be seen** (L25 §5). Show the mechanism — an issue that gets updated, a message, a summary in the run, a badge. **Then say what happens if it is red on a Tuesday**: who looks, and by when. **"We would check it" scores 0; a named person or a rotation scores fully.**

---

### Q3: The Image (25 points)

**(a) [12]** A **multi-stage Dockerfile** with all five decisions from L26 §4. 2 each for: dependency layers before source; multi-stage with no build tools in the runtime image; **non-root**; **no config baked in**; a healthcheck. **[2]** for the image size, before and after multi-stage.

**(b) [7]** **Build once, tag with the commit SHA, push to a registry** — GHCR is free for your repository. Then **run your tests against that image**, not against a fresh build.

**[3 of the 7]** are for explaining **why rebuilding for a later stage is dangerous**, concretely.

**(c) [6]** **Pin something and break something.**

- **[3]** Pin your base image to a patch version or digest. Show the diff.
- **[3]** **Demonstrate one of L26 §3's five "works on my machine" causes** in your own project — an unset environment variable, a volume mount hiding the baked-in source, an architecture mismatch, a moving base tag. **Show it failing, then fix it.** If you cannot reproduce one, say which you checked and how.

---

### Q4: Deploy and Verify (20 points)

**(a) [8]** **Deploy the SHA-tagged image to a staging environment on every merge to `main`**, with **migrations as a separate step before the deploy.** Any host is acceptable — a free tier, a container on a VM, a local target reachable by a self-hosted runner. **What is marked is the shape, not the vendor.**

**[3 of the 8]** are for migrations being a separate step, and for saying why **running them on application startup is wrong.**

**(b) [7]** **Deployment verification** — L27 §4, which is the answer to Knight Capital's eighth server.

- **[4]** A `/health` endpoint reporting its own **SHA**, baked in at image build.
- **[3]** A pipeline step that **asserts the deployed SHA matches the commit**, and **fails if it does not.** Show it failing — deploy a mismatched tag deliberately, capture the output, revert.

**(c) [5]** **A smoke test after deployment**: book one slot against the deployed instance and read it back. **This is Week 1's walking skeleton, run as a post-deployment check.** Link a run.

---

### Q5: Reversal, and Your Part (15 points)

**(a) [6]** **"If this deploy is wrong, how do we get back, and how long does it take?"** Answer for your project, with a **number**. Then name the one change you could make to your schema or deployment that would make the answer *"never"* — and say what discipline prevents it.

**(b) [5]** **The Knight Capital five** (L27 §2). For each of the five failures, say in one line whether your pipeline now prevents it, and by what mechanism. **An honest "no" with a reason scores more than a "yes" you cannot point at.**

**(c) [4]** **Which part of this pipeline did you build?** Name it, link the commits, and say what you learned that you did not expect. **`git log --format='%an' .github/ Dockerfile docker-compose.yml` will be read** — a student claiming a part with no commits loses these 4 marks and is asked about it.

---

## Marking

| Band | |
|---|---|
| **90–100** | Before/after timings linked. Gate blocks and sweep does not, with a named owner for sweep failures. All five Dockerfile decisions, with image sizes. Tests run against the pushed image. A "works on my machine" cause **reproduced and fixed**. The SHA check **shown failing**. Reversal answered with a number. Honest verdicts on all five Knight Capital failures |
| **75–89** | Both workflows green and correctly split. Multi-stage image, SHA-tagged, staging deploy with separate migrations. Health endpoint and smoke test present. Reversal answered |
| **60–74** | One pipeline doing everything, or a sweep that blocks. Dockerfile missing two of the five decisions. Deploy present, verification absent. Timings not measured |
| **45–59** | A workflow that runs tests. No image pushed, no deployment, no verification |
| **< 45** | Nothing runs, or the pipeline is described rather than built |

**Two automatic caps.** **No linked green run for the gate → 50**, because this assignment is about things that run. **A sweep that blocks merges → 75**, because it inverts L25 §5's principle and will be disabled within a fortnight — which is the failure the split exists to prevent.

---

*CS 212 · Week 8 · Assignment 8 · 100 points · due Friday 3 April, 17:00*
