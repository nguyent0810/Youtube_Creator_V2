"""Chế độ upload TAY cho kênh `upload="manual"` (factory/channels.py).

VÌ SAO (05/10/2026): MIM nối qua GCP project CHƯA audit -- mọi video upload
bằng API bị khoá private vĩnh viễn, kể cả đổi tay trong Studio. Nên với kênh
này máy làm mọi thứ TRỪ upload:

    dựng video (run_batch / motion) -> export(): gói output/manual/<CH>/<slug>/
    người upload gói đó qua YouTube Studio (dán tiêu đề, mô tả, tag, hẹn giờ)
    adopt(): đọc upload gần đây của kênh, nhận ra video nhờ token yf-<slug>,
             ghi sổ upload_log (giãn nhịp + vòng phản hồi thấy video) và đánh
             dấu item `published`.

Nhận diện bằng TOKEN, không bằng tiêu đề: người hay sửa tiêu đề trong Studio,
và hai video có thể trùng tiêu đề. Token nằm ở hai chỗ -- một tag (người xem
không thấy) và dòng cuối mô tả (phòng khi quên dán tag). Phải khớp NGUYÊN tag
hoặc NGUYÊN dòng cuối: yf-mim-a không được khớp nhầm yf-mim-a-2. Không còn
token nào thì người chỉ định: adopt_one(slug, video_id).

Thiết kế: docs/audit/2026-10-05-one-store-design.md.
"""
from __future__ import annotations

import shutil
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

from factory import channels, store
from factory.bundle import MAX_DESCRIPTION_CHARS, MAX_TAGS_TOTAL_CHARS
from factory.channel import SHORTS_MARKER, Channel
from factory.publish import PublishError

TOKEN_PREFIX = "yf-"


def token(slug: str) -> str:
    return f"{TOKEN_PREFIX}{slug}"


def _description(b) -> str:
    """Mô tả y như đường API (Channel._meta thêm #Shorts cho short) + dòng token."""
    d = b.description
    if b.kind == "short" and SHORTS_MARKER.lower() not in d.lower():
        d = f"{d}\n\n{SHORTS_MARKER}".strip()
    return f"{d}\n\n{token(b.slug)}"


