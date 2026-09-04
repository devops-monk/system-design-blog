---
title: "Scale From Zero to Millions of Users: A Complete System Design Walkthrough"
description: "Learn how to evolve a system from a single server all the way to supporting millions of users. Covers databases, load balancers, caching, CDN, stateless architecture, data centers, message queues, and database sharding — step by step with diagrams."
author: Abhay
type: post
date: 2026-05-29T00:00:00+00:00
url: /2026/05/scale-from-zero-to-millions/
image: /images/articles/scale-from-zero-to-millions.webp
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

Designing a system that supports millions of users is challenging — it is a journey that requires continuous refinement and endless improvement. In this post, we build a system that supports a single user and gradually scale it up to serve millions of users. After reading this, you will master a handful of techniques that will help you crack system design interview questions.

A journey of a thousand miles begins with a single step. Building a complex system is no different.

---

## Step 1: The Single Server Setup

To start with something simple, everything runs on a single server — web app, database, and cache all on the same machine.

<svg viewBox="0 0 740 380" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a1" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a1g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
  </defs>
  <rect width="740" height="380" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="20" y="70" width="150" height="120" rx="12" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="95" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#3730A3">USER</text>
  <rect x="34" y="102" width="46" height="32" rx="5" fill="#4F46E5"/>
  <rect x="36" y="104" width="42" height="8" rx="2" fill="#818CF8"/>
  <text x="57" y="128" text-anchor="middle" font-size="9" fill="#C7D2FE">Browser</text>
  <rect x="100" y="100" width="26" height="36" rx="5" fill="#6366F1"/>
  <rect x="106" y="106" width="14" height="16" rx="2" fill="#A5B4FC"/>
  <text x="113" y="130" text-anchor="middle" font-size="9" fill="#C7D2FE">App</text>
  <circle cx="370" cy="105" r="52" fill="#FFFBEB" stroke="#FCD34D" stroke-width="2"/>
  <ellipse cx="370" cy="105" rx="22" ry="52" fill="none" stroke="#FCD34D" stroke-width="1.5"/>
  <line x1="318" y1="105" x2="422" y2="105" stroke="#FCD34D" stroke-width="1.5"/>
  <line x1="328" y1="78" x2="412" y2="78" stroke="#FCD34D" stroke-width="1"/>
  <line x1="328" y1="132" x2="412" y2="132" stroke="#FCD34D" stroke-width="1"/>
  <text x="370" y="99" text-anchor="middle" font-size="13" font-weight="700" fill="#92400E">DNS</text>
  <text x="370" y="117" text-anchor="middle" font-size="10" fill="#B45309">api.mysite.com</text>
  <rect x="540" y="45" width="180" height="300" rx="14" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2.5"/>
  <text x="630" y="70" text-anchor="middle" font-size="13" font-weight="700" fill="#14532D">Single Server</text>
  <rect x="556" y="82" width="148" height="60" rx="10" fill="#3B82F6"/>
  <text x="630" y="108" text-anchor="middle" font-size="12" font-weight="600" fill="white">🖥  Web Server</text>
  <text x="630" y="128" text-anchor="middle" font-size="10" fill="#BFDBFE">App logic · HTTP</text>
  <rect x="556" y="156" width="148" height="60" rx="10" fill="#8B5CF6"/>
  <text x="630" y="182" text-anchor="middle" font-size="12" font-weight="600" fill="white">🗄  Database</text>
  <text x="630" y="202" text-anchor="middle" font-size="10" fill="#DDD6FE">All data storage</text>
  <rect x="556" y="230" width="148" height="60" rx="10" fill="#F59E0B"/>
  <text x="630" y="256" text-anchor="middle" font-size="12" font-weight="600" fill="white">⚡  Cache</text>
  <text x="630" y="276" text-anchor="middle" font-size="10" fill="#FEF3C7">In-memory store</text>
  <rect x="540" y="355" width="180" height="26" rx="8" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.5"/>
  <text x="630" y="372" text-anchor="middle" font-size="11" font-weight="600" fill="#DC2626">⚠ Single Point of Failure</text>
  <line x1="172" y1="95" x2="315" y2="98" stroke="#64748B" stroke-width="2" marker-end="url(#a1)"/>
  <text x="243" y="87" text-anchor="middle" font-size="10" fill="#475569">① DNS query</text>
  <line x1="315" y1="112" x2="172" y2="115" stroke="#10B981" stroke-width="2" marker-end="url(#a1g)"/>
  <text x="243" y="130" text-anchor="middle" font-size="10" fill="#10B981">② IP: 15.125.23.214</text>
  <path d="M 170 148 C 300 210 420 195 537 165" fill="none" stroke="#64748B" stroke-width="2" marker-end="url(#a1)"/>
  <text x="350" y="210" text-anchor="middle" font-size="10" fill="#475569">③ HTTP Request</text>
  <path d="M 537 215 C 420 290 300 275 170 175" fill="none" stroke="#10B981" stroke-width="2" marker-end="url(#a1g)"/>
  <text x="350" y="295" text-anchor="middle" font-size="10" fill="#10B981">④ HTML / JSON Response</text>
</svg>

### How the request flow works

To understand this setup, let's trace every step of a single request:

1. **Users access websites through domain names** such as `api.mysite.com`. The Domain Name System (DNS) is a paid service provided by third parties and not hosted on our servers. DNS translates human-readable domain names into numeric IP addresses.

2. **An IP address is returned** to the browser or mobile app. In the example, IP address `15.125.23.214` is returned.

3. **Once the IP address is obtained**, Hypertext Transfer Protocol (HTTP) requests are sent directly to your web server.

4. **The web server returns** HTML pages or JSON responses for rendering.

### Where traffic comes from

Traffic to your web server comes from two sources: **web applications** and **mobile applications**.

- **Web application** — it uses a combination of server-side languages (Java, Python, etc.) to handle business logic and storage, and client-side languages (HTML + JavaScript) for presentation in the browser.

- **Mobile application** — HTTP is the communication protocol between the mobile app and the web server. JavaScript Object Notation (JSON) is the most commonly used API response format due to its simplicity. Here is an example:

```json
GET /users/12

{
  "id": 12,
  "firstName": "John",
  "lastName": "Smith",
  "address": {
    "streetAddress": "21 2nd Street",
    "city": "New York",
    "state": "NY",
    "postalCode": 10021
  },
  "phoneNumbers": ["212 555-1234", "646 555-4567"]
}
```

### What breaks first on a single server

A single server is fine for development and early-stage products. Two problems emerge as traffic grows:

- **No separation of concerns** — the web server and database compete for the same CPU and RAM. A traffic spike starves the database of resources, and vice versa. You cannot scale them independently.
- **No redundancy** — if this one server crashes, your entire product is offline. Every user gets an error until you restart it. This is called a **Single Point of Failure (SPOF)**.

The fix for the first problem: separate the web tier from the data tier.

---

## Step 2: Separating the Database

With the growth of your user base, one server is no longer enough. We need multiple servers: one for web/mobile traffic, the other for the database. Separating web/mobile traffic (web tier) and database (data tier) servers allows them to be **scaled independently**.

<svg viewBox="0 0 740 240" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a2" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
  </defs>
  <rect width="740" height="240" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="30" y="80" width="120" height="80" rx="12" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="90" y="115" text-anchor="middle" font-size="28">👤</text>
  <text x="90" y="148" text-anchor="middle" font-size="12" font-weight="600" fill="#3730A3">User</text>
  <rect x="240" y="60" width="160" height="120" rx="12" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <text x="320" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#1E40AF">WEB TIER</text>
  <rect x="258" y="98" width="124" height="52" rx="8" fill="#3B82F6"/>
  <text x="320" y="121" text-anchor="middle" font-size="12" font-weight="600" fill="white">🖥  Web Server</text>
  <text x="320" y="139" text-anchor="middle" font-size="10" fill="#BFDBFE">App logic · HTTP</text>
  <text x="320" y="196" text-anchor="middle" font-size="10" fill="#64748B">Scale independently ↕</text>
  <rect x="510" y="60" width="205" height="120" rx="12" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="2"/>
  <text x="612" y="88" text-anchor="middle" font-size="11" font-weight="700" fill="#4C1D95">DATA TIER</text>
  <rect x="528" y="98" width="169" height="52" rx="8" fill="#8B5CF6"/>
  <text x="612" y="121" text-anchor="middle" font-size="12" font-weight="600" fill="white">🗄  Database Server</text>
  <text x="612" y="139" text-anchor="middle" font-size="10" fill="#DDD6FE">Storage · Indexing · Queries</text>
  <text x="612" y="196" text-anchor="middle" font-size="10" fill="#64748B">Scale independently ↕</text>
  <line x1="152" y1="120" x2="237" y2="120" stroke="#64748B" stroke-width="2" marker-end="url(#a2)"/>
  <line x1="402" y1="108" x2="507" y2="108" stroke="#64748B" stroke-width="2" marker-end="url(#a2)"/>
  <text x="455" y="100" text-anchor="middle" font-size="10" fill="#475569">read / write</text>
  <line x1="507" y1="130" x2="402" y2="130" stroke="#64748B" stroke-width="2" marker-end="url(#a2)"/>
  <text x="455" y="148" text-anchor="middle" font-size="10" fill="#475569">return data</text>
</svg>

### Which database should you use?

You can choose between a **relational database** and a **non-relational database**.

**Relational databases (SQL)** are also called RDBMS or SQL databases. The most popular ones are MySQL, Oracle, and PostgreSQL. Relational databases represent and store data in tables and rows. You can perform JOIN operations across different tables using SQL. Relational databases have been around for over 40 years and have worked well historically — they are the best default choice for most developers.

