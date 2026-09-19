"""Demo caption kiểu TikTok + test tra tấn dấu tiếng Việt.

Kịch bản cố ý nhồi những chữ có dấu CHỒNG TẦNG -- ế, ồ, ữ, ợ, ẩ, ỡ, ặ, ộ,
ườ -- vì đây đúng là nhóm bị cắt cụt khi viền quá dày hoặc chữ quá to. Test
bằng chữ không dấu sẽ không bao giờ lộ ra lỗi này.

Hook dùng kiểu "phản trực giác" (xem factory/hooks.py).
"""
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import assemble, speak, store  # noqa: E402
from factory.bundle import Bundle  # noqa: E402

b = Bundle(
    channel="FS", kind="short", slug="huong-bep-quan-trong-hon",
    # Hook phản trực giác + mỗi câu nhồi dấu khó.
    script=("Hướng nhà đẹp mà bếp đặt sai thì vẫn chưa ổn. "
            "Người xưa xem bếp là nơi giữ lửa, nên vị trí của nó được coi trọng hơn cả cửa chính. "
            "Bếp kỵ đối diện thẳng nhà vệ sinh, và cũng nên tránh kề sát bồn rửa. "
            "Chỉ cần dịch chuyển một chút, không gian bếp đã dễ chịu hẳn. "
            "Hướng nhà quan trọng, nhưng chỗ đặt bếp mới là thứ bạn dùng mỗi ngày."),
    title="Hướng bếp quan trọng hơn hướng nhà?",
    description="Vì sao vị trí bếp được xem trọng hơn cả cửa chính.",
    tags=["phong thuy", "huong bep", "phong thuy nha o"],
    thumbnail_text="",
    publish_at="2026-10-02T23:00:00Z",
    voice="Phạm Tuyên",
    bgm="deliberate_thought.mp3",
    broll_queries=[
        "modern kitchen interior warm light",
        "wooden kitchen counter close up",
        "steam cooking pot slow motion",
        "minimal home interior daylight",
    ],
)

STAGE = sys.argv[1] if len(sys.argv) > 1 else "all"

store.save_bundle(b)
with store.connect() as conn:
    store.sync_from_disk(conn)

out_dir = ROOT / "output"
base = out_dir / b.channel / b.slug

if STAGE in ("tts", "all"):
    print(f"[1/2] TTS  ({b.word_count} tu)...")
    t0 = time.perf_counter()
    res = speak.speak_bundle(b, out_dir)
    print(f"      {res['duration']}s audio, {res['n_segments']} cau, {round(time.perf_counter()-t0,1)}s")
    if STAGE == "tts":
        sys.exit(0)
else:
    res = {"wav_path": str(base.with_suffix(".wav")), "timing_path": str(base.with_suffix(".json"))}

key = re.search(r"PEXELS_API_KEY=(.+)",
                (ROOT.parent / "video-editor" / ".env").read_text(encoding="utf-8-sig")).group(1).strip()
timing = json.loads(Path(res["timing_path"]).read_text(encoding="utf-8"))
bgm_src = ROOT.parent / "vietneu-tts" / "bgm" / b.bgm
mp4 = out_dir / b.channel / f"{b.slug}.mp4"

print(f"[2/2] Dung video (caption TikTok, {len(b.broll_queries)} query)...")
t0 = time.perf_counter()
ar = assemble.assemble_short(b, Path(res["wav_path"]), timing, mp4,
                             pexels_key=key,
                             bgm_path=bgm_src if bgm_src.exists() else None)
print(f"      {ar.scene_count} canh, {Path(ar.video_path).stat().st_size/1024/1024:.1f} MB, "
      f"{round(time.perf_counter()-t0,1)}s")

with store.connect() as conn:
    store.mark(conn, b.id, "assembled", wav_path=res["wav_path"],
               timing_path=res["timing_path"], video_path=ar.video_path)
    print("      summary:", store.summary(conn))
print("\nVIDEO:", ar.video_path)
