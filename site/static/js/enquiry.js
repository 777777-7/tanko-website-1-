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
    var BASE = (window.__BASE__ || "/").replace(/\/?$/, "/");
    function encPath(p) {
      return String(p || "").replace(/^\//, "").split("/").map(encodeURIComponent).join("/");
    }
    items.forEach(function (it) {
      var imgSrc = it.image ? BASE + encPath(it.image) : "";
      var img = imgSrc
        ? '<img src="' + imgSrc + '" alt="' + escapeHtml(it.sku) + '" ' +
          'onerror="var s=this.getAttribute(\'src\');' +
          'if(/\\.png($|\\?)/i.test(s)){this.src=s.replace(/\\.png/i,\'.jpg\');return;}' +
          'if(/\\.jpeg($|\\?)/i.test(s)){this.src=s.replace(/\\.jpeg/i,\'.jpg\');return;}' +
          'this.style.display=\'none\';">'
        : "";
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
      var ctrl = window.AbortController ? new AbortController() : null;
      var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, 15000) : null;
      fetch(ajaxUrl, { method: "POST", headers: {"Accept": "application/json"}, body: fd, signal: ctrl ? ctrl.signal : undefined })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r); })
        .then(function (j) {
          if (j && String(j.success) === "false") throw j;
          onSuccess();
        })
        .catch(function () { onFailure(fd); })
        .then(function () { if (timer) clearTimeout(timer); });
    });
  }

  // FormSubmit failed (down, timeout or success:false): keep the basket and let the
  // customer send the same details by WhatsApp or email in one tap.
  function enquiryText(fd) {
    var lines = [], seen = {};
    fd.forEach(function (v, k) {
      if (k.charAt(0) === "_" || !String(v).trim()) return;
      var label = k.replace(/\[\]$/, "").replace(/_/g, " ");
      if (seen[label]) { lines[seen[label] - 1] += ", " + v; return; }
      lines.push(label.charAt(0).toUpperCase() + label.slice(1) + ": " + v);
      seen[label] = lines.length;
    });
    return "Quote request from storagesystem.com.my\n\n" + lines.join("\n");
  }
  function onFailure(fd) {
    var submitBtn = document.querySelector('#enq-form button[type="submit"]');
    if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "Submit Quote Request"; }
    var text = enquiryText(fd);
    var wa = "https://wa.me/601158419886?text=" + encodeURIComponent(text);
    var mail = "mailto:sales@storagesystem.my?subject=" + encodeURIComponent("Quote request") +
               "&body=" + encodeURIComponent(text.slice(0, 1800));
    var el = document.getElementById("enq-fail");
    if (!el) {
      el = document.createElement("div");
      el.id = "enq-fail";
      el.className = "enq-toast";
      document.body.appendChild(el);
    }
    el.innerHTML =
      '<div class="enq-toast-scrim"></div>' +
      '<div class="enq-toast-card">' +
        '<h3>Sorry, our email form is not working right now.</h3>' +
        '<p>Your details and basket are kept. Send them to us in one tap:</p>' +
        '<p><a class="btn" id="enq-fail-wa" href="' + wa + '" target="_blank" rel="noopener">Send by WhatsApp</a> ' +
        '<a class="btn btn-ghost" href="' + mail + '">Send by email</a></p>' +
        '<p><small>Or call +60 3-4296 4737.</small></p>' +
        '<button type="button" class="btn btn-ghost" id="enq-fail-close">Close</button>' +
      '</div>';
    el.classList.add("is-open");
    var hide = function () { el.classList.remove("is-open"); };
    document.getElementById("enq-fail-close").onclick = hide;
    el.querySelector(".enq-toast-scrim").onclick = hide;
    var waBtn = document.getElementById("enq-fail-wa");
    if (waBtn && window.primaxsAnalytics) waBtn.addEventListener("click", function () { window.primaxsAnalytics.post("whatsapp_send"); });
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