def _vn(iso_z: str) -> str:
    return (datetime.strptime(iso_z, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M")


def _tags(b) -> list[str]:
    return list(b.tags) + [token(b.slug)]


def _fits(b) -> None:
    """Bundle đã validate, nhưng token + #Shorts thêm vào SAU: vượt giới hạn thì
    Studio cắt/từ chối đúng phần cuối -- chính là token. Hỏng sớm, ở đây."""
    tags = _tags(b)
    total = sum(len(t) for t in tags) + len(tags) - 1
    if total > MAX_TAGS_TOTAL_CHARS:
        raise ValueError(f"{b.slug}: tag + token {total} ký tự > {MAX_TAGS_TOTAL_CHARS} -- bớt tag trong bundle")
    if len(_description(b)) > MAX_DESCRIPTION_CHARS:
        raise ValueError(f"{b.slug}: mô tả + token {len(_description(b))} ký tự > {MAX_DESCRIPTION_CHARS}")


def _meta_txt(b) -> str:
    return (f"[TIÊU ĐỀ]\n{b.title}\n\n"
            f"[MÔ TẢ]\n{_description(b)}\n\n"
            f"[TAGS]\n{', '.join(_tags(b))}\n\n"
            f"[LOẠI] {b.kind}    [HẸN GIỜ GỢI Ý] {_vn(b.publish_at)} (giờ VN)\n"
            f"Upload: Private -> đặt lịch (Schedule) đúng giờ trên. Đừng xoá tag/dòng cuối "
            f"`{token(b.slug)}`: máy dùng nó để nhận lại video (adopt_manual.py).\n")


def _ready(conn: sqlite3.Connection, ch: str) -> list[sqlite3.Row]:
    rows = store.next_batch(conn, "assembled", limit=500, channel=ch)
    return [r for r in rows if r["slug"].startswith(channels.prefixes(ch)) and r["video_path"]]


def export(conn: sqlite3.Connection, ch: str, out_root: Path, *, bundles: Path | None = None) -> list[Path]:
    """Ghi gói upload cho mọi item `assembled` của kênh. Chạy lại vô hại
    (file video giống hệt thì không chép lại). Không đổi stage: item vẫn chờ
    tới khi adopt thấy video trên kênh."""
    out = []
    for r in _ready(conn, ch):
        b = store.load_bundle(ch, r["slug"], bundles)
        _fits(b)
        d = out_root / ch / b.slug
        d.mkdir(parents=True, exist_ok=True)
        src, dst = Path(r["video_path"]), d / f"{b.slug}.mp4"
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copyfile(src, dst)
        if r["thumb_path"] and Path(r["thumb_path"]).exists():
            shutil.copyfile(r["thumb_path"], d / f"thumbnail{Path(r['thumb_path']).suffix}")
        (d / "meta.txt").write_text(_meta_txt(b), encoding="utf-8")
        out.append(d)
    return out


def _tokens_of(video: dict) -> set[str]:
    sn = video.get("snippet") or {}
    got = {t.strip() for t in sn.get("tags") or [] if t.strip().startswith(TOKEN_PREFIX)}
    lines = [ln.strip() for ln in (sn.get("description") or "").strip().splitlines()]
    if lines and lines[-1].startswith(TOKEN_PREFIX):
        got.add(lines[-1])
    return {t[len(TOKEN_PREFIX):] for t in got}


@dataclass
class Report:
    adopted: dict[str, str] = field(default_factory=dict)        # slug -> video_id
    ambiguous: dict[str, list[str]] = field(default_factory=dict)  # slug -> nhiều video
    unknown: dict[str, str] = field(default_factory=dict)        # token không có item chờ
    conflicts: dict[str, str] = field(default_factory=dict)      # slug -> lý do


def adopt(chan: Channel, conn: sqlite3.Connection, videos: list[dict]) -> Report:
    """Ghi sổ mọi video trong `videos` (upload gần đây của kênh) mang token
    của một item đang chờ. Không đoán: hai video cùng token -> báo, không ghi."""
    seen: dict[str, list[str]] = {}
    for v in videos:
        for slug in _tokens_of(v):
            seen.setdefault(slug, []).append(v["id"])
    rep = Report()
    for slug, vids in sorted(seen.items()):
        vids = sorted(set(vids))
        row = conn.execute("SELECT id, stage, video_id FROM item WHERE channel = ? AND slug = ?",
                           (chan.code, slug)).fetchone()
        if len(vids) > 1:                                # kể cả khi đã nhận một bản:
            rep.ambiguous[slug] = vids                   # bản thừa vẫn sẽ tự công khai
        elif row is not None and row["stage"] == "published" and row["video_id"] == vids[0]:
            continue                                     # đã nhận ở lần trước
        elif row is None or row["stage"] != "assembled":
            rep.unknown[slug] = vids[0]
        else:
            try:
                _adopt(chan, conn, row["id"], slug, vids[0])
                rep.adopted[slug] = vids[0]
            except PublishError as exc:
                rep.conflicts[slug] = str(exc)
    return rep


def adopt_one(chan: Channel, conn: sqlite3.Connection, slug: str, video_id: str, uploads: list[dict]) -> None:
    """Người chỉ định video cho slug (token đã bị xoá khi upload). Video phải nằm
    trong `uploads` (upload gần đây của CHÍNH kênh): videos.list trả cả video
    công khai của kênh khác, gõ nhầm id là ghi sổ video của người khác."""
    if video_id not in {v["id"] for v in uploads}:
        raise PublishError(f"{video_id} không nằm trong {len(uploads)} upload gần nhất của kênh {chan.code} "
                           f"-- sai id, hoặc tăng --limit")
    row = conn.execute("SELECT id, stage FROM item WHERE channel = ? AND slug = ?", (chan.code, slug)).fetchone()
    if row is None or row["stage"] not in ("assembled", "published"):
        raise PublishError(f"{chan.code}/{slug} không có trong hàng đợi ở chặng assembled "
                           f"({row['stage'] if row else 'không có'}) -- không ghi sổ")
    _adopt(chan, conn, row["id"], slug, video_id)


def _adopt(chan: Channel, conn: sqlite3.Connection, item_id: str, slug: str, video_id: str) -> None:
    chan.adopt(slug, video_id)
    store.mark(conn, item_id, "published", video_id=video_id)
