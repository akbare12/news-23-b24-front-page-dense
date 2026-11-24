#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Monday 23 November 2026, dense front page.
1024x1024, PIL only. All 31 stories verified from the 23 Nov brief.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
NAVY_D = (16, 32, 56)
CREAM2 = (238, 232, 214)
GREY = (90, 90, 90)
LINE = (200, 192, 172)

REG = {
    "NORTH AMERICA": (29, 78, 216),
    "EUROPE": (180, 83, 9),
    "MIDDLE EAST": (124, 58, 237),
    "ASIA-PACIFIC": (15, 118, 110),
    "AFRICA": (146, 64, 14),
    "WORLD": (71, 85, 105),
}
CHIP = {"REPORTED": (21, 128, 61), "CLAIM": (180, 83, 9), "ONGOING": (29, 78, 216)}

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, f, fill, lh=None, spacing=0):
    if lh is None:
        lh = f.size + 3
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=f, fill=fill)
    return y + len(lines) * lh


def chip(d, x, y, label):
    f = font(F_SANS_B, 9)
    w = d.textlength(label, font=f) + 10
    c = CHIP[label]
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=c)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 24
CW = W - 2 * MX  # 976

# ---------- masthead ----------
d.rectangle([0, 6, W, 10], fill=RED)
f_mast = font(F_SERIF, 62)
d.text((MX, 12), "THE WORLD TODAY", font=f_mast, fill=INK)
f_cnt = font(F_SANS_B, 15)
d.text((W - MX - d.textlength("31 STORIES", font=f_cnt), 22), "31 STORIES", font=f_cnt, fill=INK)
d.text((W - MX - d.textlength("6 REGIONS", font=f_cnt), 42), "6 REGIONS", font=f_cnt, fill=INK)
f_date = font(F_SANS_B, 20)
d.text((MX, 82), "MONDAY 23 NOVEMBER 2026", font=f_date, fill=RED)
f_kick = font(F_SANS_B, 12)
kick = "AI ROUT  ·  AI RULES  ·  POWER SHIFT"
d.text((W - MX - d.textlength(kick, font=f_kick), 88), kick, font=f_kick, fill=GREY)

# ---------- number strip ----------
nums = [("-3.3%", "KOSPI"), ("5.3", "US-CHINA GAP"), ("11,762", "EBOLA CASES"),
        ("10T WON", "SEOUL FUND"), ("$450M", "SKUBAL DEAL"), ("$107.3B", "ANTHROPIC IPO")]
y0, y1 = 108, 150
cell = CW / 6
f_num = font(F_SANS_B, 25)
f_numl = font(F_SANS_B, 10)
d.rectangle([MX, y0, MX + CW, y1], outline=LINE, width=1)
for i, (n, lab) in enumerate(nums):
    x = MX + i * cell
    if i:
        d.line([x, y0 + 4, x, y1 - 4], fill=LINE, width=1)
    d.text((x + cell / 2 - d.textlength(n, font=f_num) / 2, y0 + 4), n, font=f_num, fill=RED)
    d.text((x + cell / 2 - d.textlength(lab, font=f_numl) / 2, y0 + 30), lab, font=f_numl, fill=INK)

# ---------- region bar ----------
regions = [("NORTH AMERICA", 8), ("EUROPE", 6), ("MIDDLE EAST", 6),
           ("ASIA-PACIFIC", 6), ("AFRICA", 3), ("WORLD", 2)]
y0, y1 = 154, 172
f_reg = font(F_SANS_B, 11)
x = MX
for name, n in regions:
    w = CW * n / 31
    d.rectangle([x, y0, x + w, y1], fill=REG[name])
    lab = "%s %d" % (name, n)
    d.text((x + w / 2 - d.textlength(lab, font=f_reg) / 2, y0 + 3), lab, font=f_reg, fill=(255, 255, 255))
    x += w

# ---------- UTC strip ----------
y0, y1 = 176, 194
d.rectangle([MX, y0, MX + CW, y1], fill=NAVY)
f_utc = font(F_SANS_B, 11)
d.text((MX + 6, y0 + 3), "THE DAY IN UTC", font=font(F_SANS_B, 11), fill=(255, 255, 255))
items = "~00:00 ASIA OPENS  ·  06:30 KOSPI -3.3%  ·  14:30 WALL ST +3%  ·  ~16:00 GUTERRES  ·  ~21:00 FBI HACK  (~ = APPROX.)"
f_utc = font(F_SANS_B, 11)
while d.textlength(items, font=f_utc) > CW - 130 and f_utc.size > 8:
    f_utc = font(F_SANS_B, f_utc.size - 1)