**Non-relational databases (NoSQL)** — popular ones include CouchDB, Neo4j, Cassandra, HBase, and Amazon DynamoDB. These databases are grouped into four categories:
- **Key-value stores** — Redis, Memcached
- **Graph stores** — Neo4j
- **Column stores** — Cassandra, HBase
- **Document stores** — MongoDB, CouchDB

Join operations are generally **not supported** in non-relational databases. Non-relational databases might be the right choice if:

- Your application requires **super-low latency** (sub-millisecond response)
- Your data is **unstructured**, or you do not have any relational data
- You only need to **serialize and deserialize** data (JSON, XML, YAML)
- You need to store a **massive amount of data** that doesn't fit on a single machine

For everything else, start with PostgreSQL or MySQL. They are proven, well-understood, and their consistency guarantees prevent entire classes of bugs that NoSQL databases can introduce.

---

## Step 3: Vertical Scaling vs. Horizontal Scaling

When your single web server starts struggling under load, you have two paths forward.

<svg viewBox="0 0 740 360" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a3" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#475569"/></marker>
  </defs>
  <rect width="740" height="360" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <line x1="370" y1="20" x2="370" y2="340" stroke="#E2E8F0" stroke-width="2" stroke-dasharray="6,4"/>
  <!-- LEFT PANEL: servers drawn first, then text on top -->
  <rect x="60" y="105" width="60" height="80" rx="8" fill="#CBD5E1" stroke="#94A3B8" stroke-width="2"/>
  <text x="90" y="141" text-anchor="middle" font-size="9" fill="#475569">2 CPU</text>
  <text x="90" y="155" text-anchor="middle" font-size="9" fill="#475569">4 GB RAM</text>
  <rect x="145" y="85" width="80" height="100" rx="8" fill="#93C5FD" stroke="#60A5FA" stroke-width="2"/>
  <text x="185" y="131" text-anchor="middle" font-size="9" fill="#1E40AF">8 CPU</text>
  <text x="185" y="145" text-anchor="middle" font-size="9" fill="#1E40AF">32 GB RAM</text>
  <rect x="252" y="55" width="100" height="130" rx="8" fill="#3B82F6" stroke="#2563EB" stroke-width="2"/>
  <text x="302" y="111" text-anchor="middle" font-size="9" fill="white">64 CPU</text>
  <text x="302" y="127" text-anchor="middle" font-size="9" fill="white">512 GB RAM</text>
  <line x1="122" y1="145" x2="143" y2="140" stroke="#475569" stroke-width="1.5" marker-end="url(#a3)"/>
  <line x1="227" y1="128" x2="250" y2="118" stroke="#475569" stroke-width="1.5" marker-end="url(#a3)"/>
  <!-- Text rendered AFTER boxes so it shows on top -->
  <text x="185" y="38" text-anchor="middle" font-size="14" font-weight="700" fill="#1E293B">⬆ Vertical Scaling</text>
  <text x="185" y="58" text-anchor="middle" font-size="11" fill="#64748B">"Scale Up" — bigger machine</text>
  <rect x="30" y="205" width="325" height="30" rx="6" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.5"/>
  <text x="192" y="224" text-anchor="middle" font-size="11" fill="#DC2626" font-weight="600">⚠ Hardware ceiling · No failover</text>
  <text x="192" y="260" text-anchor="middle" font-size="10" fill="#16A34A">✓ Simple — no code changes needed</text>
  <text x="192" y="280" text-anchor="middle" font-size="10" fill="#DC2626">✗ Cannot add unlimited CPU/RAM</text>
  <text x="192" y="300" text-anchor="middle" font-size="10" fill="#DC2626">✗ If server goes down, site goes down</text>
  <text x="192" y="320" text-anchor="middle" font-size="10" fill="#DC2626">✗ No failover and redundancy</text>
  <!-- RIGHT PANEL: servers first, text on top -->
  <rect x="390" y="100" width="70" height="60" rx="8" fill="#3B82F6" stroke="#2563EB" stroke-width="2"/>
  <text x="425" y="135" text-anchor="middle" font-size="10" fill="white">Server 1</text>
  <rect x="475" y="100" width="70" height="60" rx="8" fill="#3B82F6" stroke="#2563EB" stroke-width="2"/>
  <text x="510" y="135" text-anchor="middle" font-size="10" fill="white">Server 2</text>
  <rect x="560" y="100" width="70" height="60" rx="8" fill="#3B82F6" stroke="#2563EB" stroke-width="2"/>
  <text x="595" y="135" text-anchor="middle" font-size="10" fill="white">Server 3</text>
  <rect x="645" y="100" width="70" height="60" rx="8" fill="#93C5FD" stroke="#60A5FA" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="680" y="128" text-anchor="middle" font-size="10" fill="#1E40AF">Server</text>
  <text x="680" y="144" text-anchor="middle" font-size="10" fill="#1E40AF">N+1...</text>
  <!-- Text on top -->
  <text x="555" y="38" text-anchor="middle" font-size="14" font-weight="700" fill="#1E293B">➡ Horizontal Scaling</text>
  <text x="555" y="58" text-anchor="middle" font-size="11" fill="#64748B">"Scale Out" — more machines</text>
  <rect x="380" y="185" width="345" height="30" rx="6" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.5"/>
  <text x="552" y="204" text-anchor="middle" font-size="11" fill="#16A34A" font-weight="600">✓ No ceiling · Redundancy built-in</text>
  <text x="552" y="240" text-anchor="middle" font-size="10" fill="#16A34A">✓ Add more servers as traffic grows</text>
  <text x="552" y="260" text-anchor="middle" font-size="10" fill="#16A34A">✓ Traffic routed away from failed servers</text>
  <text x="552" y="280" text-anchor="middle" font-size="10" fill="#16A34A">✓ Each server can be replaced independently</text>
  <text x="552" y="300" text-anchor="middle" font-size="10" fill="#DC2626">✗ Requires stateless application design</text>
</svg>

**Vertical scaling** — referred to as "scale up" — means adding more power (CPU, RAM) to your existing server. When traffic is low, vertical scaling is a great option and its main advantage is simplicity.

Unfortunately, vertical scaling comes with **serious limitations**:
- Vertical scaling has a **hard limit**. It is impossible to add unlimited CPU and memory to a single server.
- Vertical scaling does **not have failover and redundancy**. If one server goes down, the website/app goes down completely.

**Horizontal scaling** — referred to as "scale out" — allows you to scale by adding more servers into your pool of resources. It is more desirable for large-scale applications due to the limitations of vertical scaling.

In the previous single-server design, users are connected to the web server directly. Users are unable to access the website if the web server is offline. In another scenario, if many users access the web server simultaneously and it reaches its load limit, users experience slower responses or fail to connect. **A load balancer is the best technique to address these problems.**

---

## Step 4: Load Balancer — Distributing Traffic Across Servers

A load balancer evenly distributes incoming traffic among web servers that are defined in a load-balanced set.

<svg viewBox="0 0 740 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a4" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a4r" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#EF4444"/></marker>
  </defs>
  <rect width="740" height="400" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="290" y="18" width="160" height="55" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="370" y="42" text-anchor="middle" font-size="22">👥</text>
  <text x="370" y="64" text-anchor="middle" font-size="11" font-weight="600" fill="#3730A3">Users</text>
  <rect x="265" y="110" width="210" height="65" rx="12" fill="#0E7490" stroke="#06B6D4" stroke-width="2.5"/>
  <text x="370" y="136" text-anchor="middle" font-size="13" font-weight="700" fill="white">⚖  Load Balancer</text>
  <text x="370" y="156" text-anchor="middle" font-size="10" fill="#A5F3FC">Public IP: 88.88.88.1</text>
  <rect x="100" y="240" width="170" height="80" rx="12" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <rect x="115" y="258" width="140" height="46" rx="8" fill="#3B82F6"/>
  <text x="185" y="279" text-anchor="middle" font-size="12" font-weight="600" fill="white">🖥  Server 1</text>
  <text x="185" y="297" text-anchor="middle" font-size="10" fill="#BFDBFE">Private IP: 10.0.0.1</text>
  <rect x="470" y="240" width="170" height="80" rx="12" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <rect x="485" y="258" width="140" height="46" rx="8" fill="#3B82F6"/>
  <text x="555" y="279" text-anchor="middle" font-size="12" font-weight="600" fill="white">🖥  Server 2</text>
  <text x="555" y="297" text-anchor="middle" font-size="10" fill="#BFDBFE">Private IP: 10.0.0.2</text>
  <rect x="265" y="355" width="210" height="35" rx="10" fill="#8B5CF6"/>
  <text x="370" y="377" text-anchor="middle" font-size="12" font-weight="600" fill="white">🗄  Database</text>
  <line x1="370" y1="74" x2="370" y2="108" stroke="#64748B" stroke-width="2" marker-end="url(#a4)"/>
  <line x1="300" y1="168" x2="220" y2="238" stroke="#06B6D4" stroke-width="2" marker-end="url(#a4)"/>
  <text x="240" y="208" text-anchor="middle" font-size="10" fill="#0E7490">route</text>
  <line x1="440" y1="168" x2="520" y2="238" stroke="#06B6D4" stroke-width="2" marker-end="url(#a4)"/>
  <text x="500" y="208" text-anchor="middle" font-size="10" fill="#0E7490">route</text>
  <line x1="210" y1="322" x2="300" y2="353" stroke="#64748B" stroke-width="1.5" marker-end="url(#a4)"/>
  <line x1="530" y1="322" x2="442" y2="353" stroke="#64748B" stroke-width="1.5" marker-end="url(#a4)"/>
  <rect x="20" y="244" width="75" height="44" rx="8" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.5"/>
  <text x="57" y="262" text-anchor="middle" font-size="9" fill="#DC2626" font-weight="600">Server 1</text>
  <text x="57" y="278" text-anchor="middle" font-size="9" fill="#DC2626">offline →</text>
  <path d="M 93 268 Q 160 268 175 258" fill="none" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#a4r)"/>
  <text x="57" y="300" text-anchor="middle" font-size="9" fill="#DC2626">100% → S2</text>
