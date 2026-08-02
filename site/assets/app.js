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

  function buildTree(node, container, depth) {
    var ul = el("ul");
    (node.c || []).forEach(function (kid) {
      var li = el("li");
      var row = el("div", "row");
      var tw = el("button", "tw", "▸");
      var a = el("a", null, kid.t);
      a.href = PRE + kid.r;
      row.appendChild(tw);
      row.appendChild(a);
      li.appendChild(row);

      var hasKids = (kid.c && kid.c.length) || (kid.p && kid.p.length);
      if (!hasKids) tw.classList.add("leaf");
      if (kid.w && done[kid.w]) li.classList.add("done");
      li.dataset.route = kid.r;
      if (kid.w) li.dataset.week = kid.w;

      if (hasKids) {
        var sub = buildTree(kid, li, depth + 1);
        tw.addEventListener("click", function (e) {
          e.preventDefault();
          li.classList.toggle("open");
          tw.textContent = li.classList.contains("open") ? "▾" : "▸";
        });
      }
      ul.appendChild(li);
    });
    (node.p || []).forEach(function (p) {
      var li = el("li");
      var row = el("div", "row");
      var tw = el("button", "tw leaf", "");
      var a = el("a", p.s ? "sol" : null, p.t);
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

  function openToCurrent() {
    var target = document.querySelector('#nav li[data-route="' + CSS.escape(ROUTE) + '"]');
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
    var n = target;
    while (n && n.id !== "nav") {
      if (n.tagName === "LI") {
        n.classList.add("open");
        var tw = n.querySelector(":scope > .row > .tw");
        if (tw && !tw.classList.contains("leaf")) tw.textContent = "▾";
      }
      n = n.parentNode;
    }
    var a = target.querySelector(":scope > .row > a");
    if (a) setTimeout(function () { a.scrollIntoView({ block: "center" }); }, 0);
  }

  function paintProgress(weeks) {
    var total = weeks.length;
    var n = weeks.filter(function (w) { return done[w]; }).length;
    var box = document.getElementById("progress");
    if (!box) return;
    box.innerHTML = "";
    box.appendChild(el("span", null, n + " / " + total + " weeks complete"));
    var bar = el("div", "bar");
    var fill = el("i");
    fill.style.width = total ? (100 * n / total) + "%" : "0";
    bar.appendChild(fill);
    box.appendChild(bar);
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
  document.getElementById("navToggle").addEventListener("click", function () {
    body.classList.toggle("nav-open");
  });

  typeset();

  fetch(PRE + "assets/nav.json").then(function (r) { return r.json(); }).then(function (nav) {
    var host = document.getElementById("nav");
    buildTree(nav, host, 0);
    openToCurrent();
  }).catch(function () {
    document.getElementById("nav").textContent = "Navigation unavailable (serve over http).";
  });

  fetch(PRE + "assets/search.json").then(function (r) { return r.json(); }).then(function (data) {
    setupSearch(data.docs);
    paintProgress(data.weeks);
    setupWeek(data.weeks);
  }).catch(function () { /* search unavailable on file:// */ });

  setupGate();
})();
