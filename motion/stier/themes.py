"""Giao diện theo kênh cho bộ dựng S-tier (build.py) -- MỘT bộ dựng, nhiều kênh.

"case" = kênh Hình Sự (CL): hồ sơ lưu trữ cắt dán, giữ NGUYÊN mọi mặc định cũ.
"mim"  = Mind in the Machine: phòng thí nghiệm tối, lưới mảnh, nhấn xanh cyan,
         giọng riêng, nhạc nền CC BY dưới giọng đọc, Beat Text kiểu công nghệ.

Spec chọn bằng "theme": "mim" (không ghi = "case"). Thiết kế + lý do (2 vòng
Grok): docs/channels/mind-in-the-machine/2026-10-06-stier-design.md.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MUSIC_DIR = ROOT / "output" / "music"
MUSIC_LEDGER = ROOT / "data" / "variety" / "mim_music.json"

# Nhạc Kevin MacLeod (incompetech.com), CC BY 4.0 -- ghi công trong mô tả.
# Tải 06/10/2026 vào output/music/ (gitignore). Content ID có thể báo claim:
# tác giả cho phép, gỡ bằng dòng ghi công; Studio chặn thì bỏ bài đó khỏi pool.
MIM_TRACKS = {
    "bit_shift.mp3": "Bit Shift",
    "digital_lemonade.mp3": "Digital Lemonade",
    "inspired.mp3": "Inspired",
    "chill_wave.mp3": "Chill Wave",
    "hyperfun.mp3": "Hyperfun",
    "ouroboros.mp3": "Ouroboros",
}

THEMES = {
    "case": {"voice": "Anh Khôi", "accent": "#e2402d", "sound": "drone", "pools": None, "js": {}},
    "mim": {
        "voice": "Hải Đăng",            # nam, giọng Bắc, tự nhiên -- khác mọi giọng của 3 kênh kia
        "img_license": "by",            # Commons: PD/CC0 + CC BY có ghi công (không BY-SA); thêm NASA:<id>
        "accent": "#22d3ee",
        "sound": "music",
        "music_gain": 0.16,
        # Beat Text kiểu công nghệ (docs/channels/mind-in-the-machine/2026-10-06-stier-design.md):
        # - dòng lớn được đọc trọn -> "sync" (từng chữ hiện đúng lúc đọc, beatfx.apply_sync);
        #   còn lại MỖI DÒNG MỘT KIỂU: rise/blur/slice/flicker.
        # - "type" = dòng lệnh terminal (dấu nhắc "> ", canh trái) -> CHỈ khi spec ghi "fx":"type".
        # - "glitch" ở đây là glitch trên chữ (BEAT.glitch), không phải SLAM.glitch rung #stage.
        # - không redact/stamp/tape (chất hồ sơ hình sự).
        "pools": {"N": ["rise", "blur", "slice", "flicker"], "A": ["marker", "outline", "flicker", "glitch"],
                  "S": ["rise", "blur", "flicker"], "D": ["scramble", "rise"],
                  "X": ["punch", "zoom", "slice", "outline"], "per_line": True, "sync": True},
        # Gửi sang casefile.js (window.CASE.theme)
        "js": {"cls": "theme-mim", "frame": "print", "tone": "color", "pop": True, "karaoke": True,
               "prompt": True, "drift": True,
               "labels": {"unit": "NGÀY", "file": "GIẢI MÃ"}},
    },
}


def theme(spec: dict) -> dict:
    name = spec.get("theme", "case")
    if name not in THEMES:
        raise SystemExit(f"theme lạ {name!r} (có: {', '.join(THEMES)})")
    return THEMES[name]


def pick_track(slug: str, pool: list[str], ledger: Path = MUSIC_LEDGER) -> str:
    """Nhạc cho `slug`: đã chọn rồi thì giữ (dựng lại ra y hệt); chưa thì bài lâu
    chưa dùng nhất trong `pool`. Ghi sổ NGAY sau mỗi lần chọn (Grok: dựng song song
    đọc cùng một sổ sẽ chọn trùng -- dựng MIM tuần tự)."""
    led = json.loads(ledger.read_text(encoding="utf-8")) if ledger.exists() else {"picks": []}
    for p in led["picks"]:
        if p["slug"] == slug and p["file"] in pool:
            return p["file"]
    last = {p["file"]: i for i, p in enumerate(led["picks"])}
    choice = min(pool, key=lambda f: (last.get(f, -1), pool.index(f)))
    led["picks"].append({"slug": slug, "file": choice})
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(json.dumps(led, ensure_ascii=False, indent=1), encoding="utf-8")
    return choice


def music_filter(gain: float, quiet: list[tuple[float, float]]) -> str:
    """filter_complex: [1]=giọng, [2]=sfx, [3]=nhạc. Thông số trộn của video dài
    (build_long.mix_chapter): nhạc ~0.16, nén theo giọng 0.03/6/40/600, cảnh
    `question` gần như tắt nhạc (khoảng lặng là cú đấm), loudnorm SAU khi trộn."""
    duck = "".join(f",volume=enable='between(t,{a - 0.1:.2f},{z:.2f})':volume=0.12" for a, z in quiet)
    return ("[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad,asplit=3[v][vk][vk2];"
            "[2:a]volume=0.5[s0];[s0][vk]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[s];"
            f"[3:a]aresample=48000,volume={gain}{duck}[m0];"
            "[m0][vk2]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600[m];"
            "[v][s][m]amix=inputs=3:weights='1 1 1':normalize=0:duration=first,"
            "loudnorm=I=-14:TP=-1.5:LRA=11[a]")


def music_credit(file: str) -> str:
    return (f"Music: \"{MIM_TRACKS.get(file, file)}\" by Kevin MacLeod (incompetech.com). "
            "Licensed under Creative Commons: By Attribution 4.0 — http://creativecommons.org/licenses/by/4.0/")
