"""Đăng video dài lên kênh: upload (private + publishAt) → thumbnail → phụ đề SRT → playlist mới.

    python motion/long/publish_long.py <topic> <CH> <publishAt ISO UTC> [--playlist "Tên" "mô tả" id1 id2 ...] [--add-to <playlistId>]

Mỗi bước ghi vào output/long/<topic>/pub/result.json: chạy lại sẽ BỎ QUA bước đã xong
(không upload trùng, không tạo playlist trùng). Không bao giờ public ngay.

KIỂM TRƯỚC KHI UPLOAD (audit 08/10/2026) -- hỏng thì hỏng trước khi tốn quota:
  - kênh phải có thật và khớp "channel" của spec (mặc định CL); credential phải
    trỏ đúng kênh đó (channels.verify_identity);
  - publishAt đúng định dạng UTC ...Z và ở tương lai (quá khứ = công khai ngay;
    lưu ý upload_one.py nhận giờ VN, script này nhận UTC);
  - description.txt <= 5.000 BYTE và không có < >; tags <= 500 ký tự theo cách
    YouTube đếm (YouTube từ chối, sau nhiều giờ render).
Mất phản hồi sau khi upload xong: chạy lại sẽ NHẬN LẠI video mang tag dấu của
topic thay vì dừng ở "trùng tiêu đề". Cập nhật category chỉ ghi part=snippet,
không đụng lịch/quyền riêng tư.
"""
import hashlib
import json
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "motion"))
from factory import channels, publish as P  # noqa: E402
from factory.bundle import MAX_TAGS_TOTAL_CHARS, tags_total_chars  # noqa: E402


class B:  # Bundle tối thiểu cho P.upload_video
    kind = "long"

    def __init__(self, ch: str, topic: str):
        # id ổn định theo topic -> tag dấu để chạy lại nhận ra bản upload của chính mình
        self.id = hashlib.sha256(f"{ch}|long|{topic}".encode("utf-8")).hexdigest()[:16]


