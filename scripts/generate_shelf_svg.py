#!/usr/bin/env python3
"""Draws assets/shelf.svg, an animated bookshelf, from data/books.md (stdlib only).

Same art style as assets/hero.svg: Gael (brown tabby and white cat), the coffee mug
and the little plant are the hero drawings, scaled down and placed on the shelf.
"""
import hashlib
import math
import pathlib
import sys
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from update_shelf import parse  # noqa: E402

OUT = ROOT / "assets" / "shelf.svg"

W = 860
FRAME_L, FRAME_R = 26, W - 26          # outer edges of the bookcase
SIDE = 14                               # side panel width
INNER_L, INNER_R = FRAME_L + SIDE + 8, FRAME_R - SIDE - 8
TOP = 176                               # y of the top board surface
BOARD = 13                              # board thickness
ROW_H = 178                             # distance between boards
GAP = 2
LEAN_GAP = 20                           # room left for a leaning "reading" book
LEAN_DEG = 7

FONT = "Segoe UI,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

PALETTES = [  # muted, vintage tones: one palette per section of data/books.md
    ["#3d5a80", "#5c4d7d", "#2f6f7e", "#4a4e8c", "#6b5b95", "#335c67", "#45617a"],   # tech
    ["#c08a3e", "#b5643c", "#a47c3b", "#8f5b3a"],                                  # mind & habits
    ["#9e4a5a", "#7d4e7e", "#4f7a65", "#b5585f", "#5e548e", "#3f6e5a", "#c27c6b"],   # off duty
]


def rnd(text, n):
    return int(hashlib.md5(text.encode("utf-8")).hexdigest()[:8], 16) % n


def short(title, limit):
    return title if len(title) <= limit else title[: max(limit - 1, 1)].rstrip() + "…"


def star(cx, cy, r):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return "M" + " L".join(pts) + "Z"


