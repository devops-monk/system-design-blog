#!/usr/bin/env python3
"""Cover generator for the system-design blog.

One shared identity (dark ground, chapter badge, Inter title, accent rule)
with a distinct hand-drawn SVG motif per article, so the set reads as a
series without every cover looking identical.
"""
import subprocess, os, sys

SP = os.path.dirname(os.path.abspath(__file__))
OUT = "/Users/abhaypratapsingh/Documents/Personal/Blog/system-design-blog/static/images/articles"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BLUE, PINK, PURPLE = "#38bdf8", "#ec4899", "#c084fc"
GREEN, AMBER, RED = "#4ade80", "#fbbf24", "#f87171"
DIM, FAINT = "#64748b", "#334155"

SHELL = """<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
 *{margin:0;padding:0;box-sizing:border-box}
 body{width:1600px;height:640px;overflow:hidden;font-family:'Inter',sans-serif;
  background:radial-gradient(900px 600px at 12% 105%, rgba(236,72,153,.16), transparent 62%),
             radial-gradient(900px 620px at 88% -10%, rgba(56,189,248,.14), transparent 60%),
             linear-gradient(140deg,#0b1220 0%,#0f172a 48%,#111c33 100%)}
 .grid{position:absolute;inset:0;
  background-image:linear-gradient(rgba(148,163,184,.055) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(148,163,184,.055) 1px,transparent 1px);
  background-size:80px 80px}
 .edge{position:absolute;left:0;top:0;bottom:0;width:5px;
  background:linear-gradient(180deg,#38bdf8,#818cf8 55%,#ec4899)}
 .wrap{position:relative;display:flex;height:100%;align-items:center;padding:0 76px 0 104px;gap:56px}
 .left{width:600px;flex:0 0 600px}
 .kicker{display:flex;align-items:center;gap:16px;margin-bottom:28px}
 .badge{border:1.5px solid rgba(56,189,248,.55);color:#38bdf8;border-radius:7px;
  padding:8px 15px;font-size:15px;font-weight:700;letter-spacing:.15em}
 .sub{color:#7c8ba1;font-size:15px;font-weight:600;letter-spacing:.24em}
 h1{color:#fff;font-size:__FS__px;font-weight:800;line-height:1.07;letter-spacing:-.022em}
 .rule{width:82px;height:5px;border-radius:3px;margin:28px 0 24px;
  background:linear-gradient(90deg,#38bdf8,#ec4899)}
 .tag{color:#b6c2d4;font-size:21px;font-weight:500;line-height:1.5}
 .right{flex:1;display:flex;align-items:center;justify-content:center}
 .cap{position:absolute;right:76px;bottom:56px;font-family:'JetBrains Mono',monospace;
  font-size:17px;color:#8fa0b8;letter-spacing:.01em}
 .cap i{color:#38bdf8;font-style:normal}
 text{font-family:'JetBrains Mono',monospace}
</style></head><body>
<div class="grid"></div><div class="edge"></div>
<div class="wrap">
  <div class="left">
    <div class="kicker"><span class="badge">__BADGE__</span><span class="sub">SYSTEM DESIGN</span></div>
    <h1>__TITLE__</h1>
    <div class="rule"></div>
    <div class="tag">__TAG__</div>
  </div>
  <div class="right">__ART__</div>
</div>
<div class="cap">__CAP__</div>
</body></html>"""


def quad(x, y, s, depth, target):
    """Recursive quadtree subdivision; `target` picks which child to descend."""
    out = []
    if depth == 0:
        out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{PINK}" opacity=".9" rx="2"/>')
        return out
    h = s / 2
    for i, (dx, dy) in enumerate([(0, 0), (h, 0), (0, h), (h, h)]):
        if i == target[0]:
            out += quad(x + dx, y + dy, h, depth - 1, target[1:] or [0])
        else:
            op = .10 + .04 * depth
            out.append(f'<rect x="{x+dx}" y="{y+dy}" width="{h}" height="{h}" fill="{BLUE}" opacity="{op:.2f}" rx="2"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="none" stroke="{BLUE}" stroke-opacity=".45" stroke-width="1.4" rx="2"/>')
    for i, (dx, dy) in enumerate([(0, 0), (h, 0), (0, h), (h, h)]):
        out.append(f'<rect x="{x+dx}" y="{y+dy}" width="{h}" height="{h}" fill="none" stroke="{BLUE}" stroke-opacity=".28" stroke-width="1" rx="2"/>')
    return out