</svg>

As shown above, users connect to the **public IP of the load balancer directly**. With this setup, web servers are unreachable directly by clients anymore.

For better security, **private IPs** are used for communication between servers. A private IP is an IP address reachable only between servers in the same network — it is unreachable over the public internet. The load balancer communicates with web servers through these private IPs.

After adding a load balancer and a second web server, we successfully solve the no-failover problem and improve the availability of the web tier:

- **If server 1 goes offline**, all traffic is routed to server 2. This prevents the website from going offline. We also add a new healthy web server to the pool to balance the load.
- **If the website traffic grows rapidly** and two servers are not enough, the load balancer can handle this gracefully. You only need to add more servers to the web server pool, and the load balancer automatically starts sending requests to them.

The most common load balancing strategy is **round-robin** (1→2→1→2). More sophisticated strategies: **least connections** (route to the server with fewest active connections), **IP hash** (same client always hits same server), **weighted round-robin** (send more traffic to more powerful servers).

Now the web tier looks good. What about the data tier? The current design has one database, so it does not support failover and redundancy. Database replication is a common technique to address this problem.

---

## Step 5: Database Replication — Surviving Database Failures

*"Database replication can be used in many database management systems, usually with a master/slave relationship between the original (master) and the copies (slaves)."*

<svg viewBox="0 0 740 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a5w" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#EF4444"/></marker>
    <marker id="a5r" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
    <marker id="a5p" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#8B5CF6"/></marker>
  </defs>
  <rect width="740" height="400" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="235" y="18" width="270" height="55" rx="10" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <text x="370" y="38" text-anchor="middle" font-size="11" font-weight="700" fill="#1E40AF">WEB SERVERS</text>
  <rect x="248" y="44" width="75" height="20" rx="5" fill="#3B82F6"/>
  <text x="285" y="58" text-anchor="middle" font-size="9" fill="white">Server 1</text>
  <rect x="333" y="44" width="75" height="20" rx="5" fill="#3B82F6"/>
  <text x="370" y="58" text-anchor="middle" font-size="9" fill="white">Server 2</text>
  <rect x="418" y="44" width="75" height="20" rx="5" fill="#3B82F6"/>
  <text x="455" y="58" text-anchor="middle" font-size="9" fill="white">Server 3</text>
  <rect x="55" y="155" width="185" height="95" rx="14" fill="#7C3AED" stroke="#6D28D9" stroke-width="2.5"/>
  <text x="147" y="185" text-anchor="middle" font-size="14" font-weight="700" fill="white">Master DB</text>
  <text x="147" y="207" text-anchor="middle" font-size="10" fill="#DDD6FE">INSERT / UPDATE / DELETE</text>
  <text x="147" y="225" text-anchor="middle" font-size="9" fill="#C4B5FD">All writes land here first</text>
  <rect x="465" y="120" width="160" height="70" rx="12" fill="#6D28D9" stroke="#8B5CF6" stroke-width="2"/>
  <text x="545" y="150" text-anchor="middle" font-size="12" font-weight="600" fill="white">Slave DB 1</text>
  <text x="545" y="170" text-anchor="middle" font-size="10" fill="#DDD6FE">SELECT (reads only)</text>
  <rect x="465" y="210" width="160" height="70" rx="12" fill="#6D28D9" stroke="#8B5CF6" stroke-width="2"/>
  <text x="545" y="240" text-anchor="middle" font-size="12" font-weight="600" fill="white">Slave DB 2</text>
  <text x="545" y="260" text-anchor="middle" font-size="10" fill="#DDD6FE">SELECT (reads only)</text>
  <rect x="465" y="300" width="160" height="70" rx="12" fill="#6D28D9" stroke="#8B5CF6" stroke-width="2"/>
  <text x="545" y="330" text-anchor="middle" font-size="12" font-weight="600" fill="white">Slave DB 3</text>
  <text x="545" y="350" text-anchor="middle" font-size="10" fill="#DDD6FE">SELECT (reads only)</text>
  <line x1="268" y1="74" x2="185" y2="153" stroke="#EF4444" stroke-width="2.5" marker-end="url(#a5w)"/>
  <text x="200" y="118" text-anchor="middle" font-size="10" font-weight="600" fill="#EF4444">WRITES</text>
  <line x1="242" y1="185" x2="463" y2="152" stroke="#8B5CF6" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#a5p)"/>
  <text x="355" y="160" text-anchor="middle" font-size="9" fill="#7C3AED">replicate</text>
  <line x1="242" y1="200" x2="463" y2="245" stroke="#8B5CF6" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#a5p)"/>
  <text x="355" y="232" text-anchor="middle" font-size="9" fill="#7C3AED">replicate</text>
  <line x1="200" y1="250" x2="463" y2="330" stroke="#8B5CF6" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#a5p)"/>
  <text x="320" y="312" text-anchor="middle" font-size="9" fill="#7C3AED">replicate</text>
  <line x1="463" y1="142" x2="460" y2="74" stroke="#10B981" stroke-width="2" marker-end="url(#a5r)"/>
  <text x="492" y="108" text-anchor="middle" font-size="10" font-weight="600" fill="#10B981">READS</text>
</svg>

A **master database** generally only supports write operations (INSERT, UPDATE, DELETE). A **slave database** gets copies of the data from the master and only supports read operations (SELECT). All data-modifying commands must be sent to the master database. Most applications require a much higher ratio of reads to writes — thus, the number of slave databases in a system is usually larger than the number of master databases.

### Advantages of database replication

- **Better performance** — In the master-slave model, all writes and updates happen in master nodes, whereas read operations are distributed across slave nodes. This model improves performance because it allows more queries to be processed in parallel.
- **Reliability** — If one of your database servers is destroyed by a natural disaster such as a typhoon or an earthquake, data is still preserved. You do not need to worry about data loss because data is replicated across multiple locations.
- **High availability** — By replicating data across different locations, your website remains in operation even if a database is offline, as you can access data stored in another database server.

### What happens when a database goes offline?

**If only one slave database is available and it goes offline**, read operations will be directed to the master database temporarily. As soon as the issue is found, a new slave database will replace the old one. In case multiple slave databases are available, read operations are redirected to other healthy slave databases.

**If the master database goes offline**, a slave database will be promoted to be the new master. All database operations will be temporarily executed on the new master. A new slave database will replace the old one for data replication immediately. In production systems, promoting a new master is more complex because the data in a slave database might not be up to date — the missing data needs to be updated by running data recovery scripts. Although more complex replication methods like multi-master and circular replication could help, those setups are beyond the scope of this tutorial.

After adding the load balancer and database replication, the overall request flow is:
1. A user gets the IP address of the load balancer from DNS
2. A user connects to the load balancer with this IP address
3. The HTTP request is routed to either Server 1 or Server 2
4. A web server reads user data from a slave database
5. A web server routes any data-modifying operations to the master database (write, update, delete)

Now it is time to improve the load and response time. This can be done by adding a **cache layer** and shifting static content (JS/CSS/image/video files) to a **CDN**.

---

## Step 6: Cache — Stop Hitting the Database for the Same Data

A cache is a temporary storage area that stores the result of expensive responses or frequently accessed data in memory so that subsequent requests are served more quickly.

Every time a new web page loads, one or more database calls are executed to fetch data. The application performance is greatly affected by calling the database repeatedly. The cache can mitigate this problem.

The **cache tier** is a temporary data store layer, much faster than the database. The benefits of having a separate cache tier include:
- Better system performance
- Ability to reduce database workload
- Ability to scale the cache tier independently

