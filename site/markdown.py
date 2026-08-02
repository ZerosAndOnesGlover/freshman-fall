"""
Self-contained Markdown -> HTML renderer for the CSE degree vault.

Deliberately dependency-free. The vault's content has three properties that
break naive renderers, and the extraction order below exists to handle them:

  1. LaTeX is everywhere (421 files). `$f(x)_1$` would have its underscores
     eaten by emphasis parsing, and `$|x - a| < \\delta$` inside a table would
     be split into cells at the pipes.
  2. Tables carry `<br>` (the timetable grids) and emoji.
  3. Code fences contain `$`, `|`, `*` and `_` that must stay literal.

So we extract in this order -- fences, inline code, display math, inline math --
replacing each with a placeholder that contains no Markdown-significant
characters. Block and inline parsing then runs over text that is safe to touch,
and the originals are restored at the end.

Math is restored with its `$` delimiters intact; KaTeX's auto-render finds it in
the browser, configured to skip <pre> and <code>.
"""

import html
import re

# Placeholder uses control characters that cannot occur in the source files.
PH = "\x00%s:%d\x00"
PH_RE = re.compile(r"\x00(FENCE|CODE|DMATH|IMATH):(\d+)\x00")


class Extractor:
    """Pulls spans out of the text and hands back placeholders."""

    def __init__(self):
        self.store = {"FENCE": [], "CODE": [], "DMATH": [], "IMATH": []}

    def stash(self, kind, value):
        bucket = self.store[kind]
        bucket.append(value)
        return PH % (kind, len(bucket) - 1)

    def get(self, kind, idx):
        return self.store[kind][idx]


FENCE_RE = re.compile(r"^([ \t]*)(```|~~~)([^\n]*)\n(.*?)(?:^[ \t]*\2[ \t]*$|\Z)", re.M | re.S)
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.S)
DISPLAY_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.S)
# Inline math: no newline, must not start or end on whitespace (avoids matching
# prose that merely contains two dollar signs, e.g. a price range).
INLINE_MATH_RE = re.compile(r"\$(?!\s)((?:[^$\n\\]|\\.)+?)(?<!\s)\$")


def extract(text, ex):
    def fence(m):
        indent, _, info, body = m.groups()
        return indent + ex.stash("FENCE", (info.strip(), body))

    text = FENCE_RE.sub(fence, text)
    text = INLINE_CODE_RE.sub(lambda m: ex.stash("CODE", m.group(2)), text)
    text = DISPLAY_MATH_RE.sub(lambda m: ex.stash("DMATH", m.group(1)), text)
    text = INLINE_MATH_RE.sub(lambda m: ex.stash("IMATH", m.group(1)), text)
    return text


def restore(text, ex):
    def sub(m):
        kind, idx = m.group(1), int(m.group(2))
        val = ex.get(kind, idx)
        if kind == "FENCE":
            info, body = val
            lang = re.sub(r"[^A-Za-z0-9+#-]", "", info.split()[0]) if info else ""
            cls = ' class="language-%s"' % lang if lang else ""
            return "<pre><code%s>%s</code></pre>" % (cls, html.escape(body.rstrip("\n")))
        if kind == "CODE":
            return "<code>%s</code>" % html.escape(val)
        # `\|` inside math is always a table-cell escape in this vault (all 9
        # occurrences are `\ln\|x\|`-style absolute values inside table rows).
        # Left alone, KaTeX would render it as the double bar U+2016.
        val = val.replace(r"\|", "|")
        if kind == "DMATH":
            return '<span class="math-display">$$%s$$</span>' % html.escape(val)
        return '<span class="math-inline">$%s$</span>' % html.escape(val)

    # Placeholders can be nested inside restored content, so loop to a fixpoint.
    for _ in range(6):
        new = PH_RE.sub(sub, text)
        if new == text:
            break
        text = new
    return text


# --------------------------------------------------------------------------
# Inline
# --------------------------------------------------------------------------

WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
# The mirror of the case below: `*italic ... **bold.***` opens an italic, nests a
# bold inside it, and closes both on the same run of three. Handled before the
# bold rule so the shared closer is split correctly.
NEST_EMPH_RE = re.compile(r"(?<!\*)\*(?!\*)(?=\S)([^*]+?)\*\*(?=\S)([^*]+?)(?<=\S)\*\*\*", re.S)
# The trailing (?!\*) matters: in `**Author, *Title***` the run of three
# asterisks closes an italic and a bold at once. Without it the lazy match
# would close the bold on the first two, stranding the italic across the tag.
BOLD_RE = re.compile(r"\*\*(?=\S)(.+?)(?<=\S)\*\*(?!\*)", re.S)
ITAL_RE = re.compile(r"(?<![\w*])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![\w*])", re.S)
ITAL_U_RE = re.compile(r"(?<![\w_])_(?=[^\s_])(.+?)(?<=[^\s_])_(?![\w_])", re.S)
STRIKE_RE = re.compile(r"~~(?=\S)(.+?)(?<=\S)~~", re.S)
# A link target must look like one: a scheme, an anchor, a path, or a filename
# with an extension. Bare numbers are arithmetic, not destinations.
LINKISH_RE = re.compile(
    r"^(?:[a-z][a-z0-9+.-]*:|#|/|\.{1,2}/)|[/\\]|\.(?:md|html?|png|jpe?g|gif|svg|pdf|csv|txt|py|c|h)$",
    re.I,
)

