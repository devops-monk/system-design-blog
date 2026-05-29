---
title: "Scale From Zero to Millions of Users: A Complete System Design Walkthrough"
description: "Learn how to evolve a system from a single server all the way to supporting millions of users. Covers databases, load balancers, caching, CDN, stateless architecture, data centers, message queues, and database sharding — step by step with diagrams."
author: Abhay
type: post
date: 2026-05-29T00:00:00+00:00
url: /2026/05/scale-from-zero-to-millions/
image: /images/articles/scale-from-zero-to-millions.png
toc: true
categories:
  - Fundamentals
tags:
  - scalability
  - databases
  - caching
  - load-balancing
  - message-queues
  - system-design
---

Imagine you are building a new app. On day one, you have one user — yourself. Six months later you have 10,000 users. A year later, 10 million.

Most systems don't fail because of bad code. They fail because the architecture that worked for 100 users was never changed to handle 1,000,000. The decisions you make early — where to store data, how to serve traffic, whether your servers keep state — determine whether you scale gracefully or collapse under your own success.

This guide walks through every evolutionary step, from a single server to a system that handles millions of concurrent users. Each section introduces exactly one new concept, explains *why* you need it, and shows what breaks without it.

---

## Step 1: The Single Server — Where Every System Starts

Every production system in the world started here: one machine running everything — web server, database, and cache all on the same box.

<svg viewBox="0 0 740 380" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a1" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a1g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
  </defs>
  <rect width="740" height="380" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- User card -->
  <rect x="20" y="70" width="150" height="120" rx="12" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="95" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#3730A3">USER</text>
  <rect x="34" y="102" width="46" height="32" rx="5" fill="#4F46E5"/>
  <rect x="36" y="104" width="42" height="8" rx="2" fill="#818CF8"/>
  <text x="57" y="128" text-anchor="middle" font-size="9" fill="#C7D2FE">Browser</text>
  <rect x="100" y="100" width="26" height="36" rx="5" fill="#6366F1"/>
  <rect x="106" y="106" width="14" height="16" rx="2" fill="#A5B4FC"/>
  <text x="113" y="130" text-anchor="middle" font-size="9" fill="#C7D2FE">App</text>
  <!-- DNS -->
  <circle cx="370" cy="105" r="52" fill="#FFFBEB" stroke="#FCD34D" stroke-width="2"/>
  <ellipse cx="370" cy="105" rx="22" ry="52" fill="none" stroke="#FCD34D" stroke-width="1.5"/>
  <line x1="318" y1="105" x2="422" y2="105" stroke="#FCD34D" stroke-width="1.5"/>
  <line x1="328" y1="78" x2="412" y2="78" stroke="#FCD34D" stroke-width="1"/>
  <line x1="328" y1="132" x2="412" y2="132" stroke="#FCD34D" stroke-width="1"/>
  <text x="370" y="99" text-anchor="middle" font-size="13" font-weight="700" fill="#92400E">DNS</text>
  <text x="370" y="117" text-anchor="middle" font-size="10" fill="#B45309">mysite.com</text>
  <!-- Server box -->
  <rect x="540" y="45" width="180" height="295" rx="14" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2.5"/>
  <text x="630" y="70" text-anchor="middle" font-size="13" font-weight="700" fill="#14532D">Single Server</text>
  <rect x="556" y="82" width="148" height="60" rx="10" fill="#3B82F6"/>
  <text x="630" y="108" text-anchor="middle" font-size="12" font-weight="600" fill="white">🖥  Web Server</text>
  <text x="630" y="128" text-anchor="middle" font-size="10" fill="#BFDBFE">HTTP requests</text>
  <rect x="556" y="156" width="148" height="60" rx="10" fill="#8B5CF6"/>
  <text x="630" y="182" text-anchor="middle" font-size="12" font-weight="600" fill="white">🗄  Database</text>
  <text x="630" y="202" text-anchor="middle" font-size="10" fill="#DDD6FE">All data storage</text>
  <rect x="556" y="230" width="148" height="60" rx="10" fill="#F59E0B"/>
  <text x="630" y="256" text-anchor="middle" font-size="12" font-weight="600" fill="white">⚡  Cache</text>
  <text x="630" y="276" text-anchor="middle" font-size="10" fill="#FEF3C7">In-memory store</text>
  <!-- SPOF badge -->
  <rect x="540" y="352" width="180" height="26" rx="8" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.5"/>
  <text x="630" y="369" text-anchor="middle" font-size="11" font-weight="600" fill="#DC2626">⚠ Single Point of Failure</text>
  <!-- Arrows -->
  <line x1="172" y1="95" x2="315" y2="98" stroke="#64748B" stroke-width="2" marker-end="url(#a1)"/>
  <text x="243" y="87" text-anchor="middle" font-size="10" fill="#475569">① DNS query</text>
  <line x1="315" y1="112" x2="172" y2="115" stroke="#10B981" stroke-width="2" marker-end="url(#a1g)"/>
  <text x="243" y="130" text-anchor="middle" font-size="10" fill="#10B981">② returns IP</text>
  <path d="M 170 148 C 300 210 420 195 537 165" fill="none" stroke="#64748B" stroke-width="2" marker-end="url(#a1)"/>
  <text x="350" y="210" text-anchor="middle" font-size="10" fill="#475569">③ HTTP Request</text>
  <path d="M 537 215 C 420 290 300 275 170 175" fill="none" stroke="#10B981" stroke-width="2" marker-end="url(#a1g)"/>
  <text x="350" y="295" text-anchor="middle" font-size="10" fill="#10B981">④ HTML / JSON Response</text>
</svg>

### How a request works

1. **DNS lookup** — Your browser asks DNS "what is the IP for mysite.com?" DNS translates human-readable names into IP addresses like `15.125.23.214`. It's managed by third-party providers (Cloudflare, Route 53) — not your server.
2. **IP returned** — The DNS server responds with your server's IP.
3. **HTTP request** — Your browser connects to that IP and sends a request.
4. **Response** — The server sends back an HTML page (browser) or JSON (mobile app).

### What breaks first

- **No separation of concerns** — web traffic and database queries compete for the same CPU and RAM.
- **No redundancy** — if the one server crashes, every user sees an error page.

---

## Step 2: Separating the Database

The first architectural move: run your database on a separate server so each tier can be scaled independently.

<svg viewBox="0 0 740 240" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a2" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
  </defs>
  <rect width="740" height="240" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- User -->
  <rect x="30" y="80" width="120" height="80" rx="12" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="90" y="115" text-anchor="middle" font-size="28">👤</text>
  <text x="90" y="148" text-anchor="middle" font-size="12" font-weight="600" fill="#3730A3">User</text>
  <!-- Web Server -->
  <rect x="240" y="60" width="160" height="120" rx="12" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <text x="320" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#1E40AF">WEB TIER</text>
  <rect x="258" y="98" width="124" height="52" rx="8" fill="#3B82F6"/>
  <text x="320" y="121" text-anchor="middle" font-size="12" font-weight="600" fill="white">🖥  Web Server</text>
  <text x="320" y="139" text-anchor="middle" font-size="10" fill="#BFDBFE">App logic · HTTP</text>
  <text x="320" y="196" text-anchor="middle" font-size="10" fill="#64748B">Scale independently</text>
  <!-- Database -->
  <rect x="510" y="60" width="200" height="120" rx="12" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="2"/>
  <text x="610" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#4C1D95">DATA TIER</text>
  <rect x="528" y="98" width="164" height="52" rx="8" fill="#8B5CF6"/>
  <text x="610" y="121" text-anchor="middle" font-size="12" font-weight="600" fill="white">🗄  Database Server</text>
  <text x="610" y="139" text-anchor="middle" font-size="10" fill="#DDD6FE">Storage · Indexing · Queries</text>
  <text x="610" y="196" text-anchor="middle" font-size="10" fill="#64748B">Scale independently</text>
  <!-- Arrows -->
  <line x1="152" y1="120" x2="237" y2="120" stroke="#64748B" stroke-width="2" marker-end="url(#a2)"/>
  <line x1="402" y1="108" x2="507" y2="108" stroke="#64748B" stroke-width="2" marker-end="url(#a2)"/>
  <text x="455" y="100" text-anchor="middle" font-size="10" fill="#475569">read / write</text>
  <line x1="507" y1="130" x2="402" y2="130" stroke="#64748B" stroke-width="2" marker-end="url(#a2)"/>
  <text x="455" y="148" text-anchor="middle" font-size="10" fill="#475569">return data</text>
