"""Rút hàng đợi: TTS hoặc dựng video cho cả lô.

    python scripts/run_batch.py tts       [channel]   # venv vieneu
    python scripts/run_batch.py assemble  [channel]   # venv video-editor

Hai stage chạy bằng HAI venv khác nhau: vieneu và video-editor pin version
khác hẳn nhau, không import chung vào một tiến trình được.

Engine TTS nạp MỘT lần cho cả lô -- nạp mất ~7 giây, với 465 short mà nạp
lại mỗi lần thì riêng việc nạp đã hơn một giờ.

Item lỗi không làm dừng lô: ghi lại rồi đi tiếp. Một kịch bản hỏng không
được phép chặn 464 cái còn lại.

Mỗi worker GIÀNH từng hàng (store.claim, lease 30 phút) thay vì cùng đọc một lô:
chạy hai worker song song không còn làm trùng việc. Chỉ nhận engine "assemble"
(short thường) -- hồ sơ S-tier và video dài có đường dựng riêng, cổng toàn vẹn
của short sẽ loại nhầm chúng.
"""
import json
import os
import re
import socket
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import store  # noqa: E402

STAGE = sys.argv[1] if len(sys.argv) > 1 else "tts"
CHANNEL = sys.argv[2] if len(sys.argv) > 2 else None
OUT = ROOT / "output"
WORKER = f"{socket.gethostname()}:{os.getpid()}"


def _claimed(conn, stage):
    """Lần lượt từng hàng đã giành được. Bị dừng giữa chừng (Ctrl+C) thì thả hàng
    đang giữ ngay, khỏi chờ hết lease."""
    while (row := store.claim(conn, stage, WORKER, channel=CHANNEL, engine="assemble")) is not None:
        try:
            yield row
        except BaseException:
            store.release(conn, row["id"], WORKER)
            raise


def _pexels_key() -> str:
    env = (ROOT.parent / "video-editor" / ".env").read_text(encoding="utf-8-sig")
    return re.search(r"PEXELS_API_KEY=(.+)", env).group(1).strip()


def run_tts(conn):
    from factory import speak
    from factory import integrity
    engine = None
    for i, row in enumerate(_claimed(conn, "pending"), 1):
        if engine is None:
            print("Nap model TTS...")
            engine = speak._load_engine()   # một lần cho cả lô
        b = store.load_bundle(row["channel"], row["slug"])
        t0 = time.perf_counter()
        # Cổng toàn vẹn văn bản: MỘT điểm trước TTS cho mọi kênh/dòng.
        bad = integrity.blocking(b.script)
        if bad:
            store.reject(conn, b.id, "INTEGRITY: " + "; ".join(f"{f.code} «{f.span[:40]}»" for f in bad))
            print(f"  [{i}] {b.slug:16s} CHAN (toan ven van ban): {bad[0].code}")
            continue
        try:
            res = speak.speak_bundle(b, OUT, engine=engine)
            store.mark(conn, b.id, "spoken",
                       wav_path=res["wav_path"], timing_path=res["timing_path"])
            print(f"  [{i}] {b.slug:16s} {res['duration']:5.1f}s audio "
                  f"({time.perf_counter()-t0:.1f}s)")
        except Exception as exc:
            n = store.bump_attempt(conn, b.id, f"{type(exc).__name__}: {exc}")
            print(f"  [{i}] {b.slug:16s} LOI (lan {n}): {exc}")
    if engine is None:
        print("Khong co item nao o trang thai pending.")


def run_assemble(conn):
    from factory import assemble
    key = _pexels_key()
    done = 0
    for i, row in enumerate(_claimed(conn, "spoken"), 1):
        done = i
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
            print(f"  [{i}] {b.slug:16s} {ar.scene_count} canh  "
                  f"{size:4.1f} MB  ({time.perf_counter()-t0:.0f}s)")
        except Exception as exc:
            n = store.bump_attempt(conn, b.id, f"{type(exc).__name__}: {exc}")
            print(f"  [{i}] {b.slug:16s} LOI (lan {n}): {exc}")
    if not done:
        print("Khong co item nao o trang thai spoken.")


with store.connect() as conn:
    t0 = time.perf_counter()
    {"tts": run_tts, "assemble": run_assemble}[STAGE](conn)
    print(f"\nTong {time.perf_counter()-t0:.0f}s")
    print("Trang thai:", store.summary(conn))
