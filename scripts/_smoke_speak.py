"""Smoke test: chạy một Bundle thật qua pha sản xuất TTS.

Không phải test tự động (cần model thật + vài chục giây) -- đây là lệnh
chạy tay để xác nhận đường ống thông trên máy mới.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from factory import speak, store  # noqa: E402
from factory.bundle import Bundle  # noqa: E402

b = Bundle(
    channel="FS", kind="short", slug="mau-hop-menh-kim",
    script=("Mệnh Kim hợp màu gì? Trắng, bạc và ánh kim là nhóm màu bản mệnh. "
            "Nâu và vàng đất được xem là hỗ trợ. Đỏ và hồng thì nên tiết chế. "
            "Biết đúng màu, chọn đồ nhanh hơn mỗi sáng."),
    title="Mệnh Kim hợp màu gì?",
    description="Màu bản mệnh và màu tương sinh cho mệnh Kim.",
    tags=["phong thuy", "menh kim"],
    thumbnail_text="",
    publish_at="2026-10-01T23:00:00Z",
    voice="Phạm Tuyên",
    bgm="asian_drums.mp3",
    broll_queries=["silver metal texture", "white minimal interior"],
)

print("bundle id:", b.id, "| so tu:", b.word_count)
store.save_bundle(b)
with store.connect() as conn:
    print("sync (moi, tong):", store.sync_from_disk(conn))

print("Nap model + tong hop...")
t0 = time.perf_counter()
res = speak.speak_bundle(b, Path("output"))
print("  tong thoi gian (gom nap model):", round(time.perf_counter() - t0, 1), "s")
for k, v in res.items():
    print(f"  {k}: {v}")

with store.connect() as conn:
    store.mark(conn, b.id, "spoken", wav_path=res["wav_path"], timing_path=res["timing_path"])
    print("  summary:", store.summary(conn))
