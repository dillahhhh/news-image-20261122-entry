# Data — 34 cerita, 1 kartu = 1 cerita (news-image-20261122).
# Sumber: halaman OneTurn 22 Nov 2026 (day/2026-11-22, update 12:04 ET,
# 84 cerita dari 709 headline) + verifikasi silang via search:
# GP Las Vegas start 04:00 UTC (formula1 timetable), NWSL kick-off 20:00 ET
# = 01:00 UTC (laporan resmi klub), COP31 bubar dilaporkan AP 09:20 EST
# = 14:20 UTC. Semua angka di bawah berasal dari OneTurn 22 Nov / sumber
# primernya — TIDAK ADA angka karangan.
# Tuple: (num, group, title, body, tag, time_utc_or_None, lon, lat, source)
# Tag: RESMI = dikonfirmasi resmi/dilaporkan; KLAIM = klaim sepihak yg
# belum terverifikasi; DATA = angka/statistik pasar.
# Aturan tanggal (footer): berita 22 Nov = peristiwa 22 Nov + peristiwa
# 21 Nov yg DILAPORKAN 22 Nov (kebakaran Banten Sabtu, BepiColombo Sabtu,
# pasar tutup Jumat 21:00 UTC — semua ditandai di strip/footer).
# #9: atribusi "Finlandia: Ukraina likely" (OneTurn: Finnish forces said
# Ukraine was likely behind it) + ledakan korvet Merkury di Benghazi.
# #12: "98,5% pos tarif" = tarif atas barang UE (OneTurn: removes 98.5%
# of tariffs on EU goods); target berlaku awal 2027 (rilis Komisi UE).
# #13: putusan ICJ 19 Nov; berita 22 Nov = komentar "bisa pengaruhi kasus
# Gaza" (OneTurn 22 Nov). #14: sama dgn 21 Nov (day 3 of 3).
# #25: start 04:00 UTC terverifikasi (timetable F1); menang 0,639 dtk.
# #26: kick-off 20:00 ET = 01:00 UTC (laporan resmi KC Current).
STORIES = [
    # 1 — LEAD (Eropa)
    (1, "EROPA", "COP31 Gagal Tanpa Deal",
     "KTT iklim Antalya bubar Minggu; UE tolak draf tanpa fosil. "
     "Presiden KTT: tak ada keputusan diadopsi.",
     "RESMI", None, 30.7, 36.9, "Guardian"),
    # 2–6 — SEKUNDER
    (2, "EROPA", "Drone Dymer",
     "Apartemen runtuh; 2 tewas, 14 hilang.",
     "RESMI", None, 30.8, 50.8, "Le Monde"),
    (3, "TIMUR TENGAH", "Iran Hantam Bahrain",
     "Situs industri Sitra dihantam; 2 luka; Teluk kutuk.",
     "RESMI", None, 50.5, 26.2, "Japan Times"),
    (4, "AMERIKA UTARA", "Saham Global Anjlok",
     "S&P 500 -3,7%, Nasdaq -5,3%; Nikkei -5,06%, emas -4,62%.",
     "DATA", None, -74.0, 40.7, "CNBC"),
    (5, "TIMUR TENGAH", "Rabigh Diserang",
     "Houthi klaim hantam kilang Rabigh; koalisi cegat rudal.",
     "KLAIM", None, 39.0, 22.8, "Middle East Eye"),
    (6, "AMERIKA LATIN", "Chapo Isidro Ditangkap",
     "11 tewas; 8 ditangkap; buron FBI; AS bantu intelijen.",
     "RESMI", None, -108.5, 25.6, "BBC"),
    # 7–12 — REGULER
    (7, "TIMUR TENGAH", "Bakar Tepi Barat",
     "12 kendaraan dibakar, 4 desa; Israel selidiki.",
     "RESMI", None, 35.2, 31.9, "Al Jazeera"),
    (8, "ASIA-PASIFIK", "Kebakaran Cikande",
     "Pabrik permen terbakar; 3 tewas, ~33 hilang.",
     "RESMI", None, 106.3, -6.2, "BBC"),
    (9, "EROPA", "Sparta II Terbakar",
     "Finlandia: Ukraina likely; Merkury meledak di Libya.",
     "KLAIM", None, 25.0, 59.8, "BBC"),
    (10, "GLOBAL", "BepiColombo Orbit",
     "Dua wahana orbit Merkurius; 8 tahun, 10 miliar km.",
     "RESMI", None, None, None, "BBC"),
    (11, "AMERIKA UTARA", "NCIC Diretas?",
     "Database kriminal FBI diselidiki; Trump remehkan.",
     "KLAIM", None, -77.0, 38.9, "BBC"),
    (12, "ASIA-PASIFIK", "Deal UE-Indonesia",
     "98,5% pos tarif dihapus; pasar 730 juta; target awal 2027.",
     "RESMI", None, 106.8, -6.2, "DW"),
]

