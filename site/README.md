# Study Site Generator

Turns the vault's markdown into a browsable study website.

```sh
python3 site/build.py                    # build once into _site/
python3 site/build.py --serve            # build, then serve on :8000
python3 site/build.py --watch --serve    # serve and rebuild on every change
python3 site/build.py --self-test        # 12 checks on wikilink resolution
```

No third-party packages. Python 3.9+ only. Takes about three seconds for the
whole vault.

`_site/` is gitignored — it is regenerated from source, so there is nothing in
it worth versioning.

## Does it pick up new content by itself?

**The site is generated, not live.** Every figure on the dashboard is measured
from the vault at build time — none are hardcoded — but they are written into
HTML when the build runs. Add a lecture and the page count, the course bars, the
navigation tree and the search index all change, *after a rebuild*.

Two ways to get one:

- `--watch` polls every second and rebuilds when any `.md` changes, or when the
  generator's own files do. Adding, editing and deleting are all picked up.
  Leave `python3 site/build.py --watch --serve` running while you write and just
  refresh the browser.
- Run `python3 site/build.py` yourself whenever you want.

A rebuild goes into `_site.building` and is swapped in at the end, so a reader
never sees a half-built site — without that, `_site` is deleted at the start of
each build and every page 404s for the three seconds it takes.

The only things that update *without* a rebuild are the ones the browser owns:
week completion and the "continue reading" list, both in `localStorage`.

## Why serve it rather than open the file

Navigation and search load `nav.json` and `search.json` with `fetch()`, which
browsers block on `file://`. Pages, maths and styling still render if you open
the HTML directly; the sidebar tree and the search box will not. Use `--serve`.

## Layout

| Path | What it is |
|------|------------|
| `build.py` | Walks the vault, renders each file, writes `_site/` |
| `markdown.py` | Dependency-free Markdown → HTML renderer |
| `assets/app.css` | Design system, light and dark |
| `assets/app.js` | Nav tree, search, TOC, progress, solution gating |
| `vendor/katex/` | KaTeX, trimmed to woff2 fonts, so maths works offline |
| `vendor/fonts/` | Source Serif 4 + Inter, variable woff2, latin subset (208K) |

## What the site does

**Navigation** mirrors the vault: Year → Semester → Course → Week → section.
Course folders are recognised by their code, so
`2. MATH 141 - Calculus I: …` becomes `math-141`, and `MATH141 Week0` becomes
`week-0`.

**Search** is client-side over titles, breadcrumbs, headings and the first 1500
characters of each page. Press `/` to focus it.

**Progress** is per-week. "Mark week complete" is stored in `localStorage`
under `cse.progress.v1`, so it stays in your browser and never leaves the
machine. Completed weeks get a tick in the sidebar and feed the counter at the
top.

**Solutions are hidden by default.** Anything under `solutions_instructor/`, or
containing "NOT FOR STUDENTS" / "INSTRUCTOR ONLY", renders behind a reveal
button so you can attempt the problems first.

## Design

The site is a reading environment before it is an app, so the type does the
work:

- **Source Serif 4** for prose, at 68 characters and 1.72 line height. It was
  drawn for screen reading and sits comfortably beside KaTeX's Computer Modern.
- **Inter** for chrome only — sidebar, breadcrumbs, tables, buttons. Keeping the
  interface in a different voice from the material stops the two competing.
- Both are variable woff2, latin subset, 208K for all four faces, vendored so
  the site stays fully offline.

Colour is deliberately narrow: warm paper rather than flat white, near-black
ink, one teal accent, and amber reserved exclusively for solutions so hidden
material is recognisable at a glance. Dark mode is a genuine repaint, not an
inversion.

Other details worth knowing:

- **Tables use lining tabular figures**, so the timetable columns align.
  Headers stick while you scroll a wide grid.
- **Prose uses old-style figures**, which sit better in running text.
- A **table of contents rail** appears on pages with three or more headings and
  highlights the section you are in. On gated pages it waits for the reveal, so
  it never lists sections you cannot scroll to.
- Print styles drop the navigation and **expand hidden solutions**, so a page
  prints as a clean document.
- Respects `prefers-reduced-motion` and `prefers-color-scheme`.

## Renderer notes

The vault's content breaks naive Markdown renderers in three specific ways, and
`markdown.py` is built around them:

1. **Maths is everywhere** (421 files). `$f(x)_1$` would have its underscores
   read as emphasis, and `$|x-a| < \delta$` in a table would be split at the
   pipes. So fenced code, inline code, display maths and inline maths are all
   extracted to placeholders *before* any block or inline parsing, then restored
   at the end. Maths keeps its `$` delimiters and KaTeX renders it in the
   browser, configured to skip `<pre>` and `<code>`.

2. **`\|` inside maths** is always a table-cell escape here — all nine
   occurrences are absolute values like `$\ln\|x\|+C$`. Left alone, KaTeX would
   render `‖`. They are unescaped on restore.

3. **Bracketed arithmetic looks like a link.** The physics sheets contain
   `[(1.5−4.5)/(1.5+4.5)](6.0)`, which is `[text](url)` to a Markdown parser. A
   target is only treated as a link if it looks like one — a scheme, anchor,
   path, or a filename with an extension. Bare numbers stay as text.

4. **A filename does not identify a page.** 166 stems are shared by two or more
   pages — every `summary`, all 138 `README`s, every per-week reading guide and
   solutions sheet — so `[[Reading Guide Week 1]]` names seven files. The vault
   disambiguates the way Obsidian does, by writing a path:
   `[[MATH241 Week1/resources/Reading Guide Week 1|Reading Guide Week 1]]`.

   So a page is indexed under **every suffix of its own path**, and a target
   resolves as soon as it is specific enough to pick one page out. Where it
   still names several, the one nearest the linking page wins — a bare
   `[[summary]]` in CS 201 Week 3 means that week's. Genuine ties fall back to
   walk order.

   *(Matching stems alone left 435 of the vault's 1,059 rendered wikilinks
   broken — 41% — including every course's link to
   `Year2 - Sophomore/COURSE POLICIES`.)*

Emphasis also handles both joint-closing forms: `**Author, *Title***` and
`*italic … **bold.***`.

## Verifying a build

The build is checked three ways, all of which currently pass clean:

- `--self-test` covers wikilink resolution: each link form the vault writes,
  the proximity tie-break, targets that must *not* resolve, and that all 1,054
  rendered `wikilink` hrefs land on a file that exists
- every internal `href`/`src` resolves against the filesystem (18,297 links)
- every page parses with balanced, correctly nested tags (1,425 pages)
- no extraction placeholders survive into the output
