#!/usr/bin/env python3
"""
Static site generator for the CSE degree vault.

    python3 site/build.py                     # build once into _site/
    python3 site/build.py --serve             # build, then serve on :8000
    python3 site/build.py --watch --serve     # serve, rebuild on change
    python3 site/build.py --serve --port 9000 # serve somewhere else
    python3 site/build.py --serve --port 0    # let the OS pick a free port

--host HOST and --port PORT (or --host=HOST, --port=PORT) override the default
bind address of 127.0.0.1:8000. Port 0 asks the OS for any free port; either
way the address actually bound is what gets printed.

No third-party dependencies. KaTeX is vendored under site/vendor/katex, so the
generated site renders maths with no network access.

The vault's directory layout is regular, and the generator relies on it:

    <Year>/<Semester>/<Course>/<Course><Week>/<section>/<file>.md

Anything that does not fit that shape (the Academic Registry, for instance) is
still rendered; it simply lands in a generic folder tree.
"""

import html
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import markdown as md  # noqa: E402
import dashboard  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.dirname(HERE)
OUT = os.path.join(VAULT, "_site")

SKIP_DIRS = {".git", ".obsidian", ".claude", "site", "_site", "node_modules", "__pycache__"}
# Each course under Submissions is its own git repo; it is not course material.
SKIP_PATHS = {os.path.join("5. Academic Registry", "4. Submissions")}

SECTION_LABELS = {
    "lectures": "Lectures",
    "assignments": "Assignments",
    "lab": "Lab",
    "labs": "Labs",
    "recitation": "Recitation",
    "quiz": "Quiz",
    "quizzes": "Quizzes",
    "resources": "Resources",
    "solutions_instructor": "Solutions",
}
SECTION_ORDER = ["lectures", "lab", "labs", "recitation", "assignments",
                 "quiz", "quizzes", "resources", "solutions_instructor"]

SOLUTION_MARKERS = re.compile(r"NOT FOR STUDENTS|INSTRUCTOR ONLY", re.I)
# Word-bounded: without \b, "solution" matches inside "Collision Resolution"
# and gates two perfectly ordinary hash-table lectures.
SOLUTION_NAME = re.compile(
    r"\b(solutions?|answer\s+key|instructor\s+only|marking\s+scheme)\b", re.I)


def strip_fences(text):
    """Drop fenced blocks. A week README that merely *lists*
    `solutions_instructor/ ... NOT FOR STUDENTS` inside its directory tree is
    describing the folder, not being one."""
    out, infence = [], False
    for ln in text.split("\n"):
        if ln.lstrip().startswith(("```", "~~~")):
            infence = not infence
            continue
        if not infence:
            out.append(ln)
    return "\n".join(out)


def looks_like_solutions(src, parts, stem):
    """Is this page *itself* solutions, as opposed to a page that mentions them?

    Week READMEs describe their own folder -- in a directory-tree fence, or in a
    contents table row like `| solutions_instructor/ | ... instructor only |`.
    Those are references, not declarations, so a bare content search gates the
    week overview and makes the whole week look locked.
    """
    if "solutions_instructor" in parts:
        return True
    if SOLUTION_NAME.search(stem):
        return True
    try:
        text = strip_fences(open(src, encoding="utf-8").read())
    except OSError:
        return False
    seen = 0
    for ln in text.split("\n"):
        s = ln.strip()
        if not s or s.startswith("|"):
            continue  # table rows point at other files
        seen += 1
        if seen > 15:
            break
        # A page-level declaration sits near the top, in a heading or a callout.
        if SOLUTION_MARKERS.search(s):
            return True
    return False
ORDINAL_RE = re.compile(r"^\d+\.\s*")
COURSE_RE = re.compile(r"^(?:\d+\.\s*)?([A-Z]{2,5}\s?\d{2,3})\s*[-–—:]\s*(.*)$")
WEEK_RE = re.compile(r"^[A-Z]*\s?\d*\s*Week\s*(\d+)$", re.I)


