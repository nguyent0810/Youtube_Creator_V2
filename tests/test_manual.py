"""Chế độ upload TAY (kênh upload=manual, vd MIM trên project chưa audit).

Máy dựng video + xuất gói upload; người upload qua YouTube Studio; máy nhận
lại video bằng token `yf-<slug>` (tag, hoặc dòng cuối mô tả) và ghi sổ.
Thiết kế: docs/audit/2026-10-05-one-store-design.md.
"""
from datetime import datetime, timezone

import pytest

from factory import manual, store
from factory.bundle import Bundle
from factory.channel import Channel, ManualChannel, Upload
from factory.youtube_fake import FakeYouTube

NOW = datetime(2026, 10, 6, 3, 0, tzinfo=timezone.utc)


def bundle(slug="mim-ai-la-gi", channel="MIM", **kw):
    f = dict(channel=channel, kind="short", slug=slug, script="Một câu đủ dài để kể chuyện. " * 8,
             title=f"Tiêu đề {slug}", description="AI là gì, nói gọn trong 40 giây.", tags=["ai", "công nghệ"],
             thumbnail_text="", publish_at="2026-10-07T12:00:00Z", voice="Anh Khôi", bgm="",
             broll_queries=["robot"])
    f.update(kw)
    return Bundle(**f)


@pytest.fixture
def env(tmp_path):
    yt = FakeYouTube()
    video = tmp_path / "final.mp4"
    video.write_bytes(b"\0" * 64)
    with store.connect(tmp_path / "state.sqlite") as conn:
        yield {"yt": yt, "conn": conn, "video": video, "tmp": tmp_path, "bundles": tmp_path / "bundles"}


def assembled(env, b):
    store.save_bundle(b, env["bundles"])
    store.enqueue(b, env["conn"])
    store.mark(env["conn"], b.id, "assembled", video_path=str(env["video"]))


def chan(env):
    return Channel("MIM", env["yt"], env["conn"], now=lambda: NOW)


def stage(env, b):
    return tuple(env["conn"].execute("SELECT stage, video_id FROM item WHERE id = ?", (b.id,)).fetchone())


# ── 1. Kênh manual: máy KHÔNG upload ─────────────────────────────────────

def test_a_manual_channel_refuses_every_api_upload(env):
    u = Upload(slug="mim-x", video=env["video"], title="X", description="d", tags=(), kind="short",
               publish_at="2026-10-07T12:00:00Z")
    with pytest.raises(ManualChannel):
        chan(env).upload(u)
    assert env["yt"].inserts == 0
    assert env["conn"].execute("SELECT COUNT(*) FROM upload_log").fetchone()[0] == 0


# ── 2. Xuất gói upload ────────────────────────────────────────────────────

def test_export_writes_the_video_and_everything_to_paste_into_studio(env):
    b = bundle()
    assembled(env, b)
    out = env["tmp"] / "manual"
    got = manual.export(env["conn"], "MIM", out, bundles=env["bundles"])

    d = out / "MIM" / b.slug
    assert got == [d]
    assert (d / f"{b.slug}.mp4").read_bytes() == env["video"].read_bytes()
    meta = (d / "meta.txt").read_text(encoding="utf-8")
    assert b.title in meta
    assert "#Shorts" in meta                         # giống hệt mô tả đường API
    assert "yf-mim-ai-la-gi" in meta.split("[TAGS]")[1]                    # tag token
    assert meta.split("[MÔ TẢ]")[1].split("[TAGS]")[0].strip().endswith("yf-mim-ai-la-gi")
    assert "07/10/2026 19:00" in meta                # giờ VN gợi ý từ publish_at


def test_export_skips_other_channels_unready_items_and_foreign_prefixes(env):
    assembled(env, bundle("mim-a"))
    store.enqueue(bundle("mim-chua-dung"), env["conn"])                   # chưa dựng
    store.enqueue(bundle("mim-c"), env["conn"])
    assembled(env, bundle("lich-x", channel="FS"))
    got = manual.export(env["conn"], "MIM", env["tmp"] / "manual", bundles=env["bundles"])
    assert [p.name for p in got] == ["mim-a"]


def test_export_again_is_harmless(env):
    assembled(env, bundle())
    out = env["tmp"] / "manual"
    manual.export(env["conn"], "MIM", out, bundles=env["bundles"])
    assert manual.export(env["conn"], "MIM", out, bundles=env["bundles"]) == [out / "MIM" / "mim-ai-la-gi"]


# ── 3. Nhận lại video đã upload tay ──────────────────────────────────────

def studio_upload(env, b, *, tag=True, desc=True, published="2026-10-06T02:00:00Z"):
    """Người dán gói vào Studio. tag/desc=False: quên dán tag / sửa mất dòng cuối mô tả."""
    tok = manual.token(b.slug)
    return env["yt"].add_video(
        {"title": b.title, "publishedAt": published, "tags": list(b.tags) + ([tok] if tag else []),
         "description": b.description + (f"\n\n{tok}" if desc else "")},
        {"privacyStatus": "private", "publishAt": "2026-10-07T12:00:00Z"})


def test_adopt_finds_the_video_by_its_tag_and_marks_the_item_published(env):
    b = bundle()
    assembled(env, b)
    vid = studio_upload(env, b, desc=False)
    rep = manual.adopt(chan(env), env["conn"], env["yt"].list_uploads(50))
    assert rep.adopted == {b.slug: vid}
    assert stage(env, b) == ("published", vid)
    row = env["conn"].execute("SELECT state, video_id FROM upload_log WHERE slug = ?", (b.slug,)).fetchone()
    assert tuple(row) == ("done", vid)


