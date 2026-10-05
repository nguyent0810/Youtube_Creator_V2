"""Channel -- MỘT cửa cho mọi lần ghi lên YouTube của một kênh (mọi đường chạy
định kỳ; hai script một lần repair_titles.py / week_2026-10-05.py chưa chuyển).

VÌ SAO (audit 05/10/2026, docs/audit/2026-10-05-channel-design.md): trước đây
11 file tự gọi YouTube, luật giãn nhịp chỉ nằm trong drip.py, và chống trùng
bằng TIÊU ĐỀ. Hệ quả có thật:
  - 30/09 kênh CL nhận 61 video/ngày (~53 trong 47 phút), 1-2 ngày sau Shorts
    rơi khỏi feed -- publish_batch không biết luật của drip;
  - 9 ngày Lịch trùng tiêu đề bị "chống trùng" trả về video_id của ngày khác,
    store ghi là đã đăng (scripts/repair_titles.py).

Module này giữ CHÍNH SÁCH; nói chuyện với YouTube là việc của adapter
(factory/youtube_api.py thật, factory/youtube_fake.py cho test):
  - định danh = (kênh, slug), không bao giờ là tiêu đề;
  - sổ upload_log trong state.sqlite: dòng `started` là chỗ giữ slot giãn
    nhịp, ghi TRƯỚC mọi HTTP; session URI lưu trước byte đầu tiên;
  - privacy luôn private khi đặt lịch; sửa video là merge, không ghi đè.
"""
from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from factory import channels, store
from factory.youtube_api import HttpYouTube, PublishError, SessionDead, UploadInterrupted, YouTubeApi

SHORTS_MARKER = "#Shorts"
DEFAULT_CATEGORY = "22"      # People & Blogs -- giá trị upload_video cũ, giữ nguyên cho short

_ISO = "%Y-%m-%dT%H:%M:%SZ"

# Tiến trình đang upload một slug giữ LEASE tới mốc này. Tiến trình khác thấy
# lease còn hạn thì lùi (UploadInterrupted) chứ không xoá hay nối tiếp phiên
# của nó -- publish_batch và drip có thể cùng nhặt một item CL. Chết cứng
# giữa chừng thì lease hết hạn và slug được xử lý lại. 3 giờ: đủ cho file
# video dài qua mạng nhà.
LEASE = timedelta(hours=3)

# Toàn bộ trường GHI ĐƯỢC của từng part (tài liệu videos.update). Merge = giá
# trị hiện tại của mọi trường này + phần đổi. Thiếu một trường là YouTube xoá
# trắng nó -- set_schedule cũ làm rơi defaultAudioLanguage, reschedule.py phải
# nhớ gửi lại embeddable/license bằng tay.
_SNIPPET_WRITABLE = ("title", "description", "tags", "categoryId", "defaultLanguage",
                     "defaultAudioLanguage")
_STATUS_WRITABLE = ("privacyStatus", "publishAt", "embeddable", "license", "publicStatsViewable",
                    "selfDeclaredMadeForKids", "containsSyntheticMedia")


def _writable(part: dict, keys: tuple[str, ...]) -> dict:
    return {k: part[k] for k in keys if k in part}

_SCHEMA = """
CREATE TABLE IF NOT EXISTS upload_log (
    channel      TEXT NOT NULL,
    slug         TEXT NOT NULL,
    title        TEXT,
    state        TEXT NOT NULL,          -- started | done
    video_id     TEXT,
    session_uri  TEXT,
    publish_at   TEXT,                   -- NULL = upload không hẹn giờ (probe)
    started_at   TEXT NOT NULL,          -- giờ giữ slot = giờ upload, dùng cho giãn nhịp
    done_at      TEXT,
    attempt      TEXT,                   -- lần thử đang giữ dòng này
    lease_until  TEXT,                   -- NULL / đã qua = không ai đang upload
    PRIMARY KEY (channel, slug)
);
"""