def slug(text):
    text = ORDINAL_RE.sub("", text)
    text = text.replace("&", " and ")
    text = re.sub(r"[^\w\s-]", "", text, flags=re.U).strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-") or "item"


def clean_title(name):
    return ORDINAL_RE.sub("", name).strip()


def describe_dir(name):
    """Return (slug, display title, kind) for one directory component."""
    m = COURSE_RE.match(name)
    if m:
        code, title = m.group(1), m.group(2).strip()
        return slug(code), "%s · %s" % (code, title), "course"
    m = WEEK_RE.match(name.strip())
    if m:
        n = int(m.group(1))
        return "week-%d" % n, "Week %d" % n, "week"
    t = clean_title(name)
    if t.lower() in SECTION_LABELS:
        return t.lower(), SECTION_LABELS[t.lower()], "section"
    return slug(name), t, "folder"


class Page:
    def __init__(self, src, route, title, crumbs, kind, week_route, is_solution):
        self.src = src
        self.route = route          # e.g. freshman/fall/math-141/week-0/lectures/x.html
        self.title = title
        self.crumbs = crumbs        # list of (title, route|None)
        self.kind = kind            # 'page' | 'index'
        self.week_route = week_route
        self.is_solution = is_solution
        self.html = ""
        self.headings = []
        self.text = ""
        self.words = 0
        self.math = 0


def walk():
    """Collect directories and markdown files into a navigable tree."""
    nodes = {}          # dirroute -> dict(title, kind, children[], parent, page)
    pages = []

    def ensure(dirroute, title, kind, parent):
        if dirroute not in nodes:
            nodes[dirroute] = {"route": dirroute, "title": title, "kind": kind,
                               "parent": parent, "children": [], "pages": [], "index": None}
            if parent is not None:
                nodes[parent]["children"].append(dirroute)
        return nodes[dirroute]

    ensure("", "CSE Degree", "root", None)

    for root, dirs, files in os.walk(VAULT):
        rel = os.path.relpath(root, VAULT)
        rel = "" if rel == "." else rel
        if any(rel == s or rel.startswith(s + os.sep) for s in SKIP_PATHS):
            dirs[:] = []
            continue
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        if rel == "":
            dirroute, crumbs, week_route = "", [], None
        else:
            parts = rel.split(os.sep)
            segs, crumbs, week_route = [], [], None
            for i, part in enumerate(parts):
                s, t, kind = describe_dir(part)
                segs.append(s)
                sofar = "/".join(segs)
                crumbs.append((t, sofar))
                if kind == "week":
                    week_route = sofar
            dirroute = "/".join(segs)
            parent = "/".join(segs[:-1])
            _, t, kind = describe_dir(parts[-1])
            ensure(dirroute, t, kind, parent)
            nodes[dirroute]["week_route"] = week_route
            nodes[dirroute]["crumbs"] = crumbs

        for fn in sorted(f for f in files if f.endswith(".md")):
            src = os.path.join(root, fn)
            stem = fn[:-3]
            crumbs = nodes[dirroute].get("crumbs", []) if dirroute else []
            wr = nodes[dirroute].get("week_route") if dirroute else None
            is_sol = looks_like_solutions(src, root.split(os.sep), stem)
            if stem.upper() == "README":
                route = (dirroute + "/index.html") if dirroute else "index.html"
                title = nodes[dirroute]["title"] if dirroute else "CSE Degree"
                p = Page(src, route, title, crumbs, "index", wr, is_sol)
                nodes[dirroute]["index"] = p
            else:
                route = ((dirroute + "/") if dirroute else "") + slug(stem) + ".html"
                p = Page(src, route, clean_title(stem), crumbs + [(clean_title(stem), None)],
                         "page", wr, is_sol)
                nodes[dirroute]["pages"].append(p)
            pages.append(p)
    return nodes, pages


