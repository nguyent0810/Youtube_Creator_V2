"""Đăng video dài lên kênh: upload (private + publishAt) → thumbnail → phụ đề SRT → playlist mới.

    python motion/long/publish_long.py <topic> <CH> <publishAt ISO UTC> [--wait] [--playlist "Tên" "mô tả" id1 id2 ...] [--add-to <playlistId>]

--wait (retro 2 mục 15): chưa tới lượt giãn nhịp thì NGỦ tới Channel.next_upload_at() (in mốc đích) rồi upload, thay vì
ném PacingHold. Chuỗi tự động dùng cờ này, không viết vòng "thử lại N lần".

Mỗi bước ghi vào output/long/<topic>/pub/result.json: chạy lại sẽ BỎ QUA bước đã xong
(không upload trùng, không tạo playlist trùng). Không bao giờ public ngay.

Upload (video + category + thumbnail) đi qua factory/channel.py: cùng luật giãn nhịp,
cùng sổ chống upload trùng (slug "long-<topic>") với mọi đường đăng khác.

Video dài cũng có Bundle (render.engine="casewide") và một hàng trong kho `item`
như short (05/10/2026, docs/audit/2026-10-05-one-store-design.md): status_report và
vòng phản hồi thấy nó như mọi video khác. (Kênh upload tay chưa xuất gói video dài:
export_manual chỉ lấy slug theo tiền tố kênh.)
"""
import json
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "motion"))
from factory import channels, publish as P, store  # noqa: E402
from factory.bundle import Bundle  # noqa: E402
from factory.channel import Channel, Upload, upload_when_free, wait_turn  # noqa: E402


def long_bundle(topic: str, ch: str, publish_at: str, sd: Path, od: Path) -> Bundle:
    """Bundle của video dài, suy từ spec + description.txt đã có. Lời đọc =
    các câu của mọi chương (để truy vết/đếm từ); dựng vẫn đi theo spec."""
    spec = json.loads((sd / "spec.json").read_text(encoding="utf-8"))
    y = spec["youtube"]
    said = []
    for c in spec["chapters"]:
        p = sd / f"{c}.json"
        if p.exists():
            said += [ln["t"] if isinstance(ln, dict) else ln
                     for ln in json.loads(p.read_text(encoding="utf-8")).get("lines", [])]
    return Bundle(channel=ch, kind="long", slug=f"long-{topic}", script=" ".join(said), title=spec["title"],
                  description=(od / "description.txt").read_text(encoding="utf-8"), tags=list(y["tags"]),
                  # thumbnail dựng sẵn (pub/<thumb>); chữ trên đó là tiêu đề hồ sơ
                  thumbnail_text=spec["title"][:60], publish_at=publish_at,
                  voice={"MIM": "Thanh Bình", "CK": "Ngọc Huyền"}.get(spec.get("channel", "CL"), "Anh Khôi"), bgm="",
                  broll_queries=[], render={"engine": "casewide", "spec": f"data/long/{topic}/spec.json"},
                  source_note="; ".join(y.get("sources", [])))


def register(conn, b: Bundle, res: dict, video: Path, chan: Channel, bundles: Path | None = None) -> None:
    """Ghi Bundle + hàng `item`. Chạy lại vô hại: KHÔNG BAO GIỜ hạ `published`
    về `assembled` (lần chạy thứ hai để thêm playlist không được làm video đã
    lên kênh trông như đang chờ upload). result.json có video_id = đã đăng:
    ghi cả sổ upload_log (Channel.adopt, idempotent) -- vòng phản hồi chỉ đo
    video trong sổ, mà video dài cũ upload trước khi có sổ."""
    if not store.bundle_path(b, bundles).exists():     # Bundle bất biến: giữ bản đầu
        store.save_bundle(b, bundles)
    store.enqueue(b, conn)
    row = conn.execute("SELECT stage, video_id FROM item WHERE id = ?", (b.id,)).fetchone()
    if res.get("video_id"):
        chan.adopt(b.slug, res["video_id"])
        if (row["stage"], row["video_id"]) != ("published", res["video_id"]):
            store.mark(conn, b.id, "published", video_id=res["video_id"])
    elif row["stage"] != "published":
        store.mark(conn, b.id, "assembled", video_path=str(video))


