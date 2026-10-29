#!/usr/bin/env python3
"""
render_storyboard.py — Whiteboard 5-panel storyboard renderer.

Usage:
    python render_storyboard.py <input.yml> <output.png>

YAML schema (one of `type` per panel):

    type: scene      -> persona stick figure + body text
    type: flywheel   -> circular n-stage diagram with centre node
    type: stages     -> stacked rows of "<tag> | <verb> | <action>"
    type: value      -> metric badge + bullet list + happy persona

See ../templates/storyboard-input.template.yml for a worked example.
"""

from __future__ import annotations

import argparse
import math
import os
import re
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

# Sandbox-friendly matplotlib cache.
os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.environ.get("TMPDIR", "/tmp"), "mplcache"),
)
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
import yaml  # noqa: E402  (PyYAML)


# ── Style ───────────────────────────────────────────────────────────────────

CANVAS_W_IN = 16.0
CANVAS_H_IN = 10.8
DPI = 120

BG = "#FAF7F2"
INK = "#1A1A1A"
INK_SOFT = "#3A3A3A"

ACCENT = {
    "black":  INK,
    "blue":   "#1F5AA8",
    "green":  "#2E7D32",
    "red":    "#C62828",
    "orange": "#D97706",
}

TITLE_FONT = "Noteworthy"
BODY_FONT = "Bradley Hand"
ALT_FONT = "Marker Felt"

# Fallback chain so missing glyphs (arrows, math symbols) render via DejaVu Sans.
plt.rcParams["font.family"] = [BODY_FONT, "DejaVu Sans"]
plt.rcParams["path.sketch"] = (0.6, 130, 1)
plt.rcParams["lines.solid_capstyle"] = "round"
plt.rcParams["lines.solid_joinstyle"] = "round"


# ── Geometry ────────────────────────────────────────────────────────────────

@dataclass
class Box:
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def w(self): return self.x1 - self.x0
    @property
    def h(self): return self.y1 - self.y0
    @property
    def cx(self): return (self.x0 + self.x1) / 2
    @property
    def cy(self): return (self.y0 + self.y1) / 2


def layout(canvas_w=100.0, canvas_h=100.0):
    margin = 1.8
    title_h = 7.5
    inner_x0, inner_x1 = margin, canvas_w - margin
    inner_y0, inner_y1 = margin, canvas_h - margin

    title = Box(inner_x0, canvas_h - margin - title_h, inner_x1, canvas_h - margin)

    body_y0 = inner_y0
    body_y1 = title.y0 - 0.5
    row_h = (body_y1 - body_y0) / 2

    top_y0 = body_y1 - row_h
    top_y1 = body_y1
    top_w = (inner_x1 - inner_x0) / 3
    p1 = Box(inner_x0,             top_y0, inner_x0 + top_w,     top_y1)
    p2 = Box(inner_x0 + top_w,     top_y0, inner_x0 + 2 * top_w, top_y1)
    p3 = Box(inner_x0 + 2 * top_w, top_y0, inner_x1,             top_y1)

    bot_y0 = body_y0
    bot_y1 = top_y0
    p4_w = (inner_x1 - inner_x0) * 0.55
    p4 = Box(inner_x0, bot_y0, inner_x0 + p4_w, bot_y1)
    p5 = Box(inner_x0 + p4_w, bot_y0, inner_x1, bot_y1)

    return {"title": title, "P1": p1, "P2": p2, "P3": p3, "P4": p4, "P5": p5}


def dashed(ax, x0, y0, x1, y1, color=INK, alpha=0.55):
    ax.add_line(Line2D([x0, x1], [y0, y1], color=color, linewidth=1.0,
                       linestyle=(0, (4, 4)), alpha=alpha, zorder=2))


def split_items(text):
    """`a · b · c.` -> ['a', 'b', 'c']."""
    return [item.strip(" .") for item in text.split("·") if item.strip(" .")]


def persona_label(persona, persona_role):
    return f"{persona}\n({persona_role})" if persona_role else persona


# ── Panel label (numbered title + parenthetical) ─────────────────────────────

def panel_label(ax, box, n, title, kicker, accent=INK):
    pad = 0.7
    cy = box.y1 - pad - 0.9
    circ_r = 0.75
    cx = box.x0 + pad + circ_r
    ax.add_patch(plt.Circle((cx, cy), circ_r, fill=False,
                            edgecolor=INK, linewidth=1.4, zorder=3))
    ax.text(cx, cy, str(n), fontfamily=BODY_FONT, fontsize=13,
            ha="center", va="center", color=INK, zorder=4)

    tx = cx + circ_r + 0.6
    ax.text(tx, cy, title, fontfamily=ALT_FONT, fontsize=18,
            ha="left", va="center", color=accent, weight="bold", zorder=4)

    if kicker:
        ax.text(tx, cy - 1.4, kicker, fontfamily=BODY_FONT, fontsize=11,
                ha="left", va="center", color=INK_SOFT,
                style="italic", zorder=4)


# ── Stick figure ────────────────────────────────────────────────────────────