STORIES += [
    (13, "GLOBAL", "Vonis Genosida",
     "ICJ: Myanmar bersalah atas Rohingya; bisa pengaruhi kasus Gaza.",
     "RESMI", None, 96.0, 21.0, "El País"),
    (14, "GLOBAL", "Hipotesis Riemann",
     "Alpöge klaim bukti dengan Claude; 2 kelompok verifikasi.",
     "KLAIM", None, -122.4, 37.8, "NPR"),
    (15, "TIMUR TENGAH", "Gaza Diserang",
     "Serangan Israel lanjut; 3 tewas di truk pangan.",
     "RESMI", None, 34.5, 31.5, "Middle East Eye"),
    (16, "GLOBAL", "Drone Khartoum",
     "4 tewas; gedung PBB rusak; tentara tuduh Ethiopia.",
     "RESMI", None, 32.5, 15.6, "Al Jazeera"),
    (17, "EROPA", "UK-UE Teken Deal",
     "Deal dagang + mobilitas; May: lupakan Brexit.",
     "RESMI", None, -0.1, 51.5, "Guardian"),
    (18, "GLOBAL", "AI Tanpa Aturan",
     "Tanpa aturan mengikat; Palang Merah: waktu habis.",
     "RESMI", None, 6.1, 46.2, "CBC"),
    (19, "EROPA", "Turki Kuasai TV",
     "Sözcü di bawah pengelola negara; ribuan protes.",
     "RESMI", None, 28.9, 41.0, "RFI"),
    (20, "ASIA-PASIFIK", "KTT Shenzhen",
     "Trump bela Putin; Zelensky: pembunuh.",
     "KLAIM", None, 114.0, 22.5, "CBS"),
    (21, "EROPA", "Protes Biaya Hidup",
     "Prancis: 144 ditangkap; ribuan berbaris di Lisbon.",
     "RESMI", None, 2.35, 48.85, "France 24"),
    (22, "AMERIKA LATIN", "Argentina LNG",
     "Proyek ekspor $50 miliar; 12 juta ton/thn.",
     "RESMI", None, -58.4, -34.6, "Buenos Aires Times"),
    (23, "EROPA", "Denmark Usir Atase",
     "Duga plot bunuh rapper Kyivstoner; Rusia bantah.",
     "KLAIM", None, 12.6, 55.7, "BBC"),
    (24, "ASIA-PASIFIK", "Menteri Korsel Mundur",
     "Mundur usai kisruh curang AI jelang ujian masuk.",
     "RESMI", None, 127.0, 37.5, "BBC"),
]