# ---------------------------------------------------------------- hero drawings
def gael(cx, base, s):
    """The hero's Gael (original coords: centre x=612, paws at y=263)."""
    return f"""
<g transform="translate({cx - 612 * s:.1f} {base - 263 * s:.1f}) scale({s})">
  <g>
    <animateTransform attributeName="transform" type="rotate" values="-6 652 250;8 652 250;-6 652 250" dur="2.8s" repeatCount="indefinite"/>
    <path d="M652 250 C692 254 706 220 686 198" fill="none" stroke="#6e5b49" stroke-width="13" stroke-linecap="round"/>
    <path d="M652 250 C692 254 706 220 686 198" fill="none" stroke="#2b231d" stroke-width="13" stroke-dasharray="4 8"/>
  </g>
  <path d="M572 258 C566 214 588 192 612 192 C636 192 658 214 652 258 Z" fill="#6e5b49"/>
  <path d="M578 232 q10 -3 16 2 M576 220 q10 -4 18 1 M581 208 q9 -3 15 2 M644 236 q-7 -3 -14 1 M646 222 q-7 -3 -14 1" stroke="#2b231d" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>
  <path d="M596 194 Q612 186 628 194 Q640 224 632 258 H592 Q584 224 596 194 Z" fill="#fbfaf7"/>
  <path d="M612 232 V256" stroke="#e4e0d8" stroke-width="2" stroke-linecap="round"/>
  <ellipse cx="602" cy="257" rx="12" ry="6" fill="#fbfaf7" stroke="#e4e0d8" stroke-width="1"/>
  <ellipse cx="622" cy="257" rx="12" ry="6" fill="#fbfaf7" stroke="#e4e0d8" stroke-width="1"/>
  <g>
    <animateTransform attributeName="transform" type="rotate" values="-2 612 196;2 612 196;-2 612 196" dur="5s" repeatCount="indefinite"/>
    <path d="M580 160 L577 120 Q577 115 582 118 L606 140 Z" fill="#6e5b49"/>
    <g><animateTransform attributeName="transform" type="rotate" values="0 640 150;0 640 150;-14 640 150;0 640 150" keyTimes="0;.82;.88;1" dur="6s" repeatCount="indefinite"/><path d="M644 160 L647 120 Q647 115 642 118 L618 140 Z" fill="#6e5b49"/></g>
    <path d="M583 150 L582 128 L598 143 Z" fill="#e0aaa6"/><path d="M641 150 L642 128 L626 143 Z" fill="#e0aaa6"/>
    <ellipse cx="612" cy="168" rx="37" ry="30" fill="#6e5b49"/>
    <path d="M612 146 C607 156 603 164 599 172 C595 186 601 197 612 197 C623 197 629 186 625 172 C621 164 617 156 612 146 Z" fill="#fbfaf7"/>
    <path d="M603 147 q1 7 -1 11 M612 145 v10 M621 147 q-1 7 1 11" stroke="#2b231d" stroke-width="3" stroke-linecap="round" fill="none"/>
    <path d="M582 166 q6 -2 10 2 M642 166 q-6 -2 -10 2 M580 176 q6 0 9 3 M644 176 q-6 0 -9 3" stroke="#2b231d" stroke-width="2.4" stroke-linecap="round" fill="none" opacity=".85"/>
    <ellipse cx="597" cy="167" rx="7.5" ry="8" fill="#b8cc4a"><animate attributeName="ry" values="8;8;.9;8" keyTimes="0;.9;.95;1" dur="4.5s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="627" cy="167" rx="7.5" ry="8" fill="#b8cc4a"><animate attributeName="ry" values="8;8;.9;8" keyTimes="0;.9;.95;1" dur="4.5s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="597" cy="167" rx="3" ry="6.5" fill="#1d1a2e"><animate attributeName="ry" values="6.5;6.5;.8;6.5" keyTimes="0;.9;.95;1" dur="4.5s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="627" cy="167" rx="3" ry="6.5" fill="#1d1a2e"><animate attributeName="ry" values="6.5;6.5;.8;6.5" keyTimes="0;.9;.95;1" dur="4.5s" repeatCount="indefinite"/></ellipse>
    <circle cx="600" cy="164" r="1.8" fill="#fff"><animate attributeName="opacity" values="1;1;0;1" keyTimes="0;.9;.95;1" dur="4.5s" repeatCount="indefinite"/></circle>
    <circle cx="630" cy="164" r="1.8" fill="#fff"><animate attributeName="opacity" values="1;1;0;1" keyTimes="0;.9;.95;1" dur="4.5s" repeatCount="indefinite"/></circle>
    <path d="M607 178 H617 L612 184 Z" fill="#f0a3b3"/>
    <path d="M612 184 Q608 191 602 187 M612 184 Q616 191 622 187" stroke="#5b4a3d" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    <path d="M598 184 H570 M599 189 L572 197 M626 184 H654 M625 189 L652 197" stroke="#fff" stroke-width="1.3" stroke-linecap="round" opacity=".9"/>
  </g>
</g>"""


def mug(cx, base, s):
    """The hero's mug (original coords: centre x=472, base y=258)."""
    return f"""
<g transform="translate({cx - 472 * s:.1f} {base - 258 * s:.1f}) scale({s})">
  <path d="M504 212 Q530 212 530 232 Q530 250 504 250" fill="none" stroke="#e8dcc6" stroke-width="8" stroke-linecap="round"/>
  <path d="M440 198 H504 V238 Q504 258 472 258 Q440 258 440 238 Z" fill="url(#mug)"/>
  <ellipse cx="472" cy="198" rx="32" ry="7" fill="#5b3a29" stroke="#fffaf0" stroke-width="2"/>
  <path d="M472 240 C458 230 460 220 466 220 C469 220 471 222 472 224 C473 222 475 220 478 220 C484 220 486 230 472 240 Z" fill="#ff7a90"/>
  <g fill="none" stroke="#c9c6f0" stroke-width="4" stroke-linecap="round" opacity="0">
    <path d="M458 186 C448 172 468 164 458 148 C452 138 462 132 460 126"><animate attributeName="opacity" values="0;.7;0" dur="3.6s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 6;0 -10" dur="3.6s" repeatCount="indefinite"/></path>
    <path d="M474 186 C464 172 484 164 474 148 C468 138 478 132 476 126"><animate attributeName="opacity" values="0;.7;0" dur="3.6s" begin="1.2s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 6;0 -10" dur="3.6s" begin="1.2s" repeatCount="indefinite"/></path>
    <path d="M490 186 C480 172 500 164 490 148 C484 138 494 132 492 126"><animate attributeName="opacity" values="0;.7;0" dur="3.6s" begin="2.4s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 6;0 -10" dur="3.6s" begin="2.4s" repeatCount="indefinite"/></path>
  </g>
</g>"""


