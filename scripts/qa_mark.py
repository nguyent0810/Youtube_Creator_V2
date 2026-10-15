"""Đánh dấu một video dài đã QA xong: ghi sha256 của final.mp4 vào output/long/<topic>/qa_ok.
publish_long từ chối nếu final.mp4 đổi sau khi đánh dấu (retro 15/10/2026).

    python scripts/qa_mark.py <topic> [<topic> ...]
"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for t in sys.argv[1:]:
    od = ROOT / "output" / "long" / t
    h = hashlib.sha256((od / "final.mp4").read_bytes()).hexdigest()
    (od / "qa_ok").write_text(h + "\n", encoding="utf-8")
    print(f"{t}: qa_ok {h[:12]}")