STORIES += [
    (25, "OLAHRAGA", "Verstappen Menang",
     "Menang GP Las Vegas; Norris +0,639 dtk, Piastri ketiga.",
     "RESMI", "04:00", -115.2, 36.1, "CBC"),
    (26, "OLAHRAGA", "Kansas City Juara",
     "Kalahkan Washington 2-1; gelar NWSL pertama.",
     "RESMI", "01:00", -77.0, 38.9, "CBC"),
    (27, "OLAHRAGA", "Wembanyama 50 Poin",
     "50 poin, 19 rebound; Spurs 114-91 Pelicans.",
     "RESMI", None, -98.5, 29.4, "Al Jazeera"),
    (28, "EROPA", "Kate Remisi Kanker",
     "Putri Wales umumkan remisi; tampil di dok. 'Heal'.",
     "RESMI", None, -0.1, 51.5, "CBS"),
    (29, "TIMUR TENGAH", "Kebakaran Basra",
     "Kebakaran stasiun Hartha; 4 tewas, 30 luka.",
     "RESMI", None, 47.8, 30.5, "Reuters"),
    (30, "ASIA-PASIFIK", "Oplosan Manipur",
     "Minuman oplosan; ≥11 tewas, 180+ dirawat.",
     "RESMI", None, 93.9, 24.8, "Yonhap"),
    (31, "GLOBAL", "Mini-Moon Baru",
     "Objek 2026 QQ8 mengorbit Bumi sementara; tak berbahaya.",
     "RESMI", None, None, None, "BBC"),
    (32, "TIMUR TENGAH", "Eisenkot Ajak Likud",
     "Undang Likud ke koalisi; tanpa mayoritas usai pemilu Okt.",
     "RESMI", None, 35.2, 31.8, "Euronews"),
    (33, "GLOBAL", "Perahu Nigeria",
     "Perahu pemakaman terbalik; 24 tewas, 24 selamat.",
     "RESMI", None, 6.3, 4.9, "Sky News"),
    (34, "OLAHRAGA", "Alcaraz ke Final",
     "Kalahkan Shelton 3-6, 6-3, 7-6; hadapi Zverev.",
     "RESMI", None, 7.7, 45.1, "Guardian"),
]

# Warna titik region (dipakai badge meta + pin peta). Border kartu NETRAL.
GROUP_COLOR = {
    "TIMUR TENGAH": (0, 128, 128),
    "EROPA": (29, 78, 137),
    "AMERIKA UTARA": (30, 107, 52),
    "AMERIKA LATIN": (168, 74, 20),
    "ASIA-PASIFIK": (107, 45, 143),
    "OLAHRAGA": (176, 142, 20),
    "GLOBAL": (107, 101, 90),
}
GROUP_ORDER = ["TIMUR TENGAH", "EROPA", "AMERIKA UTARA", "AMERIKA LATIN",
               "ASIA-PASIFIK", "OLAHRAGA", "GLOBAL"]

# Pin peta: HANYA 6 cerita teratas (lead + 5 sekunder).
# Nudge dihitung dari jarak antar pin (>= 20 px, diameter halo):
# #1/#2: 24,2 px; #1/#5: 21,9 px; #3/#5: 26,2 px; #4/#6: 54,6 px.
PINS = [
    (1, 0, 2), (2, 0, -2), (3, 4, -2), (4, 0, 0), (5, -4, 2), (6, 0, 0),
]

# Kartu reguler yg membawa jam di meta: #25 (04:00 GP Las Vegas, start
# terverifikasi) + #26 (01:00 kick-off final NWSL, 20:00 ET terverifikasi).
TIME_IN_META = {25, 26}

# Singkatan sumber untuk meta 12px (footer menulis nama penuh).
SRC_SHORT = {
    "Middle East Eye": "MEE",
    "Al Jazeera": "AJ",
    "Buenos Aires Times": "BAT",
    "El País": "ELP",
    "Euronews": "EUR",
    "France 24": "F24",
    "Guardian": "GDN",
    "Japan Times": "JPT",
    "Le Monde": "LMD",
    "Reuters": "RTS",
    "Sky News": "SKY",
    "Yonhap": "YON",
}