def slug_path(target):
    """Slug each segment of a wikilink target, keeping the separators."""
    return "/".join(slug(seg) for seg in target.split("/") if seg)


def build_link_resolver(pages):
    """Map wikilink targets to routes, by any trailing fragment of a page's path.

    The vault writes links in two forms and both have to work:

        [[Reading Guide Week 1]]
        [[MATH241 Week1/resources/Reading Guide Week 1|Reading Guide Week 1]]

    The second is not decoration. 166 filename stems are shared by two or more
    pages -- every `summary`, all 138 `README`s, and every per-week reading
    guide and solutions sheet -- so a bare stem names a unique page less than
    half the time, and the path form is how the authors say which one they
    meant. Matching on the stem alone ignored it, which left 435 of the vault's
    1,059 rendered wikilinks broken -- 41% -- including every course's link to
    `Year2 - Sophomore/COURSE POLICIES`.

    So each page is registered under **every suffix of its own path**: a target
    resolves as soon as it is specific enough to pick the page out. Keys hold a
    list rather than one route, because a suffix can still be shared --
    `resources/Reading Guide Week 1` names seven pages -- and `resolve_target`
    settles those by proximity.
    """
    table = {}
    for p in pages:
        rel = os.path.splitext(os.path.relpath(p.src, VAULT))[0]
        parts = rel.split(os.sep)
        for i in range(len(parts)):
            frag = "/".join(parts[i:])
            for key in {frag.lower(), slug_path(frag)}:
                table.setdefault(key, []).append(p.route)
    return table


def resolve_target(table, target, from_route):
    """Route for one wikilink target, or None if nothing matches.

    Where a target still names several pages, the nearest one to the page doing
    the linking wins -- a bare `[[summary]]` in CS 201 Week 3 means that week's,
    not CS 101's. `max` keeps the first of equal candidates, so a genuine tie
    falls back to walk order, which is what the stem-only table did for every
    ambiguous name.
    """
    target = target.strip().strip("/")
    routes = table.get(target.lower()) or table.get(slug_path(target))
    if not routes:
        return None
    if len(routes) == 1:
        return routes[0]
    here = from_route.split("/")

    def shared(route):
        other = route.split("/")
        n = 0
        while n < len(here) and n < len(other) and here[n] == other[n]:
            n += 1
        return n

    return max(routes, key=shared)


def rel_prefix(route):
    depth = route.count("/")
    return "../" * depth


