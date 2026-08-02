"""
Home dashboard: what this vault actually contains, and where you are in it.

Two rules shaped this:

  * Report what is there, not what is planned. Only 7 of the 47 course folders
    hold any material, so "47 courses" as a headline would be a lie of omission.
    Build coverage is therefore the first analysis on the page.
  * Never invent a grade. The gradebooks define 237 assessment items but not one
    has a score, so this shows the inventory ahead of you and says plainly that
    nothing is recorded.

Charts are single-hue on purpose. Every bar here encodes one measure (magnitude)
across entities, so length carries the meaning and colour carries none. Teal,
green and amber never appear as series in the same chart -- teal↔green measures
ΔE 10.8 for normal vision, which is below the readable floor. Green and amber are
reserved status colours and always ship with a label, never colour alone.
"""

import html
import os
import re
import time
from collections import Counter

WPM = 230.0
MILESTONE = re.compile(r"midterm|final exam|finals|deadline|break|classes begin|"
                       r"classes end|orientation|reading day|commencement", re.I)
ROW = re.compile(r"^\|([^|]+)\|([^|]+)\|\s*$")
GB_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*(\d+)\s*\|\s*([^|]*?)\s*\|")


def _esc(s):
    return html.escape(str(s), quote=True)


# --------------------------------------------------------------------------
# collection
# --------------------------------------------------------------------------

def collect(nodes, pages, vault):
    by_route = {}
    courses = []
    for route, n in nodes.items():
        if n.get("kind") != "course":
            continue
        entry = {
            "route": route, "title": n["title"], "pages": 0, "weeks": set(),
            "words": 0, "math": 0, "sections": Counter(), "solutions": 0,
            "year": "", "sem": "",
        }
        crumbs = n.get("crumbs") or []
        if len(crumbs) >= 2:
            entry["year"], entry["sem"] = crumbs[0][0], crumbs[1][0]
        courses.append(entry)
        by_route[route] = entry

    prefixes = sorted(by_route, key=len, reverse=True)
    sections = Counter()
    newest = []
    total_words = 0

    for p in pages:
        if not p.src:
            continue
        total_words += p.words
        seg = p.route.split("/")
        sec = seg[-2] if len(seg) >= 2 else ""
        if sec in ("lectures", "assignments", "lab", "labs", "quiz",
                   "quizzes", "resources", "solutions_instructor"):
            sections[sec] += 1
        try:
            newest.append((os.path.getmtime(p.src), p.title, p.route,
                           " › ".join(t for t, _ in p.crumbs[:-1])))
        except OSError:
            pass
        for pre in prefixes:
            if p.route.startswith(pre + "/"):
                c = by_route[pre]
                c["pages"] += 1
                c["words"] += p.words
                c["math"] += p.math
                if p.week_route:
                    c["weeks"].add(p.week_route)
                if sec:
                    c["sections"][sec] += 1
                if p.is_solution:
                    c["solutions"] += 1
                break

    newest.sort(reverse=True)
    built = [c for c in courses if c["pages"]]
    built.sort(key=lambda c: -c["pages"])

    # build coverage, grouped by year then semester
    coverage = {}
    for c in courses:
        key = (c["year"], c["sem"])
        d = coverage.setdefault(key, {"total": 0, "built": 0, "weeks": 0, "pages": 0})
        d["total"] += 1
        if c["pages"]:
            d["built"] += 1
            d["weeks"] += len(c["weeks"])
            d["pages"] += c["pages"]

    # Degree order comes from the tree (folders are numbered), not from sorting
    # titles, which would run Freshman, Junior, Masters, Senior, Sophomore.
    order, k = {}, 0
    for yr in nodes.get("", {}).get("children", []):
        ynode = nodes[yr]
        for sm in ynode["children"]:
            order[(ynode["title"], nodes[sm]["title"])] = k
            k += 1

    return {
        "courses": courses,
        "built": built,
        "coverage": coverage,
        "order": order,
        "sections": sections,
        "newest": newest[:8],
        "pages": sum(1 for p in pages if p.src),
        "words": total_words,
        "weeks": len({p.week_route for p in pages if p.week_route}),
        "gradebook": read_gradebooks(vault),
        "dates": read_calendar(vault),
    }


