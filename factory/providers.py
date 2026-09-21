"""Nguồn hình: video Pexels + ẢNH Pexels, trộn theo cảnh.

VÌ SAO CẦN ẢNH, KHÔNG PHẢI CHỈ VIDEO: đo thật trên API Pexels (19/09/2026),
`total_results` bị chặn ở 8.000 nên phần lớn truy vấn chung đều chạm trần và
không so sánh được. Nhưng đúng hai truy vấn rơi xuống DƯỚI trần, và cả hai
đều là video:

    vietnamese altar incense   video 6.510  |  ảnh 8.000 (trần)
    bagua compass              video 5.689  |  ảnh 8.000 (trần)

Đó chính là hai truy vấn ĐẶC THÙ nhất. Tín hiệu: càng đi vào hình ảnh riêng
của phong thuỷ/Việt Nam, kho video càng mỏng trong khi kho ảnh vẫn dày. Nên
ảnh không phải phương án chữa cháy -- nó bắt buộc nếu muốn hình ĐÚNG nội
dung thay vì hình chung chung.

═══ QUYẾT ĐỊNH THIẾT KẾ CHÍNH ═══
Ảnh tĩnh được CHUYỂN THÀNH CLIP VIDEO ngay trong bước download, chứ không
truyền ảnh xuống đường ống.

Lý do: pipeline của video-editor giả định mọi đầu vào là video có thời
lượng -- nó probe duration, chia slot, ghép xfade, áp Ken Burns. Để dạy nó
hiểu ảnh tĩnh thì phải sửa filtergraph (thêm -loop 1 -t N cho đúng những
input là ảnh), tức đụng vào phần phức tạp và được test kỹ nhất của họ.

Đổi ảnh thành clip N giây ở biên vào thì TOÀN BỘ phần sau không cần biết gì
cả: probe ra duration thật, Ken Burns chạy y như với video thường, xfade
không đổi. Một lệnh ffmpeg ở đúng một chỗ, đổi lấy việc không phải vá thêm
bất cứ thứ gì.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
VIDEO_TOOL_ROOT = ROOT.parent / "video-editor"
FFMPEG = VIDEO_TOOL_ROOT / "vendor" / "ffmpeg" / "ffmpeg.exe"

PHOTO_SEARCH_URL = "https://api.pexels.com/v1/search"

# Thời lượng clip sinh từ ảnh. Dài hơn slot cảnh (4s) một chút để đường ống
# luôn có dư mà cắt -- thiếu vài phần mười giây là cảnh bị hụt.
PHOTO_CLIP_SEC = 8.0
PHOTO_CLIP_FPS = 30

DEFAULT_TIMEOUT = 20.0


def _ensure_importable() -> None:
    if str(VIDEO_TOOL_ROOT) not in sys.path:
        sys.path.insert(0, str(VIDEO_TOOL_ROOT))


class PexelsPhotoProvider:
    """Ảnh Pexels, trả về dưới dạng clip video để đường ống không phải đổi.

    Cùng API key với provider video -- đã kiểm chứng key hiện tại chạy được
    cả hai endpoint, không cần xin thêm gì."""

    name = "pexels_photo"

    def __init__(self, api_key: str, clip_sec: float = PHOTO_CLIP_SEC,
                 width: int = 1080, height: int = 1920):
        _ensure_importable()
        from core.stockfootage.providers.base import raise_for_provider_status  # noqa: F401
        self._key = api_key
        self._clip_sec = clip_sec
        self._w, self._h = width, height
        self._client = httpx.Client(timeout=DEFAULT_TIMEOUT,
                                    headers={"Authorization": api_key,
                                             "User-Agent": "yt-factory/2.0"})

    def search(self, query: str, orientation: str = "portrait", per_page: int = 15):
        _ensure_importable()
        from core.stockfootage.models import StockClip
        from core.stockfootage.providers.base import raise_for_provider_status

        resp = self._client.get(PHOTO_SEARCH_URL, params={
            "query": query, "per_page": per_page,
            # Short là 9:16 -> xin ảnh dọc. Ảnh ngang bị crop mất hai bên,
            # thường cắt đúng chủ thể.
            "orientation": "portrait" if orientation != "landscape" else "landscape",
        })
        raise_for_provider_status(resp, self.name)

        out = []
        for photo in resp.json().get("photos", []):
            src = photo.get("src", {})
            # "original" là bản gốc, có thể rất lớn; "large2x" đủ cho 1080px
            # và tải nhanh hơn nhiều.
            url = src.get("large2x") or src.get("original") or src.get("large")
            if not url:
                continue
            out.append(StockClip(
                id=f"photo_{photo['id']}",
                provider=self.name,
                query=query,
                thumbnail_url=src.get("medium", ""),
                download_url=url,
                width=int(photo.get("width") or 0),
                height=int(photo.get("height") or 0),
                # duration là thời lượng clip SẼ sinh ra, không phải của ảnh.
                # Đường ống dùng số này để chia slot nên phải khớp thực tế.
                duration=self._clip_sec,
                source_page_url=photo.get("url", ""),
            ))
        return out

    def download(self, clip, dest_path: Path) -> Path:
        """Tải ảnh rồi encode thành clip tĩnh N giây.

        `dest_path` do đường ống đặt tên (đuôi .mp4) -- ta tải ảnh ra file
        tạm cạnh đó rồi ghi đè bằng clip, nên phần sau không thấy khác biệt."""
        dest_path = Path(dest_path)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_img = dest_path.with_suffix(".src.jpg")

        with self._client.stream("GET", clip.download_url) as r:
            if r.status_code >= 400:
                raise RuntimeError(f"tải ảnh lỗi {r.status_code}: {clip.download_url}")
            with open(tmp_img, "wb") as fh:
                for chunk in r.iter_bytes():
                    fh.write(chunk)

        if not FFMPEG.exists():
            raise RuntimeError(f"không thấy ffmpeg vendored tại {FFMPEG}")

        # scale+crop về đúng khung đích: scale phủ kín (increase) rồi crop
        # giữa. Không dùng pad -- viền đen trên video dọc trông như lỗi.
        vf = (f"scale={self._w}:{self._h}:force_original_aspect_ratio=increase,"
              f"crop={self._w}:{self._h},setsar=1,format=yuv420p")
        out = dest_path.with_suffix(".mp4") if dest_path.suffix != ".mp4" else dest_path
        proc = subprocess.run(
            [str(FFMPEG), "-y", "-loop", "1", "-i", str(tmp_img),
             "-t", f"{self._clip_sec}", "-r", str(PHOTO_CLIP_FPS),
             "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-pix_fmt", "yuv420p", "-an", str(out)],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
        )
        tmp_img.unlink(missing_ok=True)
        if proc.returncode != 0 or not out.exists():
            raise RuntimeError(f"ffmpeg không đổi được ảnh thành clip: {proc.stderr[-400:]}")
        return out

    def close(self) -> None:
        self._client.close()


# ─── Lọc kết quả Pexels ───────────────────────────────────────────────────
#
# LỖI THẬT (21/09/2026, dựng thử 4 pillar): với từ khoá trừu tượng, Pexels
# trả về tượng thần Ganesha cho bài mệnh lý, máy bay cho bài quẻ Thái, cờ Mỹ,
# bảng chữ Scrabble. Không bộ kiểm chữ nào thấy -- chỉ lộ khi nhìn khung hình.
#
# Pexels không trả mô tả trong StockClip, nhưng URL trang có slug mô tả:
#   https://www.pexels.com/photo/red-and-white-flag-12345/
# Lọc hai lớp trên slug đó:
#   1. CẤM: chủ thể lạc tông kênh (cờ, phương tiện, biểu tượng tôn giáo
#      khác, chữ viết -- chữ Latin trên hình đè lên caption tiếng Việt).
#   2. LIÊN QUAN: slug phải chứa ít nhất một từ nội dung của query.
# Không còn gì sau lớp 2 thì chỉ giữ lớp 1 -- thà hình chung chung còn hơn
# trống cảnh; lớp cấm thì không bao giờ nới.

import re as _re

BLOCK_TERMS = (
    "flag", "airplane", "aeroplane", "plane", "aircraft", "airport", "car", "truck", "bus",
    "ganesha", "hindu", "shiva", "jesus", "church", "cross", "christmas", "mosque", "bible",
    "scrabble", "letter", "letters", "text", "word", "words", "alphabet", "sign", "logo",
    "newspaper", "typewriter", "halloween", "protest", "gun", "weapon", "bikini", "lingerie",
    "beer", "wine", "cocktail", "cigarette", "smoking", "usa", "american", "trump", "election",
    "grasshopper", "insect", "spider", "bug", "skull", "blood",
)
_STOP = {"and", "the", "with", "close", "detail", "view", "old", "from", "into", "over",
         "shot", "background", "portrait", "slow", "motion"}


def _slug_words(clip) -> set[str]:
    url = getattr(clip, "source_page_url", "") or ""
    tail = url.rstrip("/").rsplit("/", 1)[-1]
    return {w for w in _re.split(r"[^a-z]+", tail.lower()) if w and not w.isdigit()}


def filter_clips(clips: list, query: str) -> list:
    words = [_slug_words(c) for c in clips]
    safe = [(c, w) for c, w in zip(clips, words) if not (w & set(BLOCK_TERMS))]
    q = {t for t in _re.split(r"[^a-z]+", query.lower()) if len(t) >= 4 and t not in _STOP}
    # so khớp gốc từ thô: "lanterns" khớp "lantern"
    rel = [c for c, w in safe if any(any(x.startswith(t[:5]) or t.startswith(x[:5])
                                         for x in w if len(x) >= 4) for t in q)]
    return rel or [c for c, _ in safe]


class CompositeProvider:
    """Trộn nhiều nguồn, luân phiên theo THỨ TỰ CẢNH.

    Cảnh 1 luôn lấy từ nguồn đầu tiên trong danh sách -- đó là hero shot, là
    khung quyết định người xem lướt tiếp hay dừng lại, nên không để may rủi.

    Các cảnh sau xen kẽ: video cho chuyển động, ảnh cho những hình cụ thể mà
    kho video mỏng (bàn thờ, la bàn bát quái...). Xen kẽ cũng tránh việc cả
    video thành một chuỗi clip stock nhìn giống hệt nhau.

    Đếm lần gọi search() để biết đang ở cảnh thứ mấy: đường ống gọi đúng một
    lần cho mỗi cảnh, theo thứ tự. Hơi ngầm, nhưng đổi lại không phải sửa
    chữ ký hàm của video-editor.
    """

    name = "composite"

    def __init__(self, providers: list, pattern: str = "vpvp"):
        if not providers:
            raise ValueError("CompositeProvider cần ít nhất 1 nguồn")
        self._providers = providers
        self._pattern = pattern or "v"
        self._scene = 0
        self._by_id: dict[str, object] = {}

    def _pick(self):
        kind = self._pattern[self._scene % len(self._pattern)]
        for p in self._providers:
            is_photo = "photo" in p.name
            if (kind == "p") == is_photo:
                return p
        return self._providers[0]

    def search(self, query: str, orientation: str = "portrait", per_page: int = 15):
        provider = self._pick()
        self._scene += 1
        clips = filter_clips(provider.search(query, orientation=orientation, per_page=per_page), query)
        # Nhớ clip nào thuộc provider nào -- download() phải gọi đúng nguồn
        # đã tìm ra nó, vì cách tải ảnh và tải video khác hẳn nhau.
        for c in clips:
            self._by_id[c.id] = provider
        if not clips and len(self._providers) > 1:
            other = next(p for p in self._providers if p is not provider)
            clips = filter_clips(other.search(query, orientation=orientation, per_page=per_page), query)
            for c in clips:
                self._by_id[c.id] = other
        return clips

    def download(self, clip, dest_path: Path) -> Path:
        provider = self._by_id.get(clip.id) or self._providers[0]
        return provider.download(clip, dest_path)

    def close(self) -> None:
        for p in self._providers:
            try:
                p.close()
            except Exception:
                pass
