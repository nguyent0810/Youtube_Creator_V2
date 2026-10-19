"""Độ lặp khuôn theo dòng nội dung -- in ra, không chặn gì.

    python scripts/sameness_report.py                  # mọi kênh
    python scripts/sameness_report.py --channel FS

Cùng khối với brief tuần (scripts/feedback_loop.py). Đọc bundle trên đĩa, không
gọi mạng. Lý do + cách đo: factory/sameness.py.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, sameness  # noqa: E402

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")      # console Windows cp1252 không in được tiếng Việt
    for ch in ([channels.pick()] if "--channel" in sys.argv else list(channels.CHANNELS)):
        print(f"# {ch}{sameness.render_for(ch)}")