</svg>

**Relational (SQL)** — MySQL, PostgreSQL. Rows and columns, supports JOINs. Default choice for most apps.

**Non-Relational (NoSQL)** — Redis (key-value), Cassandra (wide-column), MongoDB (documents). Choose NoSQL when you need sub-millisecond latency, truly unstructured data, or massive write volume.

---

## Step 3: Vertical vs. Horizontal Scaling

<svg viewBox="0 0 740 300" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <rect width="740" height="300" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Divider -->
  <line x1="370" y1="20" x2="370" y2="280" stroke="#E2E8F0" stroke-width="2" stroke-dasharray="6,4"/>
  <!-- Vertical scaling label -->
  <text x="185" y="42" text-anchor="middle" font-size="14" font-weight="700" fill="#1E293B">⬆ Vertical Scaling</text>
  <text x="185" y="60" text-anchor="middle" font-size="11" fill="#64748B">"Scale Up" — bigger machine</text>
  <!-- Small server -->
  <rect x="60" y="80" width="60" height="80" rx="8" fill="#CBD5E1" stroke="#94A3B8" stroke-width="2"/>
  <text x="90" y="116" text-anchor="middle" font-size="9" fill="#475569">2 CPU</text>
  <text x="90" y="130" text-anchor="middle" font-size="9" fill="#475569">4 GB RAM</text>
  <!-- Medium server -->
  <rect x="145" y="60" width="80" height="100" rx="8" fill="#93C5FD" stroke="#60A5FA" stroke-width="2"/>
  <text x="185" y="104" text-anchor="middle" font-size="9" fill="#1E40AF">8 CPU</text>
  <text x="185" y="118" text-anchor="middle" font-size="9" fill="#1E40AF">32 GB RAM</text>
  <!-- Large server -->
  <rect x="252" y="32" width="100" height="128" rx="8" fill="#3B82F6" stroke="#2563EB" stroke-width="2"/>
  <text x="302" y="88" text-anchor="middle" font-size="9" fill="white">64 CPU</text>
  <text x="302" y="104" text-anchor="middle" font-size="9" fill="white">512 GB RAM</text>
  <!-- Arrows between servers -->
  <line x1="122" y1="120" x2="143" y2="115" stroke="#475569" stroke-width="1.5" marker-end="url(#a3)"/>
  <line x1="227" y1="108" x2="250" y2="100" stroke="#475569" stroke-width="1.5" marker-end="url(#a3)"/>
  <!-- Ceiling label -->
  <rect x="50" y="175" width="310" height="28" rx="6" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.5"/>
  <text x="205" y="193" text-anchor="middle" font-size="11" fill="#DC2626" font-weight="600">⚠ Hardware ceiling · No redundancy</text>
  <!-- Pros -->
  <text x="205" y="235" text-anchor="middle" font-size="10" fill="#16A34A">✓ Simple — no code changes</text>
  <text x="205" y="255" text-anchor="middle" font-size="10" fill="#DC2626">✗ Single point of failure</text>
  <text x="205" y="275" text-anchor="middle" font-size="10" fill="#DC2626">✗ Hardware limits</text>
  <!-- Horizontal scaling label -->
  <text x="555" y="42" text-anchor="middle" font-size="14" font-weight="700" fill="#1E293B">➡ Horizontal Scaling</text>
  <text x="555" y="60" text-anchor="middle" font-size="11" fill="#64748B">"Scale Out" — more machines</text>
  <defs>
    <marker id="a3" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#475569"/></marker>
  </defs>
  <!-- Multiple servers -->
  <rect x="390" y="80" width="70" height="60" rx="8" fill="#3B82F6" stroke="#2563EB" stroke-width="2"/>
  <text x="425" y="115" text-anchor="middle" font-size="10" fill="white">Server 1</text>
  <rect x="475" y="80" width="70" height="60" rx="8" fill="#3B82F6" stroke="#2563EB" stroke-width="2"/>
  <text x="510" y="115" text-anchor="middle" font-size="10" fill="white">Server 2</text>
  <rect x="560" y="80" width="70" height="60" rx="8" fill="#3B82F6" stroke="#2563EB" stroke-width="2"/>
  <text x="595" y="115" text-anchor="middle" font-size="10" fill="white">Server 3</text>
  <rect x="645" y="80" width="70" height="60" rx="8" fill="#93C5FD" stroke="#60A5FA" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="680" y="108" text-anchor="middle" font-size="10" fill="#1E40AF">Server</text>
  <text x="680" y="124" text-anchor="middle" font-size="10" fill="#1E40AF">N+1 ...</text>
  <!-- Pros -->
  <rect x="380" y="175" width="340" height="28" rx="6" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.5"/>
  <text x="550" y="193" text-anchor="middle" font-size="11" fill="#16A34A" font-weight="600">✓ No ceiling · Redundancy built-in</text>
  <text x="550" y="235" text-anchor="middle" font-size="10" fill="#16A34A">✓ Add servers as traffic grows</text>
  <text x="550" y="255" text-anchor="middle" font-size="10" fill="#16A34A">✓ Failover when one server crashes</text>
  <text x="550" y="275" text-anchor="middle" font-size="10" fill="#DC2626">✗ Requires stateless architecture</text>
</svg>

---

## Step 4: Load Balancer — The Traffic Distributor

A load balancer sits in front of your web servers and evenly distributes incoming requests. Users connect to the load balancer's **public IP**. Web servers hide behind **private IPs** — unreachable directly from the internet.

<svg viewBox="0 0 740 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a4" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a4r" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#EF4444"/></marker>
  </defs>
  <rect width="740" height="400" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Users -->
  <rect x="290" y="18" width="160" height="55" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="370" y="42" text-anchor="middle" font-size="22">👥</text>
  <text x="370" y="64" text-anchor="middle" font-size="11" font-weight="600" fill="#3730A3">Users</text>
  <!-- Load Balancer -->
  <rect x="265" y="110" width="210" height="65" rx="12" fill="#0E7490" stroke="#06B6D4" stroke-width="2.5"/>
  <text x="370" y="136" text-anchor="middle" font-size="13" font-weight="700" fill="white">⚖  Load Balancer</text>
  <text x="370" y="156" text-anchor="middle" font-size="10" fill="#A5F3FC">Public IP: 88.88.88.1</text>
  <!-- Server 1 -->
  <rect x="100" y="240" width="170" height="80" rx="12" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <rect x="115" y="258" width="140" height="46" rx="8" fill="#3B82F6"/>
  <text x="185" y="279" text-anchor="middle" font-size="12" font-weight="600" fill="white">🖥  Server 1</text>
  <text x="185" y="297" text-anchor="middle" font-size="10" fill="#BFDBFE">Private IP: 10.0.0.1</text>
  <!-- Server 2 -->
  <rect x="470" y="240" width="170" height="80" rx="12" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <rect x="485" y="258" width="140" height="46" rx="8" fill="#3B82F6"/>
  <text x="555" y="279" text-anchor="middle" font-size="12" font-weight="600" fill="white">🖥  Server 2</text>
  <text x="555" y="297" text-anchor="middle" font-size="10" fill="#BFDBFE">Private IP: 10.0.0.2</text>
  <!-- Database -->
  <rect x="265" y="355" width="210" height="35" rx="10" fill="#8B5CF6"/>
  <text x="370" y="377" text-anchor="middle" font-size="12" font-weight="600" fill="white">🗄  Database</text>
  <!-- Arrows: Users → LB -->
  <line x1="370" y1="74" x2="370" y2="108" stroke="#64748B" stroke-width="2" marker-end="url(#a4)"/>
  <!-- LB → Server 1 -->
  <line x1="300" y1="168" x2="220" y2="238" stroke="#06B6D4" stroke-width="2" marker-end="url(#a4)"/>
  <text x="240" y="208" text-anchor="middle" font-size="10" fill="#0E7490">route</text>
  <!-- LB → Server 2 -->
  <line x1="440" y1="168" x2="520" y2="238" stroke="#06B6D4" stroke-width="2" marker-end="url(#a4)"/>
  <text x="500" y="208" text-anchor="middle" font-size="10" fill="#0E7490">route</text>
  <!-- Server 1 → DB -->
  <line x1="210" y1="322" x2="300" y2="353" stroke="#64748B" stroke-width="1.5" marker-end="url(#a4)"/>
  <!-- Server 2 → DB -->
  <line x1="530" y1="322" x2="442" y2="353" stroke="#64748B" stroke-width="1.5" marker-end="url(#a4)"/>
  <!-- Failover label -->
  <rect x="30" y="340" width="60" height="22" rx="6" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.5"/>
  <text x="60" y="355" text-anchor="middle" font-size="9" fill="#DC2626">If S1 fails →</text>
  <path d="M 89 351 Q 200 360 300 178" fill="none" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#a4r)"/>
  <text x="60" y="375" text-anchor="middle" font-size="9" fill="#DC2626">100% → S2</text>
