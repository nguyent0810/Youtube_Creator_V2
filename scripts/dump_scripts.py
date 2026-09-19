"""Xuất kịch bản ra Markdown để đọc và duyệt trước khi thu âm.

Người duyệt cần đọc LỜI, không cần đọc JSON. File này gom mọi bundle của
một kênh thành một trang, kèm điểm chấm của script_craft.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import store  # noqa: E402
from factory.script_craft import review, split_sentences  # noqa: E402

channel = sys.argv[1] if len(sys.argv) > 1 else "FS"
prefix = sys.argv[2] if len(sys.argv) > 2 else ""

bundles = [b for b in store.iter_bundles(channel=channel) if b.slug.startswith(prefix)]
bundles.sort(key=lambda b: b.publish_at)

lines = [f"# Kịch bản — kênh {channel}", ""]
for b in bundles:
    checks = review(b.script)
    verdict = "ĐẠT" if all(c.ok for c in checks) else "CẦN SỬA"
    sents = split_sentences(b.script)
    lines += [
        f"## {b.title}",
        "",
        f"`{b.slug}` · **{b.word_count} từ** · đăng `{b.publish_at}` · chấm: **{verdict}**",
        "",
    ]
    for i, s in enumerate(sents):
        mark = " ←— **hook**" if i == 0 else (" ←— **chốt**" if i == len(sents) - 1 else "")
        lines.append(f"> {s}{mark}")
        lines.append(">")
    lines += ["", f"*Nguồn:* `{b.source_note}`", "",
              f"*B-roll:* {' · '.join(b.broll_queries)}", "", "---", ""]

out = ROOT / "output" / f"kich-ban-{channel}.md"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(lines), encoding="utf-8")
print(f"{len(bundles)} kịch bản -> {out}")