def stick_figure(ax, cx, cy, mood="neutral", color=INK, scale=1.0):
    head_r = 0.55 * scale
    head_cy = cy + 1.6 * scale
    ax.add_patch(plt.Circle((cx, head_cy), head_r, fill=False,
                            edgecolor=color, linewidth=1.3, zorder=3))
    # eyes
    ax.add_patch(plt.Circle((cx - 0.16, head_cy + 0.1), 0.045,
                            color=color, zorder=4))
    ax.add_patch(plt.Circle((cx + 0.16, head_cy + 0.1), 0.045,
                            color=color, zorder=4))
    # mouth
    if mood == "smile":
        theta = (200, 340)
    elif mood == "frown":
        theta = (20, 160)
    else:
        theta = None
    if theta:
        ax.add_patch(plt.matplotlib.patches.Arc(
            (cx, head_cy - 0.15), 0.45, 0.36,
            theta1=theta[0], theta2=theta[1],
            color=color, linewidth=1.1, zorder=4))
    # body
    body_top = head_cy - head_r
    body_bot = cy - 0.5 * scale
    ax.add_line(Line2D([cx, cx], [body_top, body_bot],
                       color=color, linewidth=1.3))
    # arms
    arm_y = body_top - 0.45 * scale
    ax.add_line(Line2D([cx - 0.8 * scale, cx + 0.8 * scale],
                       [arm_y, arm_y], color=color, linewidth=1.3))
    # legs
    ax.add_line(Line2D([cx, cx - 0.5 * scale],
                       [body_bot, body_bot - 1.1 * scale],
                       color=color, linewidth=1.3))
    ax.add_line(Line2D([cx, cx + 0.5 * scale],
                       [body_bot, body_bot - 1.1 * scale],
                       color=color, linewidth=1.3))
    if mood == "smile":
        # thumbs-up: replace right arm with bent arm + small fist circle
        ax.add_line(Line2D([cx + 0.55 * scale, cx + 0.55 * scale],
                           [arm_y, arm_y + 0.75 * scale],
                           color=color, linewidth=1.3))
        ax.add_patch(plt.Circle((cx + 0.55 * scale, arm_y + 0.95 * scale),
                                0.11, fill=False, edgecolor=color,
                                linewidth=1.2))


# ── Panel renderers ─────────────────────────────────────────────────────────

