"""publish_long: đủ đồ TRƯỚC upload + tìm thumbnail ở cả hai chỗ (retro 2 mục 19).

07/10: thumb.py ghi t1.jpg thẳng vào output/long/<topic>/, publish_long chỉ nhìn pub/ -> MIM #2 (sP0ch8-NYec) lên kênh không
thumbnail, rồi sập khi ghi pub/result.json (thư mục chưa có) -> không phụ đề, chuỗi tưởng xong và đăng tiếp teaser.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "long"), str(ROOT / "motion"), str(ROOT)]
import publish_long as PL  # noqa: E402


def test_thumbnail_found_in_topic_dir_when_pub_has_none(tmp_path):
    (tmp_path / "t1.jpg").write_bytes(b"j")
    assert PL.find_thumb(tmp_path) == tmp_path / "t1.jpg"
    (tmp_path / "pub").mkdir()
    (tmp_path / "pub" / "t1.jpg").write_bytes(b"j")
    assert PL.find_thumb(tmp_path) == tmp_path / "pub" / "t1.jpg"      # pub/ (cách cũ) vẫn ưu tiên


def test_preflight_lists_every_missing_piece(tmp_path):
    assert PL.preflight(tmp_path, PL.find_thumb(tmp_path)) == ["final.mp4", "description.txt", "captions.vi.srt", "t1.jpg"]
    for n in ("final.mp4", "description.txt", "captions.vi.srt", "t1.jpg"):
        (tmp_path / n).write_bytes(b"x")
    assert PL.preflight(tmp_path, PL.find_thumb(tmp_path)) == []


def test_main_checks_before_upload_and_creates_pub_dir():
    src = (ROOT / "motion" / "long" / "publish_long.py").read_text(encoding="utf-8")
    assert src.index("missing = preflight(od, thumb)") < src.index("chan.upload(u)")
    assert "rp.parent.mkdir(parents=True, exist_ok=True)" in src
