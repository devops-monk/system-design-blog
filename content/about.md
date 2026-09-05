---
title: About
author: Abhay
type: page
date: 2026-05-29T00:00:00+00:00
url: /about/
hide_title: true
description: "Abhay Pratap Singh — Principal Software Engineer. Why this blog exists, what it covers, and how to get in touch."
---

<div class="about-hero">
  <img src="/images/abhay.jpeg" alt="Abhay Pratap Singh" class="about-avatar" width="132" height="132" loading="eager" />
  <div class="about-hero-body">
    <p class="about-eyebrow">About the author</p>
    <h1 class="about-name">Abhay Pratap Singh</h1>
    <p class="about-role">Principal Software Engineer — distributed systems, cloud infrastructure, and the parts of scaling nobody writes down.</p>
    <div class="about-links">
      <a href="https://github.com/abhi15sep" target="_blank" rel="noopener"><i class="fa-brands fa-github"></i> GitHub</a>
      <a href="https://www.linkedin.com/in/abhay-singh-831997b5" target="_blank" rel="noopener"><i class="fa-brands fa-linkedin-in"></i> LinkedIn</a>
      <a href="mailto:abhaypratap3537@gmail.com"><i class="fa-solid fa-envelope"></i> Email</a>
      <a href="/index.xml" target="_blank" rel="noopener"><i class="fa-solid fa-rss"></i> RSS</a>
    </div>
  </div>
</div>

<div class="about-stats">
  <div class="about-stat"><span class="about-stat-num">15</span><span class="about-stat-label">In-depth articles</span></div>
  <div class="about-stat"><span class="about-stat-num">151</span><span class="about-stat-label">Diagrams</span></div>
  <div class="about-stat"><span class="about-stat-num">64k</span><span class="about-stat-label">Words written</span></div>
  <div class="about-stat"><span class="about-stat-num">0</span><span class="about-stat-label">Ads or paywalls</span></div>
</div>

## Why this blog exists

Most system design material fails in one of two directions. Blog posts stay at the level of boxes and arrows — "add a cache, add a queue" — without ever saying what breaks if you don't. Papers go the other way and assume you already know why the problem is hard.

Neither helps when you're staring at a whiteboard, or at a production incident.

So I write the version I wanted: **each design worked out end to end, with the reasoning left in.** Not just what the architecture is, but what the obvious approach was, exactly where it fell over, and what the fix costs you. A design you can't defend under questioning isn't a design you understand.

## How these articles are written

Every case study follows the same shape, because that's the shape of the actual work:

- **Requirements first** — scope the problem, then commit to numbers. Vague requirements produce vague designs.
- **Capacity on the back of an envelope** — QPS, storage, bandwidth. The arithmetic decides the architecture far more often than taste does.
- **A high-level design that's deliberately naive** — the version most people would draw.
- **The deep dive, where it breaks** — the celebrity account that kills fan-out on write, the single inserted byte that invalidates every block hash, the ID collision that only shows up at 10,000 writes per second.
- **What real systems actually shipped** — with links to the papers and engineering posts, so you can check my work.

Diagrams are treated as part of the argument, not decoration. If a picture doesn't show a mechanism you couldn't have explained in a sentence, it doesn't earn its place.

## What's covered

- **Scaling fundamentals** — how a system grows from one server to millions of users: replication, caching, CDNs, stateless tiers, sharding.
- **Estimation** — turning "design Twitter" into concrete storage, throughput, and memory budgets in under five minutes.
- **Distributed systems core** — consistent hashing, quorums and CAP in practice, vector clocks, gossip, anti-entropy.
- **Building blocks** — rate limiters, unique ID generation, message queues, notification pipelines.
- **Full product designs** — news feed, chat, search autocomplete, web crawler, video streaming, file sync.
- **Interview technique** — a repeatable four-step framework, time budgets, and the failure modes that sink otherwise strong candidates.

Everything is indexed in chapter order in the **[Complete Guide](/guide/)** — that's the best place to start if you're new here.

## Background

I'm a Principal Software Engineer. I've spent my career building and operating systems that had to keep working while they grew, which is where most of this material comes from.

**Cloud &amp; infrastructure**

<div class="chips"><span>AWS</span><span>Terraform</span><span>Vault</span><span>Infrastructure as Code</span></div>

**Containers &amp; orchestration**

<div class="chips"><span>Kubernetes</span><span>Helm</span><span>Docker</span><span>ArgoCD</span></div>

**Application development**

<div class="chips"><span>Java</span><span>Spring Boot</span><span>Spring Batch</span><span>Spring Kafka</span></div>

**Data stores**

<div class="chips"><span>PostgreSQL</span><span>Redis</span><span>Cassandra</span><span>DynamoDB</span><span>Kafka</span></div>

**Delivery**

<div class="chips"><span>GitHub Actions</span><span>Jenkins</span><span>ArgoCD</span><span>Observability</span></div>

### Certifications

<div class="cert-grid">
  <div class="cert"><i class="fa-brands fa-aws"></i><span>AWS Certified Solutions Architect — Associate</span></div>
  <div class="cert"><i class="fa-solid fa-dharmachakra"></i><span>Certified Kubernetes Application Developer (CKAD)</span></div>
  <div class="cert"><i class="fa-solid fa-cubes"></i><span>HashiCorp Certified: Terraform Associate</span></div>
  <div class="cert"><i class="fa-solid fa-lock"></i><span>HashiCorp Certified: Vault Associate</span></div>
  <div class="cert"><i class="fa-brands fa-docker"></i><span>Docker Certified Associate</span></div>
</div>

## Get in touch

I read everything. If an explanation didn't land, if you think I got something wrong, or if there's a system you'd like to see taken apart — tell me. Corrections are especially welcome; several articles are better because a reader pushed back.

<div class="about-cta">
  <a class="about-cta-primary" href="mailto:abhaypratap3537@gmail.com"><i class="fa-solid fa-envelope"></i> abhaypratap3537@gmail.com</a>
  <a class="about-cta-secondary" href="https://www.linkedin.com/in/abhay-singh-831997b5" target="_blank" rel="noopener"><i class="fa-brands fa-linkedin-in"></i> Connect on LinkedIn</a>
  <a class="about-cta-secondary" href="/guide/"><i class="fa-solid fa-book-open"></i> Start with the Guide</a>
</div>