</svg>

**Round-robin** distributes requests sequentially (1→2→1→2). Other strategies: **least connections** (route to least busy), **IP hash** (same user always hits same server).

---

## Step 5: Database Replication — Surviving Database Failures

One database is still a single point of failure. Database replication solves this with a **primary-replica** (master-slave) setup.

<svg viewBox="0 0 740 380" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a5w" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#EF4444"/></marker>
    <marker id="a5r" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
    <marker id="a5p" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#8B5CF6"/></marker>
  </defs>
  <rect width="740" height="380" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Web Servers -->
  <rect x="235" y="18" width="270" height="55" rx="10" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <text x="370" y="38" text-anchor="middle" font-size="11" font-weight="700" fill="#1E40AF">WEB SERVERS</text>
  <rect x="248" y="44" width="75" height="20" rx="5" fill="#3B82F6"/>
  <text x="285" y="58" text-anchor="middle" font-size="9" fill="white">Server 1</text>
  <rect x="333" y="44" width="75" height="20" rx="5" fill="#3B82F6"/>
  <text x="370" y="58" text-anchor="middle" font-size="9" fill="white">Server 2</text>
  <rect x="418" y="44" width="75" height="20" rx="5" fill="#3B82F6"/>
  <text x="455" y="58" text-anchor="middle" font-size="9" fill="white">Server 3</text>
  <!-- Master DB -->
  <rect x="60" y="155" width="185" height="90" rx="14" fill="#7C3AED" stroke="#6D28D9" stroke-width="2.5"/>
  <text x="152" y="182" text-anchor="middle" font-size="14" font-weight="700" fill="white">Master DB</text>
  <text x="152" y="202" text-anchor="middle" font-size="10" fill="#DDD6FE">INSERT / UPDATE / DELETE</text>
  <text x="152" y="220" text-anchor="middle" font-size="10" fill="#DDD6FE">All writes go here first</text>
  <!-- Slave 1 -->
  <rect x="470" y="120" width="160" height="70" rx="12" fill="#6D28D9" stroke="#8B5CF6" stroke-width="2"/>
  <text x="550" y="148" text-anchor="middle" font-size="12" font-weight="600" fill="white">Slave DB 1</text>
  <text x="550" y="166" text-anchor="middle" font-size="10" fill="#DDD6FE">SELECT (reads)</text>
  <!-- Slave 2 -->
  <rect x="470" y="210" width="160" height="70" rx="12" fill="#6D28D9" stroke="#8B5CF6" stroke-width="2"/>
  <text x="550" y="238" text-anchor="middle" font-size="12" font-weight="600" fill="white">Slave DB 2</text>
  <text x="550" y="256" text-anchor="middle" font-size="10" fill="#DDD6FE">SELECT (reads)</text>
  <!-- Slave 3 -->
  <rect x="470" y="300" width="160" height="70" rx="12" fill="#6D28D9" stroke="#8B5CF6" stroke-width="2"/>
  <text x="550" y="328" text-anchor="middle" font-size="12" font-weight="600" fill="white">Slave DB 3</text>
  <text x="550" y="346" text-anchor="middle" font-size="10" fill="#DDD6FE">SELECT (reads)</text>
  <!-- Arrows: Web Servers → Master (WRITES) -->
  <line x1="260" y1="74" x2="185" y2="153" stroke="#EF4444" stroke-width="2.5" marker-end="url(#a5w)"/>
  <text x="200" y="118" text-anchor="middle" font-size="10" font-weight="600" fill="#EF4444">WRITES</text>
  <!-- Master → Slaves (replication) -->
  <line x1="247" y1="178" x2="468" y2="152" stroke="#8B5CF6" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#a5p)"/>
  <text x="358" y="158" text-anchor="middle" font-size="9" fill="#7C3AED">replicate</text>
  <line x1="247" y1="200" x2="468" y2="245" stroke="#8B5CF6" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#a5p)"/>
  <text x="358" y="230" text-anchor="middle" font-size="9" fill="#7C3AED">replicate</text>
  <line x1="200" y1="246" x2="468" y2="330" stroke="#8B5CF6" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#a5p)"/>
  <text x="320" y="312" text-anchor="middle" font-size="9" fill="#7C3AED">replicate</text>
  <!-- Slaves → Web Servers (READS) -->
  <line x1="468" y1="142" x2="460" y2="74" stroke="#10B981" stroke-width="2" marker-end="url(#a5r)"/>
  <text x="490" y="108" text-anchor="middle" font-size="10" font-weight="600" fill="#10B981">READS</text>
</svg>

**Why reads go to replicas:** Most apps read far more than they write. Three replicas = roughly 3× read throughput. The master handles 100% of writes; replicas handle 100% of reads.

**Failover:** If a replica fails, reads go to another replica. If the master fails, a replica is promoted to master — though recent writes may need recovery from logs.

---

## Step 6: Cache — Stop Hitting the Database for the Same Data

Every page load fires database queries. If 10,000 users load the same product page simultaneously, that's 10,000 identical queries. A cache stores results in memory so the database is hit only once.

