#!/usr/bin/env python3
"""The World in One Day -- Wednesday 25 November 2026.

Draws a one-page newspaper front page summarising the day's world news
(make.fun bounty news-image-20261125) with Pillow, from fixed text and
fixed geometry only: no network, no clock, no randomness, so every run
writes byte-identical PNG output.

Usage:
    python3 main.py                 # writes entry.png
    python3 main.py --verify FILE   # exit 0 iff FILE matches the pinned SHA-256

Output goes to $MAKEFUN_OUTPUT_DIR/entry.png, or ./entry.png when the
variable is unset.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# SHA-256 pin of the entry.png this program produces. Filled in after the
# first render; main() refuses to exit 0 when the rendered bytes differ.
PIN = "becdc62d138f1d15a674e8c1b035eed9766f8eeeb671a361865df6adcdcf2a1f"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# Palette: newsprint on warm paper.
PAPER = (253, 251, 245)
INK = (17, 17, 17)
SOFT = (74, 74, 74)
RULE = (17, 17, 17)
ACCENT = (163, 18, 26)          # deep red for kickers
BOX_BG = (242, 239, 230)
BOX_LINE = (120, 116, 104)
NAVY = (26, 42, 74)             # lead illustration sky
STEEL = (58, 66, 84)
FLAME = (232, 122, 32)
FLAME2 = (244, 196, 66)
SMOKE = (176, 176, 168)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)          # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)      # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)             # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap of fixed text to a pixel width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_lead_art(draw, x, y, w, h):
    """Night refinery under drone attack: sky, towers, flames, smoke, drone."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # distant skyline
    draw.rectangle([x, y + h - 46, x + w, y + h], fill=(16, 26, 48))
    # refinery towers and chimneys (silhouette)
    draw.rectangle([x + 22, y + h - 108, x + 66, y + h - 46], fill=STEEL)
    draw.rectangle([x + 78, y + h - 88, x + 118, y + h - 46], fill=STEEL)
    draw.rectangle([x + 130, y + h - 118, x + 138, y + h - 46], fill=STEEL)
    draw.rectangle([x + 150, y + h - 96, x + 158, y + h - 46], fill=STEEL)
    draw.rectangle([x + 196, y + h - 80, x + 246, y + h - 46], fill=STEEL)
    draw.rectangle([x + 258, y + h - 110, x + 266, y + h - 46], fill=STEEL)
    draw.rectangle([x + 278, y + h - 92, x + 318, y + h - 46], fill=STEEL)
    # flames licking from two struck towers
    for fx, fy, s in ((x + 34, y + h - 128, 16), (x + 262, y + h - 132, 18),
                      (x + 100, y + h - 104, 12)):
        draw.polygon([(fx - s, fy), (fx, fy - s - 8), (fx + s, fy),
                      (fx + s // 2, fy - s // 2), (fx - s // 2, fy - s // 2)],
                     fill=FLAME)
        draw.polygon([(fx - s // 2, fy), (fx, fy - s), (fx + s // 2, fy)],
                     fill=FLAME2)
    # smoke puffs
    for sx, sy, r in ((x + 44, y + 22, 12), (x + 66, y + 12, 9),
                      (x + 272, y + 20, 11), (x + 290, y + 10, 8)):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SMOKE)
    # drone top right: body, arms, four rotors
    dx, dy = x + w - 66, y + 34
    draw.line([(dx - 22, dy - 8), (dx + 22, dy + 8)], fill=(220, 220, 220), width=2)
    draw.line([(dx - 22, dy + 8), (dx + 22, dy - 8)], fill=(220, 220, 220), width=2)
    draw.rectangle([dx - 9, dy - 5, dx + 9, dy + 5], fill=(220, 220, 220))
    for rx, ry in ((dx - 24, dy - 10), (dx + 24, dy + 10),
                   (dx - 24, dy + 10), (dx + 24, dy - 10)):
        draw.ellipse([rx - 7, ry - 2, rx + 7, ry + 2], fill=(200, 200, 200))
    # caption bar inside the art
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(0, 0, 0))
    draw.text((x + 8, y + h - 19),
              "Drones hit two refineries in the Samara region",
              font=SANS(11), fill=(240, 240, 235))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 28                      # side margin
    RX = W - MX                  # right edge

    # ---- Masthead -------------------------------------------------------
    hrule(d, MX, RX, 14, width=3)
    d.text((MX, 20), "THE WORLD IN ONE DAY", font=SERIF_B(56), fill=INK)
    d.text((MX, 84), "WEDNESDAY  25  NOVEMBER  2026      \u00b7      No. 25",
           font=SANS_B(19), fill=INK)
    d.text((RX - 268, 84), "THE DAY IN ONE PAGE", font=SANS(19), fill=SOFT)
    hrule(d, MX, RX, 110, width=2)

    # ---- Lead story -----------------------------------------------------
    d.text((MX, 120), "UKRAINE  \u00b7  RUSSIA  \u00b7  OIL WAR", font=SANS_B(18),
           fill=ACCENT)
    headline = ("Putin vows retaliation as Ukraine hits "
                "two more refineries")
    y = draw_lines(d, wrap(d, headline, SERIF_B(40), RX - MX), MX, 144,
                   SERIF_B(40), INK, 44)
    deck = ("Drones strike the Syzran and Kuibyshev plants in the Samara "
            "region; Russian crude runs are down about 45% since late "
            "October.")
    y = draw_lines(d, wrap(d, deck, SANS(19), RX - MX), MX, 240, SANS(19),
                   SOFT, 24)
    # body column (left) + illustration (right)
    body_w = 600
    body = [
        "President Vladimir Putin said on Tuesday that retaliatory "
        "measures were \u201cinevitable\u201d after Ukraine kept striking "
        "Russian refineries despite a direct request from US President "
        "Donald Trump to stop.",
        "Overnight, Ukrainian drones hit two major refineries in the "
        "Samara region, some 800 km from the border, sparking fires \u2014 "
        "a large blaze at the Kuibyshev plant. Kyiv says it will stop "
        "only if Moscow does the same.",
        "A Russian strike on a block of flats in Zaporizhzhia killed "
        "2 people and wounded about 50.",
    ]
    by = 292
    for para in body:
        by = draw_lines(d, wrap(d, para, SANS(16), body_w), MX, by,
                        SANS(16), INK, 19)
        by += 5
    draw_lead_art(d, MX + body_w + 16, 292, RX - (MX + body_w + 16), 162)
    hrule(d, MX, RX, 462, width=2)

    # ---- Four-story grid ------------------------------------------------
    grid = [
        ("MARKETS",
         "Monday's rally dies in a day; Bitcoin slips back under $60,000",
         "Nasdaq \u22121.48%, S&P 500 \u22120.50% as chip stocks plunged "
         "nearly 8%. Bitcoin about $59,300; spot Bitcoin ETFs saw "
         "$569.7m of outflows on 23 Nov, a fifth straight day. Gold "
         "$3,547; oil $81.65. US October PCE inflation due today."),
        ("RIYADH",
         "Houthi drone hits the PIF Tower again; 11 wounded",
         "A drone struck the 385-metre PIF Tower in Riyadh's financial "
         "district \u2014 the second hit in under a week. 11 wounded, at "
         "least 2 in critical condition. The Saudi-led coalition vowed "
         "a decisive response; the Houthis have not claimed Tuesday's "
         "attack."),
        ("CHINA",
         "Huawei convicted in the US; spy death sentence; Shanghai chief probed",
         "A Brooklyn jury found Huawei guilty of conspiring to steal "
         "trade secrets and bank fraud. China handed a death sentence "
         "to an official accused of leaking state secrets. Shanghai "
         "party chief Chen Jining is under investigation."),
        ("GAZA",
         "Israeli strike kills Hamas internal security chief",
         "Israeli airstrikes in Gaza on Tuesday killed 7 people, "
         "including Naim Abu Nahl, head of Hamas's internal security "
         "service. Gaza officials say 1,700 people have been killed in "
         "ceasefire violations."),
    ]
    gw = (RX - MX - 16) // 2     # box width
    gh = 186                     # box height
    gy0 = 472
    for i, (kicker, head, text) in enumerate(grid):
        gx = MX + (i % 2) * (gw + 16)
        gy = gy0 + (i // 2) * (gh + 10)
        d.rectangle([gx, gy, gx + gw, gy + gh], fill=BOX_BG,
                    outline=BOX_LINE, width=1)
        d.text((gx + 12, gy + 9), kicker, font=SANS_B(16), fill=ACCENT)
        hy = draw_lines(d, wrap(d, head, SERIF_B(20), gw - 24), gx + 12,
                        gy + 32, SERIF_B(20), INK, 24)
        draw_lines(d, wrap(d, text, SANS(15), gw - 24), gx + 12, hy + 6,
                   SANS(15), INK, 19)
    hrule(d, MX, RX, 862, width=2)

    # ---- In Brief --------------------------------------------------------
    d.text((MX, 870), "IN BRIEF", font=SANS_B(18), fill=ACCENT)
    brief = [
        "Sarkozy and wife Carla Bruni ordered to stand trial in a corruption "
        "case; first hearing 1 April 2027.",
        "Indonesia's vice-president resigns amid political strain.",
        "US prepares fresh tariff hikes on China and the EU to replace "
        "court-struck levies.",
        "CIA and ODNI hit by a hack of unclassified systems; classified "
        "systems unaffected.",
        "Norway to give Ukraine at least $7bn in 2027, air defence first.",
        "Mount Mayon eruption in the Philippines raises fears of a larger event.",
    ]
    by = 894
    for item in brief:
        d.text((MX, by), "\u2022", font=SANS_B(15), fill=ACCENT)
        draw_lines(d, wrap(d, item, SANS(15), RX - MX - 18), MX + 18, by,
                   SANS(15), INK, 16)
        by += 16

    # ---- Footer ----------------------------------------------------------
    hrule(d, MX, RX, 994, width=1, fill=BOX_LINE)
    d.text((MX, 1000),
           "Sources: Reuters \u00b7 AP \u00b7 The Independent \u00b7 The Wall "
           "Street Journal \u00b7 Al Jazeera \u00b7 Kyiv Independent \u00b7 "
           "Dawn \u00b7 KuCoin \u00b7 Finnhub",
           font=SANS(13), fill=SOFT)
    return img


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify(path):
    """Exit 0 iff the file at path matches the pinned SHA-256."""
    digest = sha256_file(path)
    if digest != PIN:
        print("MISMATCH: %s sha256=%s expected=%s" % (path, digest, PIN),
              file=sys.stderr)
        return 1
    print("OK: %s sha256=%s" % (path, digest))
    return 0


def main(argv):
    if len(argv) == 3 and argv[1] == "--verify":
        return verify(argv[2])
    if len(argv) != 1:
        print("usage: main.py [--verify FILE]", file=sys.stderr)
        return 2
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img = build()
    img.save(out_path, format="PNG")
    return verify(out_path)


if __name__ == "__main__":
    sys.exit(main(sys.argv))

