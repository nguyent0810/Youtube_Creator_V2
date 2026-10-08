"""Cờ --channel, danh tính kênh, khoá chống chạy chồng, và tính bất biến của bundle."""
import pytest

from factory import channels, store
from factory.bundle import Bundle, BundleInvalid


def _bundle(**over) -> Bundle:
    base = dict(
        channel="FS", kind="short", slug="giap-test-store",
        script=" ".join(["chữ"] * 60), title="Tiêu đề thử", description="Mô tả.",
        tags=["phong thuy"], thumbnail_text="", publish_at="2026-12-01T04:30:00Z", voice="Anh Khôi",
        bgm="asian_drums.mp3", broll_queries=["x"])
    base.update(over)
    return Bundle(**base)


# ─── --channel ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("argv,want", [
    (["x", "--channel", "BUD"], "BUD"),
    (["x", "--channel=BUD", "--apply"], "BUD"),        # bản cũ: âm thầm thành FS
    (["x", "run", "--channel", "cl"], "CL"),
])
def test_channel_flag_forms(argv, want):
    assert channels.pick(argv, required=True) == want


@pytest.mark.parametrize("argv", [
    ["x", "--chanel", "BUD", "--apply"],               # gõ nhầm
    ["x", "--channels", "BUD"],
    ["x", "--channel"],                                # thiếu giá trị
    ["x", "--channel", "XYZ"],                         # kênh lạ
    ["x", "--apply"],                                  # script ghi lên kênh mà không ghi rõ kênh
])
def test_bad_channel_flags_stop_instead_of_defaulting_to_fs(argv):
    with pytest.raises(SystemExit):
        channels.pick(argv, required=True)


def test_args_without_channel():
    assert channels.args_without_channel(["x", "run", "--channel", "FS", "--limit", "3"]) == ["run", "--limit", "3"]
    assert channels.args_without_channel(["x", "giap-", "--channel=FS"]) == ["giap-"]


def test_bulk_prefixes_exclude_drip_only_lines():
    assert "cl-hs-" not in channels.bulk_prefixes("CL")
    assert channels.bulk_prefixes("FS") == channels.prefixes("FS")


# ─── Danh tính kênh: tin lần đầu, khoá về sau ─────────────────────────────

def _ident(monkeypatch, cid, title="Kênh"):
    from factory import publish
    monkeypatch.setattr(publish, "channel_identity", lambda tok: {"id": cid, "title": title, "uploads": "UU" + cid})
    monkeypatch.setattr(channels, "load_creds", lambda ch: {})


def test_identity_is_recorded_then_enforced(monkeypatch, tmp_path):
    with store.connect(tmp_path / "s.sqlite") as conn:
        _ident(monkeypatch, "UC_FS")
        assert channels.verify_identity("FS", "tok", conn)["id"] == "UC_FS"     # lần đầu: ghi nhận
        channels.verify_identity("FS", "tok", conn)                             # lần sau: khớp
        _ident(monkeypatch, "UC_OTHER")
        with pytest.raises(channels.ChannelMismatch):                           # credential đổi kênh
            channels.verify_identity("FS", "tok", conn)


def test_two_channels_can_never_point_at_one_youtube_channel(monkeypatch, tmp_path):
    with store.connect(tmp_path / "s.sqlite") as conn:
        _ident(monkeypatch, "UC_FS")
        channels.verify_identity("FS", "tok", conn)
        with pytest.raises(channels.ChannelMismatch):                           # CL creds trỏ vào kênh FS
            channels.verify_identity("CL", "tok", conn)


def test_pinned_channel_id_in_credentials_wins(monkeypatch, tmp_path):
    _ident(monkeypatch, "UC_X")
    monkeypatch.setattr(channels, "load_creds", lambda ch: {"channel_id": "UC_FS"})
    with store.connect(tmp_path / "s.sqlite") as conn, pytest.raises(channels.ChannelMismatch):
        channels.verify_identity("FS", "tok", conn)


# ─── Khoá ─────────────────────────────────────────────────────────────────

def test_second_runner_is_refused_while_the_lock_is_held(tmp_path):
    db = tmp_path / "s.sqlite"
    with store.connect(db) as a, store.connect(db) as b:
        with store.locked(a, "publish-FS"):
            with pytest.raises(store.LockBusy):
                with store.locked(b, "publish-FS"):
                    pass
        with store.locked(b, "publish-FS"):          # đã nhả -> lấy được
            pass


