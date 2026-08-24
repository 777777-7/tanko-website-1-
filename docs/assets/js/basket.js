/* Primaxs basket — localStorage-backed, cross-page, with fly-to-basket animation.
   Public API: window.PrimaxsBasket.add({sku, name, image, url})  */
(function () {
  var KEY = "primaxs.basket.v1";

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return []; }
  }
  function save(items) { localStorage.setItem(KEY, JSON.stringify(items)); render(); }

  function find(items, sku) { return items.findIndex(function (x) { return x.sku === sku; }); }

  function add(item) {
    if (!item || !item.sku) return;
    var items = load();
    var i = find(items, item.sku);
    if (i >= 0) items[i].qty += 1;
    else items.push({
      sku: item.sku, name: item.name || item.sku,
      image: item.image || "", url: item.url || "", qty: 1
    });
    save(items);
  }
  function setQty(sku, qty) {
    var items = load();
    var i = find(items, sku);
    if (i < 0) return;
    qty = Math.max(0, Math.min(999, parseInt(qty, 10) || 0));
    if (qty === 0) items.splice(i, 1);
    else items[i].qty = qty;
    save(items);
  }
  function remove(sku) {
    var items = load().filter(function (x) { return x.sku !== sku; });
    save(items);
  }
  function clear() { save([]); }

  function count() {
    return load().reduce(function (n, x) { return n + x.qty; }, 0);
  }

  // ─── render ─────────────────────────────────────────────
  function render() {
    var items = load();
    var badge = document.getElementById("basket-count");
    var n = count();
    if (badge) {
      badge.textContent = n;
      badge.setAttribute("data-count", String(n));
    }
    var list = document.getElementById("basket-list");
    var empty = document.getElementById("basket-empty");
    var foot = document.getElementById("basket-foot");
    if (!list) return;
    list.innerHTML = "";
    if (!items.length) {
      empty && empty.removeAttribute("hidden");
      foot && (foot.hidden = true);
      return;
    }
    empty && empty.setAttribute("hidden", "");
    foot && (foot.hidden = false);
    items.forEach(function (it) {
      var li = document.createElement("li");
      li.className = "basket-item";
      var img = it.image ? '<img src="/' + it.image.replace(/^\//, "") + '" alt="' + escapeHtml(it.sku) + '">' : "";
      var link = it.url ? ('/' + it.url.replace(/^\//, "")) : null;
      li.innerHTML =
        '<div class="basket-item-img">' + img + '</div>' +
        '<div class="basket-item-body">' +
          (link ? '<a href="' + link + '" class="basket-item-name">' + escapeHtml(it.name) + '</a>'
                : '<span class="basket-item-name">' + escapeHtml(it.name) + '</span>') +
          '<span class="basket-item-sku">' + escapeHtml(it.sku) + '</span>' +
          '<div class="basket-item-qty">' +
            '<button type="button" class="qty-btn" data-dec="' + escapeHtml(it.sku) + '" aria-label="Decrease">−</button>' +
            '<input type="number" min="1" max="999" value="' + it.qty + '" data-sku="' + escapeHtml(it.sku) + '" aria-label="Quantity">' +
            '<button type="button" class="qty-btn" data-inc="' + escapeHtml(it.sku) + '" aria-label="Increase">+</button>' +
          '</div>' +
        '</div>' +
        '<button type="button" class="basket-item-remove" data-remove="' + escapeHtml(it.sku) + '" aria-label="Remove">×</button>';
      list.appendChild(li);
    });
    var total = document.getElementById("basket-total");
    if (total) total.textContent = String(n);
  }
  function escapeHtml(s) {
    return String(s || "").replace(/[&<>"']/g, function (c) {
      return {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c];
    });
  }

  // ─── panel open/close ────────────────────────────────────
  var panel = null;
  function openPanel() {
    panel = document.getElementById("basket-panel");
    if (!panel) return;
    panel.classList.add("is-open");
    panel.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }
  function closePanel() {
    panel = document.getElementById("basket-panel");
    if (!panel) return;
    panel.classList.remove("is-open");
    panel.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  // ─── fly-to-basket animation ────────────────────────────
  function fly(fromEl, imageUrl) {
    var target = document.getElementById("basket-fab");
    if (!fromEl || !target || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var rectFrom = fromEl.getBoundingClientRect();
    var rectTo = target.getBoundingClientRect();
    var flyEl = document.createElement("div");
    flyEl.className = "basket-fly";
    if (imageUrl) {
      flyEl.style.backgroundImage = 'url("/' + imageUrl.replace(/^\//, "") + '")';
    }
    document.body.appendChild(flyEl);
    var startX = rectFrom.left + rectFrom.width / 2 - 30;
    var startY = rectFrom.top + rectFrom.height / 2 - 30;
    var endX = rectTo.left + rectTo.width / 2 - 30;
    var endY = rectTo.top + rectTo.height / 2 - 30;
    flyEl.style.left = startX + "px";
    flyEl.style.top = startY + "px";
    // trigger transition on next frame
    requestAnimationFrame(function () {
      flyEl.style.transform = "translate(" + (endX - startX) + "px," + (endY - startY) + "px) scale(0.28)";
      flyEl.style.opacity = "0.15";
    });
    setTimeout(function () {
      flyEl.remove();
      target.classList.add("is-bumping");
      setTimeout(function () { target.classList.remove("is-bumping"); }, 500);
    }, 700);
  }

  // ─── delegated events ────────────────────────────────────
  document.addEventListener("click", function (e) {
    // add to basket buttons (main product page + variant pages)
    var addBtn = e.target.closest("#add-to-basket, .add-to-basket-btn");
    if (addBtn) {
      e.preventDefault();
      var item = {
        sku: addBtn.getAttribute("data-sku"),
        name: addBtn.getAttribute("data-name"),
        image: addBtn.getAttribute("data-image"),
        url: addBtn.getAttribute("data-url"),
      };
      // if the picker is live, the model button reflects the current pick; sync from picker
      var modelVal = document.getElementById("model-val");
      var stageImg = document.getElementById("stage-img");
      if (modelVal && addBtn.id === "add-to-basket") {
        item.sku = modelVal.textContent.trim() || item.sku;
      }
      if (stageImg && addBtn.id === "add-to-basket") {
        item.image = stageImg.getAttribute("src") || item.image;
      }
      fly(addBtn, item.image);
      add(item);
      return;
    }
    // open basket
    if (e.target.closest("#basket-fab")) {
      e.preventDefault(); render(); openPanel(); return;
    }
    // close basket
    if (e.target.closest("[data-close-basket]")) {
      e.preventDefault(); closePanel(); return;
    }
    // remove item
    var rem = e.target.closest("[data-remove]");
    if (rem) { e.preventDefault(); remove(rem.getAttribute("data-remove")); return; }
    // inc / dec
    var inc = e.target.closest("[data-inc]");
    if (inc) { var s = inc.getAttribute("data-inc"); setQty(s, (load()[find(load(), s)] || {qty: 0}).qty + 1); return; }
    var dec = e.target.closest("[data-dec]");
    if (dec) { var s2 = dec.getAttribute("data-dec"); setQty(s2, (load()[find(load(), s2)] || {qty: 0}).qty - 1); return; }
    // clear
    if (e.target.closest("#basket-clear")) {
      e.preventDefault();
      if (confirm("Clear all items from your basket?")) clear();
      return;
    }
  });
  document.addEventListener("input", function (e) {
    var t = e.target;
    if (t.matches && t.matches("#basket-list input[type=number]")) {
      setQty(t.getAttribute("data-sku"), t.value);
    }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closePanel();
  });

  window.PrimaxsBasket = { add: add, remove: remove, setQty: setQty, clear: clear, load: load, count: count, render: render };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
})();
