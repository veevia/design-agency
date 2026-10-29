#!/usr/bin/env python3
"""
render_storyboard_svg.py — High-fidelity hand-drawn native SVG whiteboard 5-panel storyboard builder.

This script parses a 5-panel storyboard YAML schema and renders a vector SVG file in a dry-erase
whiteboard style: wobbly lines (via SVG displacement filters), stick-figure personas, a thought bubble,
system windows, a flywheel, a chain of linked records, a checklist and a metric badge. Every word drawn
comes from the spec; the icons (clock, laptop, phone, vehicle, wrench, calendar, stars) carry no text.

Body-line conventions (see ../templates/storyboard-input.template.yml):
    Thought: "..."              a thought bubble (beside the persona in P1)
    "  a · b · c" (indented)    one window per item
    S<n> STAGE description      a flywheel stage (P2 draws the wheel); "← note" marks the focus stage
    a ↔ b ↔ c                   a chain of linked record nodes
    "  · item" (indented)       a checklist item
    P5's first line             the headline metric; P5's other lines become ticked bullets
    anything else               handwritten text

Usage:
    python render_storyboard_svg.py <input.yml> <output.svg>
"""

from __future__ import annotations

import argparse
import math
import re
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
import yaml

# ── Color Palette ───────────────────────────────────────────────────────────
BG_COLOR = "#FAF7F2"       # Warm dry-erase whiteboard background
INK_DARK = "#1A1A1A"       # Standard black marker ink
INK_SOFT = "#4A4A4A"       # Soft grey secondary marker ink
WHITEBOARD_GRID = "#F3EDE4"# Subtle grid guidelines

ACCENTS = {
    "black":  INK_DARK,
    "blue":   "#1F5AA8",   # Primary structural diagram accent
    "green":  "#2E7D32",   # Value and happy state accent
    "red":    "#C62828",   # Pain and alert accent
    "orange": "#D97706",   # Attention / review accent
}

# Fonts used for organic handwriting appearance
FONT_HEADING = "Marker Felt, Chalkboard SE, Comic Sans MS, cursive, sans-serif"
FONT_BODY = "Bradley Hand, Chalkboard SE, Comic Sans MS, cursive, sans-serif"

@dataclass
class Box:
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def w(self) -> float: return self.x1 - self.x0
    @property
    def h(self) -> float: return self.y1 - self.y0
    @property
    def cx(self) -> float: return (self.x0 + self.x1) / 2
    @property
    def cy(self) -> float: return (self.y0 + self.y1) / 2


class SVGBuilder:
    def __init__(self, width: int = 1600, height: int = 1080):
        self.width = width
        self.height = height
        self.elements: list[str] = []
        self.defs: list[str] = []
        self._init_defs()

    def _init_defs(self):
        # 1. Sketch displacement filter for beautiful natural wobbly marker hand strokes
        self.defs.append("""
    <filter id="hand-drawn-sketch" x="-10%" y="-10%" width="120%" height="120%">
        <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="4" result="noise" />
        <feDisplacementMap in="SourceGraphic" in2="noise" scale="3.5" xChannelSelector="R" yChannelSelector="G" />
    </filter>
        """)
        # 2. Subtle drop shadow for sticker-like sticky notes and elements
        self.defs.append("""
    <filter id="sticker-shadow" x="-10%" y="-10%" width="130%" height="130%">
        <feDropShadow dx="2" dy="4" stdDeviation="3.5" flood-color="#554433" flood-opacity="0.12" />
    </filter>
        """)
        # 3. Arrow markers for flowing layout arrows between stages and flywheels
        for name, color in ACCENTS.items():
            self.defs.append(f"""
    <marker id="arrow-{name}" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="{color}" />
    </marker>
            """)

    def rect(self, x: float, y: float, w: float, h: float, fill: str = "none", stroke: str = "none",
             stroke_width: float = 1.0, rx: float = 0.0, filter_id: str | None = None,
             extra: str = "") -> None:
        filt = f' filter="url(#{filter_id})"' if filter_id else ""
        self.elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" ry="{rx:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"{filt} {extra}/>'
        )

    def circle(self, cx: float, cy: float, r: float, fill: str = "none", stroke: str = "none",
               stroke_width: float = 1.0, filter_id: str | None = None, extra: str = "") -> None:
        filt = f' filter="url(#{filter_id})"' if filter_id else ""
        self.elements.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{stroke_width:.1f}"{filt} {extra}/>'
        )

    def line(self, x1: float, y1: float, x2: float, y2: float, stroke: str, stroke_width: float = 1.0,
             dashed: bool = False, filter_id: str | None = None, extra: str = "") -> None:
        filt = f' filter="url(#{filter_id})"' if filter_id else ""
        dash = ' stroke-dasharray="6,8"' if dashed else ""
        self.elements.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
            f'stroke-width="{stroke_width:.1f}"{dash}{filt} {extra}/>'
        )

    def path(self, d: str, fill: str = "none", stroke: str = "none", stroke_width: float = 1.0,
             dashed: bool = False, filter_id: str | None = None, extra: str = "") -> None:
        filt = f' filter="url(#{filter_id})"' if filter_id else ""
        dash = ' stroke-dasharray="6,8"' if dashed else ""
        self.elements.append(
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"{dash}{filt} {extra}/>'
        )

    def text(self, x: float, y: float, content: str, font_size: float = 14.0, font_weight: str = "normal",
             font_style: str = "normal", color: str = INK_DARK, anchor: str = "start",
             use_heading: bool = False, extra: str = "") -> None:
        family = FONT_HEADING if use_heading else FONT_BODY
        escaped_content = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.elements.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{font_size:.1f}" '
            f'font-weight="{font_weight}" font-style="{font_style}" fill="{color}" text-anchor="{anchor}" {extra}>'
            f'{escaped_content}</text>'
        )

    def text_wrapped(self, x: float, y: float, lines: list[str], line_height: float, font_size: float = 14.0,
                     font_weight: str = "normal", font_style: str = "normal", color: str = INK_DARK,
                     anchor: str = "start", use_heading: bool = False) -> None:
        for i, line in enumerate(lines):
            self.text(x, y + i * line_height, line, font_size=font_size, font_weight=font_weight,
                      font_style=font_style, color=color, anchor=anchor, use_heading=use_heading)

    def draw_whiteboard_grid(self) -> None:
        # Subtle whiteboard math grid guidelines
        spacing = 40.0
        for gx in range(0, self.width, int(spacing)):
            self.line(gx, 0, gx, self.height, stroke=WHITEBOARD_GRID, stroke_width=0.8)
        for gy in range(0, self.height, int(spacing)):
            self.line(0, gy, self.width, gy, stroke=WHITEBOARD_GRID, stroke_width=0.8)

    def compile(self) -> str:
        defs_block = "\n".join(self.defs)
        elements_block = "\n".join(self.elements)
        return f"""<svg width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
{defs_block}
  </defs>
{elements_block}
</svg>"""


