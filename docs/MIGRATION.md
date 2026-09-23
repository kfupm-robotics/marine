# Moving to a KFUPM subdomain

The site currently lives at `https://kfupm-robotics.github.io/marine/`. Links inside the site are relative, and the URL is set in one place (`_quarto.yml`), so the move needs a DNS record, a `CNAME` file and one config line.

## Steps

1. **Choose the hostname** with KFUPM IT, for example `marine-robotics.kfupm.edu.sa`.
2. **Ask KFUPM IT to create a DNS record**: a `CNAME` for that hostname pointing to `kfupm-robotics.github.io`.
3. **Add a `CNAME` file** at the project root containing only the hostname, and list it in `_quarto.yml` under `project: resources:` so it is published. Or set the domain in Settings → Pages → Custom domain. Do one of the two, not both differently.
4. **Change `site-url`** in `_quarto.yml` to `https://<hostname>`. Nothing else contains the URL.
5. **Merge to `main`.** The workflow republishes.
6. In **Settings → Pages**, confirm the custom domain, wait for the certificate check, then tick **Enforce HTTPS**.
7. **Verify**: open the site, run `python scripts/check_site.py`, check that the language switch, images and downloads work.
8. **Redirect**: after the move, the old `github.io` address redirects to the custom domain automatically.

## After the move

- `robots.txt` works at the domain root only. It is not honored under `/marine/`, so until then `noindex` is what keeps the site out of search.
- To launch, follow the pre-launch checklist.
- If a page or Arabic link breaks, search the repo for hard-coded `github.io`: there should be none.
