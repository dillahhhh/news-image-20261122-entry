#!/usr/bin/env python3
"""Render entry.png 1024x1024 — news-image-20261122 (Bahasa Indonesia).

Layout (total HARUS 1024 — di-assert di render):
header 58 + strip 42 + lead 118 + sekunder 142 + grid (610 + 6 gap)
+ footer 48 = 1024. Grid 4 kolom, baris [76, 93, 76, 76, 98, 98, 93]:
baris 76 = judul 1 baris + badan max 2 baris; baris 93/98 = badan
max 3 baris (judul 1 baris) atau 2 baris (judul 2 baris).
Font: DejaVu (fonts/), lantai badan 16px, judul reguler 20px,
sekunder 24px, lead 36px — TIDAK PERNAH dikecilkan.
1 kartu = 1 cerita, 34 cerita terverifikasi 22 Nov 2026 (lihat
stories.py). Meta seragam 4 segmen: dot grup + "N [TAG] · 22 NOV ·
SRC"; #25/#26 tambah segmen ke-5 berupa jam UTC terverifikasi.
Peta dot-matrix: darat diperluas vs versi 21 Nov (Turki barat,
Ukraina, Hejaz) agar ke-6 pin duduk DI ATAS dot darat — pin
Antalya/Dymer/Rabigh sebelumnya melayang di luar matriks.
Strip UTC: sumbu SAB 21 NOV 21:00 -> MIN 22 NOV 24:00 (27 jam).
Tick SABTU + PAGI adalah label hari/bagian-hari (bukan jam palsu);
3 tick lain berjam eksak terverifikasi (01:00, 04:00, 14:20).
"""
from PIL import Image, ImageDraw, ImageFont
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stories import (STORIES, PINS, GROUP_COLOR, GROUP_ORDER,
                     SRC_SHORT, TIME_IN_META)

W, H = 1024, 1024
OUT = "entry.png"

# ---- palet ----
PAPER = (250, 248, 243)
INK = (17, 24, 39)
MUTED = (107, 114, 128)
BORDER = (209, 213, 219)
WHITE = (255, 255, 255)
BLUE = (37, 99, 235)
RED = (220, 38, 38)
GREEN = (22, 163, 74)
AMBER = (217, 119, 6)

TAG_STYLE = {
    "RESMI": (GREEN, (220, 252, 231)),
    "DATA": (BLUE, (219, 234, 254)),
    "KLAIM": (AMBER, (254, 243, 199)),
}

# ---- geometri (px) — total 1024, di-assert di render() ----
HEADER_H = 58
STRIP_H = 42
LEAD_H = 118
SEC_H = 142
FOOTER_H = 48
GRID_ROWS = [76, 93, 76, 76, 98, 98, 93]
GRID_GAP = 1
LEAD_W = 644
SEC_W = 194
SEC_GAP = 5
GRID_W = 243
GRID_GAP_X = 2
MARGIN = 17

# ---- posisi y (dihitung, total harus 1024) ----
Y_HEADER = 0
Y_STRIP = Y_HEADER + HEADER_H            # 58
Y_LEAD = Y_STRIP + STRIP_H               # 100
Y_SEC = Y_LEAD + LEAD_H                  # 218
Y_GRID = Y_SEC + SEC_H                   # 360
Y_FOOTER = Y_GRID + sum(GRID_ROWS) + 6 * GRID_GAP   # 976
assert Y_FOOTER + FOOTER_H == 1024, Y_FOOTER