# ── Geometry layout ─────────────────────────────────────────────────────────

def calculate_layout() -> dict[str, Box]:
    margin_x = 14.0
    margin_y = 18.0
    title_h = 92.0
    panel_y0 = margin_y + title_h + 10.0
    panel_y1 = 1048.0
    col_w = (1600.0 - 2 * margin_x) / 5

    title_box = Box(margin_x, margin_y, 1600.0 - margin_x, margin_y + title_h)
    layout = {"title": title_box}
    for index in range(5):
        x0 = margin_x + index * col_w
        layout[f"P{index + 1}"] = Box(x0, panel_y0, x0 + col_w, panel_y1)

    return layout


# ── Body-line conventions ───────────────────────────────────────────────────

CHAR_EM = 0.5      # conservative average glyph width of the handwriting fonts, in em
BODY_SIZE = 16.0   # body text size, px
LEADING = 1.3      # line height as a multiple of the font size
GAP = 10.0         # space after each body item, px

THOUGHT = re.compile(r"^thought:\s*", re.IGNORECASE)
STAGE = re.compile(r"^S(\d+)\s+(\S+)\s*(.*)$")
CHAIN_LEAD = re.compile(r"^(.*[—–:])\s*(.+)$")
FOCUS_MARK = "←"
LINK_MARK = "↔"
ITEM_MARK = "·"
MARKERS = {color: name for name, color in ACCENTS.items()}


@dataclass
class Stage:
    tag: str
    name: str
    text: str
    focus: str


def wrap(text: str, width: float, font_size: float) -> list[str]:
    """Split text into lines that fit `width` px at `font_size`."""
    return textwrap.wrap(text, max(6, int(width / (font_size * CHAR_EM)))) or [""]


def body_lines(panel: dict) -> list[str]:
    return [str(line) for line in panel.get("body") or [] if str(line).strip()]


def items_of(text: str) -> list[str]:
    """`a · b · c.` -> ['a', 'b', 'c']."""
    return [item.strip(" .") for item in text.split(ITEM_MARK) if item.strip(" .")]


def thought_of(line: str) -> str | None:
    match = THOUGHT.match(line.strip())
    return (line.strip()[match.end():].strip('"“” ') or None) if match else None


def stage_of(line: str) -> Stage | None:
    match = STAGE.match(line.strip())
    if not match:
        return None
    text, _, focus = match.group(3).partition(FOCUS_MARK)
    return Stage(f"S{match.group(1)}", match.group(2), text.strip(), focus.strip())


def chain_of(line: str) -> tuple[str, list[str]]:
    """`Goal: one record — a ↔ b ↔ c.` -> ('Goal: one record', ['a', 'b', 'c'])."""
    first, *rest = [part.strip(" .") for part in line.strip().split(LINK_MARK)]
    lead = ""
    match = CHAIN_LEAD.match(first)
    if match:
        lead, first = match.group(1).rstrip("—–: "), match.group(2)
    return lead, [node for node in (first, *rest) if node]


def kind_of(line: str) -> str:
    stripped = line.strip()
    indented = line[:1].isspace()
    if thought_of(line) is not None:
        return "thought"
    if stage_of(line):
        return "stage"
    if LINK_MARK in stripped:
        return "chain"
    if indented and stripped.startswith(ITEM_MARK):
        return "check"
    if indented and len(items_of(stripped)) > 1:
        return "systems"
    return "text"


# ── Rendering Components ───────────────────────────────────────────────────

def draw_header_bar(svg: SVGBuilder, box: Box, title: str, subtitle: str) -> None:
    # Shrink long lines so the title and subtitle each stay on one line (capitals run ≈0.6 em wide).
    size = min(45.0, (box.w - 60.0) / (0.6 * max(len(title), 1)))
    svg.text(box.cx, box.y0 + 42, title.upper(), font_size=size, font_weight="bold", color=INK_DARK, anchor="middle", use_heading=True)
    if subtitle:
        sub_size = min(20.0, (box.w - 60.0) / (CHAR_EM * len(subtitle)))
        svg.text(box.cx, box.y0 + 73, subtitle, font_size=sub_size, font_weight="bold", color=INK_SOFT, anchor="middle")
    svg.line(box.x0, box.y1 + 3.0, box.x1, box.y1 + 3.0, stroke=INK_DARK, stroke_width=2.0, filter_id="hand-drawn-sketch")


def draw_panel_label(svg: SVGBuilder, box: Box, idx: int, title: str, kicker: str | None, accent_color: str) -> None:
    num_cx = box.x0 + 27.0
    num_cy = box.y0 + 28.0
    svg.circle(num_cx, num_cy, 16.0, fill="#FFFDF7", stroke=INK_DARK, stroke_width=1.8, filter_id="hand-drawn-sketch")
    svg.text(num_cx, num_cy + 5.0, str(idx), font_size=15.0, font_weight="bold", color=INK_DARK, anchor="middle", use_heading=True)

    title_size = 18.0 if len(title) <= 18 else 15.5
    svg.text(num_cx + 24.0, num_cy + 4.0, title.upper(), font_size=title_size, font_weight="bold", color=INK_DARK, anchor="start", use_heading=True)
    svg.line(num_cx + 24.0, num_cy + 10.0, min(box.x1 - 14.0, num_cx + 235.0), num_cy + 10.0, stroke=accent_color, stroke_width=1.8, filter_id="hand-drawn-sketch")
    if kicker:
        svg.text(num_cx + 24.0, num_cy + 27.0, kicker, font_size=11.5, font_weight="bold", color=accent_color, anchor="start")


