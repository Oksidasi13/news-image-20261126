#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up
Thursday 26 November 2026 in six verified stories.

Pure Pillow drawing primitives: no photos, no network, no external
assets beyond the system DejaVu fonts. The render is deterministic —
the same code always writes the same bytes.

Run:  python3 draw.py   (writes entry.png beside this file)

Stories (each checked against at least two sources, 26 Nov 2026):
 1. Houthis claim a drone strike on Saudi Arabia's Ras Tanura refinery;
    satellite images show smoke; the coalition says four drones were
    shot down and no damage is confirmed.
 2. Nasdaq dives about 4% intraday in an AI sell-off, then pares the
    loss to 0.6% at the close; Nvidia falls about 4%.
 3. USTR proposes new Section 301 tariffs on 14 economies: 15% for the
    EU, Japan, Korea, Switzerland and Taiwan; up to 35% for Vietnam.
 4. A fuel tanker overturns on Cairo's Ring Road; at least 31 killed,
    21 injured, 27 vehicles charred.
 5. Shenzhou-24 docks at Tiangong with Pakistan's first astronaut,
    Muhammad Zeeshan Ali, the first foreign visitor to the station.
 6. Champions League: Liverpool win 3-0 at Club Brugge; PSG held 2-2
    by Roma; Lille stun Bayern 2-1.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 26  # outer margin

PAPER = (247, 243, 231)
INK = (24, 24, 24)
MUTED = (96, 91, 80)
NAVY = (21, 34, 62)
GOLD = (196, 152, 58)
RED = (176, 32, 22)
GREEN = (28, 118, 50)
BLUE = (34, 82, 136)
ORANGE = (212, 94, 18)
CARD = (255, 253, 245)
CARD_LINE = (203, 196, 176)
TINT_BLUE = (224, 234, 244)
TINT_RED = (244, 226, 222)
TINT_GOLD = (243, 234, 210)
TINT_GREEN = (230, 242, 230)
TINT_GREY = (235, 233, 228)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns the lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, fnt, fill, lead):
    """Draw lines top to bottom; returns the y after the last line."""
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lead
    return y


# ------------------------------------------------------------- pictograms
def pic_refinery(d, x, y, s):
    """Two refinery towers with a flame and a smoke plume."""
    d.rectangle([x, y, x + s, y + s], fill=TINT_GOLD, outline=CARD_LINE)
    d.rectangle([x, y + s * 0.84, x + s, y + s], fill=(210, 182, 120))
    # distillation towers
    d.rectangle([x + s * 0.18, y + s * 0.30, x + s * 0.34, y + s * 0.84],
                fill=INK)
    d.rectangle([x + s * 0.44, y + s * 0.18, x + s * 0.58, y + s * 0.84],
                fill=INK)
    # tower tops
    d.rectangle([x + s * 0.14, y + s * 0.26, x + s * 0.38, y + s * 0.30],
                fill=INK)
    d.rectangle([x + s * 0.40, y + s * 0.14, x + s * 0.62, y + s * 0.18],
                fill=INK)
    # storage tank, lower right
    d.rounded_rectangle([x + s * 0.66, y + s * 0.66, x + s * 0.92, y + s * 0.84],
                        radius=10, fill=INK)
    # flame on the right tower
    fx, fy = x + s * 0.72, y + s * 0.30
    d.polygon([(fx, fy - s * 0.20), (fx + s * 0.11, fy + s * 0.05),
               (fx + s * 0.05, fy + s * 0.12), (fx - s * 0.05, fy + s * 0.12),
               (fx - s * 0.11, fy + s * 0.05)], fill=ORANGE)
    d.ellipse([fx - s * 0.035, fy + s * 0.02, fx + s * 0.035, fy + s * 0.09],
              fill=GOLD)
    # smoke dots rising left
    for i, (sx, sy, sr) in enumerate([(0.12, 0.22, 0.045), (0.08, 0.12, 0.06),
                                      (0.16, 0.06, 0.05)]):
        d.ellipse([x + s * (sx - sr), y + s * (sy - sr),
                   x + s * (sx + sr), y + s * (sy + sr)], fill=MUTED)


