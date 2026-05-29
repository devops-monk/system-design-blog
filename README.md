# System Design Blog

> In-depth system design tutorials — from zero to millions of users.

Source code for **[system-design.devops-monk.com](https://system-design.devops-monk.com/)** — a Hugo blog covering system design concepts, distributed systems patterns, and real-world architecture walkthroughs. Written for engineers who want to understand how large-scale systems actually work, whether they're preparing for interviews or building for production.

---

## Content Plan

Each post maps to a chapter from *System Design Interview* by Alex Xu, expanded with additional context, real-world examples, and ASCII diagrams.

| # | Topic | Status |
|---|-------|--------|
| 1 | Scale from Zero to Millions of Users | ✅ Published |
| 2 | Back-of-the-Envelope Estimation | 🔜 |
| 3 | A Framework for System Design Interviews | 🔜 |
| 4 | Design a Rate Limiter | 🔜 |
| 5 | Design Consistent Hashing | 🔜 |
| 6 | Design a Key-Value Store | 🔜 |
| 7 | Design a Unique ID Generator | 🔜 |
| 8 | Design a URL Shortener | 🔜 |
| 9 | Design a Web Crawler | 🔜 |
| 10 | Design a Notification System | 🔜 |
| 11 | Design a News Feed System | 🔜 |
| 12 | Design a Chat System | 🔜 |
| 13 | Design a Search Autocomplete System | 🔜 |
| 14 | Design YouTube | 🔜 |
| 15 | Design Google Drive | 🔜 |

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Static site generator | [Hugo](https://gohugo.io/) |
| Theme | Wellington (customised) |
| Hosting | GitHub Pages |
| DNS | Porkbun (CNAME → `devops-monk.github.io`) |
| CI/CD | GitHub Actions (auto-deploy on push to `main`) |

---

## Local Development

### Prerequisites

```bash
# macOS
brew install hugo

# Ubuntu / Debian
sudo apt install hugo
```

### Run locally

```bash
git clone git@github.com:devops-monk/system-design-blog.git
cd system-design-blog
hugo server
```

Open [http://localhost:1313](http://localhost:1313). Live-reloads on every file save.

### Build (production)

```bash
hugo --minify
# Output written to public/
```

---

## Writing a New Post

Create a Markdown file under `content/posts/<year>/`:

```bash
touch content/posts/2026/my-topic.md
```

Use this front matter:

```markdown
---
title: "Design a Rate Limiter"
description: "How to design a rate limiter that handles millions of requests per second — token bucket, sliding window, and distributed counters explained."
author: Abhay
type: post
date: 2026-06-01T00:00:00+00:00
url: /2026/06/design-rate-limiter/
image: /images/articles/design-rate-limiter.png
toc: true
categories:
  - Fundamentals
tags:
  - scalability
  - rate-limiting
  - system-design
---

Your content in Markdown...
```

Push to `main` — the pipeline builds and deploys automatically within ~60 seconds.

### Categories

| Category | Use for |
|----------|---------|
| `Fundamentals` | Core concepts, building blocks |
| `Case Studies` | Design walkthroughs (URL shortener, YouTube, etc.) |

### Image assets

Place post cover images in `static/images/articles/` and reference them as `/images/articles/filename.png` in the front matter `image` field.

---

## CI/CD Pipeline

Every push to `main` triggers `.github/workflows/deploy.yml`:

```
push to main
    │
    ▼
Checkout source
    │
    ▼
Setup Hugo 0.128.0
    │
    ▼
hugo --minify  (builds to public/)
    │
    ▼
peaceiris/actions-gh-pages
    │  pushes public/ to devops-monk/system-design-blog
    ▼  on master branch
GitHub Pages serves system-design.devops-monk.com
```

### One-time setup

1. Create repo `devops-monk/system-design-blog` on GitHub
2. Go to repo **Settings → Pages** → set source to `master` branch, root `/`
3. Set custom domain to `system-design.devops-monk.com`
4. Create a fine-grained PAT with **Contents: Read + Write** on that repo
5. In this source repo → **Settings → Secrets → Actions** → add secret `PAGES_TOKEN`

**Porkbun DNS:**
```
Type   Host              Value
CNAME  system-design     devops-monk.github.io
```

---

## Project Structure

```
system-design-blog/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
├── content/
│   ├── about.md
│   └── posts/
│       └── 2026/
│           └── *.md            # Blog posts
├── layouts/
│   └── partials/               # Customised theme partials
├── static/
│   ├── CNAME                   # system-design.devops-monk.com
│   └── images/
│       └── articles/           # Post cover images
├── themes/
│   └── wellington/             # Base theme
└── config.toml                 # Site config
```

---

## Author

**Abhay Pratap Singh** — Principal Software Engineer

- Blog: [system-design.devops-monk.com](https://system-design.devops-monk.com/)
- DevOps Blog: [blog.devops-monk.com](https://blog.devops-monk.com/)
- GitHub: [@abhi15sep](https://github.com/abhi15sep)
- LinkedIn: [abhay-singh-831997b5](https://www.linkedin.com/in/abhay-singh-831997b5/)
