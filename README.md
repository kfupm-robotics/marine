# KFUPM Marine Robotics Lab website

Source for the KFUPM Marine Robotics Lab site (IRC for Intelligent Manufacturing and Robotics, KFUPM). Built with [Quarto](https://quarto.org), deployed to GitHub Pages by GitHub Actions.

**This repository is public. Never commit confidential material.** See [CONTRIBUTING.md](CONTRIBUTING.md).

## Layout

| Path | Purpose |
|---|---|
| `_quarto.yml` | Site config. `site-url` is set here and nowhere else |
| `_data/` | Content as data: `platforms.yml`, `people.yml`, `news.yml`, `publications.bib`, `site.yml` |
| `scripts/build_data.py` | Runs before each render and turns `_data/` into page fragments in `_generated/` |
| `scripts/check_site.py` | Link, alt-text, size, placeholder and confidentiality checks |
| `*.qmd`, `platforms/`, `ar/` | Pages (`ar/` holds the Arabic pages, right-to-left) |
| `theme/` | Design tokens and styles (direction B, light and dark) |
| `media/` | Images and short video (files under 10 MB where possible, never over 50 MB) |
| `docs/` | Pre-launch checklist, migration guide, branch protection, media guide |
| `design/` | Static design mockups (not part of the site) |

## Build locally

```bash
pip install pyyaml
quarto render        # or: quarto preview
python scripts/check_site.py
```

## Deployment

Every push to `main` runs `.github/workflows/publish.yml`: render, run checks, publish to the `gh-pages` branch. Pull requests build and check but do not deploy. In the repository settings, set Pages to deploy from the `gh-pages` branch.

## Pre-launch

While `prelaunch: true` in `_data/site.yml`, every page carries `noindex` and `robots.txt` disallows all crawling. See [docs/PRELAUNCH_CHECKLIST.md](docs/PRELAUNCH_CHECKLIST.md).

## More

- [CONTRIBUTING.md](CONTRIBUTING.md): how students add news, people and publications
- [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md)
- [docs/MIGRATION.md](docs/MIGRATION.md): moving to a KFUPM subdomain
- [docs/MEDIA.md](docs/MEDIA.md): video and image guidance
