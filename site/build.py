#!/usr/bin/env python3
"""
Static site generator for the CSE degree vault.

    python3 site/build.py            # build into _site/
    python3 site/build.py --serve    # build, then serve on localhost:8000

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
    "quiz": "Quiz",
    "quizzes": "Quizzes",
    "resources": "Resources",
    "solutions_instructor": "Solutions",
}
SECTION_ORDER = ["lectures", "lab", "labs", "assignments", "quiz", "quizzes",
                 "resources", "solutions_instructor"]

SOLUTION_MARKERS = re.compile(r"NOT FOR STUDENTS|INSTRUCTOR ONLY", re.I)
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
            is_sol = "solutions_instructor" in root.split(os.sep)
            if not is_sol:
                try:
                    head = open(src, encoding="utf-8").read(4000)
                    is_sol = bool(SOLUTION_MARKERS.search(head))
                except OSError:
                    pass
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


def build_link_resolver(pages):
    """Map wikilink targets (by file stem, case-insensitive) to routes."""
    table = {}
    for p in pages:
        stem = os.path.basename(p.src)[:-3]
        table.setdefault(stem.lower(), p.route)
        table.setdefault(slug(stem), p.route)
    return table


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
<link rel="stylesheet" href="{pre}vendor/katex/katex.min.css">
<link rel="stylesheet" href="{pre}assets/app.css">
</head>
<body data-route="{route}" data-week="{week}" data-prefix="{pre}">
<button id="navToggle" aria-label="Toggle navigation">&#9776;</button>
<aside id="sidebar">
  <a class="brand" href="{pre}index.html">CSE Degree</a>
  <div class="search"><input id="q" type="search" placeholder="Search&hellip;" autocomplete="off"><div id="results"></div></div>
  <div id="progress" class="progress"></div>
  <nav id="nav"></nav>
</aside>
<main>
  <nav class="crumbs">{crumbs}</nav>
  <article id="content">{body}</article>
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
        '<button class="reveal" type="button">Reveal solutions%s</button>'
        '<p class="gate-note">Hidden so you can attempt the problems first.</p>'
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


def main():
    nodes, pages = walk()
    link_table = build_link_resolver(pages)

    # ---- render every markdown file -------------------------------------
    for p in pages:
        pre = rel_prefix(p.route)

        def resolve(target, _pre=pre):
            route = link_table.get(target.lower()) or link_table.get(slug(target))
            return (_pre + route) if route else None

        try:
            raw = open(p.src, encoding="utf-8").read()
        except OSError as e:
            print("  skip %s (%s)" % (p.src, e))
            continue
        body, headings = md.render(raw, resolve_link=resolve)
        p.html, p.headings = body, headings
        p.text = strip_html(body)[:1500]

    # ---- write pages -----------------------------------------------------
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

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
        out_path = os.path.join(OUT, p.route)
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

    # ---- home page -------------------------------------------------------
    weeks = sorted({p.week_route for p in pages if p.week_route})
    top = [nodes[c] for c in nodes[""]["children"]]
    cards = []
    for node in sorted(top, key=lambda n: natural_key(n["route"])):
        courses = [nodes[c] for c in node["children"]]
        sub = []
        for sem in sorted(courses, key=lambda n: natural_key(n["title"])):
            names = [nodes[c]["title"] for c in sem["children"]]
            sub.append("<li><a href=\"%s/index.html\">%s</a> <span class=\"muted\">%d</span></li>"
                       % (sem["route"], html.escape(sem["title"]), len(names)))
        cards.append('<section class="card"><h2><a href="%s/index.html">%s</a></h2><ul>%s</ul></section>'
                     % (node["route"], html.escape(node["title"]), "".join(sub)))
    home = ('<h1>CSE Degree</h1>'
            '<p class="lede">%d pages across %d weeks. Progress is stored in this browser.</p>'
            '<div class="cards">%s</div>' % (written, len(weeks), "".join(cards)))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(SHELL.format(title="CSE Degree", pre="", route="index.html", week="",
                              crumbs='<span>Home</span>', body=home))
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

    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "assets", "nav.json"), "w", encoding="utf-8") as fh:
        json.dump(nav, fh, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(OUT, "assets", "search.json"), "w", encoding="utf-8") as fh:
        json.dump({"weeks": weeks, "docs": search}, fh, ensure_ascii=False, separators=(",", ":"))

    for asset in ("app.css", "app.js"):
        shutil.copy(os.path.join(HERE, "assets", asset), os.path.join(OUT, "assets", asset))
    shutil.copytree(os.path.join(HERE, "vendor"), os.path.join(OUT, "vendor"))

    print("built %d pages, %d weeks -> %s" % (written, len(weeks), OUT))
    sz = sum(os.path.getsize(os.path.join(r, f))
             for r, _, fs in os.walk(OUT) for f in fs)
    print("output size: %.1f MB" % (sz / 1e6))
    return weeks


if __name__ == "__main__":
    main()
    if "--serve" in sys.argv:
        import http.server
        import socketserver
        os.chdir(OUT)
        with socketserver.TCPServer(("127.0.0.1", 8000),
                                    http.server.SimpleHTTPRequestHandler) as httpd:
            print("serving http://127.0.0.1:8000  (ctrl-c to stop)")
            httpd.serve_forever()