def sketch_stick_figure(svg: SVGBuilder, cx: float, cy: float, mood: str = "neutral", color: str = INK_DARK, scale: float = 1.0) -> None:
    head_r = 18.0 * scale
    head_cy = cy - 25.0 * scale

    # 1. Head circle with sketch jitter
    svg.circle(cx, head_cy, head_r, fill="none", stroke=color, stroke_width=1.8, filter_id="hand-drawn-sketch")

    # 2. Facial features
    eye_offset_x = 5.0 * scale
    eye_offset_y = 3.0 * scale
    svg.circle(cx - eye_offset_x, head_cy - eye_offset_y, 2.0 * scale, fill=color, stroke="none")
    svg.circle(cx + eye_offset_x, head_cy - eye_offset_y, 2.0 * scale, fill=color, stroke="none")

    # Mouth wobbly curves
    mouth_y = head_cy + 4.0 * scale
    if mood == "smile":
        # Happy smile arc
        svg.path(f"M {cx-7*scale:.1f} {mouth_y:.1f} Q {cx:.1f} {mouth_y+8*scale:.1f} {cx+7*scale:.1f} {mouth_y:.1f}",
                 fill="none", stroke=color, stroke_width=1.5, filter_id="hand-drawn-sketch")
        # Thumbs-up uplift arm action
        svg.line(cx + 10.0*scale, cy, cx + 35.0*scale, cy - 25.0*scale, stroke=color, stroke_width=1.8, filter_id="hand-drawn-sketch")
        # Thumb path
        svg.circle(cx + 35.0*scale, cy - 25.0*scale, 4.0*scale, fill=color, stroke="none")
        # Radiant win indicator shine rays (sparkles)
        for a in range(0, 360, 45):
            rad = math.radians(a)
            r_start = head_r + 5.0
            r_end = head_r + 15.0
            x_st = cx + r_start * math.cos(rad)
            y_st = head_cy + r_start * math.sin(rad)
            x_ed = cx + r_end * math.cos(rad)
            y_ed = head_cy + r_end * math.sin(rad)
            svg.line(x_st, y_st, x_ed, y_ed, stroke=color, stroke_width=1.0, filter_id="hand-drawn-sketch")
    elif mood == "frown":
        # Distressed frown
        svg.path(f"M {cx-6*scale:.1f} {mouth_y+3*scale:.1f} Q {cx:.1f} {mouth_y-3*scale:.1f} {cx+6*scale:.1f} {mouth_y+3*scale:.1f}",
                 fill="none", stroke=color, stroke_width=1.5, filter_id="hand-drawn-sketch")
        # Sad floppy downward arms
        svg.line(cx, cy, cx - 18.0*scale, cy + 18.0*scale, stroke=color, stroke_width=1.8, filter_id="hand-drawn-sketch")
        svg.line(cx, cy, cx + 18.0*scale, cy + 18.0*scale, stroke=color, stroke_width=1.8, filter_id="hand-drawn-sketch")
    else:
        # Straight line neutral mouth
        svg.line(cx - 5*scale, mouth_y + 1, cx + 5*scale, mouth_y + 1, stroke=color, stroke_width=1.5, filter_id="hand-drawn-sketch")
        # Normal relaxed arms
        svg.line(cx - 20.0*scale, cy, cx, cy, stroke=color, stroke_width=1.8, filter_id="hand-drawn-sketch")
        svg.line(cx, cy, cx + 20.0*scale, cy, stroke=color, stroke_width=1.8, filter_id="hand-drawn-sketch")

    # 3. Torso body line
    torso_bottom = cy + 25.0 * scale
    svg.line(cx, head_cy + head_r, cx, torso_bottom, stroke=color, stroke_width=2.0)

    # 4. Legs
    svg.line(cx, torso_bottom, cx - 14.0 * scale, torso_bottom + 25.0 * scale, stroke=color, stroke_width=1.8, filter_id="hand-drawn-sketch")
    svg.line(cx, torso_bottom, cx + 14.0 * scale, torso_bottom + 25.0 * scale, stroke=color, stroke_width=1.8, filter_id="hand-drawn-sketch")


def draw_panel_border(svg: SVGBuilder, box: Box) -> None:
    svg.rect(box.x0, box.y0, box.w, box.h, fill="#FFFDF7", stroke=INK_DARK, stroke_width=1.6, rx=1.0, filter_id="hand-drawn-sketch")


def draw_persona_label(svg: SVGBuilder, cx: float, y: float, name: str, role: str, color: str) -> None:
    svg.text(cx, y, name, font_size=17.0, font_weight="bold", color=color, anchor="middle", use_heading=True)
    if role:
        svg.text(cx, y + 17.0, role, font_size=12.5, font_weight="bold", color=INK_SOFT, anchor="middle")


# ── Body text: one drawer per body-line convention ───────────────────────────

def draw_text(svg: SVGBuilder, x: float, y: float, width: float, text: str, size: float = BODY_SIZE,
              color: str = INK_DARK, weight: str = "normal", heading: bool = False, anchor: str = "start") -> float:
    """Write `text` wrapped to `width`, its first line's top at y; return the y below it."""
    lines = wrap(text, width, size)
    svg.text_wrapped(x, y + size, lines, size * LEADING, font_size=size, font_weight=weight, color=color,
                     anchor=anchor, use_heading=heading)
    return y + len(lines) * size * LEADING