# Raw HTML we allow through untouched; everything else is escaped.
ALLOWED_HTML = re.compile(
    r"</?(?:br|b|i|em|strong|sub|sup|kbd|mark|small|details|summary|span|div|hr)\b[^>]*/?>",
    re.I,
)


def inline(text, resolve_link=None):
    """Render inline constructs. `text` still holds placeholders."""
    # Protect permitted raw HTML from escaping.
    tags = []

    def keep(m):
        tags.append(m.group(0))
        return "\x01%d\x01" % (len(tags) - 1)

    text = ALLOWED_HTML.sub(keep, text)
    text = html.escape(text, quote=False)

    def wiki(m):
        target, alias = m.group(1).strip(), (m.group(2) or "").strip()
        label = alias or target
        href = resolve_link(target) if resolve_link else None
        if href:
            return '<a class="wikilink" href="%s">%s</a>' % (html.escape(href, True), label)
        return '<span class="wikilink broken" title="no page named &quot;%s&quot;">%s</span>' % (
            html.escape(target, True),
            label,
        )

    text = WIKILINK_RE.sub(wiki, text)
    text = IMAGE_RE.sub(
        lambda m: '<img src="%s" alt="%s">' % (html.escape(m.group(2), True), html.escape(m.group(1), True)),
        text,
    )
    def link(m):
        target = m.group(2)
        # `[a/b](6.0)` occurs in the physics sheets as bracketed arithmetic, not
        # a link. Only treat the target as a URL if it actually looks like one.
        if not LINKISH_RE.match(target):
            return m.group(0)
        return '<a href="%s">%s</a>' % (html.escape(target, True), m.group(1))

    text = LINK_RE.sub(link, text)
    text = NEST_EMPH_RE.sub(r"<em>\1<strong>\2</strong></em>", text)
    text = BOLD_RE.sub(r"<strong>\1</strong>", text)
    text = STRIKE_RE.sub(r"<del>\1</del>", text)
    text = ITAL_RE.sub(r"<em>\1</em>", text)
    text = ITAL_U_RE.sub(r"<em>\1</em>", text)

    text = re.sub(r"\x01(\d+)\x01", lambda m: tags[int(m.group(1))], text)
    return text


# --------------------------------------------------------------------------
# Block
# --------------------------------------------------------------------------

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
BANNER_RE = re.compile(r"^\s*[═=]{5,}\s*$")
ULI_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
OLI_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
TABLE_DELIM_RE = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)+\|?\s*$")
FENCE_ONLY_RE = re.compile(r"(?:\x00FENCE:\d+\x00\s*)+")


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    cells, buf, i = [], "", 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            buf += "|"
            i += 2
            continue
        if c == "|":
            cells.append(buf.strip())
            buf = ""
            i += 1
            continue
        buf += c
        i += 1
    cells.append(buf.strip())
    return cells


def alignments(delim):
    out = []
    for cell in split_row(delim):
        left, right = cell.startswith(":"), cell.endswith(":")
        out.append("center" if left and right else "right" if right else "left" if left else None)
    return out