def art_quadtree():
    body = "".join(quad(60, 30, 340, 3, [3, 0, 1]))
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{body}' \
           f'<text x="60" y="404" fill="{DIM}" font-size="15">recursive subdivision — dense areas go deeper</text></svg>'


def art_fanout():
    import math
    cx, cy = 120, 205
    s = [f'<circle cx="{cx}" cy="{cy}" r="30" fill="{BLUE}" opacity=".16"/>',
         f'<circle cx="{cx}" cy="{cy}" r="14" fill="{BLUE}"/>']
    n = 20
    for i in range(n):
        a = -1.02 + (2.04 * i / (n - 1))
        r = 380 + (i % 3) * 22
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        x = min(x, 600); y = max(28, min(y, 360))
        near = i % 4 == 0
        col = PINK if near else FAINT
        op = ".95" if near else ".5"
        s.append(f'<line x1="{cx+15}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="{col}" stroke-opacity="{op}" stroke-width="{1.9 if near else 1}"/>')
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{6.5 if near else 4}" fill="{col}" opacity="{op}"/>')
    s.append(f'<text x="20" y="404" fill="{DIM}" font-size="15">one update, forty deliveries</text>')
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{"".join(s)}</svg>'


def art_zoom():
    s = []
    levels = [(1, 120, .32), (2, 150, .48), (4, 186, .72)]
    x = 26
    for li, (n, size, op) in enumerate(levels):
        oy = 210 - size / 2
        cell = size / n
        for r in range(n):
            for c in range(n):
                hot = (li == 2 and r == 2 and c == 1)
                col = PINK if hot else BLUE
                s.append(f'<rect x="{x+c*cell:.1f}" y="{oy+r*cell:.1f}" width="{cell-2.5:.1f}" height="{cell-2.5:.1f}" '
                         f'fill="{col}" opacity="{.95 if hot else op}" rx="1.5"/>')
        s.append(f'<text x="{x}" y="{oy+size+26:.0f}" fill="{DIM}" font-size="14">z={li*3}</text>')
        if li < 2:
            s.append(f'<path d="M{x+size+18:.0f} 210 h26" stroke="{FAINT}" stroke-width="1.6" marker-end="url(#z)"/>')
        x += size + 60
    s.append(f'<defs><marker id="z" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">'
             f'<path d="M0 0 L8 4 L0 8 z" fill="{FAINT}"/></marker></defs>')
    s.append(f'<text x="26" y="404" fill="{DIM}" font-size="15">every level: 4x the tiles</text>')
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{"".join(s)}</svg>'


def art_log():
    s = []
    x0, y = 30, 150
    w, h = 46, 62
    for i in range(11):
        x = x0 + i * (w + 6)
        active = i >= 8
        col = PINK if active else BLUE
        op = ".92" if active else ".30"
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" opacity="{op}" rx="3"/>')
        s.append(f'<text x="{x+w/2}" y="{y+h+22}" fill="{DIM}" font-size="13" text-anchor="middle">{i}</text>')
    tail = x0 + 11 * (w + 6)
    s.append(f'<path d="M{tail+4} {y+h/2} h44" stroke="{GREEN}" stroke-width="2.4" fill="none" marker-end="url(#a)"/>')
    s.append(f'<defs><marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">'
             f'<path d="M0 0 L9 4.5 L0 9 z" fill="{GREEN}"/></marker></defs>')
    s.append(f'<text x="{tail+2}" y="{y-14}" fill="{GREEN}" font-size="14">append</text>')
    s.append(f'<path d="M{x0} {y+h+40} H{x0+8*(w+6)-6}" stroke="{FAINT}" stroke-width="1.5"/>')
    s.append(f'<path d="M{x0+8*(w+6)} {y+h+40} H{tail-6}" stroke="{PINK}" stroke-opacity=".6" stroke-width="1.5"/>')
    s.append(f'<text x="{x0}" y="{y+h+62}" fill="{DIM}" font-size="13">sealed segments</text>')
    s.append(f'<text x="{x0+8*(w+6)}" y="{y+h+62}" fill="{DIM}" font-size="13">active</text>')
    s.append(f'<text x="30" y="404" fill="{DIM}" font-size="15">writes only ever go to the end</text>')
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{"".join(s)}</svg>'