def plant(cx, base, s):
    """The hero's plant (original coords: centre x=766, pot bottom y=196)."""
    return f"""
<g transform="translate({cx - 766 * s:.1f} {base - 196 * s:.1f}) scale({s})">
  <path d="M748 196 H784 L779 174 H753 Z" fill="#e07a5f"/>
  <rect x="750" y="172" width="32" height="5" rx="2" fill="#c96a50"/>
  <g>
    <animateTransform attributeName="transform" type="rotate" values="-3 766 176;3 766 176;-3 766 176" dur="4s" repeatCount="indefinite"/>
    <path d="M766 176 C752 170 746 156 750 144 C762 148 768 160 766 176 Z" fill="#4ade80"/>
    <path d="M766 176 C780 170 786 156 782 144 C770 148 764 160 766 176 Z" fill="#22c55e"/>
    <path d="M766 176 C760 160 762 146 766 136 C770 146 772 160 766 176 Z" fill="#86efac"/>
  </g>
</g>"""


def lying_stack(x, base):
    """A small decorative stack of books lying flat (not data, just decor)."""
    return f"""
<g>
  <rect x="{x}" y="{base - 15}" width="92" height="15" rx="3" fill="#4f7a8c"/><rect x="{x + 84}" y="{base - 12}" width="6" height="9" rx="1.5" fill="#e9e2cf"/>
  <rect x="{x + 6}" y="{base - 30}" width="82" height="15" rx="3" fill="#8c6a9e"/><rect x="{x + 22}" y="{base - 30}" width="4" height="19" rx="1" fill="#c75c5c"/><rect x="{x + 80}" y="{base - 27}" width="6" height="9" rx="1.5" fill="#efe6d6"/>
  <g transform="rotate(-4 {x + 44} {base - 38})"><rect x="{x}" y="{base - 45}" width="88" height="15" rx="3" fill="#6f9a7a"/><rect x="{x + 80}" y="{base - 42}" width="6" height="9" rx="1.5" fill="#ece4d0"/></g>
</g>"""


# ---------------------------------------------------------------- books
GOLD = "#e9c46a"


