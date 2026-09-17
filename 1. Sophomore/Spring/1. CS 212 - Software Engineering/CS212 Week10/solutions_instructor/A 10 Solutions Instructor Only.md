# CS 212 · Assignment 10 — Marking Guidance
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 10.** The compatibility table in L31 §2 is a **theorem**, not a
preference — it follows from Liskov substitution — **so Q1(b) is the one part of this paper with
right and wrong answers, and it should be marked strictly.** Everything else is engineering argument
and is marked on reasoning.

**Mark from the repository first**: the versioned paths, the committed schema, and the gate step.
Then the PDF.

**The three discriminators:**

1. **Q3(b) — the CI check shown failing.** Fourth time this term (A 3, A 5, A 8, A 10) and it remains
   the most reliable signal: a check never observed failing is not known to check anything.
2. **Q4(b) — does the usage metric exist and has it recorded something?** This is the phase teams skip
   and the reason `roomsvc` has seventeen undead deprecations. **Check the code, then check the
   evidence of a recorded call.**
3. **Q1(c) — two real Hyrum's-law exposures in their own API.** Generic answers are common; a specific
   one about their own response shape is a strong signal.

**Two automatic caps, both stated:** no breaking-change check in the gate → 70; expand-and-contract
with no usage metric → 75.

**Calibration:** median 70–74. This paper marks a little high because most of it is mechanical, and
the spread is in Q1(c), Q4(b) and Q5.

---

## Q1: Audit Your Own API Against Liskov (20)

### (a) [8]

| | |
|---|---|
| 5 | A complete table: method, path, request shape, response shape, status codes |
| 3 | Richardson level per endpoint, **with honest reasons** |

**Spot-check two endpoints against the code.** Audits are written from memory and get status codes
wrong.

**Expected honest answer: level 2 for most, level 1 for any endpoint that returns 200 on failure.**
**A student claiming level 3 must show `_links` in an actual response** — otherwise deduct 2 and note
that HATEOAS means the links exist, not that the state machine exists.

**A student who marks something level 0** — a single `POST /api` that switches on an action field —
has been honest about something bad, and should be credited for the honesty.

### (b) [7]

| | |
|---|---|
| 3 | Three changes, real ones |
| **4** | **Correct classification, with the reason from the table** |

**Mark this strictly; it is the theorem.** Reference classifications:

| Change | Breaking? |
|---|---|
| Add an optional request field | **No** |
| Add a response field | **No** |
| Add a new endpoint | **No** |
| Relax a validation rule | **No** |
| Make an error `detail` more specific | **No** (if `type` is unchanged and documented as prose) |
| Add a **required** request field | **Yes** |
| Remove or rename a response field | **Yes** |
| **Add a required field with a default** | **Yes** — round-tripping clients overwrite user data |
| Tighten validation | **Yes** |
| Change a status code | **Yes** |
| Rename a path | **Yes** |
| Change a field's type, even widening | **Yes** in JSON — a client's parser may be strict |

**Deduct 2 per misclassification.** The most common error is calling *"add a required field with a
default"* non-breaking — **it is L31 §2's first trap and it is worth a feedback note**, because it is
a real outage pattern.

**Deduct 3** if all three changes fall on one side; the paper says so.

### (c) [5]

| | |
|---|---|
| 4 | **Two specific unpromised behaviours in their own API** |
| 1 | Which documented response they can now not change |

**Good answers, and they should be about their code:**

- *"`GET /bookings` returns insertion order because our query has no `ORDER BY`. Our own week-view
  client depends on it. Adding an index could change the plan."* **The `roomsvc` failure, found in
  their own code — full marks.**
- *"Our ids are UUID4 strings, but our tests assert 36 characters. If we moved to ULIDs, our own test
  suite is a client that breaks."* **Excellent, and it identifies their test suite as an API
  consumer, which is a genuinely good observation.**
- *"We never return an empty `_links` object — it is omitted. A client doing `Object.keys(links)`
  would break if we started returning `{}`."*

**2 of 4** for generic answers lifted from the lecture's candidate list without tying them to their
code. **0** for "clients might depend on things".

---

## Q2: Get to Level 2 (20)

### (a) [8]

**1 per correct pairing (5), plus 3 for the 409 and the 500 point.**

