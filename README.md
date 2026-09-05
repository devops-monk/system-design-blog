# System Design Blog

> In-depth system design walkthroughs — from zero to millions of users.

Source for **[system-design.devops-monk.com](https://system-design.devops-monk.com/)**: a Hugo blog covering distributed systems patterns and real-world architecture, written for engineers preparing for interviews or building for production.

**29 articles**, 213 diagrams, and 13 interactive explainers.

---

## Content

Two volumes, indexed in order at **[/guide/](https://system-design.devops-monk.com/guide/)**.

### Volume 1 — Foundations and core designs

| | | |
|---|---|---|
| **Foundations** | 1–3 | Scaling walkthrough · estimation · the interview framework |
| **Core building blocks** | 4–6 | Rate limiter · consistent hashing · key-value store |
| **Services at scale** | 7–10 | Unique IDs · URL shortener · web crawler · notifications |
| **Large-scale products** | 11–15 | News feed · chat · autocomplete · YouTube · Google Drive |

### Volume 2 — Advanced designs

Every Volume 2 article carries an **interactive element** — a calculator, simulator, or working model.

| | | |
|---|---|---|
| **Location services** | 1–3 | Proximity service · nearby friends · Google Maps |
| **Streams and pipelines** | 4–6 | Message queue · metrics monitoring · ad click aggregation |
| **Storage and retrieval** | 7–9 | Email · S3-like object storage · gaming leaderboard |
| **Money and correctness** | 10–13 | Hotel reservation · payments · digital wallet · stock exchange |

Plus **[What to Read Next](https://system-design.devops-monk.com/2026/06/what-to-read-next/)** — a closing reading list.

---

## Tech stack

| Layer | Tool |
|---|---|
| Static site generator | [Hugo](https://gohugo.io/) **0.160.1 extended** |
| Theme | Wellington, heavily customised via `layouts/` |
| Diagrams | [Mermaid 11](https://mermaid.js.org/), rendered client-side |
| Hosting | GitHub Pages |
| DNS | Porkbun (CNAME → `devops-monk.github.io`) |
| CI/CD | GitHub Actions, auto-deploy on push to `main` |

> **The Hugo version matters.** `layouts/partials/post-cover.html` uses `hash.FNV32a`, which requires Hugo ≥ 0.129. Building with an older version fails with `function "hash" not defined`. `.github/workflows/deploy.yml` pins the version — keep it in sync with local.

---

## Local development

```bash
brew install hugo          # macOS — must be the extended build
git clone git@github.com:devops-monk/system-design-blog.git
cd system-design-blog
hugo server                # http://localhost:1313, live reload
hugo --minify              # production build into public/
```

---

## Writing a new article

Create `content/posts/<year>/my-topic.md`:

```markdown
---
title: "Design a Rate Limiter"
image: /images/articles/rate-limiter.webp
toc: true
date: 2026-06-01T00:00:00+00:00
description: "One sentence that sells the article — used in search, social cards, and the RSS feed."
tags: ["system-design", "rate-limiting", "scalability"]
categories: ["Case Studies"]
url: /2026/06/design-rate-limiter/
series: "Volume 1 — Foundations and Core Designs"
series_order: 4
---
```

`description` is not optional decoration — it is what the RSS feed and search index use. Write it deliberately.

**Categories:** `Fundamentals` for concepts and building blocks, `Case Studies` for design walkthroughs.

**`series` / `series_order`** drive the previous/next chapter links. The volumes are chained into one continuous reading order by `params.series_sequence` in `config.toml`, so the last chapter of Volume 1 leads into the first of Volume 2, and the last of Volume 2 into the closing essay. Inserting a chapter means renumbering the ones after it — the order is explicit on purpose, because the old date-based `.PrevInSection` wandered across volumes.

Keep `series_order` in step with the `VOLUME n · CH n` badge baked into the cover.

### Diagrams

Fenced ` ```mermaid ` blocks are rendered client-side by `layouts/partials/head.html`.

> **Gotcha: a semicolon inside a mermaid label silently kills the whole diagram.** Mermaid treats `;` as a statement separator, so `A-->>B: joined; you are the leader` truncates the line and the diagram renders nothing — with no error on the page. Use a dash or comma instead.
>
> Because a failed diagram is invisible, always check the **rendered SVG count against the source block count**, not just that some SVGs exist:
> ```bash
> grep -c '^```mermaid' content/posts/2026/my-post.md   # source blocks
> # rendered: count the ids mermaid assigns, NOT `<pre class="mermaid"...><svg`.
> # The <pre> carries the diagram source in data-src, and that source contains
> # `-->`, so any regex ending the tag at the first `>` matches nothing.
> chrome --headless --dump-dom "$URL" | grep -c 'id="mermaid-svg-'
> ```

Clicking a diagram opens it full-screen with wheel/pinch zoom and drag to pan (`enhancements.js`). Clicks are delegated from `document` rather than bound per block, because mermaid renders asynchronously and replaces each block's `innerHTML` — on first render and again on every dark-mode toggle. The hover "Expand" chip is a `::after` on `pre.mermaid` for the same reason.

### Interactive widgets

Volume 2 articles embed self-contained HTML + CSS + JS. Styles live in `static/assets/css/custom-styles.css`, keyed by a per-widget class prefix (`gh-`, `fo-`, `te-`, `sem-`, `cc-`, `wm-`, `rs-`, `dc-`, `du-`, `lb-`, `ld-`, `es-`, `ob-`).

> **Gotcha: no blank lines inside a raw HTML block.** Goldmark terminates an HTML block at the first blank line, so anything after it is parsed as Markdown and the widget breaks apart. Keep the markup on one line or with no blank lines anywhere inside it.

Every widget must also style its dark variant under `[data-theme="dark"]`, and collapse to a single column under `@media (max-width: 40em)`.

### Cover images

Generated by **`tools/gen_covers.py`** — each article has a hand-drawn SVG motif on a shared dark template, so the set reads as a series without every cover looking identical.

```bash
python3 tools/gen_covers.py                    # rebuild all
python3 tools/gen_covers.py stock-exchange     # rebuild one
```

To add a cover: write an `art_*()` function returning a 640×420 SVG, then add an entry to `COVERS`. Output is written straight to `static/images/articles/<name>.webp`.

Requires headless Chrome and `cwebp` (`brew install webp`).

### Social share cards

`tools/gen_social.py` derives `static/images/social/<name>.jpg` from each cover. Run it after any cover change:

```bash
python3 tools/gen_social.py
```

The covers themselves cannot be used as share images: they are 1600x640 WebP, and networks want 1.91:1 JPEG (LinkedIn has never reliably rendered WebP). Each cover is scaled to 1200x480 and centred on a 1200x630 canvas, with the bands above and below filled by a blurred copy of the cover so there is no seam.

---

## Custom layouts

The theme is overridden in `layouts/`:

| File | Purpose |
|---|---|
| `index.html` | Home page — uses `all-posts.html` for cover cards and pagination |
| `page/single.html` | Clean layout for `type: page` (About, Contact, Guide) — no post chrome |
| `_default/single.html` | Article layout — hero cover, TOC, share, related |
| `_default/rss.xml` | Feed: posts only, front-matter descriptions, cover images attached |
| `index.json` | Search index consumed by the Fuse.js client-side search |
| `partials/post-cover.html` | Resolves `image:` → `images:` → a generated gradient fallback |
| `partials/head.html` | Mermaid bootstrap, theme-aware, re-renders on dark-mode toggle |
| `partials/social-meta.html` | `og:image` + Twitter card + canonical — Hugo's internal OpenGraph template reads `.Params.images`, which this site never sets |
| `partials/social-image.html` | Resolves the share card URL; the one source of truth for both the meta tags and the JSON-LD |
| `partials/site-schema.html` | JSON-LD, built with `dict`/`jsonify` so a quote in a title cannot break it |
| `partials/series-badge.html` | "Volume 2 · Chapter 10 of 13" under the title |
| `partials/series-nav.html` | Previous/next chapter, from `series_order` rather than date |
| `_default/_markup/render-codeblock-mermaid.html` | Turns ` ```mermaid ` fences into `<pre class="mermaid">` |

---

## CI/CD

Every push to `main` runs `.github/workflows/deploy.yml`:

```
push to main → checkout → setup Hugo 0.160.1 extended
             → hugo --minify → peaceiris/actions-gh-pages
             → pushes public/ to the master branch
             → GitHub Pages serves system-design.devops-monk.com
```

Deploys land in roughly a minute. GitHub Pages and the CDN cache aggressively — **hard-refresh (Cmd+Shift+R) before concluding a change didn't ship**, or append a cache-busting query string when checking with `curl`.

### One-time setup

1. Repo **Settings → Pages** → source `master`, root `/`
2. Custom domain `system-design.devops-monk.com`
3. Fine-grained PAT with **Contents: Read + Write**, stored as the `PAGES_TOKEN` secret
4. Porkbun DNS: `CNAME  system-design → devops-monk.github.io`

---

## Project structure

```
system-design-blog/
├── .github/workflows/deploy.yml    # CI/CD
├── content/
│   ├── about.md
│   ├── pages/guide.md              # the two-volume index
│   └── posts/2026/*.md             # 29 articles
├── layouts/                        # theme overrides — see table above
├── static/
│   ├── assets/css/custom-styles.css   # design tokens + all widget styles
│   ├── assets/js/enhancements.js      # dark mode, copy buttons
│   ├── images/articles/*.webp         # covers, generated by tools/
│   └── images/social/*.jpg            # share cards, generated by tools/
├── tools/
│   ├── gen_covers.py               # cover generator
│   └── gen_social.py               # 1200x630 JPEG share cards from the covers
├── themes/wellington/              # base theme
└── config.toml
```

---

## Author

**Abhay Pratap Singh** — Principal Software Engineer

- Blog: [system-design.devops-monk.com](https://system-design.devops-monk.com/)
- DevOps blog: [blog.devops-monk.com](https://blog.devops-monk.com/)
- GitHub: [@abhi15sep](https://github.com/abhi15sep)
- LinkedIn: [abhay-singh-831997b5](https://www.linkedin.com/in/abhay-singh-831997b5/)
