"""Test cho hợp đồng Bundle và kho lưu trữ.

Nguyên tắc: mỗi test khoá lại MỘT cách hỏng thật, hoặc đã xảy ra ở v1, hoặc
là giả định mà cả kiến trúc v2 dựa vào. Không test cho có.
"""
import json

import pytest

from factory.bundle import (MAX_TAGS_TOTAL_CHARS, MAX_TITLE_CHARS, Bundle,
                            BundleInvalid, make_slug)
from factory import store


def _bundle(**over) -> Bundle:
    base = dict(
        channel="FS", kind="short", slug="mau-hop-menh-kim",
        script="Mệnh Kim hợp màu gì? Trắng, bạc và ánh kim là nhóm màu bản mệnh. "
               "Nâu và vàng đất được xem là hỗ trợ. Đỏ và hồng thì nên tiết chế. "
               "Biết đúng màu, chọn đồ nhanh hơn mỗi sáng.",
        title="Mệnh Kim hợp màu gì?",
        description="Màu bản mệnh và màu tương sinh cho mệnh Kim.",
        tags=["phong thuy", "menh kim", "mau hop menh"],
        thumbnail_text="",
        publish_at="2026-10-01T23:00:00Z",
        voice="Phạm Tuyên",
        bgm="asian_drums.mp3",
        broll_queries=["silver metal texture", "white minimal interior"],
    )
    base.update(over)
    return Bundle(**base)


# ─── Định danh ────────────────────────────────────────────────────────────

def test_id_is_stable_across_script_edits():
    """Sửa câu chữ trong kịch bản KHÔNG được tạo ra content item mới --
    nếu không, mỗi lần tinh chỉnh lại thêm một hàng vào hàng đợi và ta đăng
    trùng."""
    a = _bundle()
    b = _bundle(script=a.script + " Chúc bạn một ngày thuận lợi.")
    assert a.id == b.id


def test_id_differs_across_channels_for_same_slug():
    """Cùng chủ đề trên hai kênh là hai video khác nhau."""
    assert _bundle(channel="FS").id != _bundle(channel="BUD").id


# ─── Kiểm tra: mỗi luật ứng một cách hỏng thật ────────────────────────────

def test_rejects_title_over_youtube_limit():
    """YouTube cắt cụt tiêu đề quá 100 ký tự. Bắt ở lúc sinh, không để phát
    hiện ở bước upload -- lúc đó đã tốn TTS và render rồi."""
    with pytest.raises(BundleInvalid, match="title"):
        _bundle(title="M" * (MAX_TITLE_CHARS + 1)).validate()


def test_rejects_angle_brackets_in_title():
    with pytest.raises(BundleInvalid, match="< hoặc >"):
        _bundle(title="Mệnh Kim <hợp> màu gì").validate()


