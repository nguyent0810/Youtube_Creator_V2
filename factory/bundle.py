"""Bundle -- hợp đồng duy nhất giữa PHA SINH (chat) và PHA SẢN XUẤT (CLI).

Đây là file quan trọng nhất của v2. Mọi thứ khác đều phục vụ nó.

KIẾN TRÚC HIT & RUN: v1 nặng 26.000 dòng không phải vì logic nội dung phức
tạp, mà vì phải dựng lớp phòng thủ quanh những thứ không đáng tin -- quota
codex/agy, PATH tối giản của launchd, Google Drive làm database, registry
JSON + flock, fallback ba tầng nhà cung cấp. v2 bỏ hết bằng cách cắt pipeline
đúng ở chỗ THẬT SỰ cần trí tuệ:

    PHA SINH (trong chat, Claude tự viết + tự phản biện)
        -> Bundle: kịch bản + SEO + chữ thumbnail + giờ đăng, ĐẦY ĐỦ
    PHA SẢN XUẤT (CLI, chạy nền, KHÔNG có LLM nào)
        -> TTS -> dựng video -> thumbnail -> upload

Hệ quả thiết kế quan trọng: CLI KHÔNG ĐƯỢC PHÉP cần LLM. Nghĩa là mọi thứ
cần ngôn ngữ -- tiêu đề, mô tả, tag, chữ thumbnail -- phải nằm sẵn trong
Bundle. Nếu một trường nào đó "để CLI tự sinh sau", kiến trúc này sụp: CLI
lại cần API key, lại có quota, lại có fallback, và ta quay về v1.

Bundle là bản ghi BẤT BIẾN. Pha sản xuất chỉ đọc nó và ghi kết quả (đường
dẫn file, video_id) vào bảng trạng thái riêng -- không bao giờ sửa Bundle.
Nhờ vậy chạy lại luôn tái lập được, và một lần sinh hỏng không thể lặng lẽ
biến thành một lần sinh khác.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

SCHEMA_VERSION = 1

# YouTube ép cứng các giới hạn này; vượt là API trả lỗi lúc upload -- tức là
# phát hiện ở bước CUỐI, sau khi đã tốn TTS + render. Validate ngay lúc sinh
# để hỏng thì hỏng sớm và rẻ.
MAX_TITLE_CHARS = 100
MAX_DESCRIPTION_CHARS = 5000
MAX_TAGS_TOTAL_CHARS = 500

# Short phải <= 3 phút mới được YouTube xếp vào Shorts. Ta nhắm 25-45 giây:
# đủ dài để kể một ý trọn vẹn, đủ ngắn để giữ chân.
SHORT_MIN_WORDS = 35
SHORT_MAX_WORDS = 130

_ILLEGAL_TITLE = re.compile(r"[<>]")


class BundleInvalid(ValueError):
    """Bundle không đủ điều kiện đưa vào sản xuất.

    Cố ý là lỗi CỨNG, không phải cảnh báo: cả kiến trúc dựa trên giả định
    Bundle đã đầy đủ khi rời pha sinh. Một Bundle thiếu trường mà vẫn lọt
    xuống CLI sẽ hỏng ở bước upload -- sau khi đã tốn TTS và render."""


@dataclass(frozen=True)
class Bundle:
    """Một video hoàn chỉnh, đã sẵn sàng sản xuất mà không cần hỏi ai nữa."""

    channel: str              # "FS" | "BUD" | "CL"
    kind: str                 # "short" | "long"
    slug: str                 # định danh ổn định, dùng làm tên file
    script: str               # lời đọc -- ĐÚNG văn bản đưa vào TTS
    title: str
    description: str
    tags: list[str]
    thumbnail_text: str       # chữ phủ lên thumbnail (Long); Short để rỗng
    publish_at: str           # ISO-8601 UTC, luôn kết thúc bằng Z
    voice: str                # tên giọng vieneu
    bgm: str                  # tên file trong bgm/, hoặc "" nếu không nhạc nền
    broll_queries: list[str]  # từ khoá tìm B-roll, tiếng Anh, theo thứ tự cảnh
    source_note: str = ""     # nguồn/căn cứ -- để truy vết, không lên video
    schema_version: int = SCHEMA_VERSION
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    # ─── Định danh ────────────────────────────────────────────────────────

    @property
    def id(self) -> str:
        """Định danh tất định, suy từ NỘI DUNG chứ không phải thời điểm sinh.

        Cùng kênh + cùng slug -> cùng id, nên chạy lại pha sinh không tạo ra
        bản trùng. Cố ý KHÔNG băm cả script: sửa một chữ trong lời đọc vẫn
        phải là cùng một content item, nếu không mọi lần tinh chỉnh đều sinh
        ra một hàng mới trong hàng đợi."""
        return hashlib.sha256(f"{self.channel}|{self.kind}|{self.slug}".encode("utf-8")).hexdigest()[:16]

    @property
    def word_count(self) -> int:
        return len(self.script.split())

    # ─── Kiểm tra ─────────────────────────────────────────────────────────

    def validate(self) -> None:
        """Ném BundleInvalid nếu Bundle chưa đủ điều kiện sản xuất.

        Mỗi luật ở đây tương ứng một cách hỏng THẬT đã biết từ v1, không
        phải kiểm tra cho có."""
        err = []

        if self.channel not in ("FS", "BUD", "CL"):
            err.append(f"channel lạ: {self.channel!r}")
        if self.kind not in ("short", "long"):
            err.append(f"kind lạ: {self.kind!r}")
        if not self.slug or not re.fullmatch(r"[A-Za-z0-9_-]{3,80}", self.slug):
            err.append(f"slug phải là [A-Za-z0-9_-]{{3,80}}, nhận {self.slug!r}")

        # Kịch bản: thứ duy nhất KHÔNG thể sinh lại ở pha sản xuất.
        if not self.script.strip():
            err.append("script rỗng")
        elif self.kind == "short":
            n = self.word_count
            if not (SHORT_MIN_WORDS <= n <= SHORT_MAX_WORDS):
                err.append(f"short phải {SHORT_MIN_WORDS}-{SHORT_MAX_WORDS} từ, đang {n}")

        # Tiêu đề: YouTube từ chối '<' '>' và cắt cụt quá 100 ký tự.
        if not self.title.strip():
            err.append("title rỗng")
        if len(self.title) > MAX_TITLE_CHARS:
            err.append(f"title {len(self.title)} ký tự > {MAX_TITLE_CHARS}")
        if _ILLEGAL_TITLE.search(self.title):
            err.append("title chứa ký tự YouTube từ chối: < hoặc >")

        if len(self.description) > MAX_DESCRIPTION_CHARS:
            err.append(f"description {len(self.description)} ký tự > {MAX_DESCRIPTION_CHARS}")

        # Tag: YouTube tính TỔNG độ dài, không phải từng cái.
        total_tags = sum(len(t) for t in self.tags) + max(0, len(self.tags) - 1)
        if total_tags > MAX_TAGS_TOTAL_CHARS:
            err.append(f"tổng tag {total_tags} ký tự > {MAX_TAGS_TOTAL_CHARS}")
        if any(not t.strip() for t in self.tags):
            err.append("có tag rỗng")

        # publish_at: sai múi giờ là đăng nhầm giờ, im lặng và khó phát hiện.
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", self.publish_at):
            err.append(f"publish_at phải là ISO-8601 UTC kết thúc bằng Z, nhận {self.publish_at!r}")
        else:
            try:
                datetime.strptime(self.publish_at, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                err.append(f"publish_at không phải ngày giờ hợp lệ: {self.publish_at!r}")

        if not self.voice.strip():
            err.append("voice rỗng -- pha sản xuất không có cách nào tự chọn giọng")
        if not self.broll_queries:
            err.append("broll_queries rỗng -- không có gì để dựng hình")
        if any(not q.strip() for q in self.broll_queries):
            err.append("có broll_query rỗng")

        # Long BẮT BUỘC có chữ thumbnail; Short thì không dùng tới.
        if self.kind == "long" and not self.thumbnail_text.strip():
            err.append("long thiếu thumbnail_text")

        if err:
            raise BundleInvalid(f"Bundle {self.channel}/{self.slug}: " + "; ".join(err))

    # ─── Tuần tự hoá ──────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True)

    @classmethod
    def from_dict(cls, data: dict) -> "Bundle":
        got = data.get("schema_version", 1)
        if got != SCHEMA_VERSION:
            raise BundleInvalid(
                f"schema_version {got} không khớp {SCHEMA_VERSION} -- "
                "bundle sinh bởi bản khác, đừng đoán ý nghĩa các trường."
            )
        known = {f for f in cls.__dataclass_fields__}
        unknown = set(data) - known
        if unknown:
            raise BundleInvalid(f"trường lạ trong bundle: {sorted(unknown)}")
        return cls(**{k: v for k, v in data.items() if k in known})

    @classmethod
    def from_json(cls, text: str) -> "Bundle":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise BundleInvalid(f"không parse được JSON: {exc}") from exc
        return cls.from_dict(data)


def make_slug(text: str, max_len: int = 60) -> str:
    """Biến tiêu đề tiếng Việt thành slug an toàn cho tên file/định danh.

    Bỏ dấu qua NFD rồi lọc ký tự tổ hợp -- giữ được ý nghĩa ("Người sống và
    người mất" -> "Nguoi-song-va-nguoi-mat") thay vì băm ra chuỗi hash vô
    nghĩa. v1 có đúng lỗi này: tên file kiểu "Nmkinhinccaphongthy" do lọc
    thô ký tự có dấu, nhìn vào không đoán nổi nội dung gì."""
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    stripped = stripped.replace("đ", "d").replace("Đ", "D")
    ascii_only = re.sub(r"[^A-Za-z0-9]+", "-", stripped).strip("-")
    slug = re.sub(r"-{2,}", "-", ascii_only)[:max_len].strip("-")
    return slug or "untitled"