def draw_flow(svg: SVGBuilder, x: float, y: float, width: float, lines: list[str], accent: str,
              ticked: bool = False, bottom: float | None = None) -> float:
    """Draw body lines top-down in reading order; spread them out towards `bottom` when given."""
    extra = 0.0
    if bottom is not None and len(lines) > 1:
        natural = draw_flow(SVGBuilder(), x, y, width, lines, accent, ticked) - y
        extra = max(0.0, min(40.0, (bottom - y - natural) / (len(lines) - 1)))
    stages = [stage for stage in map(stage_of, lines) if stage]
    tag_w = min(width * 0.45, max((len(f"{s.tag} {s.name}") for s in stages), default=0) * 13.0 * 0.6 + 12.0)
    for line in lines:
        kind, stripped = kind_of(line), line.strip()
        if kind == "thought":
            y = draw_thought(svg, x, y, width, thought_of(line) or "")
        elif kind == "stage":
            y = draw_stage_row(svg, x, y, width, stage_of(line), tag_w, accent)
        elif kind == "chain":
            y = draw_chain(svg, x, y, width, *chain_of(line))
        elif kind == "systems":
            y = draw_windows(svg, x, y, width, items_of(stripped))
        elif kind == "check":
            y = draw_check_item(svg, x + 10.0, y, width - 10.0, stripped.lstrip(ITEM_MARK).strip())
        elif ticked:
            y = draw_check_item(svg, x, y, width, stripped, checked=True)
        else:
            y = draw_text(svg, x, y, width, stripped)
        y += GAP + extra
    return y


def draw_thought(svg: SVGBuilder, x: float, y: float, w: float, text: str,
                 tail: tuple[float, float] | None = None) -> float:
    """A thought bubble; `tail` is the head its trailing bubbles point at."""
    size = 15.0
    lines = wrap(text, w - 28.0, size)
    h = 20.0 + len(lines) * size * LEADING
    svg.rect(x, y, w, h, fill="#FFFFFF", stroke=INK_DARK, stroke_width=1.4, rx=min(h / 2, 24.0), filter_id="hand-drawn-sketch")
    svg.text_wrapped(x + w / 2, y + 10.0 + size, lines, size * LEADING, font_size=size, font_weight="bold",
                     color=INK_DARK, anchor="middle")
    if tail:
        bx, by = x + w * 0.3, y + h
        for step, radius in ((0.3, 6.0), (0.65, 4.0)):
            svg.circle(bx + (tail[0] - bx) * step, by + (tail[1] - by) * step, radius, fill="#FFFFFF",
                       stroke=INK_DARK, stroke_width=1.1)
    return y + h


def draw_stage_row(svg: SVGBuilder, x: float, y: float, width: float, stage: Stage, tag_w: float, accent: str) -> float:
    color = ACCENTS["orange"] if stage.focus else accent
    size = 15.0
    tag = f"{stage.tag} {stage.name}"
    svg.text(x, y + size, tag, font_size=min(13.0, (tag_w - 8.0) / (0.6 * len(tag))), font_weight="bold",
             color=color, use_heading=True)
    end = draw_text(svg, x + tag_w, y, width - tag_w, stage.text, size=size)
    if stage.focus:
        end = draw_text(svg, x + tag_w, end, width - tag_w, f"{FOCUS_MARK} {stage.focus}", size=size, color=color, weight="bold")
    return end


def draw_floating_window_box(svg: SVGBuilder, x: float, y: float, w: float, h: float, title: str) -> None:
    # Shadow offset
    svg.rect(x + 3.0, y + 4.0, w, h, fill="#EFECE6", stroke="none", rx=5.0)
    # Clear browser pane
    svg.rect(x, y, w, h, fill="#FAF7F2", stroke=INK_DARK, stroke_width=1.0, rx=5.0, filter_id="hand-drawn-sketch")
    # Browser window main horizontal line bar
    svg.line(x, y + 14, x + w, y + 14, stroke=INK_DARK, stroke_width=0.8)
    # Window control spots
    svg.circle(x + 7.0, y + 7.5, 1.8, fill=INK_DARK)
    svg.circle(x + 13.0, y + 7.5, 1.8, fill=INK_DARK)
    # Window name centred in the pane
    size = min(12.0, (w - 8.0) / (CHAR_EM * max(len(title), 1)))
    svg.text(x + w / 2, y + 14.0 + (h - 14.0) / 2 + size * 0.35, title, font_size=size, font_weight="bold", color=INK_DARK, anchor="middle")


def draw_windows(svg: SVGBuilder, x: float, y: float, width: float, names: list[str]) -> float:
    cols = min(3, len(names))
    rows = math.ceil(len(names) / cols)
    gap, h = 8.0, 46.0
    w = (width - gap * (cols - 1)) / cols
    for index, name in enumerate(names):
        row, col = divmod(index, cols)
        draw_floating_window_box(svg, x + col * (w + gap), y + row * (h + gap), w, h, name)
    return y + rows * (h + gap) - gap


def draw_record_node(svg: SVGBuilder, cx: float, cy: float, w: float, h: float, label: str, stroke: str,
                     fill: str = "#F8FBFF") -> None:
    svg.rect(cx - w / 2, cy - h / 2, w, h, fill=fill, stroke=stroke, stroke_width=1.5, rx=h / 2, filter_id="hand-drawn-sketch")
    size = min(13.0, (w - 18.0) / (0.62 * max(len(label), 1)))
    svg.text(cx, cy + size * 0.36, label, font_size=size, font_weight="bold", color=stroke, anchor="middle", use_heading=True)


def draw_chain(svg: SVGBuilder, x: float, y: float, width: float, lead: str, nodes: list[str]) -> float:
    """Linked record nodes zig-zagging down a dashed frame titled by `lead`."""
    if not nodes:
        return y
    color = ACCENTS["blue"]
    top = y
    y += 8.0
    if lead:
        y = draw_text(svg, x + width / 2, y, width - 20.0, lead, size=15.0, color=color, weight="bold", anchor="middle") + 4.0
    node_w, node_h, step = min(150.0, width * 0.56), 38.0, 64.0
    left, right = x + 8.0 + node_w / 2, x + width - 8.0 - node_w / 2
    centres = [(left if index % 2 == 0 else right, y + node_h / 2 + index * step) for index in range(len(nodes))]
    marker = f"url(#arrow-{MARKERS[color]})"
    for (ax, ay), (bx, by) in zip(centres, centres[1:]):
        # Trim each link to the node outlines so both arrowheads stay visible.
        t = min((node_h / 2 + 5.0) / max(abs(by - ay), 1e-6), (node_w / 2 + 5.0) / max(abs(bx - ax), 1e-6))
        svg.line(ax + (bx - ax) * t, ay + (by - ay) * t, bx - (bx - ax) * t, by - (by - ay) * t, stroke=color,
                 stroke_width=1.8, extra=f'marker-start="{marker}" marker-end="{marker}"')
    for (cx, cy), name in zip(centres, nodes):
        draw_record_node(svg, cx, cy, node_w, node_h, name.upper(), color)
    bottom = centres[-1][1] + node_h / 2 + 12.0
    svg.rect(x, top, width, bottom - top, stroke=color, stroke_width=1.2, rx=14.0, filter_id="hand-drawn-sketch",
             extra='stroke-dasharray="6,8"')
    return bottom