def render_scene(ax, box, body, accent_color=INK, persona=None,
                 persona_role=None, mood="frown"):
    """Scene panel: body lines on a clipboard beside the persona at a desk.

    A `Thought: ...` line becomes the thought cloud and an indented `a · b · c` line becomes up to
    six floating system windows (see ../templates/storyboard-input.template.yml).
    """
    rx = lambda f: box.x0 + f * box.w
    ry = lambda f: box.y0 + f * box.h

    thought, systems, lines = None, [], []
    for line in body or []:
        text = str(line)
        stripped = text.strip()
        said = stripped[len("thought:"):].strip('"“” ') if stripped.lower().startswith("thought:") else ""
        if thought is None and said:
            thought = said
        elif not systems and text[:1].isspace() and len(split_items(stripped)) > 1:
            systems = split_items(stripped)
        else:
            lines.append(text)

    # ── 1. Left Column: Clipboard Intake Sheet (the manual work) ──
    cb_x0, cb_x1 = rx(0.04), rx(0.45)
    cb_y0, cb_y1 = ry(0.05), ry(0.88)
    cb_w, cb_h = cb_x1 - cb_x0, cb_y1 - cb_y0

    # Draw wooden backing clipboard
    ax.add_patch(FancyBboxPatch(
        (cb_x0, cb_y0), cb_w, cb_h,
        boxstyle="round,pad=0.15,rounding_size=0.4",
        fill=True, facecolor="#F5EFE6", edgecolor=INK, linewidth=1.4, zorder=2.5))

    # Internal cream paper sheet
    ax.add_patch(FancyBboxPatch(
        (cb_x0 + 0.4, cb_y0 + 0.4), cb_w - 0.8, cb_h - 1.2,
        boxstyle="round,pad=0.1,rounding_size=0.3",
        fill=True, facecolor="#FFFDEF", edgecolor=INK, linewidth=0.9, zorder=2.8))

    # Metallic Clip at top
    clip_cx = (cb_x0 + cb_x1) / 2
    clip_cy = cb_y1 - 0.2
    ax.add_patch(FancyBboxPatch(
        (clip_cx - 1.6, clip_cy - 0.5), 3.2, 0.7,
        boxstyle="round,pad=0.04,rounding_size=0.1",
        fill=True, facecolor="#D8D8D8", edgecolor=INK, linewidth=1.2, zorder=3.5))
    ax.add_patch(plt.Circle((clip_cx, clip_cy - 0.15), 0.14, color=INK, zorder=4))

    # Plot the YAML body lines inside the clipboard sheet
    start_y = cb_y1 - 1.7
    line_h = max(1.1, (start_y - cb_y0 - 0.8) / max(len(lines), 1))
    for i, line in enumerate(lines):
        by = start_y - i * line_h
        # Skip empty lines
        if not line.strip():
            continue
        # Indent sub-bullets
        is_sub = line.startswith("  ")
        tx = cb_x0 + 1.8 if is_sub else cb_x0 + 0.9
        font_sz = 9.5 if is_sub else 10.5
        font_wt = "normal" if is_sub else "bold"
        color = INK_SOFT if is_sub else INK
        prefix = "• " if is_sub else "- "
        clean_text = line.strip().lstrip("·").strip()

        ax.text(tx, by, prefix + clean_text, fontfamily=BODY_FONT, fontsize=font_sz,
                ha="left", va="center", color=color, weight=font_wt, zorder=4)

    # ── 2. Right Column/Area: Sitting persona (Frustrated / Manual) ──
    # Desk at bottom right
    desk_y = ry(0.20)
    desk_x0 = rx(0.49)
    desk_x1 = rx(0.80)

    # Draw desk table top
    ax.add_line(Line2D([desk_x0, desk_x1], [desk_y, desk_y], color=INK, linewidth=1.5, zorder=3))
    # Desk legs
    ax.add_line(Line2D([desk_x0 + 1.0, desk_x0 + 1.0], [desk_y, ry(0.04)], color=INK, linewidth=1.3, zorder=3))
    ax.add_line(Line2D([desk_x1 - 1.0, desk_x1 - 1.0], [desk_y, ry(0.04)], color=INK, linewidth=1.3, zorder=3))

    # Laptop
    lap_cx = rx(0.70)
    ax.add_line(Line2D([lap_cx - 1.0, lap_cx + 1.0], [desk_y, desk_y], color=INK, linewidth=2.0, zorder=4))  # base
    ax.add_line(Line2D([lap_cx + 0.4, lap_cx + 1.4], [desk_y, desk_y + 1.4], color=INK, linewidth=2.0, zorder=4))  # screen

    # Chair
    chair_x = rx(0.56)
    chair_y = ry(0.14)
    # Chair seat
    ax.add_line(Line2D([chair_x - 0.9, chair_x + 0.9], [chair_y, chair_y], color=INK, linewidth=1.3, zorder=3))
    # Chair backrest
    ax.add_line(Line2D([chair_x - 0.9, chair_x - 0.9], [chair_y, chair_y + 2.0], color=INK, linewidth=1.3, zorder=3))
    # Chair leg
    ax.add_line(Line2D([chair_x, chair_x], [chair_y, ry(0.04)], color=INK, linewidth=1.3, zorder=3))

    # Sitting persona (distressed stick figure)
    sf_cx = chair_x + 0.5
    head_cy = chair_y + 2.6
    scale = 0.72
    # Head circle
    ax.add_patch(plt.Circle((sf_cx, head_cy), 0.50 * scale, fill=False, edgecolor=INK, linewidth=1.3, zorder=3.5))
    # Slanted, stressed eyes
    ax.add_line(Line2D([sf_cx - 0.14, sf_cx - 0.04], [head_cy + 0.1, head_cy + 0.05], color=INK, linewidth=1.2, zorder=4))
    ax.add_line(Line2D([sf_cx + 0.04, sf_cx + 0.14], [head_cy + 0.05, head_cy + 0.1], color=INK, linewidth=1.2, zorder=4))
    # Mouth: a frown before, a smile after
    mouth = (200, 340) if mood == "smile" else (20, 160)
    ax.add_patch(plt.matplotlib.patches.Arc(
        (sf_cx, head_cy - 0.18), 0.36, 0.25,
        theta1=mouth[0], theta2=mouth[1], color=INK, linewidth=1.1, zorder=4))

    # Torso (slouching/slanted forward structure)
    ax.add_line(Line2D([sf_cx, sf_cx + 0.15], [head_cy - 0.52 * scale, chair_y], color=INK, linewidth=1.4, zorder=3))
    # Typing Arms reaching laptop
    ax.add_line(Line2D([sf_cx + 0.10, lap_cx], [head_cy - 0.8 * scale, desk_y + 0.15], color=INK, linewidth=1.4, zorder=3))
    # Sitting legs
    ax.add_line(Line2D([sf_cx + 0.15, sf_cx + 0.9], [chair_y, chair_y], color=INK, linewidth=1.4, zorder=3))
    ax.add_line(Line2D([sf_cx + 0.9, sf_cx + 0.9], [chair_y, ry(0.04)], color=INK, linewidth=1.4, zorder=3))

    # Label persona text
    if persona:
        ax.text(sf_cx - 1.4, head_cy + 0.3, persona_label(persona, persona_role), fontfamily=BODY_FONT,
                fontsize=10, ha="right", va="center", color=accent_color, weight="bold")

    # ── 3. Thought Cloud above the persona ──
    if thought:
        tb_cx = rx(0.66)
        tb_cy = ry(0.77)
        # Bubbles pointing from head to cloud
        ax.add_patch(plt.Circle((sf_cx + 0.5, head_cy + 0.8), 0.20, fill=False, edgecolor=INK, linewidth=1.0, zorder=3))
        ax.add_patch(plt.Circle((sf_cx + 1.0, head_cy + 1.5), 0.28, fill=False, edgecolor=INK, linewidth=1.0, zorder=3))

        # Puffy background cloud circles (color-filled, no outlines overlapping inside)
        cloud_pts = [
            (tb_cx, tb_cy),
            (tb_cx - 2.2, tb_cy), (tb_cx + 2.2, tb_cy),
            (tb_cx, tb_cy + 1.4), (tb_cx, tb_cy - 1.4),
            (tb_cx - 1.6, tb_cy + 1.0), (tb_cx + 1.6, tb_cy + 1.0),
            (tb_cx - 1.6, tb_cy - 1.0), (tb_cx + 1.6, tb_cy - 1.0)
        ]
        # First render all solid back fills to completely block background
        for cp_x, cp_y in cloud_pts:
            ax.add_patch(plt.Circle((cp_x, cp_y), 1.6, fill=True, color=BG, zorder=3))
        # Then render outer outlines
        for cp_x, cp_y in cloud_pts:
            ax.add_patch(plt.Circle((cp_x, cp_y), 1.6, fill=False, edgecolor=INK, linewidth=0.8, zorder=3))
        ax.add_patch(plt.Circle((tb_cx, tb_cy), 2.4, fill=True, color=BG, zorder=3.2))

        # Cloud text: one sentence per line
        text_bubble = [part for sentence in re.findall(r"[^?!.]+[?!.]*", thought)
                       for part in textwrap.wrap(sentence.strip(), 22)]
        top = tb_cy + (len(text_bubble) - 1) * 0.375
        for idx, ln in enumerate(text_bubble):
            ax.text(tb_cx, top - idx * 0.75, ln, fontfamily=BODY_FONT, fontsize=9.5,
                    ha="center", va="center", color=INK_SOFT, weight="bold", zorder=4)

    # ── 4. Floating Orbiting Browsers (The Overhead Churn) ──
    slots = [
        (rx(0.48), ry(0.44)),
        (rx(0.78), ry(0.44)),
        (rx(0.50), ry(0.28)),
        (rx(0.80), ry(0.28)),
        (rx(0.52), ry(0.12)),
        (rx(0.82), ry(0.12))
    ]
    sys_w = 4.2
    sys_h = 1.35
    for s_name, (sx, sy) in zip(systems, slots):
        # Mini Browser shadow offset for wobbly depth
        ax.add_patch(FancyBboxPatch(
            (sx + 0.08, sy - 0.08), sys_w, sys_h,
            boxstyle="round,pad=0.03,rounding_size=0.1",
            fill=True, color="#E8E8E8", zorder=2.1))
        # Main browser window
        ax.add_patch(FancyBboxPatch(
            (sx, sy), sys_w, sys_h,
            boxstyle="round,pad=0.03,rounding_size=0.1",
            fill=True, facecolor=BG, edgecolor=INK, linewidth=1.0, zorder=2.2))
        # Window bar
        ax.add_line(Line2D([sx, sx + sys_w], [sy + sys_h - 0.35, sy + sys_h - 0.35], color=INK, linewidth=0.8, zorder=2.3))
        # URL dot indicators
        ax.add_patch(plt.Circle((sx + 0.22, sy + sys_h - 0.18), 0.06, color=INK, zorder=2.4))
        ax.add_patch(plt.Circle((sx + 0.44, sy + sys_h - 0.18), 0.06, color=INK, zorder=2.4))
        # Floating window title
        ax.text(sx + sys_w/2, sy + (sys_h - 0.35)/2, s_name, fontfamily=BODY_FONT, fontsize=8.5,
                ha="center", va="center", color=INK, zorder=2.4)

    # ── 5. Clock: the manual cost ──
    clock_cx = rx(0.88)
    clock_cy = ry(0.56)
    clock_r = 1.25
    ax.add_patch(plt.Circle((clock_cx, clock_cy), clock_r, fill=False, edgecolor=accent_color, linewidth=1.4, zorder=3))
    # Hands pointing to midnight overhead
    ax.add_line(Line2D([clock_cx, clock_cx], [clock_cy, clock_cy + 0.75], color=accent_color, linewidth=1.3, zorder=3.5))
    ax.add_line(Line2D([clock_cx, clock_cx + 0.6], [clock_cy, clock_cy - 0.15], color=accent_color, linewidth=1.3, zorder=3.5))
    # Alarm vibration arcs
    ax.add_patch(plt.matplotlib.patches.Arc((clock_cx - 1.1, clock_cy), 0.4, 0.8, theta1=110, theta2=250, color=accent_color, linewidth=1.1, zorder=3))
    ax.add_patch(plt.matplotlib.patches.Arc((clock_cx + 1.1, clock_cy), 0.4, 0.8, theta1=290, theta2=70, color=accent_color, linewidth=1.1, zorder=3))