<svg viewBox="0 0 740 360" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a6g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
    <marker id="a6" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a6o" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#F97316"/></marker>
  </defs>
  <rect width="740" height="360" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="15" y="15" width="340" height="330" rx="12" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2"/>
  <text x="185" y="42" text-anchor="middle" font-size="13" font-weight="700" fill="#14532D">✅  Cache HIT</text>
  <text x="185" y="60" text-anchor="middle" font-size="10" fill="#166534">Data found in cache — no DB query needed</text>
  <rect x="40" y="80" width="120" height="55" rx="10" fill="#3B82F6"/>
  <text x="100" y="104" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Server</text>
  <text x="100" y="124" text-anchor="middle" font-size="9" fill="#BFDBFE">receives request</text>
  <rect x="210" y="80" width="120" height="55" rx="10" fill="#10B981"/>
  <text x="270" y="104" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚡ Cache</text>
  <text x="270" y="124" text-anchor="middle" font-size="9" fill="#D1FAE5">data found!</text>
  <rect x="210" y="215" width="120" height="55" rx="10" fill="#E2E8F0"/>
  <text x="270" y="239" text-anchor="middle" font-size="11" fill="#94A3B8">Database</text>
  <text x="270" y="259" text-anchor="middle" font-size="9" fill="#CBD5E1">not contacted</text>
  <line x1="162" y1="100" x2="208" y2="100" stroke="#10B981" stroke-width="2" marker-end="url(#a6g)"/>
  <text x="185" y="92" text-anchor="middle" font-size="9" fill="#16A34A">① check</text>
  <line x1="208" y1="118" x2="162" y2="118" stroke="#10B981" stroke-width="2.5" marker-end="url(#a6g)"/>
  <text x="185" y="136" text-anchor="middle" font-size="9" fill="#16A34A">② return (~1ms)</text>
  <rect x="40" y="200" width="140" height="70" rx="10" fill="#ECFDF5" stroke="#6EE7B7" stroke-width="1.5"/>
  <text x="110" y="228" text-anchor="middle" font-size="14" font-weight="700" fill="#065F46">⚡ ~1ms</text>
  <text x="110" y="248" text-anchor="middle" font-size="10" fill="#047857">Served from RAM</text>
  <text x="110" y="266" text-anchor="middle" font-size="10" fill="#047857">No DB query</text>
  <rect x="385" y="15" width="340" height="330" rx="12" fill="#FFF7ED" stroke="#FED7AA" stroke-width="2"/>
  <text x="555" y="42" text-anchor="middle" font-size="13" font-weight="700" fill="#92400E">❌  Cache MISS</text>
  <text x="555" y="60" text-anchor="middle" font-size="10" fill="#B45309">Not in cache — must query database</text>
  <rect x="405" y="80" width="120" height="55" rx="10" fill="#3B82F6"/>
  <text x="465" y="104" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Server</text>
  <text x="465" y="124" text-anchor="middle" font-size="9" fill="#BFDBFE">receives request</text>
  <rect x="575" y="80" width="120" height="55" rx="10" fill="#F59E0B"/>
  <text x="635" y="104" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚡ Cache</text>
  <text x="635" y="124" text-anchor="middle" font-size="9" fill="#FEF3C7">not found</text>
  <rect x="575" y="205" width="120" height="55" rx="10" fill="#8B5CF6"/>
  <text x="635" y="229" text-anchor="middle" font-size="11" font-weight="600" fill="white">Database</text>
  <text x="635" y="249" text-anchor="middle" font-size="9" fill="#DDD6FE">fetch data</text>
  <line x1="527" y1="100" x2="573" y2="100" stroke="#64748B" stroke-width="2" marker-end="url(#a6)"/>
  <text x="550" y="92" text-anchor="middle" font-size="9" fill="#475569">① check</text>
  <line x1="635" y1="137" x2="635" y2="203" stroke="#64748B" stroke-width="2" marker-end="url(#a6)"/>
  <text x="660" y="172" text-anchor="middle" font-size="9" fill="#475569">② query</text>
  <line x1="573" y1="222" x2="527" y2="118" stroke="#F97316" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#a6o)"/>
  <text x="540" y="178" text-anchor="middle" font-size="9" fill="#EA580C">③ store + return</text>
  <rect x="405" y="278" width="280" height="45" rx="10" fill="#FEF3C7" stroke="#FCD34D" stroke-width="1.5"/>
  <text x="545" y="297" text-anchor="middle" font-size="11" font-weight="600" fill="#92400E">Next request → Cache HIT ✅</text>
  <text x="545" y="315" text-anchor="middle" font-size="10" fill="#B45309">Data now cached for future requests</text>
</svg>

This caching strategy is called a **read-through cache**. After receiving a request, a web server first checks if the cache has the available response. If it does, it sends data back to the client. If not, it queries the database, stores the response in cache, and sends it back to the client.

Interacting with cache servers is simple because most cache servers provide APIs for common programming languages. Here are typical Memcached APIs:

```python
SECONDS = 1
cache.set('myKey', 'hi there', 3600 * SECONDS)
cache.get('myKey')
```

### Considerations for using cache

**When to use cache.** Consider using cache when data is read frequently but modified infrequently. Since cached data is stored in volatile memory, a cache server is not ideal for persisting data. For instance, if a cache server restarts, all the data in memory is lost. Thus, important data should be saved in persistent data stores.

**Expiration policy.** It is a good practice to implement an expiration policy. Once cached data is expired, it is removed from the cache. When there is no expiration policy, cached data will be stored in memory permanently. It is advisable not to make the expiration date too short (this will cause the system to reload data from the database too frequently) nor too long (the data can become stale).

**Consistency.** This involves keeping the data store and the cache in sync. Inconsistency can happen because data-modifying operations on the data store and cache are not in a single transaction. When scaling across multiple regions, maintaining consistency between the data store and cache is challenging. (See the paper "Scaling Memcache at Facebook" for further details.)

**Mitigating failures.** A single cache server represents a potential **single point of failure (SPOF)** — a part of a system that, if it fails, will stop the entire system from working. As a result, multiple cache servers across different data centers are recommended to avoid SPOF. Another recommended approach is to overprovision the required memory by certain percentages — this provides a buffer as memory usage increases.

**Eviction policy.** Once the cache is full, any requests to add items to the cache might cause existing items to be removed. This is called **cache eviction**. Least-recently-used (LRU) is the most popular cache eviction policy. Other policies — Least Frequently Used (LFU) or First In First Out (FIFO) — can be adopted to satisfy different use cases.

---

## Step 7: Content Delivery Network (CDN)

A CDN is a network of geographically dispersed servers used to deliver **static content**. CDN servers cache static content like images, videos, CSS, and JavaScript files.

Dynamic content caching is a relatively new concept. This tutorial focuses on how to use CDN to cache static content.

Here is how CDN works at a high level: when a user visits a website, a CDN server closest to the user will deliver static content. Intuitively, the further users are from CDN servers, the slower the website loads. For example, if CDN servers are in San Francisco, users in Los Angeles will get content faster than users in Europe.

<svg viewBox="0 0 740 360" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a7" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a7g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
    <marker id="a7p" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#EC4899"/></marker>
  </defs>
  <rect width="740" height="360" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="20" y="55" width="120" height="70" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="80" y="80" text-anchor="middle" font-size="20">👤</text>
  <text x="80" y="100" text-anchor="middle" font-size="11" font-weight="600" fill="#3730A3">User A</text>
  <text x="80" y="116" text-anchor="middle" font-size="9" fill="#6366F1">Tokyo</text>
  <rect x="20" y="230" width="120" height="70" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="80" y="255" text-anchor="middle" font-size="20">👤</text>
  <text x="80" y="275" text-anchor="middle" font-size="11" font-weight="600" fill="#3730A3">User B</text>
  <text x="80" y="291" text-anchor="middle" font-size="9" fill="#6366F1">Tokyo</text>
  <rect x="270" y="120" width="200" height="115" rx="14" fill="#FDF2F8" stroke="#F9A8D4" stroke-width="2.5"/>
  <text x="370" y="152" text-anchor="middle" font-size="28">⚡</text>
  <text x="370" y="180" text-anchor="middle" font-size="13" font-weight="700" fill="#9D174D">CDN Edge Node</text>
  <text x="370" y="200" text-anchor="middle" font-size="10" fill="#BE185D">Tokyo · ~5ms latency</text>
  <text x="370" y="218" text-anchor="middle" font-size="9" fill="#DB2777">Caches images, CSS, JS</text>
  <rect x="570" y="120" width="155" height="115" rx="14" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <text x="647" y="152" text-anchor="middle" font-size="22">🖥</text>
  <text x="647" y="178" text-anchor="middle" font-size="12" font-weight="700" fill="#1E40AF">Origin Server</text>
  <text x="647" y="198" text-anchor="middle" font-size="10" fill="#3B82F6">Virginia · ~150ms</text>
  <text x="647" y="218" text-anchor="middle" font-size="9" fill="#60A5FA">Web server / S3 bucket</text>
  <line x1="142" y1="82" x2="268" y2="158" stroke="#64748B" stroke-width="2" marker-end="url(#a7)"/>
  <text x="180" y="108" text-anchor="middle" font-size="9" fill="#475569">① GET image.png</text>
  <line x1="472" y1="158" x2="568" y2="163" stroke="#EC4899" stroke-width="2" marker-end="url(#a7p)"/>
  <text x="520" y="150" text-anchor="middle" font-size="9" fill="#DB2777">② MISS → fetch</text>
  <line x1="568" y1="183" x2="472" y2="183" stroke="#64748B" stroke-width="1.5" marker-end="url(#a7)"/>
  <text x="520" y="200" text-anchor="middle" font-size="9" fill="#475569">③ return file + TTL</text>
  <line x1="268" y1="168" x2="142" y2="100" stroke="#10B981" stroke-width="2.5" marker-end="url(#a7g)"/>
  <text x="180" y="148" text-anchor="middle" font-size="9" fill="#059669">④ cached + returned</text>
  <line x1="142" y1="258" x2="268" y2="210" stroke="#64748B" stroke-width="2" marker-end="url(#a7)"/>
  <text x="180" y="246" text-anchor="middle" font-size="9" fill="#475569">⑤ GET image.png</text>
  <line x1="268" y1="222" x2="142" y2="270" stroke="#10B981" stroke-width="2.5" marker-end="url(#a7g)"/>
  <text x="185" y="264" text-anchor="middle" font-size="9" fill="#059669">⑥ HIT! 5ms ⚡</text>
  <rect x="20" y="320" width="700" height="28" rx="8" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.5"/>
  <text x="370" y="338" text-anchor="middle" font-size="11" fill="#166534" font-weight="600">Without CDN: 150ms · With CDN edge node: ~5ms — 30× faster</text>
</svg>

### CDN workflow step-by-step

1. **User A tries to get** `image.png` using an image URL. The URL's domain is provided by the CDN provider (e.g., `https://mysite.cloudfront.net/logo.jpg` or `https://mysite.akamai.com/image-manager/img/logo.jpg`).
2. **If the CDN server does not have** `image.png` in its cache, the CDN server requests the file from the origin, which can be a web server or online storage like Amazon S3.
3. **The origin returns** `image.png` to the CDN server, which includes an optional HTTP `Cache-Control` header `Time-to-Live (TTL)` that describes how long the image is cached.
4. **The CDN caches the image** and returns it to User A. The image remains cached in the CDN until the TTL expires.
5. **User B sends a request** to get the same image.
6. **The image is returned from the CDN cache** as long as the TTL has not expired. User B gets it instantly from the nearby edge node.

