#!/usr/bin/env python3
"""Generate crisp, dual-theme animated pixel SVGs for kenji0011's GitHub profile README.

Outputs:
  - assets/hero-dark.svg
  - assets/hero-light.svg
  - assets/divider-dark.svg
  - assets/divider-light.svg

All typography in the display header and all sprites are compiled directly into
integer-aligned <rect> geometry with shape-rendering="crispEdges" so GitHub's
<img> / <picture> sanitizer renders razor-sharp pixel art with zero external
font dependencies and zero JavaScript.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"

THEMES: Dict[str, Dict[str, str]] = {
    "dark": {
        "canvas": "#09090b",
        "panel": "#111113",
        "bar": "#18181b",
        "subtle": "#18181b",
        "surface": "#27272a",
        "border": "#27272a",
        "border_hi": "#3f3f46",
        "muted": "#71717a",
        "secondary": "#a1a1aa",
        "fg": "#fafafa",
        "accent": "#22c55e",
        "accent_soft": "#4ade80",
        "accent_dim": "#14532d",
        "screen_bg": "#09090b",
        "glint": "#ffffff",
    },
    "light": {
        "canvas": "#fafafa",
        "panel": "#ffffff",
        "bar": "#f4f4f5",
        "subtle": "#f4f4f5",
        "surface": "#e4e4e7",
        "border": "#e4e4e7",
        "border_hi": "#d4d4d8",
        "muted": "#71717a",
        "secondary": "#52525b",
        "fg": "#09090b",
        "accent": "#10b981",
        "accent_soft": "#059669",
        "accent_dim": "#d1fae5",
        "screen_bg": "#18181b",
        "glint": "#09090b",
    },
}

# Handcrafted 5x7 pixel-bitmap font for crisp, OS-independent display text.
FONT_5X7: Dict[str, List[str]] = {
    "A": [
        ".###.",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
    ],
    "E": [
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#####",
    ],
    "H": [
        "#...#",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
    ],
    "K": [
        "#...#",
        "#..#.",
        "#.#..",
        "##...",
        "#.#..",
        "#..#.",
        "#...#",
    ],
    "L": [
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#####",
    ],
    "N": [
        "#...#",
        "##..#",
        "#.#.#",
        "#..##",
        "#...#",
        "#...#",
        "#...#",
    ],
    "P": [
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#....",
        "#....",
        "#....",
    ],
    "S": [
        ".####",
        "#....",
        "#....",
        ".###.",
        "....#",
        "....#",
        "####.",
    ],
    "V": [
        "#...#",
        "#...#",
        "#...#",
        ".#.#.",
        ".#.#.",
        "..#..",
        "..#..",
    ],
    "O": [
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ],
    "R": [
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#.#..",
        "#..#.",
        "#...#",
    ],
    "U": [
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ],
    " ": [
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
    ],
}

# Compact 3x5 pixel micro-font for tiny pixel indicators (e.g., OK, PASS, RUN).
FONT_3X5: Dict[str, List[str]] = {
    "A": [".#.", "#.#", "###", "#.#", "#.#"],
    "K": ["#.#", "#.#", "##.", "#.#", "#.#"],
    "N": ["###", "#.#", "#.#", "#.#", "#.#"],
    "O": ["###", "#.#", "#.#", "#.#", "###"],
    "P": ["###", "#.#", "###", "#..", "#.."],
    "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "S": [".##", "#..", ".#.", "..#", "##."],
    "U": ["#.#", "#.#", "#.#", "#.#", "###"],
    ">": ["#..", ".#.", "..#", ".#.", "#.."],
    "_": ["...", "...", "...", "...", "###"],
    "[": ["##.", "#..", "#..", "#..", "##."],
    "]": [".##", "..#", "..#", "..#", ".##"],
    " ": ["..", "..", "..", "..", ".."],
}


def rect(
    x: int,
    y: int,
    w: int,
    h: int,
    fill: str,
    opacity: float | None = None,
    cls: str | None = None,
) -> str:
    attrs = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"', f'fill="{fill}"']
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    if cls:
        attrs.append(f'class="{cls}"')
    return f"  <rect {' '.join(attrs)} />"


def render_pixel_text(
    text: str,
    x0: int,
    y0: int,
    px: int,
    fill: str,
    font: Dict[str, List[str]] = FONT_5X7,
    gap_cols: int = 1,
    cls: str | None = None,
) -> Tuple[List[str], int]:
    """Render pixel-bitmap text as crisp merged horizontal <rect> spans."""
    elements: List[str] = []
    cursor_x = x0
    for ch in text:
        glyph = font[ch]
        width_cols = len(glyph[0])
        for row_idx, row in enumerate(glyph):
            col = 0
            while col < width_cols:
                if row[col] == "#":
                    start = col
                    while col < width_cols and row[col] == "#":
                        col += 1
                    span = col - start
                    elements.append(
                        rect(
                            cursor_x + start * px,
                            y0 + row_idx * px,
                            span * px,
                            px,
                            fill,
                            cls=cls,
                        )
                    )
                else:
                    col += 1
        cursor_x += (width_cols + gap_cols) * px
    total_w = cursor_x - x0 - gap_cols * px
    return elements, total_w


def render_sprite(
    grid: List[str],
    x0: int,
    y0: int,
    px: int,
    palette: Dict[str, str],
) -> List[str]:
    """Render an ASCII-art pixel matrix using merged horizontal spans."""
    elements: List[str] = []
    for r, row in enumerate(grid):
        c = 0
        n = len(row)
        while c < n:
            ch = row[c]
            if ch in palette:
                start = c
                while c < n and row[c] == ch:
                    c += 1
                elements.append(
                    rect(x0 + start * px, y0 + r * px, (c - start) * px, px, palette[ch])
                )
            else:
                c += 1
    return elements


def build_hero_svg(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 850, 240
    parts: List[str] = []

    # Subtle background dot matrix inside terminal body
    dots: List[str] = []
    for dx in range(24, w - 16, 24):
        for dy in range(48, h - 14, 24):
            dots.append(rect(dx, dy, 2, 2, t["border"], opacity=0.35))

    # Crisp 8-bit notched border frame (2px stroke, 4px corner steps)
    frame_rects = [
        # Outer panel fill (notched corners)
        rect(6, 2, w - 12, h - 4, t["panel"]),
        rect(2, 6, w - 4, h - 12, t["panel"]),
        # Titlebar fill
        rect(6, 4, w - 12, 28, t["bar"]),
        rect(4, 6, w - 8, 26, t["bar"]),
        # Top & bottom border
        rect(6, 2, w - 12, 2, t["border"]),
        rect(6, h - 4, w - 12, 2, t["border"]),
        # Left & right border
        rect(2, 6, 2, h - 12, t["border"]),
        rect(w - 4, 6, 2, h - 12, t["border"]),
        # 4 stepped corner pixels
        rect(4, 4, 2, 2, t["border"]),
        rect(w - 6, 4, 2, 2, t["border"]),
        rect(4, h - 6, 2, 2, t["border"]),
        rect(w - 6, h - 6, 2, 2, t["border"]),
        # Titlebar divider line
        rect(4, 32, w - 8, 2, t["border"]),
        # Monochrome pixel window controls (left)
        rect(18, 15, 6, 6, t["border_hi"]),
        rect(30, 15, 6, 6, t["border_hi"]),
        rect(42, 15, 6, 6, t["muted"]),
    ]

    # Pixel-bitmap Display Name: "KEAN SALVAHAN"
    title_x, title_y, title_px = 30, 68, 6
    shadow_rects, title_w = render_pixel_text(
        "KEAN SALVAHAN", title_x + 3, title_y + 3, title_px, t["surface"]
    )
    title_rects, _ = render_pixel_text(
        "KEAN SALVAHAN", title_x, title_y, title_px, t["fg"]
    )

    # Pixel dashed divider under subtitle
    sep_rects: List[str] = []
    for sx in range(30, 534, 8):
        sep_rects.append(rect(sx, 144, 4, 2, t["border"]))

    # Recessed terminal prompt box (x=30..536, y=158..216)
    term_box = [
        rect(32, 158, 502, 58, t["canvas"]),
        rect(30, 160, 506, 54, t["canvas"]),
        rect(32, 158, 502, 2, t["border"]),
        rect(32, 214, 502, 2, t["border"]),
        rect(30, 160, 2, 54, t["border"]),
        rect(534, 160, 2, 54, t["border"]),
    ]

    # Right-side Pixel-Art Monochrome Workstation (4px uniform pixel grid)
    # Origin inside right pane: x=566, y=46  (64x44 grid -> 256x176)
    wx, wy, u = 568, 46, 4

    # Monitor bezel, screen, stand, desk, mug (static shell)
    workstation_palette = {
        "B": t["border_hi"],  # outer monitor bezel / dark chrome
        "H": t["muted"],      # bevel highlight
        "S": t["screen_bg"],  # monitor CRT/flat dark screen
        "D": t["border"],     # desk & stand base dark
        "M": t["secondary"],  # mug body / accents
        "F": t["fg"],         # crisp highlight
        "A": t["accent"],     # power LED
        "U": t["surface"],    # subtle depth / desk shadow
    }

    # Build static workstation scene on a 64-col x 44-row grid
    ws_static: List[str] = []
    # Monitor body: cols 6..40 (35 cols), rows 5..26 (22 rows)
    for r in range(44):
        row = ["."] * 64
        # Monitor outer bezel
        if r == 5:
            for c in range(7, 40):
                row[c] = "B"
        elif r == 6:
            row[6] = "B"
            for c in range(7, 40):
                row[c] = "H"
            row[40] = "B"
        elif 7 <= r <= 24:
            row[6] = "B"
            row[7] = "B"
            for c in range(8, 39):
                row[c] = "S"
            row[39] = "B"
            row[40] = "B"
        elif r == 25:
            row[6] = "B"
            for c in range(7, 40):
                row[c] = "B"
            row[40] = "B"
            row[37] = "A"  # monitor emerald power LED
            row[38] = "A"
        elif r == 26:
            for c in range(7, 40):
                row[c] = "D"

        # Monitor stand neck & base
        if 27 <= r <= 30:
            for c in range(21, 26):
                row[c] = "B"
            row[22] = "H"
        if r == 31:
            for c in range(15, 32):
                row[c] = "H"
        if r == 32:
            for c in range(14, 33):
                row[c] = "B"

        # Mini Coffee Mug on right of desk (cols 46..53, rows 26..32)
        if r == 26:
            for c in range(47, 53):
                row[c] = "F"
        elif 27 <= r <= 31:
            row[46] = "H"
            for c in range(47, 53):
                row[c] = "M"
            row[53] = "H"
            # Handle
            if r in (28, 30):
                row[54] = "H"
                row[55] = "H"
            elif r == 29:
                row[55] = "H"
        elif r == 32:
            for c in range(47, 53):
                row[c] = "B"

        # Desk surface (row 33) & shadow (row 34)
        if r == 33:
            for c in range(2, 62):
                row[c] = "H"
        elif r == 34:
            for c in range(2, 62):
                row[c] = "U"

        # Subtle hardware rack / LED strip under desk (rows 37..40)
        if r == 37:
            for c in range(6, 58):
                row[c] = "D"
        elif r in (38, 39):
            row[6] = "D"
            row[57] = "D"
            for c in range(7, 57):
                row[c] = "U"
        elif r == 40:
            for c in range(6, 58):
                row[c] = "D"

        ws_static.append("".join(row))

    ws_static_rects = render_sprite(ws_static, wx, wy, u, workstation_palette)

    # Monitor screen content frames (screen interior: cols 9..37, rows 8..23)
    # Screen always stays dark (#09090b / #18181b) for authentic high-contrast terminal feel
    scr_palette = {
        "W": "#fafafa",
        "G": "#22c55e",
        "L": "#4ade80",
        "D": "#3f3f46",
        "M": "#71717a",
        "S": "#a1a1aa",
    }

    # Screen Frame 0: Data Analytics Bar Chart + KPI strip
    scr_f0 = [
        "WWWW..MMMMMM.........GGG...",  # r=9  top header bar + status
        "...........................",
        "DDDDDDDDDDDDDDDDDDDDDDDDDDD",  # r=11 axis divider
        ".......................GGG.",
        ".................SSS...GGG.",
        ".................SSS...GGG.",
        "...........MMM...SSS...GGG.",
        ".....MMM...MMM...SSS...GGG.",
        ".....MMM...MMM...SSS...GGG.",
        ".DDD.MMM...MMM...SSS...GGG.",
        ".DDD.MMM...MMM...SSS...GGG.",
        ".DDD.MMM...MMM...SSS...GGG.",
        "DDDDDDDDDDDDDDDDDDDDDDDDDDD",  # r=21 baseline
    ]
    scr_f0_rects = render_sprite(scr_f0, wx + 10 * u, wy + 9 * u, u, scr_palette)

    # Screen Frame 1: QA Automation Test Suite [PASS]
    scr_f1 = [
        "SSSS..MMMM...........GGG...",
        "...........................",
        ".GG..WWWWWWWWWW....MMMM....",
        "...........................",
        ".GG..WWWWWWWWWWWW..MMMM....",
        "...........................",
        ".GG..WWWWWWWW......MMMM....",
        "...........................",
        ".GG..WWWWWWWWWW....MMMM....",
        "...........................",
        "DDDDDDDDDDDDDDDDDDDDDDDDDDD",
        ".GGG..GGGG..GGGG..GGGG.....",
        "...........................",
    ]
    scr_f1_rects = render_sprite(scr_f1, wx + 10 * u, wy + 9 * u, u, scr_palette)

    # Screen Frame 2: Rust + SQLite System Telemetry Waveform
    scr_f2 = [
        "WWWW..SSS............GGG...",
        "...........................",
        "..................GGG......",
        ".................G...G.....",
        "........SSS.....G.....G....",
        ".......S...S...G.......G...",
        "......S.....S.G.........G..",
        ".SSSSS.......G...........GG",
        "...........................",
        "DDDDDDDDDDDDDDDDDDDDDDDDDDD",
        ".GGG..MMMMMM....SSSS.......",
        "...........................",
        ".DDD..WWWWWW....GGGG.......",
    ]
    scr_f2_rects = render_sprite(scr_f2, wx + 10 * u, wy + 9 * u, u, scr_palette)

    # Rising pixel steam over the mug (cols 48..52, rows 19..24) - 3 frames
    steam_palette = {"S": t["muted"], "L": t["border_hi"]}
    steam_f0 = [
        "..L..",
        ".S...",
        "..S..",
        ".S...",
        "..S..",
    ]
    steam_f1 = [
        ".L...",
        "..S..",
        ".S...",
        "..S..",
        ".S...",
    ]
    steam_f2 = [
        "...L.",
        "..S..",
        "...S.",
        "..S..",
        ".S...",
    ]
    steam0_rects = render_sprite(steam_f0, wx + 47 * u, wy + 20 * u, u, steam_palette)
    steam1_rects = render_sprite(steam_f1, wx + 47 * u, wy + 20 * u, u, steam_palette)
    steam2_rects = render_sprite(steam_f2, wx + 47 * u, wy + 20 * u, u, steam_palette)

    # Animated under-desk telemetry LED blocks (inside rows 38..39, cols 9..55)
    led_y = wy + 38 * u + 2
    rack_leds = [
        rect(wx + 9 * u, led_y, 8, 4, t["accent"], cls="led-a"),
        rect(wx + 12 * u, led_y, 8, 4, t["muted"], cls="led-b"),
        rect(wx + 15 * u, led_y, 8, 4, t["accent_soft"], cls="led-c"),
        rect(wx + 18 * u, led_y, 8, 4, t["border_hi"]),
        # Right progress ticks
        rect(wx + 37 * u, led_y, 12, 4, t["muted"]),
        rect(wx + 41 * u, led_y, 12, 4, t["secondary"]),
        rect(wx + 45 * u, led_y, 12, 4, t["accent"], cls="led-a"),
        rect(wx + 49 * u, led_y, 20, 4, t["border_hi"]),
    ]

    # Tiny screen reflection glint (top-right inside monitor)
    glint_rects = [
        rect(wx + 35 * u, wy + 8 * u, u, u, "#ffffff", opacity=0.14),
        rect(wx + 36 * u, wy + 9 * u, u, u, "#ffffff", opacity=0.10),
    ]

    # Ambient 1-pixel stars/ticks in upper workstation area (very restrained)
    ambient_ticks = [
        rect(wx + 46 * u, wy + 9 * u, 4, 4, t["border_hi"], cls="twinkle-a"),
        rect(wx + 56 * u, wy + 15 * u, 4, 4, t["border_hi"], cls="twinkle-b"),
        rect(wx + 51 * u, wy + 6 * u, 4, 4, t["accent"], cls="twinkle-a"),
    ]

    # Assemble SVG with clean stepped CSS animations
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" role="img" aria-label="Kean Salvahan — Data Analytics, QA and Automation">
  <style>
    .mono {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }}
    @keyframes blink {{
      0%, 49% {{ opacity: 1; }}
      50%, 100% {{ opacity: 0; }}
    }}
    @keyframes pulseDot {{
      0%, 60% {{ opacity: 1; }}
      61%, 100% {{ opacity: 0.25; }}
    }}
    @keyframes slot0 {{
      0%, 32.5% {{ opacity: 1; }}
      33.3%, 100% {{ opacity: 0; }}
    }}
    @keyframes slot1 {{
      0%, 32.5% {{ opacity: 0; }}
      33.3%, 65.8% {{ opacity: 1; }}
      66.6%, 100% {{ opacity: 0; }}
    }}
    @keyframes slot2 {{
      0%, 65.8% {{ opacity: 0; }}
      66.6%, 99.2% {{ opacity: 1; }}
      100% {{ opacity: 0; }}
    }}
    @keyframes out0 {{
      0%, 6% {{ opacity: 0; }}
      7%, 32.5% {{ opacity: 1; }}
      33.3%, 100% {{ opacity: 0; }}
    }}
    @keyframes out1 {{
      0%, 39% {{ opacity: 0; }}
      40%, 65.8% {{ opacity: 1; }}
      66.6%, 100% {{ opacity: 0; }}
    }}
    @keyframes out2 {{
      0%, 72% {{ opacity: 0; }}
      73%, 99.2% {{ opacity: 1; }}
      100% {{ opacity: 0; }}
    }}
    @keyframes steam0 {{
      0%, 33% {{ opacity: 0.75; }}
      34%, 100% {{ opacity: 0; }}
    }}
    @keyframes steam1 {{
      0%, 33% {{ opacity: 0; }}
      34%, 66% {{ opacity: 0.75; }}
      67%, 100% {{ opacity: 0; }}
    }}
    @keyframes steam2 {{
      0%, 66% {{ opacity: 0; }}
      67%, 100% {{ opacity: 0.75; }}
    }}
    @keyframes titleGlint {{
      0% {{ transform: translateX(0px); opacity: 0; }}
      4% {{ opacity: 0.14; }}
      22% {{ transform: translateX({title_w + 18}px); opacity: 0.14; }}
      24%, 100% {{ transform: translateX({title_w + 18}px); opacity: 0; }}
    }}
    @keyframes twinkleA {{
      0%, 45% {{ opacity: 0.8; }}
      46%, 100% {{ opacity: 0.15; }}
    }}
    @keyframes twinkleB {{
      0%, 55% {{ opacity: 0.15; }}
      56%, 100% {{ opacity: 0.8; }}
    }}
    .cursor {{ animation: blink 1s steps(1) infinite; }}
    .status-dot {{ animation: pulseDot 1.8s steps(1) infinite; }}
    .s0 {{ animation: slot0 10.8s steps(1) infinite; }}
    .s1 {{ animation: slot1 10.8s steps(1) infinite; }}
    .s2 {{ animation: slot2 10.8s steps(1) infinite; }}
    .o0 {{ animation: out0 10.8s steps(1) infinite; }}
    .o1 {{ animation: out1 10.8s steps(1) infinite; }}
    .o2 {{ animation: out2 10.8s steps(1) infinite; }}
    .st0 {{ animation: steam0 1.8s steps(1) infinite; }}
    .st1 {{ animation: steam1 1.8s steps(1) infinite; }}
    .st2 {{ animation: steam2 1.8s steps(1) infinite; }}
    .glint-bar {{ animation: titleGlint 6s steps(24) infinite; }}
    .led-a {{ animation: pulseDot 1.6s steps(1) infinite; }}
    .led-b {{ animation: twinkleB 2.4s steps(1) infinite; }}
    .led-c {{ animation: twinkleA 2.0s steps(1) infinite; }}
    .twinkle-a {{ animation: twinkleA 2.6s steps(1) infinite; }}
    .twinkle-b {{ animation: twinkleB 3.2s steps(1) infinite; }}
  </style>

  <!-- Terminal Window Frame -->
  <g id="frame">
{chr(10).join(frame_rects)}
  </g>

  <!-- Dot-Matrix Grid Texture -->
  <g id="dot-matrix">
{chr(10).join(dots)}
  </g>

  <!-- Titlebar Metadata & Status LED -->
  <text x="64" y="22" class="mono" font-size="11" fill="{t['secondary']}">kenji0011@github:~/profile</text>
  <rect x="720" y="13" width="10" height="10" fill="{t['accent_dim']}" class="status-dot" />
  <rect x="722" y="15" width="6" height="6" fill="{t['accent']}" class="status-dot" />
  <text x="738" y="22" class="mono" font-size="10" font-weight="700" letter-spacing="0.8" fill="{t['accent']}">OPEN TO OJT</text>

  <!-- Eyebrow -->
  <text x="30" y="55" class="mono" font-size="10" letter-spacing="1.4" fill="{t['muted']}">// INTELLIGENT SYSTEMS CS · LAGUNA, PH</text>

  <!-- Pixel-Bitmap Display Title: KEAN SALVAHAN -->
  <g id="title-shadow">
{chr(10).join(shadow_rects)}
  </g>
  <g id="title-main">
{chr(10).join(title_rects)}
  </g>
  <g class="glint-bar">
    <rect x="{title_x - 12}" y="{title_y}" width="12" height="{7 * title_px}" fill="{t['glint']}" />
  </g>

  <!-- Role Subtitle -->
  <text x="30" y="132" class="mono" font-size="11.5" font-weight="600" letter-spacing="0.9" fill="{t['secondary']}">DATA ANALYTICS  /  QA &amp; AUTOMATION  /  SYSTEMS</text>

  <!-- Pixel Dashed Rule -->
  <g id="rule">
{chr(10).join(sep_rects)}
  </g>

  <!-- Interactive Terminal Prompt Readout -->
  <g id="terminal-box">
{chr(10).join(term_box)}

    <!-- Command Slot 0: PostgreSQL Data Integrity -->
    <g class="s0">
      <text x="44" y="180" class="mono" font-size="11.5"><tspan fill="{t['accent']}">kenji@dev</tspan><tspan fill="{t['muted']}">:~$ </tspan><tspan fill="{t['fg']}">psql -c &quot;SELECT integrity FROM systems;&quot;</tspan><tspan fill="{t['accent']}" class="cursor"> &#9608;</tspan></text>
    </g>
    <g class="o0">
      <text x="44" y="201" class="mono" font-size="11"><tspan fill="{t['accent']}">[OK]</tspan><tspan fill="{t['secondary']}"> 0 anomalies detected · 14 tables audited (4ms)</tspan></text>
    </g>

    <!-- Command Slot 1: PyTest Automation Suite -->
    <g class="s1">
      <text x="44" y="180" class="mono" font-size="11.5"><tspan fill="{t['accent']}">kenji@dev</tspan><tspan fill="{t['muted']}">:~$ </tspan><tspan fill="{t['fg']}">pytest -q tests/workflow_suite.py</tspan><tspan fill="{t['accent']}" class="cursor"> &#9608;</tspan></text>
    </g>
    <g class="o1">
      <text x="44" y="201" class="mono" font-size="11"><tspan fill="{t['accent']}">[PASS]</tspan><tspan fill="{t['secondary']}"> 42 passed in 1.18s · regression suite green</tspan></text>
    </g>

    <!-- Command Slot 2: Tempo Rust + SQLite Core -->
    <g class="s2">
      <text x="44" y="180" class="mono" font-size="11.5"><tspan fill="{t['accent']}">kenji@dev</tspan><tspan fill="{t['muted']}">:~$ </tspan><tspan fill="{t['fg']}">cargo test --package tempo-core</tspan><tspan fill="{t['accent']}" class="cursor"> &#9608;</tspan></text>
    </g>
    <g class="o2">
      <text x="44" y="201" class="mono" font-size="11"><tspan fill="{t['accent']}">[PASS]</tspan><tspan fill="{t['secondary']}"> rusqlite + dart:ffi offline core verified</tspan></text>
    </g>
  </g>

  <!-- Right Pixel-Art Monochrome Workstation -->
  <g id="workstation">
{chr(10).join(ws_static_rects)}
{chr(10).join(glint_rects)}
{chr(10).join(rack_leds)}
{chr(10).join(ambient_ticks)}

    <!-- Synced Screen Frames -->
    <g class="s0">
{chr(10).join(scr_f0_rects)}
    </g>
    <g class="s1">
{chr(10).join(scr_f1_rects)}
    </g>
    <g class="s2">
{chr(10).join(scr_f2_rects)}
    </g>

    <!-- Animated Coffee Steam -->
    <g class="st0">
{chr(10).join(steam0_rects)}
    </g>
    <g class="st1">
{chr(10).join(steam1_rects)}
    </g>
    <g class="st2">
{chr(10).join(steam2_rects)}
    </g>
  </g>
</svg>
"""
    return svg