def read_gradebooks(vault):
    """Assessment inventory. Counts items and points; records nothing it cannot read."""
    root = os.path.join(vault, "5. Academic Registry", "2. Gradebook")
    out = {"items": 0, "points": 0, "scored": 0, "courses": []}
    if not os.path.isdir(root):
        return out
    for dirpath, _, files in os.walk(root):
        for fn in sorted(files):
            if not fn.endswith(".md") or fn.startswith("_"):
                continue
            path = os.path.join(dirpath, fn)
            try:
                text = open(path, encoding="utf-8").read()
            except OSError:
                continue
            meta = {}
            m = re.match(r"^---\n(.*?)\n---", text, re.S)
            if m:
                for line in m.group(1).split("\n"):
                    if ":" in line:
                        k, v = line.split(":", 1)
                        meta[k.strip()] = v.strip().strip('"')
            items = pts = scored = 0
            for line in text.split("\n"):
                g = GB_ROW.match(line)
                if not g:
                    continue
                if g.group(1).strip().lower() in ("item", "component") or set(g.group(1).strip()) <= set("-: "):
                    continue
                items += 1
                pts += int(g.group(3))
                if g.group(4).strip():
                    scored += 1
            if not items:
                continue
            out["items"] += items
            out["points"] += pts
            out["scored"] += scored
            out["courses"].append({
                "code": meta.get("course", fn[:-3]),
                "title": meta.get("title", ""),
                "credits": meta.get("credits", ""),
                "sem": meta.get("semester", ""),
                "items": items, "points": pts, "scored": scored,
            })
    out["courses"].sort(key=lambda c: -c["points"])
    return out


def read_calendar(vault):
    """Milestones per semester heading. No year is stated in the source, so none
    is invented here and nothing is presented as 'upcoming'."""
    path = os.path.join(vault, "5. Academic Registry", "0. Institution", "ACADEMIC CALENDAR.md")
    groups = []
    if not os.path.isfile(path):
        return groups
    cur = None
    try:
        lines = open(path, encoding="utf-8").read().split("\n")
    except OSError:
        return groups
    for line in lines:
        h = re.match(r"^###\s+(.*?)\s*$", line)
        if h:
            cur = {"title": h.group(1), "rows": []}
            groups.append(cur)
            continue
        if cur is None:
            continue
        m = ROW.match(line)
        if not m:
            continue
        date, event = m.group(1).strip(), m.group(2).strip()
        if date.lower() == "date" or set(date) <= set("-: "):
            continue
        if MILESTONE.search(event):
            cur["rows"].append((date, event))
    return [g for g in groups if g["rows"]][:2]


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def _hours(words):
    return words / WPM / 60.0


def tile(value, label, sub=""):
    return ('<div class="tile"><div class="tv">%s</div><div class="tl">%s</div>'
            '%s</div>' % (_esc(value), _esc(label),
                          '<div class="ts">%s</div>' % _esc(sub) if sub else ""))


def bars(rows, unit=""):
    """rows: (label, value, sub). One measure, one hue -- length is the encoding."""
    if not rows:
        return ""
    top = max(r[1] for r in rows) or 1
    out = []
    for label, value, sub in rows:
        pct = max(1.5, 100.0 * value / top)
        out.append(
            '<div class="brow" title="%s: %s%s">'
            '<div class="blab">%s</div>'
            '<div class="btrack"><div class="bfill" style="width:%.1f%%"></div></div>'
            '<div class="bval">%s<span>%s</span></div>'
            '</div>' % (_esc(label), _esc("{:,}".format(value)), _esc(unit),
                        _esc(label), pct, _esc("{:,}".format(value)),
                        _esc(sub or ""))
        )
    return '<div class="bars">%s</div>' % "".join(out)


def card(title, body, note="", wide=False):
    return ('<section class="panel%s"><h2>%s</h2>%s%s</section>'
            % (" wide" if wide else "", _esc(title),
               '<p class="pnote">%s</p>' % note if note else "", body))


def ago(ts):
    d = (time.time() - ts) / 86400.0
    if d < 1:
        return "today"
    if d < 2:
        return "yesterday"
    if d < 14:
        return "%d days ago" % int(d)
    if d < 60:
        return "%d weeks ago" % int(d / 7)
    return time.strftime("%b %Y", time.localtime(ts))