class DuplicateTitle(PublishError):
    """Tiêu đề đã thuộc về MỘT VIDEO KHÁC (slug khác, hoặc video có sẵn trên
    kênh). Không bao giờ coi đó là "đã đăng": đó là lỗi nội dung, người sửa."""

    def __init__(self, title: str, video_id: str | None):
        super().__init__(f"tiêu đề đã có trên kênh (video {video_id}): {title!r}")
        self.video_id = video_id


class PacingHold(PublishError):
    """Chưa tới lượt upload theo luật giãn nhịp của kênh. Lỗi tạm: caller
    hoãn tới `until` (store.defer), không tính là hỏng."""

    def __init__(self, code: str, until: datetime):
        super().__init__(f"kênh {code}: chưa tới lượt upload, chờ tới {_iso(until)}")
        self.until = until


@dataclass(frozen=True)
class Pacing:
    min_gap: timedelta
    max_per_24h: int

    @classmethod
    def for_channel(cls, code: str) -> "Pacing":
        gap_min, cap = channels.CHANNELS[code]["pacing"]
        return cls(timedelta(minutes=gap_min), cap)


def _norm_title(t: str) -> str:
    """Hoa/thường và khoảng trắng không làm hai tiêu đề khác nhau. Dấu tiếng
    Việt thì CÓ: "Mệnh Kim" và "Mệnh Kìm" là hai tiêu đề."""
    return " ".join(t.split()).casefold()


def _ensure_ledger(conn: sqlite3.Connection) -> None:
    """Tạo upload_log. Lần ĐẦU tạo thì chép video đã đăng từ `item` vào sổ.

    Không có bước này thì ngay sau khi triển khai, sổ rỗng sẽ cho CL upload
    sát video drip vừa đăng. Chỉ chép thứ CHẮC là của slug đó:
      - chỉ stage 'published' -- item bị gỡ lịch (unschedule) vẫn giữ video_id
        nhưng video đã mất lịch, chép thành 'done' là gán nhầm lịch cũ;
      - bỏ video_id dùng chung bởi 2 slug -- 9 ngày Lịch từng nhận video của
        ngày khác (repair_titles.py); chép vào là đóng băng cái sai đó.
    Giờ upload lấy item.updated_at: đúng với item đăng bằng publish_batch /
    upload_one; script sửa lịch có thể đóng dấu muộn hơn -> chỉ làm giãn nhịp
    chặt hơn trong tối đa 24 giờ, không bao giờ lỏng hơn."""
    fresh = conn.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'upload_log'"
                         ).fetchone() is None
    conn.executescript(_SCHEMA)
    if not fresh or not conn.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'item'"
                                     ).fetchone():
        return
    rows = list(conn.execute(
        "SELECT channel, slug, video_id, publish_at, updated_at FROM item "
        "WHERE stage = 'published' AND video_id IS NOT NULL AND video_id != '' "
        "AND video_id IN (SELECT video_id FROM item WHERE video_id IS NOT NULL "
        "                 GROUP BY video_id HAVING COUNT(*) = 1)"))
    for r in rows:
        try:
            title = store.load_bundle(r["channel"], r["slug"]).title
        except Exception:
            title = None            # thiếu bundle: chống trùng dựa vào channel_titles
        conn.execute(
            "INSERT OR IGNORE INTO upload_log "
            "(channel, slug, title, state, video_id, publish_at, started_at, done_at) "
            "VALUES (?, ?, ?, 'done', ?, ?, ?, ?)",
            (r["channel"], r["slug"], title, r["video_id"], r["publish_at"],
             r["updated_at"], r["updated_at"]))


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _iso(t: datetime) -> str:
    return t.astimezone(timezone.utc).strftime(_ISO)