def strip_html(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preload" as="font" type="font/woff2" crossorigin
      href="{pre}vendor/fonts/source-serif-4-latin-wght-normal.woff2">
<link rel="preload" as="font" type="font/woff2" crossorigin
      href="{pre}vendor/fonts/inter-latin-wght-normal.woff2">
<link rel="stylesheet" href="{pre}vendor/katex/katex.min.css">
<link rel="stylesheet" href="{pre}assets/app.css">
</head>
<body data-route="{route}" data-week="{week}" data-prefix="{pre}">
<button id="navToggle" aria-label="Show navigation" title="Show navigation (\\)">&#9776;</button>
<div id="scrim"></div>
<aside id="sidebar">
  <div class="rail-top">
    <a class="brand" href="{pre}index.html">CSE Degree</a>
    <button id="railToggle" aria-label="Collapse sidebar" title="Collapse sidebar (\\)">
      <span aria-hidden="true">&#8249;</span>
    </button>
  </div>
  <div class="search">
    <input id="q" type="search" placeholder="Search" aria-label="Search" autocomplete="off" spellcheck="false">
    <div id="results"></div>
  </div>
  <div id="progress" class="progress"></div>
  <nav id="nav" aria-label="Course navigation"></nav>
</aside>
<main>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
    <article id="content">{body}</article>
    <aside id="toc" aria-label="On this page"></aside>
  </div>
</main>
<script src="{pre}vendor/katex/katex.min.js"></script>
<script src="{pre}vendor/katex/auto-render.min.js"></script>
<script src="{pre}assets/app.js"></script>
</body>
</html>
"""


def render_crumbs(page, pre):
    out = ['<a href="%sindex.html">Home</a>' % pre]
    for title, route in page.crumbs:
        if route:
            out.append('<a href="%s%s/index.html">%s</a>' % (pre, route, html.escape(title)))
        else:
            out.append('<span>%s</span>' % html.escape(title))
    return '<span class="sep">/</span>'.join(out)


def week_control(page):
    if not page.week_route:
        return ""
    return ('<div class="week-done" data-week="%s">'
            '<button class="mark" type="button"></button></div>' % html.escape(page.week_route, True))


def gate(body, count_hint=""):
    return (
        '<div class="gate">'
        '<span class="lock" aria-hidden="true">&#9788;</span>'
        '<button class="reveal" type="button">Reveal solutions%s</button>'
        '<p class="gate-note">Hidden by default so you can attempt the problems '
        'first. Nothing is recorded either way.</p>'
        '</div><div class="gated" hidden>%s</div>' % (count_hint, body)
    )


def build_index_body(node, nodes, pre, existing=""):
    """Listing for a directory that has no README, or appended to one that does."""
    blocks = []
    kids = [nodes[c] for c in node["children"]]
    kids_sorted = sorted(
        kids,
        key=lambda k: (SECTION_ORDER.index(os.path.basename(k["route"]))
                       if os.path.basename(k["route"]) in SECTION_ORDER else 99,
                       natural_key(k["title"])),
    )
    for kid in kids_sorted:
        items = []
        for p in kid["pages"]:
            cls = ' class="sol"' if p.is_solution else ""
            items.append('<li%s><a href="%s%s">%s</a></li>' % (cls, pre, p.route, html.escape(p.title)))
        sub = ""
        if kid["children"] or kid["index"]:
            sub = ' <a class="more" href="%s%s/index.html">open</a>' % (pre, kid["route"])
        blocks.append('<section class="group"><h3>%s%s</h3>%s</section>' % (
            html.escape(kid["title"]), sub,
            ("<ul>%s</ul>" % "".join(items)) if items else ""))
    own = []
    for p in node["pages"]:
        cls = ' class="sol"' if p.is_solution else ""
        own.append('<li%s><a href="%s%s">%s</a></li>' % (cls, pre, p.route, html.escape(p.title)))
    if own:
        blocks.insert(0, '<section class="group"><h3>Pages</h3><ul>%s</ul></section>' % "".join(own))
    if not blocks:
        return existing
    return existing + '<div class="listing">%s</div>' % "".join(blocks)


def natural_key(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def main(quiet=False):
    nodes, pages = walk()
    link_table = build_link_resolver(pages)

    # ---- render every markdown file -------------------------------------
    for p in pages:
        pre = rel_prefix(p.route)

        def resolve(target, _pre=pre, _route=p.route):
            route = resolve_target(link_table, target, _route)
            return (_pre + route) if route else None

        try:
            raw = open(p.src, encoding="utf-8").read()
        except OSError as e:
            print("  skip %s (%s)" % (p.src, e))
            continue
        body, headings = md.render(raw, resolve_link=resolve)
        p.html, p.headings = body, headings
        plain = strip_html(body)
        p.text = plain[:1500]
        p.words = len(plain.split())
        p.math = body.count('class="math-')

    # ---- write pages -----------------------------------------------------
    # Build into a staging directory and swap it in at the end. Deleting OUT
    # first would 404 the whole site for the ~3s a rebuild takes, which the
    # watcher would do on every keystroke-triggered save.
    STAGE = OUT + ".building"
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(STAGE, exist_ok=True)

    written = 0
    for route, node in nodes.items():
        idx = node["index"]
        pre = rel_prefix((route + "/index.html") if route else "index.html")
        if idx:
            body = idx.html + build_index_body(node, nodes, pre)
            page = idx
        else:
            if route == "":
                continue  # home page is generated separately
            page = Page(None, route + "/index.html", node["title"],
                        node.get("crumbs", []), "index", node.get("week_route"), False)
            body = "<h1>%s</h1>" % html.escape(node["title"])
            body += build_index_body(node, nodes, pre)
            pages.append(page)
        page.html = body

    for p in pages:
        if not p.html:
            continue
        pre = rel_prefix(p.route)
        body = p.html
        if p.is_solution:
            body = gate(body)
        body += week_control(p)
        out_path = os.path.join(STAGE, p.route)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(SHELL.format(
                title=html.escape(p.title) + " · CSE Degree",
                pre=pre,
                route=html.escape(p.route, True),
                week=html.escape(p.week_route or "", True),
                crumbs=render_crumbs(p, pre),
                body=body,
            ))
        written += 1

    # ---- home dashboard --------------------------------------------------
    weeks = sorted({p.week_route for p in pages if p.week_route})
    stats = dashboard.collect(nodes, pages, VAULT)
    home = dashboard.render(stats, pre="")
    with open(os.path.join(STAGE, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(SHELL.format(title="CSE Degree", pre="", route="index.html", week="",
                              crumbs='<span>Home</span>', body=home).replace(
            '<body data-route="index.html"', '<body class="dash" data-route="index.html"'))
    written += 1

    # ---- nav + search indexes -------------------------------------------
    def nav_node(route):
        n = nodes[route]
        kids = sorted((nav_node(c) for c in n["children"]),
                      key=lambda d: natural_key(d["t"]))
        files = sorted(
            ({"t": p.title, "r": p.route, "s": 1 if p.is_solution else 0} for p in n["pages"]),
            key=lambda d: natural_key(d["t"]),
        )
        return {"t": n["title"], "r": (route + "/index.html") if route else "index.html",
                "k": n["kind"], "w": n.get("week_route") or "", "c": kids, "p": files}

    nav = nav_node("")
    search = [{"t": p.title, "r": p.route,
               "b": " › ".join(t for t, _ in p.crumbs[:-1]) if p.crumbs else "",
               "h": [h[1] for h in p.headings][:40], "x": p.text}
              for p in pages if p.text]

    os.makedirs(os.path.join(STAGE, "assets"), exist_ok=True)
    with open(os.path.join(STAGE, "assets", "nav.json"), "w", encoding="utf-8") as fh:
        json.dump(nav, fh, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(STAGE, "assets", "search.json"), "w", encoding="utf-8") as fh:
        json.dump({"weeks": weeks, "docs": search}, fh, ensure_ascii=False, separators=(",", ":"))

    for asset in ("app.css", "app.js"):
        shutil.copy(os.path.join(HERE, "assets", asset), os.path.join(STAGE, "assets", asset))
    shutil.copytree(os.path.join(HERE, "vendor"), os.path.join(STAGE, "vendor"))

    # swap: near-instant, so a reader never sees a half-built site
    RETIRE = OUT + ".old"
    if os.path.isdir(RETIRE):
        shutil.rmtree(RETIRE, ignore_errors=True)
    if os.path.isdir(OUT):
        os.rename(OUT, RETIRE)
    os.rename(STAGE, OUT)
    shutil.rmtree(RETIRE, ignore_errors=True)

    if not quiet:
        print("built %d pages, %d weeks -> %s" % (written, len(weeks), OUT))
        sz = sum(os.path.getsize(os.path.join(r, f))
                 for r, _, fs in os.walk(OUT) for f in fs)
        print("output size: %.1f MB" % (sz / 1e6))
    return weeks


def snapshot():
    """Modification times of everything a build depends on: the vault's markdown
    and the generator itself, so editing a template rebuilds too."""
    seen = {}
    for root, dirs, files in os.walk(VAULT):
        rel = os.path.relpath(root, VAULT)
        rel = "" if rel == "." else rel
        if any(rel == s or rel.startswith(s + os.sep) for s in SKIP_PATHS):
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if f.endswith(".md"):
                p = os.path.join(root, f)
                try:
                    seen[p] = os.path.getmtime(p)
                except OSError:
                    pass
    for f in ("build.py", "markdown.py", "dashboard.py",
              os.path.join("assets", "app.css"), os.path.join("assets", "app.js")):
        p = os.path.join(HERE, f)
        try:
            seen[p] = os.path.getmtime(p)
        except OSError:
            pass
    return seen


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000


def arg_value(name, default, cast=str):
    """Read `--name VALUE` or `--name=VALUE` out of argv, else return default."""
    raw = None
    for i, a in enumerate(sys.argv):
        if a == name and i + 1 < len(sys.argv):
            raw = sys.argv[i + 1]
        elif a.startswith(name + "="):
            raw = a.split("=", 1)[1]
    if raw is None:
        return default
    try:
        return cast(raw)
    except ValueError:
        sys.exit("%s: not a valid value for %s" % (raw, name))


def make_server(port=DEFAULT_PORT, host=DEFAULT_HOST):
    """Bind a server for _site/ without serving yet. Port 0 means any free port."""
    import http.server
    import socketserver

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=OUT, **kw)

        def log_message(self, *a):
            pass  # keep the watch output readable

        def end_headers(self):
            # never let a browser cache a page the watcher may have just rebuilt
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

    socketserver.TCPServer.allow_reuse_address = True
    try:
        return socketserver.TCPServer((host, port), Handler)
    except OSError as e:
        sys.exit("cannot serve on %s:%d — %s\n"
                 "try --port 0 to let the OS pick a free port" % (host, port, e))


def server_url(httpd):
    host, port = httpd.server_address[:2]
    return "http://%s:%d" % (host, port)


def serve_background(port=DEFAULT_PORT, host=DEFAULT_HOST):
    import threading
    httpd = make_server(port, host)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def watch(serve=False, port=DEFAULT_PORT, host=DEFAULT_HOST):
    import time
    if serve:
        print("serving %s" % server_url(serve_background(port, host)), flush=True)
    print("watching for changes — ctrl-c to stop", flush=True)
    prev = snapshot()
    try:
        while True:
            time.sleep(1.0)
            cur = snapshot()
            if cur == prev:
                continue
            added = len(set(cur) - set(prev))
            removed = len(set(prev) - set(cur))
            changed = sum(1 for k in set(cur) & set(prev) if cur[k] != prev[k])
            bits = []
            if added:
                bits.append("%d added" % added)
            if removed:
                bits.append("%d removed" % removed)
            if changed:
                bits.append("%d changed" % changed)
            print("[%s] %s — rebuilding…" % (time.strftime("%H:%M:%S"), ", ".join(bits)), end=" ", flush=True)
            try:
                main(quiet=True)
                print("done", flush=True)
            except Exception as e:  # a syntax slip should not kill the watcher
                print("FAILED: %s: %s" % (type(e).__name__, e), flush=True)
            prev = cur
    except KeyboardInterrupt:
        print("\nstopped")


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------

def self_test():
    """Verify link resolution against the live vault.

    The resolver settles ambiguous targets by proximity, which is the kind of
    rule that keeps working while pointing somewhere subtly wrong. These check
    the shapes the vault actually writes, and that every rendered href lands on
    a file that exists.
    """
    ok = failed = 0

    def check(name, got, want):
        nonlocal ok, failed
        good = (want in got) if (want and got) else (got == want)
        print("  %s  %s%s" % ("PASS" if good else "FAIL", name,
                              "" if good else "\n          got %r, want %r" % (got, want)))
        ok, failed = ok + good, failed + (not good)

    nodes, pages = walk()
    table = build_link_resolver(pages)
    print("Resolver built from %d pages" % len(pages))

    HERE_M0 = "sophomore/fall/math-241/week-0/index.html"
    HERE_M1 = "sophomore/fall/math-241/week-1/index.html"

    # A bare stem that is unique in the vault.
    check("bare unique stem", resolve_target(table, "ACADEMIC CALENDAR", HERE_M0),
          "academic-registry/institution/academic-calendar.html")
    # The registry form every Year 2 course links: a two-segment path.
    check("registry path form", resolve_target(table, "Year2 - Sophomore/COURSE POLICIES", HERE_M0),
          "academic-registry/scheduling/year2-sophomore/course-policies.html")
    # A course path form, where the stem alone names seven different pages.
    check("course path form", resolve_target(table, "MATH241 Week1/resources/Reading Guide Week 1", HERE_M1),
          "sophomore/fall/math-241/week-1/resources/reading-guide-week-1.html")
    # A leading ordinal segment must not defeat the match.
    check("ordinal path segment", resolve_target(table, "5. Academic Registry/README", HERE_M0),
          "academic-registry/index.html")
    # An underscore-prefixed gradebook file.
    check("underscored stem", resolve_target(table, "_MATH 241 Quiz Record", HERE_M0),
          "academic-registry/gradebook/year2-sophomore/fall/math-241-quiz-record.html")

    # Proximity: the same ambiguous suffix must resolve per linking page.
    amb = "resources/Reading Guide Week 1"
    check("ambiguous suffix is genuinely ambiguous",
          str(len(table.get(amb.lower(), [])) > 1), "True")
    check("proximity picks own course (math-241)", resolve_target(table, amb, HERE_M1),
          "sophomore/fall/math-241/week-1/resources/reading-guide-week-1.html")
    check("proximity picks own course (prog-201)",
          resolve_target(table, amb, "sophomore/fall/prog-201/week-1/index.html"),
          "sophomore/fall/prog-201/week-1/resources/reading-guide-week-1.html")
    check("proximity picks own week for a bare stem",
          resolve_target(table, "summary",
                         "sophomore/fall/math-241/week-1/lectures/l04-matrix-multiplication-four-ways.html"),
          "sophomore/fall/math-241/week-1/summary.html")

    # Targets that must NOT resolve.
    check("unknown target stays unresolved", resolve_target(table, "no such page anywhere", HERE_M0), None)
    check("skipped tree stays unresolved", resolve_target(table, "4. Submissions/README", HERE_M0), None)

    # Every href the last build wrote must land on a real file.
    import re as _re
    href = _re.compile(r'class="wikilink" href="([^"]+)"')
    checked = dangling = 0
    if os.path.isdir(OUT):
        for root, _d, fs in os.walk(OUT):
            for f in fs:
                if not f.endswith(".html"):
                    continue
                page = os.path.join(root, f)
                for h in href.findall(open(page, encoding="utf-8").read()):
                    checked += 1
                    if not os.path.isfile(os.path.normpath(os.path.join(root, h))):
                        dangling += 1
        check("no dangling hrefs in %d links in %s/" % (checked, os.path.basename(OUT)),
              str(dangling), "0")
    else:
        print("  SKIP  href check (no %s/ -- run a build first)" % os.path.basename(OUT))

    print("\n%d/%d checks passing" % (ok, ok + failed))
    return 0 if not failed else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    # Parsed before the build so a bad --port fails now, not minutes from now.
    host = arg_value("--host", DEFAULT_HOST)
    port = arg_value("--port", DEFAULT_PORT, int)
    main()
    if "--watch" in sys.argv:
        watch(serve="--serve" in sys.argv, port=port, host=host)
    elif "--serve" in sys.argv:
        with make_server(port, host) as httpd:
            print("serving %s  (ctrl-c to stop)" % server_url(httpd), flush=True)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nstopped")