def test_tag_limit_counts_total_not_each():
    """YouTube tính TỔNG độ dài tag, không phải từng cái. Kiểm tra từng cái
    sẽ cho lọt bộ tag hợp lệ-từng-phần nhưng bị API từ chối."""
    many = ["x" * 40 for _ in range(MAX_TAGS_TOTAL_CHARS // 40 + 2)]
    with pytest.raises(BundleInvalid, match="tổng tag"):
        _bundle(tags=many).validate()


def test_rejects_publish_at_without_utc_marker():
    """Thiếu 'Z' nghĩa là múi giờ mơ hồ -- video lên sai giờ, im lặng, và
    chỉ phát hiện khi xem thống kê tuần sau."""
    with pytest.raises(BundleInvalid, match="publish_at"):
        _bundle(publish_at="2026-10-01T23:00:00").validate()


def test_rejects_impossible_datetime():
    with pytest.raises(BundleInvalid, match="publish_at"):
        _bundle(publish_at="2026-02-31T23:00:00Z").validate()


def test_short_word_count_must_fit_the_format():
    with pytest.raises(BundleInvalid, match="short phải"):
        _bundle(script="Quá ngắn.").validate()


def test_long_requires_thumbnail_text():
    """Long BẮT BUỘC có thumbnail; thiếu chữ thì bước tạo thumbnail ở pha
    sản xuất không có gì để vẽ -- mà pha đó KHÔNG được phép gọi LLM."""
    with pytest.raises(BundleInvalid, match="thumbnail_text"):
        _bundle(kind="long", script="từ " * 200, thumbnail_text="").validate()


def test_rejects_empty_voice_and_broll():
    """Hai trường này là lý do pha sản xuất không cần trí tuệ. Thiếu chúng
    thì CLI buộc phải tự quyết định -- tức là cần LLM, tức là kiến trúc sụp."""
    with pytest.raises(BundleInvalid, match="voice"):
        _bundle(voice="").validate()
    with pytest.raises(BundleInvalid, match="broll_queries"):
        _bundle(broll_queries=[]).validate()


# ─── Tuần tự hoá ──────────────────────────────────────────────────────────

def test_round_trip_preserves_everything():
    b = _bundle()
    assert Bundle.from_json(b.to_json()) == b


def test_unknown_field_is_rejected_not_ignored():
    """Trường lạ nghĩa là bundle sinh bởi bản code khác. Bỏ qua im lặng sẽ
    khiến dữ liệu mất mà không ai biết."""
    data = _bundle().to_dict()
    data["gia_tri_la"] = 1
    with pytest.raises(BundleInvalid, match="trường lạ"):
        Bundle.from_dict(data)


def test_schema_version_mismatch_is_rejected():
    data = _bundle().to_dict()
    data["schema_version"] = 99
    with pytest.raises(BundleInvalid, match="schema_version"):
        Bundle.from_dict(data)


# ─── Slug ─────────────────────────────────────────────────────────────────

def test_slug_keeps_meaning_from_vietnamese():
    """v1 sinh tên file kiểu 'Nmkinhinccaphongthy' vì lọc thô ký tự có dấu
    -- nhìn vào không đoán nổi nội dung. Bỏ dấu đúng cách thì vẫn đọc được."""
    assert make_slug("Người sống và người mất") == "Nguoi-song-va-nguoi-mat"
    assert make_slug("Năm điều cần biết về phong thuỷ") == "Nam-dieu-can-biet-ve-phong-thuy"


def test_slug_never_empty():
    assert make_slug("...") == "untitled"
    assert make_slug("") == "untitled"


# ─── Kho ──────────────────────────────────────────────────────────────────

def test_save_load_round_trip(tmp_path):
    b = _bundle()
    store.save_bundle(b, base=tmp_path)
    assert store.load_bundle("FS", b.slug, base=tmp_path) == b


def test_invalid_bundle_never_reaches_disk(tmp_path):
    """Bundle hỏng không được nằm trong hàng đợi chờ hỏng tiếp ở bước đắt
    tiền hơn."""
    with pytest.raises(BundleInvalid):
        store.save_bundle(_bundle(title=""), base=tmp_path)
    assert not list(tmp_path.rglob("*.json"))


def test_enqueue_is_idempotent(tmp_path):
    """Nạp lại cùng bundle phải vô hại. Đây là thứ v1 phải dựng
    'production-write guard' mới đạt được."""
    b = _bundle()
    with store.connect(tmp_path / "s.sqlite") as conn:
        assert store.enqueue(b, conn) is True
        assert store.enqueue(b, conn) is False
        assert conn.execute("SELECT COUNT(*) FROM item").fetchone()[0] == 1


def test_enqueue_does_not_reset_completed_work(tmp_path):
    """Chạy lại sync sau khi đã render xong KHÔNG được đưa item về pending
    -- nếu không, mỗi lần đồng bộ là render lại từ đầu."""
    b = _bundle()
    with store.connect(tmp_path / "s.sqlite") as conn:
        store.enqueue(b, conn)
        store.mark(conn, b.id, "assembled", video_path="/x/y.mp4")
        store.enqueue(b, conn)
        row = conn.execute("SELECT stage, video_path FROM item WHERE id = ?", (b.id,)).fetchone()
        assert row["stage"] == "assembled"
        assert row["video_path"] == "/x/y.mp4"


def test_next_batch_orders_by_publish_at(tmp_path):
    """Việc sắp tới hạn phải làm trước, không theo thứ tự ngẫu nhiên."""
    with store.connect(tmp_path / "s.sqlite") as conn:
        for slug, when in [("muon", "2026-10-05T00:00:00Z"),
                           ("som", "2026-10-01T00:00:00Z"),
                           ("giua", "2026-10-03T00:00:00Z")]:
            store.enqueue(_bundle(slug=slug, publish_at=when), conn)
        got = [r["slug"] for r in store.next_batch(conn, "pending", limit=10)]
        assert got == ["som", "giua", "muon"]


def test_failed_items_stop_blocking_the_queue(tmp_path):
    """Một item hỏng vĩnh viễn không được thử lại vô hạn qua nhiều lần chạy
    -- đếm ở tầng dữ liệu nên batch bị giết giữa chừng vẫn nhớ."""
    b = _bundle()
    with store.connect(tmp_path / "s.sqlite") as conn:
        store.enqueue(b, conn)
        for _ in range(3):
            store.bump_attempt(conn, b.id, "lỗi giả lập")
        assert store.next_batch(conn, "failed", max_attempts=3) == []
        assert store.next_batch(conn, "failed", max_attempts=99) != []


def test_mark_rejects_unknown_stage_and_field(tmp_path):
    b = _bundle()
    with store.connect(tmp_path / "s.sqlite") as conn:
        store.enqueue(b, conn)
        with pytest.raises(ValueError, match="stage lạ"):
            store.mark(conn, b.id, "xong_roi")
        with pytest.raises(ValueError, match="trường lạ"):
            store.mark(conn, b.id, "spoken", duong_dan_la="/x")


def test_sync_from_disk_bridges_the_two_phases(tmp_path):
    """Cầu nối giữa pha chat và pha sản xuất: Claude ghi JSON, gọi sync,
    CLI có việc. Chạy lại phải vô hại."""
    bundles = tmp_path / "bundles"
    for slug in ("a-mot", "b-hai", "c-ba"):
        store.save_bundle(_bundle(slug=slug), base=bundles)
    with store.connect(tmp_path / "s.sqlite") as conn:
        assert store.sync_from_disk(conn, base=bundles) == (3, 3)
        assert store.sync_from_disk(conn, base=bundles) == (0, 3)
        assert store.summary(conn) == {"FS": {"pending": 3}}


def test_corrupt_bundle_raises_instead_of_being_skipped(tmp_path):
    """File hỏng nằm im trong hàng đợi là thứ sẽ phát hiện vào lúc tệ nhất."""
    bundles = tmp_path / "bundles" / "FS"
    bundles.mkdir(parents=True)
    (bundles / "hong.json").write_text("{ khong phai json", encoding="utf-8")
    with pytest.raises(BundleInvalid):
        list(store.iter_bundles(base=tmp_path / "bundles"))