def captions_insert(tok, vid, srt: Path, name="Tiếng Việt"):
    meta = json.dumps({"snippet": {"videoId": vid, "language": "vi", "name": name, "isDraft": False}}).encode()
    bnd = uuid.uuid4().hex
    body = (f"--{bnd}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n").encode() + meta + \
           (f"\r\n--{bnd}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + srt.read_bytes() + f"\r\n--{bnd}--\r\n".encode()
    req = urllib.request.Request("https://www.googleapis.com/upload/youtube/v3/captions?part=snippet&uploadType=multipart", data=body, method="POST")
    req.add_header("Authorization", f"Bearer {tok}")
    req.add_header("Content-Type", f"multipart/related; boundary={bnd}")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)["id"]
    except urllib.error.HTTPError as e:
        raise P.PublishError(f"captions HTTP {e.code}: {e.read().decode()[:400]}")


def find_thumb(od: Path, name: str = "t1.jpg") -> Path:
    """Thumbnail: pub/<name> (C1 trở về trước, PM chép vào pub/) hoặc <topic>/<name> (thumb.py ghi thẳng, từ D1 07/10).
    Trước đây chỉ nhìn pub/ -> MIM #2 lên kênh KHÔNG có thumbnail rồi sập (retro 2 mục 19)."""
    p = od / "pub" / name
    return p if p.exists() or not (od / name).exists() else od / name


def preflight(od: Path, thumb: Path) -> list[str]:
    """Đủ đồ trước khi upload: video, mô tả, phụ đề, thumbnail. Trả về tên file thiếu (rỗng = đi tiếp)."""
    return [p.name for p in (od / "final.mp4", od / "description.txt", od / "captions.vi.srt", thumb) if not p.exists()]


