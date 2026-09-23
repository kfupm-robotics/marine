"""Quality checks on the rendered site (_site/) and the repository. Run after `quarto render`.

Checks:
  1. internal links and images resolve to files
  2. every <img> has an alt attribute
  3. every page has <html lang> and a <title>
  4. no file in the repo or site is larger than 50 MB; warns above 10 MB
  5. nothing from the private reference folders is tracked or in the site
  6. no "[TO CONFIRM" or "[للتأكيد" placeholder on the site once prelaunch is false
Exit code 1 on any error.
"""
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
errors, warnings = [], []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.imgs_missing_alt, self.lang, self.title, self._in_title = [], 0, None, "", False
        self.h1s = []
        self._in_h1 = False
        self.nav_texts = []
        self._in_nav = False
        self._in_nav_container = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self._in_title = True
        if tag == "h1":
            self._in_h1 = True
        if tag == "nav":
            self._in_nav_container = True
        if tag == "a" and self._in_nav_container:
            self._in_nav = True
        if tag == "img" and "alt" not in a:
            self.imgs_missing_alt += 1
        for key in ("href", "src"):
            if key in a and a[key]:
                self.refs.append(a[key])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "h1":
            self._in_h1 = False
        if tag == "a" and self._in_nav:
            self._in_nav = False
        if tag == "nav":
            self._in_nav_container = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_h1:
            self.h1s.append(data.strip())
        if self._in_nav and self._in_nav_container:
            self.nav_texts.append(data.strip().lower())


if not SITE.exists():
    sys.exit("_site/ not found. Run `quarto render` first.")

site_cfg = yaml.safe_load((ROOT / "_data" / "site.yml").read_text(encoding="utf8"))
prelaunch = bool(site_cfg.get("prelaunch", True))

for page in SITE.rglob("*.html"):
    rel = page.relative_to(SITE)
    text = page.read_text(encoding="utf8")
    p = Page()
    p.feed(text)
    if not p.lang:
        errors.append(f"{rel}: missing <html lang>")
    if not p.title.strip():
        errors.append(f"{rel}: missing <title>")
    if p.imgs_missing_alt:
        errors.append(f"{rel}: {p.imgs_missing_alt} <img> without alt")
    for ref in p.refs:
        u = urlparse(ref)
        if u.scheme or ref.startswith(("#", "mailto:", "//", "data:")):
            continue
        target = (page.parent / unquote(u.path)).resolve() if u.path else page
        if target.is_dir():
            target = target / "index.html"
        if u.path and not target.exists():
            errors.append(f"{rel}: broken link {ref}")
    if not prelaunch and re.search(r"\[TO CONFIRM|\[للتأكيد", text):
        errors.append(f"{rel}: contains a [TO CONFIRM] placeholder, which must not be live")
    if prelaunch and 'content="noindex' not in text:
        errors.append(f"{rel}: prelaunch is on but noindex meta is missing")
    if not prelaunch and 'content="noindex' in text:
        errors.append(f"{rel}: prelaunch is off but noindex meta is still present")
    if len([h for h in p.h1s if h]) > 1:
        errors.append(f"{rel}: multiple <h1> tags found: {p.h1s}")
    if any("platforms" in t for t in p.nav_texts):
        errors.append(f"{rel}: 'Platforms' found in navbar text")

# ---- file sizes: only files git actually tracks (or is about to), plus the built site.
# A large file sitting untracked in the working tree (e.g. a raw video draft) is not a repo-size
# problem until it's added, so we check `git ls-files` rather than walking the whole directory.
try:
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
except (OSError, subprocess.CalledProcessError):
    tracked = []
    warnings.append("git not available: skipped tracked-files checks")

for rel in tracked:
    f = ROOT / rel
    if f.is_file():
        mb = f.stat().st_size / 1e6
        if mb > 50:
            errors.append(f"{rel}: {mb:.1f} MB exceeds 50 MB limit")
        elif mb > 10:
            warnings.append(f"{rel}: {mb:.1f} MB (target: 10 MB or less)")
    if rel.startswith(("privite-references/", "privite_references/", "private-notes/")) or rel.lower().endswith(".pptx"):
        errors.append(f"{rel}: confidential file is tracked by git")

for f in SITE.rglob("*"):
    if f.is_file():
        mb = f.stat().st_size / 1e6
        if mb > 50:
            errors.append(f"_site/{f.relative_to(SITE)}: {mb:.1f} MB exceeds 50 MB limit")
for bad in ("privite-references", "privite_references", "private-notes"):
    if (SITE / bad).exists():
        errors.append(f"_site/{bad} exists")

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"check_site: {len(errors)} error(s), {len(warnings)} warning(s), prelaunch={prelaunch}")
sys.exit(1 if errors else 0)
