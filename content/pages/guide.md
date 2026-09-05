---
title: "System Design — The Complete Guide"
description: "A complete, chapter-by-chapter system design course — from a single server to millions of users, then twenty-eight real architectures built from first principles. Every article includes diagrams, capacity numbers, and the trade-offs interviewers actually probe."
author: Abhay
type: page
date: 2026-06-03T00:00:00+00:00
url: /guide/
---

This series teaches system design the way it actually gets used — not as a list of buzzwords, but as a small set of mechanisms you combine differently for every problem. Every article works through a real design end to end: requirements, capacity estimates, a high-level architecture, then the deep dive where the interesting trade-offs live.

**What you'll learn:** How to scale a single server to millions of users, how to size a system on the back of an envelope, and how to design twenty-eight real architectures — rate limiters, key-value stores, news feeds, chat, video, file sync, maps, message queues, monitoring, payments and an exchange — knowing not just what the design is, but why every alternative was rejected.

**Who it's for:** Engineers preparing for system design interviews, and anyone who wants to understand how large-scale systems genuinely work. No prior distributed systems background assumed.

---

## Volume 1 — Foundations and Core Designs

### Foundations

Start here. These three give you the vocabulary, the arithmetic, and the interview method every later chapter assumes.

1. [Scale From Zero to Millions of Users](/2026/05/scale-from-zero-to-millions/) — Evolve one server into a multi-datacenter system: load balancers, replication, caching, CDN, stateless tiers, message queues, and sharding.
2. [Back-of-the-Envelope Estimation](/2026/05/back-of-the-envelope-estimation/) — Power-of-two tables, latency numbers, and a repeatable method for estimating QPS, storage, bandwidth, and memory.
3. [A Framework for System Design Interviews](/2026/05/framework-for-system-design-interviews/) — The 4-step framework, time budgets per step, worked examples, and the dos and don'ts that decide the outcome.

### Core building blocks

The components that appear inside almost every design that follows.

4. [Design a Rate Limiter](/2026/05/design-a-rate-limiter/) — All five algorithms compared, Redis-backed counters, and the race conditions that appear only when you distribute it.
5. [Design Consistent Hashing](/2026/05/design-consistent-hashing/) — Hash rings, virtual nodes, and why this one algorithm underpins DynamoDB, Cassandra, Discord, and Akamai.
6. [Design a Key-Value Store](/2026/05/design-a-key-value-store/) — CAP in practice, quorum tuning, vector clocks, gossip, Merkle trees, and the full read and write paths.

### Services at scale

Standalone systems, each built around one hard constraint.

7. [Design a Unique ID Generator](/2026/05/design-unique-id-generator/) — Snowflake from first principles, plus UUIDv7 and ULID and how to choose between them today.
8. [Design a URL Shortener](/2026/05/design-url-shortener/) — Base62, why seven characters is exactly right, and the 301-vs-302 choice that quietly destroys your analytics.
9. [Design a Web Crawler](/2026/05/design-web-crawler/) — The URL frontier, politeness and priority, spider traps, SimHash near-duplicate detection, and what RFC 9309 changed.
10. [Design a Notification System](/2026/05/design-notification-system/) — Per-channel queues, why exactly-once delivery is impossible, priority lanes, and retry logic that doesn't amplify outages.

### Large-scale products

Full consumer products. Each takes the building blocks above and pushes them until something breaks.

11. [Design a News Feed System](/2026/06/design-news-feed-system/) — Fan-out on write vs on read, why one celebrity account breaks the obvious design, and the hybrid everyone actually ships.
12. [Design a Chat System](/2026/06/design-chat-system/) — WebSocket over polling, server-assigned sequence numbers for ordering, multi-device sync, presence, and reconnect storms.
13. [Design a Search Autocomplete System](/2026/06/design-search-autocomplete/) — Sub-100ms suggestions on every keystroke: tries with cached top-k, offline ranking, and the trending-query gap.
14. [Design YouTube](/2026/06/design-youtube/) — Transcoding as a DAG, adaptive bitrate ladders, resumable uploads, and the cost work that decides whether the business survives.
15. [Design Google Drive](/2026/06/design-google-drive/) — Delta sync, content-defined chunking, conflict resolution that never loses data, and the dedup trick that leaks information.

