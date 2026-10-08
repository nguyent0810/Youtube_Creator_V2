"""Ghi công nhạc nền — một chỗ cho mọi đường đăng.

LỖI THẬT (audit 08/10/2026): 256 Shorts trộn nhạc Kevin MacLeod (CC BY 4.0)
nhưng KHÔNG mô tả nào ghi công; chỉ video dài (motion/long/describe.py) làm
đúng. CC BY bắt buộc ghi tác giả + tên bài + giấy phép. Thiếu là vi phạm
giấy phép, không phải chuyện "cho đẹp".

Nên: mô tả cuối cùng gửi lên YouTube luôn đi qua `final_description()`, và
Bundle.validate() từ chối bgm chưa có trong danh mục -- nhạc không rõ giấy
phép thì không được lên kênh.
"""
from __future__ import annotations

from pathlib import Path

SHORTS_MARKER = "#Shorts"

LICENSE_LINE = ("Licensed under Creative Commons: By Attribution 4.0 License — "
                "http://creativecommons.org/licenses/by/4.0/")

# file (không đuôi) -> tên gốc trên incompetech.com. Tất cả của Kevin MacLeod,
# CC BY 4.0. Bài nhạc mới cho Shorts phải thêm vào đây TRƯỚC khi dùng.
SHORTS_MUSIC = {
    "asian_drums": "Asian Drums",
    "comfortable_mystery_4": "Comfortable Mystery 4",
    "deliberate_thought": "Deliberate Thought",
    "meditation_impromptu_01": "Meditation Impromptu 01",
    "meditation_impromptu_02": "Meditation Impromptu 02",
    "meditation_impromptu_03": "Meditation Impromptu 03",
    "thinking_music": "Thinking Music",
}


def music_title(bgm: str) -> str | None:
    """Tên gốc của bài nhạc, hoặc None nếu chưa rõ giấy phép."""
    if not bgm:
        return None
    stem = Path(bgm).stem
    if stem in SHORTS_MUSIC:
        return SHORTS_MUSIC[stem]
    # Danh mục của video dài (motion/long/music_catalog.json) cũng là Kevin MacLeod.
    import json
    cat = Path(__file__).resolve().parent.parent / "motion" / "long" / "music_catalog.json"
    if cat.exists():
        for t in json.loads(cat.read_text(encoding="utf-8")).get("tracks", {}).values():
            if Path(t.get("file", "")).stem == stem and t.get("author") == "Kevin MacLeod":
                return t.get("title")
    return None


def music_credit(bgm: str) -> str | None:
    title = music_title(bgm)
    if not title:
        return None
    return f"🎵 Nhạc nền: \"{title}\" by Kevin MacLeod (incompetech.com)\n{LICENSE_LINE}"


def final_description(bundle) -> str:
    """Mô tả ĐÚNG như sẽ gửi lên YouTube: mô tả gốc + #Shorts + ghi công nhạc.

    Validate và upload cùng gọi hàm này, nên giới hạn 5.000 byte được kiểm
    trên chính văn bản sẽ gửi đi, không phải bản trước khi nối thêm."""
    desc = (bundle.description or "").rstrip()
    credit = music_credit(getattr(bundle, "bgm", "") or "")
    if credit and "incompetech" not in desc.lower():
        desc = f"{desc}\n\n{credit}" if desc else credit
    if getattr(bundle, "kind", "") == "short" and SHORTS_MARKER.lower() not in desc.lower():
        desc = f"{desc}\n\n{SHORTS_MARKER}" if desc else SHORTS_MARKER
    return desc.strip()