def render_flywheel(ax, box, stages, center, caption=None, accent_color=INK):
    """Clockwise n-stage flywheel around a centre record, with a small helper robot."""
    rx = lambda f: box.x0 + f * box.w
    ry = lambda f: box.y0 + f * box.h

    cx, cy = rx(0.5), ry(0.49)
    bw, bh = 4.4, 1.4
    r_outer = min(box.w / 2 - bw / 2 - 0.4, box.h / 2 - bh / 2 - 1.1)
    n = len(stages)

    # Centre record: a stacked file labelled with the spec's `center`
    ctr_w, ctr_h = box.w * 0.24, box.h * 0.08
    # cylinder bottom block
    ax.add_patch(FancyBboxPatch(
        (cx - ctr_w / 2, cy - ctr_h / 2), ctr_w, ctr_h,
        boxstyle="round,pad=0.1,rounding_size=0.2",
        fill=True, facecolor="#FFFCEE", edgecolor=INK, linewidth=1.4, zorder=4))
    # Database disk divisions representing a unified record schema
    ax.add_line(Line2D([cx - ctr_w/2 - 0.08, cx + ctr_w/2 + 0.08], [cy, cy], color=INK, linewidth=1.0, zorder=4.5))
    ax.add_line(Line2D([cx - ctr_w/2 - 0.08, cx + ctr_w/2 + 0.08], [cy + ctr_h/4, cy + ctr_h/4], color=INK, linewidth=1.0, zorder=4.5))
    ax.text(cx, cy - ctr_h*0.1, "\n".join(textwrap.wrap(str(center), 12)), fontfamily=BODY_FONT, fontsize=10.5,
            ha="center", va="center", color=INK, weight="bold", zorder=5)

    # Curved rotating arrows between stages
    r_inner = r_outer - 1.4
    for i in range(n):
        a0 = math.pi / 2 - (2 * math.pi * i / n) - 0.18
        a1 = math.pi / 2 - (2 * math.pi * (i + 1) / n) + 0.18
        x0 = cx + r_inner * math.cos(a0)
        y0 = cy + r_inner * math.sin(a0)
        x1 = cx + r_inner * math.cos(a1)
        y1 = cy + r_inner * math.sin(a1)
        ax.add_patch(FancyArrowPatch(
            (x0, y0), (x1, y1),
            connectionstyle="arc3,rad=-0.35",
            arrowstyle="-|>", mutation_scale=14,
            color=accent_color, linewidth=1.6, zorder=3))

    # Flywheel Stage Card Boxes
    for i in range(n):
        angle = math.pi / 2 - (2 * math.pi * i / n)
        sx = cx + r_outer * math.cos(angle)
        sy = cy + r_outer * math.sin(angle)
        # Background box
        ax.add_patch(FancyBboxPatch(
            (sx - bw / 2, sy - bh / 2), bw, bh,
            boxstyle="round,pad=0.10,rounding_size=0.25",
            fill=True, facecolor=BG, edgecolor=accent_color,
            linewidth=1.4, zorder=4))
        ax.text(sx, sy, stages[i], fontfamily=BODY_FONT, fontsize=10.5,
                ha="center", va="center", color=INK,
                weight="bold", zorder=5)

    # Cute Robot Agent hovering at top-right
    rx_bot = rx(0.85)
    ry_bot = ry(0.52)
    # Head
    ax.add_patch(plt.Circle((rx_bot, ry_bot), 0.55, fill=True, facecolor="#E6F2FF", edgecolor=INK, linewidth=1.2, zorder=4))
    # Antenna
    ax.add_line(Line2D([rx_bot, rx_bot], [ry_bot + 0.55, ry_bot + 0.95], color=INK, linewidth=1.2, zorder=4.5))
    ax.add_patch(plt.Circle((rx_bot, ry_bot + 0.95), 0.12, color=accent_color, zorder=5))
    # Eyes
    ax.add_patch(plt.Circle((rx_bot - 0.16, ry_bot + 0.08), 0.04, color=INK, zorder=5))
    ax.add_patch(plt.Circle((rx_bot + 0.16, ry_bot + 0.08), 0.04, color=INK, zorder=5))
    # Smiling mouth
    ax.add_patch(plt.matplotlib.patches.Arc(
        (rx_bot, ry_bot - 0.14), 0.38, 0.28,
        theta1=200, theta2=340, color=INK, linewidth=1.1, zorder=5))
    # Robot body
    ax.add_patch(FancyBboxPatch(
        (rx_bot - 0.7, ry_bot - 1.5), 1.4, 0.95,
        boxstyle="round,pad=0.05,rounding_size=0.15",
        fill=True, facecolor="#E6F2FF", edgecolor=INK, linewidth=1.2, zorder=3.5))
    ax.text(rx_bot, ry_bot - 1.0, "BOT", fontfamily=ALT_FONT, fontsize=8,
            ha="center", va="center", color=accent_color, weight="bold", zorder=4)
    # Joints
    ax.add_line(Line2D([rx_bot, rx_bot], [ry_bot - 0.55, ry_bot - 0.65], color=INK, linewidth=1.2, zorder=3.5))

    if caption:
        ax.text(cx, box.y0 + 1.6, caption,
                fontfamily=BODY_FONT, fontsize=10,
                ha="center", va="bottom", color=INK_SOFT,
                style="italic", zorder=4)