---

## Volume 2 — Advanced Designs

Harder problems, the ones that come up most often for senior roles. **Every chapter here has something interactive** — a calculator, a simulator, or a working model of the idea.

### Location services

Geospatial data, static and moving.

1. [Design a Proximity Service](/2026/06/design-a-proximity-service/) — Why two B-tree indexes are not a 2D index, and how geohash, quadtrees, S2 and H3 each fold two dimensions into one. *Interactive geohash encoder.*
2. [Design Nearby Friends](/2026/06/design-nearby-friends/) — The same problem with moving data: 333K location updates a second becoming 13.3 million. *Interactive fan-out calculator.*
3. [Design Google Maps](/2026/06/design-google-maps/) — 100 petabytes of tiles, a road graph too large for memory, and CDN economics that decide the design. *Interactive tile explorer.*

### Streams and pipelines

Moving and aggregating enormous volumes of events.

4. [Design a Distributed Message Queue](/2026/06/design-distributed-message-queue/) — Why an append-only file beats a database, how partitions make ordering tunable, and what exactly-once costs. *Interactive delivery-semantics explorer.*
5. [Design a Metrics Monitoring and Alerting System](/2026/06/design-metrics-monitoring-alerting/) — Time-series storage, pull versus push, Gorilla compression, and the cardinality bomb. *Interactive cardinality calculator.*
6. [Design an Ad Click Event Aggregation System](/2026/06/design-ad-click-aggregation/) — Event time versus processing time, watermarks, and exactly-once as a genuine requirement. *Interactive watermark simulator.*

### Storage and retrieval

Keeping data, finding it again, and not losing it.

7. [Design a Distributed Email Service](/2026/06/design-distributed-email-service/) — Two exabytes a year, forty-year-old protocols, and the deliverability problem that isn't engineering. *Interactive deliverability checker.*
8. [Design S3-like Object Storage](/2026/06/design-s3-object-storage/) — Eleven nines on hardware that fails constantly: immutability, replication versus erasure coding. *Interactive durability calculator.*
9. [Design a Real-time Gaming Leaderboard](/2026/06/design-gaming-leaderboard/) — Why SQL cannot rank 25 million players, and how a skip list makes it logarithmic. *Live leaderboard.*

### Money and correctness

Where being slightly wrong is not an option.

10. [Design a Hotel Reservation System](/2026/06/design-hotel-reservation-system/) — Three transactions a second, and double booking: locking strategies and the one-statement fix. *Interactive race simulator.*
11. [Design a Payment System](/2026/06/design-payment-system/) — Double-entry bookkeeping, idempotency, and reconciliation as the last line of defence. *Interactive ledger.*
12. [Design a Digital Wallet](/2026/06/design-digital-wallet/) — Four designs, each fixing what the last one broke: 2PC, TC/C, Saga, then event sourcing over Raft. *Interactive event replay.*
13. [Design a Stock Exchange](/2026/06/design-stock-exchange/) — The one design that scales in rather than out: a single server, mmap as a message bus, an O(1) order book. *Interactive matching engine.*

---

## Where to go next

[**What to Read Next**](/2026/06/what-to-read-next/) — a method for reading an engineering post so it leaves you something reusable, then the papers, blogs and courses worth your evenings.

---

## How to read this series

**Preparing for an interview?** Read Part 1 in order, then pick any four designs from Parts 3 and 4. The framework in Chapter 3 is what you'll actually perform under time pressure — the case studies are practice reps for it.

**Learning distributed systems?** Read Parts 1 and 2 in order. Consistent hashing and the key-value store chapter carry most of the theory the rest of the series leans on.

**Already comfortable?** Jump straight to whichever product interests you. Every case study is self-contained and links back to the concepts it depends on.