d.text((MX + 118, y0 + 3), items, font=f_utc, fill=(220, 228, 240))

# ---------- hero scenes ----------
HX, HY, HW, HH = MX, 200, 318, 132  # scene boxes, 3 across with 11px gaps
GAP = 11

def hero_scene_kospi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY_D)
    # skyline
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 14:
        bw = rnd.randint(12, 24)
        bh = rnd.randint(22, 62)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(24, 48, 84))
        for wy in range(y + h - bh + 5, y + h - 4, 9):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 204, 21))
        bx += bw + 4
    # falling chart
    pts = [(x + 12, y + 26), (x + 62, y + 34), (x + 112, y + 30), (x + 162, y + 52),
           (x + 212, y + 62), (x + 262, y + 78), (x + w - 12, y + 96)]
    d.line(pts, fill=(248, 113, 113), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255), outline=(248, 113, 113))
    d.text((x + 10, y + 6), "intraday -5.8%", font=font(F_SANS_B, 11), fill=(255, 255, 255))
    d.text((x + w - 92, y + 8), "-3.3%", font=font(F_SANS_B, 30), fill=(248, 113, 113))


def hero_scene_guterres(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY_D)
    # globe
    cx, cy, r = x + 62, y + 66, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 165, 250))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.ellipse([cx - 18, cy - r, cx + 18, cy + r], outline=(255, 255, 255), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=1)
    d.arc([cx - r, cy - 26, cx + r, cy + 26], 0, 360, fill=(255, 255, 255), width=1)
    # network: fixed nodes spread across the right half
    nodes = [(x + 150, y + 22), (x + 200, y + 40), (x + 252, y + 20), (x + 290, y + 44),
             (x + 168, y + 66), (x + 224, y + 80), (x + 276, y + 68), (x + 296, y + 100),
             (x + 188, y + 104), (x + 238, y + 112)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if abs(nodes[i][0] - nodes[j][0]) + abs(nodes[i][1] - nodes[j][1]) < 80:
                d.line([nodes[i], nodes[j]], fill=(147, 197, 253), width=1)
    for nx, ny in nodes:
        d.ellipse([nx - 4, ny - 4, nx + 4, ny + 4], fill=(250, 204, 21))
    # podium silhouette
    d.rectangle([x + w - 52, y + h - 34, x + w - 14, y + h], fill=(10, 20, 40))
    d.ellipse([x + w - 40, y + h - 62, x + w - 26, y + h - 48], fill=(10, 20, 40))
    d.rectangle([x + 8, y + 6, x + 118, y + 24], fill=(250, 204, 21))
    d.text((x + 14, y + 8), "150 DELEGATES", font=font(F_SANS_B, 11), fill=(17, 17, 17))


def hero_scene_power(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 10, y + 6), "ASIA POWER INDEX 2026", font=font(F_SANS_B, 13), fill=INK)
    f_b = font(F_SANS_B, 12)
    rows = [("US", 78.9, (29, 78, 216)), ("CHINA", 73.6, RED), ("INDIA 3rd", 40.5, (120, 120, 120))]
    yy = y + 30
    for lab, v, col in rows:
        d.text((x + 10, yy), lab, font=f_b, fill=INK)
        bw = (w - 130) * v / 85.0
        d.rectangle([x + 88, yy + 1, x + 88 + bw, yy + 13], fill=col)
        d.text((x + 88 + bw + 6, yy), "%.1f" % v, font=f_b, fill=INK)
        yy += 22
    d.text((x + 10, y + h - 24), "GAP 5.3", font=font(F_SANS_B, 15), fill=RED)
    d.text((x + 82, y + h - 22), "narrowest since 2018", font=font(F_SANS, 11), fill=GREY)