def draw_check_box(svg: SVGBuilder, x: float, baseline: float, checked: bool = False) -> None:
    box_fill = "#E8F5E9" if checked else "none"
    box_stroke = ACCENTS["green"] if checked else INK_DARK
    svg.rect(x, baseline - 12.0, 14.0, 14.0, fill=box_fill, stroke=box_stroke, stroke_width=1.3, rx=1.0, filter_id="hand-drawn-sketch")
    if checked:
        svg.path(f"M {x+2.5:.1f} {baseline-5.0:.1f} L {x+6.0:.1f} {baseline-1.0:.1f} L {x+13.0:.1f} {baseline-11.0:.1f}",
                 fill="none", stroke=ACCENTS["green"], stroke_width=2.2, filter_id="hand-drawn-sketch")


def draw_check_item(svg: SVGBuilder, x: float, y: float, width: float, text: str, checked: bool = False) -> float:
    draw_check_box(svg, x, y + BODY_SIZE, checked)
    color = ACCENTS["green"] if checked else INK_DARK
    return draw_text(svg, x + 24.0, y, width - 24.0, text, color=color, weight="bold" if checked else "normal")


def draw_metric_badge(svg: SVGBuilder, x: float, y: float, w: float, text: str, color: str) -> float:
    size = 24.0
    rows = wrap(text, w - 30.0, size)
    h = 26.0 + len(rows) * size * 1.2
    svg.rect(x, y, w, h, fill="#EBF7EB", stroke=color, stroke_width=2.0, rx=12.0, filter_id="sticker-shadow")
    svg.rect(x - 4.0, y - 4.0, w + 8.0, h + 8.0, stroke=color, stroke_width=1.0, rx=14.0, filter_id="hand-drawn-sketch")
    svg.text_wrapped(x + w / 2, y + 13.0 + size, rows, size * 1.2, font_size=size, font_weight="bold", color=color,
                     anchor="middle", use_heading=True)
    return y + h


def draw_flywheel(svg: SVGBuilder, cx: float, cy: float, radius: float, stages: list[Stage], accent: str) -> None:
    """Stage nodes clockwise round a ring, arrows between them, a service vehicle at the hub."""
    count = len(stages)
    node_w, node_h = 90.0, 36.0
    angles = [math.radians(-90.0 + 360.0 * index / count) for index in range(count)]
    centres = [(cx + radius * math.cos(angle), cy + radius * math.sin(angle)) for angle in angles]

    def clear_of(index: int, step: float) -> float:
        """The ring angle where an arrow leaves (step > 0) or reaches (step < 0) node `index`."""
        node_x, node_y = centres[index]
        angle = angles[index]
        for _ in range(180):
            angle += step
            px, py = cx + radius * math.cos(angle), cy + radius * math.sin(angle)
            if abs(px - node_x) > node_w / 2 + 6.0 or abs(py - node_y) > node_h / 2 + 6.0:
                break
        return angle

    marker = f"url(#arrow-{MARKERS.get(accent, 'black')})"
    for index in range(count if count > 1 else 0):
        start = clear_of(index, math.radians(1.0))
        end = clear_of((index + 1) % count, -math.radians(1.0)) + (2 * math.pi if index + 1 == count else 0.0)
        if end - start < math.radians(4.0):
            continue
        sx, sy = cx + radius * math.cos(start), cy + radius * math.sin(start)
        ex, ey = cx + radius * math.cos(end), cy + radius * math.sin(end)
        svg.path(f"M {sx:.1f} {sy:.1f} A {radius:.1f} {radius:.1f} 0 0 1 {ex:.1f} {ey:.1f}", stroke=accent,
                 stroke_width=2.2, extra=f'marker-end="{marker}"', filter_id="hand-drawn-sketch")
    draw_van(svg, cx - 52.0, cy + 12.0, 0.75, accent)
    for (node_x, node_y), stage in zip(centres, stages):
        stroke = ACCENTS["orange"] if stage.focus else accent
        fill = "#FFF3E0" if stage.focus else "#FFFDF7"
        svg.rect(node_x - node_w / 2, node_y - node_h / 2, node_w, node_h, fill=fill, stroke=stroke,
                 stroke_width=1.8 if stage.focus else 1.4, rx=10.0, filter_id="hand-drawn-sketch")
        label = f"{stage.tag} {stage.name}"
        size = min(12.5, (node_w - 10.0) / (0.6 * len(label)))
        svg.text(node_x, node_y + size * 0.36, label, font_size=size, font_weight="bold", color=stroke, anchor="middle", use_heading=True)


# ── Icons (drawings only, no words) ──────────────────────────────────────────

def draw_clipboard(svg: SVGBuilder, x: float, y: float, w: float, h: float) -> None:
    # Hand-sketched backing board
    svg.rect(x, y, w, h, fill="#FAF0E6", stroke=INK_DARK, stroke_width=1.8, rx=10.0, filter_id="hand-drawn-sketch")
    # Paper sheet
    svg.rect(x + 10.0, y + 25.0, w - 20.0, h - 35.0, fill="#FFFDF0", stroke=INK_DARK, stroke_width=1.0, rx=4.0)
    # Spring clamp
    clip_w = w * 0.45
    svg.rect(x + (w - clip_w) / 2, y - 5.0, clip_w, 24.0, fill="#D0D0D0", stroke=INK_DARK, stroke_width=1.5, rx=5.0, filter_id="hand-drawn-sketch")
    svg.circle(x + w / 2, y + 4.0, 3.5, fill=INK_DARK)


