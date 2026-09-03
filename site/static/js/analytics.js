// =============================================================================
// Primaxs analytics — records WhatsApp clicks + quote-email submissions to
// Supabase along with a snapshot of the visitor's basket. Read by /sales/.
//
// Public-site side: this file only ever INSERTs; row-level security on the
// `events` table prevents anonymous SELECTs. See supabase-config.js.
// =============================================================================
(function () {
  const URL_ = window.SUPABASE_URL, KEY = window.SUPABASE_KEY;
  if (!URL_ || !KEY) { console.warn("[analytics] supabase-config missing"); return; }

  // Stable opaque visitor id — no PII, only helps deduplicate a session's
  // repeat clicks in the dashboard.
  const VKEY = "primaxs_vid";
  let vid = null;
  try {
    vid = localStorage.getItem(VKEY);
    if (!vid) {
      vid = (crypto.randomUUID ? crypto.randomUUID()
                               : String(Date.now()) + "-" + Math.random().toString(36).slice(2, 10));
      localStorage.setItem(VKEY, vid);
    }
  } catch (_) { /* private mode: skip */ }

  function readBasket() {
    // Storage key matches basket.js (see var KEY).
    try {
      const raw = localStorage.getItem("primaxs.basket.v1") || "[]";
      const arr = JSON.parse(raw);
      return Array.isArray(arr) ? arr : [];
    } catch (_) { return []; }
  }

  function post(eventType, extraBasket) {
    const basket = extraBasket || readBasket();
    const payload = {
      event_type: eventType,
      basket: basket,
      basket_count: basket.reduce((n, i) => n + (Number(i.qty) || 1), 0),
      page_url: location.pathname + location.search,
      user_agent: (navigator.userAgent || "").slice(0, 400),
      visitor_id: vid,
    };
    // Use sendBeacon for click-then-navigate cases (WA / mailto) so the
    // request survives the page unload; fall back to keepalive fetch.
    const url = URL_ + "/rest/v1/events";
    const body = JSON.stringify(payload);
    const blob = new Blob([body], { type: "application/json" });
    // sendBeacon can't set custom headers, so use fetch(keepalive) which can
    // carry the apikey + auth headers Supabase requires.
    try {
      fetch(url, {
        method: "POST",
        headers: {
          "apikey": KEY,
          "Authorization": "Bearer " + KEY,
          "Content-Type": "application/json",
          "Prefer": "return=minimal",
        },
        body: body,
        keepalive: true,
        mode: "cors",
      }).catch(function (e) { console.warn("[analytics]", e); });
    } catch (e) {
      // Very old browser: fall back to Beacon (works without headers because
      // the PostgREST endpoint accepts anonymous when RLS allows, but the
      // apikey header IS required, so this is best-effort only).
      try { navigator.sendBeacon(url, blob); } catch (_) {}
    }
  }

  // Expose so other scripts can log custom events if needed.
  window.primaxsAnalytics = { post: post, readBasket: readBasket };

  // --- Auto-instrumentation --------------------------------------------------
  // WhatsApp float button opens the WA modal.
  document.addEventListener("click", function (e) {
    // 1. WhatsApp float FAB — treated as "browsing the WA option"
    if (e.target.closest("#wa-fab")) {
      post("whatsapp_open");
      return;
    }
    // 2. WhatsApp SEND button inside the modal — actual send with basket
    if (e.target.closest("#wa-send-btn")) {
      post("whatsapp_send");
      return;
    }
  }, true);

  // 3. Enquiry form submit — the email quote path.
  const enq = document.getElementById("enq-form");
  if (enq) {
    enq.addEventListener("submit", function () { post("email_submit"); }, true);
  }
})();