def parse_args(argv: list[str]):
    pos, i = [], 0
    while i < len(argv) and not argv[i].startswith("--"):
        pos.append(argv[i])
        i += 1
    if len(pos) < 3:
        raise SystemExit(__doc__)
    playlist, add_to, flags = None, [], argv[i:]
    j = 0
    while j < len(flags):
        if flags[j] == "--playlist":
            vals, j = [], j + 1
            while j < len(flags) and not flags[j].startswith("--"):
                vals.append(flags[j])
                j += 1
            if len(vals) < 2:
                raise SystemExit('--playlist cần "Tên" "mô tả" [videoId ...]')
            playlist = (vals[0], vals[1], vals[2:])
        elif flags[j] == "--add-to":
            if j + 1 >= len(flags) or flags[j + 1].startswith("--"):
                raise SystemExit("--add-to cần playlistId")
            add_to.append(flags[j + 1])
            j += 2
        else:
            raise SystemExit(f"cờ lạ {flags[j]!r}")
    # Bản cũ lấy MỌI thứ sau "--playlist Tên mô tả" làm video id -- kể cả "--add-to"
    # và id playlist -> playlistItems.insert lỗi 4xx, mọi lần chạy lại chết ở đó.
    return pos[0], pos[1].upper(), pos[2], playlist, add_to


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
    topic, ch, publish_at, playlist, add_to = parse_args(sys.argv[1:])
    if ch not in channels.CHANNELS:
        raise SystemExit(f"kênh lạ {ch!r} (có: {', '.join(channels.CHANNELS)})")
    sd, od = ROOT / "data" / "long" / topic, ROOT / "output" / "long" / topic
    spec = json.loads((sd / "spec.json").read_text(encoding="utf-8"))
    if spec.get("channel", "CL") != ch:
        raise SystemExit(f"topic {topic} thuộc kênh {spec.get('channel', 'CL')}, không phải {ch}")
    y = spec["youtube"]
    rp = od / "pub" / "result.json"
    res = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
    save = lambda: rp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    P.parse_publish_at(publish_at)
    if res.get("publish_at") and res["publish_at"] != publish_at:
        raise SystemExit(f"video đã upload với lịch {res['publish_at']}, khác {publish_at} -- sửa lịch trong Studio")
    creds = channels.load_creds(ch)
    tok = P.access_token(creds)
    ident = channels.verify_identity(ch, tok)

    if not res.get("video_id"):
        P.check_publish_at(publish_at)
        b = B(ch, topic)
        b.title = spec["title"]
        b.description = (od / "description.txt").read_text(encoding="utf-8")
        nbytes = len(b.description.encode("utf-8"))
        if nbytes > 5000 or "<" in b.description or ">" in b.description:
            raise SystemExit(f"description.txt {nbytes} byte (tối đa 5.000) hoặc có < > -- YouTube sẽ từ chối. "
                             "Rút gọn (credit_name_len/credit_by_len trong spec) rồi chạy describe.py lại.")
        b.tags = y["tags"]
        n = tags_total_chars(list(b.tags) + [P.marker_tag(b)])
        if n > MAX_TAGS_TOTAL_CHARS:      # đếm theo cách YouTube đếm, cả tag dấu yf<id>
            raise SystemExit(f"tags {n} ký tự (tối đa {MAX_TAGS_TOTAL_CHARS}, tag có dấu cách tính thêm 2) -- bớt tag trong spec")
        b.publish_at = publish_at
        dup = P.already_published(b.title, ident["uploads"], tok)
        adopted = P.adopt_existing(b, dup, tok) if dup else None    # video lạ cùng tiêu đề -> DuplicateTitle
        if adopted:
            print("NHẬN LẠI video đã upload:", adopted.video_id, flush=True)
            res["video_id"] = adopted.video_id
        else:
            print("upload…", flush=True)
            res["video_id"] = P.upload_video(b, od / "final.mp4", tok)
        res["publish_at"] = publish_at
        save()
        print("video", res["video_id"], flush=True)
        tok = P.access_token(creds)   # upload lâu -> token mới
    vid = res["video_id"]

    if not res.get("meta_fixed"):
        # upload_video mặc định category 22 -> đổi sang category của spec. Chỉ ghi
        # part=snippet: lịch và quyền riêng tư KHÔNG bị đụng (bản cũ gửi lại cả
        # status với publishAt -- chạy lại sau giờ lên sóng là gửi giờ quá khứ).
        sn = P.video_status(vid, tok)["snippet"]
        P._api(tok, "PUT", "videos", {"part": "snippet"}, {"id": vid, "snippet": {
            "title": sn["title"], "description": sn["description"], "tags": sn.get("tags", []),
            "categoryId": y.get("category", "24"), "defaultLanguage": "vi", "defaultAudioLanguage": "vi"}})
        res["meta_fixed"] = True
        save()
        print("category OK", flush=True)

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

    if playlist and not res.get("playlist_id"):
        name, desc, ids = playlist
        pl = P._api(tok, "POST", "playlists", {"part": "snippet,status"},
                    {"snippet": {"title": name, "description": desc, "defaultLanguage": "vi"}, "status": {"privacyStatus": "public"}})
        res["playlist_id"] = pl["id"]
        res["playlist_items"] = []
        save()
        print("playlist", pl["id"], flush=True)
    if res.get("playlist_id") and playlist:
        ids = playlist[2]
        for v in [vid] + [x for x in ids if x != vid]:
            if v in res["playlist_items"]:
                continue
            P.add_to_playlist(v, res["playlist_id"], tok)
            res["playlist_items"].append(v)
            save()
        print("playlist items", len(res["playlist_items"]), flush=True)
    for pid in add_to:   # thêm vào playlist CÓ SẴN (vd. PLM35iHclYa34 "Thế Giới Ngầm Toàn Cầu")
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