def test_the_description_line_is_the_fallback_when_the_tag_was_not_pasted(env):
    b = bundle()
    assembled(env, b)
    vid = studio_upload(env, b, tag=False)
    assert manual.adopt(chan(env), env["conn"], env["yt"].list_uploads(50)).adopted == {b.slug: vid}


def test_the_token_must_be_the_whole_tag_or_last_line_not_any_substring(env):
    b, longer = bundle("mim-a"), bundle("mim-a-2")
    assembled(env, b)
    assembled(env, longer)
    vid = studio_upload(env, longer)
    rep = manual.adopt(chan(env), env["conn"], env["yt"].list_uploads(50))
    assert rep.adopted == {"mim-a-2": vid}
    assert stage(env, b) == ("assembled", None)


def test_videos_without_a_token_are_left_alone(env):
    b = bundle()
    assembled(env, b)
    env["yt"].add_video({"title": b.title, "publishedAt": "2026-10-06T02:00:00Z", "description": "x"},
                        {"privacyStatus": "public"})
    rep = manual.adopt(chan(env), env["conn"], env["yt"].list_uploads(50))
    assert rep.adopted == {} and stage(env, b) == ("assembled", None)


def test_two_videos_claiming_one_slug_are_reported_not_guessed(env):
    b = bundle()
    assembled(env, b)
    v1, v2 = studio_upload(env, b), studio_upload(env, b)
    rep = manual.adopt(chan(env), env["conn"], env["yt"].list_uploads(50))
    assert rep.adopted == {} and rep.ambiguous == {b.slug: sorted([v1, v2])}
    assert stage(env, b) == ("assembled", None)


def test_a_token_for_a_slug_not_waiting_in_the_queue_is_reported(env):
    b = bundle()
    vid = studio_upload(env, b)                       # chưa từng enqueue
    rep = manual.adopt(chan(env), env["conn"], env["yt"].list_uploads(50))
    assert rep.adopted == {} and rep.unknown == {b.slug: vid}


def test_adopt_again_is_harmless(env):
    b = bundle()
    assembled(env, b)
    studio_upload(env, b)
    manual.adopt(chan(env), env["conn"], env["yt"].list_uploads(50))
    rep = manual.adopt(chan(env), env["conn"], env["yt"].list_uploads(50))
    assert rep.adopted == {} and rep.unknown == {}


def test_a_human_can_pin_the_video_when_no_token_survived(env):
    b = bundle()
    assembled(env, b)
    vid = studio_upload(env, b, tag=False, desc=False)
    manual.adopt_one(chan(env), env["conn"], b.slug, vid, env["yt"].list_uploads(50))
    assert stage(env, b) == ("published", vid)


def test_pinning_a_slug_that_is_not_in_the_queue_is_refused(env):
    from factory.publish import PublishError
    vid = studio_upload(env, bundle(), tag=False, desc=False)
    with pytest.raises(PublishError):
        manual.adopt_one(chan(env), env["conn"], "mim-khong-co", vid, env["yt"].list_uploads(50))
    assert env["conn"].execute("SELECT COUNT(*) FROM upload_log").fetchone()[0] == 0


def test_pinning_an_item_that_was_never_built_is_refused(env):
    from factory.publish import PublishError
    b = bundle()
    store.enqueue(b, env["conn"])                     # pending: chưa dựng, chưa export
    vid = studio_upload(env, b, tag=False, desc=False)
    with pytest.raises(PublishError):
        manual.adopt_one(chan(env), env["conn"], b.slug, vid, env["yt"].list_uploads(50))
    assert stage(env, b) == ("pending", None)


def test_a_second_copy_is_reported_even_after_the_first_was_adopted(env):
    # Review: người upload cùng gói hai lần, adopt chạy giữa hai lần -> bản thứ hai
    # tự công khai theo lịch mà không ai biết.
    b = bundle()
    assembled(env, b)
    v1 = studio_upload(env, b)
    manual.adopt(chan(env), env["conn"], env["yt"].list_uploads(50))
    v2 = studio_upload(env, b)
    rep = manual.adopt(chan(env), env["conn"], env["yt"].list_uploads(50))
    assert rep.ambiguous == {b.slug: sorted([v1, v2])}
    assert stage(env, b) == ("published", v1)


def test_pinning_a_video_that_is_not_among_this_channels_uploads_is_refused(env):
    # Gõ nhầm --video-id thành video công khai của kênh khác: videos.list vẫn trả về.
    from factory.publish import PublishError
    b = bundle()
    assembled(env, b)
    vid = studio_upload(env, b, tag=False, desc=False)
    with pytest.raises(PublishError):
        manual.adopt_one(chan(env), env["conn"], b.slug, vid, [])
    assert stage(env, b) == ("assembled", None)


def test_export_refuses_a_package_whose_token_would_not_fit(env):
    # Review: tag token / dòng token thêm vào sau validate -> vượt 500 / 5000 ký tự,
    # Studio cắt mất chính token.
    b = bundle(tags=["x" * 54] * 9)                     # 9*54 + 8 = 494 <= 500; + token (15+1) = 510
    assembled(env, b)
    with pytest.raises(ValueError, match="token"):
        manual.export(env["conn"], "MIM", env["tmp"] / "manual", bundles=env["bundles"])
