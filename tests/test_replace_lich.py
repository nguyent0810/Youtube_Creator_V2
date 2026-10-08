"""Công cụ thay video Lịch sai (N1): xếp nhóm đúng, làm đúng thứ tự, chạy lại an toàn.

Không gọi mạng: trạng thái YouTube và lệnh gỡ lịch đều là bản giả.
"""
import json
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from factory import publish, store

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import replace_lich as R  # noqa: E402

SLUGS = ["lich-20261015", "lich-20261016", "lich-20261017", "lich-20261018", "lich-20261019", "lich-20261020"]
LEAD = timedelta(hours=12)


@pytest.fixture
def env(tmp_path, monkeypatch):
    """6 ngày Lịch thật (bundle SAI dữ kiện, như trên kênh), store riêng, YouTube giả."""
    for s in SLUGS:
        dst = tmp_path / "bundles" / "FS" / f"{s}.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / "bundles" / "FS" / f"{s}.json", dst)
    monkeypatch.setattr(store, "BUNDLE_DIR", tmp_path / "bundles")
    monkeypatch.setattr(store, "DB_PATH", tmp_path / "state.sqlite")
    monkeypatch.setattr(R, "ARCHIVE", tmp_path / "archive")
    yt, calls = {}, []

    def status(ids, tok):
        return {i: dict(yt[i]) for i in ids if i in yt}

    def unschedule(vid, tok, prefix):
        calls.append(vid)
        if yt[vid].get("fail"):
            raise publish.PublishError("403 forbidden")
        yt[vid] = {**yt[vid], "title": prefix + yt[vid]["title"], "publishAt": None}

    return {"yt": yt, "calls": calls, "status": status, "unschedule": unschedule, "tmp": tmp_path}


def _bundle(slug):
    return store.load_bundle("FS", slug)


def _upload(env, slug, privacy="private", scheduled=True):
    b = _bundle(slug)
    with store.connect() as conn:
        store.enqueue(b, conn)
        store.mark(conn, b.id, "published", video_id="V" + slug[-4:])
    env["yt"]["V" + slug[-4:]] = {"title": b.title, "privacyStatus": privacy,
                                  "publishAt": b.publish_at if scheduled and privacy == "private" else None}


def _slot(slug):
    return publish.parse_publish_at(_bundle(slug).publish_at)


def _plan(env, now, keep_near=False):
    days, ok, text = R.plan("FS", None, None, now, LEAD, keep_near, "tok", status_fn=env["status"])
    return {d.slug: d for d in days}, ok, text


