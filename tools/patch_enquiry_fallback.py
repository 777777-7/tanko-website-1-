# One-off: make the enquiry form fail honestly and hand the enquiry to WhatsApp/email
# when FormSubmit is unreachable (it returned HTTP 521 on 29 Oct 2026).
import re, sys
FALLBACK_FN = r'''
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
'''
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    assert 'onFailure' not in s, p
    # fetch with a 15s timeout and a real success check
    s, n1 = re.subn(
        r'fetch\(ajaxUrl, \{ method: "POST", headers: \{"Accept": "application/json"\}, body: fd \}\)\s*'
        r'\.then\(function \(r\) \{ return r\.ok \? r\.json\(\) : Promise\.reject\(r\); \}\)\s*'
        r'\.then\(function \(\) \{ onSuccess\(\); \}\)\s*'
        r'\.catch\(function \(\) \{.*?onSuccess\(\);[^\n]*\n\s*\}\);',
        '''var ctrl = window.AbortController ? new AbortController() : null;
      var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, 15000) : null;
      fetch(ajaxUrl, { method: "POST", headers: {"Accept": "application/json"}, body: fd, signal: ctrl ? ctrl.signal : undefined })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r); })
        .then(function (j) {
          if (j && String(j.success) === "false") throw j;
          onSuccess();
        })
        .catch(function () { onFailure(fd); })
        .then(function () { if (timer) clearTimeout(timer); });''',
        s, flags=re.S)
    i = s.index('  function onSuccess() {')
    s = s[:i] + FALLBACK_FN.lstrip('\n') + '\n' + s[i:]
    assert n1 == 1, (p, n1)
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('patched', p)
