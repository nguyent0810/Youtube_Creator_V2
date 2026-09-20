"""Đối chiếu 7 kịch bản Lịch với nguồn trước khi thu âm."""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory.factcheck import report  # noqa: E402
from factory.lunar import facts_range  # noqa: E402

src = (ROOT / "scripts" / "make_lich_oct.py").read_text(encoding="utf-8")
ns: dict = {}
exec(src[src.index("SCRIPTS = {"):src.index("\ncreated = []")], ns)
SCRIPTS = ns["SCRIPTS"]

all_ok = True
for f in facts_range(date(2026, 10, 1), 7):
    hook, body, _, title = SCRIPTS[f.target.isoformat()]
    ok, text = report(f"{hook} {body}", f, f.publish_at,
                      label=f"{f.target}  {f.god_name} / {f.truc_name}")
    all_ok &= ok
    print(text)
    print()

print("=" * 60)
print("TỔNG:", "TẤT CẢ ĐẠT" if all_ok else "CÓ BẢN CHƯA ĐẠT")
sys.exit(0 if all_ok else 1)