### Considerations for using a CDN

**Cost.** CDNs are run by third-party providers, and you are charged for data transfers in and out of the CDN. Caching infrequently used assets provides no significant benefits so you should consider moving them out of the CDN.

**Setting an appropriate cache expiry.** For time-sensitive content, setting a cache expiry time is important. The cache expiry time should neither be too long nor too short. If it is too long, the content might no longer be fresh. If it is too short, it can cause repeat reloading of content from origin servers to the CDN.

**CDN fallback.** You should consider how your website/application copes with CDN failure. If there is a temporary CDN outage, clients should be able to detect the problem and request resources directly from the origin.

**Invalidating files.** You can remove a file from the CDN before it expires by:
- Invalidating the CDN object using APIs provided by CDN vendors
- Using **object versioning** to serve a different version of the object — add a parameter to the URL such as a version number: `image.png?v=2`

After adding CDN and cache: static assets (JS, CSS, images) are no longer served by web servers — they are fetched from the CDN for better performance. The database load is lightened by caching data.

---

## Step 8: Stateless Web Tier — The Key to Horizontal Scaling

Now it is time to consider scaling the web tier **horizontally**. To do this, we need to move state (for instance, user session data) out of the web tier. A good practice is to store session data in persistent storage such as a relational database or NoSQL. Each web server in the cluster can then access state data from databases. This is called a **stateless web tier**.

### Stateful architecture (the problem)

A stateful server and a stateless server have some key differences. A **stateful server** remembers client data (state) from one request to the next. A **stateless server** keeps no state information.

<svg viewBox="0 0 740 380" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a8r" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#EF4444"/></marker>
    <marker id="a8g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
    <marker id="a8" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
  </defs>
  <rect width="740" height="380" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="10" y="10" width="355" height="360" rx="14" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="2"/>
  <text x="188" y="36" text-anchor="middle" font-size="14" font-weight="700" fill="#991B1B">❌  Stateful (Bad)</text>
  <text x="188" y="55" text-anchor="middle" font-size="10" fill="#B91C1C">Session data stored in server memory</text>
  <text x="55" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User A</text>
  <text x="188" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User B</text>
  <text x="320" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User C</text>
  <rect x="20" y="110" width="145" height="100" rx="10" fill="#EF4444"/>
  <text x="93" y="135" text-anchor="middle" font-size="11" font-weight="600" fill="white">Server 1</text>
  <text x="93" y="155" text-anchor="middle" font-size="9" fill="#FEE2E2">• Session: User A ✓</text>
  <text x="93" y="172" text-anchor="middle" font-size="9" fill="#FEE2E2">• Profile image: User A</text>
  <text x="93" y="192" text-anchor="middle" font-size="8" fill="#FECACA">User B → FAIL ✗</text>
  <rect x="200" y="110" width="145" height="100" rx="10" fill="#EF4444"/>
  <text x="273" y="135" text-anchor="middle" font-size="11" font-weight="600" fill="white">Server 2</text>
  <text x="273" y="155" text-anchor="middle" font-size="9" fill="#FEE2E2">• Session: User B ✓</text>
  <text x="273" y="172" text-anchor="middle" font-size="9" fill="#FEE2E2">• Profile image: User B</text>
  <text x="273" y="192" text-anchor="middle" font-size="8" fill="#FECACA">User A → FAIL ✗</text>
  <line x1="55" y1="95" x2="55" y2="108" stroke="#EF4444" stroke-width="2" marker-end="url(#a8r)"/>
  <line x1="188" y1="95" x2="260" y2="108" stroke="#EF4444" stroke-width="2" marker-end="url(#a8r)"/>
  <line x1="320" y1="95" x2="130" y2="108" stroke="#EF4444" stroke-width="2" marker-end="url(#a8r)"/>
  <rect x="20" y="228" width="325" height="55" rx="8" fill="#FEE2E2" stroke="#FCA5A5" stroke-width="1.5"/>
  <text x="183" y="249" text-anchor="middle" font-size="11" font-weight="600" fill="#991B1B">Problem: each user "stuck" to one server</text>
  <text x="183" y="268" text-anchor="middle" font-size="10" fill="#B91C1C">If Server 1 crashes → User A is logged out</text>
  <text x="183" y="300" text-anchor="middle" font-size="10" fill="#9F1239">• Adding/removing servers is risky</text>
  <text x="183" y="320" text-anchor="middle" font-size="10" fill="#9F1239">• Uneven load distribution</text>
  <text x="183" y="340" text-anchor="middle" font-size="10" fill="#9F1239">• Server failure causes user logout</text>
  <rect x="375" y="10" width="355" height="360" rx="14" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2"/>
  <text x="553" y="36" text-anchor="middle" font-size="14" font-weight="700" fill="#14532D">✅  Stateless (Good)</text>
  <text x="553" y="55" text-anchor="middle" font-size="10" fill="#166534">Session stored in shared data store</text>
  <text x="430" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User A</text>
  <text x="553" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User B</text>
  <text x="676" y="90" text-anchor="middle" font-size="11" font-weight="600" fill="#374151">User C</text>
  <rect x="478" y="108" width="150" height="35" rx="8" fill="#06B6D4"/>
  <text x="553" y="130" text-anchor="middle" font-size="11" font-weight="600" fill="white">Load Balancer</text>
  <rect x="385" y="165" width="115" height="55" rx="8" fill="#3B82F6"/>
  <text x="443" y="190" text-anchor="middle" font-size="11" font-weight="600" fill="white">Server 1</text>
  <text x="443" y="208" text-anchor="middle" font-size="9" fill="#BFDBFE">stateless</text>
  <rect x="606" y="165" width="115" height="55" rx="8" fill="#3B82F6"/>
  <text x="664" y="190" text-anchor="middle" font-size="11" font-weight="600" fill="white">Server 2</text>
  <text x="664" y="208" text-anchor="middle" font-size="9" fill="#BFDBFE">stateless</text>
  <rect x="453" y="252" width="200" height="60" rx="10" fill="#10B981"/>
  <text x="553" y="278" text-anchor="middle" font-size="12" font-weight="600" fill="white">🗄  Shared Session Store</text>
  <text x="553" y="298" text-anchor="middle" font-size="9" fill="#D1FAE5">Memcached / Redis / NoSQL / SQL</text>
  <line x1="430" y1="95" x2="510" y2="106" stroke="#10B981" stroke-width="1.5" marker-end="url(#a8g)"/>
  <line x1="553" y1="95" x2="553" y2="106" stroke="#10B981" stroke-width="1.5" marker-end="url(#a8g)"/>
  <line x1="676" y1="95" x2="596" y2="106" stroke="#10B981" stroke-width="1.5" marker-end="url(#a8g)"/>
  <line x1="510" y1="143" x2="460" y2="163" stroke="#64748B" stroke-width="1.5" marker-end="url(#a8)"/>
  <line x1="596" y1="143" x2="646" y2="163" stroke="#64748B" stroke-width="1.5" marker-end="url(#a8)"/>
  <line x1="443" y1="222" x2="490" y2="250" stroke="#64748B" stroke-width="1.5" marker-end="url(#a8)"/>
  <line x1="664" y1="222" x2="616" y2="250" stroke="#64748B" stroke-width="1.5" marker-end="url(#a8)"/>
  <rect x="385" y="325" width="335" height="35" rx="8" fill="#DCFCE7" stroke="#86EFAC" stroke-width="1.5"/>
  <text x="553" y="342" text-anchor="middle" font-size="10" fill="#166534" font-weight="600">Any server handles any user's request</text>
  <text x="553" y="356" text-anchor="middle" font-size="10" fill="#166534">Add/remove servers without disruption</text>
</svg>

In the **stateful** diagram above, User A's session data and profile image are stored in Server 1. To authenticate User A, HTTP requests must be routed to Server 1. If a request is sent to Server 2, authentication would fail because Server 2 does not contain User A's session data.

The issue is that **every request from the same client must be routed to the same server**. This can be done with **sticky sessions** in most load balancers — however, this adds overhead. Adding or removing servers is much more difficult, and it is also challenging to handle server failures.

### Stateless architecture (the solution)

In the stateless architecture, HTTP requests from users can be sent to **any web server**, which fetches state data from a shared data store. State data is stored in a shared data store and kept out of web servers. A stateless system is simpler, more robust, and scalable.

The shared data store could be a relational database, Memcached/Redis, or NoSQL. The **NoSQL data store is chosen as it is easy to scale**. After the state data is removed out of web servers, auto-scaling of the web tier is easily achieved by adding or removing servers based on traffic load.

---

## Step 9: Multiple Data Centers — Geographic Redundancy

Your website grows rapidly and attracts a significant number of users internationally. To improve availability and provide a better user experience across wider geographical areas, supporting multiple data centers is crucial.