def draw_clock(svg: SVGBuilder, cx: float, cy: float, r: float, color: str) -> None:
    svg.circle(cx, cy, r, fill="#FFFDF7", stroke=color, stroke_width=2.0, filter_id="hand-drawn-sketch")
    svg.line(cx, cy, cx, cy - r * 0.65, stroke=color, stroke_width=2.0)
    svg.line(cx, cy, cx + r * 0.5, cy + r * 0.2, stroke=color, stroke_width=2.0)
    svg.circle(cx, cy, 2.2, fill=color)
    for side in (-1, 1):  # ringing marks
        svg.path(f"M {cx + side * r * 1.25:.1f} {cy - r * 0.5:.1f} Q {cx + side * r * 1.5:.1f} {cy:.1f} {cx + side * r * 1.25:.1f} {cy + r * 0.5:.1f}",
                 stroke=color, stroke_width=1.5, filter_id="hand-drawn-sketch")


def draw_laptop(svg: SVGBuilder, x: float, y: float, w: float, h: float, accent: str) -> None:
    svg.rect(x, y, w, h, fill="#EEF6FF", stroke=INK_DARK, stroke_width=1.3, rx=3.0, filter_id="hand-drawn-sketch")
    svg.rect(x + 8.0, y + 8.0, w - 16.0, h - 16.0, fill="#FFFDF7", stroke=INK_SOFT, stroke_width=0.8, rx=2.0)
    svg.path(f"M {x-10:.1f} {y+h+3:.1f} L {x+w+10:.1f} {y+h+3:.1f} L {x+w-2:.1f} {y+h+16:.1f} L {x+2:.1f} {y+h+16:.1f} Z",
             fill="#E7E2DA", stroke=INK_DARK, stroke_width=1.2, filter_id="hand-drawn-sketch")
    # Inbox rows; the accent one is the request that gets buried
    for index, color in enumerate((INK_SOFT, INK_SOFT, accent, INK_SOFT)):
        row_y = y + 17.0 + index * 11.0
        svg.line(x + 16.0, row_y, x + w - 16.0 - (index % 2) * 14.0, row_y, stroke=color,
                 stroke_width=1.8 if color == accent else 1.0, filter_id="hand-drawn-sketch")


def draw_phone(svg: SVGBuilder, cx: float, cy: float, scale: float, color: str) -> None:
    w, h = 28.0 * scale, 48.0 * scale
    svg.rect(cx - w / 2, cy - h / 2, w, h, fill="#FFFDF7", stroke=INK_DARK, stroke_width=1.5, rx=6.0 * scale, filter_id="hand-drawn-sketch")
    svg.rect(cx - w / 2 + 4.0 * scale, cy - h / 2 + 7.0 * scale, w - 8.0 * scale, h - 17.0 * scale, fill="#EEF6FF", stroke=INK_SOFT, stroke_width=0.8, rx=2.0)
    svg.circle(cx, cy + h / 2 - 5.0 * scale, 2.0 * scale, fill=INK_DARK)
    for ring in (1, 2):
        r = w / 2 + 6.0 * ring * scale
        for side in (-1, 1):
            svg.path(f"M {cx + side * r:.1f} {cy - h * 0.25:.1f} Q {cx + side * (r + 5.0 * scale):.1f} {cy:.1f} {cx + side * r:.1f} {cy + h * 0.25:.1f}",
                     stroke=color, stroke_width=1.5, filter_id="hand-drawn-sketch")


def draw_wrench(svg: SVGBuilder, cx: float, cy: float, length: float, angle: float, color: str) -> None:
    """An open-ended wrench centred on (cx, cy), rotated `angle` degrees."""
    turn = f'transform="rotate({angle:.1f} {cx:.1f} {cy:.1f})"'
    half = length / 2
    svg.line(cx - half, cy, cx + half * 0.4, cy, stroke=color, stroke_width=length * 0.16, extra=f'stroke-linecap="round" {turn}')
    r = length * 0.2
    hx = cx + half * 0.62
    jaw = math.radians(45.0)
    svg.path(f"M {hx + r * math.cos(jaw):.1f} {cy - r * math.sin(jaw):.1f} A {r:.1f} {r:.1f} 0 1 0 {hx + r * math.cos(jaw):.1f} {cy + r * math.sin(jaw):.1f}",
             stroke=color, stroke_width=length * 0.13, extra=f'stroke-linecap="round" {turn}')


def draw_van(svg: SVGBuilder, x: float, y: float, scale: float, color: str) -> None:
    """A service vehicle facing right; (x, y) is the rear end of its floor."""
    s = scale
    svg.rect(x, y - 44 * s, 96 * s, 44 * s, fill="#FFFDF7", stroke=INK_DARK, stroke_width=1.5, rx=5.0, filter_id="hand-drawn-sketch")
    svg.path(f"M {x+96*s:.1f} {y-44*s:.1f} L {x+120*s:.1f} {y-44*s:.1f} L {x+138*s:.1f} {y-20*s:.1f} L {x+138*s:.1f} {y:.1f} L {x+96*s:.1f} {y:.1f} Z",
             fill="#EEF6FF", stroke=INK_DARK, stroke_width=1.5, filter_id="hand-drawn-sketch")
    svg.path(f"M {x+102*s:.1f} {y-38*s:.1f} L {x+118*s:.1f} {y-38*s:.1f} L {x+130*s:.1f} {y-22*s:.1f} L {x+102*s:.1f} {y-22*s:.1f} Z",
             fill="#BDE7FF", stroke=INK_DARK, stroke_width=0.9)
    svg.line(x + 6 * s, y - 10 * s, x + 90 * s, y - 10 * s, stroke=color, stroke_width=3.0 * s, filter_id="hand-drawn-sketch")
    draw_wrench(svg, x + 48 * s, y - 27 * s, 36 * s, -30.0, color)
    for wheel_x in (x + 26 * s, x + 114 * s):
        svg.circle(wheel_x, y + 2 * s, 10 * s, fill="#FFFDF7", stroke=INK_DARK, stroke_width=1.6, filter_id="hand-drawn-sketch")
        svg.circle(wheel_x, y + 2 * s, 3 * s, fill=INK_DARK)


