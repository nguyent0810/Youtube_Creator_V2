"""Mô tả YouTube cho video dài: tóm tắt + mốc chương (tính từ timing thật) + nguồn + ghi công ảnh/nhạc/video.

    python motion/long/describe.py <topic>   -> output/long/<topic>/description.txt
Chỉ ghi công ảnh THỰC SỰ xuất hiện trong cảnh (không phải mọi ảnh đã tải).
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
MUSIC = {  # file -> tên gốc trên incompetech (Kevin MacLeod, CC BY 4.0)
    "oppressive_gloom.mp3": "Oppressive Gloom", "ossuary_6_air.mp3": "Ossuary 6 - Air", "echoes_of_time_v2.mp3": "Echoes of Time v2",
    "darkest_child.mp3": "Darkest Child", "gathering_darkness.mp3": "Gathering Darkness", "lightless_dawn.mp3": "Lightless Dawn",
    "dark_times.mp3": "Dark Times", "crypto.mp3": "Crypto", "heart_of_nowhere.mp3": "Heart of Nowhere", "deep_haze.mp3": "Deep Haze",
    "long_note_four.mp3": "Long Note Four", "despair_and_triumph.mp3": "Despair and Triumph", "night_cave.mp3": "Night Cave",
    "impact_lento.mp3": "Impact Lento"}
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import variety  # noqa: E402
for _m in variety.catalog()["tracks"].values():   # bài mới thêm vào danh mục nhạc cũng được ghi công
    if _m.get("author") == "Kevin MacLeod":
        MUSIC.setdefault(_m["file"], _m["title"])


def _lic_url(lic):
    m = re.match(r"CC BY(-SA)? (\d\.\d)", lic)
    return f"https://creativecommons.org/licenses/{'by-sa' if m.group(1) else 'by'}/{m.group(2)}/" if m else ""


FOOTER = {"MIM": "Mind in the Machine — AI và công nghệ, kể dễ hiểu bằng tiếng Việt.",
          "CK": "Biểu Đồ Biết Nói — tiền bạc, giải thích bằng dữ liệu. Mỗi tuần một câu hỏi tiền bạc thật."}
DATA_CREDIT = {"CK": "📊 DỮ LIỆU BIỂU ĐỒ: VN-Index — HOSE; vàng miếng — SJC (sjc.com.vn); truy xuất qua Vnstock. Bitcoin — CoinGecko."}


def mim_lines(spec, meta, chapters, used, vids, music, od):
    """Kênh MIM / CK: nguồn gốc (không phải Wikipedia), ảnh CC BY ghi đủ tác giả + giấy phép + link trang Commons, ghi tên
    người quay clip; kênh CK thêm nguồn dữ liệu biểu đồ (giấy phép Vnstock yêu cầu trích dẫn công cụ)."""
    ch = spec.get("channel", "MIM")
    L = [meta.get("summary", ""), "", *meta.get("more", []), "", "⏱ CHƯƠNG", *chapters, "",
         "📚 NGUỒN (tài liệu gốc, bài báo, trang chính thức)", SRC_SLOT, "",
         *([meta.get("data_credit") or DATA_CREDIT[ch], ""] if ch in DATA_CREDIT else []),   # spec youtube.data_credit: ghi đè theo video
         "Lời dẫn là bản viết mới dựa trên các nguồn trên; câu có nhãn TRÍCH DỊCH là bản dịch tiếng Việt của nguyên văn.",
         "Hình ảnh/video có nhãn MINH HỌA hoặc MÔ PHỎNG chỉ để minh họa, không phải tư liệu gốc của sự kiện."]
    if used:
        L += ["", "🖼 ẢNH (Wikimedia Commons)"]
    pd = 0
    for k in sorted(used):
        f = spec["imgs"][k]
        m = json.loads((od / "img" / f"{k}.json").read_text(encoding="utf-8"))
        if m["license"].lower().startswith(("public", "pd", "cc0", "no restr")):
            pd += 1
            continue
        by = re.sub(r"\s*\d\d:\d\d, .*UTC\)", "", m["artist"].split("\n")[0]).strip() or "không rõ tác giả"
        by = re.sub(r"^(.+?)\1$", r"\1", by).replace("Unknown author", "không rõ tác giả")   # Commons hay lặp "Unknown author"
        name = re.sub(r"\s*\(\d{6,}\)|\.(jpe?g|png|tif)$", "", f[5:], flags=re.I)[:80].strip()
        L.append(f"• {name} — {by[:40].strip()} — {m['license']} {_lic_url(m['license'])} — "
                 f"https://commons.wikimedia.org/wiki/{quote(f.replace(' ', '_'), safe=":()',")}")
    if pd:
        L.append(f"• Và {pd} ảnh thuộc phạm vi công cộng (Public domain / CC0).")
    idx_p = od / "broll" / "index.json"
    idx = json.loads(idx_p.read_text(encoding="utf-8")) if idx_p.exists() else {}
    users = sorted({idx[v]["user"] for v in vids if v in idx})
    L += ["", "🎬 VIDEO: Pexels (pexels.com), giấy phép Pexels" + (" — quay bởi " + ", ".join(users) if users else ""), "", "🎵 NHẠC NỀN"]
    mac = [b for b in music if b in MUSIC]
    if mac:
        L.append(", ".join(f"\"{MUSIC[b]}\"" for b in mac) + " by Kevin MacLeod (incompetech.com)")
        L.append("Licensed under Creative Commons: By Attribution 4.0 License — http://creativecommons.org/licenses/by/4.0/")
    L += ["", FOOTER.get(ch, ""), "", " ".join("#" + x for x in meta.get("hashtags", []))]
    i = L.index(SRC_SLOT)
    rest = len("\n".join(L[:i] + L[i + 1:]))
    return L[:i] + fit_sources(meta.get("sources", []), DESC_CAP - rest) + L[i + 1:]


SRC_SLOT = object()
DESC_CAP = 4900   # YouTube: mô tả tối đa 5000 ký tự (Bundle.validate chặn) -- chừa lề


def fit_sources(src: list[str], budget: int) -> list[str]:
    """Danh sách nguồn vừa ngân sách ký tự của mô tả (D1 07/10/2026: 32 nguồn = 5.079 ký tự -> mô tả 8.199 > 5.000, upload
    bị chặn). Thứ tự: đủ nguyên văn -> bỏ tên bài ("Báo dd/mm — tên bài: URL" -> "Báo dd/mm: URL") -> giữ các nguồn đầu (spec
    xếp theo thứ tự xuất hiện) + một dòng nói phần còn lại ghi trên màn hình ở từng cảnh."""
    size = lambda xs: len("\n".join(xs)) + 1
    if size(src) <= budget:
        return list(src)
    short = [re.sub(r"^(.+?) — .+?: (https?://\S+)$", r"\1: \2", x) for x in src]
    if size(short) <= budget:
        return short
    out = []
    for k, x in enumerate(short):
        tail = f"…và {len(short) - k - 1} nguồn khác: tên báo và ngày đăng ghi trên màn hình ở từng cảnh."
        if size(out + [x, tail]) > budget:
            return out + [f"…và {len(short) - k} nguồn khác: tên báo và ngày đăng ghi trên màn hình ở từng cảnh."]
        out.append(x)
    return out


def main(topic):
    sd, od = ROOT / "data" / "long" / topic, ROOT / "output" / "long" / topic
    spec = json.loads((sd / "spec.json").read_text(encoding="utf-8"))
    meta = spec.get("youtube", {})
    used, music, chapters, t, vids = set(), [], [], 0.0, set()
    mim = spec.get("channel") in FOOTER          # kênh MIM / CK: mô tả kiểu "nguồn gốc"
    for c in spec["chapters"]:
        ch = json.loads((sd / f"{c}.json").read_text(encoding="utf-8"))
        for s in ch["scenes"]:
            for k in (s.get("img"), s.get("bg"), (s.get("a") or {}).get("img"), (s.get("b") or {}).get("img"), *[q.get("img") for q in s.get("pins") or []]):
                if k:
                    used.add(k)
            if s.get("vid"):
                vids.add(str(s["vid"]))
        bg = ch.get("bgm") or []
        picks = variety._picks(topic)   # bgm chọn theo mood: file nằm trong bgm_picks.json
        for b in [q.get("file") or picks.get(f"{c}.{k}") for k, q in enumerate([bg] if isinstance(bg, dict) else bg)]:
            if b and b not in music:
                music.append(b)
        title = ch["hud"]["t"].title() if c != "ch00" else meta.get("ch00_title", "Mở đầu")
        if mim:                                      # tiêu đề chương viết tay (.title() làm hỏng chữ hoa kiểu "AI")
            title = meta.get("chapter_titles", {}).get(c, title)
        elif c == spec["chapters"][-1]:
            title = "Kết: " + title
        chapters.append(f"{int(t // 60):02d}:{int(t % 60):02d} {title}")
        t += json.loads((od / c / "timing.json").read_text(encoding="utf-8"))["duration"]
    lines = [meta.get("summary", ""), "", *meta.get("more", []), "", "⏱ CHƯƠNG", *chapters, "", "📚 NGUỒN THAM KHẢO (Wikipedia tiếng Anh và các nguồn được trích trong đó)",
             *meta.get("sources", [])[:8], "và các bài Wikipedia liên quan.", "",
             "Lời dẫn là bản viết mới dựa trên tư liệu công khai; những câu có nhãn DIỄN Ý là diễn đạt lại, không phải nguyên văn.",
             "Hình ảnh/video có nhãn MINH HỌA chỉ mang tính minh họa bối cảnh.", "", "🖼 ẢNH (Wikimedia Commons và các kho tư liệu mở)"]
    pd, bylic, pdsrc = 0, {}, set()
    INST = {"wellcome": "Wellcome Collection", "artic": "Art Institute of Chicago"}
    for k in sorted(used):
        f = spec["imgs"][k]
        mp = od / "img" / f"{k}.json"
        m = json.loads(mp.read_text(encoding="utf-8"))
        if m["license"].lower().startswith(("public", "pd", "cc0", "no restr")):
            pd += 1
            if m.get("source", "").split(":")[0] in INST:   # PD từ kho bảo tàng: vẫn ghi tên kho (lịch sự, không bắt buộc)
                pdsrc.add(INST[m["source"].split(":")[0]])
            continue
        by = re.sub(r"\s*\d\d:\d\d, .*UTC\)", "", m["artist"].split("\n")[0]).strip() or "không rõ tác giả"
        src = {"wellcome": " · Wellcome Collection", "artic": " · Art Institute of Chicago"}.get(m.get("source", "").split(":")[0], "")
        if m.get("source", "").startswith("europeana:"):
            src = " · " + m["source"].split(":", 1)[1]
        if m.get("source") == "sentinel2":                        # Copernicus: ghi đúng câu bắt buộc
            bylic.setdefault("Copernicus Sentinel data", []).append(m["artist"])
            continue
        name = re.sub(r"\s*\(\d{6,}\)|\.(jpe?g|png|tif)$|, Sicily, Italy| - panoramio", "", m.get("title") or f[5:], flags=re.I)[:meta.get("credit_name_len", 48)]
        by = re.sub(r"^The original uploader was |No machine-readable author provided\. ", "", by)
        bylic.setdefault(m["license"], []).append(f"{name.strip()} ({by[:meta.get('credit_by_len', 40)].strip()}{src})")
    if not any(str(spec["imgs"][k]).startswith("EXT:") for k in used):   # chỉ Commons -> giữ tiêu đề cũ
        lines = [x.replace("🖼 ẢNH (Wikimedia Commons và các kho tư liệu mở)", "🖼 ẢNH (Wikimedia Commons)") for x in lines]
    lines += [f"• {lic}: " + "; ".join(v) for lic, v in sorted(bylic.items())]   # gom theo giấy phép: đủ tác giả + giấy phép, ít byte hơn
    lines += [f"• Và {pd} ảnh tư liệu thuộc phạm vi công cộng (Public domain / CC0)" + (f", gồm ảnh từ {', '.join(sorted(pdsrc))}." if pdsrc else "."), "",
              "🎬 VIDEO B-ROLL: Pexels (pexels.com) — giấy phép Pexels, dùng tự do.", "", "🎵 NHẠC NỀN"]
    mac = [b for b in music if b in MUSIC]
    if mac:
        lines.append(", ".join(f"\"{MUSIC[b]}\"" for b in mac) + " by Kevin MacLeod (incompetech.com)")
        lines.append("Licensed under Creative Commons: By Attribution 4.0 License — http://creativecommons.org/licenses/by/4.0/")
    for b in music:   # bản thu tự do từ Commons: ghi tên file + giấy phép (json cạnh file nhạc)
        mj = od / "bgm" / (Path(b).stem + ".json")
        if b not in MUSIC and mj.exists():
            m = json.loads(mj.read_text(encoding="utf-8"))
            name = re.sub(r"\.(flac|ogg|oga|wav|mp3)$", "", m["file"][5:], flags=re.I)
            lines.append(f"Mascagni — Intermezzo (Cavalleria rusticana) · {m.get('short', name[:40])} — Wikimedia Commons — {m['license']}")
    lines += ["", " ".join("#" + x for x in meta.get("hashtags", []))]
    if mim:
        lines = mim_lines(spec, meta, chapters, used, vids, music, od)
    (od / "description.txt").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print((od / "description.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    import pathlib, sys  # noqa: E401
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    main(sys.argv[1])
