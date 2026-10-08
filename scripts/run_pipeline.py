"""Chạy TRỌN đường ống bằng MỘT lệnh: sinh → TTS → dựng → đăng → xác minh.

    python scripts/run_pipeline.py 2026-12-01 31 --channel FS
    python scripts/run_pipeline.py 2026-12-01 31 --channel FS --no-publish
    python scripts/run_pipeline.py resume --channel FS     # chỉ rút hàng đợi + thử lại item hỏng
    python scripts/run_pipeline.py 2026-10-02 30 --channel FS --only pillars   # chỉ 4 dòng pillar
    python scripts/run_pipeline.py 2026-10-02 30 --channel FS --only lich      # chỉ Lịch

Bắt buộc --channel và (trừ `resume`) ngày bắt đầu + số ngày: bản cũ gọi trần
là sinh + ĐĂNG kênh FS cho 2026-12-01 + 31 ngày, và sau 31/12/2026 thì cùng
lệnh đó sinh nội dung cho ngày đã qua.

Mặc định sinh CẢ 5 dòng cho dải ngày: Lịch + Con Giáp + Lục Trụ + Kinh Dịch
+ Mệnh số = 5 short/ngày.

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
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, paths, store  # noqa: E402

PY_TTS, PY_VID = paths.PY_TTS, paths.PY_VID     # YF_PY_TTS / YF_PY_VID (factory/paths.py)

CH = channels.pick(required=True)
CHARG = ["--channel", CH]

_POS = [a for a in channels.args_without_channel() if not a.startswith("--")]
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else "all"
_POS = [a for a in _POS if a != ONLY]
RESUME = bool(_POS) and _POS[0] == "resume"
do_publish = "--no-publish" not in sys.argv
if not RESUME:
    if len(_POS) < 2:
        sys.exit(__doc__)
    start, days = _POS[0], _POS[1]
    try:
        _d0, _n = date.fromisoformat(start), int(days)
    except ValueError:
        sys.exit(f"ngày bắt đầu phải là YYYY-MM-DD và số ngày là số nguyên, nhận {start!r} {days!r}")
    _tomorrow_vn = (datetime.now(timezone.utc) + timedelta(hours=7)).date() + timedelta(days=1)
    if _n <= 0 or _d0 < _tomorrow_vn:
        sys.exit(f"ngày bắt đầu {start} đã qua hoặc là hôm nay (giờ VN) -- nội dung cho ngày đã qua "
                 "không được sinh/đăng. Chọn từ ngày mai trở đi.")


def run(label: str, py: Path, args: list[str]) -> float:
    """Chạy một chặng. Hỏng thì dừng cả đường ống."""
    print(f"\n{'=' * 62}\n{label}\n{'=' * 62}", flush=True)
    t0 = time.perf_counter()
    try:
        proc = subprocess.run([str(py), *args], cwd=ROOT, text=True,
                              encoding="utf-8", errors="replace",
                              capture_output=True, timeout=7200)
    except subprocess.TimeoutExpired:
        sys.exit(f"\nDỪNG ở chặng {label!r}: quá 2 giờ, tiến trình con đã bị dừng. Kiểm tra "
                 "`publish_batch.py check` trước khi chạy lại (có thể đã upload dở).")
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
    back = store.requeue_failed(_c, channel=CH)
    wait = store.deferred(_c, CH)
print(f"Thử lại {len(back)} item hỏng: {back[:5]}" if back else "Không có item hỏng cần thử lại")
if wait:
    print(f"Đang hoãn chờ quota: {len(wait)} item, tự chạy lại từ {wait[0]['retry_after']}")

if not RESUME and ONLY in ("all", "lich") and CH == "FS":
    timings["1a. sinh Lịch"] = run(
        "CHẶNG 1a — Lịch: sinh kịch bản + kiểm từng bản + kiểm chéo lô",
        PY_TTS, ["scripts/make_lich_month.py", start, days])
if not RESUME and ONLY in ("all", "pillars"):
    timings["1b. sinh 4 pillar"] = run(
        "CHẶNG 1b — 4 pillar: chọn chủ đề theo lịch sử + kiểm + kiểm chéo",
        PY_TTS, ["scripts/make_pillars_day.py", start, days, *CHARG])

timings["2. TTS"] = run(
    "CHẶNG 2 — TTS (venv vieneu)",
    PY_TTS, ["scripts/run_batch.py", "tts", CH])

timings["3. dựng video"] = run(
    "CHẶNG 3 — dựng video (venv video-editor)",
    PY_VID, ["scripts/run_batch.py", "assemble", CH])

if do_publish:
    timings["4. kiểm trước đăng"] = run(
        "CHẶNG 4 — kiểm trước khi đăng (không ghi gì)",
        PY_TTS, ["scripts/publish_batch.py", "check", *CHARG])
    timings["5. đăng"] = run(
        "CHẶNG 5 — đăng (private + hẹn giờ)",
        PY_TTS, ["scripts/publish_batch.py", "run", *CHARG])
    timings["6. xác minh"] = run(
        "CHẶNG 6 — xác minh lại trên YouTube",
        PY_TTS, ["scripts/verify_published.py", *CHARG])

total = time.perf_counter() - T0
print(f"\n{'=' * 62}\nTỔNG KẾT\n{'=' * 62}")
for k, v in timings.items():
    print(f"  {k:24s} {v:6.0f}s  ({v / total:4.0%})")
print(f"  {'TỔNG':24s} {total:6.0f}s  ({total / 60:.1f} phút)")
if not RESUME:
    n = int(days) * (len(channels.prefixes(CH)) if CH != "FS" else
                     5 if ONLY == "all" else 4 if ONLY == "pillars" else 1)
    print(f"\n  {n} video → {total / n:.0f}s mỗi video")
