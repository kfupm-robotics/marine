# Pre-launch checklist

## Removing `noindex` (launch switch)

In [`_data/site.yml`](../_data/site.yml), change one line:

```yaml
prelaunch: false
```

This removes the `noindex` meta tag from every page and switches `robots.txt` to allow crawling. With `prelaunch: false` the build **fails** if any `[TO CONFIRM]` placeholder is still on the site.

## Before switching

- [ ] No `[TO CONFIRM]` or `[للتأكيد]` anywhere (the build enforces this)
- [ ] Marjan-R1: depth-rating basis confirmed; dimensions, mass, speed confirmed
- [ ] Glider: hardware status wording confirmed
- [ ] Fish robots, hyperspectral rig, three-camera system, simulation pages: evidence supplied, text approved, or the page removed from `_data/platforms.yml` and `_quarto.yml`
- [ ] Contact email set in `_data/site.yml`
- [ ] Real media replaces every `MEDIA PLACEHOLDER`, with alt text and captions; renders labelled as renders
- [ ] Hero video 10 MB or less, muted, with a still fallback
- [ ] People profiles complete or hidden; photos with consent
- [ ] Publications: DOIs and venues verified
- [ ] Arabic pages reviewed by a native speaker; terms table approved
- [ ] Confidentiality review: no client, partner, budget, schedule, phone number or internal figure; `git log --all --name-only` shows no reference files
- [ ] Branch protection set (see BRANCH_PROTECTION.md)
- [ ] `python scripts/check_site.py` passes
- [ ] Accessibility: keyboard-only pass, contrast in light and dark, and an automated check (for example `npx pa11y-ci` or the axe browser extension) on Home, Platforms, Marjan-R1, Applications, Publications and the Arabic pages
- [ ] Mobile check at 360 px width
- [ ] PI and Co-PI written approval to launch
