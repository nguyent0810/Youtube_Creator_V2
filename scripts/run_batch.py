"""Rút hàng đợi: TTS hoặc dựng video cho cả lô.

    python scripts/run_batch.py tts       [channel]   # venv vieneu
    python scripts/run_batch.py assemble  [channel]   # venv video-editor

Hai stage chạy bằng HAI venv khác nhau: vieneu và video-editor pin version
khác hẳn nhau, không import chung vào một tiến trình được.

Engine TTS nạp MỘT lần cho cả lô -- nạp mất ~7 giây, với 465 short mà nạp
lại mỗi lần thì riêng việc nạp đã hơn một giờ.

Item lỗi không làm dừng lô: ghi lại rồi đi tiếp. Một kịch bản hỏng không
được phép chặn 464 cái còn lại.
"""
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import store  # noqa: E402

STAGE = sys.argv[1] if len(sys.argv) > 1 else "tts"
CHANNEL = sys.argv[2] if len(sys.argv) > 2 else None
OUT = ROOT / "output"


def _pexels_key() -> str:
    env = (ROOT.parent / "video-editor" / ".env").read_text(encoding="utf-8-sig")
    return re.search(r"PEXELS_API_KEY=(.+)", env).group(1).strip()


def run_tts(conn):
    from factory import speak
    rows = store.next_batch(conn, "pending", limit=200, channel=CHANNEL)
    if not rows:
        print("Khong co item nao o trang thai pending.")
        return
    print(f"{len(rows)} item. Nap model TTS...")
    engine = speak._load_engine()
    for i, row in enumerate(rows, 1):
        b = store.load_bundle(row["channel"], row["slug"])
        t0 = time.perf_counter()
        try:
            res = speak.speak_bundle(b, OUT, engine=engine)
            store.mark(conn, b.id, "spoken",
                       wav_path=res["wav_path"], timing_path=res["timing_path"])
            print(f"  [{i}/{len(rows)}] {b.slug:16s} {res['duration']:5.1f}s audio "
                  f"({time.perf_counter()-t0:.1f}s)")
        except Exception as exc:
            n = store.bump_attempt(conn, b.id, f"{type(exc).__name__}: {exc}")
            print(f"  [{i}/{len(rows)}] {b.slug:16s} LOI (lan {n}): {exc}")


def run_assemble(conn):
    from factory import assemble
    key = _pexels_key()
    rows = store.next_batch(conn, "spoken", limit=200, channel=CHANNEL)
    if not rows:
        print("Khong co item nao o trang thai spoken.")
        return
    print(f"{len(rows)} item can dung video.")
    for i, row in enumerate(rows, 1):
        b = store.load_bundle(row["channel"], row["slug"])
        t0 = time.perf_counter()
        try:
            timing = json.loads(Path(row["timing_path"]).read_text(encoding="utf-8"))
            bgm = ROOT.parent / "vietneu-tts" / "bgm" / b.bgm
            mp4 = OUT / b.channel / f"{b.slug}.mp4"
            ar = assemble.assemble_short(b, Path(row["wav_path"]), timing, mp4,
                                         pexels_key=key,
                                         bgm_path=bgm if bgm.exists() else None)
            store.mark(conn, b.id, "assembled", video_path=ar.video_path)
            size = Path(ar.video_path).stat().st_size / 1024 / 1024
            print(f"  [{i}/{len(rows)}] {b.slug:16s} {ar.scene_count} canh  "
                  f"{size:4.1f} MB  ({time.perf_counter()-t0:.0f}s)")
        except Exception as exc:
            n = store.bump_attempt(conn, b.id, f"{type(exc).__name__}: {exc}")
            print(f"  [{i}/{len(rows)}] {b.slug:16s} LOI (lan {n}): {exc}")


with store.connect() as conn:
    t0 = time.perf_counter()
    {"tts": run_tts, "assemble": run_assemble}[STAGE](conn)
    print(f"\nTong {time.perf_counter()-t0:.0f}s")
    print("Trang thai:", store.summary(conn))
