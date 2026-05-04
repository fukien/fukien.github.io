# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The owner's personal academic homepage, served via GitHub Pages at `https://fukien.github.io/`. This repo replaced an older NUS-hosted page (`https://www.comp.nus.edu.sg/~huang/`) — the migration was a straight copy of that site's `public_html` folder into the repo root.

It is a static site: no build step, no dependencies, no tests. GitHub Pages serves the repo root of `master` directly. Edits go live on push.

## Layout

- `index.html` — the entire page. Single-file design built on the Hugo "aafu" theme by Darshan Baral, but exported to plain HTML — Hugo is **not** used here, do not try to "rebuild" or "regenerate" anything.
- `assets/css/` — Bootstrap + the aafu theme's CSS (`aafu.css`, `aafu_light.css`). Don't edit the bootstrap file.
- `assets/js/accordion.js` — drives the collapsible "About / Experience / Publications / …" sections in `index.html` (`expandAccordion()` and the `.accordion`/`.panel` markup).
- `assets/img/` — profile photo, favicon, NUS logo.
- `assets/pdf/` — CV.
- `assets/works/<VENUE>-<YEAR>/<project>/` — per-paper artifacts (paper, slides, supplementary, technical reports). Follow this naming when adding new publications.

All paths in `index.html` are relative (`./assets/...`), which works both locally and on GitHub Pages — keep them relative.

## Editing patterns

- **Adding a publication**: add a `<p>` inside the `Publications` accordion `<div class="panel overflow-hidden">`. Bold the owner's name with `<strong>Wentao Huang</strong>`. Link patterns to follow what's already there: `[Paper]`, `[Code]`, `[Slides]`, `[Technical Report]`, `[Video]`, `[中文博客]`, etc. Drop new local PDFs into `assets/works/<VENUE>-<YEAR>/<project>/`.
- **Toggling a section** (Talks, Services, Teaching, Skills, Hobbies, Miscellaneous): the file already contains commented-out scaffolding for these. To enable one, uncomment the matching `<h2 class="accordion ">…</h2>` + `<div class="panel overflow-hidden">…</div>` block rather than writing one from scratch — that preserves consistent styling and the accordion JS hookup.
- **First-loaded-open section**: only one `<h2>` carries `class="accordion  active "` (currently "About"). The inline `<script>` in `<head>` reads `.accordion.active` on load to expand it. If you want a different default-open section, move the `active` class.

## Local preview

`python3 -m http.server 8000` from the repo root, then open `http://localhost:8000/`. No other tooling is involved.
