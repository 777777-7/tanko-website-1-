/* Nav SKU / product search — full-screen modal popup, product cards with
   images, keyboard navigation. Loads the index once, filters client-side. */
(function () {
  var btn = document.getElementById("nav-search-btn");
  var modal = document.getElementById("nav-search-modal");
  var input = document.getElementById("nav-search-input");
  var out = document.getElementById("nav-search-results");
  if (!btn || !modal || !input || !out) return;

  var index = null;
  var loading = false;
  var visibleHits = []; // current DOM elements, for keyboard nav
  var focusIndex = -1;

  var BASE = (window.__BASE__ || "/").replace(/\/?$/, "/");

  function loadIndex() {
    if (index || loading) return;
    loading = true;
    fetch(BASE + "search_index.json")
      .then(function (r) { return r.json(); })
      .then(function (data) { index = data; loading = false; if (input.value) render(); })
      .catch(function () { loading = false; });
  }

  function open() {
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    loadIndex();
    setTimeout(function () { input.focus(); input.select(); }, 30);
    if (!input.value) renderEmpty();
  }
  function close() {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    focusIndex = -1;
  }

  btn.addEventListener("click", function () { open(); });
  modal.addEventListener("click", function (e) {
    if (e.target.closest("[data-close-search]")) close();
  });
  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key === "k") { e.preventDefault(); open(); return; }
    if (!modal.classList.contains("is-open")) return;
    if (e.key === "Escape") { e.preventDefault(); close(); return; }
    if (e.key === "ArrowDown") { e.preventDefault(); moveFocus(1); return; }
    if (e.key === "ArrowUp") { e.preventDefault(); moveFocus(-1); return; }
    if (e.key === "Enter") {
      if (focusIndex >= 0 && visibleHits[focusIndex]) {
        location.href = visibleHits[focusIndex].getAttribute("href");
      } else if (visibleHits.length) {
        location.href = visibleHits[0].getAttribute("href");
      }
    }
  });

  function moveFocus(delta) {
    if (!visibleHits.length) return;
    focusIndex = ((focusIndex + delta) % visibleHits.length + visibleHits.length) % visibleHits.length;
    visibleHits.forEach(function (a, i) {
      if (i === focusIndex) { a.classList.add("is-focused"); a.scrollIntoView({block: "nearest"}); }
      else a.classList.remove("is-focused");
    });
  }

  function escapeHtml(s) {
    return String(s || "").replace(/[&<>"']/g, function (c) {
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
    });
  }
  function highlight(text, q) {
    var idx = text.toLowerCase().indexOf(q.toLowerCase());
    if (idx < 0) return escapeHtml(text);
    return escapeHtml(text.slice(0, idx)) +
      '<mark>' + escapeHtml(text.slice(idx, idx + q.length)) + '</mark>' +
      escapeHtml(text.slice(idx + q.length));
  }

  function renderEmpty() {
    out.innerHTML =
      '<div class="ns-hint">' +
      '<p><strong>Search the catalog</strong> — type an SKU (WE-47, RA-6091), a product name (workbench, locker), or a category (cnc, workstation).</p>' +
      '</div>';
    visibleHits = []; focusIndex = -1;
  }

  var debounceT = null;
  input.addEventListener("input", function () {
    clearTimeout(debounceT);
    debounceT = setTimeout(render, 60);
  });

  function render() {
    var q = input.value.trim();
    if (!q) { renderEmpty(); return; }
    if (!index) {
      out.innerHTML = '<div class="ns-hint">Loading catalog…</div>';
      return;
    }
    var ql = q.toLowerCase();
    var scored = [];
    var fuzzyPrefix = fuzzyKey(ql); // e.g. "was-54032" -> "was-5403"
    for (var i = 0; i < index.length; i++) {
      var it = index[i];
      var pos = it.h.indexOf(ql);
      // Family pages (2-path URLs like "rack/me/") rank above variants (3-path like "rack/me/me-321/")
      var isFamily = (it.url.match(/\//g) || []).length <= 2;
      var familyBoost = isFamily ? -200 : 0;
      if (pos >= 0) {
        var score = pos + familyBoost;
        if (it.sku.toLowerCase() === ql) score = -1000 + familyBoost;
        else if (it.sku.toLowerCase().indexOf(ql) === 0) score = -500 + pos + familyBoost;
        scored.push({ it: it, score: score, fuzzy: false, isFamily: isFamily });
        continue;
      }
      // Fuzzy fallback: if the query looks like an SKU (letters-digits-hyphen),
      // match on the shared numeric prefix so slightly-wrong codes still hit.
      if (fuzzyPrefix && it.h.indexOf(fuzzyPrefix) >= 0) {
        scored.push({ it: it, score: 400 + pos + it.h.indexOf(fuzzyPrefix) + familyBoost, fuzzy: true, isFamily: isFamily });
      }
    }
    scored.sort(function (a, b) { return a.score - b.score; });
    // dedupe by URL, exact/fuzzy combined, exact wins
    var seenUrl = {};
    var top = [];
    for (var j = 0; j < scored.length && top.length < 24; j++) {
      var r = scored[j];
      if (seenUrl[r.it.url]) continue;
      seenUrl[r.it.url] = true;
      top.push(r);
    }
    if (!top.length) {
      out.innerHTML = '<div class="ns-hint">No results for “' + escapeHtml(q) + '”. Try a shorter or different keyword.</div>';
      visibleHits = []; focusIndex = -1;
      return;
    }
    var html = '<div class="ns-count">' + top.length + ' of ' + scored.length + ' matches</div>' +
               '<ul class="ns-grid" role="listbox">';
    top.forEach(function (r) {
      var it = r.it;
      var typeLabel = r.isFamily ? ' <span class="ns-type-badge">Series</span>' : '';
      html +=
        '<li>' +
          '<a class="ns-card' + (r.fuzzy ? ' ns-card-fuzzy' : '') + (r.isFamily ? ' ns-card-family' : '') + '" href="' + BASE + it.url + '" role="option">' +
            '<div class="ns-card-img">' +
              (it.img ? '<img src="' + BASE + it.img + '" alt="" loading="lazy" onerror="this.parentElement.innerHTML=\'<div class=\'ns-img-placeholder\'>No image</div\'">' : '<div class="ns-img-placeholder">No image</div>') +
            '</div>' +
            '<div class="ns-card-body">' +
              '<div class="ns-card-sku">' + highlight(it.sku, q) + typeLabel + '</div>' +
              '<div class="ns-card-name">' + highlight(it.name, q) + '</div>' +
              '<div class="ns-card-cat">' + escapeHtml(it.cat) + (r.fuzzy ? ' · similar SKU' : '') + '</div>' +
            '</div>' +
          '</a>' +
        '</li>';
    });
    html += '</ul>';
    out.innerHTML = html;
    visibleHits = [].slice.call(out.querySelectorAll(".ns-card"));
    focusIndex = -1;
  }

  // Build a tolerant key from an SKU-like query: keep the letter prefix and the
  // first N digits, so "was-54032" -> "was-5403" still matches real "was-54031".
  function fuzzyKey(q) {
    var m = q.match(/^([a-z]{1,5}-)(\d{2,})/);
    if (!m) return "";
    // drop the last digit to tolerate off-by-one codes
    var digits = m[2].slice(0, -1);
    if (digits.length < 3) return "";
    return m[1] + digits;
  }
})();