def pic_chart(d, x, y, s):
    """A jagged line chart plunging down, with a red arrowhead."""
    d.rectangle([x, y, x + s, y + s], fill=TINT_RED, outline=CARD_LINE)
    # faint grid
    for gy in (0.25, 0.5, 0.75):
        d.line([(x + s * 0.10, y + s * gy), (x + s * 0.90, y + s * gy)],
               fill=(225, 200, 195), width=2)
    pts = [(0.12, 0.22), (0.28, 0.30), (0.40, 0.26), (0.54, 0.48),
           (0.66, 0.44), (0.80, 0.68), (0.90, 0.78)]
    xy = [(x + s * px, y + s * py) for px, py in pts]
    d.line(xy, fill=RED, width=7, joint="curve")
    ex, ey = xy[-1]
    d.polygon([(ex, ey), (ex - s * 0.10, ey - s * 0.02),
               (ex - s * 0.02, ey - s * 0.10)], fill=RED)
    # last point marker
    d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=INK)


def pic_container(d, x, y, s):
    """A shipping container stamped with a big percent sign."""
    d.rectangle([x, y, x + s, y + s], fill=TINT_BLUE, outline=CARD_LINE)
    # container body
    cx0, cy0 = x + s * 0.12, y + s * 0.30
    cx1, cy1 = x + s * 0.88, y + s * 0.72
    d.rectangle([cx0, cy0, cx1, cy1], fill=NAVY, outline=INK, width=3)
    for i in range(5):
        vx = cx0 + s * 0.14 + i * s * 0.13
        d.line([(vx, cy0), (vx, cy1)], fill=(255, 255, 255), width=3)
    # percent sign in gold so it stands out from the white ribs
    d.text((x + s * 0.36, y + s * 0.36), "%", font=font(SANS_B, int(s * 0.30)),
           fill=GOLD)
    # wheels / ground
    d.line([(x + s * 0.10, y + s * 0.84), (x + s * 0.90, y + s * 0.84)],
           fill=INK, width=5)
    d.ellipse([x + s * 0.20, y + s * 0.78, x + s * 0.30, y + s * 0.88],
              fill=INK)
    d.ellipse([x + s * 0.66, y + s * 0.78, x + s * 0.76, y + s * 0.88],
              fill=INK)


def pic_tanker(d, x, y, s):
    """A fuel tanker under a burst of flame."""
    d.rectangle([x, y, x + s, y + s], fill=TINT_RED, outline=CARD_LINE)
    # flame burst
    cx, cy = x + s * 0.5, y + s * 0.30
    star = []
    for k in range(16):
        ang = k * 22.5
        rr = s * 0.24 if k % 2 == 0 else s * 0.11
        star.append((cx + rr * math.cos(math.radians(ang)),
                     cy + rr * math.sin(math.radians(ang))))
    d.polygon(star, fill=ORANGE, outline=INK)
    d.ellipse([cx - s * 0.06, cy - s * 0.06, cx + s * 0.06, cy + s * 0.06],
              fill=(255, 255, 255))
    # tanker body
    d.rounded_rectangle([x + s * 0.12, y + s * 0.58, x + s * 0.72, y + s * 0.80],
                        radius=12, fill=INK)
    d.rectangle([x + s * 0.72, y + s * 0.60, x + s * 0.88, y + s * 0.80],
                fill=INK)
    d.rectangle([x + s * 0.74, y + s * 0.62, x + s * 0.82, y + s * 0.68],
                fill=(255, 255, 255))
    # wheels
    for wx in (0.24, 0.58, 0.78):
        d.ellipse([x + s * (wx - 0.05), y + s * 0.78,
                   x + s * (wx + 0.05), y + s * 0.88], fill=INK,
                  outline=(255, 255, 255), width=2)
    d.line([(x + s * 0.08, y + s * 0.90), (x + s * 0.92, y + s * 0.90)],
           fill=(60, 60, 60), width=5)


