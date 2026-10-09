# CS 212 · Software Engineering
## Week 8 · Lecture 2 of 3
### Docker, and the Image You Ship

*“Every program is a part of some other program and rarely fits.”* — Alan Perlis, "Epigrams on Programming" (1982), #4

---

**Sat:** Wednesday of Week 8, 10:00–10:50, TH 200 · **Reading:** Docker docs, "Best practices for writing Dockerfiles"; the Twelve-Factor App, factors III, V and X · **Next:** L27, deployment

**Coursework:** 📝 **Assignment 8** released today 17:00, due Fri of Week 9 17:00 · 📝 **Assignment 7** due Fri this week 17:00 · 📊 **Quiz 9** Tue of Week 9
**A 8 is released after this lecture**, Wednesday 17:00.

---

## 1. What a Container Actually Is

**It is not a virtual machine, and the difference is the whole reason it is fast.**

A virtual machine runs a **kernel**. A container is **a process on your kernel**, with three things restricted:

| Mechanism | What it does |
|---|---|
| **Namespaces** | The process sees its own PIDs, mounts, network interfaces, hostname, users. **It cannot see yours** |
| **cgroups** | Its CPU, memory and I/O are limited and accounted |
| **A union filesystem** | Its root filesystem is assembled from read-only layers plus one writable layer |

**CS 202 is teaching you exactly this from the other side.** Its Week 10 is virtualization and its Week 12 covers `seccomp`; **namespaces and cgroups are kernel features, and a container is a configuration of them, not a new kind of thing.** *(Which is also why a container shares your kernel — a Linux container cannot run on a Windows kernel, and Docker Desktop is quietly running a Linux VM to provide one.)*

**The consequence that matters for engineering:** a container starts in milliseconds because **there is no kernel to boot.** That is what makes the session-scoped Postgres in your tests (W5 L16 §5) cost 9 seconds rather than 40.

---

## 2. What It Buys, and What It Does Not

**Buys:**

| | |
|---|---|
| **A reproducible filesystem** | The same libraries, the same versions, the same paths, on every machine |
| **An artefact** | One thing you build, test, and deploy — **not a thing you rebuild on the server** |
| **Isolation of dependencies** | Postgres 16 for `slot` and Postgres 14 for another project, simultaneously |
| **Fast, disposable infrastructure in tests** | The reason your integration tests can use real Postgres at all |

**Does not buy — and this is where teams are surprised:**

| | Why |
|---|---|
| **"Works on my machine" immunity** | **§3.** Containers fix the filesystem, not the environment |
| **Security isolation equal to a VM** | Shared kernel means a kernel vulnerability crosses the boundary. Containers are a *good* boundary, not a *strong* one |
| **Any architectural property** | A monolith in a container is a monolith. **A container is a packaging decision, not a design one** |
| **Performance** | Roughly native on Linux; **noticeably slower for filesystem-heavy work on macOS and Windows**, where a VM is involved |

> **The third row is worth saying out loud in your Phase 1 or final viva.** "We containerised it" is
> not an architecture. It is how the thing is shipped.

---

## 3. Why "Works On My Machine" Survives Docker

**Everybody expects containers to end this, and they do not, for five specific reasons.** Every one of these will happen to your team.

| What still differs | What happens |
|---|---|
| **Environment variables** | The container is identical; `DATABASE_URL` is not. **The commonest CI-passes-locally-fails cause by a wide margin** |
| **Volume mounts** | Your `docker-compose.yml` mounts `./src`; the CI image bakes it in. **You have been testing your local files, not the image** |
| **The build context and `.dockerignore`** | You have a `.env` locally that is not committed. The image builds without it and fails at import |
| **Architecture** | An image built on an Apple Silicon laptop is `arm64`; CI is `amd64`. **A wheel that exists for one and not the other fails only in one place** |
| **Base image tags** | `FROM python:3.12` is **not** a version. It moved last Tuesday. **Pin the digest or a patch version** |

**The fourth row costs teams a whole evening every year**, and the fix is one flag:

```bash
docker build --platform linux/amd64 -t slot:dev .
```

**The fifth is the most insidious**, because it produces a build that worked yesterday and fails today with no change to your code:

```dockerfile
FROM python:3.12               # ❌ a moving target
FROM python:3.12.3-slim        # ✅ better
FROM python:3.12.3-slim@sha256:1e4...   # ✅✅ reproducible
```

---

## 4. A Dockerfile Worth Copying

**Every line here is a decision, and the comments say which.**