heroes = [
    (hero_scene_kospi, "#1 ASIA · MARKETS", "AI ROUT HITS ASIA",
     "Kospi closes 4,708.54, sheds 161 pts. Samsung -3.1%, SK Hynix -2.5%. AI sell-off spreads from Wall Street.",
     "Source: Yonhap · Korea JoongAng", "REPORTED"),
    (hero_scene_guterres, "#2 WORLD · UNITED NATIONS", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "Source: UN News · Reuters", "REPORTED"),
    (hero_scene_power, "#3 ASIA-PACIFIC · POWER", "US LEAD OVER CHINA AT RECORD LOW",
     "Gap 5.3 narrowest since 2018. US diplomatic influence -6 to 76.7. India third at 40.5.",
     "Source: Lowy Institute", "REPORTED"),
]
f_hkick = font(F_SANS_B, 10)
f_htitle = font(F_SANS_B, 16)
f_hbody = font(F_SANS, 11)
f_hsrc = font(F_SANS, 9)
for i, (scene, kick, title, body, src, clab) in enumerate(heroes):
    x = HX + i * (HW + GAP)
    scene(x, HY, HW, HH)
    ty = HY + HH + 5
    d.text((x, ty), kick, font=f_hkick, fill=RED)
    ty += 14
    for ln in wrap(d, title, f_htitle, HW):
        d.text((x, ty), ln, font=f_htitle, fill=INK)
        ty += 19
    for ln in wrap(d, body, f_hbody, HW):
        d.text((x, ty), ln, font=f_hbody, fill=INK)
        ty += 14
    d.text((x, ty + 2), src, font=f_hsrc, fill=GREY)
    chip(d, x + HW - 74, ty, clab)

# ---------- 10 small cards ----------
cards = [
    (4, "SPORT · US", "NORTH AMERICA", "Skubal signs $450M Mets deal",
     "Two-time Cy Young winner, nine years — a record for a pitcher.", "ESPN", "REPORTED"),
    (5, "TECH · US", "NORTH AMERICA", "Anthropic IPO: $107.3B, largest ever",
     "Claude maker raised at $83 a share; debut close $97.17.", "Bloomberg", "REPORTED"),
    (6, "EUROPE · WAR", "EUROPE", "Poland: 3 Russian missiles crossed airspace",
     "Kyiv: three Kh-101 entered Poland Friday; Tusk: provocation.", "AP", "CLAIM"),
    (7, "EUROPE · SECURITY", "EUROPE", "Intel warns of Russian nuclear satellite",
     "Moscow built a satellite to carry a warhead; launch next month.", "Bloomberg", "CLAIM"),
    (8, "EUROPE · ECONOMY", "EUROPE", "Paris: 100+ back 2% billionaire tax",
     "Economists and unions rally behind France's 2% wealth tax.", "AFP", "REPORTED"),
    (9, "EUROPE · UK", "EUROPE", "Manchester: 12,000 cleared after scare",
     "Substance scare empties arena district; no casualties reported.", "AP", "REPORTED"),
    (10, "EUROPE · WAR", "EUROPE", "Zelenskyy: 165 Russian missiles in a week",
     "Moscow fired 165 missiles in a week as the US delays Patriots.", "Kyiv", "CLAIM"),
    (11, "WORLD · CLIMATE", "WORLD", "COP31: the day after",
     "194 nations reject the pact; Guterres 'profoundly frustrated'.", "CNN", "REPORTED"),
    (12, "AFRICA · LIBYA", "AFRICA", "Benghazi: UN demands probe of port attacks",
     "Drones hit two Russian ships; UN calls for an investigation.", "UN News", "CLAIM"),
    (13, "MIDDLE EAST · ISRAEL", "MIDDLE EAST", "Israel unity talks resume",
     "Likud and Gantz's Yesh Atid return to the table after Sunday's stall.", "Reuters", "ONGOING"),
]
CGAP = 8
CWID = (CW - 4 * CGAP) // 5  # 188
CHT = 100
CY0 = 452
f_ckick = font(F_SANS_B, 9)
f_ctitle = font(F_SANS_B, 12)
f_cbody = font(F_SANS, 10)
f_csrc = font(F_SANS, 8)
for idx, (num, kick, reg, title, body, src, clab) in enumerate(cards):
    r, c = divmod(idx, 5)
    x = MX + c * (CWID + CGAP)
    y = CY0 + r * (CHT + CGAP)
    d.rectangle([x, y, x + CWID, y + CHT], fill=(255, 255, 255), outline=LINE, width=1)
    # mini illustration strip: region colour with simple motif
    d.rectangle([x, y, x + CWID, y + 18], fill=REG[reg])
    d.text((x + 5, y + 3), "#%d" % num, font=f_ckick, fill=(255, 255, 255))
    d.text((x + 30, y + 3), kick, font=f_ckick, fill=(255, 255, 255))
    ty = y + 22
    for ln in wrap(d, title, f_ctitle, CWID - 10)[:2]:
        d.text((x + 5, ty), ln, font=f_ctitle, fill=INK)
        ty += 15
    for ln in wrap(d, body, f_cbody, CWID - 10)[:2]:
        d.text((x + 5, ty), ln, font=f_cbody, fill=INK)
        ty += 13
    d.text((x + 5, y + CHT - 16), src, font=f_csrc, fill=GREY)
    chip(d, x + CWID - 79, y + CHT - 18, clab)