def art_cardinality():
    s = []
    import math
    for i in range(26):
        op = .10 + (i / 26) * .55
        col = RED if i > 17 else BLUE
        pts = []
        for x in range(0, 561, 20):
            t = x / 560
            y = 300 - t * (i * 8.6) + math.sin(x / 45 + i) * (5 + t * 12)
            y = max(26, y)
            pts.append(f"{40+x:.0f},{y:.0f}")
        s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-opacity="{op:.2f}" stroke-width="1.6"/>')
    s.append(f'<text x="40" y="344" fill="{DIM}" font-size="14">one label added</text>')
    s.append(f'<path d="M40 356 h120" stroke="{AMBER}" stroke-width="2"/>')
    s.append(f'<text x="40" y="404" fill="{DIM}" font-size="15">series = metrics x product of cardinalities</text>')
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{"".join(s)}</svg>'


def art_windows():
    s = []
    y, w, gap, x0 = 148, 128, 18, 26
    for i in range(3):
        x = x0 + i * (w + gap)
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="92" fill="{BLUE}" opacity=".13" rx="4"/>')
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="92" fill="none" stroke="{BLUE}" stroke-opacity=".5" stroke-width="1.4" rx="4"/>')
        s.append(f'<text x="{x+4}" y="{y-12}" fill="{DIM}" font-size="13">window {i+1}</text>')
        for k in range(4):
            s.append(f'<circle cx="{x+22+k*29}" cy="{y+46}" r="7" fill="{GREEN}" opacity=".9"/>')
    wx = x0 + 3 * (w + gap) - gap
    s.append(f'<rect x="{wx}" y="{y}" width="42" height="92" fill="{AMBER}" opacity=".14" rx="4"/>')
    s.append(f'<rect x="{wx}" y="{y}" width="42" height="92" fill="none" stroke="{AMBER}" stroke-opacity=".75" stroke-width="1.4" stroke-dasharray="4 3" rx="4"/>')
    s.append(f'<circle cx="{wx+21}" cy="{y+46}" r="7" fill="{AMBER}" opacity=".95"/>')
    s.append(f'<text x="{wx-26}" y="{y+120}" fill="{AMBER}" font-size="13">watermark</text>')
    for dx in (46, 96):
        s.append(f'<circle cx="{wx+42+dx}" cy="{y+46}" r="7" fill="{RED}" opacity=".9"/>')
    s.append(f'<text x="{wx+58}" y="{y-12}" fill="{RED}" font-size="13">too late</text>')
    s.append(f'<path d="M{x0} {y+136} H{wx+150}" stroke="{FAINT}" stroke-width="1.5"/>')
    s.append(f'<text x="{x0}" y="404" fill="{DIM}" font-size="15">late enough, and no window will take it</text>')
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{"".join(s)}</svg>'