<svg viewBox="0 0 740 420" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a9" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a9p" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#8B5CF6"/></marker>
  </defs>
  <rect width="740" height="420" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="295" y="15" width="150" height="50" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="370" y="44" text-anchor="middle" font-size="22">👥</text>
  <text x="370" y="58" text-anchor="middle" font-size="10" font-weight="600" fill="#3730A3">Worldwide Users</text>
  <rect x="295" y="92" width="150" height="45" rx="10" fill="#FFFBEB" stroke="#FCD34D" stroke-width="2"/>
  <text x="370" y="119" text-anchor="middle" font-size="12" font-weight="700" fill="#92400E">🌐 GeoDNS</text>
  <rect x="20" y="195" width="320" height="195" rx="14" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2.5"/>
  <text x="180" y="220" text-anchor="middle" font-size="13" font-weight="700" fill="#1E40AF">🏢 DC1 — US-East (Primary)</text>
  <rect x="38" y="232" width="130" height="45" rx="8" fill="#3B82F6"/>
  <text x="103" y="253" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Servers</text>
  <text x="103" y="270" text-anchor="middle" font-size="9" fill="#BFDBFE">auto-scaled</text>
  <rect x="180" y="232" width="130" height="45" rx="8" fill="#8B5CF6"/>
  <text x="245" y="253" text-anchor="middle" font-size="11" font-weight="600" fill="white">Database</text>
  <text x="245" y="270" text-anchor="middle" font-size="9" fill="#DDD6FE">primary</text>
  <rect x="38" y="292" width="272" height="40" rx="8" fill="#10B981"/>
  <text x="174" y="317" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚡ Cache Cluster</text>
  <rect x="400" y="195" width="320" height="195" rx="14" fill="#FFF7ED" stroke="#FED7AA" stroke-width="2.5"/>
  <text x="560" y="220" text-anchor="middle" font-size="13" font-weight="700" fill="#92400E">🏢 DC2 — US-West (Failover)</text>
  <rect x="418" y="232" width="130" height="45" rx="8" fill="#3B82F6"/>
  <text x="483" y="253" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Servers</text>
  <text x="483" y="270" text-anchor="middle" font-size="9" fill="#BFDBFE">auto-scaled</text>
  <rect x="560" y="232" width="130" height="45" rx="8" fill="#8B5CF6"/>
  <text x="625" y="253" text-anchor="middle" font-size="11" font-weight="600" fill="white">Database</text>
  <text x="625" y="270" text-anchor="middle" font-size="9" fill="#DDD6FE">replica</text>
  <rect x="418" y="292" width="272" height="40" rx="8" fill="#10B981"/>
  <text x="554" y="317" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚡ Cache Cluster</text>
  <line x1="370" y1="65" x2="370" y2="90" stroke="#64748B" stroke-width="2" marker-end="url(#a9)"/>
  <line x1="325" y1="135" x2="215" y2="193" stroke="#64748B" stroke-width="2" marker-end="url(#a9)"/>
  <text x="243" y="163" text-anchor="middle" font-size="10" fill="#475569">x% (US users)</text>
  <line x1="415" y1="135" x2="525" y2="193" stroke="#64748B" stroke-width="2" marker-end="url(#a9)"/>
  <text x="497" y="163" text-anchor="middle" font-size="10" fill="#475569">(100-x)% traffic</text>
  <line x1="342" y1="315" x2="398" y2="315" stroke="#8B5CF6" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#a9p)"/>
  <line x1="398" y1="332" x2="342" y2="332" stroke="#8B5CF6" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#a9p)"/>
  <text x="370" y="360" text-anchor="middle" font-size="9" fill="#7C3AED">async replication</text>
  <rect x="155" y="375" width="430" height="30" rx="8" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.5"/>
  <text x="370" y="395" text-anchor="middle" font-size="11" fill="#DC2626" font-weight="600">If DC2 goes offline → GeoDNS routes 100% traffic to DC1</text>
</svg>

In normal operation, users are **geoDNS-routed** to the closest data center, with a split traffic of *x%* in US-East and *(100–x)%* in US-West. **GeoDNS** is a DNS service that allows domain names to be resolved to IP addresses based on the location of a user.

In the event of any significant data center outage, we direct all traffic to a healthy data center. If data center 2 (US-West) is offline, 100% of the traffic is routed to data center 1 (US-East).

### Technical challenges in multi-data center setup

Several technical challenges must be resolved:

**Traffic redirection.** Effective tools are needed to direct traffic to the correct data center. GeoDNS can be used to direct traffic to the nearest data center depending on where a user is located.

**Data synchronization.** Users from different regions could use different local databases or caches. In failover cases, traffic might be routed to a data center where data is unavailable. A common strategy is to **replicate data across multiple data centers**. A previous study shows how Netflix implements asynchronous multi-data center replication.

**Test and deployment.** With multi-data center setup, it is important to test your website/application at different locations. Automated deployment tools are vital to keep services consistent through all the data centers.

To further scale our system, we need to decouple different components of the system so they can be scaled independently. **Messaging queue** is a key strategy employed by many real-world distributed systems to solve this problem.

---

## Step 10: Message Queue — Decouple and Scale Independently

A message queue is a **durable component**, stored in memory, that supports asynchronous communication. It serves as a buffer and distributes asynchronous requests. The basic architecture of a message queue is simple:
- **Input services** (called producers/publishers) create messages and publish them to a message queue
- **Other services** (called consumers/subscribers) connect to the queue and perform actions defined by the messages

<svg viewBox="0 0 740 300" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a10" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a10o" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#F97316"/></marker>
    <marker id="a10g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
  </defs>
  <rect width="740" height="300" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="20" y="90" width="155" height="120" rx="12" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <text x="97" y="115" text-anchor="middle" font-size="11" font-weight="700" fill="#1E40AF">PRODUCER</text>
  <rect x="35" y="124" width="125" height="50" rx="8" fill="#3B82F6"/>
  <text x="97" y="146" text-anchor="middle" font-size="11" font-weight="600" fill="white">🖥 Web Server</text>
  <text x="97" y="164" text-anchor="middle" font-size="9" fill="#BFDBFE">publishes jobs</text>
  <rect x="20" y="228" width="155" height="30" rx="8" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.5"/>
  <text x="97" y="248" text-anchor="middle" font-size="10" fill="#166534">② Returns to user instantly</text>
  <rect x="255" y="78" width="230" height="140" rx="14" fill="#FFF7ED" stroke="#FED7AA" stroke-width="2.5"/>
  <text x="370" y="103" text-anchor="middle" font-size="12" font-weight="700" fill="#92400E">📬 Message Queue</text>
  <text x="370" y="120" text-anchor="middle" font-size="10" fill="#B45309">Kafka · RabbitMQ · AWS SQS</text>
  <rect x="270" y="130" width="45" height="35" rx="5" fill="#F97316"/>
  <text x="292" y="153" text-anchor="middle" font-size="10" fill="white">job</text>
  <rect x="323" y="130" width="45" height="35" rx="5" fill="#F97316"/>
  <text x="345" y="153" text-anchor="middle" font-size="10" fill="white">job</text>
  <rect x="376" y="130" width="45" height="35" rx="5" fill="#F97316"/>
  <text x="398" y="153" text-anchor="middle" font-size="10" fill="white">job</text>
  <rect x="429" y="130" width="45" height="35" rx="5" fill="#FED7AA" stroke="#F97316" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="451" y="153" text-anchor="middle" font-size="10" fill="#92400E">...</text>
  <text x="370" y="200" text-anchor="middle" font-size="9" fill="#B45309">Queue grows → add workers | Queue empty → reduce workers</text>
  <rect x="575" y="50" width="145" height="55" rx="10" fill="#F0FDFA" stroke="#99F6E4" stroke-width="2"/>
  <rect x="590" y="62" width="115" height="34" rx="7" fill="#14B8A6"/>
  <text x="647" y="82" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚙ Worker 1</text>
  <rect x="575" y="120" width="145" height="55" rx="10" fill="#F0FDFA" stroke="#99F6E4" stroke-width="2"/>
  <rect x="590" y="132" width="115" height="34" rx="7" fill="#14B8A6"/>
  <text x="647" y="152" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚙ Worker 2</text>
  <rect x="575" y="190" width="145" height="55" rx="10" fill="#F0FDFA" stroke="#99F6E4" stroke-width="2"/>
  <rect x="590" y="202" width="115" height="34" rx="7" fill="#14B8A6"/>
  <text x="647" y="222" text-anchor="middle" font-size="11" font-weight="600" fill="white">⚙ Worker 3</text>
  <line x1="177" y1="145" x2="253" y2="145" stroke="#F97316" stroke-width="2.5" marker-end="url(#a10o)"/>
  <text x="215" y="135" text-anchor="middle" font-size="9" fill="#EA580C">① publish job</text>
  <line x1="487" y1="148" x2="572" y2="88" stroke="#10B981" stroke-width="2" marker-end="url(#a10g)"/>
  <line x1="487" y1="155" x2="572" y2="155" stroke="#10B981" stroke-width="2" marker-end="url(#a10g)"/>
  <line x1="487" y1="162" x2="572" y2="218" stroke="#10B981" stroke-width="2" marker-end="url(#a10g)"/>
  <text x="536" y="132" text-anchor="middle" font-size="9" fill="#059669">③ consume</text>
</svg>

**Decoupling makes the message queue a preferred architecture for building scalable and reliable applications.** With the message queue, the producer can post a message to the queue when the consumer is unavailable to process it. The consumer can read messages from the queue even when the producer is unavailable.

### A real-world example: photo customization

Consider an application that supports photo customization — cropping, sharpening, blurring, etc. Those customization tasks take time to complete.

- Web servers **publish photo processing jobs** to the message queue
- Photo processing **workers pick up jobs** from the queue and asynchronously perform photo customization tasks
- The producer (web server) and the consumer (worker) can be **scaled independently**
- When the size of the queue becomes large, more workers are added to reduce the processing time
- However, if the queue is empty most of the time, the number of workers can be reduced