# ---- peta dot-matrix (baris 0..15, kolom 12..58 di-crop) ----
# Pemetaan: kolom c ~= lon 5c-177,5; baris r ~= lat 77,5-5r.
# Tambahan vs matriks 21 Nov (agar pin 22 Nov duduk di darat):
# (5,41,44) Ukraina; (6,42,44) Ukraina selatan; (7,41,43) Turki utara;
# (8,41,44) Turki; (9,43,44) Arabia utara; (10,43,44) Hejaz;
# (11,43,44) Hejaz selatan. Semua darat yg benar secara geografis.
LAND = [(0, 13, 14), (0, 31, 33), (1, 10, 12), (1, 17, 20), (1, 31, 38),
        (1, 50, 51), (2, 10, 15), (2, 17, 21), (2, 28, 35), (2, 50, 52),
        (3, 10, 13), (3, 16, 17), (3, 29, 33), (3, 48, 52),
        (4, 9, 11), (4, 14, 17), (4, 28, 31), (4, 46, 49),
        (5, 8, 10), (5, 15, 17), (5, 26, 31), (5, 41, 44), (5, 46, 47),
        (5, 49, 50), (6, 8, 9), (6, 14, 16), (6, 19, 22), (6, 26, 28),
        (6, 42, 44), (6, 48, 49), (7, 6, 9), (7, 15, 16), (7, 19, 22),
        (7, 25, 26), (7, 41, 45), (7, 48, 50), (8, 6, 8), (8, 14, 16),
        (8, 19, 22), (8, 26, 27), (8, 41, 46), (8, 54, 58),
        (9, 5, 7), (9, 15, 16), (9, 25, 26), (9, 43, 58),
        (10, 5, 7), (10, 15, 17), (10, 25, 27), (10, 43, 58),
        (11, 5, 6), (11, 15, 16), (11, 25, 28), (11, 43, 57),
        (12, 5, 6), (12, 25, 29), (12, 47, 57), (13, 25, 29),
        (13, 53, 57),
        (14, 26, 29), (15, 26, 28)]
LAND_DOT = (100, 116, 139)

# ---- font (DejaVu, satu-satunya di fonts/) ----
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

def f(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(BASE, name), size)

def tw(draw, text, font):
    return draw.textlength(text, font=font)

def wrap(text, font, width, draw):
    """Bungkus teks ke <=width; kembalikan list baris (kata utuh)."""
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(draw, t, font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

# ---- peta: crop lon -120..110, lat 0..80, K=1.45 ----
MAP_K = 1.45
MAP_LON0, MAP_LON1, MAP_LAT1 = -120, 110, 80   # lat bawah 0
MAP_W = int((MAP_LON1 - MAP_LON0) * MAP_K)     # 333
MAP_H = int(MAP_LAT1 * MAP_K)                  # 116

def map_xy(lon, lat, ox, oy):
    return (ox + (lon - MAP_LON0) * MAP_K, oy + (MAP_LAT1 - lat) * MAP_K)

def draw_map(draw, x, y, w, h):
    """Panel peta: dot-matrix darat + 6 pin (dot 16px, angka 12px bold)."""
    ox = x + (w - MAP_W) // 2
    oy = y + (h - MAP_H) // 2
    for row, c0, c1 in LAND:
        if row > 15:
            continue
        for c in range(max(c0, 12), min(c1, 58) + 1):
            cx = ox + (c - 12 + 0.5) * 5 * MAP_K
            cy = oy + (row + 0.5) * 5 * MAP_K
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=LAND_DOT)
    pts = []
    for num, dx, dy in PINS:
        s = next(t for t in STORIES if t[0] == num)
        px, py = map_xy(s[6], s[7], ox, oy)
        px, py = px + dx, py + dy
        pts.append((num, px, py, GROUP_COLOR[s[1]]))
    # cek tabrakan pin: halo putih 20px -> pusat min 20px.
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = ((pts[i][1] - pts[j][1]) ** 2 + (pts[i][2] - pts[j][2]) ** 2) ** 0.5
            assert d >= 20, f"pin #{pts[i][0]} dan #{pts[j][0]} tabrakan ({d:.1f}px)"
    for num, px, py, col in pts:
        draw.ellipse([px - 10, py - 10, px + 10, py + 10], fill=WHITE)
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col)
        if num == 1:
            draw.ellipse([px - 11, py - 11, px + 11, py + 11],
                         outline=RED, width=2)
        t = str(num)
        tf = f(12, True)
        draw.text((px - tw(draw, t, tf) / 2, py - 6), t, font=tf, fill=WHITE)
    return pts

# ---- strip UTC: sumbu SAB 21 NOV 21:00 -> MIN 22 NOV 24:00 UTC (27 jam) ----
# Tick 21:00 = SABTU (bukan Minggu). "SABTU" + "PAGI" adalah label
# hari/bagian-hari — BUKAN jam palsu. 01:00 (kick-off NWSL 20:00 ET),
# 04:00 (start GP Las Vegas) dan 14:20 (COP31 bubar, AP 09:20 EST)
# adalah jam eksak terverifikasi. Legenda menautkan tiap tick ke nomor
# kartu.
STRIP_EVENTS = [  # (label, jam_dari_Sab_21_00, warna)
    ("SABTU", 0.0, GREEN),
    ("01:00", 4.0, BLUE),
    ("04:00", 7.0, BLUE),
    ("PAGI", 10.0, GREEN),
    ("14:20", 17.33, RED),
]