def art_collision():
    s = []
    cell, ox, oy = 62, 150, 70
    for r in range(4):
        for c in range(5):
            last = (r == 2 and c == 2)
            col = AMBER if last else BLUE
            op = ".95" if last else (".14" if (r * 5 + c) % 3 else ".22")
            s.append(f'<rect x="{ox+c*cell}" y="{oy+r*cell}" width="{cell-8}" height="{cell-8}" fill="{col}" opacity="{op}" rx="3"/>')
    tx, ty = ox + 2 * cell + (cell - 8) / 2, oy + 2 * cell + (cell - 8) / 2
    for sx, sy, col in [(30, 40, PINK), (30, 370, PURPLE)]:
        s.append(f'<path d="M{sx} {sy} Q{(sx+tx)/2:.0f} {ty:.0f} {tx-22:.0f} {ty:.0f}" stroke="{col}" stroke-width="2.6" fill="none" opacity=".9" marker-end="url(#b)"/>')
    s.append(f'<defs><marker id="b" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">'
             f'<path d="M0 0 L9 4.5 L0 9 z" fill="{PINK}"/></marker></defs>')
    s.append(f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="26" fill="none" stroke="{RED}" stroke-width="2" opacity=".8"/>')
    s.append(f'<text x="30" y="404" fill="{DIM}" font-size="15">two bookings, one room</text>')
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{"".join(s)}</svg>'


def art_storage():
    s = []
    bars = [("metadata", 730, BLUE), ("attachments", 1460, PINK)]
    y = 110
    for label, val, col in bars:
        w = val / 1460 * 520
        s.append(f'<rect x="40" y="{y}" width="{w:.0f}" height="58" fill="{col}" opacity=".85" rx="4"/>')
        s.append(f'<text x="48" y="{y+36}" fill="#0b1220" font-size="17" font-weight="700">{val} PB</text>')
        s.append(f'<text x="40" y="{y-12}" fill="{DIM}" font-size="14">{label}</text>')
        y += 108
    s.append(f'<rect x="40" y="{y}" width="520" height="58" fill="none" stroke="{AMBER}" stroke-width="2" stroke-dasharray="6 4" rx="4"/>')
    s.append(f'<text x="52" y="{y+36}" fill="{AMBER}" font-size="17" font-weight="700">2.2 EB every year</text>')
    s.append(f'<text x="40" y="404" fill="{DIM}" font-size="15">and nothing is ever deleted</text>')
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{"".join(s)}</svg>'



def art_erasure():
    """8 data chunks + 4 parity, with 4 lost and reconstructible."""
    s = []
    cw, gap, x0, y0 = 62, 12, 34, 96
    lost = {2, 5, 8, 11}
    for i in range(12):
        r, c = divmod(i, 4)
        x = x0 + c * (cw + gap)
        y = y0 + r * (cw + gap)
        parity = i >= 8
        if i in lost:
            s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{cw}" fill="none" stroke="{RED}" '
                     f'stroke-width="1.8" stroke-dasharray="5 4" rx="4" opacity=".85"/>')
            s.append(f'<path d="M{x+20} {y+20} l{cw-40} {cw-40} M{x+cw-20} {y+20} l{-(cw-40)} {cw-40}" '
                     f'stroke="{RED}" stroke-width="2" opacity=".7"/>')
        else:
            col = PURPLE if parity else BLUE
            s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{cw}" fill="{col}" opacity=".8" rx="4"/>')
            s.append(f'<text x="{x+cw/2}" y="{y+cw/2+6}" fill="#0b1220" font-size="17" font-weight="700" '
                     f'text-anchor="middle">{"p" if parity else "d"}</text>')
    bx = x0 + 4 * (cw + gap) + 22
    s.append(f'<text x="{bx}" y="{y0+30}" fill="{BLUE}" font-size="15">d = data</text>')
    s.append(f'<text x="{bx}" y="{y0+56}" fill="{PURPLE}" font-size="15">p = parity</text>')
    s.append(f'<text x="{bx}" y="{y0+82}" fill="{RED}" font-size="15">lost</text>')
    s.append(f'<text x="{x0}" y="{y0+3*(cw+gap)+18}" fill="{DIM}" font-size="15">any 8 of 12 rebuild the object</text>')
    s.append(f'<text x="{x0}" y="404" fill="{DIM}" font-size="15">50% overhead, not 200%</text>')
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{"".join(s)}</svg>'



def art_skiplist():
    """A skip list: express lanes above a sorted base list."""
    s = []
    vals = [1, 4, 7, 8, 10, 15, 26, 36, 45, 60]
    lanes = [vals, [1, 8, 15, 36, 60], [1, 15, 60]]
    x0, step, ytop = 34, 62, 96
    pos = {v: x0 + i * step for i, v in enumerate(vals)}
    for li, lane in enumerate(reversed(lanes)):
        y = ytop + li * 84
        label = ["level 2", "level 1", "base"][li]
        s.append(f'<text x="{x0-8}" y="{y-16}" fill="{DIM}" font-size="13">{label}</text>')
        for j, v in enumerate(lane):
            cx = pos[v]
            hot = v in (1, 15, 36, 45)
            col = PINK if (hot and li < 2) or (li == 2 and v == 45) else BLUE
            s.append(f'<circle cx="{cx}" cy="{y}" r="15" fill="{col}" opacity="{.92 if col==PINK else .55}"/>')
            s.append(f'<text x="{cx}" y="{y+5}" fill="#0b1220" font-size="13" font-weight="700" text-anchor="middle">{v}</text>')
            if j < len(lane) - 1:
                nx = pos[lane[j + 1]]
                s.append(f'<line x1="{cx+16}" y1="{y}" x2="{nx-16}" y2="{y}" stroke="{FAINT}" stroke-width="1.6"/>')
    s.append(f'<path d="M{pos[1]} 112 V172 M{pos[15]} 112 V172 M{pos[15]} 196 V256 M{pos[36]} 196 V256 M{pos[45]} 256 V264" '
             f'stroke="{PINK}" stroke-width="2" stroke-dasharray="4 3" opacity=".75"/>')
    s.append(f'<text x="{x0}" y="404" fill="{DIM}" font-size="15">searching 45: eleven hops, not sixty-two</text>')
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{"".join(s)}</svg>'



