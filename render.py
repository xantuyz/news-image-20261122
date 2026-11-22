#!/usr/bin/env python3
"""Render the 22 November 2026 world-news image (1024x1024 PNG).

Fresh code for news-image-20261122. Draws six verified stories with PIL
only; no network, no external assets. Deterministic: fixed fonts, fixed
layout, no timestamps or randomness in the output.
"""
import textwrap
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
# The grader mounts the repository read-only, so render into the path the
# caller gives (main.py points it at the writable output directory).
OUT = os.environ.get("ENTRY_OUT", "entry.png")

# --- palette: midnight teal + warm amber + paper cream (new identity) ---
INK = (14, 42, 58)        # deep teal-navy
TEAL = (18, 96, 110)      # accent teal
AMBER = (232, 148, 28)    # warm amber
PAPER = (250, 246, 236)   # cream paper
CARD = (255, 255, 255)
MUTED = (74, 92, 102)
RULE = (214, 205, 188)
RED = (178, 44, 36)
GREEN = (38, 120, 74)
BLUE = (42, 84, 160)
PURPLE = (96, 66, 140)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label, color):
    f = font(SANS_B, 15)
    w = draw.textlength(label, font=f) + 16
    draw.rounded_rectangle([x, y, x + w, y + 24], radius=12, fill=color)
    draw.text((x + 8, y + 4), label, font=f, fill=(255, 255, 255))
    return w


# --- small pictograms, one per story (simple PIL shapes) ---

def icon_ship(draw, cx, cy, s):
    # hull + mast + flame on a dark sea
    draw.polygon([(cx - s, cy + s * 0.2), (cx + s, cy + s * 0.2),
                  (cx + s * 0.7, cy + s * 0.7), (cx - s * 0.7, cy + s * 0.7)],
                 fill=INK)
    draw.rectangle([cx - 3, cy - s, cx + 3, cy + s * 0.2], fill=INK)
    draw.polygon([(cx + 3, cy - s), (cx + s * 0.7, cy - s * 0.5),
                  (cx + 3, cy - s * 0.5)], fill=AMBER)
    draw.polygon([(cx - s * 0.5, cy - s * 0.4), (cx - s * 0.2, cy - s * 1.0),
                  (cx + s * 0.1, cy - s * 0.4)], fill=(226, 88, 34))
    draw.polygon([(cx + s * 0.1, cy - s * 0.3), (cx + s * 0.35, cy - s * 0.8),
                  (cx + s * 0.55, cy - s * 0.3)], fill=(240, 160, 40))


def icon_badge(draw, cx, cy, s):
    draw.polygon([(cx, cy - s), (cx + s * 0.35, cy - s * 0.35),
                  (cx + s, cy), (cx + s * 0.35, cy + s * 0.35),
                  (cx, cy + s), (cx - s * 0.35, cy + s * 0.35),
                  (cx - s, cy), (cx - s * 0.35, cy - s * 0.35)],
                 fill=BLUE)
    draw.ellipse([cx - s * 0.42, cy - s * 0.42, cx + s * 0.42, cy + s * 0.42],
                 fill=(255, 255, 255))
    draw.text((cx - 7, cy - 11), "$", font=font(SANS_B, 22), fill=BLUE)


def icon_globe(draw, cx, cy, s):
    draw.ellipse([cx - s, cy - s, cx + s, cy + s], fill=TEAL)
    draw.ellipse([cx - s * 0.55, cy - s * 0.25, cx + s * 0.1, cy + s * 0.55],
                 fill=GREEN)
    draw.ellipse([cx + s * 0.25, cy - s * 0.7, cx + s * 0.8, cy - s * 0.1],
                 fill=GREEN)
    draw.arc([cx - s, cy - s, cx + s, cy + s], 200, 340, fill=(255, 255, 255),
             width=3)


def icon_blast(draw, cx, cy, s):
    draw.polygon([(cx - s, cy + s * 0.5), (cx, cy - s),
                  (cx + s, cy + s * 0.5)], fill=RED)
    draw.ellipse([cx - s * 0.3, cy + s * 0.1, cx + s * 0.3, cy + s * 0.7],
                 fill=AMBER)
    for dx in (-s * 0.9, s * 0.9):
        draw.line([cx + dx, cy - s * 0.4, cx + dx * 0.6, cy - s * 0.1],
                  fill=RED, width=4)


def icon_quake(draw, cx, cy, s):
    pts = [(cx - s, cy + s * 0.3), (cx - s * 0.5, cy - s * 0.4),
           (cx, cy + s * 0.4), (cx + s * 0.5, cy - s * 0.5),
           (cx + s, cy + s * 0.2)]
    draw.line(pts, fill=AMBER, width=6, joint="curve")
    draw.ellipse([cx - s * 0.25, cy - s * 0.25, cx + s * 0.25, cy + s * 0.25],
                 outline=RED, width=4)


def icon_shield(draw, cx, cy, s):
    draw.polygon([(cx - s * 0.7, cy - s * 0.6), (cx + s * 0.7, cy - s * 0.6),
                  (cx + s * 0.7, cy), (cx, cy + s),
                  (cx - s * 0.7, cy)], fill=PURPLE)
    draw.text((cx - 13, cy - s * 0.45), "FBI", font=font(SANS_B, 17),
              fill=(255, 255, 255))


ICONS = {"ship": icon_ship, "badge": icon_badge, "globe": icon_globe,
         "blast": icon_blast, "quake": icon_quake, "shield": icon_shield}