def draw_strip(draw, y):
    x0, x1 = MARGIN, W - MARGIN
    title = "STRIP UTC — SAB 21 NOV 21:00 → MIN 22 NOV 24:00 (UTC)"
    draw.text((x0, y + 2), title, font=f(12, True), fill=INK)
    right = "WAKTU TERVERIFIKASI · 6 PIN = 6 CERITA TERATAS"
    draw.text((x1 - tw(draw, right, f(11, True)), y + 3), right,
              font=f(11, True), fill=MUTED)
    axis_y = y + 26
    draw.text((x0 + 6, y + 15), "SAB 21 NOV", font=f(10, True), fill=MUTED)
    draw.text((x0 + 125, y + 15), "MIN 22 NOV", font=f(10, True), fill=MUTED)
    draw.line([(x0, axis_y), (x1, axis_y)], fill=BORDER, width=2)
    for h in range(28):
        tx = x0 + (x1 - x0) * h / 27.0
        draw.line([(tx, axis_y - 3), (tx, axis_y + 3)], fill=BORDER, width=1)
    for label, h, col in STRIP_EVENTS:
        tx = x0 + (x1 - x0) * h / 27.0
        draw.line([(tx, axis_y - 7), (tx, axis_y)], fill=col, width=3)
        draw.ellipse([tx - 3, axis_y - 3, tx + 3, axis_y + 3], fill=col)
    legend = ("SABTU Pabrik permen → #8 · 01:00 NWSL → #26 · "
              "04:00 GP Las Vegas → #25 · PAGI Dymer → #2 · "
              "14:20 COP31 → #1")
    assert tw(draw, legend, f(11)) <= 990, "legenda strip terlalu lebar"
    draw.text((x0, y + 30), legend, font=f(11), fill=MUTED)

# ---- meta per kartu ----
# Format SERAGAM: dot grup 12px + "N [TAG] · 22 NOV · SRC" (4 segmen)
# di SEMUA kartu; #25/#26 membawa "· HH:MM" sebagai satu-satunya
# pengecualian segmen ke-5 (jam, bukan region).
META_FONT = 12
META_DOT = 11
META_GAP = 1
META_MARGIN = 2

def meta_segs(draw, s, inner_w):
    """Segmen meta (teks, warna). inner_w = anggaran visual teks."""
    num, group, title, body, tag, t, lon, lat, src = s
    assert src, f"kartu #{num} tanpa sumber"
    code = SRC_SHORT.get(src, src)
    fb = f(META_FONT, True)
    segs = [(str(num) + " ", fb, INK),
            ("[" + tag + "]", fb, TAG_STYLE[tag][0]),
            (" · 22 NOV", fb, INK)]
    if num in TIME_IN_META:
        assert t, f"kartu #{num} tanpa jam"
        segs.append((" · " + t, fb, INK))
    segs.append((" · " + code, fb, MUTED))
    return segs

def meta_text(segs):
    return "".join(t for t, _, _ in segs)

def draw_meta(draw, s, x, y, card_w):
    """Gambar meta; tegakkan: '22 NOV' + [TAG] + sumber ada, lebar muat."""
    inner_w = card_w - META_MARGIN - META_DOT - META_GAP
    segs = meta_segs(draw, s, inner_w)
    w = sum(tw(draw, t, fn) for t, fn, _ in segs)
    assert w <= inner_w, (f"meta #{s[0]} {w:.0f}px > {inner_w}px: "
                          f"{meta_text(segs)}")
    mt = meta_text(segs)
    assert "22 NOV" in mt and "[" in mt and "]" in mt, f"meta #{s[0]}: {mt}"
    assert SRC_SHORT.get(s[8], s[8]) in mt, f"meta #{s[0]} tanpa sumber: {mt}"
    col = GROUP_COLOR[s[1]]
    draw.ellipse([x, y + 1, x + META_DOT, y + 1 + META_DOT], fill=col)
    cx = x + META_DOT + META_GAP
    for t, fn, c in segs:
        draw.text((cx, y), t, font=fn, fill=c)
        cx += tw(draw, t, fn)
    return mt

