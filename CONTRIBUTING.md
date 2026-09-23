# Contributing

This site is built from a few data files. You can update News, People and Publications by editing **one file in the GitHub web editor**. No software needed.

## Ground rules

- Only publish things that are true, finished and approved for public release.
- Never add confidential material: client or partner names, budgets, funding amounts, schedules, unpublished CAD, or internal documents. This repository and its full history are public.
- Do not state field deployment, sea trials, endurance, autonomy or commercial readiness unless the PI or Co-PI has confirmed it.
- Use American English. Short sentences. No hype words.
- Every image needs alt text.
- Never write `[TO CONFIRM]` in something you want to go live. It blocks launch on purpose.

## How to make any change

1. Open the file on GitHub and click the pencil icon (Edit).
2. Make the change, then choose **Create a new branch and start a pull request**.
3. A reviewer approves it and merges it. The site rebuilds in a few minutes.

`main` is protected: changes go through a pull request with one review.

## Add a news item

Edit [`_data/news.yml`](_data/news.yml). Add a block at the **top** of the list:

```yaml
- date: 2026-10-01
  title: "Short, factual headline"
  summary: "One or two sentences."
  link: "https://example.org"     # optional
  tag: "Demonstration"            # optional
```

If the file currently contains only `[]`, delete that line first. Keep the two-space indent exactly as shown.

## Add or update a person

Edit [`_data/people.yml`](_data/people.yml).

- To complete a placeholder profile, fill in the fields and change `hidden: true` to `hidden: false`.
- To add someone, copy an existing block. Set `group` to one of: `leadership`, `postdoc`, `phd`, `engineers`, `alumni`.
- Photo: upload a square JPEG (at least 400 px, under 300 KB) to `media/people/` and write `photo: "media/people/your-name.jpg"`.
- Links: Google Scholar, ORCID, LinkedIn, GitHub. Leave blank if none.
- Alumni: use `group: alumni` and add `years` and `now` (current position).

## Add a publication

Edit [`_data/publications.bib`](_data/publications.bib). Add a BibTeX entry:

```bibtex
@article{lastname2026short,
  author  = {Lastname, Firstname and Other, Person},
  title   = {Title of the paper},
  journal = {Journal Name},
  year    = {2026},
  doi     = {10.xxxx/xxxxx},
  theme   = {modelling-control},
  pdf     = {https://...},
  code    = {https://github.com/...}
}
```

- Use `@article` for journals and `@inproceedings` (with `booktitle`) for conferences.
- `theme` takes one or more of: `modelling-control`, `state-estimation`, `energy-aware-autonomy`, `simulation-digital-twins`, `underwater-perception`, `hyperspectral-sensing`, `bioinspired-locomotion` (comma-separated).
- `doi`, `pdf`, `code` and `dataset` are optional. Check every DOI before adding it.
- Wrap capitalized acronyms in braces: `{ROV}`, `{MIMO}`.

## Update a platform's specification

Edit [`_data/platforms.yml`](_data/platforms.yml). Update `Last updated` whenever you change a spec. If you cannot verify a value, write `[TO CONFIRM]`: the site stays private until it is resolved.

## Check your change

Open the pull request and wait for the **Build and publish** check. If it fails, click Details and read the message: it lists broken links, missing alt text and leftover placeholders.

## Preview locally (optional)

Install [Quarto](https://quarto.org) and Python with `pip install pyyaml`, then run `quarto preview`.