def pic_rocket(d, x, y, s):
    """A rocket climbing past stars toward a ringed planet."""
    d.rectangle([x, y, x + s, y + s], fill=TINT_BLUE, outline=CARD_LINE)
    # stars
    for sx, sy in [(0.16, 0.16), (0.84, 0.12), (0.88, 0.42), (0.12, 0.52),
                   (0.78, 0.82)]:
        d.ellipse([x + s * (sx - 0.02), y + s * (sy - 0.02),
                   x + s * (sx + 0.02), y + s * (sy + 0.02)], fill=NAVY)
    # ringed planet, lower right
    px, py, pr = x + s * 0.74, y + s * 0.72, s * 0.13
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=GOLD, outline=INK,
              width=3)
    d.line([(px - pr * 1.6, py + pr * 0.5), (px + pr * 1.6, py - pr * 0.5)],
           fill=INK, width=4)
    # rocket body, tilted
    rx, ry = x + s * 0.42, y + s * 0.46
    d.polygon([(rx, ry - s * 0.30), (rx + s * 0.09, ry - s * 0.10),
               (rx + s * 0.09, ry + s * 0.16), (rx, ry + s * 0.24),
               (rx - s * 0.09, ry + s * 0.16), (rx - s * 0.09, ry - s * 0.10)],
              fill=(255, 255, 255), outline=INK)
    d.ellipse([rx - s * 0.035, ry - s * 0.20, rx + s * 0.035, ry - s * 0.13],
              fill=BLUE)
    # fins
    d.polygon([(rx - s * 0.09, ry + s * 0.10), (rx - s * 0.17, ry + s * 0.26),
               (rx - s * 0.09, ry + s * 0.24)], fill=RED)
    d.polygon([(rx + s * 0.09, ry + s * 0.10), (rx + s * 0.17, ry + s * 0.26),
               (rx + s * 0.09, ry + s * 0.24)], fill=RED)
    # flame
    d.polygon([(rx - s * 0.05, ry + s * 0.24), (rx + s * 0.05, ry + s * 0.24),
               (rx, ry + s * 0.38)], fill=ORANGE)


def pic_ball(d, x, y, s):
    """A football with a centre pentagon and seams."""
    d.rectangle([x, y, x + s, y + s], fill=TINT_GREEN, outline=CARD_LINE)
    cx, cy, r = x + s * 0.5, y + s * 0.52, s * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=INK, width=4)
    pr = r * 0.34
    pent = [(cx + pr * math.cos(math.radians(-90 + k * 72)),
             cy + pr * math.sin(math.radians(-90 + k * 72)))
            for k in range(5)]
    d.polygon(pent, fill=INK)
    for k in range(5):
        ang = math.radians(-90 + k * 72)
        vx = cx + pr * math.cos(ang)
        vy = cy + pr * math.sin(ang)
        ex = cx + r * 0.95 * math.cos(ang)
        ey = cy + r * 0.95 * math.sin(ang)
        d.line([(vx, vy), (ex, ey)], fill=INK, width=3)