# ---------- map + ALSO ----------
MY0, MY1 = 668, 836
MAPX, MAPW = MX, 560
MAPY, MAPH = 686, 150
f_mapt = font(F_SANS_B, 13)
d.text((MX, MY0), "THE WORLD — WHERE IT HAPPENED", font=f_mapt, fill=RED)
d.text((MX, MY0 + 16), "PIN = STORY NUMBER", font=font(F_SANS_B, 9), fill=GREY)
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], fill=(214, 228, 240))
# graticule
for gx in range(MAPX, MAPX + MAPW + 1, 56):
    d.line([gx, MAPY, gx, MAPY + MAPH], fill=(190, 205, 220), width=1)
for gy in range(MAPY, MAPY + MAPH + 1, 30):
    d.line([MAPX, gy, MAPX + MAPW, gy], fill=(190, 205, 220), width=1)

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-85, 70), (-75, 62), (-60, 55), (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 20), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-50, -30), (-60, -38), (-70, -50), (-75, -40), (-70, -20), (-80, -5)],
    [(-10, 36), (-9, 43), (0, 48), (-2, 50), (5, 53), (8, 57), (18, 56), (21, 55), (28, 60), (30, 70), (40, 68), (45, 60), (40, 50), (35, 45), (28, 41), (23, 36), (19, 40), (12, 44), (3, 43)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -25), (12, -10), (9, 4), (-8, 5), (-15, 11)],
    [(40, 68), (60, 70), (90, 75), (120, 73), (150, 70), (170, 66), (178, 65), (160, 60), (140, 45), (130, 42), (127, 38), (122, 30), (115, 22), (108, 12), (100, 8), (97, 16), (90, 22), (85, 20), (80, 8), (76, 10), (72, 20), (66, 25), (60, 25), (55, 26), (50, 29), (48, 30), (44, 30), (40, 36), (36, 36), (35, 42), (40, 50), (45, 55)],
    [(113, -22), (122, -14), (132, -12), (142, -11), (150, -22), (153, -27), (150, -37), (140, -38), (130, -32), (120, -34), (113, -30)],
]


def ll(lon, lat):
    return (MAPX + (lon + 180) / 360.0 * MAPW, MAPY + (75 - lat) / 135.0 * MAPH)


for poly in CONTINENTS:
    pts = [ll(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=(222, 205, 170), outline=(160, 145, 120))

CLAIMS = {6, 7, 10, 12}
PINS = [
    (1, 127, 37, 0, 0), (2, -59, 13, 0, 0), (3, 150, -45, 0, 0),
    (4, -74, 40, 0, 0), (5, -122, 37, 0, 0), (6, 21, 52, 6, -4),
    (7, 37, 55, 8, -6), (8, 2, 48, 4, 8), (9, -2, 53, -8, -6),
    (10, 30, 50, 4, 6), (11, 30, 36, 0, 0), (12, 20, 32, 0, 0),
    (13, 35, 31, 0, 0), (14, 34, 31, 10, 10), (15, 35, 32, -12, -6),
    (16, 51, 35, 0, 0), (17, 35, 33, 12, -8), (18, 50, 26, 0, 0),
    (19, 32, 15, 0, 0), (20, 25, -2, 0, 0), (21, 90, 23, 0, 0),
    (22, 127, 37, 12, -10), (23, 127, 37, -12, 10), (24, 116, 39, 0, 0),
    (25, 127, 37, 14, 8), (26, -77, 38, 0, 0), (27, -77, 38, 12, -8),
    (28, -77, 38, -12, 8), (29, -74, 40, 12, -10), (30, -105, 39, 0, 0),
    (31, -121, 38, 0, 0),
]
f_pin = font(F_SANS_B, 8)
for num, lon, lat, dx, dy in PINS:
    px, py = ll(lon, lat)
    px += dx
    py += dy
    col = (180, 83, 9) if num in CLAIMS else ((29, 78, 216) if num == 13 else RED)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col, outline=(255, 255, 255), width=1)
    t = str(num)
    d.text((px - d.textlength(t, font=f_pin) / 2, py - 5), t, font=f_pin, fill=(255, 255, 255))
