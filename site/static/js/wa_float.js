/* WhatsApp floating button — opens a basket-review modal, then builds a
   pre-filled wa.me link that includes the selected product codes.
   Empty basket → original greeting only + catalogue link. */
(function () {
  var KEY = "primaxs.basket.v1";
  var WA_NUMBER = "601158419886";
  var WA_GREETING = "Hi, I'm interested in Tanko industrial storage products.";

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return []; }
  }
  function escapeHtml(s) {
    return String(s || "").replace(/[&<>"']/g, function (c) {
      return {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c];
    });
  }
  function encPath(p) {
    return String(p || "").replace(/^\//, "").split("/").map(encodeURIComponent).join("/");
  }

  function buildWaUrl(items) {
    var text = WA_GREETING;
    if (items && items.length) {
      text += "\n\nProduct code:\n" + items.map(function (it) {
        return "- " + it.sku + (it.qty > 1 ? " x" + it.qty : "") + (it.name ? " — " + it.name : "");
      }).join("\n");
    }
    return "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(text);
  }

  function render() {
    var items = load();
    var list = document.getElementById("wa-basket-list");
    var empty = document.getElementById("wa-basket-empty");
    var sendBtn = document.getElementById("wa-send-btn");
    var sendLabel = document.getElementById("wa-send-label");
    if (!list) return;

    list.innerHTML = "";
    if (!items.length) {
      empty && empty.removeAttribute("hidden");
      if (sendBtn) {
        sendBtn.href = buildWaUrl([]);
        if (sendLabel) sendLabel.textContent = "Contact Us on WhatsApp";
      }
      return;
    }
    empty && empty.setAttribute("hidden", "");

    var BASE = (window.__BASE__ || "/").replace(/\/?$/, "/");
    items.forEach(function (it) {
      var li = document.createElement("li");
      li.className = "wa-basket-item";
      var imgSrc = it.image ? BASE + encPath(it.image) : "";
      var img = imgSrc
        ? '<img src="' + imgSrc + '" alt="' + escapeHtml(it.sku) + '" ' +
          'onerror="var s=this.getAttribute(\'src\');' +
          'if(/\\.png($|\\?)/i.test(s)){this.src=s.replace(/\\.png/i,\'.jpg\');return;}' +
          'if(/\\.jpeg($|\\?)/i.test(s)){this.src=s.replace(/\\.jpeg/i,\'.jpg\');return;}' +
          'this.style.display=\'none\';">'
        : '<div class="wa-item-img-placeholder"></div>';
      var link = it.url ? (BASE + encPath(it.url)) : null;
      li.innerHTML =
        '<div class="wa-item-img">' + img + '</div>' +
        '<div class="wa-item-body">' +
          (link ? '<a href="' + link + '" class="wa-item-name">' + escapeHtml(it.name || it.sku) + '</a>'
                : '<span class="wa-item-name">' + escapeHtml(it.name || it.sku) + '</span>') +
          '<span class="wa-item-sku">' + escapeHtml(it.sku) + '</span>' +
        '</div>' +
        '<span class="wa-item-qty">×' + it.qty + '</span>';
      list.appendChild(li);
    });

    if (sendBtn) {
      sendBtn.href = buildWaUrl(items);
      if (sendLabel) sendLabel.textContent = "Send " + items.length + " item" + (items.length > 1 ? "s" : "") + " via WhatsApp";
    }
  }

  function openModal() {
    var m = document.getElementById("wa-modal");
    if (!m) return;
    render();
    m.classList.add("is-open");
    m.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }
  function closeModal() {
    var m = document.getElementById("wa-modal");
    if (!m) return;
    m.classList.remove("is-open");
    m.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  document.addEventListener("click", function (e) {
    if (e.target.closest("#wa-fab")) {
      e.preventDefault();
      openModal();
      return;
    }
    var waClose = e.target.closest("[data-close-wa]");
    if (waClose) {
      // If the closer is a link with an href, let navigation happen — just
      // close the modal. Otherwise treat it as a plain close button.
      var link = waClose.closest("a[href]");
      if (link && link.getAttribute("href") && link.getAttribute("href") !== "#") {
        closeModal();
        return;
      }
      e.preventDefault();
      closeModal();
      return;
    }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeModal();
  });

  // keep the send link fresh if the basket changes while modal is open
  window.addEventListener("storage", function (e) {
    if (e.key === KEY && document.getElementById("wa-modal") &&
        document.getElementById("wa-modal").classList.contains("is-open")) {
      render();
    }
  });
})();