def card(draw, x, y, w, h, story):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=RULE, width=1)
    draw.rounded_rectangle([x, y, x + w, y + 6], radius=3, fill=story["color"])
    kicker(draw, x + 14, y + 16, story["tag"], story["color"])
    # icon disc, top right
    cx, cy, r = x + w - 42, y + 42, 30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PAPER,
                 outline=story["color"], width=2)
    ICONS[story["icon"]](draw, cx, cy, 17)
    ty = y + 50
    # Headlines wrap short of the icon disc in the top-right corner.
    hl = wrap(draw, story["head"], font(SERIF_B, 21), w - 118)
    ty = draw_lines(draw, x + 14, ty, hl, font(SERIF_B, 21), INK, 25)
    body = wrap(draw, story["body"], font(SANS, 15), w - 28)
    draw_lines(draw, x + 14, ty + 6, body, font(SANS, 15), MUTED, 20)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 148], fill=INK)
    d.rectangle([0, 148, W, 153], fill=AMBER)
    d.text((32, 22), "THE WORLD TODAY", font=font(SERIF_B, 58), fill=(255, 255, 255))
    d.text((32, 96), "SUNDAY, 22 NOVEMBER 2026  •  SIX STORIES FROM AROUND THE GLOBE",
           font=font(SANS_B, 17), fill=AMBER)
    d.text((W - 32 - d.textlength("No. 22", font=font(SERIF, 20)), 100),
           "No. 22", font=font(SERIF, 20), fill=(200, 210, 215))

    # ---- lead story (hero, full width) ----
    lx, ly, lw, lh = 24, 168, W - 48, 218
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=12, fill=INK)
    d.rounded_rectangle([lx, ly, lx + lw, ly + 6], radius=3, fill=AMBER)
    kicker(d, lx + 20, ly + 18, "LEAD  •  BALTIC SEA", AMBER)
    cx, cy, r = lx + lw - 78, ly + 92, 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    icon_ship(d, cx, cy, 34)
    head = "Russian cargo ship ablaze after drone strike"
    d.text((lx + 20, ly + 52), head, font=font(SERIF_B, 30),
           fill=(255, 255, 255))
    lead_body = ("The Sparta II was hit by two drones in the Gulf of Finland on "
                 "Saturday 21 November, caught fire and drifted into Finnish "
                 "waters. All 16 crew escaped in lifeboats. Finland says Ukraine "
                 "was most likely behind the attack; the sanctioned ship, owned "
                 "by Oboronlogistika, was bound for Kaliningrad.")
    lines = wrap(d, lead_body, font(SANS, 17), lw - 190)
    draw_lines(d, lx + 20, ly + 96, lines, font(SANS, 17),
               (220, 228, 232), 23)
    d.text((lx + 20, ly + lh - 28), "Sources: Reuters, CNN",
           font=font(SANS, 13), fill=(160, 175, 185))

    # ---- grid: stories 2-5 (2 x 2) ----
    stories = [
        dict(tag="MEXICO", color=BLUE, icon="badge",
             head="Top-10 FBI fugitive \u201cChapo Isidro\u201d captured",
             body="Mexican troops seized Fausto Isidro Meza Flores in Sinaloa "
                  "on Friday night, 20 November, with two aides. The US had "
                  "offered a $5m reward. Follow-on violence killed 11 people, "
                  "with burning roadblocks in Culiacán."),
        dict(tag="CLIMATE  •  COP31", color=GREEN, icon="globe",
             head="Climate talks drag on as fossil fuels vanish from draft",
             body="Negotiations in Antalya ran into Saturday with no mention of "
                  "fossil fuels in the latest draft, despite about 130 nations "
                  "demanding phase-out language. Talks may run into Sunday, "
                  "with an open clash with Saudi Arabia possible."),
        dict(tag="UKRAINE", color=RED, icon="blast",
             head="\u201cTriple-tap\u201d strike hits Zelensky\u2019s home city",
             body="A Russian ballistic missile hit a restaurant area in Kryvyi "
                  "Rih on Friday night, 20 November, then drones struck "
                  "rescuers. A 7-year-old and a 20-year-old paramedic were "
                  "killed; 60+ were hurt, on Ukraine\u2019s Children\u2019s Day."),
        dict(tag="PERU", color=AMBER, icon="quake",
             head="Magnitude 6.7 quake shakes central Peru",
             body="The quake struck at 19:09 local time on Friday 20 November, "
                  "9 km north-east of Carhuamayo in Junín, 108 km deep. It was "
                  "felt as far as Lima. No casualties were reported."),
    ]
    gx, gy, gw, gh, gap = 24, 402, (W - 48 - 16) // 2, 236, 16
    for i, st in enumerate(stories):
        x = gx + (i % 2) * (gw + gap)
        y = gy + (i // 2) * (gh + gap)
        card(d, x, y, gw, gh, st)

    # ---- bottom strip: FBI story + footer ----
    bx, by, bw, bh = 24, 890, W - 48, 78
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=CARD,
                        outline=RULE, width=1)
    d.rounded_rectangle([bx, by, bx + bw, by + 6], radius=3, fill=PURPLE)
    kicker(d, bx + 14, by + 14, "UNITED STATES", PURPLE)
    fbi_head = wrap(d, "FBI probes suspected hack of its crime database (NCIC)",
                    font(SERIF_B, 19), 640)
    draw_lines(d, bx + 14, by + 42, fbi_head, font(SERIF_B, 19), INK, 22)
    d.text((bx + 690, by + 16), "2nd FBI-system intrusion",
           font=font(SANS_B, 14), fill=PURPLE)
    d.text((bx + 690, by + 40), "in months, after FBIjobs.gov",
           font=font(SANS, 14), fill=MUTED)
    d.text((32, 982), "All six stories happened or were first reported 20\u201322 November 2026.  Sources: Reuters, CNN, AP, USGS.",
           font=font(SANS, 13), fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