| Situation | Correct |
|---|---|
| Slot already confirmed | **409** |
| Outside opening hours | **422** (accept 400 if argued — the line between malformed and semantically invalid is genuinely arguable) |
| Unknown booking id | **404** |
| Authenticated, not the owner | **403** (not 401) |
| Malformed body | **400** (accept 422 — FastAPI returns 422 for validation by default, and a student who notes the framework's choice and keeps it is right) |

**The 3 marks:** 409 for the conflict, **and why a 500 on bad input is a defect** — 5xx means *your*
fault, and returning it for a client error makes every error-rate dashboard and alert wrong (W8
L27 §6), and tells the client to retry something that will never succeed.

**Watch for the real defect**, which several teams will have: an unhandled `IntegrityError` from the
unique index reaching the client as a 500. **A student who finds this in their own code and fixes it
has done the best available version of (a)** — it is the exact seam L31 §4 and W3 L10 §6 both point
at. Full marks and say so.

### (b) [6]

| | |
|---|---|
| 4 | Named transition endpoints, shown |
| 2 | **What `PATCH {"state": "HELD"}` does now, and what it should** |

**The expected answer to the second part:** either there is no `PATCH`, in which case say so and say
it should stay that way; or there is, and it currently permits an illegal transition, which is a bug
**and should return 409 or 422 via the transition table** (W4 L15 §3).

**Full marks and a note** for a student who discovers their `PATCH` allows `CONFIRMED → HELD`,
violating invariant I3. That is a real bug found by this question.

### (c) [6]

| | |
|---|---|
| 3 | A real problem+json body, with `type`, `title`, `status`, `detail` |
| 3 | **The contract/prose distinction documented**, and why it is the only defence |

**Check the `type` is a URI and is stable-looking** — `"type": "error"` misses the point. **Deduct 1**
for a `type` that encodes the detail (`/problems/th200-taken-at-1000`), because that is not a stable
identifier, it is prose in a URI.

**The 3 marks for the distinction** require it to be **written down somewhere a client would read** —
the OpenAPI description, a README section, the schema. **Saying it only in the PDF scores 1.**

---

## Q3: The Schema, and the Check (20)

### (a) [6]

6 for a committed, generated document with the command shown. **4 if hand-written** — it works, and it
will drift, and the paper's own reference file says so. Note it.

**Check it is committed, not generated at request time.** A schema that only exists at
`/openapi.json` cannot be diffed against `main`, which makes (b) impossible — and a student who has
done (b) has necessarily done this right.

### (b) [10]

| | |
|---|---|
| 5 | The step in the gate, green run linked |
| **5** | **Shown failing on a deliberate breaking change** |

**Accept any tool**: `oasdiff breaking`, `openapi-diff`, `buf breaking` for protobuf, or a hand-rolled
script. **A hand-rolled Python script that compares required fields and paths and fails on removals
is entirely acceptable** and arguably better, since they had to decide what "breaking" means.

**The failing demonstration [5]** must show the step exiting non-zero. **2 of 5** for the passing case
only.

**A good failing demonstration** looks like:

```
oasdiff breaking openapi-main.json openapi-head.json
1 breaking changes:
error [response-property-removed] at openapi-head.json
    in API GET /bookings/{id} response 200: removed property 'room_id'
exit status 1
```

### (c) [4]

2 each for two behavioural breaks invisible to a schema diff:

- **Tightened validation inside a handler** — the schema still says `string`, the handler now rejects strings over 40 characters.
- **A changed default** for an optional field.
- **Altered ordering** of a list — the schema says `array`, and Hyrum's law says someone depends on the order.
- **A status code that moved within the same response schema** — 200 to 204, or a conflict that used to be 422 and is now 409.
- **A semantic change** to a field's meaning: `slot` was the start, now it is the midpoint.
- **A rate limit introduced.**

**The last one is the best answer** and about one student in ten gives it: **adding a rate limit is a
breaking change and appears in no schema.**

---

## Q4: One Expand-and-Contract, Properly (25)

### (a) [10]

| | |
|---|---|
| 4 | Both forms accepted on input |
| 3 | Both returned on output |
| 3 | The old one marked deprecated **in the schema**, and a real response shown |

**Check the precedence.** `body.get("resource_id") or body.get("room_id")` is right; reading the
deprecated one first is a bug, because a client sending both (during its own migration) gets the old
value. **Deduct 2** and explain — it is a subtle and real failure.

**Deduct 2** for deprecating in a comment or the PDF rather than in the schema. The marker is
machine-readable or it is not a marker.

### (b) [8]

| | |
|---|---|
| 4 | Instrumentation exists, in the code, with a **caller tag** |
| 4 | **Evidence it has recorded at least one use** |

**This is the heart of the assignment.** The second 4 marks need evidence: a metrics screenshot, a log
line, a counter value, a committed test that asserts the counter increments. **A student who called
their own deprecated endpoint with `curl` and showed the resulting log line has satisfied it** — the
paper says so explicitly.

**Deduct 2** for instrumentation with no caller identification. **The tag is what turns an impossible
removal into three emails**, and that is the whole argument.

**Apply the 75 cap** if there is no instrumentation at all.

### (c) [7]

**All four things, and check them against the response headers:**

| | |
|---|---|
| 2 | Machine-readable marker — `Deprecation` header, or `deprecated: true` in the schema |
| **2** | **A date** — in the `Sunset` header, not "soon" |
| 1 | The usage metric, cross-referenced to (b) |
| 2 | **A named replacement**, and **the card on the board, linked** |

**The card is checkable** and about half of students will skip it. **It is 1 of the 2**, and the point
is L33 §5's closing line: a deprecation that is not scheduled work does not happen. **Look at the
board.**

---

## Q5: The Ones You Did Not Choose (15)

### (a) [6]

| | |
|---|---|
| 3 | What the SQL alternative keeps |
| 3 | **Three of the five costs**, named specifically |

**What it keeps:** HTTP caching (free, by URL), bounded query cost (per endpoint, by construction),
one permission check, meaningful status codes, and `curl`-debuggability.

**The five costs:** caching gone; N+1 moved into resolvers; unbounded query cost; **errors return
200**, so every HTTP-level tool sees success; per-field authorisation.

**Deduct 3** for "GraphQL is more complex" with no specifics.

**The argue-for route is fully creditable** and must be honoured. It requires: a named client they do
not control, a story for bounding cost (depth limit, complexity budget, persisted queries), and a
story for caching (normalised client cache, persisted queries as GET). **A student who does all three
scores 6** — and it is a harder answer than the expected one.

### (b) [5]

| | |
|---|---|
| 3 | **The number is the contract; the name is not** — with the consequence that renaming is free and reusing a number is catastrophic, and `reserved` exists for it |
| 2 | Which they would rather have, with a reason |

**Both preferences are creditable.** *"JSON's, because our clients are humans reading responses in a
browser and a meaningful name is worth more than a free rename"* → 2. *"Protobuf's, because our worst
API problem is that we cannot rename anything"* → 2.

**Deduct 3** for an answer that says only "protobuf is binary".

### (c) [4]

| | |
|---|---|
| 2 | **Who chooses when the upgrade happens** — a library consumer chooses; a service consumer is upgraded when you deploy |
| 1 | So a MAJOR bump on a service means "we broke you, now" |
| 1 | What `slot` uses instead |

**Full marks and a note** for a student who adds that *"breaking" is decided by the author and
experienced by the user* — which is Hyrum's law appearing for the third time in the paper and is the
connection the final exam rewards.

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Honest Richardson levels including a level-0 admission if true. All three changes correctly classified, on both sides. Two Hyrum's-law exposures in their own code. The unhandled `IntegrityError` found and fixed, or an equivalent real status-code defect. Contract/prose distinction documented where a client reads it. **CI check shown failing.** A usage metric with a caller tag that has recorded a real call, and a dated card on the board. GraphQL argued down with three specific costs |
| **75–89** | Audit complete, level 2 reached, schema committed and checked, expand-and-contract instrumented, Q5 correct |
| **60–74** | Levels asserted. One misclassification. Schema committed, no CI check (capped at 70). Expand done, measurement absent (capped at 75). Q5 from the lecture |
| **45–59** | No schema in CI, no instrumentation, status codes unexamined, deprecation with no date |
| **< 45** | No versioning, no schema, nothing in the repository |

**Feedback note for every paper:** name the one breaking change they are most likely to want to make
before May, and ask whether their gate would catch it. **Week 11's debt register and the final report
both ask them to prioritise**, and an API compatibility item is the kind of debt teams never think to
put on a register.

---

*CS 212 · Week 10 · A 10 marking guidance · INSTRUCTOR ONLY*