def spine(b, x, board_y, section):
    """Returns (shapes, overlay). Shapes get the hand-drawn filter; text stays crisp."""
    w, hh, color, t = b["w"], b["h"], b["color"], b["title"]
    y = board_y - hh
    cx = x + w / 2
    thin = w < 25
    style = rnd(t + "s", 3)
    if thin and style == 1:
        style = 0
    bulge = 0.8 + rnd(t + "b", 6) / 10
    body = (f"M{x} {y + 3} Q{cx:.1f} {y - 1.5} {x + w} {y + 3} "
            f"Q{x + w + bulge:.1f} {(y + board_y) / 2:.1f} {x + w} {board_y + 1} L{x} {board_y + 1} "
            f"Q{x - bulge:.1f} {(y + board_y) / 2:.1f} {x} {y + 3} Z")
    sh = [f'<path d="{body}" fill="{color}"/>', f'<path d="{body}" fill="url(#cyl)"/>']
    ov = []
    text_top, text_bottom = y + 18, board_y - 14
    if style == 0:    # classic hardcover: gilded bands
        for dy in (9, 13):
            sh.append(f'<path d="M{x} {y + dy + 3} Q{cx:.1f} {y + dy - 1.5} {x + w} {y + dy + 3}" fill="none" stroke="{GOLD}" stroke-width="1.4" opacity=".8"/>')
        for dy in (9, 13):
            sh.append(f'<path d="M{x} {board_y - dy} H{x + w}" stroke="{GOLD}" stroke-width="1.4" opacity=".8"/>')
        text_top, text_bottom = y + 22, board_y - 18
    elif style == 1:  # paper label near the bottom
        lw = w - 10
        sh.append(f'<rect x="{x + 5}" y="{board_y - 30}" width="{lw}" height="18" rx="3" fill="#f3e9d2" opacity=".92"/>')
        sh.append(f'<path d="M{x + 9} {board_y - 24} H{x + w - 9} M{x + 11} {board_y - 19} H{x + w - 11}" stroke="#7a6a58" stroke-width="1" opacity=".6"/>')
        sh.append(f'<path d="M{x} {y + 3} Q{cx:.1f} {y - 1.5} {x + w} {y + 3} V{y + 12} H{x} Z" fill="#000" opacity=".2"/>')
        text_top, text_bottom = y + 20, board_y - 36
    else:             # cloth binding: soft texture and a dark cap
        sh.append(f'<path d="M{x} {y + 3} Q{cx:.1f} {y - 1.5} {x + w} {y + 3} V{y + 16} H{x} Z" fill="#000" opacity=".18"/>')
        sh.append(f'<path d="M{x + w * .3:.1f} {y + 18} V{board_y - 4} M{x + w * .7:.1f} {y + 18} V{board_y - 4}" stroke="#fff" stroke-width=".8" opacity=".07"/>')
        sh.append(f'<rect x="{x}" y="{board_y - 9}" width="{w}" height="9" fill="#000" opacity=".16"/>')
        text_top = y + 24

    star_cy = None
    if b["status"] == "read":                         # star lives inside the spine, never above it
        star_cy = text_top + 4
        text_top += 16
    serif = section == 2
    fs = round(min(max(w * 0.36, 8), 13), 1)          # font grows with the spine width
    char_w = fs * (0.55 if serif else 0.6)
    title = escape(short(t, int((text_bottom - text_top) / char_w)))
    fam = 'Georgia,"Times New Roman",serif' if serif else FONT
    weight = "400" if serif else "600"
    fill = "#fbe7b5" if style == 0 else "#fffaf0"
    mid = (text_top + text_bottom) / 2                  # centre the title along the spine
    ov.append(f'<text transform="translate({cx + fs * 0.36:.1f} {mid:.1f}) rotate(90)" text-anchor="middle" font-family={fam!r} '
              f'font-size="{fs}" font-weight="{weight}" fill="{fill}" letter-spacing=".3">{title}</text>')

    if b["status"] == "read":
        sh.append(f'<path d="M{x} {board_y - 5} H{x + w} V{board_y} H{x} Z" fill="#f4c542"/>')
        sr = min(w * 0.3, 8)
        ov.append(f'<circle cx="{cx:.1f}" cy="{star_cy:.1f}" r="{sr + 2:.1f}" fill="#fde68a" opacity=".25">'
                  f'<animate attributeName="r" values="{sr:.1f};{sr + 4:.1f};{sr:.1f}" dur="2.6s" repeatCount="indefinite"/></circle>'
                  f'<path d="{star(cx, star_cy, sr)}" fill="#fcd34d" stroke="#b7791f" stroke-width="1" stroke-linejoin="round"/>')

    if b["status"] == "reading":
        rx_ = x + w * 0.62
        ov.append(f'<path d="M{rx_ - 3.5:.1f} {y + 4} V{y - 15} l3.5 4 l3.5 -4 V{y + 4} Z" fill="#d94b4b">'
                  f'<animateTransform attributeName="transform" type="rotate" values="-5 {rx_:.1f} {y + 4};5 {rx_:.1f} {y + 4};-5 {rx_:.1f} {y + 4}" dur="2.6s" repeatCount="indefinite"/></path>')
        tr = f'rotate(-{LEAN_DEG} {x} {board_y})'
    else:
        tilt = (rnd(t + "a", 17) - 8) / 10    # -0.8 .. 0.8 degrees, like real books
        tr = f'rotate({tilt} {cx:.1f} {board_y + 1})'
    return (f'<g transform="{tr}">' + "".join(sh) + "</g>",
            f'<g transform="{tr}">' + "".join(ov) + "</g>")


