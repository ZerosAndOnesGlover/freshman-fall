/* Client behaviour for the CSE degree study site.
   Progress lives in localStorage, so it is per-browser and never leaves the machine. */
(function () {
  "use strict";

  var body = document.body;
  var PRE = body.dataset.prefix || "";
  var ROUTE = body.dataset.route || "";
  var WEEK = body.dataset.week || "";
  var KEY = "cse.progress.v1";

  // ---------- progress ----------
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function save(o) {
    try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) { /* private mode */ }
  }
  var done = load();

  // ---------- maths ----------
  function typeset() {
    if (!window.renderMathInElement) return;
    window.renderMathInElement(document.getElementById("content"), {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false }
      ],
      ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"],
      throwOnError: false,
      errorColor: "#b4560c"
    });
  }

  // ---------- navigation tree ----------
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function toggle(li) {
    li.classList.toggle("open");
    var tw = li.querySelector(":scope > .row > .tw");
    if (tw) tw.setAttribute("aria-expanded", li.classList.contains("open"));
  }

  function buildTree(node, container, depth) {
    var ul = el("ul");
    (node.c || []).forEach(function (kid) {
      var li = el("li");
      var hasKids = (kid.c && kid.c.length) || (kid.p && kid.p.length);
      var row = el("div", hasKids ? "row branch" : "row");
      var tw = el("button", "tw", "▸");
      tw.type = "button";
      tw.setAttribute("aria-label", "Expand " + kid.t);
      tw.setAttribute("aria-expanded", "false");

      // A folder row is a toggle, not a link. Its own page is reachable via the
      // "Overview" entry below, so there is no hidden click target.
      var label = hasKids ? el("span", "label", kid.t) : el("a", "label", kid.t);
      if (!hasKids) label.href = PRE + kid.r;

      if (!hasKids) tw.classList.add("leaf");
      if (kid.w && done[kid.w]) li.classList.add("done");
      li.dataset.route = kid.r;
      if (kid.w) li.dataset.week = kid.w;

      row.appendChild(tw);
      row.appendChild(label);
      li.appendChild(row);

      if (hasKids) {
        var sub = buildTree(kid, li, depth + 1);
        var ov = el("li");
        var ovRow = el("div", "row");
        var ovTw = el("button", "tw leaf", "");
        ovTw.type = "button";
        var ovA = el("a", "label ov", "Overview");
        ovA.href = PRE + kid.r;
        ov.dataset.route = kid.r;
        ovRow.appendChild(ovTw);
        ovRow.appendChild(ovA);
        ov.appendChild(ovRow);
        sub.insertBefore(ov, sub.firstChild);

        // Clicking anywhere on the row toggles -- a much larger target than
        // the chevron alone.
        row.addEventListener("click", function (e) {
          if (e.target.closest("a")) return;
          e.preventDefault();
          toggle(li);
        });
      }
      ul.appendChild(li);
    });
    (node.p || []).forEach(function (p) {
      var li = el("li");
      var row = el("div", "row");
      var tw = el("button", "tw leaf", "");
      tw.type = "button";
      var a = el("a", "label" + (p.s ? " sol" : ""), p.t);
      a.href = PRE + p.r;
      li.dataset.route = p.r;
      row.appendChild(tw);
      row.appendChild(a);
      li.appendChild(row);
      ul.appendChild(li);
    });
    container.appendChild(ul);
    return ul;
  }

  function expandAncestors(node) {
    var n = node;
    while (n && n.id !== "nav") {
      if (n.tagName === "LI" && !n.classList.contains("open")) {
        n.classList.add("open");
        var tw = n.querySelector(":scope > .row > .tw");
        if (tw && !tw.classList.contains("leaf")) tw.setAttribute("aria-expanded", "true");
      }
      n = n.parentNode;
    }
  }

  function openToCurrent() {
    // Match on the actual link, so an "Overview" entry wins over the folder row
    // that shares its route.
    var links = document.querySelectorAll("#nav a.label[href]");
    var target = null;
    for (var i = 0; i < links.length; i++) {
      if (links[i].getAttribute("href") === PRE + ROUTE) { target = links[i].closest("li"); break; }
    }
    if (!target) {
      // a page inside a folder: fall back to the nearest ancestor index
      var parts = ROUTE.split("/");
      while (parts.length > 1 && !target) {
        parts.pop();
        target = document.querySelector(
          '#nav li[data-route="' + CSS.escape(parts.join("/") + "/index.html") + '"]');
      }
    }
    if (!target) return;
    target.classList.add("cur");
    expandAncestors(target);
    var a = target.querySelector(":scope > .row > .label");
    if (a) setTimeout(function () { a.scrollIntoView({ block: "center" }); }, 0);
  }

  function paintProgress(weeks) {
    var total = weeks.length;
    var n = weeks.filter(function (w) { return done[w]; }).length;
    var box = document.getElementById("progress");
    if (!box) return;
    box.innerHTML = "";
    var lbl = el("div", "lbl");
    lbl.appendChild(el("span", null, "Progress"));
    var b = el("b", null, n + " / " + total);
    lbl.appendChild(b);
    box.appendChild(lbl);
    var bar = el("div", "bar");
    var fill = el("i");
    bar.appendChild(fill);
    box.appendChild(bar);
    // set width after insertion so the transition runs
    requestAnimationFrame(function () {
      fill.style.width = total ? (100 * n / total) + "%" : "0";
    });
  }

  // ---------- table of contents ----------
  function buildToc() {
    var toc = document.getElementById("toc");
    var content = document.getElementById("content");
    if (!toc || !content) return;
    // On a gated page the headings exist but are hidden; wait for the reveal
    // so the rail never lists sections the reader cannot see or scroll to.
    if (document.querySelector(".gate")) { body.classList.add("no-toc"); return; }

    var hs = content.querySelectorAll("h2[id], h3[id]");
    // A rail is only worth the space when there is something to navigate.
    if (hs.length < 3) { body.classList.add("no-toc"); return; }

    toc.textContent = "";
    body.classList.remove("no-toc");
    toc.appendChild(el("div", "toc-h", "On this page"));
    var links = [];
    hs.forEach(function (h) {
      // skip the injected "#" anchor so it does not land in the label
      var label = "";
      h.childNodes.forEach(function (n) {
        if (n.nodeType === 1 && n.classList && n.classList.contains("anchor")) return;
        label += n.textContent;
      });
      var a = el("a", h.tagName === "H3" ? "lv3" : null, label.trim());
      a.href = "#" + h.id;
      toc.appendChild(a);
      links.push({ a: a, h: h });
    });

    if (!("IntersectionObserver" in window)) return;
    var seen = new Map();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { seen.set(e.target, e); });
      var best = null;
      seen.forEach(function (e) {
        if (!e.isIntersecting) return;
        if (!best || e.target.offsetTop < best.target.offsetTop) best = e;
      });
      if (!best) return;
      links.forEach(function (l) { l.a.classList.toggle("on", l.h === best.target); });
    }, { rootMargin: "0px 0px -72% 0px", threshold: 0 });
    links.forEach(function (l) { io.observe(l.h); });
  }

  // ---------- search ----------
  function setupSearch(docs) {
    var q = document.getElementById("q");
    var out = document.getElementById("results");
    if (!q || !out) return;
    var timer;

    function run() {
      var term = q.value.trim().toLowerCase();
      out.innerHTML = "";
      if (term.length < 2) return;
      var words = term.split(/\s+/);
      var hits = [];
      for (var i = 0; i < docs.length && hits.length < 400; i++) {
        var d = docs[i];
        var hay = (d.t + " " + d.b + " " + (d.h || []).join(" ") + " " + d.x).toLowerCase();
        var score = 0, ok = true;
        for (var w = 0; w < words.length; w++) {
          var idx = hay.indexOf(words[w]);
          if (idx < 0) { ok = false; break; }
          score += d.t.toLowerCase().indexOf(words[w]) >= 0 ? 10 : 1;
        }
        if (ok) hits.push({ d: d, s: score });
      }
      if (!hits.length) {
        out.appendChild(el("div", "rn", "No matches"));
        return;
      }
      hits.sort(function (a, b) { return b.s - a.s; });
      hits.slice(0, 30).forEach(function (h) {
        var a = el("a");
        a.href = PRE + h.d.r;
        a.appendChild(el("span", null, h.d.t));
        if (h.d.b) a.appendChild(el("span", "rb", h.d.b));
        out.appendChild(a);
      });
      if (hits.length > 30) {
        out.appendChild(el("div", "rn", hits.length - 30 + " more…"));
      }
    }

    q.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(run, 110);
    });
    q.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { q.value = ""; out.innerHTML = ""; q.blur(); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && document.activeElement !== q) { e.preventDefault(); q.focus(); }
    });
  }

  // ---------- solution gate ----------
  function setupGate() {
    var btn = document.querySelector(".gate .reveal");
    var panel = document.querySelector(".gated");
    if (!btn || !panel) return;
    btn.addEventListener("click", function () {
      panel.hidden = false;
      btn.closest(".gate").remove();
      typeset();
      buildToc();
    });
  }

  // ---------- week completion ----------
  function setupWeek(weeks) {
    var box = document.querySelector(".week-done");
    if (!box) return;
    var week = box.dataset.week;
    var btn = box.querySelector(".mark");
    function paint() {
      var on = !!done[week];
      box.classList.toggle("on", on);
      btn.textContent = on ? "✓ Week complete" : "Mark week complete";
    }
    btn.addEventListener("click", function () {
      if (done[week]) delete done[week]; else done[week] = Date.now();
      save(done);
      paint();
      paintProgress(weeks);
      var li = document.querySelector('#nav li[data-week="' + CSS.escape(week) + '"]');
      if (li) li.classList.toggle("done", !!done[week]);
    });
    paint();
  }

  // ---------- boot ----------
  // ---------- visit history (for "Continue reading") ----------
  var VISITS = "cse.visits.v1";
  function recordVisit() {
    if (ROUTE === "index.html") return;
    var title = document.querySelector("#content h1");
    var crumbs = document.querySelectorAll(".crumbs a, .crumbs span");
    var trail = [];
    crumbs.forEach(function (c, i) {
      if (i > 0 && i < crumbs.length - 1) trail.push(c.textContent.trim());
    });
    try {
      var list = JSON.parse(localStorage.getItem(VISITS)) || [];
      list = list.filter(function (v) { return v.r !== ROUTE; });
      list.unshift({
        r: ROUTE,
        t: (title ? title.textContent : document.title).replace(/^#/, "").trim(),
        b: trail.join(" › "),
        d: Date.now()
      });
      localStorage.setItem(VISITS, JSON.stringify(list.slice(0, 12)));
    } catch (e) { /* ignore */ }
  }

  function paintDashboard(weeks) {
    var box = document.getElementById("dashProgress");
    if (box) {
      var total = weeks.length;
      var n = weeks.filter(function (w) { return done[w]; }).length;
      var pct = total ? Math.round(100 * n / total) : 0;
      box.innerHTML = "";
      var big = el("div", "big", n + " / " + total);
      big.appendChild(el("small", null, "weeks complete · " + pct + "%"));
      box.appendChild(big);
      var track = el("div", "track");
      var fill = el("i");
      track.appendChild(fill);
      box.appendChild(track);
      requestAnimationFrame(function () { fill.style.width = pct + "%"; });

      // per-course rollup, so the number is actionable rather than decorative
      var byCourse = {};
      weeks.forEach(function (w) {
        var course = w.split("/").slice(0, 3).join("/");
        byCourse[course] = byCourse[course] || { t: 0, n: 0 };
        byCourse[course].t++;
        if (done[w]) byCourse[course].n++;
      });
      var keys = Object.keys(byCourse).sort();
      if (keys.length) {
        var wrap = el("div", "bars");
        keys.forEach(function (k) {
          var c = byCourse[k];
          var row = el("div", "brow");
          row.title = k + ": " + c.n + " of " + c.t + " weeks";
          var name = k.split("/").pop().toUpperCase().replace(/-/g, " ");
          row.appendChild(el("div", "blab", name));
          var tr = el("div", "btrack");
          var f = el("div", "bfill");
          f.style.background = "var(--green)";
          f.style.width = (100 * c.n / c.t) + "%";
          tr.appendChild(f);
          row.appendChild(tr);
          var v = el("div", "bval", String(c.n));
          v.appendChild(el("span", null, "of " + c.t));
          row.appendChild(v);
          wrap.appendChild(row);
        });
        box.appendChild(wrap);
      }
    }

    var rec = document.getElementById("dashRecent");
    if (rec) {
      var list = [];
      try { list = JSON.parse(localStorage.getItem(VISITS)) || []; } catch (e) { list = []; }
      if (!list.length) return;
      rec.innerHTML = "";
      var ul = el("ul", "feed");
      list.slice(0, 8).forEach(function (v) {
        var li = el("li");
        var a = el("a", null, v.t);
        a.href = PRE + v.r;
        li.appendChild(a);
        if (v.b) li.appendChild(el("span", null, v.b));
        ul.appendChild(li);
      });
      rec.appendChild(ul);
    }
  }

  // ---------- sidebar collapse ----------
  var RAIL = "cse.rail.v1";
  try {
    if (localStorage.getItem(RAIL) === "1") body.classList.add("rail-collapsed");
  } catch (e) { /* ignore */ }

  function setRail(collapsed) {
    body.classList.toggle("rail-collapsed", collapsed);
    try { localStorage.setItem(RAIL, collapsed ? "1" : "0"); } catch (e) { /* ignore */ }
  }
  function toggleRail() {
    if (window.matchMedia("(max-width: 900px)").matches) {
      body.classList.toggle("nav-open");
    } else {
      setRail(!body.classList.contains("rail-collapsed"));
    }
  }
  var railBtn = document.getElementById("railToggle");
  if (railBtn) railBtn.addEventListener("click", toggleRail);
  document.getElementById("navToggle").addEventListener("click", toggleRail);
  var scrim = document.getElementById("scrim");
  if (scrim) scrim.addEventListener("click", function () { body.classList.remove("nav-open"); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "\\" && !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) {
      e.preventDefault();
      toggleRail();
    }
  });

  // ---------- heading anchors ----------
  (function () {
    var c = document.getElementById("content");
    if (!c) return;
    c.querySelectorAll("h2[id], h3[id], h4[id]").forEach(function (h) {
      var a = el("a", "anchor", "#");
      a.href = "#" + h.id;
      a.setAttribute("aria-label", "Link to this section");
      h.insertBefore(a, h.firstChild);
    });
  })();

  typeset();
  buildToc();

  fetch(PRE + "assets/nav.json").then(function (r) { return r.json(); }).then(function (nav) {
    var host = document.getElementById("nav");
    buildTree(nav, host, 0);
    openToCurrent();
  }).catch(function () {
    document.getElementById("nav").textContent = "Navigation unavailable (serve over http).";
  });

  recordVisit();

  fetch(PRE + "assets/search.json").then(function (r) { return r.json(); }).then(function (data) {
    setupSearch(data.docs);
    paintProgress(data.weeks);
    setupWeek(data.weeks);
    paintDashboard(data.weeks);
  }).catch(function () { /* search unavailable on file:// */ });

  setupGate();
})();