def test_expired_lock_is_reclaimed(tmp_path):
    with store.connect(tmp_path / "s.sqlite") as conn:
        conn.execute("INSERT INTO lock VALUES ('publish-FS', 'chet', '2000-01-01T00:00:00Z', '2000-01-01T03:00:00Z')")
        with store.locked(conn, "publish-FS"):
            pass


# ─── Bundle bất biến, store đồng bộ ───────────────────────────────────────

def test_save_bundle_refuses_silent_overwrite(tmp_path):
    store.save_bundle(_bundle(), base=tmp_path)
    store.save_bundle(_bundle(), base=tmp_path)                      # y hệt: vô hại
    with pytest.raises(BundleInvalid):
        store.save_bundle(_bundle(title="Tiêu đề khác"), base=tmp_path)
    store.save_bundle(_bundle(title="Tiêu đề khác"), base=tmp_path, overwrite=True)


def test_enqueue_syncs_publish_at_only_for_items_not_yet_on_youtube(tmp_path):
    with store.connect(tmp_path / "s.sqlite") as conn:
        a = _bundle(slug="giap-a")
        b = _bundle(slug="giap-b")
        store.enqueue(a, conn)
        store.enqueue(b, conn)
        store.mark(conn, b.id, "published", video_id="V")
        new = "2026-12-05T04:30:00Z"
        store.enqueue(_bundle(slug="giap-a", publish_at=new), conn)
        store.enqueue(_bundle(slug="giap-b", publish_at=new), conn)
        got = {r["slug"]: r["publish_at"] for r in conn.execute("SELECT slug, publish_at FROM item")}
    assert got == {"giap-a": new, "giap-b": "2026-12-01T04:30:00Z"}


def test_kind_change_is_a_clear_error(tmp_path):
    with store.connect(tmp_path / "s.sqlite") as conn:
        store.enqueue(_bundle(), conn)
        with pytest.raises(BundleInvalid):
            store.enqueue(_bundle(kind="long", thumbnail_text="x"), conn)


def test_mark_unknown_item_is_loud(tmp_path):
    with store.connect(tmp_path / "s.sqlite") as conn, pytest.raises(KeyError):
        store.mark(conn, "khongco", "published", video_id="V")


def test_requeue_can_be_scoped_to_one_channel(tmp_path):
    with store.connect(tmp_path / "s.sqlite") as conn:
        fs, cl = _bundle(slug="giap-x"), _bundle(channel="CL", slug="cl-hoso-x")
        for b in (fs, cl):
            store.enqueue(b, conn)
            store.bump_attempt(conn, b.id, "lỗi")
        assert store.requeue_failed(conn, channel="FS") == ["giap-x"]


# ─── Validate theo đúng cách YouTube đếm ──────────────────────────────────

def test_description_limit_is_bytes_not_characters():
    desc = "ệ" * 2000                       # 2.000 ký tự nhưng 6.000 byte
    with pytest.raises(BundleInvalid, match="byte"):
        _bundle(description=desc).validate()


def test_angle_brackets_in_description_are_rejected():
    with pytest.raises(BundleInvalid, match="description"):
        _bundle(description="Lãi > 30%/tháng").validate()


def test_tags_with_spaces_count_their_quotes():
    tags = [f"tag so {i:02d}" for i in range(42)]      # 42 x (9 + 2 ngoặc) + 41 phẩy + tag dấu = 522; không tính ngoặc chỉ 438
    with pytest.raises(BundleInvalid, match="tag"):
        _bundle(tags=tags).validate()


def test_wrong_types_are_rejected():
    with pytest.raises(BundleInvalid, match="kiểu"):
        _bundle(tags="phongthuy").validate()


def test_music_without_license_record_is_rejected():
    with pytest.raises(BundleInvalid, match="bgm"):
        _bundle(bgm="bai_nhac_la.mp3").validate()


def test_missing_field_is_bundle_invalid_not_type_error():
    d = _bundle().to_dict()
    del d["voice"]
    with pytest.raises(BundleInvalid):
        Bundle.from_dict(d)
