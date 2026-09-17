# CS 212 · Reading Guide · Week 7

---

## Required

| # | What | Length | Why |
|---|---|---|---|
| 1 | **Google, *"The Standard of Code Review"* and *"What to Look For in a Code Review"*** (google.github.io/eng-practices) | **~20 min for both** | Free, short, and the best practical writing on review anywhere. **The standard in #1 is the one sentence to memorise** |
| 2 | **Bacchelli & Bird**, *"Expectations, Outcomes, and Challenges of Modern Code Review"* (ICSE 2013) | ~11 pages | **The study that reframes what review is for.** Read §4 — the classification of 570 comments — and note that defect finding is expected first and delivers fourth |
| 3 | **ruff and mypy documentation** — rule selection / configuration | ~20 min | Enough to do A 7 Q4. **Read the `select` page in particular**, because the interesting decision is what to turn *off* |

**About an hour.** Read #1 before Wednesday's lecture; it is the checklist's source.

---

## Recommended

| What | Why |
|---|---|
| **Sadowski et al.**, *"Modern Code Review: A Case Study at Google"* (ICSE-SEIP 2018) | ~9M changes. **Median change ~24 lines, one reviewer, first response under an hour.** The numbers that justify "small and fast" |
| **Cohen et al.** / SmartBear, *Best Kept Secrets of Peer Code Review* — the Cisco study chapter | 2,500 reviews, 3.2M lines. Where the **200-line and 60-minute** thresholds come from |
| **Fagan**, *"Design and Code Inspections to Reduce Errors in Program Development"* (IBM Systems Journal, 1976) | **Read the method section.** Ten minutes, and it will permanently stop you quoting the 60% figure about pull requests |
| **Gao, Bird & Barr**, *"To Type or Not to Type"* (ICSE 2017) | The 15% figure. **Note that it is JavaScript**, which L24 §3 makes a point about |
| **Google, *"How to Write Code Review Comments"*** | Six pages, and the source of most of L23 §4 |

---

## Read Fagan Before You Quote Anyone

**Ten minutes, and it is the most useful debunking exercise in the course.**

Open the 1976 paper and read only how an inspection was *run*: three to six people; hours of individual preparation before the meeting; a **reader who paraphrases the code aloud** while the author stays quiet; **150 lines per hour**; defects **logged, not solved**; a separate rework stage; a follow-up to verify.

**Then think about the last pull request you approved.** One person, no preparation, no paraphrase, five minutes, several hundred lines, comments and fixes interleaved, no follow-up.

**These are different activities with the same name.** The 60%-of-defects figure belongs to the first one. **Transferring it to the second is the same error as quoting a JavaScript typing study as a Python number** (L24 §3) — and once you have noticed the pattern, you will find it repeatedly in this field.

---

## A Note on the Weakness of This Week's Evidence

W0 L02 §8 rated the evidence for code review **moderate**: good for formal inspection, weaker and messier for modern pull requests. **That rating is still right, and this week's reading is why.**

**What is well established:** size effects. Both the Cisco and Google datasets are large, the direction is consistent, and the mechanism — attention exhausts in under an hour, a large diff exceeds working memory — is plausible and independently supported.

**What is not established:** how much review improves quality, in what conditions, compared with what alternative. **There is no randomised trial of pull-request review, for the obvious reason** that no organisation will ship half its changes unreviewed to find out.

**So read the Bacchelli paper for what it actually is:** a careful *observational* study of what reviewers do and what they believe they are doing. **Its finding — that those two differ sharply — is robust, and it does not tell you that review works.** What justifies review, on the evidence available, is L22 §3's four reasons, of which only one is defect detection.

---

*CS 212 · Week 7 · Reading Guide*
