"""Video dài vào cùng kho với short (bước 4, docs/audit/2026-10-05-one-store-design.md)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "motion" / "long"))
import publish_long as pl  # noqa: E402

from factory import store  # noqa: E402
from factory.channel import Channel  # noqa: E402
from factory.youtube_fake import FakeYouTube  # noqa: E402


@pytest.fixture
def env(tmp_path):
    sd, od = tmp_path / "data" / "long" / "kowloon", tmp_path / "out"
    sd.mkdir(parents=True)
    od.mkdir()
    (sd / "spec.json").write_text(json.dumps({
        "title": "Cửu Long Thành Trại ngoài đời thật", "chapters": ["ch00", "ch01"],
        "youtube": {"tags": ["kowloon"], "sources": ["https://en.wikipedia.org/wiki/Kowloon_Walled_City"]}}),
        encoding="utf-8")
    (sd / "ch00.json").write_text(json.dumps({"lines": [{"t": "Chương một.", "p": 0.8}, "Câu hai."]}), encoding="utf-8")
    (sd / "ch01.json").write_text(json.dumps({"lines": ["Câu ba."]}), encoding="utf-8")
    (od / "description.txt").write_text("Mô tả dài.", encoding="utf-8")
    yt = FakeYouTube()
    with store.connect(tmp_path / "state.sqlite") as conn:
        yield {"conn": conn, "sd": sd, "od": od, "bundles": tmp_path / "bundles", "yt": yt,
               "chan": Channel("CL", yt, conn)}


def bundle(env, when="2026-11-01T12:00:00Z"):
    return pl.long_bundle("kowloon", "CL", when, env["sd"], env["od"])


def row(env, b):
    return tuple(env["conn"].execute("SELECT stage, video_id, engine FROM item WHERE id = ?", (b.id,)).fetchone())


def test_a_long_video_gets_a_casewide_bundle_built_from_its_spec(env):
    b = bundle(env)
    b.validate()
    assert (b.kind, b.slug, b.engine) == ("long", "long-kowloon", "casewide")
    assert b.render["spec"] == "data/long/kowloon/spec.json"
    assert b.script == "Chương một. Câu hai. Câu ba."


def test_register_queues_the_built_video_as_assembled(env):
    b = bundle(env)
    pl.register(env["conn"], b, {}, env["od"] / "final.mp4", env["chan"], env["bundles"])
    assert row(env, b) == ("assembled", None, "casewide")
    assert store.load_bundle("CL", "long-kowloon", env["bundles"]) == b


def test_rerunning_after_upload_never_demotes_published_back_to_assembled(env):
    # Chạy lại publish_long để thêm playlist: video đã lên kênh, không được
    # trông như đang chờ upload (export_manual / publish_batch sẽ đăng lại).
    b = bundle(env)
    pl.register(env["conn"], b, {}, env["od"] / "final.mp4", env["chan"], env["bundles"])
    store.mark(env["conn"], b.id, "published", video_id="vidL")
    pl.register(env["conn"], b, {}, env["od"] / "final.mp4", env["chan"], env["bundles"])
    assert row(env, b)[:2] == ("published", "vidL")


def test_a_video_id_in_result_json_marks_an_old_upload_published_and_puts_it_in_the_ledger(env):
    # Video dài upload trước khi có kho chung: result.json là bằng chứng. Vòng phản
    # hồi chỉ đo video trong upload_log -> phải ghi sổ, không chỉ đổi stage (Grok).
    b = bundle(env)
    old = env["yt"].add_video({"title": "Cửu Long", "publishedAt": "2026-09-20T12:00:00Z"},
                              {"privacyStatus": "public"})
    pl.register(env["conn"], b, {"video_id": old}, env["od"] / "final.mp4", env["chan"], env["bundles"])
    pl.register(env["conn"], b, {"video_id": old}, env["od"] / "final.mp4", env["chan"], env["bundles"])
    assert row(env, b)[:2] == ("published", old)
    led = env["conn"].execute("SELECT state, video_id, started_at FROM upload_log WHERE slug = 'long-kowloon'").fetchone()
    assert tuple(led) == ("done", old, "2026-09-20T12:00:00Z")


def test_the_first_bundle_on_disk_is_kept(env):
    first = bundle(env)
    pl.register(env["conn"], first, {}, env["od"] / "final.mp4", env["chan"], env["bundles"])
    pl.register(env["conn"], bundle(env, "2026-12-01T12:00:00Z"), {}, env["od"] / "final.mp4", env["chan"], env["bundles"])
    assert store.load_bundle("CL", "long-kowloon", env["bundles"]).publish_at == first.publish_at