def art_ledger():
    """Debits on the left, credits on the right, summing to zero."""
    s = []
    x0, y0, w, rowh = 40, 96, 250, 46
    entries = [("Platform cash", 100, True), ("Seller payable", 100, False),
               ("Seller payable", 10, True), ("Platform revenue", 10, False),
               ("Seller payable", 90, True), ("Platform cash", 90, False)]
    for i, (acct, amt, is_dr) in enumerate(entries):
        y = y0 + i * rowh
        x = x0 if is_dr else x0 + w + 30
        col = BLUE if is_dr else PINK
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{rowh-8}" fill="{col}" opacity=".16" rx="4"/>')
        s.append(f'<rect x="{x}" y="{y}" width="3" height="{rowh-8}" fill="{col}" rx="2"/>')
        s.append(f'<text x="{x+14}" y="{y+25}" fill="#cbd5e1" font-size="14">{acct}</text>')
        s.append(f'<text x="{x+w-14}" y="{y+25}" fill="{col}" font-size="15" font-weight="700" text-anchor="end">${amt}</text>')
    s.append(f'<text x="{x0}" y="{y0-14}" fill="{BLUE}" font-size="13" letter-spacing="1.5">DEBIT</text>')
    s.append(f'<text x="{x0+w+30}" y="{y0-14}" fill="{PINK}" font-size="13" letter-spacing="1.5">CREDIT</text>')
    ly = y0 + len(entries) * rowh + 6
    s.append(f'<rect x="{x0}" y="{ly}" width="{2*w+30}" height="40" fill="{GREEN}" opacity=".12" rx="5"/>')
    s.append(f'<rect x="{x0}" y="{ly}" width="{2*w+30}" height="40" fill="none" stroke="{GREEN}" stroke-opacity=".55" stroke-width="1.5" rx="5"/>')
    s.append(f'<text x="{x0+(2*w+30)/2}" y="{ly+26}" fill="{GREEN}" font-size="16" font-weight="700" text-anchor="middle">'
             f'200 &#8722; 200 = 0</text>')
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{"".join(s)}</svg>'



def art_replay():
    """An immutable event log with derived state recomputed beneath it."""
    s = []
    x0, y, bw, gap = 34, 120, 52, 8
    labels = ["+100", "+50", "-30", "+20", "-45", "-10", "+25", "+60", "-15", "-5"]
    for i, lab in enumerate(labels):
        x = x0 + i * (bw + gap)
        on = i < 6
        col = GREEN if on else FAINT
        s.append(f'<rect x="{x}" y="{y}" width="{bw}" height="58" fill="{col}" opacity="{.75 if on else .35}" rx="4"/>')
        s.append(f'<text x="{x+bw/2}" y="{y+34}" fill="{"#0b1220" if on else "#94a3b8"}" font-size="14" '
                 f'font-weight="700" text-anchor="middle">{lab}</text>')
        s.append(f'<text x="{x+bw/2}" y="{y-12}" fill="{DIM}" font-size="11" text-anchor="middle">e{i+1}</text>')
    cut = x0 + 6 * (bw + gap) - gap / 2
    s.append(f'<path d="M{cut} {y-26} V{y+96}" stroke="{PINK}" stroke-width="2.2" stroke-dasharray="5 4"/>')
    s.append(f'<text x="{cut+8}" y="{y+112}" fill="{PINK}" font-size="13">replay to here</text>')
    s.append(f'<text x="{x0}" y="{y+112}" fill="{DIM}" font-size="13">immutable log</text>')
    by = y + 150
    for i, (acct, amt) in enumerate([("wallet A", "$60"), ("wallet B", "$35"), ("wallet C", "$75")]):
        bx = x0 + i * 200
        s.append(f'<rect x="{bx}" y="{by}" width="180" height="58" fill="{BLUE}" opacity=".15" rx="5"/>')
        s.append(f'<rect x="{bx}" y="{by}" width="180" height="58" fill="none" stroke="{BLUE}" stroke-opacity=".45" stroke-width="1.4" rx="5"/>')
        s.append(f'<text x="{bx+14}" y="{by+24}" fill="{DIM}" font-size="12">{acct}</text>')
        s.append(f'<text x="{bx+14}" y="{by+46}" fill="{BLUE}" font-size="18" font-weight="700">{amt}</text>')
    s.append(f'<text x="{x0}" y="{by-12}" fill="{DIM}" font-size="13">state — computed, never stored</text>')
    s.append(f'<text x="{x0}" y="404" fill="{DIM}" font-size="15">every past balance is still recoverable</text>')
    return f'<svg width="640" height="420" viewBox="0 0 640 420">{"".join(s)}</svg>'