Other real-world uses: **email delivery** (don't make users wait for SMTP), **video transcoding** (YouTube processes uploads asynchronously), **search indexing** (Elasticsearch indexes new documents in the background), **push notifications**, and **audit logging**.

---

## Step 11: Logging, Metrics, and Automation

When working with a small website that runs on a few servers, logging, metrics, and automation support are good practices but not a necessity. However, now that your site has grown to serve a large business, investing in these tools is essential.

<svg viewBox="0 0 740 230" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <rect width="740" height="230" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="20" y="25" width="165" height="190" rx="12" fill="#EFF6FF" stroke="#93C5FD" stroke-width="2"/>
  <text x="102" y="52" text-anchor="middle" font-size="24">📋</text>
  <text x="102" y="76" text-anchor="middle" font-size="13" font-weight="700" fill="#1E40AF">Logging</text>
  <text x="102" y="96" text-anchor="middle" font-size="10" fill="#3B82F6">Identify errors &amp;</text>
  <text x="102" y="112" text-anchor="middle" font-size="10" fill="#3B82F6">problems in the system</text>
  <text x="102" y="135" text-anchor="middle" font-size="10" fill="#64748B">ELK Stack</text>
  <text x="102" y="153" text-anchor="middle" font-size="10" fill="#64748B">Grafana Loki</text>
  <text x="102" y="171" text-anchor="middle" font-size="10" fill="#64748B">AWS CloudWatch</text>
  <text x="102" y="200" text-anchor="middle" font-size="9" fill="#94A3B8">Per-server or centralized</text>
  <rect x="200" y="25" width="165" height="190" rx="12" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2"/>
  <text x="282" y="52" text-anchor="middle" font-size="24">📊</text>
  <text x="282" y="76" text-anchor="middle" font-size="13" font-weight="700" fill="#14532D">Metrics</text>
  <text x="282" y="96" text-anchor="middle" font-size="10" fill="#16A34A">Host: CPU, Memory,</text>
  <text x="282" y="112" text-anchor="middle" font-size="10" fill="#16A34A">disk I/O</text>
  <text x="282" y="130" text-anchor="middle" font-size="10" fill="#16A34A">Aggregated: DB, Cache</text>
  <text x="282" y="148" text-anchor="middle" font-size="10" fill="#16A34A">Business: DAU, revenue</text>
  <text x="282" y="171" text-anchor="middle" font-size="10" fill="#64748B">Prometheus + Grafana</text>
  <text x="282" y="189" text-anchor="middle" font-size="10" fill="#64748B">Datadog · CloudWatch</text>
  <rect x="380" y="25" width="165" height="190" rx="12" fill="#FFF7ED" stroke="#FED7AA" stroke-width="2"/>
  <text x="462" y="52" text-anchor="middle" font-size="24">🔔</text>
  <text x="462" y="76" text-anchor="middle" font-size="13" font-weight="700" fill="#92400E">Monitoring</text>
  <text x="462" y="96" text-anchor="middle" font-size="10" fill="#B45309">Alert on thresholds</text>
  <text x="462" y="112" text-anchor="middle" font-size="10" fill="#B45309">Page on-call engineers</text>
  <text x="462" y="135" text-anchor="middle" font-size="10" fill="#64748B">PagerDuty</text>
  <text x="462" y="153" text-anchor="middle" font-size="10" fill="#64748B">OpsGenie</text>
  <text x="462" y="171" text-anchor="middle" font-size="10" fill="#64748B">CloudWatch Alarms</text>
  <text x="462" y="200" text-anchor="middle" font-size="9" fill="#94A3B8">Auto-detect outages</text>
  <rect x="560" y="25" width="165" height="190" rx="12" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="2"/>
  <text x="642" y="52" text-anchor="middle" font-size="24">🤖</text>
  <text x="642" y="76" text-anchor="middle" font-size="13" font-weight="700" fill="#4C1D95">Automation</text>
  <text x="642" y="96" text-anchor="middle" font-size="10" fill="#7C3AED">CI: verify each code</text>
  <text x="642" y="112" text-anchor="middle" font-size="10" fill="#7C3AED">check-in via automation</text>
  <text x="642" y="130" text-anchor="middle" font-size="10" fill="#7C3AED">CD: auto-deploy builds</text>
  <text x="642" y="148" text-anchor="middle" font-size="10" fill="#7C3AED">Auto Scaling</text>
  <text x="642" y="171" text-anchor="middle" font-size="10" fill="#64748B">GitHub Actions</text>
  <text x="642" y="189" text-anchor="middle" font-size="10" fill="#64748B">Terraform / CDK</text>
</svg>

**Logging** — Monitoring error logs is important because it helps identify errors and problems in the system. You can monitor error logs at the per-server level or use tools to aggregate them to a centralized service for easy search and viewing.

**Metrics** — Collecting different types of metrics helps gain business insights and understand the health status of the system. Some useful metrics are:
- *Host level metrics*: CPU, Memory, disk I/O, etc.
- *Aggregated level metrics*: for example, the performance of the entire database tier, cache tier, etc.
- *Key business metrics*: daily active users, retention, revenue, etc.

**Automation** — When a system gets big and complex, we need to build or leverage automation tools to improve productivity. **Continuous integration** is a good practice in which each code check-in is verified through automation, allowing teams to detect problems early. Besides automating your build, test, and deploy process, automation can significantly improve developer productivity.

The design now includes a message queue (which helps make the system more loosely coupled and failure resilient) plus logging, monitoring, metrics, and automation tools.

As the data grows every day, your database gets more overloaded. It is time to scale the data tier.

---

## Step 12: Database Sharding — Scaling the Data Tier

There are two broad approaches for database scaling: **vertical scaling** and **horizontal scaling**.

**Vertical scaling** (scale up) means adding more power (CPU, RAM, DISK) to an existing machine. There are some powerful database servers available — according to Amazon Relational Database Service (RDS), you can get a database server with **24 TB of RAM**. This kind of powerful database server could store and handle lots of data. For example, stackoverflow.com in 2013 had over 10 million monthly unique visitors, but it only had 1 master database.

However, vertical scaling comes with serious drawbacks:
- You can add more hardware, but there are **hardware limits** — if you have a large user base, a single server is not enough
- **Greater risk of single point of failure**
- **The overall cost is high** — powerful servers are much more expensive

**Horizontal scaling** — also known as **sharding** — is the practice of adding more servers.

<svg viewBox="0 0 740 340" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="a12" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
    <marker id="a12g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#10B981"/></marker>
  </defs>
  <rect width="740" height="340" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="255" y="15" width="230" height="55" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="370" y="38" text-anchor="middle" font-size="12" font-weight="700" fill="#3730A3">Query: user_id = 13</text>
  <text x="370" y="58" text-anchor="middle" font-size="11" fill="#6366F1">13 % 4 = 1  →  Shard 1</text>
  <rect x="285" y="92" width="170" height="38" rx="10" fill="#7C3AED" stroke="#6D28D9" stroke-width="2"/>
  <text x="370" y="116" text-anchor="middle" font-size="12" font-weight="700" fill="white">Hash: user_id % 4</text>
  <rect x="20" y="185" width="155" height="115" rx="12" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="2"/>
  <text x="98" y="212" text-anchor="middle" font-size="13" font-weight="700" fill="#64748B">Shard 0</text>
  <text x="98" y="232" text-anchor="middle" font-size="10" fill="#94A3B8">user_id % 4 = 0</text>
  <text x="98" y="252" text-anchor="middle" font-size="10" fill="#94A3B8">0, 4, 8, 12 ...</text>
  <rect x="192" y="175" width="162" height="130" rx="12" fill="#F0FDF4" stroke="#10B981" stroke-width="3"/>
  <text x="273" y="205" text-anchor="middle" font-size="13" font-weight="700" fill="#14532D">Shard 1 ✅</text>
  <text x="273" y="225" text-anchor="middle" font-size="10" fill="#16A34A">user_id % 4 = 1</text>
  <text x="273" y="245" text-anchor="middle" font-size="10" fill="#16A34A" font-weight="600">1, 5, 9, 13 ← match!</text>
  <text x="273" y="265" text-anchor="middle" font-size="10" fill="#16A34A">17, 21 ...</text>
  <rect x="199" y="278" width="148" height="22" rx="6" fill="#10B981"/>
  <text x="273" y="293" text-anchor="middle" font-size="10" fill="white" font-weight="600">Query routed here</text>
  <rect x="373" y="185" width="155" height="115" rx="12" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="2"/>
  <text x="450" y="212" text-anchor="middle" font-size="13" font-weight="700" fill="#64748B">Shard 2</text>
  <text x="450" y="232" text-anchor="middle" font-size="10" fill="#94A3B8">user_id % 4 = 2</text>
  <text x="450" y="252" text-anchor="middle" font-size="10" fill="#94A3B8">2, 6, 10, 14 ...</text>
  <rect x="548" y="185" width="172" height="115" rx="12" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="2"/>
  <text x="634" y="212" text-anchor="middle" font-size="13" font-weight="700" fill="#64748B">Shard 3</text>
  <text x="634" y="232" text-anchor="middle" font-size="10" fill="#94A3B8">user_id % 4 = 3</text>
  <text x="634" y="252" text-anchor="middle" font-size="10" fill="#94A3B8">3, 7, 11, 15 ...</text>
  <line x1="337" y1="130" x2="130" y2="183" stroke="#CBD5E1" stroke-width="1.5" marker-end="url(#a12)"/>
  <line x1="358" y1="130" x2="298" y2="173" stroke="#10B981" stroke-width="2.5" marker-end="url(#a12g)"/>
  <line x1="393" y1="130" x2="465" y2="183" stroke="#CBD5E1" stroke-width="1.5" marker-end="url(#a12)"/>
  <line x1="415" y1="130" x2="595" y2="183" stroke="#CBD5E1" stroke-width="1.5" marker-end="url(#a12)"/>
</svg>

Sharding separates large databases into smaller, more easily managed parts called shards. **Each shard shares the same schema**, though the actual data on each shard is unique to that shard.

User data is allocated to a database server based on user IDs. Anytime you access data, a hash function is used to find the corresponding shard. In our example, `user_id % 4` is used as the hash function. If the result equals 0, Shard 0 is used. If the result equals 1, Shard 1 is used. And so on.

The most important factor to consider when implementing a sharding strategy is the choice of the **sharding key** (also known as partition key). The sharding key consists of one or more columns that determine how data is distributed. A sharding key allows you to retrieve and modify data efficiently by routing database queries to the correct database. When choosing a sharding key, one of the most important criteria is to choose a key that can **evenly distribute data**.

### Sharding challenges

Sharding is a great technique to scale the database but it is far from a perfect solution. It introduces complexities and new challenges:

**Resharding data** — Resharding is needed when: (1) a single shard can no longer hold more data due to rapid growth, (2) certain shards might experience shard exhaustion faster than others due to uneven data distribution. When shard exhaustion happens, it requires updating the sharding function and moving data around. **Consistent hashing** (covered in Chapter 5) is a commonly used technique to solve this problem.

**Celebrity problem** — This is also called a hotspot key problem. Excessive access to a specific shard could cause server overload. Imagine data for Katy Perry, Justin Bieber, and Lady Gaga all end up on the same shard. For social applications, that shard will be overwhelmed with read operations. To solve this problem, we may need to allocate a shard for each celebrity. Each shard might even require further partition.

**Join and de-normalization** — Once a database has been sharded across multiple servers, it is hard to perform JOIN operations across database shards. A common workaround is to **de-normalize** the database so that queries can be performed in a single table.

---

## The Full Architecture: Zero to Millions of Users

<svg viewBox="0 0 740 590" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:740px;margin:2rem auto;display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <defs>
    <marker id="af" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#64748B"/></marker>
  </defs>
  <rect width="740" height="590" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="30" y="18" width="100" height="48" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="2"/>
  <text x="80" y="36" text-anchor="middle" font-size="18">👥</text>
  <text x="80" y="56" text-anchor="middle" font-size="10" font-weight="600" fill="#3730A3">Users</text>
  <rect x="300" y="18" width="140" height="48" rx="10" fill="#FDF2F8" stroke="#F9A8D4" stroke-width="2"/>
  <text x="370" y="38" text-anchor="middle" font-size="11" font-weight="700" fill="#9D174D">⚡ CDN</text>
  <text x="370" y="56" text-anchor="middle" font-size="9" fill="#BE185D">Static assets · Global edge</text>
  <rect x="590" y="18" width="120" height="48" rx="10" fill="#FFFBEB" stroke="#FCD34D" stroke-width="2"/>
  <text x="650" y="38" text-anchor="middle" font-size="11" font-weight="700" fill="#92400E">🌐 GeoDNS</text>
  <text x="650" y="56" text-anchor="middle" font-size="9" fill="#B45309">Routes by location</text>
  <rect x="270" y="100" width="200" height="45" rx="12" fill="#0E7490" stroke="#06B6D4" stroke-width="2.5"/>
  <text x="370" y="120" text-anchor="middle" font-size="12" font-weight="700" fill="white">⚖  Load Balancer</text>
  <text x="370" y="137" text-anchor="middle" font-size="9" fill="#A5F3FC">Round-robin · Health checks · Failover</text>
  <rect x="80" y="183" width="115" height="52" rx="10" fill="#3B82F6"/>
  <text x="138" y="204" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Server 1</text>
  <text x="138" y="222" text-anchor="middle" font-size="9" fill="#BFDBFE">stateless</text>
  <rect x="313" y="183" width="115" height="52" rx="10" fill="#3B82F6"/>
  <text x="370" y="204" text-anchor="middle" font-size="11" font-weight="600" fill="white">Web Server 2</text>
  <text x="370" y="222" text-anchor="middle" font-size="9" fill="#BFDBFE">stateless</text>
  <rect x="546" y="183" width="115" height="52" rx="10" fill="#60A5FA" stroke="#3B82F6" stroke-dasharray="5,3" stroke-width="2"/>
  <text x="603" y="204" text-anchor="middle" font-size="11" font-weight="600" fill="#1E3A8A">Web Server N</text>
  <text x="603" y="222" text-anchor="middle" font-size="9" fill="#1D4ED8">auto-scaled</text>
  <rect x="80" y="278" width="160" height="65" rx="12" fill="#10B981"/>
  <text x="160" y="302" text-anchor="middle" font-size="12" font-weight="700" fill="white">⚡ Cache</text>
  <text x="160" y="320" text-anchor="middle" font-size="9" fill="#D1FAE5">Redis · Memcached · LRU</text>
  <rect x="500" y="278" width="200" height="65" rx="12" fill="#F97316"/>
  <text x="600" y="302" text-anchor="middle" font-size="12" font-weight="700" fill="white">📬 Message Queue</text>
  <text x="600" y="320" text-anchor="middle" font-size="9" fill="#FEF3C7">Kafka · RabbitMQ · SQS</text>
  <rect x="30" y="393" width="170" height="75" rx="12" fill="#7C3AED" stroke="#6D28D9" stroke-width="2"/>
  <text x="115" y="418" text-anchor="middle" font-size="11" font-weight="700" fill="white">Sharded DBs</text>
  <text x="115" y="436" text-anchor="middle" font-size="9" fill="#DDD6FE">Shard 1 · 2 · 3 ...</text>
  <text x="115" y="452" text-anchor="middle" font-size="9" fill="#DDD6FE">Writes → Master DB</text>
  <rect x="220" y="393" width="140" height="75" rx="12" fill="#6D28D9" stroke="#8B5CF6" stroke-width="2"/>
  <text x="290" y="418" text-anchor="middle" font-size="11" font-weight="700" fill="white">Slave DBs</text>
  <text x="290" y="436" text-anchor="middle" font-size="9" fill="#DDD6FE">Read Replicas</text>
  <text x="290" y="452" text-anchor="middle" font-size="9" fill="#DDD6FE">Reads → Here</text>
  <rect x="380" y="393" width="160" height="75" rx="12" fill="#14B8A6"/>
  <text x="460" y="418" text-anchor="middle" font-size="11" font-weight="700" fill="white">⚙ Workers</text>
  <text x="460" y="436" text-anchor="middle" font-size="9" fill="#CCFBF1">Async processing</text>
  <text x="460" y="452" text-anchor="middle" font-size="9" fill="#CCFBF1">Email · Images · Index</text>
  <rect x="560" y="393" width="150" height="75" rx="12" fill="#84CC16"/>
  <text x="635" y="418" text-anchor="middle" font-size="11" font-weight="700" fill="white">NoSQL Store</text>
  <text x="635" y="436" text-anchor="middle" font-size="9" fill="#F7FEE7">Non-relational data</text>
  <text x="635" y="452" text-anchor="middle" font-size="9" fill="#F7FEE7">Cassandra · DynamoDB</text>
  <rect x="30" y="510" width="680" height="55" rx="12" fill="#1E293B"/>
  <text x="200" y="535" text-anchor="middle" font-size="11" font-weight="700" fill="white">📋 Logging</text>
  <text x="370" y="535" text-anchor="middle" font-size="11" font-weight="700" fill="white">📊 Metrics</text>
  <text x="540" y="535" text-anchor="middle" font-size="11" font-weight="700" fill="white">🔔 Monitoring · 🤖 Automation</text>
  <text x="370" y="553" text-anchor="middle" font-size="10" fill="#94A3B8">Prometheus · Grafana · ELK · Datadog · PagerDuty · GitHub Actions</text>
  <line x1="80" y1="66" x2="300" y2="35" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="130" y1="66" x2="589" y2="40" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="370" y1="66" x2="370" y2="98" stroke="#64748B" stroke-width="2" marker-end="url(#af)"/>
  <line x1="330" y1="145" x2="195" y2="181" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="370" y1="145" x2="370" y2="181" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="410" y1="145" x2="545" y2="181" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="160" y1="235" x2="160" y2="276" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="370" y1="235" x2="200" y2="276" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="600" y1="235" x2="620" y2="276" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="160" y1="343" x2="115" y2="391" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="600" y1="343" x2="460" y2="391" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
  <line x1="635" y1="343" x2="635" y2="391" stroke="#64748B" stroke-width="1.5" marker-end="url(#af)"/>
</svg>

---

## Summary: How We Scale to Millions of Users

Scaling a system is an iterative process. More fine-tuning and new strategies are needed to scale beyond millions of users. For example, you might need to optimize your system and decouple the system into even smaller services. All the techniques learned in this chapter should provide a good foundation to tackle new challenges.

Here is a summary of how we scale our system to support millions of users:

| Principle | What It Means |
|-----------|---------------|
| **Keep web tier stateless** | Store sessions in shared storage (Redis/SQL/NoSQL), not in server memory |
| **Build redundancy at every tier** | No single point of failure — load balancers, DB replicas, multiple cache nodes |
| **Cache data as much as you can** | CDN for static assets, Redis for dynamic data, reduce DB load |
| **Support multiple data centers** | Geographic redundancy protects against regional outages |
| **Host static assets in CDN** | Images, CSS, JS from edge nodes — not your origin server |
| **Scale your data tier by sharding** | Partition by a key that distributes load evenly across shards |
| **Split tiers into individual services** | Decouple components so they scale independently |
| **Monitor your system and use automation tools** | Logging, metrics, CI/CD — you cannot improve what you cannot measure |

Congratulations on getting this far! Now give yourself a pat on the back. Good job!

---

## What's Next

In the next post, we cover **Back-of-the-Envelope Estimation** — how to quickly calculate QPS, storage requirements, and bandwidth before designing a system. This skill separates engineers who guess from those who reason from numbers.

---
