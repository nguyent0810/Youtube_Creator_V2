"""Playlist theo chuỗi nội dung (data/playlists.json) — tạo playlist còn thiếu, thêm mọi video dài ĐÃ ĐĂNG vào đúng playlist.

    python scripts/playlists.py plan            # in việc sẽ làm, không gọi API ghi
    python scripts/playlists.py sync [--channel CK]

Không trùng: id playlist ghi lại vào data/playlists.json ngay khi tạo; video đã thêm ghi vào pub/result.json "added_to"
(cùng sổ với publish_long --add-to) -> chạy lại vô hại. Chỉ THÊM, không xoá/sửa playlist cũ của kênh.
publish_long gọi add_for_topic() sau mỗi lần đăng -> video mới tự vào playlist của nó.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
PL = ROOT / "data" / "playlists.json"


def load() -> dict:
    return json.loads(PL.read_text(encoding="utf-8"))


def _save(d: dict) -> None:
    PL.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def ensure(ch: str, key: str, tok: str, P) -> str:
    """id playlist (tạo nếu chưa có, ghi id lại ngay)."""
    d = load()
    p = d[ch][key]
    if not p.get("id"):
        r = P._api(tok, "POST", "playlists", {"part": "snippet,status"},
                   {"snippet": {"title": p["title"], "description": p["desc"], "defaultLanguage": "vi"}, "status": {"privacyStatus": "public"}})
        p["id"] = r["id"]
        _save(d)
        print(f"tạo playlist {ch}/{key}: {p['title']} -> {r['id']}", flush=True)
    return p["id"]


def add_for_topic(topic: str, ch: str, tok: str, P, res: dict, save) -> None:
    """Thêm video của topic vào mọi playlist (kênh ch) có topic đó. res = pub/result.json đã nạp; save() ghi lại."""
    vid = res.get("video_id")
    if not vid:
        return
    for key, p in load().get(ch, {}).items():
        if key.startswith("_") or topic not in p["topics"]:
            continue
        pid = ensure(ch, key, tok, P)
        done = res.setdefault("added_to", [])
        if pid in done:
            continue
        P.add_to_playlist(vid, pid, tok)
        done.append(pid)
        save()
        print(f"  {topic} ({vid}) -> {p['title']}", flush=True)


def main(argv: list[str]) -> None:
    cmd = argv[0] if argv else "plan"
    only = argv[argv.index("--channel") + 1] if "--channel" in argv else None
    d = load()
    for ch, pls in d.items():
        if ch.startswith("_") or (only and ch != only):
            continue
        topics = sorted({t for k, p in pls.items() if not k.startswith("_") for t in p["topics"]})
        if cmd == "plan":
            for k, p in pls.items():
                print(f"{ch}/{k}: {p['title']} id={p.get('id')}")
                for t in p["topics"]:
                    rp = ROOT / "output" / "long" / t / "pub" / "result.json"
                    r = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
                    print(f"    {t}: {r.get('video_id') or '(chưa đăng)'}{' ✓' if p.get('id') in r.get('added_to', []) else ''}")
            continue
        from factory import channels, publish as P
        tok = P.access_token(json.loads(channels.creds_path(ch).read_text(encoding="utf-8")))
        for t in topics:
            rp = ROOT / "output" / "long" / t / "pub" / "result.json"
            if not rp.exists():
                continue
            res = json.loads(rp.read_text(encoding="utf-8"))
            add_for_topic(t, ch, tok, P, res, lambda: rp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8"))


if __name__ == "__main__":
    from factory.console import utf8_console
    utf8_console()
    main(sys.argv[1:])
