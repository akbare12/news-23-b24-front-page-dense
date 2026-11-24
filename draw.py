#!/usr/bin/env python3
"""news-23 b24 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories: 3 heroes + 10 cards + 18 ALSO. 1024x1024 PNG, < 1 MiB."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 232)
INK = (20, 20, 20)
RED = (163, 18, 18)
GOLD = (201, 162, 39)
NAVY = (30, 58, 95)
TEAL = (14, 122, 109)
GREEN = (143, 174, 107)
CREAM = (247, 243, 232)
GREY = (90, 90, 90)
LINE = (200, 192, 172)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, maxw, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(text, fnt, maxw, draw):
    if draw.textlength(text, font=fnt) <= maxw:
        return text
    while len(text) > 3 and draw.textlength(text + "\u2026", font=fnt) > maxw:
        text = text[:-1]
    return text + "\u2026"


def chip(draw, x, y, label, color):
    f = font(F_SANSB, 8)
    w = int(draw.textlength(label, font=f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 12], radius=2, fill=color)
    draw.text((x + 5, y + 1), label, font=f, fill=(255, 255, 255))
    return w


def draw():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 60], fill=(12, 12, 12))
    f_mast = font(F_SERIF, 40)
    d.text((12, 8), "THE WORLD TODAY", font=f_mast, fill=(255, 255, 255))
    f_date = font(F_SANSB, 20)
    dt = "MONDAY  23 NOVEMBER 2026"
    d.text((W - 12 - d.textlength(dt, font=f_date), 18), dt, font=f_date, fill=GOLD)

    # ---------- kicker ----------
    f_kick = font(F_SANSB, 13)
    kick = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
    d.text(((W - d.textlength(kick, font=f_kick)) / 2, 64), kick, font=f_kick, fill=RED)

    # ---------- number strip (5 cols x 2 rows) ----------
    nums = [
        ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
        ("11,762", "EBOLA CASES, DRC", (90, 90, 20)), ("10T won", "SEOUL STABILISATION FUND", (120, 80, 10)),
        ("2%", "BILLIONAIRE TAX IN PARIS", (0, 110, 60)),
        ("$450M", "SKUBAL DEAL", (140, 30, 140)), ("165", "RUSSIAN MISSILES IN A WEEK", RED),
        ("12,000", "CLEARED IN MANCHESTER", NAVY), ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", (120, 80, 10)),
        ("$107.3B", "ANTHROPIC IPO \u2014 LARGEST EVER", (140, 30, 140)),
    ]
    f_num = font(F_SANSB, 22)
    f_numlab = font(F_SANSB, 9)
    for i, (val, lab, col) in enumerate(nums):
        col_i, row_i = i % 5, i // 5
        x = 8 + col_i * 202
        y = 84 + row_i * 33
        d.text((x, y), val, font=f_num, fill=col)
        d.text((x, y + 23), fit(lab, f_numlab, 196, d), font=f_numlab, fill=INK)

    # ---------- region bar ----------
    regions = [("ASIA-PACIFIC 7", (0, 110, 60)), ("AMERICAS 8", NAVY),
               ("MIDDLE EAST 6", (150, 120, 20)), ("EUROPE 5", TEAL),
               ("AFRICA 3", (120, 40, 120)), ("WORLD 2", (100, 100, 100))]
    f_reg = font(F_SANSB, 11)
    seg_w = 1008 // 6
    for i, (lab, col) in enumerate(regions):
        x = 8 + i * seg_w
        d.rectangle([x, 152, x + seg_w - 2, 174], fill=col)
        d.text((x + (seg_w - 2 - d.textlength(lab, font=f_reg)) / 2, 157), lab, font=f_reg, fill=(255, 255, 255))

    # ---------- UTC strip ----------
    d.rectangle([0, 176, W, 196], fill=(15, 30, 55))
    f_utc = font(F_SANS, 10)
    utc = "~00:00 Kospi dives  \u00b7  ~06:30 Guterres opens  \u00b7  ~09:00 Power Index  \u00b7  ~12:00 Paris 2% tax  \u00b7  ~15:00 Kyiv missiles  \u00b7  ~18:00 Anthropic $97.17  \u00b7  ~ APPROX"
    d.text(((W - d.textlength(utc, font=f_utc)) / 2, 181), utc, font=f_utc, fill=(200, 215, 235))

    # ---------- hero scenes ----------
    hx = [8, 348, 688]
    hw = 328
    sy, sh = 198, 150

    # scene 1: Kospi chart over skyline
    x0 = hx[0]
    d.rectangle([x0, sy, x0 + hw, sy + sh], fill=(22, 35, 63))
    import random
    random.seed(23)
    for bx in range(x0 + 6, x0 + hw - 6, 22):
        bh = random.randint(28, 62)
        d.rectangle([bx, sy + sh - 26 - bh, bx + 18, sy + sh - 26], fill=(8, 16, 34))
        for wy in range(sy + sh - 22 - bh, sy + sh - 28, 8):
            for wx in (bx + 3, bx + 10):
                if random.random() < 0.6:
                    d.rectangle([wx, wy, wx + 4, wy + 4], fill=(255, 210, 90))
    pts = [(x0 + 12, sy + 62), (x0 + 60, sy + 48), (x0 + 110, sy + 58),
           (x0 + 160, sy + 44), (x0 + 210, sy + 66), (x0 + 260, sy + 78), (x0 + 316, sy + 96)]
    d.line(pts, fill=(230, 60, 50), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 210, 90), outline=(230, 60, 50))
    d.text((x0 + 10, sy + 6), "-3.3%", font=font(F_SANSB, 30), fill=(230, 60, 50))
    d.rectangle([x0, sy + sh - 24, x0 + hw, sy + sh], fill=(0, 0, 0))
    d.text((x0 + 10, sy + sh - 21), "KOSPI  4,708.54  \u00b7  -161 PTS", font=font(F_SANSB, 12), fill=(255, 255, 255))

    # scene 2: Guterres globe + flags
    x0 = hx[1]
    d.rectangle([x0, sy, x0 + hw, sy + sh], fill=TEAL)
    d.ellipse([x0 + hw - 92, sy + 18, x0 + hw - 12, sy + 98], fill=(191, 227, 216))
    d.ellipse([x0 + hw - 78, sy + 34, x0 + hw - 58, sy + 54], fill=(60, 160, 110))
    d.ellipse([x0 + hw - 56, sy + 62, x0 + hw - 34, sy + 84], fill=(60, 160, 110))
    d.ellipse([x0 + hw - 88, sy + 66, x0 + hw - 70, sy + 82], fill=(60, 160, 110))
    for fx, fc in [(x0 + 22, RED), (x0 + 62, NAVY), (x0 + 102, GOLD)]:
        d.line([fx, sy + 96, fx, sy + 138], fill=(255, 255, 255), width=2)
        d.polygon([(fx, sy + 96), (fx + 26, sy + 104), (fx, sy + 112)], fill=fc)
    d.text((x0 + 10, sy + 8), "150 DELEGATES", font=font(F_SANSB, 26), fill=(255, 220, 80))
    d.text((x0 + 10, sy + 40), "BACK A RISK", font=font(F_SANSB, 22), fill=(255, 255, 255))
    d.text((x0 + 10, sy + 66), "FRAMEWORK", font=font(F_SANSB, 22), fill=(255, 255, 255))
    d.rectangle([x0, sy + sh - 24, x0 + hw, sy + sh], fill=(0, 0, 0))
    d.text((x0 + 10, sy + sh - 21), "UN  \u00b7  BRIDGETOWN", font=font(F_SANSB, 12), fill=(255, 255, 255))

    # scene 3: power-index bars
    x0 = hx[2]
    d.rectangle([x0, sy, x0 + hw, sy + sh], fill=(255, 255, 255), outline=(150, 150, 150))
    d.text((x0 + 10, sy + 6), "NARROWEST SINCE 2018", font=font(F_SANSB, 11), fill=INK)
    d.text((x0 + hw - 78, sy + 6), "GAP 5.3", font=font(F_SANSB, 11), fill=GOLD)
    bars = [("US", 78.9, NAVY), ("CHINA", 73.6, RED), ("INDIA", 40.5, GOLD)]
    base = sy + sh - 30
    for i, (lab, val, col) in enumerate(bars):
        bx = x0 + 22 + i * 104
        bh = int(val * 0.95)
        d.rectangle([bx, base - bh, bx + 62, base], fill=col)
        d.text((bx + 8, base - bh - 18), str(val), font=font(F_SANSB, 14), fill=col)
        d.text((bx + 8, base + 4), lab, font=font(F_SANSB, 11), fill=INK)

    # hero headlines / bodies / sources
    heroes = [
        ("1", "AI ROUT HITS ASIA",
         "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5.",
         "KOREA EXCHANGE", "REPORTED"),
        ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
         "UNITED NATIONS", "REPORTED"),
        ("3", "US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
         "LOWY INSTITUTE", "REPORTED"),
    ]
    f_hhead = font(F_SANSB, 15)
    f_hbody = font(F_SANS, 11)
    f_hsrc = font(F_SANS, 9)
    for i, (num, head, body, src, ch) in enumerate(heroes):
        x0 = hx[i]
        lines = wrap(head, f_hhead, hw - 30, d)[:2]
        y = 350
        d.ellipse([x0, y + 2, x0 + 18, y + 20], fill=RED)
        d.text((x0 + 6, y + 3), num, font=font(F_SANSB, 11), fill=(255, 255, 255))
        for ln in lines:
            d.text((x0 + 24, y), ln, font=f_hhead, fill=INK)
            y += 18
        blines = wrap(body, f_hbody, hw - 6, d)[:2]
        y = 390
        for ln in blines:
            d.text((x0, y), ln, font=f_hbody, fill=INK)
            y += 13
        d.text((x0, 418), src, font=f_hsrc, fill=GREY)
        chip(d, x0 + hw - 62, 418, ch, NAVY)

    # ---------- MORE OF THE DAY ----------
    d.text((8, 436), "MORE OF THE DAY  \u2014  10 STORIES", font=font(F_SANSB, 14), fill=INK)
    d.line([8, 454, W - 8, 454], fill=INK, width=2)

    cards = [
        ("AMERICAS", (140, 30, 30), "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", "REPORTED", NAVY),
        ("FBI", (110, 40, 140), "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", "REPORTED", NAVY),
        ("WHITE HOUSE", (150, 120, 20), "TRUMP: IRAN STRIKES MAY RESUME", "Strikes could resume in the New Year.", "Reuters", "REPORTED", NAVY),
        ("MARKETS", TEAL, "US FUTURES JUMP 3%", "Holiday rally lifts Nasdaq futures 3%.", "Bloomberg", "REPORTED", NAVY),
        ("SPORT", (0, 110, 60), "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever for a pitcher.", "AP", "REPORTED", NAVY),
        ("SPORT", (0, 110, 60), "TOM JACKSON DIES AT 75", "Broncos LB turned ESPN voice dies.", "ESPN", "REPORTED", NAVY),
        ("LEGAL", (110, 40, 140), "STATES SUE SPACEX", "Ten states challenge AI safety claims.", "AP", "REPORTED", NAVY),
        ("TECH", NAVY, "ANTHROPIC IPO: $107.3B", "Raises at $83; debut closes $97.17.", "WSJ", "REPORTED", NAVY),
        ("EUROPE", (140, 30, 30), "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed airspace.", "AP", "CLAIM", RED),
        ("SPACE", (100, 100, 100), "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite built to carry a nuke.", "Reuters", "CLAIM", RED),
    ]
    f_ccat = font(F_SANSB, 9)
    f_chead = font(F_SANSB, 11)
    f_cbody = font(F_SANS, 8)
    f_csrc = font(F_SANS, 8)
    cw, chh, gap = 198, 70, 4
    for i, (cat, ccol, head, body, src, ch, chcol) in enumerate(cards):
        cx = 8 + (i % 5) * (cw + gap)
        cy = 458 + (i // 5) * (chh + gap)
        d.rectangle([cx, cy, cx + cw, cy + chh], fill=(255, 255, 255), outline=(180, 175, 160))
        d.rectangle([cx, cy, cx + cw, cy + 14], fill=ccol)
        d.text((cx + 4, cy + 2), cat, font=f_ccat, fill=(255, 255, 255))
        d.text((cx + cw - 14, cy + 2), str(i + 4), font=f_ccat, fill=(255, 255, 255))
        hlines = wrap(head, f_chead, cw - 8, d)[:2]
        y = cy + 17
        for ln in hlines:
            d.text((cx + 4, y), ln, font=f_chead, fill=INK)
            y += 12
        nbody = 1 if len(hlines) == 2 else 2
        blines = wrap(body, f_cbody, cw - 8, d)[:nbody]
        for ln in blines:
            d.text((cx + 4, y), ln, font=f_cbody, fill=(60, 60, 60))
            y += 10
        d.text((cx + 4, cy + chh - 12), src, font=f_csrc, fill=GREY)
        chip(d, cx + cw - 62, cy + chh - 13, ch, chcol)

    # ---------- map + ALSO ----------
    d.text((8, 606), "WHERE IT HAPPENED", font=font(F_SANSB, 14), fill=INK)
    d.line([8, 624, 472, 624], fill=INK, width=2)
    d.text((480, 606), "ALSO ON MONDAY", font=font(F_SANSB, 14), fill=INK)
    d.line([480, 624, W - 8, 624], fill=INK, width=2)

    mx0, my0, mw, mh = 8, 628, 464, 240
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=(207, 227, 238))
    for gx in range(mx0, mx0 + mw, 24):
        d.line([gx, my0, gx, my0 + mh], fill=(190, 212, 226))
    for gy in range(my0, my0 + mh, 24):
        d.line([mx0, gy, mx0 + mw, gy], fill=(190, 212, 226))
    land = [
        [(28, 668), (98, 648), (158, 658), (178, 688), (158, 728), (118, 748), (68, 738), (33, 708)],
        [(188, 658), (218, 653), (223, 673), (198, 680)],
        [(118, 768), (158, 763), (173, 798), (148, 838), (123, 808)],
        [(248, 658), (298, 648), (308, 673), (278, 693), (248, 683)],
        [(258, 708), (308, 703), (328, 738), (308, 788), (273, 778), (253, 738)],
        [(318, 648), (448, 643), (468, 678), (438, 728), (388, 748), (338, 728), (318, 688)],
        [(408, 798), (458, 793), (463, 818), (418, 823)],
    ]
    for poly in land:
        d.polygon(poly, fill=GREEN)
    pins = [(425, 680), (158, 753), (418, 668), (103, 708), (123, 693),
            (338, 708), (83, 698), (53, 708), (78, 723), (93, 738),
            (273, 663), (298, 676), (318, 658)]
    f_pin = font(F_SANSB, 9)
    for i, (px, py) in enumerate(pins, start=1):
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=2)
        lab = str(i)
        d.text((px - d.textlength(lab, font=f_pin) / 2, py - 6), lab, font=f_pin, fill=(255, 255, 255))

    also = [
        "Paris: 100+ back 2% billionaire tax", "Manchester: 12,000 cleared",
        "Zelenskyy: 165 missiles in a week", "COP31: the day after pact rejected",
        "Benghazi: UN demands port probe", "Israel unity talks resume",
        "Gaza: two killed in Israeli strike", "West Bank settler attacks",
        "Iran war: no deal in sight", "Lebanon seizes 264 kg explosives",
        "Bahrain: strike hits plant, 2 hurt", "Sudan: defences down drones",
        "DRC: fighting traps Ebola teams", "Bangladesh: Hasina jailed if she returns",
        "Seoul minister quits in exam row", "SK Telecom -7.3% as hype cools",
        "China eases margin rules", "Seoul readies 10T-won fund",
    ]
    f_also = font(F_SANS, 10)
    y = 630
    for i, item in enumerate(also, start=14):
        d.text((480, y), f"{i}. {item}", font=f_also, fill=INK)
        y += 13

    # pin legend (wrapped to map width)
    f_leg = font(F_SANS, 8)
    legend = ("Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Washington \u00b7 "
              "5 New York \u00b7 6 Tehran \u00b7 7 Chicago \u00b7 8 San Francisco \u00b7 9 Denver \u00b7 "
              "10 Austin \u00b7 11 Warsaw \u00b7 12 Kyiv \u00b7 13 Moscow")
    y = 872
    for ln in wrap(legend, f_leg, mw, d):
        d.text((mx0, y), ln, font=f_leg, fill=GREY)
        y += 11

    # ---------- DATE CHECK ----------
    d.rectangle([8, 900, W - 8, 962], outline=RED, width=2)
    d.text((16, 906), "DATE CHECK", font=font(F_SANSB, 13), fill=RED)
    d.text((140, 907), "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY",
           font=font(F_SANSB, 10), fill=INK)
    f_dc = font(F_SANS, 10)
    left = ("LEFT OUT \u2014 NOT 23 NOV: Democrats reach 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 "
            "El Chapo Isidro captured (22 Nov) \u00b7 EU\u2013Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 "
            "ICJ Myanmar ruling (19 Nov)")
    y = 924
    for ln in wrap(left, f_dc, 992, d):
        d.text((16, y), ln, font=f_dc, fill=INK)
        y += 12
    d.text((16, y), "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
           font=f_dc, fill=INK)

    # ---------- footer ----------
    f_foot = font(F_SANS, 9)
    d.text((8, 968), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
           font=f_foot, fill=GREY)
    d.text((8, 980), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing",
           font=f_foot, fill=GREY)

    # ---------- bottom bar ----------
    d.rectangle([0, 992, W, H], fill=(12, 12, 12))
    f_bot = font(F_SANSB, 10)
    bot = "Scenes are drawn illustrations, not photographs.  \u00b7  THE WORLD TODAY \u2014 Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
    d.text(((W - d.textlength(bot, font=f_bot)) / 2, 1004), bot, font=f_bot, fill=GOLD)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    draw()