def build_divider_svg(theme_name: str) -> str:
    """Build an 850x44 animated pixel QA-scanner bot gliding across 12 test nodes."""
    t = THEMES[theme_name]
    w, h = 850, 44

    # Left terminal prompt badge: [>_]
    left_label, _ = render_pixel_text("[>_]", 10, 20, 2, t["muted"], FONT_3X5, gap_cols=1)

    # Right status badge: PASS (dimmed initially, flips to emerald when scan finishes)
    right_dim, _ = render_pixel_text("PASS", 794, 20, 2, t["border_hi"], FONT_3X5, gap_cols=1)
    right_lit, _ = render_pixel_text("PASS", 794, 20, 2, t["accent"], FONT_3X5, gap_cols=1)

    # Dashed pixel rail spanning x=66..782 at y=28
    rail_rects: List[str] = []
    for rx in range(66, 782, 8):
        rail_rects.append(rect(rx, 28, 4, 2, t["border"]))

    # 12 evenly spaced test/data nodes along the rail (x=96, 156, ..., 756)
    num_nodes = 12
    node_xs = [96 + i * 60 for i in range(num_nodes)]

    node_base_rects: List[str] = []
    node_lit_groups: List[str] = []
    node_keyframes: List[str] = []

    # Bot travels from x=64 to x=772 across t=0%..84% of an 8.4s cycle.
    bot_start_x = 64
    bot_end_x = 772
    travel_dist = bot_end_x - bot_start_x  # 708px

    for i, nx in enumerate(node_xs):
        # Static node housing (12x12 pixel block centered at nx, y=23..35)
        bx = nx - 6
        by = 23
        node_base_rects.extend(
            [
                rect(bx, by, 12, 12, t["panel"]),
                rect(bx, by, 12, 2, t["border_hi"]),
                rect(bx, by + 10, 12, 2, t["border_hi"]),
                rect(bx, by, 2, 12, t["border_hi"]),
                rect(bx + 10, by, 2, 12, t["border_hi"]),
                rect(bx + 4, by + 4, 4, 4, t["subtle"]),
            ]
        )

        # Compute exact percentage when bot center (bot_x + 10) crosses node center (nx)
        progress = (nx - (bot_start_x + 10)) / travel_dist
        hit_pct = max(1.0, min(83.0, progress * 84.0))
        node_keyframes.append(
            f"    @keyframes n{i} {{"
            f" 0%, {hit_pct - 0.5:.1f}% {{ opacity: 0; }}"
            f" {hit_pct:.1f}%, 95% {{ opacity: 1; }}"
            f" 96%, 100% {{ opacity: 0; }}"
            f" }}\n"
            f"    .n{i} {{ animation: n{i} 8.4s steps(1) infinite; }}"
        )

        # Lit emerald PASS core + top highlight pixel
        node_lit_groups.append(
            f'  <g class="n{i}">\n'
            f'    <rect x="{bx}" y="{by}" width="12" height="2" fill="{t["accent"]}" />\n'
            f'    <rect x="{bx}" y="{by + 10}" width="12" height="2" fill="{t["accent"]}" />\n'
            f'    <rect x="{bx}" y="{by}" width="2" height="12" fill="{t["accent"]}" />\n'
            f'    <rect x="{bx + 10}" y="{by}" width="2" height="12" fill="{t["accent"]}" />\n'
            f'    <rect x="{bx + 4}" y="{by + 4}" width="4" height="4" fill="{t["accent"]}" />\n'
            f"  </g>"
        )

    # Custom Monochrome Pixel QA-Scanner Bot (10x9 matrix @ 2px = 20x18px)
    # Drawn relative to origin (bot_start_x, 3) and translated horizontally
    bot_palette = {
        "A": t["accent"],     # antenna tip + scan emitter
        "F": t["fg"],         # bot chassis / eyes
        "B": t["border_hi"],  # frame shadow
        "V": t["canvas"],     # dark visor interior
        "M": t["muted"],      # thruster trim
    }
    bot_f0 = [
        "....AA....",
        "....BB....",
        ".FFFFFFFF.",
        "FFVVVVVVFF",
        "FFVFVVFVFF",
        "FFVVVVVVFF",
        ".FFFFFFFF.",
        "..MM..MM..",
        "....AA....",
    ]
    bot_f1 = [
        "....AA....",
        "....BB....",
        ".FFFFFFFF.",
        "FFVVVVVVFF",
        "FFVFVVFVFF",
        "FFVVVVVVFF",
        ".FFFFFFFF.",
        "...M..M...",
        "....AA....",
    ]
    bot0_rects = render_sprite(bot_f0, bot_start_x, 3, 2, bot_palette)
    bot1_rects = render_sprite(bot_f1, bot_start_x, 2, 2, bot_palette)

    # Downward scan beam pixel dots under bot center (bot_start_x + 8..12)
    beam_rects = [
        rect(bot_start_x + 8, 21, 4, 2, t["accent"], opacity=0.85),
        rect(bot_start_x + 8, 25, 4, 2, t["accent"], opacity=0.45),
    ]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" role="img" aria-label="Automated QA pixel scanner divider">
  <style>
    @keyframes botGlide {{
      0% {{ transform: translateX(0px); opacity: 1; }}
      84% {{ transform: translateX({travel_dist}px); opacity: 1; }}
      88% {{ transform: translateX({travel_dist}px); opacity: 0; }}
      97% {{ transform: translateX(0px); opacity: 0; }}
      100% {{ transform: translateX(0px); opacity: 1; }}
    }}
    @keyframes frameA {{
      0%, 49% {{ opacity: 1; }}
      50%, 100% {{ opacity: 0; }}
    }}
    @keyframes frameB {{
      0%, 49% {{ opacity: 0; }}
      50%, 100% {{ opacity: 1; }}
    }}
    @keyframes passLit {{
      0%, 82% {{ opacity: 0; }}
      83%, 95% {{ opacity: 1; }}
      96%, 100% {{ opacity: 0; }}
    }}
    .bot-track {{ animation: botGlide 8.4s steps(48) infinite; }}
    .bot-f0 {{ animation: frameA 0.45s steps(1) infinite; }}
    .bot-f1 {{ animation: frameB 0.45s steps(1) infinite; }}
    .pass-lit {{ animation: passLit 8.4s steps(1) infinite; }}
{chr(10).join(node_keyframes)}
  </style>

  <!-- Terminal Prompt Cap -->
  <g id="cap-left">
{chr(10).join(left_label)}
  </g>

  <!-- Pixel Rail -->
  <g id="rail">
{chr(10).join(rail_rects)}
  </g>

  <!-- Pending Test Nodes -->
  <g id="nodes-base">
{chr(10).join(node_base_rects)}
  </g>

  <!-- Scanned PASS Nodes -->
{chr(10).join(node_lit_groups)}

  <!-- Right PASS Indicator -->
  <g id="cap-right-dim">
{chr(10).join(right_dim)}
  </g>
  <g id="cap-right-lit" class="pass-lit">
{chr(10).join(right_lit)}
  </g>

  <!-- QA-Scanner Pixel Bot -->
  <g class="bot-track">
    <g class="bot-f0">
{chr(10).join(bot0_rects)}
    </g>
    <g class="bot-f1">
{chr(10).join(bot1_rects)}
    </g>
    <g id="scan-beam">
{chr(10).join(beam_rects)}
    </g>
  </g>
</svg>
"""
    return svg


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    for theme_name in ("dark", "light"):
        hero_path = ASSETS_DIR / f"hero-{theme_name}.svg"
        divider_path = ASSETS_DIR / f"divider-{theme_name}.svg"

        hero_path.write_text(build_hero_svg(theme_name), encoding="utf-8")
        divider_path.write_text(build_divider_svg(theme_name), encoding="utf-8")

        print(
            f"Generated {hero_path.name} ({hero_path.stat().st_size:,} B) "
            f"and {divider_path.name} ({divider_path.stat().st_size:,} B)"
        )


if __name__ == "__main__":
    main()
