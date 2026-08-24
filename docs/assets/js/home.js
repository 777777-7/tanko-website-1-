/* Primaxs homepage — hero slide cross-fade + auto-advance + scroll-reveal.
   Vanilla JS, respects prefers-reduced-motion. */
(function () {
  var track = document.getElementById("hero-track");
  if (!track) return;
  var slides = track.querySelectorAll(".v4-slide, .hero-slide");
  var ticks = document.querySelectorAll(".v4-hero-ticks .v4-tick, .hero-ticks .hero-tick");
  var i = 0;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (slides.length) {
    function show(n) {
      n = ((n % slides.length) + slides.length) % slides.length;
      slides.forEach(function (s, idx) { s.classList.toggle("is-active", idx === n); });
      ticks.forEach(function (t, idx) { t.classList.toggle("is-active", idx === n); });
      i = n;
    }
    ticks.forEach(function (t) {
      t.addEventListener("click", function (e) {
        e.preventDefault();
        show(parseInt(t.getAttribute("data-goto"), 10) - 1);
        restart();
      });
    });
    var timer;
    function restart() {
      if (reduce) return;
      clearInterval(timer);
      timer = setInterval(function () { show(i + 1); }, 7000);
    }
    restart();
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) clearInterval(timer); else restart();
    });
  }

  // Scroll reveal via IntersectionObserver — lightweight, no library
  if (!reduce && "IntersectionObserver" in window) {
    var targets = document.querySelectorAll(".v4-head, .v4-cat, .v4-feat-card, .v4-ind-row, .v4-why, .v4-cta");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("in-view");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    // reveal immediately if reduced motion
    document.querySelectorAll(".v4-head, .v4-cat, .v4-feat-card, .v4-ind-row, .v4-why, .v4-cta").forEach(function (t) { t.classList.add("in-view"); });
  }
})();