def render(s, pre=""):
    built_n = len(s["built"])
    total_n = len(s["courses"])
    hours = _hours(s["words"])
    gb = s["gradebook"]

    out = ['<h1>CSE Degree</h1>']
    out.append('<p class="lede">%d pages of course material across %d weeks. '
               'Everything below is measured from the vault itself.</p>'
               % (s["pages"], s["weeks"]))

    # ---- headline tiles ----
    out.append('<div class="tiles">')
    out.append(tile("{:,}".format(s["pages"]), "Pages"))
    out.append(tile("%d of %d" % (built_n, total_n), "Courses built",
                    "%d still empty" % (total_n - built_n)))
    out.append(tile(s["weeks"], "Weeks of material"))
    out.append(tile("%.0f h" % hours, "Reading time", "at %d wpm" % WPM))
    out.append(tile("{:,}".format(gb["items"]), "Assessed items",
                    "%d scored" % gb["scored"]))
    out.append('</div>')

    # ---- progress + continue (client-side) ----
    out.append('<div class="grid2">')
    out.append(card("Your progress",
                    '<div id="dashProgress" class="dash-progress">'
                    '<p class="empty">Loading&hellip;</p></div>',
                    "Stored in this browser only."))
    out.append(card("Continue reading",
                    '<div id="dashRecent"><p class="empty">Pages you open will '
                    'appear here.</p></div>'))
    out.append('</div>')

    # ---- build coverage: the honest headline ----
    rows = []
    order = s.get("order", {})
    for (year, sem), d in sorted(s["coverage"].items(),
                                 key=lambda kv: order.get(kv[0], 10 ** 6)):
        if not year:
            continue
        label = "%s · %s" % (year, sem) if sem else year
        rows.append((label, d["built"], "of %d" % d["total"]))
    body = bars(rows)
    empty = total_n - built_n
    out.append(card(
        "Build coverage",
        body,
        "Course folders exist for the whole degree, but only %d hold material. "
        "The remaining %d are scaffolding — counting them as coursework would "
        "overstate what is here." % (built_n, empty),
        wide=True))

    # ---- where the material is ----
    rows = [(c["title"], c["pages"],
             "%d wk · %.0f h" % (len(c["weeks"]), _hours(c["words"])))
            for c in s["built"]]
    out.append(card("Where the material is", bars(rows, " pages"),
                    "Pages per course, with weeks covered and reading time.",
                    wide=True))

    # ---- content mix ----
    labels = {"lectures": "Lectures", "lab": "Lab", "labs": "Labs",
              "assignments": "Assignments", "quiz": "Quizzes",
              "quizzes": "Quizzes", "resources": "Resources",
              "solutions_instructor": "Solutions"}
    mix = Counter()
    for k, v in s["sections"].items():
        mix[labels.get(k, k)] += v
    rows = [(k, v, "") for k, v in mix.most_common()]

    # ---- assessment inventory ----
    if gb["courses"]:
        grows = [(c["code"], c["points"], "%d items" % c["items"]) for c in gb["courses"]]
        gnote = ("%s points defined across %d items. <strong>None recorded yet</strong> — "
                 "enter scores in the gradebook and run <code>tools/gpa.py</code>."
                 % ("{:,}".format(gb["points"]), gb["items"]))
        gbody = bars(grows, " pts")
    else:
        gnote, gbody = "No gradebooks found.", ""

    out.append('<div class="grid2">')
    out.append(card("Content mix", bars(rows, " pages")))
    out.append(card("Assessment inventory", gbody, gnote))
    out.append('</div>')

    # ---- recent + dates ----
    items = []
    for ts, title, route, crumb in s["newest"]:
        items.append('<li><a href="%s%s">%s</a><span>%s · %s</span></li>'
                     % (pre, _esc(route), _esc(title), _esc(crumb), _esc(ago(ts))))
    recent = '<ul class="feed">%s</ul>' % "".join(items) if items else ""

    dl = []
    for g in s["dates"]:
        dl.append('<h3>%s</h3><ul class="feed dates">' % _esc(g["title"]))
        for date, event in g["rows"][:7]:
            dl.append('<li><b>%s</b><span>%s</span></li>' % (_esc(date), _esc(event)))
        dl.append("</ul>")
    dates = "".join(dl)

    out.append('<div class="grid2">')
    out.append(card("Recently updated", recent, "Newest files in the vault."))
    out.append(card("Key dates", dates,
                    "From the academic calendar. No calendar year is given in the "
                    "source, so these are listed as reference rather than countdowns."))
    out.append('</div>')

    return "".join(out)