def draw_header(draw):
    h1 = "BERITA DUNIA — 34 DATE-CHECKED STORIES, 7 TOPIK"
    assert tw(draw, h1, f(30, True)) <= 990, "h1 terlalu lebar"
    draw.text((MARGIN, 1), h1, font=f(30, True), fill=INK)
    h2 = ("MINGGU, 22 NOVEMBER 2026 · 6 LOKASI UTAMA · 4 JAM TERVERIFIKASI "
          "· SEMUA BERITA BERTANGGAL")
    assert tw(draw, h2, f(14)) <= 990, "h2 terlalu lebar"
    draw.text((MARGIN, 29), h2, font=f(14), fill=MUTED)
    # legenda tag SATU BARIS 11px, nama tag berwarna
    segs = [("RESMI", TAG_STYLE["RESMI"][0]),
            (" = dikonfirmasi resmi/dilaporkan · ", MUTED),
            ("KLAIM", TAG_STYLE["KLAIM"][0]),
            (" = klaim belum terverifikasi · ", MUTED),
            ("DATA", TAG_STYLE["DATA"][0]),
            (" = angka/statistik pasar", MUTED)]
    cx = MARGIN
    for t, c in segs:
        draw.text((cx, 43), t, font=f(11), fill=c)
        cx += tw(draw, t, f(11))
    assert cx - MARGIN <= 990, "legenda tag terlalu lebar"
    draw.line([(MARGIN, 57), (W - MARGIN, 57)], fill=BORDER, width=1)

def draw_lead(draw, x, y):
    """Lead #1 (COP31) + panel peta 6 pin di kanan."""
    s = STORIES[0]
    assert s[0] == 1
    draw.rectangle([x, y, x + LEAD_W - 1, y + LEAD_H - 1],
                   outline=BORDER, width=1, fill=WHITE)
    px = x + 12
    kicker = "LEAD · EROPA · [RESMI] · 22 NOV 2026 · GUARDIAN"
    assert tw(draw, kicker, f(12, True)) <= LEAD_W - 24, "kicker lead lebar"
    draw.text((px, y + 12), kicker, font=f(12, True), fill=RED)
    title = s[2]
    tf = f(36, True)
    assert tw(draw, title, tf) <= LEAD_W - 24, f"judul lead {tw(draw, title, tf):.0f}px"
    draw.text((px, y + 26), title, font=tf, fill=INK)
    body = s[3]
    bf = f(16)
    bl = wrap(body, bf, LEAD_W - 24, draw)
    assert len(bl) <= 2, f"body lead {len(bl)} baris"
    for i, ln in enumerate(bl):
        draw.text((px, y + 70 + i * 19), ln, font=bf, fill=INK)
    # panel peta (kanan lead)
    mx = x + LEAD_W + 6
    mw = W - MARGIN - mx
    draw.rectangle([mx, y, mx + mw - 1, y + LEAD_H - 1],
                   outline=BORDER, width=1, fill=WHITE)
    draw_map(draw, mx, y, mw, LEAD_H)

def draw_secondary(draw, x, y):
    """5 kartu sekunder #2-6 (w 194, judul 24px, isi 16px SEMUA).
    Badan max 4 baris, berakhir y+140 max (SEC_H 142)."""
    for i, s in enumerate(STORIES[1:6]):
        cx = x + i * (SEC_W + SEC_GAP)
        draw.rectangle([cx, y, cx + SEC_W - 1, y + SEC_H - 1],
                       outline=BORDER, width=1, fill=WHITE)
        draw_meta(draw, s, cx + META_MARGIN, y + 5, SEC_W)
        tf = f(24, True)
        tl = wrap(s[2], tf, SEC_W - 12, draw)
        assert len(tl) <= 2, f"judul sekunder #{s[0]} {len(tl)} baris"
        for j, ln in enumerate(tl):
            draw.text((cx + 6, y + 20 + j * 26), ln, font=tf, fill=INK)
        bf = f(16)
        bl = wrap(s[3], bf, SEC_W - 12, draw)
        assert len(bl) <= 4, f"body sekunder #{s[0]} {len(bl)} baris"
        assert 72 + len(bl) * 17 <= SEC_H - 2, \
            f"body sekunder #{s[0]} meluber ({len(bl)} baris)"
        for j, ln in enumerate(bl):
            draw.text((cx + 6, y + 72 + j * 17), ln, font=bf, fill=INK)

