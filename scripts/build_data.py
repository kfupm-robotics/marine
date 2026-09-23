"""Pre-render step: turn the files in _data/ into include fragments in _generated/.

Runs automatically before every `quarto render` / `quarto preview` (see _quarto.yml).
Needs PyYAML (pip install pyyaml). Everything written here is regenerated on each build,
so never edit _generated/ by hand.
"""
import html
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"
GEN = ROOT / "_generated"
GEN.mkdir(exist_ok=True)

THEMES = {
    "modelling-control": "Dynamic modelling and control",
    "state-estimation": "State estimation and system identification",
    "energy-aware-autonomy": "Energy-aware autonomy",
    "simulation-digital-twins": "Simulation and digital twins",
    "underwater-perception": "Underwater perception",
    "hyperspectral-sensing": "Hyperspectral sensing",
    "bioinspired-locomotion": "Bioinspired locomotion",
}
TYPES = {"article": "Journal", "inproceedings": "Conference"}
GROUPS = [
    ("leadership", "Leadership"),
    ("postdoc", "Postdoctoral researchers"),
    ("phd", "PhD students"),
    ("ms", "MS students"),
    ("engineers", "Research engineers"),
    ("alumni", "Alumni"),
]


def load(name):
    with open(DATA / name, encoding="utf8") as f:
        return yaml.safe_load(f) or []


def esc(text):
    """Escape for HTML and highlight [TO CONFIRM ...] placeholders."""
    out = html.escape(str(text))
    return re.sub(r"(\[TO CONFIRM[^\]]*\])", r'<span class="tc">\1</span>', out)


def raw(block):
    return "```{=html}\n" + block + "\n```\n"


def write(name, text):
    (GEN / name).write_text(text, encoding="utf8")


site = load("site.yml")
platforms = load("platforms.yml")
people = load("people.yml")
news = load("news.yml")

# ---- pre-launch switch: noindex meta and robots.txt ----
prelaunch = bool(site.get("prelaunch", True))
write("head.html", '<meta name="robots" content="noindex, nofollow">\n' if prelaunch else "<!-- launched -->\n")
(ROOT / "robots.txt").write_text(
    "User-agent: *\nDisallow: /\n" if prelaunch else "User-agent: *\nAllow: /\n", encoding="utf8"
)

# ---- contact email (mailto only) ----
email = (site.get("contact_email") or "").strip()
write("email-link.md", f"[{email}](mailto:{email})" if email else "[TO CONFIRM contact email]")

# ---- platform spec blocks and cards ----
for p in platforms:
    rows = "".join(
        f'<tr><th scope="row">{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in p["spec"].items()
    )
    write(f"spec-{p['id']}.md", raw(f'<table class="spec"><caption class="visually-hidden">Specification of {esc(p["title"])}</caption><tbody>{rows}</tbody></table>'))


def cards(group, prefix):
    items = []
    for p in platforms:
        if p["group"] != group:
            continue
        items.append(
            f'<a class="card" href="{prefix}{p["page"]}"><span class="status">{esc(p["status"])}</span>'
            f'<h3>{esc(p["title"])}</h3><p>{esc(p["card"])}</p></a>'
        )
    return raw('<div class="cards">' + "".join(items) + "</div>")


for group in ("vehicle", "testbed"):
    write(f"cards-{group}.md", cards(group, ""))
    write(f"cards-{group}-sub.md", cards(group, "../"))

# ---- people ----
def person_card(p):
    name = p.get("name") or "[TO CONFIRM name]"
    if p.get("photo"):
        img = f'<img src="{html.escape(p["photo"])}" alt="Portrait of {html.escape(name)}" loading="lazy" width="120" height="120">'
    else:
        initials = "".join(w[0] for w in name.split() if w[0].isalpha())[:2] or "?"
        img = f'<div class="avatar" aria-hidden="true">{html.escape(initials)}</div>'
    links = [
        f'<a href="{html.escape(u)}">{label}</a>'
        for key, label in (("scholar", "Google Scholar"), ("orcid", "ORCID"), ("linkedin", "LinkedIn"), ("github", "GitHub"))
        if (u := (p.get("links") or {}).get(key))
    ]
    extra = ""
    if p.get("dept"):
        extra += f'<p class="dept">{esc(p["dept"])}</p>'
    if p.get("years") or p.get("now"):
        extra += f'<p class="dept">{esc(p.get("years", ""))} {esc(p.get("now", ""))}</p>'
    if p.get("focus"):
        extra += f'<p><strong>Research focus.</strong> {esc(p["focus"])}</p>'
    if p.get("bio"):
        extra += f'<p>{esc(p["bio"])}</p>'
    if links:
        extra += '<p class="links">' + " · ".join(links) + "</p>"
    return f'<article class="person">{img}<div><h3>{esc(name)}</h3><p class="role">{esc(p.get("role", ""))}</p>{extra}</div></article>'


parts = []
for key, heading in GROUPS:
    members = [p for p in people if p.get("group") == key and not p.get("hidden")]
    if members:
        parts.append(f'<h2>{heading}</h2><div class="people">' + "".join(person_card(p) for p in members) + "</div>")
write("people.md", raw("".join(parts)) if parts else "")

# ---- news ----
def news_item(n):
    link = f'<p><a href="{html.escape(n["link"])}">Read more</a></p>' if n.get("link") else ""
    tag = f'<span class="status">{esc(n["tag"])}</span>' if n.get("tag") else ""
    return (
        f'<article class="card news-item">{tag}<time datetime="{n["date"]}">{n["date"]}</time>'
        f'<h3>{esc(n["title"])}</h3><p>{esc(n.get("summary", ""))}</p>{link}</article>'
    )