def wood_board(x1, x2, y, ext=0):
    x1, x2 = x1 - ext, x2 + ext
    grain = "".join(
        f'<path d="M{x1 + 6} {y + gy} C{x1 + (x2 - x1) * .3:.0f} {y + gy - 1.6} {x1 + (x2 - x1) * .6:.0f} {y + gy + 1.8} {x2 - 6} {y + gy - .5}" '
        f'fill="none" stroke="#5a2f17" stroke-width=".9" opacity=".28"/>' for gy in (4.5, 8.5))
    return (f'<g><rect x="{x1}" y="{y}" width="{x2 - x1}" height="{BOARD}" rx="4" fill="url(#wood)"/>{grain}'
            f'<rect x="{x1 + 2}" y="{y + 1}" width="{x2 - x1 - 4}" height="2" rx="1" fill="#e9b88a" opacity=".55"/></g>')


def garland(y_ends, y_mid):
    x1, x2 = FRAME_L + 6, FRAME_R - 6
    p0, p1, p2, p3 = (x1, y_ends), (x1 + 260, y_mid + 20), (x2 - 260, y_mid + 20), (x2, y_ends)
    out = [f'<path d="M{x1} {y_ends} C{p1[0]} {p1[1]} {p2[0]} {p2[1]} {x2} {y_ends}" fill="none" stroke="#3b2f4f" stroke-width="1.6"/>']
    colors = ["#ffd27a", "#ff9fb7", "#a7f3d0", "#ffd27a", "#c4b5fd"]
    n = 17
    for i in range(1, n):
        tt = i / n
        bx = (1 - tt) ** 3 * p0[0] + 3 * (1 - tt) ** 2 * tt * p1[0] + 3 * (1 - tt) * tt ** 2 * p2[0] + tt ** 3 * p3[0]
        by = (1 - tt) ** 3 * p0[1] + 3 * (1 - tt) ** 2 * tt * p1[1] + 3 * (1 - tt) * tt ** 2 * p2[1] + tt ** 3 * p3[1]
        c = colors[i % len(colors)]
        d = (i * 0.37) % 2.4
        out.append(f'<circle cx="{bx:.1f}" cy="{by + 5:.1f}" r="9" fill="url(#bulb)" opacity=".7">'
                   f'<animate attributeName="opacity" values=".25;.85;.25" dur="2.4s" begin="{d:.2f}s" repeatCount="indefinite"/></circle>'
                   f'<path d="M{bx:.1f} {by:.1f} v2" stroke="#3b2f4f" stroke-width="2"/>'
                   f'<ellipse cx="{bx:.1f}" cy="{by + 5:.1f}" rx="2.6" ry="3.4" fill="{c}"/>')
    return "".join(out)


def spine_width(t):
    kind = rnd(t + "k", 10)
    if kind < 3:
        return 18 + rnd(t + "w", 6)    # thin: 18-23 px
    if kind < 8:
        return 28 + rnd(t + "w", 10)   # medium: 28-37 px
    return 40 + rnd(t + "w", 8)        # thick: 40-47 px