```dockerfile
# ---- build stage: has compilers, is thrown away -------------------------
FROM python:3.12.3-slim AS build
WORKDIR /app

# Dependencies first, and ONLY the dependency files.  This layer is cached
# unless the lockfile changes -- which is the single biggest CI speed win.
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev

# Source last, because it changes on every commit and invalidates
# everything below it.
COPY src/ ./src/

# ---- runtime stage: no compilers, no build tools, much smaller ---------
FROM python:3.12.3-slim AS runtime
WORKDIR /app

# Do not run as root.  A container escape from root is a much worse day.
RUN useradd --create-home --uid 10001 slot
USER slot

COPY --from=build /app/.venv /app/.venv
COPY --from=build /app/src   /app/src
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1

# Config comes from the environment, never from a baked-in file
# (Twelve-Factor III).  No defaults for secrets.
ENV DATABASE_URL=""

EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=2s --start-period=5s \
  CMD python -c "import urllib.request,sys; \
    sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["uvicorn", "slot.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**The five decisions, in order of how much they matter:**

1. **Layer ordering.** Dependencies before source. **This is a pure caching win** and it is the difference between a 4-minute and a 20-second rebuild — and `roomsvc`'s pipeline spends 4:10 not doing it (L25 §4).
2. **Multi-stage.** The runtime image has no compiler, no `gcc`, no build headers. **Smaller, and a much smaller attack surface.**
3. **Non-root.** One line. **A container escape as `root` is categorically worse than one as uid 10001.**
4. **No config baked in.** Twelve-Factor factor III: configuration comes from the environment, because **the same image must run in test and in production.** An image with a hard-coded database URL is not an artefact, it is an environment.
5. **A healthcheck.** Which is what lets `docker compose up --wait` and your deployment know when the thing is actually ready, rather than merely started.

---

## 5. Compose, and the Test Database

**`docker-compose.yml` is for development and tests, not for production.** Its job is: one command brings up everything.

```yaml
services:
  db:
    image: postgres:16.3-alpine
    environment:
      POSTGRES_PASSWORD: dev          # dev only. Never a real secret here.
      POSTGRES_DB: slot
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 2s
      retries: 15
    tmpfs: /var/lib/postgresql/data    # ← in RAM. Much faster, and disposable.

  app:
    build: .
    depends_on:
      db: {condition: service_healthy}   # ← waits for ready, not for started
    environment:
      DATABASE_URL: postgresql://postgres:dev@db:5432/slot
    ports: ["8000:8000"]
    volumes: ["./src:/app/src"]          # dev only; the CI image has no mount
```

**Three lines are worth more than the rest:**

- **`tmpfs` on the data directory.** The test database lives in RAM. **Typically 2–4× faster on write-heavy test suites, and it disappears when the container does** — which is what you want.
- **`condition: service_healthy`.** Without it, `depends_on` waits only for the container to *start*, and your app races Postgres's initialisation. **This is the cause of about half of all "flaky CI" reports in this project.**
- **`db` as the hostname.** Not `localhost`. The service name is the DNS name — the single most common first-day container confusion (W1's walking skeleton predicted it).

---

## 6. The Image Is the Artefact

**The principle that makes deployment safe** (and L27 builds on it):

> **Build the image once. Test *that* image. Promote *that* image.** Never rebuild for production.

**Why rebuilding is dangerous, concretely:** a rebuild resolves dependencies again. Between your test run and your production build, a transitive dependency published a patch. **The thing you tested and the thing you deployed are different**, and nothing in your pipeline can tell you.

**So the pipeline shape is:**

```
build → tag with the commit SHA → run all tests against that tag
      → promote the same tag to staging → promote the same tag to production
```

**Tag with the commit SHA, not with `latest`.** `latest` is not a version; it is a mutable pointer, and it makes *"what is running in production?"* unanswerable — which is the question you most need answered during an incident.

**And `slot`'s version of the Knight Capital problem is here.** Their eighth server ran different code from the other seven. **An image tagged with a SHA, deployed by a pipeline that verifies every target reports that SHA, is the mechanism that makes that impossible.** L27 §4.

---

## 7. Migrations, Which Are the Hard Part

**Containers make code deployment easy and change nothing about the database**, which is where your real risk is. Three rules, and they are not optional.

**1. Migrations run as a separate step, not on application startup.**

```yaml
# a job, before the deploy
- run: docker run --rm -e DATABASE_URL=$PROD_URL slot:$SHA alembic upgrade head
```

**Why:** with three application replicas starting simultaneously, three migration runs race. And a failed migration inside a startup path produces a crash loop rather than a clear failure.

**2. Every migration must be backward-compatible with the *currently running* code.**

Because during any rolling deployment, **old and new code run at the same time against one schema.** So a column rename is never one migration:

| Step | Migration | Code |
|---|---|---|
| 1 | Add `resource_id`, nullable | — |
| 2 | — | Write both columns, read the old |
| 3 | Backfill | — |
| 4 | — | Read the new |
| 5 | Drop `room_id` | — |

**Five deploys to rename a column.** That is not bureaucracy; it is what "no downtime" costs, and **a team that discovers this in May discovers it during their demo.**

**3. Test the migration against realistic data**, and **test that it runs backwards at least once.** A migration that has never been reversed is a migration you cannot roll back — which means your rollback plan is fiction.

---

## 8. Summary

- **A container is a process on your kernel** with namespaces, cgroups and a union filesystem — **not a VM.** No kernel to boot is why it starts in milliseconds and why your test Postgres costs 9 s.
- **It buys a reproducible filesystem, an artefact, dependency isolation and fast disposable test infrastructure.** It does **not** buy "works on my machine" immunity, VM-grade security isolation, or **any architectural property** — containerising is a packaging decision.
- **Five things still differ**: environment variables (the commonest cause by far), volume mounts (**you may have been testing your local files, not the image**), the build context, **architecture** (`--platform linux/amd64`), and **unpinned base tags** — `FROM python:3.12` moved last Tuesday.
- **The Dockerfile's five decisions:** dependency layers before source (**the biggest CI speed win**), multi-stage, non-root, **no config baked in** (Twelve-Factor III, because the same image must run everywhere), and a healthcheck.
- **Compose: `tmpfs` for the test database, `condition: service_healthy`** (about half of all "flaky CI" in this project), and **the service name is the hostname.**
- **Build once, test that image, promote that image.** Tag with the **commit SHA**, never `latest`, or *"what is running in production?"* is unanswerable during an incident.
- **Migrations are the hard part**: a separate step, **backward-compatible with running code** — five deploys to rename a column — and **reversed at least once**, or your rollback plan is fiction.

**Next:** L27 — deployment: pipelines, environments, how to fail safely, and the answer to Knight Capital's eighth server.

---

*CS 212 · Week 8 · L26 · © CSE Department*
