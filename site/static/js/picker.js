/* Primaxs interactive variant picker — vanilla JS, no dependencies.
   Reads JSON from #picker-data:
   {
     base: "/",
     axes: [ {key, label, values:[...]} ],
     variants: [ {sku, values:{axis:val}, image, thumbs:[...], dims, material, color, load, url} ],
     defaultSku: "..."
   }
*/
(function () {
  var el = document.getElementById("picker-data");
  if (!el) return;
  var data;
  try { data = JSON.parse(el.textContent); } catch (e) { return; }
  var base = data.base || "/";
  var axes = data.axes || [];
  var variants = data.variants || [];
  if (!variants.length) return;

  var bySku = {};
  variants.forEach(function (v) { bySku[v.sku] = v; });

  var current = bySku[data.defaultSku] || variants[0];
  var selection = Object.assign({}, current.values);

  var optContainer = document.getElementById("opt-container");
  var specList = document.getElementById("product-specs");
  var stageImg = document.getElementById("stage-img");
  var modelVal = document.getElementById("model-val");
  var quoteLink = document.getElementById("quote-link");           // legacy — may be null
  var detailsLink = document.getElementById("details-link");
  var addBtn = document.getElementById("add-to-basket");            // basket-flow replacement
  var thumbsWrap = document.getElementById("stage-thumbs");

  // Find a variant exactly matching a full selection object
  function findExact(sel) {
    for (var i = 0; i < variants.length; i++) {
      var ok = true;
      for (var k in sel) {
        if (String(variants[i].values[k]) !== String(sel[k])) { ok = false; break; }
      }
      if (ok) return variants[i];
    }
    return null;
  }

  // Does any variant satisfy current selection on all axes EXCEPT `axisKey`,
  // while having axisKey === value?
  function isAvailable(axisKey, value) {
    for (var i = 0; i < variants.length; i++) {
      var v = variants[i];
      if (String(v.values[axisKey]) !== String(value)) continue;
      var ok = true;
      for (var a = 0; a < axes.length; a++) {
        var k = axes[a].key;
        if (k === axisKey) continue;
        if (String(v.values[k]) !== String(selection[k])) { ok = false; break; }
      }
      if (ok) return true;
    }
    return false;
  }

  function chooseValue(axisKey, value) {
    var trial = Object.assign({}, selection);
    trial[axisKey] = value;
    var match = findExact(trial);
    if (!match) {
      // adopt-nearest: first variant with this axis=value, take its full combo
      for (var i = 0; i < variants.length; i++) {
        if (String(variants[i].values[axisKey]) === String(value)) { match = variants[i]; break; }
      }
    }
    if (!match) return;
    current = match;
    selection = Object.assign({}, match.values);
    render();
  }

  function renderOptions() {
    optContainer.innerHTML = "";
    axes.forEach(function (axis) {
      var group = document.createElement("div");
      group.className = "opt-group";

      var head = document.createElement("div");
      head.className = "opt-head";
      head.innerHTML = '<span class="opt-label">' + axis.label + '</span>' +
                       '<span class="opt-chosen">' + (selection[axis.key] || "") + '</span>';
      group.appendChild(head);

      var choices = document.createElement("div");
      choices.className = "opt-choices";
      axis.values.forEach(function (val) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "opt-choice";
        b.textContent = val;
        b.setAttribute("aria-pressed", String(selection[axis.key]) === String(val) ? "true" : "false");
        b.setAttribute("data-available", isAvailable(axis.key, val) ? "true" : "false");
        b.addEventListener("click", function () { chooseValue(axis.key, val); });
        choices.appendChild(b);
      });
      group.appendChild(choices);
      optContainer.appendChild(group);
    });
  }

  function renderSpecs() {
    var rows = [];
    if (current.dims) rows.push(["Dimensions", current.dims]);
    if (current.material) rows.push(["Material / Top", current.material]);
    if (current.color) rows.push(["Colour", current.color]);
    if (current.load) rows.push(["Load capacity", current.load]);
    // any axis not already covered by the fixed rows above
    var covered = { "Top": 1, "Material": 1, "Color": 1, "Colour": 1, "__color__": 1, "__model__": 1 };
    axes.forEach(function (axis) {
      if (covered[axis.key]) return;
      var v = current.values[axis.key];
      if (v && String(v).toLowerCase() !== "none") rows.push([axis.label, v]);
    });
    specList.innerHTML = rows.map(function (r) {
      return '<li><span class="k">' + r[0] + '</span><span class="v">' + r[1] + '</span></li>';
    }).join("");
  }

  function currentImages() {
    // Pick attribute-specific images when the current selection matches a
    // parenthesised token in one of the variant's image filenames.
    // Falls back to the variant's regular thumbs, then to current.image.
    var ai = current.attr_images || {};
    var picked = [];
    Object.keys(selection).forEach(function (k) {
      var v = String(selection[k] || "").toLowerCase();
      if (v && ai[v]) picked = picked.concat(ai[v]);
    });
    // de-dup in order
    var seen = {}, out = [];
    picked.forEach(function (p) { if (!seen[p]) { seen[p] = 1; out.push(p); } });
    if (out.length) return out;
    if (current.thumbs && current.thumbs.length) return current.thumbs.slice();
    return current.image ? [current.image] : [];
  }

  function renderMedia() {
    var imgs = currentImages();
    if (imgs.length) stageImg.src = base + imgs[0];
    stageImg.alt = data.family + " — " + current.sku;
    if (thumbsWrap) {
      thumbsWrap.innerHTML = "";
      var thumbs = imgs;
      thumbs.forEach(function (t, i) {
        var btn = document.createElement("button");
        btn.type = "button";
        if (i === 0) btn.className = "active";
        btn.setAttribute("data-src", base + t);
        btn.innerHTML = '<img src="' + base + t + '" alt="' + current.sku + ' view ' + (i + 1) + '">';
        btn.addEventListener("click", function () {
          stageImg.src = base + t;
          Array.prototype.forEach.call(thumbsWrap.children, function (c) { c.className = ""; });
          btn.className = "active";
        });
        thumbsWrap.appendChild(btn);
      });
      thumbsWrap.style.display = thumbs.length > 1 ? "flex" : "none";
    }
  }

  function displaySku() {
    // Build the SKU string the customer sees + we save to basket. Append the
    // material/colour attribute so tanko-shared SKUs (RA-6091 both tops) are
    // differentiable in quote emails: RA-6091(Wood) vs RA-6091(Stainless steel).
    var suffixKeys = ["Top", "Material", "Color", "Colour", "__color__"];
    var pieces = [];
    suffixKeys.forEach(function (k) {
      var v = selection[k];
      if (v && String(v).toLowerCase() !== "none" && pieces.indexOf(v) < 0) {
        pieces.push(v);
      }
    });
    return pieces.length ? current.sku + "(" + pieces.join(", ") + ")" : current.sku;
  }

  function render() {
    var dsku = displaySku();
    if (modelVal) modelVal.textContent = dsku;
    if (quoteLink) quoteLink.href = base + "enquiry/?sku=" + encodeURIComponent(dsku);
    if (addBtn) {
      addBtn.setAttribute("data-sku", dsku);
      var imgs = currentImages();
      var pickImg = imgs[0] || current.image;
      if (pickImg) addBtn.setAttribute("data-image", pickImg);
      if (current.url) addBtn.setAttribute("data-url", current.url);
      addBtn.setAttribute("data-name",
        (data.family || "") + " — " + dsku);
    }
    if (detailsLink) {
      if (current.url) { detailsLink.href = base + current.url; detailsLink.style.display = ""; }
      else { detailsLink.style.display = "none"; }
    }
    renderOptions();
    renderSpecs();
    renderMedia();
  }

  render();
})();