COVERS = [
    ("proximity-service", "VOLUME 2 · CH 1", "Design a<br>Proximity Service", 58,
     "200 million businesses, 500 metres, under 100ms.", "two B-tree indexes are <i>not</i> a 2D index", art_quadtree),
    ("nearby-friends", "VOLUME 2 · CH 2", "Design<br>Nearby Friends", 62,
     "People move. The index is stale before you finish building it.", "333K in, <i>13.3M</i> out", art_fanout),
    ("google-maps", "VOLUME 2 · CH 3", "Design<br>Google Maps", 62,
     "A billion users and 100 petabytes of map tiles.", "62.5 GB/s — the CDN <i>is</i> the architecture", art_zoom),
    ("message-queue", "VOLUME 2 · CH 4", "Design a Distributed<br>Message Queue", 50,
     "Retention turns a networking problem into a storage problem.", "an append-only file beats a <i>database</i>", art_log),
    ("metrics-monitoring", "VOLUME 2 · CH 5", "Metrics Monitoring<br>and Alerting", 54,
     "The system that tells you everything else is broken.", "one label can cost you <i>everything</i>", art_cardinality),
    ("ad-click-aggregation", "VOLUME 2 · CH 6", "Ad Click Event<br>Aggregation", 58,
     "A billion clicks a day, and the numbers become invoices.", "a watermark is an optimisation, <i>not</i> correctness", art_windows),
    ("hotel-reservation", "VOLUME 2 · CH 7", "Design a Hotel<br>Reservation System", 50,
     "Three reservations per second — and the hardest design in the series.", "every read-then-write is a <i>race</i>", art_collision),
    ("email-service", "VOLUME 2 · CH 8", "Design a Distributed<br>Email Service", 50,
     "Protocols from the 1980s, carrying two exabytes a year.", "a <i>storage</i> system that sends messages", art_storage),
    ("object-storage", "VOLUME 2 · CH 9", "Design S3-like<br>Object Storage", 54,
     "Eleven nines of durability on drives that fail constantly.", "immutability is what makes it <i>tractable</i>", art_erasure),
    ("gaming-leaderboard", "VOLUME 2 · CH 10", "Real-time Gaming<br>Leaderboard", 56,
     "Ranking 25 million players, and telling each one where they stand.", "rank belongs to the <i>set</i>, not the row", art_skiplist),
    ("payment-system", "VOLUME 2 · CH 11", "Design a<br>Payment System", 58,
     "Ten transactions per second, and the hardest correctness problem yet.", "a lost cent is <i>structurally</i> impossible", art_ledger),
    ("digital-wallet", "VOLUME 2 · CH 12", "Design a<br>Digital Wallet", 58,
     "Four designs, each one fixing what the last one broke.", "store the <i>facts</i>, derive the state", art_replay),
]

def build(only=None):
    for name, badge, title, fs, tag, cap, art in COVERS:
        if only and name not in only:
            continue
        html = (SHELL.replace("__BADGE__", badge).replace("__TITLE__", title)
                     .replace("__FS__", str(fs)).replace("__TAG__", tag)
                     .replace("__CAP__", cap).replace("__ART__", art()))
        hp = os.path.join(SP, f"cv_{name}.html")
        pp = os.path.join(SP, f"cv_{name}.png")
        open(hp, "w").write(html)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1600,640", "--virtual-time-budget=8000",
                        f"--screenshot={pp}", "file://" + hp],
                       capture_output=True)
        subprocess.run(["cwebp", "-q", "90", pp, "-o", os.path.join(OUT, name + ".webp")],
                       capture_output=True)
        print("built", name)

if __name__ == "__main__":
    build(sys.argv[1:] or None)
