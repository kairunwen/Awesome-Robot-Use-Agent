# Contributing

Resources, corrections, broken-link reports, and website improvements are welcome.

**Just suggesting something?** [Open an issue](https://github.com/kairunwen/Awesome-Robot-Use-Agent/issues) with its **name, official link, and one sentence about its relevance**. No coding required.

**Making a pull request?** Fork the repository and follow these four steps.

## 1. Choose a section

We collect robot-use agents and resources that help build or evaluate them. Preprints and demos are welcome; there is no minimum star count.

| Section | Add here |
| --- | --- |
| **Articles** | Research blogs, introductions, and perspectives. |
| **Papers** | Surveys, methods, datasets, benchmark papers, and relevant self-improvement research. |
| **Projects → Systems & Frameworks** | Agent systems and robot integration frameworks. |
| **Projects → Environment & Sandbox** | Simulators and environments for robot interaction. |
| **Projects → Tools & Utilities** | Robot-specific perception, planning, control, and integration tools. |
| **Projects → Social Demos** | Original real-robot, simulation, or perception demonstrations. |
| **Benchmarks** | Evaluation suites, scoring, and limitations. |

Check for duplicates. Keep a paper and its code together; cross-link related demos or benchmarks. Explain the robot-use connection for supporting models/datasets. General dependencies such as PyTorch or Open3D do not need standalone entries.

## 2. Edit the README

**Copy a nearby row in the same section of [README.md](README.md).** Papers use three columns; Benchmarks use four. Social Demos use a three-column gallery (fill the existing last row before starting another; only the final row may have fewer than three cards): copy a `demo-gallery-card`, preserving its preview, name/date, environment/tasks, links, and collapsible description. Preserve its HTML structure, anchors, and `layout-*` classes.

- **Name and summary:** Official name plus one short English sentence describing what it does.
- **Date and type:** Below the name, use the first release date and verified venue/year, e.g. `2024-10-30 · ICLR 2025`, `2026-05-28 · ArXiv 2026`, or `2026-09-10 · Research Blog 2026`. Use `YYYY-MM-DD`, or `YYYY-MM` if only the month is known. Never guess acceptance or dates. Keep Papers newest-first within each subsection and Benchmarks newest-first. Social Demo dates use UTC+8.
- **Links and previews:** Use official sources and descriptive image alt text. Update both the destination and badge URLs. Give each available Paper, Project, Code, Data, and Models link its own visible badge; a thumbnail link is not enough. Check the paper’s first-page links/footnotes and the repository’s About homepage as well as its README. Order badges as Paper → Project → Code / Stars → Data → Models → other links, omitting unavailable items. Keep badge labels descriptive—the website reads them. For gallery badges, keep the full environment and task text in `alt`; the first task badge starts with `Task: `. Code badges display live stars. Preserve original post/video links for demos. Keep one environment badge, one main task badge, and primary links in Post / RedNote → Video → Code order (at most five badges total). Put additional tasks and secondary links in Details as plain text. Use one Details fold per demo; keep supplementary context and limitations in `.demo-notes`, without repeating badges or adding review logs.
- **Notes:** Put additional setup, evidence, and limitations in `<details class="entry-notes">`. Benchmarks use **Evaluation notes**, without repeating the summary or Badge links. Distinguish real robots from simulation, released code from planned releases, and progress scores from success rates.

Missing a date or suitable preview? Flag it in the PR so a maintainer can help.

## 3. Keep the website in sync

**The website reads README.md—do not add the same resource twice.**

| Change | Edit |
| --- | --- |
| Resource content and links | [README.md](README.md) |
| Paper/article/benchmark dates, authors, institutions, or venue | [website/metadata.json](website/metadata.json): use the source URL as the key and include evidence links. |
| Website paper/article covers | [website/previews.json](website/previews.json) and `website/previews/`; see [cover instructions](website/README.md#paper-and-article-previews). |
| Website design or behavior | `website/style.css`, `website/template.html`, or `website/app.js`. Parsing/rendering lives in `website/build.py`. |

Copy nearby metadata records. Edit source files, **not `website/dist/`**. Stars and citations update automatically; local contributions need no API keys.

## 4. Check and open a PR

For new entries or website changes, run from the repository root:

```sh
python3 -m venv website/.venv
website/.venv/bin/pip install -r website/requirements.txt
website/.venv/bin/python -m unittest discover -s website -p 'test_*.py'
git diff --check
python3 -m http.server 8000 --directory website/dist
```

Tests build the website. Open [localhost:8000](http://localhost:8000) and check the rendered README on GitHub. Local builds do not publish anything.

- Check changed images, badges, links, and notes. For website behavior changes, check mobile layout and affected filters/sorting too.
- When adding/removing entries, update the README's **Resources**, **Demo**, and **Tools** badges as applicable, plus expected counts in `website/test_build.py`. Resources counts catalogue rows; Tools counts all Tools & Utilities entries. Investigate unexpected failures.
- Describe **what changed, why it belongs, and what you checked**. Mention missing metadata or checks you could not run.

For typo-only edits, a rendered read-back and `git diff --check` are enough. Optional link checks, browser tests, and deployment details are in the [website guide](website/README.md).