def render_stages(ax, box, rows, caption=None, accent_color=INK):
    """Stacked rows of: S1-S3 or S4-S6 with gorgeous illustrative whiteboard icons on the right side of each."""
    rx = lambda f: box.x0 + f * box.w
    ry = lambda f: box.y0 + f * box.h

    inset_top = 4.2
    inset_bot = 2.4 if caption else 1.2
    area = Box(box.x0 + 0.8, box.y0 + inset_bot,
               box.x1 - 0.8, box.y1 - inset_top)

    n = len(rows)
    gap = 0.5
    row_h = (area.h - (n - 1) * gap) / n

    tag_w = 4.8
    text_left = area.x0 + tag_w + 1.2
    # Determine which stages card we are: P3 (S1-S3) vs P4 (S4-S6)
    is_top_stages = any("S1" in row.get("tag", "") for row in rows)

    for i, row in enumerate(rows):
        ry1 = area.y1 - i * (row_h + gap)
        ry0 = ry1 - row_h
        tag = row.get("tag", "")
        text = row.get("text", "")

        # Tag pill on the left
        pill_h = min(row_h - 0.3, 1.8)
        pill_y = (ry0 + ry1) / 2 - pill_h / 2
        ax.add_patch(FancyBboxPatch(
            (area.x0, pill_y), tag_w, pill_h,
            boxstyle="round,pad=0.10,rounding_size=0.4",
            fill=True, facecolor=BG, edgecolor=accent_color,
            linewidth=1.4, zorder=3))
        ax.text(area.x0 + tag_w / 2, (ry0 + ry1) / 2, tag,
                fontfamily=BODY_FONT, fontsize=11,
                ha="center", va="center", color=accent_color,
                weight="bold", zorder=4)

        # Action description in the middle
        text_lines = text.split("\n") if isinstance(text, str) else list(text)
        block_h = (len(text_lines) - 1) * 1.15
        start_y = (ry0 + ry1) / 2 + block_h / 2
        for k, ln in enumerate(text_lines):
            ax.text(text_left, start_y - k * 1.15, ln,
                    fontfamily=BODY_FONT, fontsize=11,
                    ha="left", va="center", color=INK, zorder=4)

        # Draw custom interactive whiteboard artwork on the far right of the row
        icon_cx = area.x1 - 4.5
        icon_cy = (ry0 + ry1) / 2

        if is_top_stages:
            if i == 0:  # Intake: a ringing phone
                ax.add_patch(FancyBboxPatch((icon_cx - 0.45, icon_cy - 0.8), 0.9, 1.6, boxstyle="round,pad=0.03,rounding_size=0.15", fill=True, facecolor="#FFFDEF", edgecolor=accent_color, linewidth=1.2, zorder=3))
                ax.add_patch(plt.Circle((icon_cx, icon_cy - 0.6), 0.07, color=accent_color, zorder=3.5))
                # Ringer soundwaves
                ax.add_patch(plt.matplotlib.patches.Arc((icon_cx - 0.9, icon_cy), 0.4, 0.8, theta1=110, theta2=250, color=accent_color, linewidth=1.0))
                ax.add_patch(plt.matplotlib.patches.Arc((icon_cx + 0.9, icon_cy), 0.4, 0.8, theta1=290, theta2=70, color=accent_color, linewidth=1.0))
            elif i == 1:  # Assess: approve / reject card
                cw, ch = 2.6, 1.6
                ax.add_patch(FancyBboxPatch((icon_cx - cw/2, icon_cy - ch/2), cw, ch, boxstyle="round,pad=0.05,rounding_size=0.1", fill=True, facecolor="#FFFDEF", edgecolor=accent_color, linewidth=1.0, zorder=3))
                ax.text(icon_cx - 0.5, icon_cy + 0.3, "[y] Approve", fontfamily=BODY_FONT, fontsize=8, color="green", ha="left", va="center", weight="bold", zorder=4)
                ax.text(icon_cx - 0.5, icon_cy - 0.3, "[x] Reject", fontfamily=BODY_FONT, fontsize=8, color="red", ha="left", va="center", zorder=4)
            elif i == 2:  # Match: three linked records
                nx0, ny0 = icon_cx - 0.8, icon_cy - 0.4
                nx1, ny1 = icon_cx + 0.8, icon_cy - 0.4
                nx2, ny2 = icon_cx,     icon_cy + 0.5
                ax.add_line(Line2D([nx0, nx2], [ny0, ny2], color=accent_color, linewidth=1.1, zorder=3))
                ax.add_line(Line2D([nx1, nx2], [ny1, ny2], color=accent_color, linewidth=1.1, zorder=3))
                ax.add_line(Line2D([nx0, nx1], [ny0, ny1], color=accent_color, linewidth=1.1, zorder=3))
                ax.add_patch(plt.Circle((nx0, ny0), 0.35, fill=True, facecolor="#FFE5CC", edgecolor=accent_color, linewidth=1.0, zorder=4))
                ax.add_patch(plt.Circle((nx1, ny1), 0.35, fill=True, facecolor="#FFE5CC", edgecolor=accent_color, linewidth=1.0, zorder=4))
                ax.add_patch(plt.Circle((nx2, ny2), 0.35, fill=True, facecolor="#FFE5CC", edgecolor=accent_color, linewidth=1.0, zorder=4))
        else:
            if i == 0:  # Schedule: a calendar with the booked day ticked
                cw, ch = 2.2, 1.7
                ax.add_patch(FancyBboxPatch((icon_cx - cw/2, icon_cy - ch/2), cw, ch, boxstyle="round,pad=0.03,rounding_size=0.1", fill=True, facecolor="#FFFDEF", edgecolor=accent_color, linewidth=1.1, zorder=3))
                ax.add_line(Line2D([icon_cx - cw/2, icon_cx + cw/2], [icon_cy + ch/2 - 0.45, icon_cy + ch/2 - 0.45], color=accent_color, linewidth=1.1, zorder=3.5))
                for k in range(4):
                    if k != 2:
                        ax.add_patch(plt.Circle((icon_cx - 0.75 + k * 0.5, icon_cy - 0.25), 0.06, color=INK, zorder=4))
                ax.add_line(Line2D([icon_cx + 0.1, icon_cx + 0.25, icon_cx + 0.5], [icon_cy - 0.2, icon_cy - 0.4, icon_cy + 0.05], color="green", linewidth=1.6, zorder=4.5))
            elif i == 1:  # Fix: a wrench
                ax.add_line(Line2D([icon_cx - 1.0, icon_cx + 0.45], [icon_cy - 0.5, icon_cy + 0.2], color=accent_color, linewidth=4.0, solid_capstyle="round", zorder=3))
                ax.add_patch(plt.matplotlib.patches.Arc((icon_cx + 0.7, icon_cy + 0.32), 0.7, 0.7, theta1=76, theta2=336, color=accent_color, linewidth=3.0, zorder=3))
            elif i == 2:  # Learn: feedback loop
                ax.add_patch(plt.Circle((icon_cx, icon_cy), 0.8, fill=False, edgecolor=accent_color, linestyle="--", linewidth=1.0, zorder=3))
                # recursive arrows wrapping circular
                ax.add_patch(FancyArrowPatch((icon_cx - 0.3, icon_cy + 0.8), (icon_cx + 0.4, icon_cy + 0.8), arrowstyle="-|>", mutation_scale=9, color=accent_color, linewidth=1.3, zorder=4))
                ax.add_patch(FancyArrowPatch((icon_cx + 0.3, icon_cy - 0.8), (icon_cx - 0.4, icon_cy - 0.8), arrowstyle="-|>", mutation_scale=9, color=accent_color, linewidth=1.3, zorder=4))
                ax.text(icon_cx, icon_cy, "Train", fontfamily=BODY_FONT, fontsize=7.5, color=accent_color, ha="center", va="center", weight="bold", zorder=4)

    if caption:
        ax.text(area.cx, box.y0 + 1.4, caption,
                fontfamily=BODY_FONT, fontsize=10,
                ha="center", va="bottom", color=INK_SOFT,
                style="italic", zorder=4)


