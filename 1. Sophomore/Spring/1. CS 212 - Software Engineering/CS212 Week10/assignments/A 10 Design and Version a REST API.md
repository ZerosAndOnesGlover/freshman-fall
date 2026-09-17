# CS 212 · Assignment 10
## Design and Version a REST API; Document the Breaking Change

---

**Released:** Week 10, Wednesday 17:00 · **Due:** Week 11, Friday 17 April, 17:00
**Total: 100 points** · Submit a PDF, `A10_{LastName}_{StudentID}.pdf`, plus **the API, the schema and the CI check in your team repository**

> **Three deliverables are in the repository, not the PDF**: the versioned paths, the committed
> OpenAPI document, and **the breaking-change check in your gate.** The last one is the only mechanism
> in this week that catches a break before a client does, and it is one CI step.
>
> **⚠️ A heavy Friday.** A 10 is due 17 April, the same day as **CS 202's Project 1** and **Problem
> Set 10 in every course**, and CS 290's Position Paper 2. **Do Q1–Q3 in the first week.**

---

### Q1: Audit Your Own API Against Liskov (20 points)

**(a) [8]** List every endpoint `slot` currently exposes: method, path, request shape, response shape, status codes. **A table.** Then mark each one **level 0, 1, 2 or 3** on the Richardson model, with a one-line reason.

**(b) [7]** **Find three things you would change** about your current API, and for each say **whether the change is breaking** under L31 §2's table — and why. **At least one of your three must be breaking and at least one must not**; if all three fall on one side, you have not looked hard enough.

**(c) [5]** **Hyrum's law, applied to your own API.** Name **two observable behaviours you never promised** that a client could come to depend on. *(Candidates: result ordering, id format, error wording, the absence of a field, latency, the fact that a list is never empty.)* **Then say which of your documented responses you would be unable to change** as a result.

> **`roomsvc`'s instance:** `GET /bookings` has always returned insertion order because nothing said
> otherwise, the timetable generator depends on it, and adding an index broke the timetable in 2023.
> **Find yours before someone else does.**

---

### Q2: Get to Level 2 (20 points)

**(a) [8]** **Fix your status codes.** For each of these, show the endpoint, the code you return, and the code you should return:

- A slot that is already confirmed
- A slot outside opening hours
- A booking id that does not exist
- A cancellation attempted by someone who does not own it, while authenticated
- A malformed request body

**[3 of the 8]** are for **409 being used for the conflict** — and for saying why a 500 on a client's bad input is a defect.

**(b) [6]** **Model your state transitions as named endpoints**, not as an assignable `state` field. Show the paths. Then answer: **what does `PATCH /bookings/{id}` with `{"state": "HELD"}` do in your system, and what should it do?**

**(c) [6]** **Errors as contract.** Adopt `application/problem+json` (RFC 9457) for at least your conflict and validation errors. Show a real response body. **Then state in your documentation which fields are stable contract and which are human-readable** — and say why that distinction is the only defence against Hyrum's law available to you.

---

### Q3: The Schema, and the Check (20 points)

**(a) [6]** **Generate your OpenAPI document and commit it.** FastAPI produces it from your annotations. Show the command and the committed path.

**(b) [10]** **Add breaking-change detection to your gate** (L32 §5): compare `HEAD`'s schema against `main`'s and **fail the build on a breaking change.**

| | |
|---|---|
| 5 | The step exists in the gate and a green run is linked |
| **5** | **It is shown failing** — make a breaking change deliberately, capture the output, revert |

**(c) [4]** **What does it not catch?** Name two breaking changes that are invisible to a schema diff. *(Think about behaviour rather than shape: tightened validation inside a handler, a changed default, altered ordering, a status code that moved within the same schema type.)*

---

### Q4: One Expand-and-Contract, Properly (25 points)

**Make a breaking change compatibly.** Pick a real one — a field rename, a type change, splitting one field into two, moving something from a query parameter to a body.

**(a) [10]** **Phase 1, expand.** Accept both forms on input, return both on output, mark the old one deprecated in your schema. **Show the diff and a response containing both.**

**(b) [8]** **Phase 3, measure.** **Instrument the deprecated form** so that usage is a number, with a tag identifying the caller (L33 §4). Show the code and **show the metric having recorded at least one use** — call it yourself if you have no other clients.

> **These 8 marks are the heart of the assignment.** Phase 3 is the phase teams skip, and skipping it
> is exactly why `roomsvc` has **seventeen deprecated endpoints, the oldest from March 2021**, all
> still live. **Four lines convert "we think nobody uses it" into a number, and the caller tag tells
> you who to email.**

**(c) [7]** **The deprecation notice.** All four things from L33 §5: a machine-readable marker, **a date**, the usage metric, and a named replacement. Show the response headers. **Then put the sunset date on your board as a card and link it** — a deprecation that is not scheduled work does not happen.

---

### Q5: The Ones You Did Not Choose (15 points)

**(a) [6]** **GraphQL for `slot`: argue it down.** Your week view is a 32-request problem (L32 §1) and GraphQL solves exactly that. **Say what the twenty-line SQL alternative keeps** — and name **three** of the five costs you avoid.

**If you want to argue *for* GraphQL, you may** — and you must then name the client you do not control, and say how you would bound query cost and rebuild caching.

**(b) [5]** **Protobuf's field numbers.** Explain why **renaming a field is free and reusing a number is catastrophic**, and why JSON makes the opposite choice. Then answer: **which choice would you rather have for `slot`, and why?**

**(c) [4]** **SemVer for a service.** Explain why it works for libraries and badly for a deployed service, in terms of **who chooses when the upgrade happens.** Then say what `slot` uses instead and why.

---

## Marking

| Band | |
|---|---|
| **90–100** | Endpoint audit with honest Richardson levels. Three changes correctly classified on both sides of breaking. Two real Hyrum's-law exposures in their own API. Status codes fixed including 409. Problem-JSON with the contract/prose distinction documented. **The CI check shown failing.** Expand-and-contract with a metric that has actually recorded a use, and a dated card on the board |
| **75–89** | Audit complete, level 2 reached, schema committed and checked in CI, expand-and-contract done with instrumentation. GraphQL argued down with real costs |
| **60–74** | Endpoints listed without levels. Breaking/non-breaking classified but thinly reasoned. Schema committed, no CI check. Expand phase done, measurement missing. Q5 paraphrases the lecture |
| **45–59** | No schema in CI. No instrumentation. Status codes unexamined. Deprecation without a date |
| **< 45** | No versioning, no schema, nothing in the repository |

**Two automatic caps.** **No breaking-change check in the gate → 70**, because it is one step and it is the only mechanism this week that catches a break before a client does. **An expand-and-contract with no usage metric → 75**, because phase 3 is the phase that makes removal possible, and without it you have built `roomsvc`'s seventeen deprecations.

---

*CS 212 · Week 10 · Assignment 10 · 100 points · due Friday 17 April, 17:00*