<svg viewBox="0 0 740 340" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a6g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
    <marker id="a6" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a6o" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#F97316"/></marker>
  </defs>
  <rect width="740" height="340" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Cache HIT panel -->
  <rect x="15" y="15" width="340" height="310" rx="12" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2"/>
  <text x="185" y="40" text-anchor="middle" font-size="13" font-weight="700" fill="#14532D">✅  Cache HIT</text>
  <!-- Web Server -->
  <rect x="40" y="60" width="120" height="55" rx="10" fill="#3B82F6"/>
  <text x="100" y="84" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Server</text>
  <text x="100" y="104" text-anchor="middle" font-size="9" fill="#BFDBFE">receives request</text>
  <!-- Cache (hit) -->
  <rect x="210" y="60" width="120" height="55" rx="10" fill="#10B981"/>
  <text x="270" y="84" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚡ Cache</text>
  <text x="270" y="104" text-anchor="middle" font-size="9" fill="#D1FAE5">data found!</text>
  <!-- DB (greyed) -->
  <rect x="210" y="200" width="120" height="55" rx="10" fill="#E2E8F0"/>
  <text x="270" y="224" text-anchor="middle" font-size="11" fill="#94A3B8">Database</text>
  <text x="270" y="244" text-anchor="middle" font-size="9" fill="#CBD5E1">not needed</text>
  <!-- Arrows HIT -->
  <line x1="162" y1="80" x2="208" y2="80" stroke="#10B981" stroke-width="2" marker-end="url(#a6g)"/>
  <text x="185" y="72" text-anchor="middle" font-size="9" fill="#16A34A">① check</text>
  <line x1="208" y1="100" x2="162" y2="100" stroke="#10B981" stroke-width="2.5" marker-end="url(#a6g)"/>
  <text x="185" y="118" text-anchor="middle" font-size="9" fill="#16A34A">② return (~1ms)</text>
  <!-- Speed label -->
  <rect x="40" y="190" width="140" height="65" rx="10" fill="#ECFDF5" stroke="#6EE7B7" stroke-width="1.5"/>
  <text x="110" y="215" text-anchor="middle" font-size="11" font-weight="700" fill="#065F46">⚡ ~1 ms</text>
  <text x="110" y="235" text-anchor="middle" font-size="10" fill="#047857">No DB query</text>
  <text x="110" y="252" text-anchor="middle" font-size="10" fill="#047857">Served from RAM</text>
  <!-- Cache MISS panel -->
  <rect x="385" y="15" width="340" height="310" rx="12" fill="#FFF7ED" stroke="#FED7AA" stroke-width="2"/>
  <text x="555" y="40" text-anchor="middle" font-size="13" font-weight="700" fill="#92400E">❌  Cache MISS</text>
  <!-- Web Server -->
  <rect x="405" y="60" width="120" height="55" rx="10" fill="#3B82F6"/>
  <text x="465" y="84" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Server</text>
  <text x="465" y="104" text-anchor="middle" font-size="9" fill="#BFDBFE">receives request</text>
  <!-- Cache (miss) -->
  <rect x="575" y="60" width="120" height="55" rx="10" fill="#F59E0B"/>
  <text x="635" y="84" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚡ Cache</text>
  <text x="635" y="104" text-anchor="middle" font-size="9" fill="#FEF3C7">not found</text>
  <!-- Database -->
  <rect x="575" y="190" width="120" height="55" rx="10" fill="#8B5CF6"/>
  <text x="635" y="214" text-anchor="middle" font-size="11" font-weight="600" fill="white">Database</text>
  <text x="635" y="234" text-anchor="middle" font-size="9" fill="#DDD6FE">fetch data</text>
  <!-- Arrows MISS -->
  <line x1="527" y1="80" x2="573" y2="80" stroke="#64748B" stroke-width="2" marker-end="url(#a6)"/>
  <text x="550" y="72" text-anchor="middle" font-size="9" fill="#475569">① check</text>
  <line x1="635" y1="117" x2="635" y2="188" stroke="#64748B" stroke-width="2" marker-end="url(#a6)"/>
  <text x="660" y="155" text-anchor="middle" font-size="9" fill="#475569">② query</text>
  <line x1="573" y1="210" x2="527" y2="105" stroke="#F97316" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#a6o)"/>
  <text x="540" y="165" text-anchor="middle" font-size="9" fill="#EA580C">③ store+return</text>
  <!-- Next request label -->
  <rect x="405" y="260" width="280" height="45" rx="10" fill="#FEF3C7" stroke="#FCD34D" stroke-width="1.5"/>
  <text x="545" y="279" text-anchor="middle" font-size="11" font-weight="600" fill="#92400E">Next request → Cache HIT ✅</text>
  <text x="545" y="297" text-anchor="middle" font-size="10" fill="#B45309">Data now cached for future requests</text>
</svg>