class Renderer:
    def __init__(self, resolve_link=None):
        self.resolve_link = resolve_link
        self.headings = []

    def render(self, text):
        ex = Extractor()
        text = extract(text.replace("\r\n", "\n").replace("\r", "\n"), ex)
        html_out = self.blocks(text.split("\n"))
        return restore(html_out, ex)

    def inl(self, s):
        return inline(s, self.resolve_link)

    def blocks(self, lines):
        out, i, n = [], 0, len(lines)
        while i < n:
            line = lines[i]

            if not line.strip():
                i += 1
                continue

            # A fence is its own block even when no blank line precedes it;
            # otherwise it would be swallowed into the paragraph above and we
            # would emit <p><pre>, which is invalid.
            if FENCE_ONLY_RE.fullmatch(line.strip()):
                out.append(line.strip())
                i += 1
                continue

            if BANNER_RE.match(line):
                out.append('<hr class="banner">')
                i += 1
                continue

            if HR_RE.match(line):
                out.append("<hr>")
                i += 1
                continue

            m = HEADING_RE.match(line)
            if m:
                level = len(m.group(1))
                body = self.inl(m.group(2))
                anchor = self.slug_heading(m.group(2))
                self.headings.append((level, m.group(2), anchor))
                out.append('<h%d id="%s">%s</h%d>' % (level, anchor, body, level))
                i += 1
                continue

            # table: a pipe row followed by a delimiter row
            if line.lstrip().startswith("|") and i + 1 < n and TABLE_DELIM_RE.match(lines[i + 1]):
                header = split_row(line)
                aligns = alignments(lines[i + 1])
                i += 2
                rows = []
                while i < n and lines[i].lstrip().startswith("|"):
                    rows.append(split_row(lines[i]))
                    i += 1
                out.append(self.table(header, aligns, rows))
                continue

            if QUOTE_RE.match(line):
                buf = []
                while i < n and (QUOTE_RE.match(lines[i]) or (lines[i].strip() and buf)):
                    m2 = QUOTE_RE.match(lines[i])
                    if not m2:
                        break
                    buf.append(m2.group(1))
                    i += 1
                out.append("<blockquote>%s</blockquote>" % self.blocks(buf))
                continue

            if ULI_RE.match(line) or OLI_RE.match(line):
                block, i = self.list_block(lines, i)
                out.append(block)
                continue

            # paragraph
            buf = []
            while i < n and lines[i].strip() and not (
                HEADING_RE.match(lines[i])
                or FENCE_ONLY_RE.fullmatch(lines[i].strip())
                or HR_RE.match(lines[i])
                or BANNER_RE.match(lines[i])
                or QUOTE_RE.match(lines[i])
                or ULI_RE.match(lines[i])
                or OLI_RE.match(lines[i])
                or (lines[i].lstrip().startswith("|") and i + 1 < n and TABLE_DELIM_RE.match(lines[i + 1]))
            ):
                buf.append(lines[i])
                i += 1
            if buf:
                text = "\n".join(buf)
                # A block that is only fence placeholders is a code block, not a
                # paragraph -- wrapping <pre> in <p> would be invalid HTML.
                if re.fullmatch(r"\s*(?:\x00FENCE:\d+\x00\s*)+", text):
                    out.append(text.strip())
                    continue
                # two trailing spaces = hard break, which the vault uses
                text = re.sub(r"  \n", "<br>\n", text)
                out.append("<p>%s</p>" % self.inl(text))
        return "\n".join(out)

    def list_block(self, lines, i):
        n = len(lines)
        ordered = bool(OLI_RE.match(lines[i]))
        base = len(re.match(r"^(\s*)", lines[i]).group(1))
        items, cur = [], None
        while i < n:
            line = lines[i]
            if not line.strip():
                # a blank line ends the list unless the next line continues it
                if i + 1 < n and (ULI_RE.match(lines[i + 1]) or OLI_RE.match(lines[i + 1])):
                    nxt = len(re.match(r"^(\s*)", lines[i + 1]).group(1))
                    if nxt >= base:
                        i += 1
                        continue
                break
            m = OLI_RE.match(line) if ordered else ULI_RE.match(line)
            other = ULI_RE.match(line) if ordered else OLI_RE.match(line)
            indent = len(re.match(r"^(\s*)", line).group(1))
            if (m or other) and indent < base:
                break
            if m and indent == base:
                if cur is not None:
                    items.append(cur)
                cur = [m.group(3) if ordered else m.group(2)]
                i += 1
                continue
            if cur is None:
                break
            # continuation or nested content
            cur.append(line[base:] if len(line) > base else line.strip())
            i += 1
        if cur is not None:
            items.append(cur)
        tag = "ol" if ordered else "ul"
        rendered = []
        for item in items:
            if len(item) == 1:
                rendered.append("<li>%s</li>" % self.inl(item[0]))
            else:
                rendered.append("<li>%s</li>" % self.blocks(item))
        return "<%s>%s</%s>" % (tag, "".join(rendered), tag), i

    def table(self, header, aligns, rows):
        def cell(tag, text, idx):
            a = aligns[idx] if idx < len(aligns) else None
            style = ' style="text-align:%s"' % a if a else ""
            return "<%s%s>%s</%s>" % (tag, style, self.inl(text), tag)

        head = "".join(cell("th", c, j) for j, c in enumerate(header))
        body = []
        for r in rows:
            # pad or trim so ragged rows do not break the grid
            r = (r + [""] * len(header))[: max(len(header), len(r))]
            body.append("<tr>%s</tr>" % "".join(cell("td", c, j) for j, c in enumerate(r)))
        return (
            '<div class="table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % (head, "".join(body))
        )

    @staticmethod
    def slug_heading(text):
        text = re.sub(r"[`*_$\\]", "", text)
        text = re.sub(r"[^\w\s-]", "", text, flags=re.U).strip().lower()
        return re.sub(r"[\s]+", "-", text) or "section"


def render(text, resolve_link=None):
    r = Renderer(resolve_link)
    return r.render(text), r.headings
