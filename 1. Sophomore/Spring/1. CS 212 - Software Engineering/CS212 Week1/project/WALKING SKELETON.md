# CS 212 · The Walking Skeleton
## Due Friday of Week 1, 17:00, in your repository

---

> **This is the highest-value thing your team does all term, and it takes an evening.** Every
> previous cohort's retrospectives contain the sentence *"we should have done the skeleton in
> Week 1"*, written by teams who did it in Week 4.

---

## 1. What It Is

Cockburn's definition:

> *A Walking Skeleton is a tiny implementation of the system that performs a small end-to-end
> function. It need not use the final architecture, but it should link together the main
> architectural components.*

**Thin, ugly, whole.** The emphasis is on the third word.

---

## 2. The Deliverable, Exactly

```
POST /bookings
  {"resource": "TH200", "slot": "2026-03-04T10:00:00Z"}
  → 201 {"id": "...", "resource": "TH200", "slot": "...", "state": "CONFIRMED"}

GET /bookings/{id}
  → 200 {"id": "...", "resource": "TH200", "slot": "...", "state": "CONFIRMED"}
```

**Through every layer.** HTTP route → a service function → a real SQLAlchemy insert → a real PostgreSQL running in a container. Not an in-memory dict. Not SQLite standing in for Postgres. **The point is to find out whether the pieces connect**, and a dict connects to nothing.

Plus:

- [ ] **`docker compose up` brings up the app and the database**, on every member's laptop
- [ ] **One test** that POSTs and GETs against the containerised stack, and passes
- [ ] **A GitHub Actions workflow** that runs it on every push, and a green check on `main`
- [ ] **A `README.md`** whose "how to run this" section is three lines and is correct

---

## 3. What It Deliberately Does Not Have

Resist all of it. Every item here is a thing teams add instead of finishing.

| Not now | When |
|---|---|
| Authentication | Week 3, after you have decided where it lives |
| A user interface | Whenever. Server-rendered HTML; no marks for CSS |
| Validation | Week 2 |
| **The double-booking check** | **Week 5** — and by then you will know to do it with a constraint |
| Error handling beyond a 500 | Week 3 |
| Migrations tooling | Nice to have now; required by Week 3 |
| Any second endpoint | No |

**A skeleton with a login page and no database is not a skeleton.** It is a login page.

---

## 4. The Failure Modes, Named in Advance

These are what the exercise is for. **You want to meet all of them this week.**

| What goes wrong | Why it is good that it goes wrong now |
|---|---|
| Three members have three Python versions | In Week 1 you standardise on 3.12 and add a `.python-version`. In Week 9 it is a two-day debugging session about a failing test that passes locally |
| The app cannot reach the database container | The service name is the hostname, not `localhost`. **Everyone learns this once.** Better now |
| CI passes locally and fails in Actions | Almost always an environment variable or a missing service container. **This is the single most common Week 8 crisis, met cheaply in Week 1** |
| Nobody can agree where files go | You now have a directory layout. Week 3 will change it, from a position of having one |
| The migration ran on one laptop and not another | You have discovered that you need a migration tool. Add Alembic on Monday |

**If nothing goes wrong, you have not connected real components.** Check that your test is hitting the containerised Postgres and not a local one.

---

## 5. A Sane Starting Layout

Not prescriptive. Week 3 will make you justify it, and you may well change it then.

```
slot/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
├── docs/
│   ├── charter.md
│   ├── domain-model.md
│   └── adr/                 # empty until Week 3; create it now
├── src/slot/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, routes
│   ├── models.py            # SQLAlchemy
│   └── service.py           # the one function that does the work
├── tests/
│   └── test_skeleton.py
└── .github/workflows/ci.yml
```

**`service.py` exists from day one for a reason.** It is one function and it looks pointless today. It is the seam between "the web" and "the domain", and Week 3 is about that seam. **Teams that put the database call directly in the route handler spend Week 3 undoing it.**

---

## 6. Split the Work Like This

Four people, one evening, roughly parallel:

| Person | Does | Blocked by |
|---|---|---|
| A | `docker-compose.yml` + `Dockerfile`, Postgres service, connection string | nobody |
| B | `models.py` and the migration/table creation | agreeing the two columns |
| C | `main.py` routes + `service.py` | agreeing the JSON shape |
| D | `tests/test_skeleton.py` + `.github/workflows/ci.yml` | agreeing the JSON shape |

**Agree the JSON shape and the two column names in the first ten minutes, out loud, together.** Then go. **Integrate in the same sitting** — not the next day. The integration is the deliverable; the four parts are not.

> **A fifth member takes the `README.md` and `docs/charter.md`**, which is not a consolation prize:
> the "how to run this" section has to be tested on someone else's laptop, and it is the only
> document in the repository that is read by a stranger under time pressure.

---

## 7. Checking You Are Done

From a clean clone, on a machine that has never run it:

```console
$ git clone <your repo> && cd slot
$ docker compose up -d
$ curl -sX POST localhost:8000/bookings \
     -H 'content-type: application/json' \
     -d '{"resource":"TH200","slot":"2026-03-04T10:00:00Z"}'
{"id":"b1f3...","resource":"TH200","slot":"2026-03-04T10:00:00Z","state":"CONFIRMED"}
$ curl -s localhost:8000/bookings/b1f3...
{"id":"b1f3...","resource":"TH200","slot":"2026-03-04T10:00:00Z","state":"CONFIRMED"}
```

**And the green check on the commit in GitHub.**

**Have one member do exactly this on a laptop that has not been used for development**, before Friday. It will fail the first time. That is the test working.

---

*CS 212 · Week 1 · Walking Skeleton · unmarked this week; 70% of Phase 1 depends on it*