def render_value(ax, box, bullets, metric_before, metric_after,
                 annotation=None, persona=None, persona_role=None, accent_color=ACCENT["green"]):
    """Metric badge top (styled like highlighted Post-it notes) + checkbox lists + happy thumbs-up persona."""
    rx = lambda f: box.x0 + f * box.w
    ry = lambda f: box.y0 + f * box.h

    inset_top = 4.2
    inset_bot = 1.3
    area = Box(box.x0 + 0.8, box.y0 + inset_bot,
               box.x1 - 0.8, box.y1 - inset_top)

    # 1. Double outlined highlighted sticky metric badge
    mb_h = 3.2
    mb_y = area.y1 - mb_h - 0.3
    # Inner background fill
    ax.add_patch(FancyBboxPatch(
        (area.x0, mb_y), area.w, mb_h,
        boxstyle="round,pad=0.2,rounding_size=0.4",
        fill=True, facecolor="#EBF7EB", edgecolor="none", zorder=2.5))
    # Double borders to capture organic marker line overlay sketching
    ax.add_patch(FancyBboxPatch(
        (area.x0, mb_y), area.w, mb_h,
        boxstyle="round,pad=0.2,rounding_size=0.4",
        fill=False, edgecolor=accent_color, linewidth=1.4, zorder=3))
    ax.add_patch(FancyBboxPatch(
        (area.x0 - 0.1, mb_y - 0.1), area.w + 0.2, mb_h + 0.2,
        boxstyle="round,pad=0.2,rounding_size=0.4",
        fill=False, edgecolor=accent_color, linewidth=0.8, alpha=0.6, zorder=3))

    label = f"{metric_before}   -->   {metric_after}"
    ax.text(area.cx, mb_y + mb_h * 0.65, label,
            fontfamily=ALT_FONT, fontsize=16, ha="center", va="center",
            color=accent_color, weight="bold", zorder=4)
    if annotation:
        ax.text(area.cx, mb_y + mb_h * 0.24, annotation,
                fontfamily=BODY_FONT, fontsize=11.5, ha="center", va="center",
                color=accent_color, weight="bold", style="italic", zorder=4)

    # 2. Checkbox bullet list
    bullets_y_top = mb_y - 1.2
    n = len(bullets)
    figure_zone_top = area.y0 + 4.8
    bullet_line_h = (bullets_y_top - figure_zone_top) / max(n, 1)
    bullet_line_h = min(4.5, bullet_line_h)
    for i, b in enumerate(bullets):
        by = bullets_y_top - (i + 0.5) * bullet_line_h
        # Draw nice small wobbly check square: [✓]
        sq_cx = area.x0 + 0.6
        ax.add_patch(FancyBboxPatch((sq_cx - 0.4, by - 0.4), 0.8, 0.8, boxstyle="round,pad=0.03,rounding_size=0.1", fill=True, facecolor="#FFFDEF", edgecolor=accent_color, linewidth=1.1, zorder=4))
        # Draw elegant marker checkmark ticks
        ax.add_line(Line2D([sq_cx - 0.18, sq_cx - 0.02], [by - 0.05, by - 0.22], color="green", linewidth=1.8, zorder=5))
        ax.add_line(Line2D([sq_cx - 0.02, sq_cx + 0.22], [by - 0.22, by + 0.22], color="green", linewidth=1.8, zorder=5))
        # Bullet text
        ax.text(area.x0 + 1.8, by, b,
                fontfamily=BODY_FONT, fontsize=11,
                ha="left", va="center", color=INK, zorder=4)

    # 3. Smiling stick figure at bottom right giving thumbs-up with "radiant shine rays"
    sf_cx = area.x1 - 2.0
    sf_cy = area.y0 + 1.2

    # Draw thumbs-up stick figure
    stick_figure(ax, sf_cx, sf_cy, mood="smile", color=accent_color, scale=0.95)

    # Draw radiant success lines (green marker sunbursts) around head
    head_cy = sf_cy + 1.6 * 0.95
    for a in range(0, 360, 45):
        rad = math.radians(a)
        offset_start = 0.55 * 0.95 + 0.25
        offset_end = offset_start + 0.4
        ax.add_line(Line2D([sf_cx + offset_start * math.cos(rad), sf_cx + offset_end * math.cos(rad)],
                           [head_cy + offset_start * math.sin(rad), head_cy + offset_end * math.sin(rad)],
                           color=accent_color, linewidth=0.9, alpha=0.85, zorder=2))

    if persona:
        ax.text(sf_cx - 1.8, sf_cy + 0.8, persona_label(persona, persona_role), fontfamily=BODY_FONT,
                fontsize=12, ha="right", va="center",
                color=accent_color, weight="bold")