# ------------------------------------------------------------------ layout
def card(d, x, y, w, h, kicker, head, body, pic, kicker_col):
    """One story card: pictogram left, kicker + headline + body right."""
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_LINE, width=2)
    ps = h - 24
    pic(d, x + 12, y + 12, ps)
    tx = x + 12 + ps + 14
    tw = w - (12 + ps + 14) - 14
    d.text((tx, y + 14), kicker, font=font(SANS_B, 17), fill=kicker_col)
    f_head = font(SERIF, 26)
    lines = wrap(d, head, f_head, tw)
    yy = block(d, tx, y + 38, lines, f_head, INK, 29)
    f_body = font(SANS, 19)
    blines = wrap(d, body, f_body, tw)
    room = y + h - 12 - (yy + 4)
    blines = blines[: max(1, room // 23)]
    block(d, tx, yy + 4, blines, f_body, MUTED, 23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.line([(M, M + 6), (W - M, M + 6)], fill=NAVY, width=4)
    f_title = font(SERIF, 62)
    title = "THURSDAY ECHO"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, M + 16), title, font=f_title, fill=NAVY)
    f_sub = font(SANS, 23)
    sub = "The world in one page  ·  Thursday 26 November 2026"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, M + 92), sub, font=f_sub, fill=MUTED)
    d.line([(M, M + 128), (W - M, M + 128)], fill=GOLD, width=3)

    y = M + 142
    cw = W - 2 * M

    # lead story: Ras Tanura claim
    lead_h = 210
    d.rectangle([M, y, M + cw, y + lead_h], fill=CARD, outline=CARD_LINE,
                width=2)
    pic_refinery(d, M + 12, y + 12, lead_h - 24)
    tx = M + 12 + (lead_h - 24) + 16
    tw = cw - (12 + (lead_h - 24) + 16) - 16
    d.text((tx, y + 16), "MIDDLE EAST  ·  LEAD", font=font(SANS_B, 18),
           fill=RED)
    head = "Houthis claim strike on Saudi Arabia's biggest refinery"
    hl = wrap(d, head, font(SERIF, 33), tw)
    yy = block(d, tx, y + 44, hl, font(SERIF, 33), INK, 37)
    body = ("Satellite images show smoke over Ras Tanura, which handles "
            "550,000 barrels a day. The Saudi-led coalition says four "
            "drones were shot down and no damage is confirmed.")
    bl = wrap(d, body, font(SANS, 20), tw)
    block(d, tx, yy + 6, bl, font(SANS, 20), MUTED, 25)
    y += lead_h + 12

    # two-by-two grid
    grid = [
        ("MARKETS", "Nasdaq dives 4% intraday in AI rout",
         "Pares the loss to 0.6% at the close; Nvidia falls 4%.",
         pic_chart, RED),
        ("UNITED STATES", "Tariffs proposed on 14 economies",
         "15% for the EU, Japan, Korea and Taiwan; up to 35% for Vietnam.",
         pic_container, NAVY),
        ("EGYPT", "Fuel tanker fire kills 31 near Cairo",
         "A tanker overturns on the Ring Road in Giza; 21 hurt.",
         pic_tanker, ORANGE),
        ("SPACE", "Pakistan's first astronaut boards Tiangong",
         "Muhammad Zeeshan Ali docks aboard Shenzhou-24.",
         pic_rocket, BLUE),
    ]
    gw = (cw - 12) // 2
    gh = 196
    for i, (kick, head, body, pic, col) in enumerate(grid):
        gx = M + (i % 2) * (gw + 12)
        gy = y + (i // 2) * (gh + 12)
        card(d, gx, gy, gw, gh, kick, head, body, pic, col)
    y += 2 * gh + 12 + 12

    # bottom strip: Champions League
    strip_h = 128
    d.rectangle([M, y, M + cw, y + strip_h], fill=CARD, outline=CARD_LINE,
                width=2)
    pic_ball(d, M + 12, y + 12, strip_h - 24)
    tx = M + 12 + (strip_h - 24) + 16
    tw = cw - (12 + (strip_h - 24) + 16) - 16
    d.text((tx, y + 14), "SPORT", font=font(SANS_B, 17), fill=GREEN)
    hl = wrap(d, "Liverpool cruise 3–0; PSG held, Bayern beaten",
              font(SERIF, 27), tw)
    yy = block(d, tx, y + 38, hl, font(SERIF, 27), INK, 30)
    bl = wrap(d, "Isak scores twice at Club Brugge; Roma end PSG's perfect "
              "record 2–2; Lille stun Bayern 2–1.",
              font(SANS, 20), tw)
    block(d, tx, yy + 4, bl, font(SANS, 20), MUTED, 24)
    y += strip_h + 12

    # footer
    f_foot = font(SANS, 16)
    foot = ("Six stories, each verified against at least two sources  ·  "
            "26 November 2026")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, y + 2), foot, font=f_foot, fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
