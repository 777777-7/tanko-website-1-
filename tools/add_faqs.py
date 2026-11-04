# -*- coding: utf-8 -*-
"""Add FAQs to a docs/ page, visibly and in FAQPage JSON-LD, without touching
title, meta or URL. If the page already has a <div class="faq">, the questions are
appended to it and to its FAQPage; otherwise a new FAQ section is inserted before
`anchor` and a FAQPage node is added to the page's @graph.
Usage: python tools/add_faqs.py spec.json
spec.json: {"page": "docs/x/index.html", "heading": "...", "anchor": "<exact html>",
            "faqs": [["Question?", "Answer."], ...]}"""
import io, json, re, sys
spec = json.load(io.open(sys.argv[1], encoding="utf-8"))
p, faqs = spec["page"], spec["faqs"]
s = io.open(p, encoding="utf-8").read()
for q, _ in faqs:
    assert q not in s, f"already there: {q}"
items = "".join(f"      <details><summary>{q}</summary><p>{a}</p></details>\n" for q, a in faqs)
entities = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]

if '<div class="faq">' in s:
    i = s.index('<div class="faq">')
    j = s.index("</div>", i)
    s = s[:j] + items.lstrip(" ").rstrip("\n").replace("\n      ", "\n        ") + "\n    " + s[j:]
else:
    section = (f'<section class="section" style="padding-top:0;">\n  <div class="container">\n'
               f'    <h2>{spec["heading"]}</h2>\n    <div class="faq">\n{items}    </div>\n  </div>\n</section>\n\n')
    assert s.count(spec["anchor"]) == 1, "anchor must occur exactly once"
    s = s.replace(spec["anchor"], section + spec["anchor"])

done = False
blocks = list(re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S))
blocks.sort(key=lambda m: '"FAQPage"' not in m.group(2))  # a block that already has a FAQPage first
for m in blocks:
    d = json.loads(m.group(2))
    nodes = d.get("@graph", [d])
    faq = next((n for n in nodes if n.get("@type") == "FAQPage"), None)
    if faq is None and "@graph" not in d: continue
    if faq is None:
        d["@graph"].append({"@type": "FAQPage", "mainEntity": entities})
    else:
        faq["mainEntity"].extend(entities)
    s = s[:m.start(2)] + json.dumps(d, ensure_ascii=False) + s[m.end(2):]
    done = True
    break
assert done, "no ld+json @graph or FAQPage found"
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("ok", p, len(faqs), "FAQs")
