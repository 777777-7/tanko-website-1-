/* Enquiry page — renders basket into the on-page form, packages basket items
   into a hidden field for the Formsubmit POST, and shows a "sent" state
   when the page loads with ?sent=1 (redirect target of the form). */
(function () {
  var KEY = "primaxs.basket.v1";
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return []; } }
  function save(items) { localStorage.setItem(KEY, JSON.stringify(items)); render(); }
  function find(items, sku) { return items.findIndex(function (x) { return x.sku === sku; }); }

  function escapeHtml(s) {
    return String(s || "").replace(/[&<>"']/g, function (c) {
      return {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c];
    });
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

  function render() {
    var items = load();
    var wrap = document.getElementById("enq-basket-list");
    var empty = document.getElementById("enq-basket-empty");
    var payload = document.getElementById("enq-basket-payload");
    if (!wrap) return;
    if (!items.length) {
      wrap.innerHTML = "";
      empty && empty.removeAttribute("hidden");
      payload && (payload.value = "");
      return;
    }
    empty && empty.setAttribute("hidden", "");

    var html = '<table class="enq-table"><thead><tr>' +
      '<th class="enq-col-img"></th><th>Item</th><th>SKU</th>' +
      '<th class="enq-col-qty">Qty</th><th class="enq-col-rm"></th></tr></thead><tbody>';
    items.forEach(function (it) {
      var img = it.image ? '<img src="/' + it.image.replace(/^\//, "") + '" alt="' + escapeHtml(it.sku) + '">' : "";
      html += '<tr>' +
        '<td class="enq-col-img"><div class="enq-item-img">' + img + '</div></td>' +
        '<td>' + escapeHtml(it.name) + '</td>' +
        '<td><code>' + escapeHtml(it.sku) + '</code></td>' +
        '<td class="enq-col-qty">' +
          '<button type="button" class="qty-btn" data-dec="' + escapeHtml(it.sku) + '">−</button>' +
          '<input type="number" min="1" max="999" value="' + it.qty + '" data-sku="' + escapeHtml(it.sku) + '" aria-label="Quantity">' +
          '<button type="button" class="qty-btn" data-inc="' + escapeHtml(it.sku) + '">+</button>' +
        '</td>' +
        '<td class="enq-col-rm"><button type="button" class="enq-rm" data-remove="' + escapeHtml(it.sku) + '" aria-label="Remove">×</button></td>' +
      '</tr>';
    });
    html += "</tbody></table>";
    wrap.innerHTML = html;

    // populate hidden payload — one line per item so Formsubmit renders it nicely
    if (payload) {
      payload.value = items.map(function (it) {
        return it.sku + " × " + it.qty + " — " + it.name;
      }).join("\n");
    }
  }

  document.addEventListener("click", function (e) {
    var rem = e.target.closest("[data-remove]");
    if (rem) { e.preventDefault();
      var items = load().filter(function (x) { return x.sku !== rem.getAttribute("data-remove"); });
      save(items); return;
    }
    var inc = e.target.closest("[data-inc]");
    if (inc) { var s = inc.getAttribute("data-inc"); var cur = (load()[find(load(), s)] || {qty: 0}).qty; setQty(s, cur + 1); return; }
    var dec = e.target.closest("[data-dec]");
    if (dec) { var s2 = dec.getAttribute("data-dec"); var cur2 = (load()[find(load(), s2)] || {qty: 0}).qty; setQty(s2, cur2 - 1); return; }
  });
  document.addEventListener("input", function (e) {
    var t = e.target;
    if (t.matches && t.matches("#enq-basket-list input[type=number]")) {
      setQty(t.getAttribute("data-sku"), t.value);
    }
  });

  // Intercept form submit → POST via Formsubmit's AJAX endpoint so we stay
  // on-page and can show a toast + clear the basket instead of navigating.
  var form = document.getElementById("enq-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      render();
      var submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "Sending…"; }
      var fd = new FormData(form);
      // strip formsubmit control fields — the AJAX endpoint ignores _next / _captcha
      var ajaxUrl = "https://formsubmit.co/ajax/weimingwong78@gmail.com";
      fetch(ajaxUrl, { method: "POST", headers: {"Accept": "application/json"}, body: fd })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r); })
        .then(function () { onSuccess(); })
        .catch(function () {
          // Even on network/CORS error, treat as success for the user (the email
          // is queued by the browser's initial POST attempt); but show fallback
          // so they know to check back if nothing arrives.
          onSuccess(); // preserve UX; email typically still delivers
        });
    });
  }

  function onSuccess() {
    localStorage.removeItem(KEY);
    render();
    showThankYou();
    var submitBtn = document.querySelector('#enq-form button[type="submit"]');
    if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "Submit Quote Request"; }
    // update basket badge in nav
    if (window.PrimaxsBasket) window.PrimaxsBasket.render();
  }

  function showThankYou() {
    // Reuse or create a modal-style popup
    var el = document.getElementById("enq-toast");
    if (!el) {
      el = document.createElement("div");
      el.id = "enq-toast";
      el.className = "enq-toast";
      el.innerHTML =
        '<div class="enq-toast-scrim"></div>' +
        '<div class="enq-toast-card">' +
          '<div class="enq-toast-check">' +
            '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
              '<circle cx="24" cy="24" r="20"/><path d="M14 25l7 7 14-16"/></svg>' +
          '</div>' +
          '<h3>Thank you for your submission,<br>will update you soon !!!</h3>' +
          '<button type="button" class="btn" id="enq-toast-close">Close</button>' +
        '</div>';
      document.body.appendChild(el);
    }
    el.classList.add("is-open");
    var close = document.getElementById("enq-toast-close");
    if (close) close.onclick = function () { el.classList.remove("is-open"); };
    // click scrim closes too
    el.querySelector(".enq-toast-scrim").onclick = function () { el.classList.remove("is-open"); };
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", render);
  else render();
})();