def build():
    sections = parse((ROOT / "data" / "books.md").read_text(encoding="utf-8"))
    books = []
    for si, sec in enumerate(sections):
        pal = PALETTES[si % len(PALETTES)]
        for b in sec["books"]:
            t = b["title"]
            books.append({**b, "section": si, "color": pal[rnd(t, len(pal))],
                          "w": spine_width(t), "h": 118 + rnd(t + "h", 46)})

    rows, cur, used = [], [], 0
    avail = INNER_R - INNER_L
    for b in books:
        lead = LEAN_GAP if b["status"] == "reading" else 0
        need = b["w"] + lead + (GAP if cur else 0)
        if cur and used + need > avail:
            rows.append((cur, used))
            cur, used, need = [], 0, b["w"] + lead
        cur.append(b)
        used += need
    if cur:
        rows.append((cur, used))

    counts = {"read": 0, "reading": 0, "todo": 0}
    for b in books:
        counts[b["status"]] += 1

    bottom = TOP + BOARD + len(rows) * ROW_H
    H = bottom + 64
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         f'aria-label="Bookshelf with Gael the cat: {counts["read"]} read, {counts["reading"]} reading, {counts["todo"]} to read">']
    o.append(f"""<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#171a3a"/><stop offset=".55" stop-color="#2b2559"/><stop offset="1" stop-color="#4a3270"/></linearGradient>
  <linearGradient id="back" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#21182e"/><stop offset="1" stop-color="#2e2138"/></linearGradient>
  <linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9784a"/><stop offset=".4" stop-color="#9a5c36"/><stop offset="1" stop-color="#6a3b20"/></linearGradient>
  <linearGradient id="woodside" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6a3b20"/><stop offset=".55" stop-color="#9a5c36"/><stop offset="1" stop-color="#78452a"/></linearGradient>
  <linearGradient id="cyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".3"/><stop offset=".2" stop-color="#fff" stop-opacity=".14"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".32"/></linearGradient>
  <linearGradient id="mug" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e8dcc6"/><stop offset=".5" stop-color="#fffaf0"/><stop offset="1" stop-color="#d9cbb0"/></linearGradient>
  <linearGradient id="shadow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".5"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
  <radialGradient id="bulb"><stop offset="0" stop-color="#ffe2a8" stop-opacity=".9"/><stop offset="1" stop-color="#ffe2a8" stop-opacity="0"/></radialGradient>
  <radialGradient id="warm" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffcf8a" stop-opacity=".22"/><stop offset="1" stop-color="#ffcf8a" stop-opacity="0"/></radialGradient>
  <radialGradient id="vignette" cx=".5" cy=".45" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient>
  <filter id="soft" x="-10%" y="-10%" width="125%" height="120%">
    <feDropShadow dx="1.6" dy="0" stdDeviation="1.4" flood-color="#0b0614" flood-opacity=".45"/>
  </filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
    <feComponentTransfer><feFuncA type="table" tableValues="0 .09"/></feComponentTransfer>
  </filter>
  <clipPath id="round"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#round)">
<rect width="{W}" height="{H}" fill="url(#sky)"/>""")

    for sx, sy, d in ((330, 30, 0), (420, 64, 1.1), (470, 20, 2.2), (560, 46, .6), (250, 26, 1.7), (800, 26, 2.8), (620, 18, 1.4)):
        o.append(f'<circle cx="{sx}" cy="{sy}" r="1.5" fill="#fff"><animate attributeName="opacity" values=".2;1;.2" dur="3s" begin="{d}s" repeatCount="indefinite"/></circle>')

    rl = "lido" if counts["read"] == 1 else "lidos"
    o.append(f'<text x="40" y="52" font-family={"Georgia,serif"!r} font-size="27" font-style="italic" fill="#f5d0fe">biblioKet</text>')
    o.append(f'<text x="40" y="78" font-family="{MONO}" font-size="13" fill="#c9c6f0" letter-spacing="1">a estante da Ketleen \u00b7 '
             f'{counts["read"]} {rl} \u00b7 {counts["reading"]} lendo \u00b7 {counts["todo"]} na fila</text>')

    o.append(garland(102, 112))
    o.append(f'<ellipse cx="640" cy="{TOP - 40}" rx="230" ry="90" fill="url(#warm)"/>')

    # bookcase body
    o.append(f'<rect x="{FRAME_L}" y="{TOP}" width="{FRAME_R - FRAME_L}" height="{bottom - TOP}" fill="url(#back)"/>')
    for i in range(1, 9):  # back planks with a hint of grain
        px = FRAME_L + i * (FRAME_R - FRAME_L) / 9
        o.append(f'<path d="M{px:.0f} {TOP} C{px + 3:.0f} {TOP + 120} {px - 3:.0f} {bottom - 160} {px:.0f} {bottom}" fill="none" stroke="#000" stroke-opacity=".18" stroke-width="1.4"/>')
    for sx in (FRAME_L, FRAME_R - SIDE):
        o.append(f'<g><rect x="{sx}" y="{TOP}" width="{SIDE}" height="{bottom - TOP + BOARD}" rx="3" fill="url(#woodside)"/>'
                 f'<path d="M{sx + 5} {TOP + 20} C{sx + 7} {TOP + 160} {sx + 3} {bottom - 200} {sx + 6} {bottom - 10}" fill="none" stroke="#5a2f17" stroke-width=".9" opacity=".35"/>'
                 f'<path d="M{sx + 9} {TOP + 60} C{sx + 11} {TOP + 220} {sx + 7} {bottom - 120} {sx + 10} {bottom - 40}" fill="none" stroke="#5a2f17" stroke-width=".9" opacity=".25"/></g>')

    # decor on top of the case
    o.append(plant(150, TOP, 0.95))
    o.append(lying_stack(200, TOP))
    o.append(mug(560, TOP, 0.62))
    o.append(gael(700, TOP + 2, 0.74))
    o.append(wood_board(FRAME_L, FRAME_R, TOP, ext=8))
    o.append(f'<rect x="{FRAME_L + SIDE}" y="{TOP + BOARD}" width="{FRAME_R - FRAME_L - 2 * SIDE}" height="12" fill="url(#shadow)"/>')
    o.append(f'<g transform="rotate(-2 700 {TOP + 12})"><rect x="676" y="{TOP + 4}" width="48" height="16" rx="4" fill="#fbfaf7"/>'
             f'<text x="700" y="{TOP + 16}" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="#6e5b49">Gael</text></g>')

    for ri, (row, used) in enumerate(rows):
        board_y = TOP + BOARD + (ri + 1) * ROW_H - BOARD
        x = INNER_L
        shapes, overlays = [], []
        for b in row:
            if b["status"] == "reading":
                x += LEAN_GAP
            s_, v_ = spine(b, x, board_y, b["section"])
            shapes.append(s_)
            overlays.append(v_)
            x += b["w"] + GAP
        o.append('<g filter="url(#soft)">' + "".join(shapes) + "</g>")
        o.append("<g>" + "".join(overlays) + "</g>")
        free = INNER_R - x
        if free >= 230:
            o.append(lying_stack(INNER_R - 112, board_y))
            o.append(plant(INNER_R - 165, board_y, 0.95))
        elif free >= 120:
            o.append(lying_stack(INNER_R - 102, board_y))
        o.append(wood_board(FRAME_L + SIDE - 2, FRAME_R - SIDE + 2, board_y))
        o.append(f'<rect x="{INNER_L - 2}" y="{board_y + 1}" width="{x - INNER_L + 2}" height="3" rx="1.5" fill="#1a0d06" opacity=".35"/>')
        o.append(f'<rect x="{FRAME_L + SIDE}" y="{board_y + BOARD}" width="{FRAME_R - FRAME_L - 2 * SIDE}" height="12" fill="url(#shadow)"/>')

    ly = bottom + 40
    f = f'font-family="{MONO}" font-size="12" fill="#ddd6fe" letter-spacing=".5"'
    o.append(f'<path d="{star(50, ly - 4, 8)}" fill="#fcd34d" stroke="#b7791f" stroke-width="1"/><text x="66" y="{ly}" {f}>lido \u00b7 read</text>')
    o.append(f'<g transform="rotate(-{LEAN_DEG} 214 {ly + 6})"><rect x="208" y="{ly - 12}" width="12" height="18" rx="2" fill="#5c4d7d"/>'
             f'<path d="M214 {ly - 12} v-6 h4 v6 Z" fill="#d94b4b"/></g><text x="232" y="{ly}" {f}>lendo \u00b7 reading</text>')
    o.append(f'<rect x="396" y="{ly - 12}" width="12" height="18" rx="2" fill="#9e4a5a"/><text x="418" y="{ly}" {f}>na fila \u00b7 to read</text>')
    o.append(f'<text x="{W - 40}" y="{ly}" text-anchor="end" font-family="{MONO}" font-size="11" fill="#8f86c9">auto-updated from data/books.md</text>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')
    o.append(f'<rect width="{W}" height="{H}" filter="url(#grain)"/>')
    o.append("</g></svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print("wrote", OUT)
