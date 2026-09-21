"""Chạy TRỌN đường ống bằng MỘT lệnh: sinh → TTS → dựng → đăng → xác minh.

    python scripts/run_pipeline.py 2026-12-01 31
    python scripts/run_pipeline.py 2026-12-01 31 --no-publish
    python scripts/run_pipeline.py resume     # chỉ rút hàng đợi + thử lại item hỏng

`resume` là lệnh cho lịch chạy định kỳ: không sinh gì mới, chỉ đưa item
hỏng về đúng chặng rồi chạy tiếp mọi chặng. Item hoãn vì hết quota tự hiện
lại khi tới mốc reset -- không cần người chạy tay.

VÌ SAO CẦN FILE NÀY: từ trước tới giờ mỗi bước chạy một lệnh riêng, và tôi
là người nối chúng lại. Đó không phải tự động hoá -- đó là tôi làm thủ công
nhanh. Muốn nhân rộng sang BUD và CL thì phải có một lệnh chạy được không
người.

HAI VENV, KHÔNG THỂ GỘP: vieneu và video-editor pin version khác hẳn nhau
(PySide6, faster-whisper, onnxruntime...), không import chung vào một tiến
trình được. Nên file này gọi subprocess sang đúng venv cho từng bước --
cùng cách video_tool_bridge của v1 làm, và là cách duy nhất chạy được.

FAIL-CLOSED TỪNG CHẶNG: bước nào hỏng thì DỪNG, không chạy tiếp. Đăng nhầm
lên kênh thật không rút lại được, nên thà dừng giữa chừng còn hơn đi tiếp
với dữ liệu sai.
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PY_TTS = Path(r"C:\Tools\Youtuber\vietneu-tts\.venv\Scripts\python.exe")
PY_VID = Path(r"C:\Tools\Youtuber\video-editor\.venv-video\Scripts\python.exe")

from factory import store  # noqa: E402

RESUME = len(sys.argv) > 1 and sys.argv[1] == "resume"
start = sys.argv[1] if len(sys.argv) > 1 and not RESUME else "2026-12-01"
days = sys.argv[2] if len(sys.argv) > 2 and not RESUME else "31"
do_publish = "--no-publish" not in sys.argv


def run(label: str, py: Path, args: list[str]) -> float:
    """Chạy một chặng. Hỏng thì dừng cả đường ống."""
    print(f"\n{'=' * 62}\n{label}\n{'=' * 62}", flush=True)
    t0 = time.perf_counter()
    proc = subprocess.run([str(py), *args], cwd=ROOT, text=True,
                          encoding="utf-8", errors="replace",
                          capture_output=True, timeout=7200)
    dt = time.perf_counter() - t0
    tail = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()][-8:]
    for ln in tail:
        print("  " + ln)
    if proc.returncode != 0:
        err = [ln for ln in (proc.stderr or "").splitlines() if ln.strip()][-6:]
        print("  STDERR:")
        for ln in err:
            print("    " + ln)
        sys.exit(f"\nDỪNG ở chặng {label!r} (exit {proc.returncode}). "
                 "Không chạy tiếp — đăng nhầm lên kênh thật không rút lại được.")
    print(f"  ⏱  {dt:.0f}s")
    return dt


timings: dict[str, float] = {}
T0 = time.perf_counter()

# CHẶNG 0 — item hỏng lần trước quay về đúng chặng đã hỏng (tối đa 3 lần).
with store.connect() as _c:
    back = store.requeue_failed(_c)
    wait = store.deferred(_c)
print(f"Thử lại {len(back)} item hỏng: {back[:5]}" if back else "Không có item hỏng cần thử lại")
if wait:
    print(f"Đang hoãn chờ quota: {len(wait)} item, tự chạy lại từ {wait[0]['retry_after']}")

if not RESUME:
    timings["1. sinh kịch bản"] = run(
        "CHẶNG 1 — sinh kịch bản + kiểm từng bản + kiểm chéo lô",
        PY_TTS, ["scripts/make_lich_month.py", start, days])

timings["2. TTS"] = run(
    "CHẶNG 2 — TTS (venv vieneu)",
    PY_TTS, ["scripts/run_batch.py", "tts", "FS"])

timings["3. dựng video"] = run(
    "CHẶNG 3 — dựng video (venv video-editor)",
    PY_VID, ["scripts/run_batch.py", "assemble", "FS"])

if do_publish:
    timings["4. kiểm trước đăng"] = run(
        "CHẶNG 4 — kiểm trước khi đăng (không ghi gì)",
        PY_TTS, ["scripts/publish_batch.py", "check"])
    timings["5. đăng"] = run(
        "CHẶNG 5 — đăng (private + hẹn giờ)",
        PY_TTS, ["scripts/publish_batch.py", "run"])
    timings["6. xác minh"] = run(
        "CHẶNG 6 — xác minh lại trên YouTube",
        PY_TTS, ["scripts/verify_published.py"])

total = time.perf_counter() - T0
print(f"\n{'=' * 62}\nTỔNG KẾT\n{'=' * 62}")
for k, v in timings.items():
    print(f"  {k:24s} {v:6.0f}s  ({v / total:4.0%})")
print(f"  {'TỔNG':24s} {total:6.0f}s  ({total / 60:.1f} phút)")
if not RESUME:
    n = int(days)
    print(f"\n  {n} video → {total / n:.0f}s mỗi video")
