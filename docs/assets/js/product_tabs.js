(function () {
  var btns = document.querySelectorAll(".ptabs-btn[data-tab]");
  var panels = document.querySelectorAll(".ptab-panel[data-tab]");
  if (!btns.length || !panels.length) return;
  function show(tab) {
    var found = false;
    btns.forEach(function (b) {
      var on = b.getAttribute("data-tab") === tab;
      b.setAttribute("aria-selected", on ? "true" : "false");
      if (on) found = true;
    });
    panels.forEach(function (p) {
      p.setAttribute("data-active", p.getAttribute("data-tab") === tab ? "true" : "false");
    });
    return found;
  }
  btns.forEach(function (b) {
    b.addEventListener("click", function () {
      var t = b.getAttribute("data-tab");
      show(t);
      history.replaceState(null, "", "#" + t);
    });
  });
  var initial = (location.hash || "").replace(/^#/, "");
  if (!initial || !show(initial)) show(btns[0].getAttribute("data-tab"));
  window.addEventListener("hashchange", function () {
    var t = (location.hash || "").replace(/^#/, "");
    if (t) show(t);
  });
})();