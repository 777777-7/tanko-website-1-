// =============================================================================
// Primaxs sales dashboard — /sales/
// - Supabase email/password login (session persists in localStorage forever
//   until the refresh token is invalidated).
// - Monthly calendar: WhatsApp + email counts per Malaysia-day.
// - Click a day: full event list with basket line-items and MY time.
// =============================================================================
(function () {
  if (!window.supabase || !window.SUPABASE_URL) {
    console.error("[sales] supabase SDK or config missing");
    return;
  }
  const client = window.supabase.createClient(
    window.SUPABASE_URL,
    window.SUPABASE_KEY,
    {
      auth: {
        persistSession: true,       // localStorage — survives browser restart
        autoRefreshToken: true,     // rotate access token before it expires
        detectSessionInUrl: false,  // we do not use magic-link callbacks
      },
    }
  );

  const $ = (id) => document.getElementById(id);
  const authBox = $("sales-auth");
  const dashBox = $("sales-dash");

  // ---------- Malaysia-date helpers -----------------------------------------
  const MY_TZ = "Asia/Kuala_Lumpur";
  const dfDay = new Intl.DateTimeFormat("en-CA", { timeZone: MY_TZ, year: "numeric", month: "2-digit", day: "2-digit" });
  const dfTime = new Intl.DateTimeFormat("en-GB", { timeZone: MY_TZ, hour: "2-digit", minute: "2-digit", hour12: false });
  const dfLong = new Intl.DateTimeFormat("en-GB", { timeZone: MY_TZ, weekday: "long", day: "numeric", month: "long", year: "numeric" });

  function myDayKey(iso) {
    // Returns 'YYYY-MM-DD' in Malaysia time.
    return dfDay.format(new Date(iso));
  }
  function myTime(iso) { return dfTime.format(new Date(iso)); }
  function myLong(dayKey) {
    // dayKey is YYYY-MM-DD; parse as noon to avoid TZ edge cases
    return dfLong.format(new Date(dayKey + "T12:00:00+08:00"));
  }
  function monthLabel(year, month0) {
    return new Intl.DateTimeFormat("en-GB", { timeZone: MY_TZ, month: "long", year: "numeric" })
      .format(new Date(year, month0, 15));
  }
  function pad(n) { return n < 10 ? "0" + n : "" + n; }

  // ---------- state ----------------------------------------------------------
  let viewYear, viewMonth0;           // month currently shown (0-indexed)
  let events = [];                    // events for the visible month
  let byDay = new Map();              // 'YYYY-MM-DD' -> events[]
  let activeDay = null;

  // ---------- auth flow ------------------------------------------------------
  async function refreshUI() {
    const { data: { session } } = await client.auth.getSession();
    if (session && session.user && session.user.email === window.OWNER_EMAIL) {
      authBox.hidden = true;
      dashBox.hidden = false;
      const now = new Date();
      viewYear = Number(new Intl.DateTimeFormat("en-CA", { timeZone: MY_TZ, year: "numeric" }).format(now));
      viewMonth0 = Number(new Intl.DateTimeFormat("en-CA", { timeZone: MY_TZ, month: "2-digit" }).format(now)) - 1;
      await loadMonth();
    } else {
      dashBox.hidden = true;
      authBox.hidden = false;
    }
  }

  $("sales-login-btn").addEventListener("click", async function () {
    const email = $("sales-email").value.trim();
    const pw = $("sales-pw").value;
    const err = $("sales-error");
    err.textContent = "";
    if (!email || !pw) { err.textContent = "Enter email and password."; return; }
    if (email !== window.OWNER_EMAIL) {
      err.textContent = "Only the registered owner account can access this page.";
      return;
    }
    $("sales-login-btn").disabled = true;
    const { error } = await client.auth.signInWithPassword({ email: email, password: pw });
    $("sales-login-btn").disabled = false;
    if (error) { err.textContent = error.message || "Sign-in failed."; return; }
    await refreshUI();
  });

  $("sales-logout").addEventListener("click", async function () {
    await client.auth.signOut();
    await refreshUI();
  });

  // ---------- data loading ---------------------------------------------------
  async function loadMonth() {
    $("sales-month-label").textContent = monthLabel(viewYear, viewMonth0);
    $("sales-calendar").innerHTML = '<div class="sales-cal-loading" style="grid-column:1 / -1;padding:3rem;text-align:center;color:var(--ink-muted);">Loading…</div>';
    // We store occurred_at as UTC; convert the MY month bounds to UTC ISO.
    // MY = UTC+8, so 00:00 MY on the 1st == the prior day 16:00 UTC.
    const start = new Date(Date.UTC(viewYear, viewMonth0, 1, -8, 0, 0));
    const end   = new Date(Date.UTC(viewYear, viewMonth0 + 1, 1, -8, 0, 0));
    const { data, error } = await client
      .from("events")
      .select("id, occurred_at, event_type, basket, basket_count, page_url")
      .gte("occurred_at", start.toISOString())
      .lt("occurred_at",  end.toISOString())
      .order("occurred_at", { ascending: false });
    if (error) {
      $("sales-calendar").innerHTML = '<div style="grid-column:1 / -1;padding:1rem;color:var(--accent);">Load error: ' + error.message + '</div>';
      return;
    }
    events = data || [];
    byDay = new Map();
    for (const e of events) {
      const k = myDayKey(e.occurred_at);
      if (!byDay.has(k)) byDay.set(k, []);
      byDay.get(k).push(e);
    }
    renderCalendar();
    renderSummary();
  }

  function renderSummary() {
    const wa = events.filter(e => e.event_type === "whatsapp_open" || e.event_type === "whatsapp_send").length;
    const em = events.filter(e => e.event_type === "email_submit").length;
    $("sales-summary").textContent = `${events.length} event${events.length===1?"":"s"} this month · ${wa} WhatsApp · ${em} email`;
  }

  function renderCalendar() {
    const cal = $("sales-calendar");
    cal.innerHTML = "";
    // weekday headings
    ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"].forEach(d => {
      const h = document.createElement("div");
      h.className = "sales-cal-head";
      h.textContent = d;
      cal.appendChild(h);
    });

    // First day of the month + how many days
    const firstDow = (new Date(viewYear, viewMonth0, 1).getDay() + 6) % 7; // Mon = 0
    const daysInMonth = new Date(viewYear, viewMonth0 + 1, 0).getDate();
    const todayKey = myDayKey(new Date());

    for (let i = 0; i < firstDow; i++) {
      const cell = document.createElement("div");
      cell.className = "sales-cal-cell empty";
      cal.appendChild(cell);
    }
    for (let d = 1; d <= daysInMonth; d++) {
      const key = `${viewYear}-${pad(viewMonth0 + 1)}-${pad(d)}`;
      const list = byDay.get(key) || [];
      const wa = list.filter(e => e.event_type === "whatsapp_open" || e.event_type === "whatsapp_send").length;
      const em = list.filter(e => e.event_type === "email_submit").length;
      const cell = document.createElement("div");
      cell.className = "sales-cal-cell" + (key === todayKey ? " today" : "") + (key === activeDay ? " active" : "");
      cell.setAttribute("data-day", key);
      cell.setAttribute("role", "gridcell");
      cell.innerHTML =
        `<div class="sales-cal-date">${d}</div>` +
        `<div class="sales-cal-badges">` +
        (wa ? `<span class="sales-badge wa" title="${wa} WhatsApp events">📱 ${wa}</span>` : "") +
        (em ? `<span class="sales-badge mail" title="${em} email quote submissions">✉ ${em}</span>` : "") +
        `</div>`;
      cell.addEventListener("click", () => openDay(key));
      cal.appendChild(cell);
    }
  }

  function openDay(key) {
    activeDay = key;
    document.querySelectorAll(".sales-cal-cell").forEach(c => {
      c.classList.toggle("active", c.getAttribute("data-day") === key);
    });
    const drill = $("sales-drilldown");
    const body = $("sales-drill-body");
    $("sales-drill-h").textContent = myLong(key);
    const list = (byDay.get(key) || []).slice().sort(
      (a, b) => new Date(a.occurred_at) - new Date(b.occurred_at)
    );
    if (list.length === 0) {
      body.innerHTML = '<p style="color:var(--ink-muted);margin:0;">No sales events on this day.</p>';
    } else {
      body.innerHTML =
        `<table><thead><tr><th>Time (MY)</th><th>Channel</th><th>Basket</th></tr></thead><tbody>` +
        list.map(e => {
          const chan =
            e.event_type === "whatsapp_open" ? '<span class="sales-badge wa">📱 WhatsApp opened</span>' :
            e.event_type === "whatsapp_send" ? '<span class="sales-badge wa">📱 WhatsApp sent</span>' :
                                               '<span class="sales-badge mail">✉ Email submitted</span>';
          const basket = Array.isArray(e.basket) ? e.basket : [];
          const bhtml = basket.length
            ? `<ul class="basket-mini" style="margin:.15rem 0 0;padding:0;list-style:none;">${
                basket.map(item => `<li>${(item.qty || 1)} × <strong>${escape(item.sku || "")}</strong> ${escape(item.name || "")}</li>`).join("")
              }</ul>`
            : `<span class="basket-mini">(basket was empty)</span>`;
          const pg = e.page_url ? `<div class="basket-mini" style="opacity:.7;">from ${escape(e.page_url)}</div>` : "";
          return `<tr><td>${myTime(e.occurred_at)}</td><td>${chan}</td><td>${bhtml}${pg}</td></tr>`;
        }).join("") +
        `</tbody></table>`;
    }
    drill.hidden = false;
    drill.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function escape(s) {
    return String(s || "").replace(/[&<>"']/g, c =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  $("sales-prev").addEventListener("click", () => { viewMonth0--; if (viewMonth0 < 0) { viewMonth0 = 11; viewYear--; } activeDay=null; $("sales-drilldown").hidden=true; loadMonth(); });
  $("sales-next").addEventListener("click", () => { viewMonth0++; if (viewMonth0 > 11) { viewMonth0 = 0; viewYear++; } activeDay=null; $("sales-drilldown").hidden=true; loadMonth(); });
  $("sales-today").addEventListener("click", () => {
    const now = new Date();
    viewYear = Number(new Intl.DateTimeFormat("en-CA", { timeZone: MY_TZ, year: "numeric" }).format(now));
    viewMonth0 = Number(new Intl.DateTimeFormat("en-CA", { timeZone: MY_TZ, month: "2-digit" }).format(now)) - 1;
    activeDay = null; $("sales-drilldown").hidden = true; loadMonth();
  });
  $("sales-drill-close").addEventListener("click", () => {
    $("sales-drilldown").hidden = true;
    activeDay = null;
    document.querySelectorAll(".sales-cal-cell.active").forEach(c => c.classList.remove("active"));
  });

  refreshUI();
})();