**Key considerations:**
- **TTL (Time To Live)** — expire cache entries after a sensible duration. Too short = cache stampede. Too long = stale data.
- **Eviction policy** — when cache is full, LRU (Least Recently Used) removes the oldest untouched entry.
- **Consistency** — invalidate the cache when the underlying data changes (*"There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton*)

---

## Step 7: Content Delivery Network (CDN)

Your cache handles dynamic data. But pages also serve static files — images, CSS, JavaScript, fonts. A **CDN** is a globally distributed network of servers that caches and serves static content from edge nodes close to the user.

<svg viewBox="0 0 740 340" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a7" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a7g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
    <marker id="a7p" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#EC4899"/></marker>
  </defs>
  <rect width="740" height="340" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- User A -->
  <rect x="20" y="55" width="120" height="65" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="80" y="80" text-anchor="middle" font-size="20">👤</text>
  <text x="80" y="100" text-anchor="middle" font-size="11" font-weight="600" fill="#3730A3">User A</text>
  <text x="80" y="115" text-anchor="middle" font-size="9" fill="#6366F1">Tokyo</text>
  <!-- User B -->
  <rect x="20" y="220" width="120" height="65" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="80" y="245" text-anchor="middle" font-size="20">👤</text>
  <text x="80" y="265" text-anchor="middle" font-size="11" font-weight="600" fill="#3730A3">User B</text>
  <text x="80" y="280" text-anchor="middle" font-size="9" fill="#6366F1">Tokyo</text>
  <!-- CDN Edge -->
  <rect x="270" y="120" width="200" height="100" rx="14" fill="#FDF2F8" stroke="#F9A8D4" stroke-width="2.5"/>
  <text x="370" y="150" text-anchor="middle" font-size="28">⚡</text>
  <text x="370" y="175" text-anchor="middle" font-size="13" font-weight="700" fill="#9D174D">CDN Edge Node</text>
  <text x="370" y="195" text-anchor="middle" font-size="10" fill="#BE185D">Tokyo · 5ms away</text>
  <!-- Origin Server -->
  <rect x="570" y="120" width="155" height="100" rx="14" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <text x="647" y="150" text-anchor="middle" font-size="22">🖥</text>
  <text x="647" y="175" text-anchor="middle" font-size="12" font-weight="700" fill="#1E40AF">Origin Server</text>
  <text x="647" y="195" text-anchor="middle" font-size="10" fill="#3B82F6">Virginia · 150ms away</text>
  <!-- Arrow 1: User A → CDN -->
  <line x1="142" y1="82" x2="268" y2="148" stroke="#64748B" stroke-width="2" marker-end="url(#a7)"/>
  <text x="180" y="105" text-anchor="middle" font-size="9" fill="#475569">① GET image.png</text>
  <!-- Arrow 2: CDN MISS → Origin -->
  <line x1="472" y1="155" x2="568" y2="160" stroke="#EC4899" stroke-width="2" marker-end="url(#a7p)"/>
  <text x="520" y="148" text-anchor="middle" font-size="9" fill="#DB2777">② MISS → fetch</text>
  <!-- Arrow 3: Origin → CDN -->
  <line x1="568" y1="180" x2="472" y2="178" stroke="#64748B" stroke-width="1.5" marker-end="url(#a7)"/>
  <text x="520" y="198" text-anchor="middle" font-size="9" fill="#475569">③ image.png</text>
  <!-- Arrow 4: CDN → User A -->
  <line x1="268" y1="162" x2="142" y2="100" stroke="#10B981" stroke-width="2.5" marker-end="url(#a7g)"/>
  <text x="180" y="148" text-anchor="middle" font-size="9" fill="#059669">④ cached + returned</text>
  <!-- Arrow 5: User B → CDN -->
  <line x1="142" y1="252" x2="268" y2="195" stroke="#64748B" stroke-width="2" marker-end="url(#a7)"/>
  <text x="180" y="240" text-anchor="middle" font-size="9" fill="#475569">⑤ GET image.png</text>
  <!-- Arrow 6: CDN HIT → User B -->
  <line x1="268" y1="210" x2="142" y2="262" stroke="#10B981" stroke-width="2.5" marker-end="url(#a7g)"/>
  <text x="185" y="258" text-anchor="middle" font-size="9" fill="#059669">⑥ HIT! 5ms ⚡</text>
  <!-- Latency comparison -->
  <rect x="20" y="300" width="700" height="30" rx="8" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.5"/>
  <text x="370" y="320" text-anchor="middle" font-size="11" fill="#166534" font-weight="600">Without CDN: 150ms round-trip  ·  With CDN: ~5ms from nearest edge node</text>
</svg>

**Cache busting** — when you update `style.css`, append a hash: `style.css?v=abc123`. The CDN treats it as a new file and fetches the latest version immediately.

---

## Step 8: Stateless Web Tier — The Key to Horizontal Scaling

With multiple web servers behind a load balancer, a subtle problem emerges: if a server stores session data in local memory, users get logged out when routed to a different server.

<svg viewBox="0 0 740 380" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a8r" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#EF4444"/></marker>
    <marker id="a8g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
    <marker id="a8" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
  </defs>
  <rect width="740" height="380" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Left panel: Stateful -->
  <rect x="10" y="10" width="355" height="360" rx="14" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="2"/>
  <text x="188" y="36" text-anchor="middle" font-size="14" font-weight="700" fill="#991B1B">❌  Stateful (Bad)</text>
  <text x="188" y="55" text-anchor="middle" font-size="10" fill="#B91C1C">Session stored in server memory</text>
  <!-- Users -->
  <text x="55" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User A</text>
  <text x="188" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User B</text>
  <text x="320" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User C</text>
  <!-- Server 1 -->
  <rect x="20" y="110" width="145" height="90" rx="10" fill="#EF4444"/>
  <text x="93" y="135" text-anchor="middle" font-size="11" font-weight="600" fill="white">Server 1</text>
  <text x="93" y="155" text-anchor="middle" font-size="9" fill="#FEE2E2">Session: User A ✓</text>
  <text x="93" y="170" text-anchor="middle" font-size="9" fill="#FEE2E2">Session: User C ✓</text>
  <text x="93" y="185" text-anchor="middle" font-size="8" fill="#FECACA">User B here → FAIL ✗</text>
  <!-- Server 2 -->
  <rect x="200" y="110" width="145" height="90" rx="10" fill="#EF4444"/>
  <text x="273" y="135" text-anchor="middle" font-size="11" font-weight="600" fill="white">Server 2</text>
  <text x="273" y="155" text-anchor="middle" font-size="9" fill="#FEE2E2">Session: User B ✓</text>
  <text x="273" y="185" text-anchor="middle" font-size="8" fill="#FECACA">User A here → FAIL ✗</text>
  <!-- Arrows stateful -->
  <line x1="55" y1="95" x2="55" y2="108" stroke="#EF4444" stroke-width="2" marker-end="url(#a8r)"/>
  <line x1="188" y1="95" x2="260" y2="108" stroke="#EF4444" stroke-width="2" marker-end="url(#a8r)"/>
  <line x1="320" y1="95" x2="130" y2="108" stroke="#EF4444" stroke-width="2" marker-end="url(#a8r)"/>
  <!-- Problem label -->
  <rect x="20" y="218" width="325" height="50" rx="8" fill="#FEE2E2" stroke="#FCA5A5" stroke-width="1.5"/>
  <text x="183" y="239" text-anchor="middle" font-size="11" font-weight="600" fill="#991B1B">Each user is "stuck" to one server</text>
  <text x="183" y="257" text-anchor="middle" font-size="10" fill="#B91C1C">If Server 1 crashes → User A loses session</text>
  <!-- Cannot scale label -->
  <rect x="20" y="280" width="325" height="70" rx="8" fill="#FECDD3" stroke="#FDA4AF" stroke-width="1"/>
  <text x="183" y="302" text-anchor="middle" font-size="10" fill="#9F1239">• Adding servers is risky</text>
  <text x="183" y="320" text-anchor="middle" font-size="10" fill="#9F1239">• Uneven load distribution</text>
  <text x="183" y="338" text-anchor="middle" font-size="10" fill="#9F1239">• Failover causes user logout</text>
  <!-- Right panel: Stateless -->
  <rect x="375" y="10" width="355" height="360" rx="14" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2"/>
  <text x="553" y="36" text-anchor="middle" font-size="14" font-weight="700" fill="#14532D">✅  Stateless (Good)</text>
  <text x="553" y="55" text-anchor="middle" font-size="10" fill="#166534">Session stored in shared data store</text>
  <!-- Users -->
  <text x="430" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User A</text>
  <text x="553" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User B</text>
  <text x="676" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User C</text>
  <!-- LB -->
  <rect x="478" y="108" width="150" height="35" rx="8" fill="#06B6D4"/>
  <text x="553" y="130" text-anchor="middle" font-size="11" font-weight="600" fill="white">Load Balancer</text>
  <!-- Server 1 and 2 -->
  <rect x="385" y="165" width="115" height="55" rx="8" fill="#3B82F6"/>
  <text x="443" y="190" text-anchor="middle" font-size="11" font-weight="600" fill="white">Server 1</text>
  <text x="443" y="208" text-anchor="middle" font-size="9" fill="#BFDBFE">stateless</text>
  <rect x="606" y="165" width="115" height="55" rx="8" fill="#3B82F6"/>
  <text x="664" y="190" text-anchor="middle" font-size="11" font-weight="600" fill="white">Server 2</text>
  <text x="664" y="208" text-anchor="middle" font-size="9" fill="#BFDBFE">stateless</text>
  <!-- Shared store -->
  <rect x="453" y="252" width="200" height="55" rx="10" fill="#10B981"/>
  <text x="553" y="277" text-anchor="middle" font-size="12" font-weight="600" fill="white">🗄  Shared Session Store</text>
  <text x="553" y="297" text-anchor="middle" font-size="9" fill="#D1FAE5">Redis · DynamoDB · SQL</text>
  <!-- Arrows stateless -->
  <line x1="430" y1="95" x2="510" y2="106" stroke="#10B981" stroke-width="1.5" marker-end="url(#a8g)"/>
  <line x1="553" y1="95" x2="553" y2="106" stroke="#10B981" stroke-width="1.5" marker-end="url(#a8g)"/>
  <line x1="676" y1="95" x2="596" y2="106" stroke="#10B981" stroke-width="1.5" marker-end="url(#a8g)"/>
  <line x1="510" y1="143" x2="460" y2="163" stroke="#64748B" stroke-width="1.5" marker-end="url(#a8)"/>
  <line x1="596" y1="143" x2="646" y2="163" stroke="#64748B" stroke-width="1.5" marker-end="url(#a8)"/>
  <line x1="443" y1="222" x2="490" y2="250" stroke="#64748B" stroke-width="1.5" marker-end="url(#a8)"/>
  <line x1="664" y1="222" x2="616" y2="250" stroke="#64748B" stroke-width="1.5" marker-end="url(#a8)"/>
  <!-- Benefits -->
  <rect x="385" y="318" width="335" height="40" rx="8" fill="#DCFCE7" stroke="#86EFAC" stroke-width="1.5"/>
  <text x="553" y="335" text-anchor="middle" font-size="10" fill="#166534" font-weight="600">Any server handles any user</text>
  <text x="553" y="350" text-anchor="middle" font-size="10" fill="#166534">Add or remove servers without disruption</text>
</svg>

**Rule of thumb:** Web servers should be stateless. State belongs in a database or cache, not in server memory.

---

## Step 9: Multiple Data Centers — Geographic Redundancy

<svg viewBox="0 0 740 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a9" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a9g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
    <marker id="a9r" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#8B5CF6"/></marker>
  </defs>
  <rect width="740" height="400" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Users -->
  <rect x="295" y="15" width="150" height="50" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="370" y="44" text-anchor="middle" font-size="22">👥</text>
  <text x="370" y="60" text-anchor="middle" font-size="10" font-weight="600" fill="#3730A3">Worldwide Users</text>
  <!-- GeoDNS -->
  <rect x="295" y="90" width="150" height="45" rx="10" fill="#FFFBEB" stroke="#FCD34D" stroke-width="2"/>
  <text x="370" y="116" text-anchor="middle" font-size="12" font-weight="700" fill="#92400E">🌐 GeoDNS</text>
  <!-- DC1 US-East -->
  <rect x="20" y="185" width="320" height="185" rx="14" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2.5"/>
  <text x="180" y="210" text-anchor="middle" font-size="13" font-weight="700" fill="#1E40AF">🏢 US-East (Primary)</text>
  <rect x="38" y="222" width="130" height="45" rx="8" fill="#3B82F6"/>
  <text x="103" y="243" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Servers</text>
  <text x="103" y="258" text-anchor="middle" font-size="9" fill="#BFDBFE">auto-scaled</text>
  <rect x="180" y="222" width="130" height="45" rx="8" fill="#8B5CF6"/>
  <text x="245" y="243" text-anchor="middle" font-size="11" font-weight="600" fill="white">Database</text>
  <text x="245" y="258" text-anchor="middle" font-size="9" fill="#DDD6FE">primary</text>
  <rect x="38" y="282" width="272" height="40" rx="8" fill="#10B981"/>
  <text x="174" y="307" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚡ Cache Cluster</text>
  <!-- DC2 US-West -->
  <rect x="400" y="185" width="320" height="185" rx="14" fill="#FFF7ED" stroke="#FED7AA" stroke-width="2.5"/>
  <text x="560" y="210" text-anchor="middle" font-size="13" font-weight="700" fill="#92400E">🏢 US-West (Failover)</text>
  <rect x="418" y="222" width="130" height="45" rx="8" fill="#3B82F6"/>
  <text x="483" y="243" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Servers</text>
  <text x="483" y="258" text-anchor="middle" font-size="9" fill="#BFDBFE">auto-scaled</text>
  <rect x="562" y="222" width="130" height="45" rx="8" fill="#8B5CF6"/>
  <text x="627" y="243" text-anchor="middle" font-size="11" font-weight="600" fill="white">Database</text>
  <text x="627" y="258" text-anchor="middle" font-size="9" fill="#DDD6FE">replica</text>
  <rect x="418" y="282" width="272" height="40" rx="8" fill="#10B981"/>
  <text x="554" y="307" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚡ Cache Cluster</text>
  <!-- Arrows -->
  <line x1="370" y1="65" x2="370" y2="88" stroke="#64748B" stroke-width="2" marker-end="url(#a9)"/>
  <line x1="320" y1="112" x2="215" y2="183" stroke="#64748B" stroke-width="2" marker-end="url(#a9)"/>
  <text x="238" y="148" text-anchor="middle" font-size="10" fill="#475569">70% traffic</text>
  <line x1="420" y1="112" x2="525" y2="183" stroke="#64748B" stroke-width="2" marker-end="url(#a9)"/>
  <text x="502" y="148" text-anchor="middle" font-size="10" fill="#475569">30% traffic</text>
  <!-- Replication between DCs -->
  <line x1="342" y1="310" x2="398" y2="310" stroke="#8B5CF6" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#a9r)"/>
  <line x1="398" y1="326" x2="342" y2="326" stroke="#8B5CF6" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#a9r)"/>
  <text x="370" y="347" text-anchor="middle" font-size="9" fill="#7C3AED">async replication</text>
</svg>

**GeoDNS** routes each user to the nearest data center based on their IP location. If one entire DC goes offline, GeoDNS automatically redirects 100% of traffic to the healthy DC within seconds.

---

## Step 10: Message Queue — Decouple and Scale Independently

Some operations are slow: sending emails, resizing images, indexing documents. If done synchronously, the user waits. If they fail, the user's request fails. A **message queue** solves both problems.

<svg viewBox="0 0 740 280" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a10" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a10o" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#F97316"/></marker>
    <marker id="a10g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
  </defs>
  <rect width="740" height="280" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Producer -->
  <rect x="20" y="90" width="150" height="100" rx="12" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <text x="95" y="115" text-anchor="middle" font-size="11" font-weight="700" fill="#1E40AF">PRODUCER</text>
  <rect x="35" y="124" width="120" height="46" rx="8" fill="#3B82F6"/>
  <text x="95" y="146" text-anchor="middle" font-size="11" font-weight="600" fill="white">🖥 Web Server</text>
  <text x="95" y="162" text-anchor="middle" font-size="9" fill="#BFDBFE">handles user request</text>
  <!-- Instant response to user -->
  <rect x="20" y="210" width="150" height="30" rx="8" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.5"/>
  <text x="95" y="230" text-anchor="middle" font-size="10" fill="#166534">② Returns to user instantly</text>
  <!-- Queue -->
  <rect x="255" y="80" width="230" height="120" rx="14" fill="#FFF7ED" stroke="#FED7AA" stroke-width="2.5"/>
  <text x="370" y="105" text-anchor="middle" font-size="12" font-weight="700" fill="#92400E">📬 Message Queue</text>
  <text x="370" y="122" text-anchor="middle" font-size="10" fill="#B45309">Kafka · RabbitMQ · SQS</text>
  <!-- Messages inside queue -->
  <rect x="270" y="132" width="45" height="30" rx="5" fill="#F97316"/>
  <text x="292" y="152" text-anchor="middle" font-size="10" fill="white">msg</text>
  <rect x="323" y="132" width="45" height="30" rx="5" fill="#F97316"/>
  <text x="345" y="152" text-anchor="middle" font-size="10" fill="white">msg</text>
  <rect x="376" y="132" width="45" height="30" rx="5" fill="#F97316"/>
  <text x="398" y="152" text-anchor="middle" font-size="10" fill="white">msg</text>
  <rect x="429" y="132" width="45" height="30" rx="5" fill="#FED7AA" stroke="#F97316" stroke-dasharray="3,2"/>
  <text x="451" y="152" text-anchor="middle" font-size="10" fill="#92400E">...</text>
  <!-- Workers -->
  <rect x="575" y="50" width="145" height="55" rx="10" fill="#F0FDFA" stroke="#99F6E4" stroke-width="2"/>
  <rect x="590" y="62" width="115" height="34" rx="7" fill="#14B8A6"/>
  <text x="647" y="82" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚙ Worker 1</text>
  <rect x="575" y="118" width="145" height="55" rx="10" fill="#F0FDFA" stroke="#99F6E4" stroke-width="2"/>
  <rect x="590" y="130" width="115" height="34" rx="7" fill="#14B8A6"/>
  <text x="647" y="150" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚙ Worker 2</text>
  <rect x="575" y="186" width="145" height="55" rx="10" fill="#F0FDFA" stroke="#99F6E4" stroke-width="2"/>
  <rect x="590" y="198" width="115" height="34" rx="7" fill="#14B8A6"/>
  <text x="647" y="218" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚙ Worker 3</text>
  <!-- Arrows -->
  <line x1="172" y1="130" x2="253" y2="130" stroke="#F97316" stroke-width="2.5" marker-end="url(#a10o)"/>
  <text x="212" y="120" text-anchor="middle" font-size="9" fill="#EA580C">① publish</text>
  <line x1="487" y1="145" x2="572" y2="85" stroke="#10B981" stroke-width="2" marker-end="url(#a10g)"/>
  <line x1="487" y1="155" x2="572" y2="155" stroke="#10B981" stroke-width="2" marker-end="url(#a10g)"/>
  <line x1="487" y1="162" x2="572" y2="215" stroke="#10B981" stroke-width="2" marker-end="url(#a10g)"/>
  <text x="536" y="132" text-anchor="middle" font-size="9" fill="#059669">③ consume</text>
  <!-- Scale note -->
  <rect x="255" y="218" width="230" height="40" rx="8" fill="#FEF3C7" stroke="#FCD34D" stroke-width="1.5"/>
  <text x="370" y="234" text-anchor="middle" font-size="10" fill="#92400E" font-weight="600">Queue growing? Add more workers.</text>
  <text x="370" y="250" text-anchor="middle" font-size="10" fill="#B45309">Producer and consumer scale independently.</text>
</svg>

**Real-world uses:** email delivery, video transcoding (YouTube), search indexing, push notifications, audit logging.

---

## Step 11: Logging, Metrics, and Automation

<svg viewBox="0 0 740 220" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <rect width="740" height="220" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Logging -->
  <rect x="20" y="30" width="160" height="160" rx="12" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <text x="100" y="58" text-anchor="middle" font-size="24">📋</text>
  <text x="100" y="82" text-anchor="middle" font-size="13" font-weight="700" fill="#1E40AF">Logging</text>
  <text x="100" y="102" text-anchor="middle" font-size="10" fill="#3B82F6">Centralized log</text>
  <text x="100" y="120" text-anchor="middle" font-size="10" fill="#64748B">ELK Stack</text>
  <text x="100" y="138" text-anchor="middle" font-size="10" fill="#64748B">Grafana Loki</text>
  <text x="100" y="156" text-anchor="middle" font-size="10" fill="#64748B">Datadog</text>
  <text x="100" y="176" text-anchor="middle" font-size="9" fill="#94A3B8">Who broke what at 2 AM?</text>
  <!-- Metrics -->
  <rect x="200" y="30" width="160" height="160" rx="12" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2"/>
  <text x="280" y="58" text-anchor="middle" font-size="24">📊</text>
  <text x="280" y="82" text-anchor="middle" font-size="13" font-weight="700" fill="#14532D">Metrics</text>
  <text x="280" y="102" text-anchor="middle" font-size="10" fill="#16A34A">Host: CPU, RAM, Disk</text>
  <text x="280" y="120" text-anchor="middle" font-size="10" fill="#16A34A">System: DB, Cache, LB</text>
  <text x="280" y="138" text-anchor="middle" font-size="10" fill="#16A34A">Business: DAU, Revenue</text>
  <text x="280" y="156" text-anchor="middle" font-size="10" fill="#64748B">Prometheus + Grafana</text>
  <text x="280" y="176" text-anchor="middle" font-size="9" fill="#94A3B8">Is the system healthy?</text>
  <!-- Monitoring -->
  <rect x="380" y="30" width="160" height="160" rx="12" fill="#FFF7ED" stroke="#FED7AA" stroke-width="2"/>
  <text x="460" y="58" text-anchor="middle" font-size="24">🔔</text>
  <text x="460" y="82" text-anchor="middle" font-size="13" font-weight="700" fill="#92400E">Monitoring</text>
  <text x="460" y="102" text-anchor="middle" font-size="10" fill="#B45309">Alerting on thresholds</text>
  <text x="460" y="120" text-anchor="middle" font-size="10" fill="#64748B">PagerDuty</text>
  <text x="460" y="138" text-anchor="middle" font-size="10" fill="#64748B">OpsGenie</text>
  <text x="460" y="156" text-anchor="middle" font-size="10" fill="#64748B">Cloudwatch Alarms</text>
  <text x="460" y="176" text-anchor="middle" font-size="9" fill="#94A3B8">Wake someone up when it breaks</text>
  <!-- Automation -->
  <rect x="560" y="30" width="160" height="160" rx="12" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="2"/>
  <text x="640" y="58" text-anchor="middle" font-size="24">🤖</text>
  <text x="640" y="82" text-anchor="middle" font-size="13" font-weight="700" fill="#4C1D95">Automation</text>
  <text x="640" y="102" text-anchor="middle" font-size="10" fill="#7C3AED">CI/CD pipelines</text>
  <text x="640" y="120" text-anchor="middle" font-size="10" fill="#64748B">Auto Scaling</text>
  <text x="640" y="138" text-anchor="middle" font-size="10" fill="#64748B">Infrastructure as Code</text>
  <text x="640" y="156" text-anchor="middle" font-size="10" fill="#64748B">Terraform / CDK</text>
  <text x="640" y="176" text-anchor="middle" font-size="9" fill="#94A3B8">No manual clicks at 3 AM</text>
</svg>

---

## Step 12: Database Sharding — Scaling the Data Tier

When a single database can't handle write throughput or storage volume, **sharding** splits it into smaller pieces called shards, each on a separate server.

<svg viewBox="0 0 740 320" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a12" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a12g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
  </defs>
  <rect width="740" height="320" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Query input -->
  <rect x="270" y="18" width="200" height="50" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="370" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="#3730A3">Query: user_id = 13</text>
  <text x="370" y="58" text-anchor="middle" font-size="11" fill="#6366F1">Which shard? 13 % 4 = 1 → Shard 1</text>
  <!-- Hash function box -->
  <rect x="290" y="90" width="160" height="40" rx="10" fill="#7C3AED" stroke="#6D28D9" stroke-width="2"/>
  <text x="370" y="116" text-anchor="middle" font-size="13" font-weight="700" fill="white">f(user_id) = user_id % 4</text>
  <!-- Shards -->
  <!-- Shard 0 (grey - not selected) -->
  <rect x="20" y="180" width="155" height="110" rx="12" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="2"/>
  <text x="98" y="205" text-anchor="middle" font-size="13" font-weight="700" fill="#64748B">Shard 0</text>
  <text x="98" y="225" text-anchor="middle" font-size="10" fill="#94A3B8">user_id % 4 = 0</text>
  <text x="98" y="243" text-anchor="middle" font-size="10" fill="#94A3B8">0, 4, 8, 12 ...</text>
  <!-- Shard 1 (highlighted - selected) -->
  <rect x="195" y="168" width="160" height="125" rx="12" fill="#F0FDF4" stroke="#10B981" stroke-width="3"/>
  <text x="275" y="196" text-anchor="middle" font-size="13" font-weight="700" fill="#14532D">Shard 1 ✅</text>
  <text x="275" y="216" text-anchor="middle" font-size="10" fill="#16A34A">user_id % 4 = 1</text>
  <text x="275" y="234" text-anchor="middle" font-size="10" fill="#16A34A" font-weight="600">1, 5, 9, 13 ← here!</text>
  <text x="275" y="252" text-anchor="middle" font-size="10" fill="#16A34A">17, 21 ...</text>
  <rect x="208" y="263" width="134" height="22" rx="6" fill="#10B981"/>
  <text x="275" y="278" text-anchor="middle" font-size="10" fill="white" font-weight="600">Query routed here</text>
  <!-- Shard 2 -->
  <rect x="375" y="180" width="155" height="110" rx="12" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="2"/>
  <text x="453" y="205" text-anchor="middle" font-size="13" font-weight="700" fill="#64748B">Shard 2</text>
  <text x="453" y="225" text-anchor="middle" font-size="10" fill="#94A3B8">user_id % 4 = 2</text>
  <text x="453" y="243" text-anchor="middle" font-size="10" fill="#94A3B8">2, 6, 10, 14 ...</text>
  <!-- Shard 3 -->
  <rect x="550" y="180" width="170" height="110" rx="12" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="2"/>
  <text x="635" y="205" text-anchor="middle" font-size="13" font-weight="700" fill="#64748B">Shard 3</text>
  <text x="635" y="225" text-anchor="middle" font-size="10" fill="#94A3B8">user_id % 4 = 3</text>
  <text x="635" y="243" text-anchor="middle" font-size="10" fill="#94A3B8">3, 7, 11, 15 ...</text>
  <!-- Arrows from hash function -->
  <line x1="340" y1="130" x2="130" y2="178" stroke="#CBD5E1" stroke-width="1.5" marker-end="url(#a12)"/>
  <line x1="360" y1="130" x2="298" y2="166" stroke="#10B981" stroke-width="2.5" marker-end="url(#a12g)"/>
  <line x1="390" y1="130" x2="463" y2="178" stroke="#CBD5E1" stroke-width="1.5" marker-end="url(#a12)"/>
  <line x1="410" y1="130" x2="590" y2="178" stroke="#CBD5E1" stroke-width="1.5" marker-end="url(#a12)"/>
</svg>

**Sharding challenges:**
- **Resharding** — if one shard fills up faster, you must redistribute data. Consistent hashing minimizes movement.
- **Celebrity problem** — a user with 100M followers overwhelms a single shard. Solution: dedicate a shard to hotspot keys.
- **Cross-shard joins** — JOINs across shards are expensive. Denormalize your schema to avoid them.

---

## The Full Architecture: Zero to Millions

<svg viewBox="0 0 740 580" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="af" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
  </defs>
  <rect width="740" height="580" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Layer labels -->
  <text x="14" y="60" font-size="9" fill="#94A3B8" transform="rotate(-90,14,60)">EDGE</text>
  <text x="14" y="140" font-size="9" fill="#94A3B8" transform="rotate(-90,14,140)">LB</text>
  <text x="14" y="230" font-size="9" fill="#94A3B8" transform="rotate(-90,14,230)">WEB</text>
  <text x="14" y="330" font-size="9" fill="#94A3B8" transform="rotate(-90,14,330)">CACHE/MQ</text>
  <text x="14" y="450" font-size="9" fill="#94A3B8" transform="rotate(-90,14,450)">DATA</text>
  <text x="14" y="545" font-size="9" fill="#94A3B8" transform="rotate(-90,14,545)">OPS</text>
  <!-- Row 1: Users + CDN + DNS -->
  <rect x="30" y="18" width="100" height="48" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="80" y="36" text-anchor="middle" font-size="18">👥</text>
  <text x="80" y="56" text-anchor="middle" font-size="10" font-weight="600" fill="#3730A3">Users</text>
  <rect x="300" y="18" width="140" height="48" rx="10" fill="#FDF2F8" stroke="#F9A8D4" stroke-width="2"/>
  <text x="370" y="38" text-anchor="middle" font-size="11" font-weight="700" fill="#9D174D">⚡ CDN</text>
  <text x="370" y="56" text-anchor="middle" font-size="9" fill="#BE185D">Static assets · Global edge</text>
  <rect x="590" y="18" width="120" height="48" rx="10" fill="#FFFBEB" stroke="#FCD34D" stroke-width="2"/>
  <text x="650" y="38" text-anchor="middle" font-size="11" font-weight="700" fill="#92400E">🌐 GeoDNS</text>
  <text x="650" y="56" text-anchor="middle" font-size="9" fill="#B45309">Routes by location</text>
  <!-- Row 2: Load Balancer -->
  <rect x="270" y="100" width="200" height="45" rx="12" fill="#0E7490" stroke="#06B6D4" stroke-width="2.5"/>
  <text x="370" y="120" text-anchor="middle" font-size="12" font-weight="700" fill="white">⚖  Load Balancer</text>
  <text x="370" y="137" text-anchor="middle" font-size="9" fill="#A5F3FC">Round-robin · Health checks · Failover</text>
  <!-- Row 3: Web Servers -->
  <rect x="80" y="180" width="115" height="52" rx="10" fill="#3B82F6"/>
  <text x="138" y="201" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Server 1</text>
  <text x="138" y="220" text-anchor="middle" font-size="9" fill="#BFDBFE">stateless</text>
  <rect x="313" y="180" width="115" height="52" rx="10" fill="#3B82F6"/>
  <text x="370" y="201" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Server 2</text>
  <text x="370" y="220" text-anchor="middle" font-size="9" fill="#BFDBFE">stateless</text>
  <rect x="546" y="180" width="115" height="52" rx="10" fill="#60A5FA" stroke="#3B82F6" stroke-dasharray="5,3" stroke-width="2"/>
  <text x="603" y="201" text-anchor="middle" font-size="11" font-weight="600" fill="#1E3A8A">Web Server N</text>
  <text x="603" y="220" text-anchor="middle" font-size="9" fill="#1D4ED8">auto-scaled</text>
  <!-- Row 4: Cache + MQ -->
  <rect x="80" y="272" width="160" height="65" rx="12" fill="#10B981"/>
  <text x="160" y="296" text-anchor="middle" font-size="12" font-weight="700" fill="white">⚡ Cache</text>
  <text x="160" y="314" text-anchor="middle" font-size="9" fill="#D1FAE5">Redis · Memcached</text>
  <text x="160" y="330" text-anchor="middle" font-size="9" fill="#D1FAE5">LRU · TTL</text>
  <rect x="500" y="272" width="200" height="65" rx="12" fill="#F97316"/>
  <text x="600" y="296" text-anchor="middle" font-size="12" font-weight="700" fill="white">📬 Message Queue</text>
  <text x="600" y="314" text-anchor="middle" font-size="9" fill="#FEF3C7">Kafka · RabbitMQ · SQS</text>
  <text x="600" y="330" text-anchor="middle" font-size="9" fill="#FEF3C7">Async · Decoupled</text>
  <!-- Row 5: Databases + Workers + NoSQL -->
  <rect x="30" y="385" width="170" height="75" rx="12" fill="#7C3AED" stroke="#6D28D9" stroke-width="2"/>
  <text x="115" y="410" text-anchor="middle" font-size="11" font-weight="700" fill="white">Master DB</text>
  <text x="115" y="428" text-anchor="middle" font-size="9" fill="#DDD6FE">Writes · Primary</text>
  <text x="115" y="446" text-anchor="middle" font-size="9" fill="#DDD6FE">MySQL · PostgreSQL</text>
  <rect x="220" y="385" width="140" height="75" rx="12" fill="#6D28D9" stroke="#8B5CF6" stroke-width="2"/>
  <text x="290" y="410" text-anchor="middle" font-size="11" font-weight="700" fill="white">Slave DBs</text>
  <text x="290" y="428" text-anchor="middle" font-size="9" fill="#DDD6FE">Reads · Replicas</text>
  <text x="290" y="446" text-anchor="middle" font-size="9" fill="#DDD6FE">x3 read throughput</text>
  <rect x="380" y="385" width="160" height="75" rx="12" fill="#14B8A6"/>
  <text x="460" y="410" text-anchor="middle" font-size="11" font-weight="700" fill="white">⚙ Workers</text>
  <text x="460" y="428" text-anchor="middle" font-size="9" fill="#CCFBF1">Async processing</text>
  <text x="460" y="446" text-anchor="middle" font-size="9" fill="#CCFBF1">Email · Images · Index</text>
  <rect x="560" y="385" width="150" height="75" rx="12" fill="#84CC16"/>
  <text x="635" y="410" text-anchor="middle" font-size="11" font-weight="700" fill="white">NoSQL Store</text>
  <text x="635" y="428" text-anchor="middle" font-size="9" fill="#F7FEE7">Unstructured data</text>
  <text x="635" y="446" text-anchor="middle" font-size="9" fill="#F7FEE7">Cassandra · Dynamo</text>
  <!-- Row 6: Observability -->
  <rect x="30" y="500" width="680" height="55" rx="12" fill="#1E293B"/>
  <text x="370" y="520" text-anchor="middle" font-size="11" font-weight="700" fill="white">📋 Logging</text>
  <text x="370" y="520" text-anchor="middle" font-size="11" fill="white" dx="-170">📊 Metrics</text>
  <text x="370" y="520" text-anchor="middle" font-size="11" fill="white" dx="160">🔔 Monitoring</text>
  <text x="370" y="542" text-anchor="middle" font-size="10" fill="#94A3B8">Prometheus · Grafana · ELK · Datadog · PagerDuty</text>
  <!-- Connecting arrows -->
  <line x1="80" y1="66" x2="300" y2="35" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="130" y1="66" x2="589" y2="40" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="370" y1="66" x2="370" y2="98" stroke="#64748B" stroke-width="2" marker-end="url(#af)"/>
  <line x1="330" y1="145" x2="195" y2="178" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="370" y1="145" x2="370" y2="178" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="410" y1="145" x2="545" y2="178" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="160" y1="232" x2="160" y2="270" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="370" y1="232" x2="200" y2="270" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="600" y1="232" x2="620" y2="270" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="160" y1="337" x2="115" y2="383" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="600" y1="337" x2="460" y2="383" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="635" y1="337" x2="635" y2="383" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
</svg>

---

## Summary: The 7 Principles of Scalable Systems

| Principle | What It Means |
|-----------|---------------|
| **Keep web servers stateless** | Store sessions in shared storage. Any server must handle any request. |
| **Build redundancy at every tier** | No single point of failure — load balancers, DB replicas, multi-region. |
| **Cache aggressively** | CDN for static assets, Redis for dynamic data, DB query cache. |
| **Support multiple data centers** | Geographic redundancy survives regional outages. |
| **Use a CDN for static assets** | Serve images, CSS, JS from edge nodes — not your origin server. |
| **Scale the data tier by sharding** | Partition by a key that distributes load evenly. |
| **Use message queues for async work** | Decouple producers from consumers. |

---

## What's Next

In the next post: **Back-of-the-Envelope Estimation** — how to calculate QPS, storage, and bandwidth before designing a system. The skill that separates engineers who guess from engineers who reason.

---

*Based on Chapter 1 of "System Design Interview" by Alex Xu, with additional diagrams and context.*