def test_every_case_lands_in_the_right_group(env):
    now = _slot("lich-20261017") - timedelta(hours=1)          # 17/10 sát giờ, 15-16/10 đã qua
    _upload(env, "lich-20261015", privacy="public")             # đã phát
    _upload(env, "lich-20261016", scheduled=True)               # còn hẹn nhưng giờ đã qua -> chỉ gỡ được
    env["yt"]["V1016"]["publishAt"] = (now + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    _upload(env, "lich-20261017")                               # còn 1 giờ: thay sát
    _upload(env, "lich-20261018")                               # còn > 12 giờ: thay
    with store.connect() as conn:                               # 19/10: có trong hàng đợi, chưa đăng
        store.enqueue(_bundle("lich-20261019"), conn)
    #                                                             20/10: chỉ có bundle, chưa vào hàng đợi
    days, ok, _ = _plan(env, now)
    got = {s: d.group for s, d in days.items()}
    assert got == {"lich-20261015": "ĐÃ PHÁT", "lich-20261016": "GỠ", "lich-20261017": "THAY-SÁT",
                   "lich-20261018": "THAY", "lich-20261019": "CHƯA ĐĂNG", "lich-20261020": "CHƯA ĐĂNG"}
    assert ok


def test_keep_near_leaves_near_days_alone(env):
    now = _slot("lich-20261017") - timedelta(hours=1)
    _upload(env, "lich-20261017")
    days, _, _ = _plan(env, now, keep_near=True)
    assert days["lich-20261017"].group == "LỠ" and not days["lich-20261017"].unschedule


def test_apply_replaces_and_a_second_run_is_a_no_op(env):
    now = _slot("lich-20261015") - timedelta(days=2)
    for s in SLUGS[:4]:
        _upload(env, s)
    days, ok, _ = _plan(env, now)
    assert ok and {d.group for d in days.values()} == {"THAY", "CHƯA ĐĂNG"}
    old_titles = {s: _bundle(s).title for s in SLUGS}
    done = R.apply(list(days.values()), "tok", now, unschedule_fn=env["unschedule"])
    assert done["gỡ lịch"] == 4 and done["bundle mới"] == 6 and done["về pending"] == 6 and done["lỗi"] == 0
    with store.connect() as conn:
        rows = {r["slug"]: dict(r) for r in conn.execute("SELECT * FROM item")}
    assert all(r["stage"] == "pending" and r["video_id"] is None for r in rows.values())
    for s in SLUGS:
        assert _bundle(s).title != old_titles[s]                                  # bundle đã là bản mới
        assert rows[s]["publish_at"] == _bundle(s).publish_at
    assert all(v["title"].startswith(R.TITLE_TAG) and not v["publishAt"] for v in env["yt"].values())
    arch = sorted((env["tmp"] / "archive" / "FS").glob("*.json"))
    assert len(arch) == 6
    a = json.loads(arch[0].read_text(encoding="utf-8"))
    assert a["bundle"]["title"] == old_titles["lich-20261015"] and a["old_video_id"] == "V1015"
    again, _, _ = _plan(env, now)                                                   # chạy lại
    assert {d.group for d in again.values()} == {"ĐÚNG"}


def test_failed_unschedule_leaves_that_day_untouched(env):
    now = _slot("lich-20261015") - timedelta(days=2)
    _upload(env, "lich-20261015")
    env["yt"]["V1015"]["fail"] = True
    before = (store.BUNDLE_DIR / "FS" / "lich-20261015.json").read_text(encoding="utf-8")
    days, _, _ = _plan(env, now)
    done = R.apply([days["lich-20261015"]], "tok", now, unschedule_fn=env["unschedule"])
    assert done["lỗi"] == 1 and done["bundle mới"] == 0
    assert (store.BUNDLE_DIR / "FS" / "lich-20261015.json").read_text(encoding="utf-8") == before
    with store.connect() as conn:
        assert conn.execute("SELECT video_id FROM item").fetchone()["video_id"] == "V1015"


def test_interrupted_run_is_finished_next_time(env):
    """Dừng sau khi ghi bundle mới mà chưa sửa store: lần sau không được coi là ĐÚNG."""
    now = _slot("lich-20261015") - timedelta(days=2)
    _upload(env, "lich-20261015")
    days, _, _ = _plan(env, now)
    d = days["lich-20261015"]
    env["unschedule"]("V1015", "tok", R.TITLE_TAG)          # bước 1 xong
    store.save_bundle(d.new, overwrite=True)                # bước 2 xong, "mất điện" trước bước 3
    again, _, _ = _plan(env, now)
    assert again["lich-20261015"].group == "KHÔI PHỤC" and again["lich-20261015"].reset
    R.apply(list(again.values()), "tok", now, unschedule_fn=env["unschedule"])
    with store.connect() as conn:
        r = conn.execute("SELECT stage, video_id FROM item").fetchone()
    assert (r["stage"], r["video_id"]) == ("pending", None)


def test_replacement_batch_has_no_verbatim_duplicate(env, tmp_path):
    """09/11 và 03/12/2026 từng ra kịch bản giống hệt nhau (offset biến thể reset mỗi tháng)."""
    from datetime import date

    from factory import lich, lunar
    a, _, _ = lich.build_bundle(lunar.facts_for(date(2026, 11, 9)))
    b, _, _ = lich.build_bundle(lunar.facts_for(date(2026, 12, 3)))
    assert a.script != b.script


# ─── publish.unschedule ───────────────────────────────────────────────────

def _video(monkeypatch, status, title="Tiêu đề"):
    sent = {}
    cur = {"snippet": {"title": title, "description": "D", "tags": ["a"], "categoryId": "27",
                       "defaultLanguage": "vi", "defaultAudioLanguage": "vi"},
           "status": {"embeddable": False, "license": "youtube", "publicStatsViewable": True,
                      "selfDeclaredMadeForKids": False, **status}}
    monkeypatch.setattr(publish, "video_status", lambda vid, tok: json.loads(json.dumps(cur)))
    monkeypatch.setattr(publish, "_api", lambda tok, method, path, params=None, payload=None: sent.update(payload or {}))
    return sent


def _future(hours=48):
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_unschedule_drops_publish_at_keeps_the_rest_and_tags_title_once(monkeypatch):
    sent = _video(monkeypatch, {"privacyStatus": "private", "publishAt": _future()})
    publish.unschedule("V", "tok", R.TITLE_TAG)
    assert "publishAt" not in sent["status"] and sent["status"]["privacyStatus"] == "private"
    assert sent["status"]["embeddable"] is False and sent["snippet"]["description"] == "D"
    assert sent["snippet"]["title"] == R.TITLE_TAG + "Tiêu đề"
    sent = _video(monkeypatch, {"privacyStatus": "private"}, title=R.TITLE_TAG + "Tiêu đề")
    publish.unschedule("V", "tok", R.TITLE_TAG)
    assert sent["snippet"]["title"] == R.TITLE_TAG + "Tiêu đề"


@pytest.mark.parametrize("status", [{"privacyStatus": "public"}, {"privacyStatus": "unlisted"},
                                    {"privacyStatus": "private", "publishAt": _future(hours=0.01)}])
def test_unschedule_never_touches_live_or_about_to_go_live_videos(monkeypatch, status):
    sent = _video(monkeypatch, status)
    with pytest.raises(publish.PublishError):
        publish.unschedule("V", "tok", R.TITLE_TAG)
    assert sent == {}