# ── Title bar ───────────────────────────────────────────────────────────────

def render_title_bar(ax, box, title, subtitle):
    # Two stacked text lines; title fontsize tapers if long.
    size = 22 if len(title) <= 30 else (18 if len(title) <= 60 else 16)
    title_y = box.y1 - 0.4
    sub_y = box.y0 + 0.4
    ax.text(box.cx, title_y, title, fontfamily=ALT_FONT, fontsize=size,
            ha="center", va="top", color=INK, weight="bold", zorder=4)
    if subtitle:
        ax.text(box.cx, sub_y, subtitle, fontfamily=BODY_FONT, fontsize=11,
                ha="center", va="bottom", color=INK_SOFT,
                style="italic", zorder=4)


# ── Main ────────────────────────────────────────────────────────────────────

def lint(spec):
    errs = []
    if not spec.get("title"):
        errs.append("title missing")
    panels = spec.get("panels", [])
    if len(panels) != 5:
        errs.append(f"expected 5 panels, got {len(panels)}")
    for p in panels:
        if "title" not in p or "id" not in p:
            errs.append(f"panel missing title/id: {p}")
    return errs


def render(spec, out_path):
    fig, ax = plt.subplots(figsize=(CANVAS_W_IN, CANVAS_H_IN), dpi=DPI)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    L = layout()

    render_title_bar(ax, L["title"], spec["title"], spec.get("subtitle", ""))

    # Dividers (dashed): horizontal under title, between rows; vertical between panels.
    top_y = L["P1"].y1 + 0.25
    bot_y = L["P4"].y1
    dashed(ax, L["P1"].x0, top_y, L["P3"].x1, top_y)
    dashed(ax, L["P4"].x0, bot_y, L["P5"].x1, bot_y)
    dashed(ax, L["P2"].x0, L["P1"].y0, L["P2"].x0, L["P1"].y1)
    dashed(ax, L["P3"].x0, L["P1"].y0, L["P3"].x0, L["P1"].y1)
    dashed(ax, L["P5"].x0, L["P4"].y0, L["P5"].x0, L["P4"].y1)

    panels = spec["panels"]
    persona_name = spec.get("persona_name")
    persona_role = spec.get("persona_role")

    for i, p in enumerate(panels):
        n = i + 1
        slot = L[f"P{n}"]
        accent_color = ACCENT.get(p.get("accent", "black"), INK)
        panel_label(ax, slot, n, p["title"], p.get("kicker", ""), accent_color)

        ptype = p.get("type", "scene")
        if ptype == "scene":
            mood = "smile" if n == 5 else "frown"
            render_scene(ax, slot, p.get("body", []),
                         accent_color=accent_color,
                         persona=p.get("persona"),
                         persona_role=persona_role if p.get("persona") else None,
                         mood=mood)
        elif ptype == "flywheel":
            render_flywheel(ax, slot,
                            stages=p["stages"], center=p["center"],
                            caption=p.get("caption"),
                            accent_color=accent_color)
        elif ptype == "stages":
            render_stages(ax, slot, rows=p["rows"],
                          caption=p.get("caption"),
                          accent_color=accent_color)
        elif ptype == "value":
            render_value(ax, slot,
                         bullets=p.get("bullets", []),
                         metric_before=p["metric_before"],
                         metric_after=p["metric_after"],
                         annotation=p.get("annotation"),
                         persona=p.get("persona"),
                         persona_role=persona_role if p.get("persona") else None,
                         accent_color=accent_color)
        else:
            ax.text(slot.cx, slot.cy, f"unknown panel type: {ptype}",
                    ha="center", va="center", color=ACCENT["red"])

    fig.savefig(out_path, dpi=DPI, bbox_inches="tight",
                facecolor=BG, edgecolor="none")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Storyboard YAML spec.")
    ap.add_argument("output", help="Output PNG path.")
    args = ap.parse_args()

    spec_path = Path(args.input)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    spec = yaml.safe_load(spec_path.read_text())
    errs = lint(spec)
    if errs:
        sys.stderr.write("\n".join("lint: " + e for e in errs) + "\n")
        sys.exit(2)

    render(spec, str(out_path))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