d.text((MAPX + 4, MAPY + MAPH - 14), "N ↑", font=font(F_SANS_B, 9), fill=GREY)

# ALSO list, two sub-columns
AX = MX + 576
AW = W - MX - AX  # 400
f_at = font(F_SANS_B, 13)
d.text((AX, MY0), "ALSO ON MONDAY — 18 MORE STORIES", font=f_at, fill=RED)
f_ah = font(F_SANS_B, 10)
f_ai = font(F_SANS, 10)
ALSO_L = [("MIDDLE EAST", (124, 58, 237), ["14 Gaza: two killed in strike", "15 West Bank: settler attacks",
          "16 Iran war: no deal in sight", "17 Lebanon: 264 kg explosives", "18 Bahrain: plant hit, 2 hurt"]),
          ("AFRICA", (146, 64, 14), ["19 Sudan: drones downed, Khartoum", "20 DRC: fighting traps Ebola teams"])]
ALSO_R = [("ASIA-PACIFIC", (15, 118, 110), ["21 Bangladesh: Hasina to be jailed", "22 Seoul minister quits, AI chaos",
          "23 SK Telecom -7.3%, hype cools", "24 China eases margin rules", "25 Seoul readies 10T-won fund"]),
          ("NORTH AMERICA", (29, 78, 216), ["26 Bessent demands Nvidia answers", "27 FBI probes police database hack",
          "28 Trump: Iran strikes may resume", "29 US futures jump 3% holiday week",
          "30 Tom Jackson dies at 75", "31 States sue SpaceX over AI claims"])]
for col_i, groups in enumerate([ALSO_L, ALSO_R]):
    cx = AX + col_i * (AW // 2)
    cy = MY0 + 20
    for gname, gcol, items in groups:
        d.text((cx, cy), gname, font=f_ah, fill=gcol)
        cy += 13
        for it in items:
            d.text((cx, cy), it, font=f_ai, fill=INK)
            cy += 12

# ---------- DATE CHECK ----------
DY0, DY1 = 844, 922
d.rectangle([MX, DY0, MX + CW, DY1], outline=RED, width=2)
f_dc = font(F_SANS_B, 12)
f_dcb = font(F_SANS, 11)
d.text((MX + 8, DY0 + 6), "DATE CHECK", font=f_dc, fill=RED)
d.text((MX + 96, DY0 + 7), "Every story above happened or was first reported on Monday 23 November 2026.",
       font=f_dcb, fill=INK)
d.text((W - MX - 8 - d.textlength("WIRES READ UP TO 23:00 UTC", font=f_dcb), DY0 + 7),
       "WIRES READ UP TO 23:00 UTC", font=f_dcb, fill=RED)
lo = "LEFT OUT (not 23 Nov): Democrats reach 258 (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) ·"
lo2 = "EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)."
d.text((MX + 8, DY0 + 26), lo, font=f_dcb, fill=INK)
d.text((MX + 8, DY0 + 41), lo2, font=f_dcb, fill=INK)
d.text((MX + 8, DY0 + 58), "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff.",
       font=f_dcb, fill=INK)

# ---------- footer ----------
f_ft = font(F_SANS, 9)
d.text((MX, 930), "SOURCES: AP · Reuters · Bloomberg · AFP · CNN · ESPN · UN News · WHO · Kyiv · Lowy Institute · Korea JoongAng · Morningstar",
       font=f_ft, fill=GREY)
d.text((MX, 944), "CONFIRMED = 2+ outlets · REPORTED = carried by a wire · CLAIM = one side alleges · ONGOING = developing.  Red pin = reported · Amber pin = claim (unverified).",
       font=f_ft, fill=GREY)
d.text((MX, 962), "THE WORLD TODAY · 23 NOV 2026", font=font(F_SANS_B, 9), fill=INK)
d.text((W - MX - d.textlength("Scenes are drawn illustrations, not photographs.", font=f_ft), 962),
       "Scenes are drawn illustrations, not photographs.", font=f_ft, fill=GREY)

img.save("entry.png")
print("saved entry.png", img.size)
