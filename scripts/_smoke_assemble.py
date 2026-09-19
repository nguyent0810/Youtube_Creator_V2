"""Smoke test: dựng một Short thật từ Bundle + audio đã có.

Cần: video-editor clone cạnh repo, .venv-video của nó, PEXELS_API_KEY.
"""
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import assemble, store  # noqa: E402

CHANNEL, SLUG = "FS", "mau-hop-menh-kim"

# Key đọc từ .env của video-editor (đã có sẵn từ lần setup trước).
env_file = ROOT.parent / "video-editor" / ".env"
key = re.search(r"PEXELS_API_KEY=(.+)", env_file.read_text(encoding="utf-8-sig")).group(1).strip()

b = store.load_bundle(CHANNEL, SLUG)
wav = ROOT / "output" / CHANNEL / f"{SLUG}.wav"
timing = json.loads((ROOT / "output" / CHANNEL / f"{SLUG}.json").read_text(encoding="utf-8"))
out = ROOT / "output" / CHANNEL / f"{SLUG}.mp4"

bgm_src = ROOT.parent / "vietneu-tts" / "bgm" / b.bgm
bgm = bgm_src if bgm_src.exists() else None

print(f"bundle : {b.channel}/{b.slug}  ({b.word_count} tu)")
print(f"audio  : {timing['duration']}s, {len(timing['segments'])} cau")
print(f"broll  : {b.broll_queries}")
print(f"bgm    : {bgm.name if bgm else '(khong)'}")
print("Dang dung video...")

t0 = time.perf_counter()
res = assemble.assemble_short(b, wav, timing, out, pexels_key=key, bgm_path=bgm)
elapsed = time.perf_counter() - t0

print(f"\nXONG sau {elapsed:.1f}s")
print(f"  video   : {res.video_path}")
print(f"  canh    : {res.scene_count}")
print(f"  size    : {Path(res.video_path).stat().st_size / 1024 / 1024:.1f} MB")
if res.warnings:
    print(f"  canh bao: {res.warnings}")

with store.connect() as conn:
    store.mark(conn, b.id, "assembled", video_path=res.video_path)
    print(f"  summary : {store.summary(conn)}")
