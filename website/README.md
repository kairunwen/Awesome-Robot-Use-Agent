# RUA website

A static, searchable catalogue generated from the repository's `README.md`. Layout inspired by [Awesome Python](https://awesome-python.com/); RUA branding and implementation are original.

## Build and preview

From the repository root:

```sh
python3 -m venv website/.venv
website/.venv/bin/pip install -r website/requirements.txt
website/.venv/bin/python website/build.py
python3 -m http.server 8000 --directory website/dist
```

Open http://localhost:8000. Edit the root README to update resources, then rebuild. Search, category and demo filters, Code linked filtering, demo date sorting within groups, keyboard shortcuts, and expandable source details run entirely in the browser. No API key, database, or external JavaScript is required. With JavaScript disabled, the complete catalogue remains readable.

`website/dist` is generated and ignored by Git. Its four files can be published to GitHub Pages or any static host, including under a repository subpath. Building does not publish the site.

## Check

```sh
website/.venv/bin/python -m unittest discover -s website -p 'test_*.py'
```

For external links and preview images, run `python website/check_links.py` (or use repeated `--url URL` arguments for changed destinations). HTTP errors are reported separately from access restrictions and network failures. This network check is manual; temporary third-party failures do not block site deployment.

An optional browser smoke check is available as `node website/check_browser.cjs` when Playwright and Chrome are already installed. Set `PLAYWRIGHT_PATH` if the package is outside the normal Node search path, and `PREVIEW_URL` to your running preview URL. It checks demo/code filters, date ordering, reset, anchor navigation, mobile overflow, and the no-JavaScript fallback.

## Publishing

The [public website](https://kairunwen.github.io/Awesome-Robot-Use-Agent/) is deployed by `.github/workflows/pages.yml`. Changes to the root README, logo, website source, or workflow on `main` trigger a build, validation, and deployment. It can also be run manually from **Actions → Deploy website → Run workflow**.

In repository **Settings → Pages**, the source must be **GitHub Actions**. Failed validation stops deployment, leaving the previous published version available.
