/**
 * Renders vault markdown.
 *
 * The vault's lecture notes use GitHub-flavoured markdown plus $…$ / $$…$$
 * mathematics and fenced code. marked handles the markdown, KaTeX the maths,
 * highlight.js the code. Math is extracted BEFORE marked runs, because marked
 * would otherwise mangle backslashes and underscores inside a formula.
 */
import { useMemo, useEffect, useRef } from 'react';
import { marked } from 'marked';
import katex from 'katex';
import hljs from 'highlight.js/lib/common';

const renderer = new marked.Renderer();

// Headings get ids so the table of contents can link to them.
renderer.heading = function heading({ tokens, depth }) {
  const text = this.parser.parseInline(tokens);
  const id = slug(stripTags(text));
  return `<h${depth} id="${id}">${text}</h${depth}>\n`;
};

renderer.code = function code({ text, lang }) {
  const language = (lang || '').split(/\s+/)[0];
  let out;
  try {
    out = language && hljs.getLanguage(language)
      ? hljs.highlight(text, { language }).value
      : hljs.highlightAuto(text).value;
  } catch {
    out = escapeHtml(text);
  }
  return `<pre><code class="hljs language-${escapeHtml(language || 'plaintext')}">${out}</code></pre>\n`;
};

// Wide tables scroll inside their own box rather than the page.
renderer.table = function table(token) {
  const header = token.header.map((c) => `<th>${this.parser.parseInline(c.tokens)}</th>`).join('');
  const body = token.rows.map(
    (row) => `<tr>${row.map((c) => `<td>${this.parser.parseInline(c.tokens)}</td>`).join('')}</tr>`
  ).join('');
  return `<div class="scroll-x"><table><thead><tr>${header}</tr></thead><tbody>${body}</tbody></table></div>\n`;
};

marked.setOptions({ renderer, gfm: true, breaks: false });

function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function stripTags(s) {
  return String(s).replace(/<[^>]*>/g, '');
}

/** marked escapes text before it reaches us, so TOC labels must be decoded. */
function decodeEntities(s) {
  return String(s)
    .replace(/&#(\d+);/g, (_m, n) => String.fromCharCode(Number(n)))
    .replace(/&#x([0-9a-f]+);/gi, (_m, n) => String.fromCharCode(parseInt(n, 16)))
    .replace(/&quot;/g, '"').replace(/&apos;/g, "'")
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
}
export function slug(text) {
  return String(text).toLowerCase().trim()
    .replace(/[^\w\s·-]/g, '')
    .replace(/[\s·]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}

/**
 * Pull $$…$$ and $…$ out of the source, render them with KaTeX, and leave an
 * opaque placeholder behind for marked to carry through untouched.
 */
function extractMath(src) {
  const store = [];
  const stash = (tex, display) => {
    const html = renderMath(tex, display);
    store.push(html);
    return `%%KTX${store.length - 1}%%`;
  };

  let out = '';
  let inFence = false;

  // Fenced code must be left completely alone — a $ inside a shell snippet is
  // a prompt, not mathematics.
  for (const line of src.split('\n')) {
    if (/^\s*(```|~~~)/.test(line)) inFence = !inFence;
    out += (inFence || /^\s*(```|~~~)/.test(line) ? line : maskLine(line)) + '\n';
  }

  function maskLine(line) {
    // Inline code spans are equally off limits.
    return line.replace(/`[^`]*`|\$\$([^$]+)\$\$|\$([^$\n]+)\$/g, (m, block, inline) => {
      if (m.startsWith('`')) return m;
      if (block !== undefined) return stash(block, true);
      if (inline !== undefined) return stash(inline, false);
      return m;
    });
  }

  // Display math on its own lines ($$ … $$ spanning multiple lines).
  out = out.replace(/\$\$\n?([\s\S]+?)\n?\$\$/g, (_m, tex) => stash(tex, true));

  return { text: out, store };
}

function renderMath(tex, display) {
  try {
    return katex.renderToString(tex.trim(), {
      displayMode: display,
      throwOnError: false,
      strict: false,
      output: 'html',
    });
  } catch {
    return `<code>${escapeHtml(tex)}</code>`;
  }
}

export function renderMarkdown(source) {
  if (!source) return { html: '', headings: [] };

  const { text, store } = extractMath(source);
  let html = marked.parse(text);
  html = html.replace(/%%KTX(\d+)%%/g, (_m, n) => store[Number(n)] ?? '');

  // Table of contents, from the h2/h3 the renderer just gave ids to.
  const headings = [];
  const re = /<h([23]) id="([^"]*)">([\s\S]*?)<\/h[23]>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    headings.push({ level: Number(m[1]), id: m[2], text: decodeEntities(stripTags(m[3])) });
  }

  return { html, headings };
}

/**
 * The rendered article.
 *
 * `dropFirstHeading` removes the leading h1, and `dropTitle` additionally
 * removes a following h2 that merely repeats the title already shown in the
 * page header — the vault puts the display title in the h2, because the h1
 * carries the lecture's position ("CS 101 · Lecture 5 (Week 1, Lecture 2)").
 */
export function Markdown({ source, className = 'prose', dropFirstHeading = false, dropTitle = null }) {
  const { html } = useMemo(() => {
    const r = renderMarkdown(source);
    if (!dropFirstHeading) return r;
    let out = r.html.replace(/^\s*<h1[^>]*>[\s\S]*?<\/h1>\s*/, '');
    if (dropTitle) {
      const norm = (t) => decodeEntities(stripTags(t)).replace(/\s+/g, ' ').trim().toLowerCase();
      out = out.replace(/^\s*<h2[^>]*>([\s\S]*?)<\/h2>\s*/, (m, inner) =>
        (norm(inner) === norm(dropTitle) ? '' : m));
    }
    return { ...r, html: out };
  }, [source, dropFirstHeading, dropTitle]);

  const ref = useRef(null);

  // External links open in a new tab; in-page anchors keep their default.
  useEffect(() => {
    const root = ref.current;
    if (!root) return;
    for (const a of root.querySelectorAll('a[href^="http"]')) {
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
    }
  }, [html]);

  return <div ref={ref} className={className} dangerouslySetInnerHTML={{ __html: html }} />;
}

export function useHeadings(source, dropTitle = null) {
  return useMemo(() => {
    if (!source) return [];
    const hs = renderMarkdown(source).headings;
    if (!dropTitle) return hs;
    const norm = (t) => String(t).replace(/\s+/g, ' ').trim().toLowerCase();
    return hs.filter((h, i) => !(i === 0 && h.level === 2 && norm(h.text) === norm(dropTitle)));
  }, [source, dropTitle]);
}
