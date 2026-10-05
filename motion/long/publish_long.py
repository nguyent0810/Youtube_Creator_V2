"""Đăng video dài lên kênh: upload (private + publishAt) → thumbnail → phụ đề SRT → playlist mới.

    python motion/long/publish_long.py <topic> <CH> <publishAt ISO UTC> [--playlist "Tên" "mô tả" id1 id2 ...] [--add-to <playlistId>]

Mỗi bước ghi vào output/long/<topic>/pub/result.json: chạy lại sẽ BỎ QUA bước đã xong
(không upload trùng, không tạo playlist trùng). Không bao giờ public ngay.

Upload (video + category + thumbnail) đi qua factory/channel.py: cùng luật giãn nhịp,
cùng sổ chống upload trùng (slug "long-<topic>") với mọi đường đăng khác.
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
from factory.channel import Channel, Upload  # noqa: E402


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


def main():
    topic, ch, publish_at, *rest = sys.argv[1:]
    sd, od = ROOT / "data" / "long" / topic, ROOT / "output" / "long" / topic
    spec = json.loads((sd / "spec.json").read_text(encoding="utf-8"))
    y = spec["youtube"]
    rp = od / "pub" / "result.json"
    res = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
    save = lambda: rp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    creds = json.loads(channels.creds_path(ch).read_text(encoding="utf-8"))
    tok = P.access_token(creds)       # cho các bước còn lại (phụ đề, playlist)
    thumb = od / "pub" / y.get("thumb", "t1.jpg")

    with store.connect() as conn:
        if not res.get("video_id"):
            titles = P.channel_titles(P.uploads_playlist_id(tok), tok)
            chan = Channel.open(ch, conn, channel_titles=titles)
            print("upload…", flush=True)
            try:
                up = chan.upload(Upload(
                    slug=f"long-{topic}", video=od / "final.mp4", title=spec["title"],
                    description=(od / "description.txt").read_text(encoding="utf-8"),
                    tags=tuple(y["tags"]), kind="long", publish_at=publish_at,
                    category=y.get("category", "24"), thumbnail=thumb))
            except P.PublishError as e:
                # PacingHold / UploadInterrupted: chạy lại lệnh này là đủ (nối
                # tiếp phiên cũ, không upload lại). UploadInDoubt: xem Studio rồi
                # `publish_batch.py resolve long-<topic> <video_id|none> --channel <CH>`.
                raise SystemExit(f"{type(e).__name__}: {e}")
            res.update(video_id=up.video_id, publish_at=up.publish_at, meta_fixed=True)
            if up.thumbnail_error is None and not up.reused:
                res["thumb"] = thumb.name
            save()
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
    import variety   # sổ đa dạng: video sau sẽ được so với video này (nhạc nền, look)
    variety.record(topic, publish_at[:10])
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
