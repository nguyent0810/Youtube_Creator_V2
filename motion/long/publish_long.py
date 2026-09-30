"""Đăng video dài lên kênh: upload (private + publishAt) → thumbnail → phụ đề SRT → playlist mới.

    python motion/long/publish_long.py <topic> <CH> <publishAt ISO UTC> [--playlist "Tên" "mô tả" id1 id2 ...]

Mỗi bước ghi vào output/long/<topic>/pub/result.json: chạy lại sẽ BỎ QUA bước đã xong
(không upload trùng, không tạo playlist trùng). Không bao giờ public ngay.
"""
import json
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from factory import channels, publish as P  # noqa: E402


class B:  # Bundle tối thiểu cho P.upload_video
    kind = "long"


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
    tok = P.access_token(creds)

    if not res.get("video_id"):
        b = B()
        b.title = spec["title"]
        b.description = (od / "description.txt").read_text(encoding="utf-8")
        b.tags = y["tags"]
        b.publish_at = publish_at
        up = P.uploads_playlist_id(tok)
        dup = P.already_published(b.title, up, tok)
        if dup:
            raise SystemExit(f"đã có video cùng tiêu đề trên kênh: {dup}")
        print("upload…", flush=True)
        res["video_id"] = P.upload_video(b, od / "final.mp4", tok)
        res["publish_at"] = publish_at
        save()
        print("video", res["video_id"], flush=True)
        tok = P.access_token(creds)   # upload lâu -> token mới
    vid = res["video_id"]

    if not res.get("meta_fixed"):   # upload_video mặc định category 22 -> đổi sang category của spec, giữ nguyên lịch
        cur = P._api(tok, "GET", "videos", {"part": "snippet,status", "id": vid})["items"][0]
        sn = cur["snippet"]
        P._api(tok, "PUT", "videos", {"part": "snippet,status"}, {"id": vid, "snippet": {
            "title": sn["title"], "description": sn["description"], "tags": sn.get("tags", []), "categoryId": y.get("category", "24"),
            "defaultLanguage": "vi", "defaultAudioLanguage": "vi"},
            "status": {"privacyStatus": "private", "publishAt": res["publish_at"], "selfDeclaredMadeForKids": False,
                       "embeddable": True, "publicStatsViewable": True}})
        res["meta_fixed"] = True
        save()
        print("category/lịch OK", flush=True)

    if not res.get("thumb"):
        P.set_thumbnail(vid, od / "pub" / y.get("thumb", "t1.jpg"), tok)
        res["thumb"] = y.get("thumb", "t1.jpg")
        save()
        print("thumbnail OK", flush=True)

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
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