def draw_calendar(svg: SVGBuilder, x: float, y: float, w: float, h: float, color: str) -> None:
    head_h = h * 0.24
    svg.rect(x, y, w, h, fill="#FFFDF7", stroke=INK_DARK, stroke_width=1.5, rx=4.0, filter_id="hand-drawn-sketch")
    svg.rect(x, y, w, head_h, fill=color, stroke=INK_DARK, stroke_width=1.2, rx=4.0)
    for ring_x in (x + w * 0.28, x + w * 0.72):
        svg.line(ring_x, y - 6.0, ring_x, y + 7.0, stroke=INK_DARK, stroke_width=2.4, extra='stroke-linecap="round"')
    cols, rows = 5, 3
    cell_w, cell_h = w / cols, (h - head_h) / rows
    for row in range(rows):
        for col in range(cols):
            svg.circle(x + (col + 0.5) * cell_w, y + head_h + (row + 0.5) * cell_h, 1.8, fill=INK_SOFT)
    # Predicted day ringed in red, actual day ticked in green
    ring_x, ring_y = x + 1.5 * cell_w, y + head_h + 1.5 * cell_h
    svg.circle(ring_x, ring_y, min(cell_w, cell_h) * 0.5, stroke=ACCENTS["red"], stroke_width=1.6, filter_id="hand-drawn-sketch")
    tick_x, tick_y = x + 3.5 * cell_w, y + head_h + 1.5 * cell_h
    svg.path(f"M {tick_x-7:.1f} {tick_y:.1f} L {tick_x-2:.1f} {tick_y+5:.1f} L {tick_x+8:.1f} {tick_y-7:.1f}",
             stroke=ACCENTS["green"], stroke_width=2.4, filter_id="hand-drawn-sketch")


def draw_star(svg: SVGBuilder, cx: float, cy: float, r: float, color: str, filled: bool) -> None:
    points = []
    for k in range(10):
        radius = r if k % 2 == 0 else r * 0.45
        angle = math.radians(-90.0 + 36.0 * k)
        points.append(f"{cx + radius * math.cos(angle):.1f} {cy + radius * math.sin(angle):.1f}")
    svg.path("M " + " L ".join(points) + " Z", fill=color if filled else "none", stroke=color, stroke_width=1.3,
             filter_id="hand-drawn-sketch")


# ── Panel 1 Renderer (BEFORE) ────────────────────────────────────────────────

def render_p1_before(svg: SVGBuilder, box: Box, panel: dict, accent: str, role: str) -> None:
    lines = body_lines(panel)
    thought = next((line for line in lines if kind_of(line) == "thought"), None)
    if thought is not None:
        lines.remove(thought)

    # The pain number: a ringing clock and the kicker
    clock_cx, clock_cy = box.x1 - 52.0, box.y0 + 102.0
    draw_clock(svg, clock_cx, clock_cy, 21.0, accent)
    kicker = str(panel.get("kicker") or "").strip("() ")
    if kicker:
        draw_text(svg, clock_cx, clock_cy + 28.0, 100.0, kicker, size=15.0, color=accent, weight="bold",
                  heading=True, anchor="middle")

    # The persona at a desk with a laptop, a ringing phone and the question that slows every request
    fig_cx, fig_cy = box.x0 + 60.0, box.y0 + 262.0
    if thought is not None:
        draw_thought(svg, box.x0 + 16.0, box.y0 + 76.0, box.w - 136.0, thought_of(thought) or "",
                     tail=(fig_cx + 4.0, fig_cy - 48.0))
    sketch_stick_figure(svg, fig_cx, fig_cy, mood="frown", color=INK_DARK)
    if panel.get("persona"):
        draw_persona_label(svg, fig_cx, fig_cy + 74.0, str(panel["persona"]), role, accent)
    desk_y = fig_cy + 30.0
    svg.line(box.x0 + 100.0, desk_y, box.x1 - 14.0, desk_y, stroke=INK_DARK, stroke_width=2.2, filter_id="hand-drawn-sketch")
    for leg_x in (box.x0 + 112.0, box.x1 - 26.0):
        svg.line(leg_x, desk_y, leg_x, desk_y + 44.0, stroke=INK_DARK, stroke_width=1.8, filter_id="hand-drawn-sketch")
    draw_laptop(svg, box.x0 + 112.0, desk_y - 82.0, 104.0, 66.0, accent)
    draw_phone(svg, box.x1 - 42.0, desk_y - 27.0, 0.9, accent)

    # The facts, on a clipboard
    clip_y = fig_cy + 112.0
    draw_clipboard(svg, box.x0 + 14.0, clip_y, box.w - 28.0, box.y1 - 14.0 - clip_y)
    draw_flow(svg, box.x0 + 34.0, clip_y + 40.0, box.w - 68.0, lines, accent, bottom=box.y1 - 40.0)


# ── Panel 2 Renderer (THE MECHANISM: A FLYWHEEL) ─────────────────────────────

def render_p2_flywheel(svg: SVGBuilder, box: Box, panel: dict, accent: str) -> None:
    lines = body_lines(panel)
    stages = [stage for stage in map(stage_of, lines) if stage]
    top = box.y0 + 72.0
    if stages:
        radius = min(116.0, box.w / 2 - 50.0)
        draw_flywheel(svg, box.cx, top + radius + 30.0, radius, stages, accent)
        top += 2 * radius + 82.0
    y = draw_flow(svg, box.x0 + 18.0, top, box.w - 36.0, [line for line in lines if stage_of(line)], accent)

    # Every other line is the caption, written large at the foot of the panel
    size = 20.0
    rows = [row for line in lines if not stage_of(line) for row in wrap(line.strip(), box.w - 36.0, size)]
    if rows:
        y = max(y, box.y1 - 24.0 - len(rows) * size * LEADING)
        svg.text_wrapped(box.cx, y + size, rows, size * LEADING, font_size=size, font_weight="bold", color=accent,
                         anchor="middle", use_heading=True)


# ── Panel 3 Renderer (WORKED EXAMPLE) ────────────────────────────────────────

def render_p3_example(svg: SVGBuilder, box: Box, panel: dict, accent: str) -> None:
    draw_flow(svg, box.x0 + 18.0, box.y0 + 78.0, box.w - 36.0, body_lines(panel), accent, bottom=box.y1 - 24.0)


# ── Panel 4 Renderer (THE SECRET SAUCE: THE LOOP CLOSES) ─────────────────────