@dataclass(frozen=True)
class Upload:
    slug: str
    video: Path
    title: str
    description: str
    tags: tuple[str, ...]
    kind: str                       # short | long
    publish_at: str | None          # ISO Z; None chỉ khi unscheduled=True
    category: str | None = None     # None -> mặc định kênh (chỉ cho short)
    thumbnail: Path | None = None


@dataclass(frozen=True)
class Uploaded:
    video_id: str
    url: str
    publish_at: str | None
    reused: bool
    thumbnail_error: str | None = None   # thumbnail là best-effort, không làm hỏng upload


class Channel:
    def __init__(self, code: str, api: YouTubeApi | None, conn: sqlite3.Connection, *, now=_utcnow,
                 channel_titles: dict[str, str] | None = None, pacing: Pacing | None = None):
        """`channel_titles`: tiêu đề -> video_id đang có trên kênh (chụp một lần
        mỗi lô bằng publish.channel_titles), để bắt trùng với video không do
        sổ này đăng -- v1, đăng tay, hoặc trước khi có sổ.

        api=None: chỉ hỏi giãn nhịp / sổ (drip), không cần credential."""
        self.code = code
        self.api = api
        self.conn = conn
        self.now = now
        self._titles = {_norm_title(t): v for t, v in (channel_titles or {}).items()}
        self.pacing = pacing or Pacing.for_channel(code)
        _ensure_ledger(conn)

    @classmethod
    def open(cls, code: str, conn: sqlite3.Connection, *,
             channel_titles: dict[str, str] | None = None) -> "Channel":
        """Kênh thật: credential trong channels.CREDS_DIR + HttpYouTube. Token
        lấy lười, nên mở Channel chỉ để hỏi next_upload_at() không tốn mạng."""
        creds = json.loads(channels.creds_path(code).read_text(encoding="utf-8"))
        return cls(code, HttpYouTube(creds), conn, channel_titles=channel_titles)

    def next_upload_at(self) -> datetime:
        """Mốc sớm nhất được upload tiếp. Bộ lập lịch (drip) hỏi cái này thay
        vì tự giữ đồng hồ riêng."""
        now = self.now()
        times = [datetime.strptime(r[0], _ISO).replace(tzinfo=timezone.utc) for r in self.conn.execute(
            "SELECT started_at FROM upload_log WHERE channel = ? AND started_at > ? ORDER BY started_at",
            (self.code, _iso(now - timedelta(hours=24))))]
        at = now
        if times:
            at = max(at, times[-1] + self.pacing.min_gap)
        if len(times) >= self.pacing.max_per_24h:
            at = max(at, times[len(times) - self.pacing.max_per_24h] + timedelta(hours=24))
        return at

    def unfinished(self) -> list[str]:
        """Slug đang có upload dở dang (giữ slot, chưa xong)."""
        return [r[0] for r in self.conn.execute(
            "SELECT slug FROM upload_log WHERE channel = ? AND state = 'started' ORDER BY started_at",
            (self.code,))]

    def upload(self, u: Upload, *, unscheduled: bool = False) -> Uploaded:
        """Upload private + hẹn giờ. Idempotent theo (kênh, slug).

        unscheduled=True (probe): private KHÔNG lịch -- không bao giờ tự công
        khai. Upload lại cùng slug với lịch sau đó sẽ dùng lại video và gán
        lịch, không upload lần hai.

        Ném: PacingHold, QuotaExceeded, UploadInterrupted, UploadInDoubt (đều
        là lỗi tạm hoặc chờ người, caller KHÔNG tính là hỏng), DuplicateTitle,
        PublishError."""
        self._check(u, unscheduled)
        row = self._row(u.slug)
        if row and row["state"] == "done":
            publish_at = row["publish_at"]
            if publish_at is None and u.publish_at:
                # Video probe (private không lịch) đã được duyệt: gán lịch.
                self.reschedule(row["video_id"], u.publish_at)
                publish_at = u.publish_at
            return Uploaded(row["video_id"], f"https://youtu.be/{row['video_id']}",
                            publish_at, reused=True)
        attempt, resume_uri = self._take(u)
        session_saved = resume_uri is not None

        def save_session(uri: str) -> None:
            nonlocal session_saved
            self.conn.execute("UPDATE upload_log SET session_uri = ? "
                              "WHERE channel = ? AND slug = ? AND attempt = ?",
                              (uri, self.code, u.slug, attempt))
            session_saved = True

        def heartbeat() -> None:
            # Gia hạn lease suốt lúc gửi byte. Mất quyền (tiến trình khác đã
            # giành dòng sau khi lease cũ hết) thì dừng gửi ngay.
            cur = self.conn.execute(
                "UPDATE upload_log SET lease_until = ? WHERE channel = ? AND slug = ? AND attempt = ?",
                (_iso(self.now() + LEASE), self.code, u.slug, attempt))
            if cur.rowcount == 0:
                raise UploadInterrupted(f"{self.code}/{u.slug}: mất lease, tiến trình khác đã giành")

        try:
            vid = self.api.insert_video(self._meta(u), u.video, resume_uri=resume_uri,
                                        on_session=save_session, on_progress=heartbeat)
        except SessionDead:
            self._forget(u.slug, attempt)   # YouTube xác nhận phiên hỏng, không có video
            raise
        except BaseException:
            # Đã có phiên thì KHÔNG xoá: mất phản hồi ở chunk cuối có thể là
            # video đã tạo xong. Lần sau hỏi lại phiên.
            if session_saved:
                self._release(u.slug, attempt)
            else:
                self._forget(u.slug, attempt)
            raise
        self._mark_done(u.slug, vid, attempt)
        self._titles[_norm_title(u.title)] = vid
        thumb_err = None
        if u.thumbnail:
            # Sau khi đã ghi `done`: lỗi ở đây mà ném ra thì caller sẽ ghi một
            # video đang có trên kênh là "hỏng".
            try:
                self.api.set_thumbnail(vid, u.thumbnail)
            except Exception as exc:
                thumb_err = f"{type(exc).__name__}: {exc}"
        return Uploaded(vid, f"https://youtu.be/{vid}", u.publish_at, reused=False,
                        thumbnail_error=thumb_err)

    def set_thumbnail(self, video_id: str, jpg: Path) -> None:
        self.api.set_thumbnail(video_id, jpg)

    def reschedule(self, video_id: str, publish_at: str | None) -> None:
        """Đặt lại (hoặc gỡ, khi None) lịch của video ĐANG private.

        videos.update ghi đè cả part status: gửi lại MỌI trường ghi được với
        giá trị hiện tại, chỉ đổi lịch. Video đã public thì từ chối -- đặt
        private lại là gỡ một video đang sống xuống."""
        cur = self.api.get_video(video_id, "status")
        if cur is None:
            raise PublishError(f"không thấy video {video_id} trên kênh")
        st = cur["status"]
        if st.get("privacyStatus") != "private":
            raise PublishError(f"video {video_id} đang {st.get('privacyStatus')} -- không đặt lịch lại")
        if publish_at is not None:
            self._check_future(publish_at)
        body = _writable(st, _STATUS_WRITABLE)
        body["selfDeclaredMadeForKids"] = st.get("selfDeclaredMadeForKids", st.get("madeForKids", False))
        body["privacyStatus"] = "private"
        body.pop("publishAt", None)
        if publish_at is not None:
            body["publishAt"] = publish_at
        self.api.update_video("status", {"id": video_id, "status": body})
        self.conn.execute("UPDATE upload_log SET publish_at = ? WHERE channel = ? AND video_id = ?",
                          (publish_at, self.code, video_id))

    def edit(self, video_id: str, **changes) -> None:
        """Sửa snippet (tiêu đề, mô tả, tag, category, ngôn ngữ). KHÔNG BAO GIỜ
        đụng status, nên không thể vô tình gỡ một video đang public."""
        bad = set(changes) - set(_SNIPPET_WRITABLE)
        if bad:
            raise PublishError(f"edit chỉ sửa snippet {_SNIPPET_WRITABLE}, không sửa {sorted(bad)}")
        cur = self.api.get_video(video_id, "snippet")
        if cur is None:
            raise PublishError(f"không thấy video {video_id} trên kênh")
        body = {**_writable(cur["snippet"], _SNIPPET_WRITABLE), **changes}
        self.api.update_video("snippet", {"id": video_id, "snippet": body})

    def resolve(self, slug: str, video_id: str | None) -> None:
        """Người xử lý một upload UploadInDoubt sau khi đã nhìn kênh.

        video_id = video thật của slug này -> ghi `done`. None = chắc chắn
        không có video -> xoá dòng, trả slot, lần sau upload lại."""
        row = self._row(slug)
        if not row or row["state"] != "started":
            raise PublishError(f"{self.code}/{slug} không có upload dở dang để xử lý")
        if video_id is None:
            self._forget(slug)
            return
        # video_id là duy nhất trên TOÀN YouTube: kiểm trên mọi kênh trong sổ.
        owner = self.conn.execute("SELECT channel, slug FROM upload_log WHERE video_id = ? "
                                  "AND NOT (channel = ? AND slug = ?)",
                                  (video_id, self.code, slug)).fetchone()
        if owner:
            raise PublishError(f"video {video_id} đã là của {owner[0]}/{owner[1]} -- không gán cho {slug}")
        if self.api.get_video(video_id, "status") is None:
            raise PublishError(f"không thấy video {video_id} trên kênh -- không ghi sổ")
        self._mark_done(slug, video_id, row["attempt"])

    def _check(self, u: Upload, unscheduled: bool) -> None:
        if unscheduled and u.publish_at:
            raise PublishError(f"{u.slug}: probe (unscheduled) không được có publish_at")
        if not unscheduled:
            if not u.publish_at:
                raise PublishError(f"{u.slug}: thiếu publish_at -- chỉ probe mới được đăng không lịch")
            self._check_future(u.publish_at)
        if u.kind == "long" and not u.category:
            raise PublishError(f"{u.slug}: video dài phải có category")

    def _check_future(self, publish_at: str) -> None:
        when = datetime.strptime(publish_at, _ISO).replace(tzinfo=timezone.utc)
        if when <= self.now():
            raise PublishError(f"publishAt {publish_at} không ở tương lai -- YouTube sẽ công khai ngay")

    def _take(self, u: Upload) -> tuple[str, str | None]:
        """Giành quyền upload slug này, trong MỘT transaction ghi, trước mọi HTTP.

        Trả (attempt, resume_uri). Dòng mới: kiểm trùng tiêu đề + giãn nhịp
        rồi giữ slot -- hai tiến trình không thể cùng lọt qua trần. Dòng dở
        dang có phiên: slot đã tính từ lần trước, chỉ gia hạn lease để nối
        tiếp. Lease của người khác còn hạn: lùi lại."""
        attempt = uuid.uuid4().hex
        now = self.now()
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self._row(u.slug)
            if row and row["lease_until"] and row["lease_until"] > _iso(now):
                raise UploadInterrupted(f"{self.code}/{u.slug}: tiến trình khác đang upload "
                                        f"(lease tới {row['lease_until']})")
            if row and row["session_uri"]:
                self.conn.execute("UPDATE upload_log SET attempt = ?, lease_until = ? "
                                  "WHERE channel = ? AND slug = ?",
                                  (attempt, _iso(now + LEASE), self.code, u.slug))
                resume = row["session_uri"]
            else:
                if row:     # giữ slot rồi chết trước khi có phiên: YouTube chưa có gì
                    self.conn.execute("DELETE FROM upload_log WHERE channel = ? AND slug = ?",
                                      (self.code, u.slug))
                self._refuse_duplicate_title(u)
                at = self.next_upload_at()
                if at > now:
                    raise PacingHold(self.code, at)
                self.conn.execute(
                    "INSERT INTO upload_log (channel, slug, title, state, publish_at, started_at, "
                    "attempt, lease_until) VALUES (?, ?, ?, 'started', ?, ?, ?, ?)",
                    (self.code, u.slug, u.title, u.publish_at, _iso(now), attempt, _iso(now + LEASE)))
                resume = None
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise
        self.conn.execute("COMMIT")
        return attempt, resume

    def _mark_done(self, slug: str, video_id: str, attempt: str | None) -> None:
        """Ghi `done`. Có video_id là có BẰNG CHỨNG video tồn tại, nên kể cả
        khi dòng đã đổi chủ (lease lỡ hết hạn) vẫn phải ghi -- trừ khi dòng
        đã `done` với video KHÁC: hai video cho một slug, người phải xem."""
        done_at = _iso(self.now())
        cur = self.conn.execute(
            "UPDATE upload_log SET state = 'done', video_id = ?, done_at = ?, lease_until = NULL "
            "WHERE channel = ? AND slug = ? AND attempt IS ?",
            (video_id, done_at, self.code, slug, attempt))
        if cur.rowcount:
            return
        cur = self.conn.execute(
            "UPDATE upload_log SET state = 'done', video_id = ?, done_at = ?, lease_until = NULL "
            "WHERE channel = ? AND slug = ? AND state = 'started'",
            (video_id, done_at, self.code, slug))
        if cur.rowcount:
            return
        row = self._row(slug)
        if row is None or row["video_id"] != video_id:
            raise PublishError(f"{self.code}/{slug}: video {video_id} lên kênh nhưng sổ đang ghi "
                               f"{row['video_id'] if row else 'không có dòng'} -- kiểm Studio, có thể trùng")

    def _release(self, slug: str, attempt: str) -> None:
        self.conn.execute("UPDATE upload_log SET lease_until = NULL "
                          "WHERE channel = ? AND slug = ? AND attempt = ?", (self.code, slug, attempt))

    def _refuse_duplicate_title(self, u: Upload) -> None:
        key = _norm_title(u.title)
        for r in self.conn.execute("SELECT slug, title, video_id FROM upload_log "
                                   "WHERE channel = ? AND slug != ? AND title IS NOT NULL",
                                   (self.code, u.slug)):
            if _norm_title(r["title"]) == key:
                raise DuplicateTitle(u.title, r["video_id"])
        if key in self._titles:
            raise DuplicateTitle(u.title, self._titles[key])

    def _forget(self, slug: str, attempt: str | None = None) -> None:
        """Xoá dòng dở dang -> trả slot. Có `attempt` thì chỉ xoá nếu dòng vẫn
        là của lần thử đó (không xoá nhầm dòng tiến trình khác vừa giành)."""
        self.conn.execute("DELETE FROM upload_log WHERE channel = ? AND slug = ? AND state = 'started' "
                          "AND (? IS NULL OR attempt = ?)", (self.code, slug, attempt, attempt))

    def _row(self, slug: str) -> sqlite3.Row | None:
        return self.conn.execute("SELECT * FROM upload_log WHERE channel = ? AND slug = ?",
                                 (self.code, slug)).fetchone()

    def _meta(self, u: Upload) -> dict:
        description = u.description
        if u.kind == "short" and SHORTS_MARKER.lower() not in description.lower():
            description = f"{description}\n\n{SHORTS_MARKER}".strip()
        status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False}
        if u.publish_at:
            status["publishAt"] = u.publish_at
        return {
            "snippet": {"title": u.title, "description": description, "tags": list(u.tags),
                        "categoryId": u.category or DEFAULT_CATEGORY,
                        "defaultLanguage": "vi", "defaultAudioLanguage": "vi"},
            "status": status,
        }
