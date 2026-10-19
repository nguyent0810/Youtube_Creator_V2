"""Bước 4: một hợp đồng Bundle + một kho cho mọi format (đề xuất 2 của audit).

Thiết kế: docs/audit/2026-10-05-one-store-design.md.
"""
import json
from datetime import datetime, timedelta, timezone

import pytest

from factory import store
from factory.bundle import Bundle, BundleInvalid


def bundle(**kw):
    f = dict(channel="FS", kind="short", slug="lich-x", script="Một câu đủ dài để kể chuyện. " * 8,
             title="T", description="d", tags=["x"], thumbnail_text="", publish_at="2026-11-01T23:00:00Z",
             voice="Anh Khôi", bgm="", broll_queries=["sky"])
    f.update(kw)
    return Bundle(**f)


@pytest.fixture
def conn(tmp_path):
    with store.connect(tmp_path / "state.sqlite") as c:
        yield c


# ── 1. Bundle: trường render tuỳ chọn, schema vẫn là 1 ───────────────────

def test_old_bundle_json_without_render_still_loads_as_assemble():
    d = bundle().to_dict()
    d.pop("render")
    b = Bundle.from_dict(d)
    assert b.engine == "assemble" and b.schema_version == 1


def test_casefile_and_casewide_need_a_spec_but_no_broll():
    bundle(render={"engine": "casefile", "spec": "data/stier/specs/x.json"}, broll_queries=[]).validate()
    with pytest.raises(BundleInvalid):
        bundle(render={"engine": "casefile"}, broll_queries=[]).validate()       # thiếu spec
    with pytest.raises(BundleInvalid):
        bundle(broll_queries=[]).validate()                                       # assemble vẫn cần b-roll
    with pytest.raises(BundleInvalid):
        bundle(render={"engine": "lạ", "spec": "x"}).validate()


def test_mim_is_an_allowed_channel_and_render_round_trips():
    b = bundle(channel="MIM", slug="mim-ai-la-gi", render={"engine": "casefile", "spec": "s.json"}, broll_queries=[])
    b.validate()
    assert Bundle.from_json(b.to_json()) == b


# ── 2. Cột engine của hàng đợi ────────────────────────────────────────────

def test_engine_column_is_backfilled_from_the_slug_when_it_is_first_added(tmp_path):
    path = tmp_path / "old.sqlite"
    with store.connect(path) as c:            # DB cũ: chưa có cột engine
        c.execute("ALTER TABLE item DROP COLUMN engine")
        for slug in ("cl-hs-alcatraz", "long-kowloon", "lich-1"):
            c.execute("INSERT INTO item (id, channel, kind, slug, publish_at, updated_at) "
                      "VALUES (?, 'CL', 'short', ?, '2026-11-01T00:00:00Z', 'x')", (slug, slug))
    with store.connect(path) as c:
        got = {r["slug"]: r["engine"] for r in c.execute("SELECT slug, engine FROM item")}
    assert got == {"cl-hs-alcatraz": "casefile", "long-kowloon": "casewide", "lich-1": "assemble"}


def test_enqueue_writes_the_engine_and_next_batch_can_filter_on_it(conn):
    store.enqueue(bundle(slug="lich-a"), conn)
    store.enqueue(bundle(channel="CL", slug="cl-hs-b", render={"engine": "casefile", "spec": "s"},
                         broll_queries=[]), conn)
    assert [r["slug"] for r in store.next_batch(conn, "pending", engine="assemble")] == ["lich-a"]
    assert {r["slug"] for r in store.next_batch(conn, "pending")} == {"lich-a", "cl-hs-b"}


# ── 3. Giành việc (claim) cho TTS / dựng ──────────────────────────────────

NOW = datetime(2026, 10, 6, 3, 0, tzinfo=timezone.utc)


def test_a_claimed_row_is_not_handed_to_a_second_worker(conn):
    store.enqueue(bundle(slug="lich-a"), conn)
    first = store.claim(conn, "pending", "w1", engine="assemble", now=NOW)
    second = store.claim(conn, "pending", "w2", engine="assemble", now=NOW)
    assert first["slug"] == "lich-a" and second is None


def test_an_expired_lease_can_be_reclaimed(conn):
    store.enqueue(bundle(slug="lich-a"), conn)
    store.claim(conn, "pending", "w1", engine="assemble", now=NOW)
    later = NOW + store.CLAIM_LEASE + timedelta(seconds=1)
    assert store.claim(conn, "pending", "w2", engine="assemble", now=later)["slug"] == "lich-a"


@pytest.mark.parametrize("finish", [
    lambda c, i: store.mark(c, i, "spoken"),
    lambda c, i: store.bump_attempt(c, i, "lỗi"),
    lambda c, i: store.defer(c, i, "tạm", "2000-01-01T00:00:00Z"),
    lambda c, i: store.reject(c, i, "nội dung"),
])
def test_every_way_of_finishing_a_row_releases_its_claim(conn, finish):
    b = bundle(slug="lich-a")
    store.enqueue(b, conn)
    store.claim(conn, "pending", "w1", engine="assemble", now=NOW)
    finish(conn, b.id)
    row = conn.execute("SELECT claimed_by, lease_until FROM item WHERE id = ?", (b.id,)).fetchone()
    assert tuple(row) == (None, None)


def test_requeued_failures_come_back_unclaimed(conn):
    b = bundle(slug="lich-a")
    store.enqueue(b, conn)
    store.claim(conn, "pending", "w1", engine="assemble", now=NOW)
    conn.execute("UPDATE item SET stage='failed', attempts=1, fail_stage='pending' WHERE id = ?", (b.id,))
    store.requeue_failed(conn)
    assert store.claim(conn, "pending", "w2", engine="assemble", now=NOW)["slug"] == "lich-a"


def test_claim_respects_retry_after_and_max_attempts(conn):
    a, b = bundle(slug="lich-a"), bundle(slug="lich-b")
    store.enqueue(a, conn)
    store.enqueue(b, conn)
    conn.execute("UPDATE item SET retry_after = '2999-01-01T00:00:00Z' WHERE id = ?", (a.id,))
    conn.execute("UPDATE item SET attempts = 3 WHERE id = ?", (b.id,))
    assert store.claim(conn, "pending", "w1", engine="assemble", now=NOW) is None


def test_legacy_s_tier_bundles_without_render_still_queue_as_casefile(conn):
    # Review: 91 bundle cl-hs- trên đĩa không có render (broll "hyperframes-casefile").
    # sync_from_disk vào DB mới không được biến chúng thành short assemble (B-roll Pexels).
    store.enqueue(bundle(channel="CL", slug="cl-hs-alcatraz", broll_queries=["hyperframes-casefile"]), conn)
    assert conn.execute("SELECT engine FROM item WHERE slug='cl-hs-alcatraz'").fetchone()[0] == "casefile"
    assert store.next_batch(conn, "pending", engine="assemble") == []


def test_two_connections_never_claim_the_same_row(tmp_path):
    path = tmp_path / "state.sqlite"
    with store.connect(path) as a, store.connect(path) as b:
        store.enqueue(bundle(slug="lich-a"), a)
        store.enqueue(bundle(slug="lich-b"), a)
        got = [store.claim(c, "pending", w, engine="assemble", now=NOW) for c, w in ((a, "w1"), (b, "w2"), (a, "w1"))]
    assert sorted(r["slug"] for r in got[:2]) == ["lich-a", "lich-b"] and got[2] is None