def draw_regular(draw, x, y):
    """28 kartu reguler #7-34, grid 4 kolom.
    Judul 20px (1-2 baris); badan 16px, leading 17px.
    Baris 93/98px: badan 3 baris (judul 1 baris) atau 2 baris (judul 2 baris).
    Baris 76px: badan max 2 baris, judul 1 baris."""
    for idx, s in enumerate(STORIES[6:]):
        r, c = divmod(idx, 4)
        cy = y + sum(GRID_ROWS[:r]) + r * GRID_GAP
        cx = x + c * (GRID_W + GRID_GAP_X)
        ch = GRID_ROWS[r]
        draw.rectangle([cx, cy, cx + GRID_W - 1, cy + ch - 1],
                       outline=BORDER, width=1, fill=WHITE)
        draw_meta(draw, s, cx + META_MARGIN, cy + 4, GRID_W)
        tf = f(20, True)
        tl = wrap(s[2], tf, GRID_W - 8, draw)
        tall = len(tl) == 2
        assert len(tl) <= 2, f"judul reguler #{s[0]} {len(tl)} baris"
        by = cy + 62 if tall else cy + 40
        for j, ln in enumerate(tl):
            draw.text((cx + 4, cy + 19 + j * 22), ln, font=tf, fill=INK)
        bf = f(16)
        bl = wrap(s[3], bf, GRID_W - 8, draw)
        max_body = 3 if (ch >= 93 and not tall) else 2
        assert len(bl) <= max_body, \
            f"body reguler #{s[0]} {len(bl)} baris (max {max_body})"
        assert by + len(bl) * 17 <= cy + ch - 2, \
            f"body reguler #{s[0]} meluber (y={by}, {len(bl)} baris, h={ch})"
        for j, ln in enumerate(bl):
            draw.text((cx + 4, by + j * 17), ln, font=bf, fill=INK)

def draw_footer(draw, y):
    # L1: metodologi + aturan tanggal, 11px.
    line1 = ("METODOLOGI — 34 cerita, 22 Nov 2026 (UTC); klaim ≠ fakta "
             "resmi; jam strip terverifikasi. Berita 22 Nov: peristiwa "
             "21 Nov yang dilaporkan 22 Nov.")
    assert tw(draw, line1, f(11)) <= 990, f"footer l1 {tw(draw, line1, f(11)):.0f}px"
    draw.text((MARGIN, y + 0), line1, font=f(11), fill=INK)
    # L2: legenda region 11px (dot 12px + nama penuh).
    lf = f(11)
    cx = MARGIN
    for g in GROUP_ORDER:
        draw.ellipse([cx, y + 12, cx + 11, y + 23], fill=GROUP_COLOR[g])
        cx += 13
        draw.text((cx, y + 12), g, font=lf, fill=INK)
        cx += tw(draw, g, lf) + 8
    assert cx - MARGIN <= 990, "legenda region terlalu lebar"
    # L3+L4: daftar sumber LENGKAP, nama penuh.
    src1 = ("SUMBER: Guardian, BBC, Al Jazeera, Le Monde, Japan Times, "
            "CNBC, MEE, CBC, DW, El País, NPR, RFI, CBS, France 24, "
            "Buenos Aires Times, Yonhap, Sky News, Euronews, Reuters")
    src2 = ("Data pasar: CNBC · Skor olahraga: CBC, Guardian, Al Jazeera "
            "· Waktu lomba: Formula 1, NWSL")
    assert tw(draw, src1, f(11)) <= 990, f"footer src1 {tw(draw, src1, f(11)):.0f}px"
    assert tw(draw, src2, f(11)) <= 990, f"footer src2 {tw(draw, src2, f(11)):.0f}px"
    draw.text((MARGIN, y + 24), src1, font=f(11), fill=INK)
    draw.text((MARGIN, y + 36), src2, font=f(11), fill=INK)

def render():
    assert len(STORIES) == 34, f"{len(STORIES)} cerita"
    assert [s[0] for s in STORIES] == list(range(1, 35)), "nomor kartu 1..34"
    for s in STORIES:
        assert s[4] in TAG_STYLE, f"tag #{s[0]} {s[4]}"
        assert s[8], f"kartu #{s[0]} tanpa sumber (34/34 wajib)"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_strip(d, Y_STRIP)
    draw_lead(d, MARGIN, Y_LEAD)
    draw_secondary(d, MARGIN, Y_SEC)
    draw_regular(d, MARGIN, Y_GRID)
    draw_footer(d, Y_FOOTER)
    img.save(OUT)
    import hashlib
    data = open(OUT, "rb").read()
    print(f"wrote {OUT} {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")
    print(f"size {img.size}, mode {img.mode}")

if __name__ == "__main__":
    render()