news = sorted(news, key=lambda n: str(n["date"]), reverse=True)
write("news-list.md", raw('<div class="cards">' + "".join(news_item(n) for n in news) + "</div>") if news else "No news items yet.\n")
write("news-latest.md", raw('<div class="cards">' + "".join(news_item(n) for n in news[:3]) + "</div>") if news else "")

# ---- publications from BibTeX ----
def parse_bib(text):
    text = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("%"))
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        i, fields = m.end(), {}
        while i < len(text):
            fm = re.compile(r"\s*(\w+)\s*=\s*").match(text, i)
            if not fm:
                break
            i = fm.end()
            if text[i] == "{":
                depth, j = 1, i + 1
                while depth:
                    depth += {"{": 1, "}": -1}.get(text[j], 0)
                    j += 1
                value, i = text[i + 1 : j - 1], j
            elif text[i] == '"':
                j = text.index('"', i + 1)
                value, i = text[i + 1 : j], j + 1
            else:
                j = re.compile(r"[,}\s]").search(text, i).start()
                value, i = text[i:j], j
            fields[fm.group(1).lower()] = value.strip()
            cm = re.compile(r"\s*,?\s*").match(text, i)
            i = cm.end()
            if i < len(text) and text[i] == "}":
                break
        entries.append({"type": m.group(1).lower(), "key": m.group(2), **fields})
    return entries


def clean(s):
    return re.sub(r"\s+", " ", s.replace("{", "").replace("}", "").replace("\\&", "&")).strip()


def authors(s):
    names = []
    for a in re.split(r"\s+and\s+", clean(s)):
        if "," in a:
            last, first = [x.strip() for x in a.split(",", 1)]
            a = f"{first} {last}"
        names.append(a)
    return ", ".join(names)


bib = parse_bib((DATA / "publications.bib").read_text(encoding="utf8"))
bib.sort(key=lambda e: e.get("year", "0"), reverse=True)
years = sorted({e.get("year", "") for e in bib if e.get("year")}, reverse=True)
present_themes = {t.strip() for e in bib for t in e.get("theme", "").split(",") if t.strip()}
types_present = sorted({TYPES.get(e["type"], "Other") for e in bib})


def venue(e):
    v = clean(e.get("journal") or e.get("booktitle") or e.get("publisher") or "")
    detail = ""
    if e.get("volume"):
        detail += f", {clean(e['volume'])}"
        if e.get("number"):
            detail += f"({clean(e['number'])})"
    if e.get("pages"):
        detail += f", {clean(e['pages'])}"
    return f"<em>{html.escape(v)}</em>{html.escape(detail)}" if v else ""


def pub_item(e):
    themes = [t.strip() for t in e.get("theme", "").split(",") if t.strip()]
    links = []
    if e.get("doi"):
        links.append(f'<a href="https://doi.org/{html.escape(e["doi"])}">DOI</a>')
    for key, label in (("pdf", "PDF"), ("code", "Code"), ("dataset", "Dataset")):
        if e.get(key):
            links.append(f'<a href="{html.escape(e[key])}">{label}</a>')
    tags = "".join(f'<span class="tag">{html.escape(THEMES.get(t, t))}</span>' for t in themes)
    return (
        f'<li class="pub" data-year="{html.escape(e.get("year", ""))}" data-theme="{html.escape(" ".join(themes))}" '
        f'data-type="{TYPES.get(e["type"], "Other")}"><p class="pub-title">{html.escape(clean(e.get("title", "")))}</p>'
        f'<p class="pub-authors">{html.escape(authors(e.get("author", "")))}</p>'
        f'<p class="pub-venue">{venue(e)} ({html.escape(e.get("year", ""))})</p>'
        f'<p class="pub-links">{" · ".join(links)}</p><p class="pub-tags">{tags}</p></li>'
    )


def select(id_, label, options):
    opts = '<option value="">All</option>' + "".join(f'<option value="{html.escape(v)}">{html.escape(t)}</option>' for v, t in options)
    return f'<label for="{id_}">{label}</label><select id="{id_}">{opts}</select>'


filters = (
    '<div class="filters" role="search" aria-label="Filter publications">'
    + select("f-year", "Year", [(y, y) for y in years])
    + select("f-theme", "Theme", [(k, v) for k, v in THEMES.items() if k in present_themes])
    + select("f-type", "Type", [(t, t) for t in types_present])
    + '<span id="f-count" role="status" aria-live="polite"></span></div>'
)
script = """<script>
(function(){
  var items=[].slice.call(document.querySelectorAll('.pub')),
      y=document.getElementById('f-year'),t=document.getElementById('f-theme'),k=document.getElementById('f-type'),
      c=document.getElementById('f-count');
  function apply(){
    var n=0;
    items.forEach(function(li){
      var ok=(!y.value||li.dataset.year===y.value)&&(!t.value||li.dataset.theme.split(' ').indexOf(t.value)>-1)&&(!k.value||li.dataset.type===k.value);
      li.hidden=!ok; if(ok)n++;
    });
    c.textContent=n+' of '+items.length+' shown';
  }
  [y,t,k].forEach(function(s){s.addEventListener('change',apply)});
  apply();
})();
</script>"""
write("publications.md", raw(filters + '<ul class="pubs">' + "".join(pub_item(e) for e in bib) + "</ul>" + script) if bib else "No publications listed yet.\n")

print(f"build_data: prelaunch={prelaunch}, {len(platforms)} platforms, {len(people)} people entries, {len(news)} news, {len(bib)} publications")
sys.exit(0)
