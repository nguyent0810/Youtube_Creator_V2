"""Channel: mọi lần ghi lên YouTube đi qua đây (docs/audit/2026-10-05-channel-design.md).

Test chạy trên FakeYouTube (adapter in-memory) + SQLite tạm. Không có mạng.
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from factory import store
from factory.channel import Channel, Upload
from factory.youtube_fake import FakeYouTube

T0 = datetime(2026, 10, 5, 3, 0, tzinfo=timezone.utc)


class Clock:
    def __init__(self, t=T0):
        self.t = t

    def __call__(self):
        return self.t

    def advance(self, **kw):
        self.t += timedelta(**kw)


@pytest.fixture
def env(tmp_path):
    clock = Clock()
    yt = FakeYouTube()
    video = tmp_path / "final.mp4"
    video.write_bytes(b"\0" * 64)
    with store.connect(tmp_path / "state.sqlite") as conn:
        yield {"clock": clock, "yt": yt, "conn": conn, "video": video, "tmp": tmp_path}


def ch(env, code="FS", **kw):
    return Channel(code, env["yt"], env["conn"], now=env["clock"], **kw)


def up(env, slug="lich-20261010", title="Ngày 10/10 tốt cho việc gì", when="2026-10-10T23:00:00Z", **kw):
    fields = dict(slug=slug, video=env["video"], title=title, description="Mô tả.",
                  tags=("phong thuy",), kind="short", publish_at=when)
    fields.update(kw)
    return Upload(**fields)


def test_upload_lands_private_and_scheduled_never_public(env):
    res = ch(env).upload(up(env))

    v = env["yt"].get_video(res.video_id, "snippet,status")
    assert v["status"]["privacyStatus"] == "private"
    assert v["status"]["publishAt"] == "2026-10-10T23:00:00Z"
    assert v["snippet"]["title"] == "Ngày 10/10 tốt cho việc gì"
    assert v["snippet"]["categoryId"] == "22"
    assert v["snippet"]["description"].endswith("#Shorts")
    assert res.reused is False
    assert env["yt"].inserts == 1


def test_same_slug_twice_reuses_the_video_and_never_uploads_again(env):
    first = ch(env).upload(up(env))
    again = ch(env).upload(up(env))

    assert again.video_id == first.video_id
    assert again.reused is True
    assert env["yt"].inserts == 1


def test_same_title_on_another_slug_is_refused_not_silently_reused(env):
    # Bug thật (repair_titles.py): 9 ngày Lịch trùng tiêu đề nhận video_id của ngày khác.
    from factory.channel import DuplicateTitle
    first = ch(env).upload(up(env, slug="lich-20261010"))

    with pytest.raises(DuplicateTitle) as e:
        ch(env).upload(up(env, slug="lich-20261022"))

    assert e.value.video_id == first.video_id
    assert env["yt"].inserts == 1


def test_title_already_on_the_channel_from_elsewhere_is_refused(env):
    from factory.channel import DuplicateTitle
    snapshot = {"Ngày 10/10 tốt cho việc gì": "vidOLD1"}   # chụp từ playlist uploads của kênh

    with pytest.raises(DuplicateTitle) as e:
        ch(env, channel_titles=snapshot).upload(up(env, title="  ngày 10/10 TỐT cho  việc gì "))

    assert e.value.video_id == "vidOLD1"
    assert env["yt"].inserts == 0


def test_cl_waits_three_hours_between_uploads_whoever_calls(env):
    # Sự cố 30/09: CL nhận ~53 video trong 47 phút rồi rơi khỏi feed Shorts.
    from factory.channel import PacingHold
    ch(env, "CL").upload(up(env, slug="cl-hs-a", title="A"))

    with pytest.raises(PacingHold) as e:
        ch(env, "CL").upload(up(env, slug="cl-hs-b", title="B"))
    assert e.value.until == T0 + timedelta(hours=3)
    assert ch(env, "CL").next_upload_at() == T0 + timedelta(hours=3)
    assert env["yt"].inserts == 1

    env["clock"].advance(hours=3)
    ch(env, "CL").upload(up(env, slug="cl-hs-b", title="B"))
    assert env["yt"].inserts == 2


def test_fs_uploads_at_most_24_in_any_24_hours(env):
    from factory.channel import PacingHold
    for i in range(24):
        ch(env).upload(up(env, slug=f"lich-{i}", title=f"Ngày {i}"))
        env["clock"].advance(minutes=1)

    with pytest.raises(PacingHold) as e:
        ch(env).upload(up(env, slug="lich-24", title="Ngày 24"))
    assert e.value.until == T0 + timedelta(hours=24)
    assert env["yt"].inserts == 24

    env["clock"].t = T0 + timedelta(hours=24)
    ch(env).upload(up(env, slug="lich-24", title="Ngày 24"))
    assert env["yt"].inserts == 25


def test_quota_before_any_session_frees_the_slot(env):
    from factory.youtube_api import QuotaExceeded
    env["yt"].fail_next_insert(QuotaExceeded("429 lúc khởi tạo"), after_session=False)

    with pytest.raises(QuotaExceeded):
        ch(env, "CL").upload(up(env, slug="cl-hs-a", title="A"))

    assert ch(env, "CL").next_upload_at() == T0      # slot không bị giữ
    ch(env, "CL").upload(up(env, slug="cl-hs-a", title="A"))
    assert env["yt"].inserts == 1


def test_lost_response_after_video_was_created_adopts_it_instead_of_reuploading(env):
    # Mất phản hồi 201 ở chunk cuối: video ĐÃ có trên YouTube.
    from factory.youtube_api import UploadInterrupted
    env["yt"].fail_next_insert(UploadInterrupted("mất mạng ở chunk cuối"), completed=True)

    with pytest.raises(UploadInterrupted):
        ch(env, "CL").upload(up(env, slug="cl-hs-a", title="A"))

    env["clock"].advance(minutes=10)                  # thử lại sớm: slot đã là của nó
    res = ch(env, "CL").upload(up(env, slug="cl-hs-a", title="A"))
    assert env["yt"].inserts == 1
    assert env["yt"].get_video(res.video_id, "status")["status"]["publishAt"] == "2026-10-10T23:00:00Z"


def test_interrupted_partial_upload_resumes_the_same_session(env):
    from factory.youtube_api import UploadInterrupted
    env["yt"].fail_next_insert(UploadInterrupted("503 ở chunk giữa"), completed=False)

    with pytest.raises(UploadInterrupted):
        ch(env).upload(up(env))
    ch(env).upload(up(env))

    assert env["yt"].inserts == 1
    assert len(env["yt"].sessions) == 1


def test_expired_session_is_in_doubt_keeps_its_slot_and_waits_for_a_human(env):
    from factory.channel import PacingHold
    from factory.youtube_api import UploadInDoubt, UploadInterrupted
    env["yt"].fail_next_insert(UploadInterrupted("mất mạng"), completed=False)
    with pytest.raises(UploadInterrupted):
        ch(env, "CL").upload(up(env, slug="cl-hs-a", title="A"))
    env["yt"].expire_session("fake://session/1")

    with pytest.raises(UploadInDoubt):
        ch(env, "CL").upload(up(env, slug="cl-hs-a", title="A"))
    with pytest.raises(PacingHold):                   # slot vẫn bị giữ
        ch(env, "CL").upload(up(env, slug="cl-hs-b", title="B"))
    assert env["yt"].inserts == 0


def _in_doubt(env, code="CL", slug="cl-hs-a", title="A"):
    from factory.youtube_api import UploadInDoubt, UploadInterrupted
    env["yt"].fail_next_insert(UploadInterrupted("mất mạng"), completed=False)
    with pytest.raises(UploadInterrupted):
        ch(env, code).upload(up(env, slug=slug, title=title))
    env["yt"].expire_session(list(env["yt"].sessions)[-1])     # phiên vừa đứt
    with pytest.raises(UploadInDoubt):
        ch(env, code).upload(up(env, slug=slug, title=title))


def test_resolve_none_frees_the_slot_so_the_slug_can_upload_again(env):
    _in_doubt(env)
    ch(env, "CL").resolve("cl-hs-a", None)

    ch(env, "CL").upload(up(env, slug="cl-hs-a", title="A"))
    assert env["yt"].inserts == 1


def test_resolve_with_a_video_that_does_not_exist_is_refused(env):
    from factory.youtube_api import PublishError
    _in_doubt(env)

    with pytest.raises(PublishError):
        ch(env, "CL").resolve("cl-hs-a", "vidNOPE")


def test_resolve_with_the_real_video_marks_it_done(env):
    _in_doubt(env)
    real = env["yt"].add_video({"title": "A"}, {"privacyStatus": "private"})   # người thấy nó trong Studio

    ch(env, "CL").resolve("cl-hs-a", real)
    again = ch(env, "CL").upload(up(env, slug="cl-hs-a", title="A"))
    assert again.reused and again.video_id == real


@pytest.mark.parametrize("fields, unscheduled", [
    ({"when": "2026-10-05T03:00:00Z"}, False),             # publishAt = bây giờ: YouTube sẽ công khai ngay
    ({"when": "2026-10-04T23:00:00Z"}, False),             # đã qua
    ({"when": None}, False),                               # không lịch mà không phải probe
    ({}, True),                                            # probe mà vẫn có lịch
    ({"kind": "long"}, False),                             # Long thiếu category
])
def test_bad_upload_requests_are_refused_before_touching_youtube(env, fields, unscheduled):
    from factory.youtube_api import PublishError
    with pytest.raises(PublishError):
        ch(env).upload(up(env, **fields), unscheduled=unscheduled)
    assert env["yt"].inserts == 0
    assert ch(env).next_upload_at() == T0


def test_reschedule_changes_only_the_schedule_and_keeps_every_other_status_field(env):
    c = ch(env)
    vid = c.upload(up(env)).video_id
    env["yt"].videos[vid]["status"].update(embeddable=False, license="creativeCommon",
                                           containsSyntheticMedia=False)

    c.reschedule(vid, "2026-10-20T23:00:00Z")
    st = env["yt"].get_video(vid, "status")["status"]
    assert st["publishAt"] == "2026-10-20T23:00:00Z"
    assert st["privacyStatus"] == "private"
    assert (st["embeddable"], st["license"], st["containsSyntheticMedia"]) == (False, "creativeCommon", False)

    c.reschedule(vid, None)                                # gỡ lịch: private, không bao giờ tự lên
    st = env["yt"].get_video(vid, "status")["status"]
    assert "publishAt" not in st and st["privacyStatus"] == "private"
    assert st["license"] == "creativeCommon"


def test_reschedule_refuses_a_video_that_is_already_public(env):
    from factory.youtube_api import PublishError
    c = ch(env)
    vid = c.upload(up(env)).video_id
    env["yt"].go_live(vid)

    with pytest.raises(PublishError):
        c.reschedule(vid, "2026-10-20T23:00:00Z")
    assert env["yt"].get_video(vid, "status")["status"]["privacyStatus"] == "public"


def test_edit_changes_snippet_only_and_never_takes_a_live_video_down(env):
    c = ch(env)
    vid = c.upload(up(env, tags=("a", "b"))).video_id
    env["yt"].go_live(vid)

    c.edit(vid, title="Tiêu đề mới", categoryId="27")
    v = env["yt"].get_video(vid, "snippet,status")
    assert v["snippet"]["title"] == "Tiêu đề mới"
    assert v["snippet"]["categoryId"] == "27"
    assert v["snippet"]["tags"] == ["a", "b"]
    assert v["snippet"]["defaultAudioLanguage"] == "vi"
    assert v["status"]["privacyStatus"] == "public"


def test_edit_refuses_fields_that_are_not_writable_snippet_fields(env):
    from factory.youtube_api import PublishError
    c = ch(env)
    vid = c.upload(up(env)).video_id
    with pytest.raises(PublishError):
        c.edit(vid, privacyStatus="public")


def test_probe_then_run_reuses_the_probe_video_and_schedules_it(env):
    c = ch(env)
    probe = c.upload(up(env, when=None), unscheduled=True)
    assert "publishAt" not in env["yt"].get_video(probe.video_id, "status")["status"]

    run = c.upload(up(env))
    assert run.reused and run.video_id == probe.video_id
    assert run.publish_at == "2026-10-10T23:00:00Z"
    assert env["yt"].get_video(probe.video_id, "status")["status"]["publishAt"] == "2026-10-10T23:00:00Z"
    assert env["yt"].inserts == 1


def test_thumbnail_is_set_and_its_failure_never_fails_a_finished_upload(env):
    from factory.youtube_api import PublishError
    jpg = env["tmp"] / "t1.jpg"
    jpg.write_bytes(b"jpg")

    ok = ch(env).upload(up(env, slug="a", title="A", thumbnail=jpg))
    assert env["yt"].thumbnails[ok.video_id] == jpg and ok.thumbnail_error is None

    env["yt"].fail_next_thumbnail(PublishError("thumbnails.set HTTP 403"))
    bad = ch(env).upload(up(env, slug="b", title="B", thumbnail=jpg))
    assert "403" in bad.thumbnail_error
    assert ch(env).upload(up(env, slug="b", title="B")).reused   # video vẫn ghi sổ là xong


def test_uploads_recorded_before_the_ledger_existed_still_count(env):
    # Video drip đã đăng lên CL 1 giờ trước khi Channel ra đời: chỉ có dòng trong `item`.
    from factory.bundle import Bundle
    b = Bundle(channel="CL", kind="short", slug="cl-hs-old", script="Một câu đủ dài để kể chuyện. " * 8, title="Cũ",
               description="d", tags=["x"], thumbnail_text="", publish_at="2026-10-06T11:30:00Z",
               voice="Anh Khôi", bgm="", broll_queries=["hyperframes-casefile"])
    conn = env["conn"]
    store.enqueue(b, conn)
    store.mark(conn, b.id, "published", video_id="vidOLD")
    conn.execute("UPDATE item SET updated_at = ? WHERE id = ?", ("2026-10-05T02:00:00Z", b.id))

    c = ch(env, "CL")
    assert c.next_upload_at() == T0 + timedelta(hours=2)
    assert c.upload(up(env, slug="cl-hs-old", title="Cũ", when="2026-10-06T11:30:00Z")).video_id == "vidOLD"


# ── hồi quy từ review (Grok vòng 4 + review hai trục) ─────────────────────

def test_second_process_never_steals_a_reservation_that_is_still_opening_its_session(env):
    # publish_batch đã giữ slot, đang gọi khởi tạo phiên (chưa có URI) thì drip chen vào.
    from factory.youtube_api import UploadInterrupted
    clash = []

    def second_process():
        with pytest.raises(UploadInterrupted):
            ch(env).upload(up(env))
        clash.append("refused")

    env["yt"].before_session = second_process
    first = ch(env).upload(up(env))

    assert clash == ["refused"]
    assert env["yt"].inserts == 1
    assert ch(env).upload(up(env)).video_id == first.video_id


def test_a_reservation_abandoned_before_any_session_is_reclaimed_after_the_init_budget(env):
    # Tiến trình chết cứng (kill) sau khi giữ slot, trước khi có phiên: không có gì trên YouTube.
    ch(env)                                            # tạo sổ
    env["conn"].execute("INSERT INTO upload_log (channel, slug, title, state, publish_at, started_at, attempt) "
                        "VALUES ('FS', 'lich-20261010', 'Ngày 10/10 tốt cho việc gì', 'started', "
                        "'2026-10-10T23:00:00Z', '2026-10-05T02:30:00Z', 'dead')")

    res = ch(env).upload(up(env))
    assert env["yt"].inserts == 1 and not res.reused


def test_lost_response_leaves_the_ledger_pointing_at_the_adopted_video(env):
    from factory.youtube_api import UploadInterrupted
    env["yt"].fail_next_insert(UploadInterrupted("mất mạng ở chunk cuối"), completed=True)
    with pytest.raises(UploadInterrupted):
        ch(env).upload(up(env))

    adopted = ch(env).upload(up(env))
    again = ch(env).upload(up(env))
    assert again.reused and again.video_id == adopted.video_id == "vid0001"


def test_resolve_refuses_a_video_that_already_belongs_to_another_slug(env):
    from factory.youtube_api import PublishError
    other = ch(env).upload(up(env, slug="lich-x", title="X")).video_id
    _in_doubt(env)

    with pytest.raises(PublishError):
        ch(env, "CL").resolve("cl-hs-a", other)


def _legacy_item(env, slug, video_id, stage="published", updated="2026-10-05T02:00:00Z", title="Cũ"):
    from factory.bundle import Bundle
    b = Bundle(channel="CL", kind="short", slug=slug, script="Một câu đủ dài để kể chuyện. " * 8, title=title,
               description="d", tags=["x"], thumbnail_text="", publish_at="2026-10-06T11:30:00Z",
               voice="Anh Khôi", bgm="", broll_queries=["hyperframes-casefile"])
    store.save_bundle(b, base=env["tmp"] / "bundles")
    store.enqueue(b, env["conn"])
    env["conn"].execute("UPDATE item SET stage = ?, video_id = ?, updated_at = ? WHERE id = ?",
                        (stage, video_id, updated, b.id))


def test_backfill_skips_ids_shared_by_two_slugs_and_videos_that_are_not_published(env, monkeypatch):
    # 9 cặp Lịch từng dùng chung một video_id; video bị gỡ lịch vẫn giữ video_id nhưng stage=failed.
    monkeypatch.setattr(store, "BUNDLE_DIR", env["tmp"] / "bundles")
    _legacy_item(env, "cl-hs-a", "vidSHARED", updated="2026-10-01T00:00:00Z", title="A")
    _legacy_item(env, "cl-hs-b", "vidSHARED", updated="2026-10-01T00:00:00Z", title="B")
    _legacy_item(env, "cl-hs-c", "vidGONE", stage="failed", updated="2026-10-01T00:00:00Z", title="C")

    c = ch(env, "CL")
    assert c.upload(up(env, slug="cl-hs-a", title="A")).reused is False
    env["clock"].advance(hours=3)
    assert c.upload(up(env, slug="cl-hs-c", title="C")).reused is False


def test_backfilled_titles_still_catch_a_duplicate_on_another_slug(env, monkeypatch):
    from factory.channel import DuplicateTitle
    monkeypatch.setattr(store, "BUNDLE_DIR", env["tmp"] / "bundles")
    _legacy_item(env, "cl-hs-old", "vidOLD", updated="2026-10-01T00:00:00Z", title="Vượt ngục Alcatraz")

    with pytest.raises(DuplicateTitle):
        ch(env, "CL").upload(up(env, slug="cl-hs-new", title="Vượt ngục  ALCATRAZ"))


def test_a_long_transfer_keeps_its_lease_alive_so_nobody_else_takes_the_slug(env):
    # Grok vòng 5: lease 3 giờ mà không gia hạn -> video dài upload > 3 giờ thì tiến trình
    # khác giành dòng, PUT cùng phiên, và upload đầu không ghi được sổ.
    from factory.youtube_api import UploadInterrupted
    seen = []

    def slow_network(step):
        env["clock"].advance(hours=2)              # mỗi chunk 2 giờ: tổng 6 giờ > LEASE
        if step == 2:
            with pytest.raises(UploadInterrupted):
                ch(env).upload(up(env, kind="long", category="24"))
            seen.append("refused at 6h")

    env["yt"].progress_steps = 3
    env["yt"].during_upload = slow_network
    first = ch(env).upload(up(env, kind="long", category="24"))

    assert seen == ["refused at 6h"]
    assert env["yt"].inserts == 1
    again = ch(env).upload(up(env, kind="long", category="24"))
    assert again.reused and again.video_id == first.video_id


def test_a_process_that_lost_its_lease_stops_sending(env):
    from factory.youtube_api import UploadInterrupted

    def stolen(step):
        env["conn"].execute("UPDATE upload_log SET attempt = 'someone-else'")

    env["yt"].progress_steps = 2
    env["yt"].during_upload = stolen
    with pytest.raises(UploadInterrupted):
        ch(env).upload(up(env))
    assert env["yt"].inserts == 0


def test_hide_takes_a_public_video_private_and_keeps_every_other_status_field(env):
    # Đổi hướng kênh: ẩn video cũ. Đảo ngược được, không xoá.
    c = ch(env)
    vid = c.upload(up(env)).video_id
    env["yt"].go_live(vid)
    env["yt"].videos[vid]["status"].update(embeddable=False, license="creativeCommon")

    c.hide(vid)

    st = env["yt"].get_video(vid, "status")["status"]
    assert st["privacyStatus"] == "private" and "publishAt" not in st
    assert (st["embeddable"], st["license"]) == (False, "creativeCommon")


def test_hide_on_a_video_that_is_already_private_and_unscheduled_changes_nothing(env):
    c = ch(env)
    vid = c.upload(up(env, when=None), unscheduled=True).video_id
    calls = []
    real = env["yt"].update_video
    env["yt"].update_video = lambda part, body: (calls.append(part), real(part, body))

    c.hide(vid)

    assert calls == []


def test_hide_clears_the_schedule_in_the_ledger_too(env):
    c = ch(env)
    vid = c.upload(up(env)).video_id
    c.hide(vid)
    assert env["conn"].execute("SELECT publish_at FROM upload_log WHERE video_id = ?", (vid,)).fetchone()[0] is None


# ── nhận video upload tay (kênh upload = manual) ──────────────────────────

def test_adopt_records_a_manual_upload_with_its_real_upload_time(env):
    env["clock"].t = T0 - timedelta(minutes=100)              # 01:20 UTC
    vid = env["yt"].add_video({"title": "AI là gì?", "publishedAt": "2026-10-05T01:00:00Z"},
                              {"privacyStatus": "private"})
    ch(env, "MIM").adopt("mim-ai-la-gi", vid)
    row = env["conn"].execute("SELECT state, video_id, started_at FROM upload_log WHERE slug = 'mim-ai-la-gi'").fetchone()
    assert tuple(row) == ("done", vid, "2026-10-05T01:00:00Z")
    # Giãn nhịp MIM (60 phút) tính cả video upload tay: lượt kế tiếp sớm nhất 02:00.
    assert ch(env, "MIM").next_upload_at() == T0 - timedelta(hours=1)


def test_adopt_uses_now_when_published_at_is_in_the_future(env):
    # Studio đã đặt lịch: publishedAt có thể nhảy sang giờ lên sóng (tương lai) -- không phải giờ upload.
    vid = env["yt"].add_video({"title": "X", "publishedAt": "2026-10-20T01:00:00Z"}, {"privacyStatus": "private"})
    ch(env, "MIM").adopt("mim-x", vid)
    assert env["conn"].execute("SELECT started_at FROM upload_log WHERE slug='mim-x'").fetchone()[0] == "2026-10-05T03:00:00Z"


def test_adopt_refuses_a_video_that_does_not_exist(env):
    from factory.youtube_api import PublishError
    with pytest.raises(PublishError):
        ch(env, "MIM").adopt("mim-x", "vidNOPE")


def test_adopt_refuses_a_video_already_owned_by_another_slug(env):
    from factory.youtube_api import PublishError
    vid = env["yt"].add_video({"title": "X", "publishedAt": "2026-10-05T01:00:00Z"}, {"privacyStatus": "private"})
    ch(env, "MIM").adopt("mim-a", vid)
    with pytest.raises(PublishError):
        ch(env, "MIM").adopt("mim-b", vid)


def test_adopt_is_idempotent_for_the_same_video_and_refuses_a_different_one(env):
    from factory.youtube_api import PublishError
    v1 = env["yt"].add_video({"title": "X", "publishedAt": "2026-10-05T01:00:00Z"}, {"privacyStatus": "private"})
    v2 = env["yt"].add_video({"title": "Y", "publishedAt": "2026-10-05T01:00:00Z"}, {"privacyStatus": "private"})
    c = ch(env, "MIM")
    c.adopt("mim-a", v1)
    c.adopt("mim-a", v1)                                  # chạy lại: không đổi gì
    with pytest.raises(PublishError):
        c.adopt("mim-a", v2)