def render_p4_sauce(svg: SVGBuilder, box: Box, panel: dict, accent: str) -> None:
    cx, cy, r = box.cx, box.y0 + 196.0, 96.0
    marker = f"url(#arrow-{MARKERS.get(accent, 'black')})"
    for start, end in ((190.0, 350.0), (10.0, 170.0)):
        a0, a1 = math.radians(start), math.radians(end)
        svg.path(f"M {cx + r * math.cos(a0):.1f} {cy + r * math.sin(a0):.1f} A {r:.1f} {r:.1f} 0 0 1 {cx + r * math.cos(a1):.1f} {cy + r * math.sin(a1):.1f}",
                 stroke=accent, stroke_width=3.0, extra=f'marker-end="{marker}"', filter_id="hand-drawn-sketch")
    draw_calendar(svg, cx - 46.0, cy - 54.0, 92.0, 72.0, accent)
    for index in range(5):
        draw_star(svg, cx - 44.0 + index * 22.0, cy + 46.0, 9.0, ACCENTS["orange"], filled=index < 4)
    draw_flow(svg, box.x0 + 18.0, cy + r + 30.0, box.w - 36.0, body_lines(panel), accent, bottom=box.y1 - 24.0)


# ── Panel 5 Renderer (VALUE) ─────────────────────────────────────────────────

def render_p5_value(svg: SVGBuilder, box: Box, panel: dict, accent: str, role: str) -> None:
    lines = body_lines(panel)
    y = box.y0 + 76.0
    if lines:
        y = draw_metric_badge(svg, box.x0 + 16.0, y, box.w - 32.0, lines[0].strip(), accent)
    y = draw_flow(svg, box.x0 + 18.0, y + 22.0, box.w - 36.0, lines[1:], accent, ticked=True)

    # The persona again, now happy, beside the vehicle leaving with the right resources on board;
    # centred in the space left below the bullets (the group spans fig_cy - 62 to fig_cy + 105)
    fig_cx = box.x0 + 72.0
    fig_cy = min(box.y1 - 130.0, (y + box.y1 - 16.0) / 2 - 21.5)
    sketch_stick_figure(svg, fig_cx, fig_cy, mood="smile", color=accent, scale=1.1)
    if panel.get("persona"):
        draw_persona_label(svg, fig_cx, fig_cy + 84.0, str(panel["persona"]), role, accent)
    draw_van(svg, box.x0 + 150.0, fig_cy + 40.0, 0.95, accent)
    for index in range(3):
        lane_y = fig_cy + 8.0 + index * 12.0
        svg.line(box.x0 + 124.0, lane_y, box.x0 + 144.0, lane_y, stroke=INK_SOFT, stroke_width=1.4, filter_id="hand-drawn-sketch")


# ── Core Orchestrator ────────────────────────────────────────────────────────

def lint_spec(spec: dict) -> list[str]:
    errors = []
    if "title" not in spec or not spec["title"]:
        errors.append("Required field 'title' is missing or empty.")
    panels = spec.get("panels", [])
    if len(panels) != 5:
        errors.append(f"Exactly 5 panels are required. Spec has {len(panels)} panels.")
    for idx, panel in enumerate(panels):
        p_num = idx + 1
        p_id = panel.get("id", f"P{p_num}")
        if "title" not in panel:
            errors.append(f"Panel {p_id} (index {idx}) is missing a 'title'.")
    return errors


def render_storyboard_to_svg(spec: dict) -> str:
    svg = SVGBuilder(1600, 1080)

    # Render background paper base
    svg.rect(0, 0, 1600, 1080, fill=BG_COLOR, stroke="none")
    svg.draw_whiteboard_grid()

    L = calculate_layout()

    # Draw Title Bar
    title = spec.get("title", "Storyboard title")
    subtitle = spec.get("subtitle", "Storyboard subtitle")
    draw_header_bar(svg, L["title"], title, subtitle)

    div_stroke = "#B2A79E"
    for divider_index in range(1, 5):
        boundary_x = L[f"P{divider_index}"].x1
        svg.line(boundary_x, L["P1"].y0, boundary_x, L["P1"].y1, stroke=div_stroke, stroke_width=1.0, dashed=True)

    panels = spec.get("panels", [])
    persona_role = str(spec.get("persona_role") or "")

    # Panel Render Loop mapping each index block
    for i, panel in enumerate(panels):
        p_num = i + 1
        p_key = f"P{p_num}"
        box = L[p_key]

        # 1. Base container card
        draw_panel_border(svg, box)

        # 2. Panel Label Header
        accent = ACCENTS.get(panel.get("accent", "black"), INK_DARK)
        draw_panel_label(svg, box, p_num, panel.get("title", ""), panel.get("kicker", ""), accent)

        # 3. Specialized Custom Illustrator
        if p_num == 1:
            render_p1_before(svg, box, panel, accent, persona_role)
        elif p_num == 2:
            render_p2_flywheel(svg, box, panel, accent)
        elif p_num == 3:
            render_p3_example(svg, box, panel, accent)
        elif p_num == 4:
            render_p4_sauce(svg, box, panel, accent)
        elif p_num == 5:
            render_p5_value(svg, box, panel, accent, persona_role)
        else:
            svg.text(box.cx, box.cy, "Unknown panel slot", font_size=15, color=ACCENTS["red"], anchor="middle")

    return svg.compile()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a five-panel whiteboard storyboard YAML into a high-fidelity SVG.")
    parser.add_argument("input", help="Path to input YAML file.")
    parser.add_argument("output", help="Path to output SVG file.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        sys.stderr.write(f"Error: Input file {input_path} does not exist.\n")
        sys.exit(1)

    try:
        with input_path.open() as f:
            spec = yaml.safe_load(f) or {}
    except Exception as e:
        sys.stderr.write(f"Error parsing YAML: {e}\n")
        sys.exit(1)

    errors = lint_spec(spec)
    if errors:
        sys.stderr.write("Storyboard Lint Errors:\n")
        for err in errors:
            sys.stderr.write(f" - {err}\n")
        sys.exit(2)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        svg_content = render_storyboard_to_svg(spec)
        output_path.write_text(svg_content)
        print(f"Successfully rendered hand-drawn whiteboard storyboard to: {output_path}")
    except Exception as e:
        sys.stderr.write(f"Error generating SVG: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