def main():
    topic, ch, publish_at, *rest = sys.argv[1:]
    wait = "--wait" in rest
    rest = [x for x in rest if x != "--wait"]      # --playlist đọc các đối số SAU nó theo vị trí
    sd, od = ROOT / "data" / "long" / topic, ROOT / "output" / "long" / topic
    spec = json.loads((sd / "spec.json").read_text(encoding="utf-8"))
    y = spec["youtube"]
    rp = od / "pub" / "result.json"
    rp.parent.mkdir(parents=True, exist_ok=True)     # MIM #2 07/10: pub/ chưa có -> upload XONG rồi sập ở save()
    res = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
    save = lambda: rp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    thumb = find_thumb(od, y.get("thumb", "t1.jpg"))
    if channels.upload_mode(ch) == "manual":
        # Kênh upload TAY (MIM): ghi kho (bundle + video + thumbnail), ghi sổ đa dạng, rồi xuất gói -- KHÔNG gọi API upload.
        b = long_bundle(topic, ch, publish_at, sd, od)
        with store.connect() as conn:
            register(conn, b, res, od / "final.mp4", Channel.open(ch, conn))
            if thumb.exists():
                conn.execute("UPDATE item SET thumb_path = ? WHERE id = ?", (str(thumb), b.id))
        import variety
        variety.record(topic, publish_at[:10])
        print(f"đã vào kho: {b.slug}. Xuất gói upload tay:  python scripts/export_manual.py --channel {ch}")
        return
    creds = json.loads(channels.creds_path(ch).read_text(encoding="utf-8"))
    tok = P.access_token(creds)       # cho các bước còn lại (phụ đề, playlist)

    if not res.get("video_id"):
        missing = preflight(od, thumb)
        if missing:      # upload là bước KHÔNG rút lại được: thiếu gì thì dừng TRƯỚC, không đăng nửa vời
            raise SystemExit(f"preflight: thiếu {', '.join(missing)} trong {od} — chưa upload gì")
    b = long_bundle(topic, ch, publish_at, sd, od)
    with store.connect() as conn:
        register(conn, b, res, od / "final.mp4", Channel.open(ch, conn))
        if not res.get("video_id"):
            if wait:      # ngủ tới lượt TRƯỚC khi chụp tiêu đề kênh + lấy token mới (chờ có thể nhiều giờ)
                wait_turn(Channel.open(ch, conn))
                tok = P.access_token(creds)
            titles = P.channel_titles(P.uploads_playlist_id(tok), tok)
            chan = Channel.open(ch, conn, channel_titles=titles)
            print("upload…", flush=True)
            try:
                u = Upload(
                    slug=f"long-{topic}", video=od / "final.mp4", title=spec["title"],
                    description=(od / "description.txt").read_text(encoding="utf-8"),
                    tags=tuple(y["tags"]), kind="long", publish_at=publish_at,
                    category=y.get("category", "24"), thumbnail=thumb)
                up = upload_when_free(chan, u) if wait else chan.upload(u)
            except P.PublishError as e:
                # PacingHold / UploadInterrupted: chạy lại lệnh này là đủ (nối
                # tiếp phiên cũ, không upload lại). UploadInDoubt: xem Studio rồi
                # `publish_batch.py resolve long-<topic> <video_id|none> --channel <CH>`.
                raise SystemExit(f"{type(e).__name__}: {e}")
            res.update(video_id=up.video_id, publish_at=up.publish_at, meta_fixed=True)
            if up.thumbnail_error is None and not up.reused:
                res["thumb"] = thumb.name
            save()
            store.mark(conn, b.id, "published", video_id=up.video_id)
            print("video", res["video_id"], flush=True)
        else:
            chan = Channel.open(ch, conn)
        vid = res["video_id"]

        if not res.get("meta_fixed"):   # video upload trước khi có Channel: category còn là 22
            chan.edit(vid, categoryId=y.get("category", "24"))
            res["meta_fixed"] = True
            save()
            print("category OK", flush=True)

        if not res.get("thumb"):
            chan.set_thumbnail(vid, thumb)
            res["thumb"] = thumb.name
            save()
            print("thumbnail OK", flush=True)

    tok = P.access_token(creds)       # upload dài có thể quá hạn token cũ
    if not res.get("captions"):
        try:
            res["captions"] = captions_insert(tok, vid, od / "captions.vi.srt")
            res.pop("captions_error", None)
            print("phụ đề OK", flush=True)
        except P.PublishError as e:
            res["captions_error"] = str(e)
            print("phụ đề LỖI:", e, flush=True)
        save()

    if "--playlist" in rest and not res.get("playlist_id"):
        i = rest.index("--playlist")
        name, desc, *ids = rest[i + 1:]
        pl = P._api(tok, "POST", "playlists", {"part": "snippet,status"},
                    {"snippet": {"title": name, "description": desc, "defaultLanguage": "vi"}, "status": {"privacyStatus": "public"}})
        res["playlist_id"] = pl["id"]
        res["playlist_items"] = []
        save()
        print("playlist", pl["id"], flush=True)
    if res.get("playlist_id") and "--playlist" in rest:
        ids = rest[rest.index("--playlist") + 3:]
        for v in [vid] + [x for x in ids if x != vid]:
            if v in res["playlist_items"]:
                continue
            P.add_to_playlist(v, res["playlist_id"], tok)
            res["playlist_items"].append(v)
            save()
        print("playlist items", len(res["playlist_items"]), flush=True)
    if "--add-to" in rest:   # thêm vào playlist CÓ SẴN (vd. PLM35iHclYa34 "Thế Giới Ngầm Toàn Cầu")
        pid = rest[rest.index("--add-to") + 1]
        done = res.setdefault("added_to", [])
        if pid not in done:
            P.add_to_playlist(vid, pid, tok)
            done.append(pid)
            save()
            print("added to playlist", pid, flush=True)
    try:     # playlist theo chuỗi (data/playlists.json): video vừa đăng tự vào đúng playlist; lỗi ở đây KHÔNG làm hỏng lần đăng
        sys.path.insert(0, str(ROOT / "scripts"))
        import playlists
        playlists.add_for_topic(topic, ch, tok, P, res, save)
    except Exception as e:      # noqa: BLE001
        print(f"! playlist chưa thêm được ({e}) — chạy: python scripts/playlists.py sync --channel {ch}", flush=True)
    import variety   # sổ đa dạng: video sau sẽ được so với video này (nhạc nền, look)
    variety.record(topic, publish_at[:10])
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    main()
