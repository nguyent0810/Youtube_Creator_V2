"""Tuần test 05–11/10/2026 trên CL: 3 short/ngày (07:00 · 18:30 · 21:30 VN), SEO lại tiêu đề + mô tả.

    python motion/stier/week_2026-10-05.py --dry      # chỉ in
    python motion/stier/week_2026-10-05.py            # áp dụng

- Video S-tier cũ (đã upload 30/09, private): đặt giờ theo kế hoạch tuần, sửa tiêu đề/mô tả.
- Video S-tier còn lịch nhưng KHÔNG nằm trong tuần test: gỡ lịch (vẫn private) — lần gỡ 04/10 sót 35 video
  vì playlist uploads chỉ trả tối đa 500 mục; từ nay quét theo store (item.video_id), không theo playlist.
- Video mới (btk, yakuza5, …) KHÔNG upload ở đây: dùng upload_one.py, mỗi lần một video, cách nhau vài giờ.
Trạng thái gốc lưu ở output/analysis/cl_week_before_2026-10-04.json.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from factory import channels, publish, store  # noqa: E402

API = "https://www.googleapis.com/youtube/v3/videos"
SRC = ("Ảnh tư liệu: Wikimedia Commons (phạm vi công cộng). Dữ kiện đối chiếu với các nguồn trên; "
       "chỗ nào là diễn ý đã ghi rõ trên hình.")


def utc(vn: str) -> str:
    return (datetime.strptime(vn, "%Y-%m-%d %H:%M") - timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ")


# slug: (giờ VN, tiêu đề SEO hoặc None = giữ, đoạn mở mô tả (từ khoá trong 125 ký tự đầu), hashtag)
WEEK = {
    "lustig": ("2026-10-05 07:00", "Lừa đảo bán tháp Eiffel… hai lần: Victor Lustig",
               "Lừa đảo bán tháp Eiffel không chỉ một mà hai lần: đó là Victor Lustig, kẻ lừa đảo lịch lãm nhất thế kỷ 20. "
               "Năm 1925 hắn mời các đại lý sắt vụn tới khách sạn sang nhất Paris, và có người trả tiền thật.",
               "#Shorts #lừađảo #vụáncóthật #hồsơvụán"),
    "alcatraz": ("2026-10-05 18:30", "Vượt ngục Alcatraz 1962: ba cái đầu giả trên gối",
                 "Vượt ngục Alcatraz 1962: sáng 12/6, cai ngục lay một tù nhân dậy và cái đầu lăn xuống sàn. "
                 "Đó là đầu giả làm từ xà phòng và giấy vệ sinh. Frank Morris và anh em nhà Anglin đã biến mất, đến nay chưa ai tìm thấy.",
                 "#Shorts #vượtngục #Alcatraz #vụáncóthật"),
    "unabomber": ("2026-10-05 21:30", "Unabomber: 17 năm FBI không bắt được, em trai nhận ra hắn",
                  "Unabomber gửi bom qua đường bưu điện suốt 17 năm mà FBI không lần ra dấu vết. "
                  "Chỉ khi bản tuyên ngôn được đăng báo, chính em trai hắn mới nhận ra lối hành văn quen thuộc.",
                  "#Shorts #FBI #vụáncóthậtởmỹ #hồsơvụán"),
    "monalisa": ("2026-10-06 07:00", None,
                 "Vì sao Mona Lisa nổi tiếng nhất thế giới? Năm 1911 bức tranh bị một người thợ lắp kính đánh cắp khỏi bảo tàng Louvre, "
                 "và hai năm vắng mặt đã biến nó thành huyền thoại.",
                 "#Shorts #MonaLisa #vụtrộm #vụáncóthật"),
    "billykid": ("2026-10-07 07:00", None,
                 "Billy the Kid vượt ngục năm 1881 chỉ bằng một lời xin đi vệ sinh, hai tuần trước ngày bị treo cổ. "
                 "Vài tháng sau, cảnh sát trưởng Pat Garrett bắt kịp hắn trong một căn phòng tối.",
                 "#Shorts #vượtngục #miềnTây #vụáncóthật"),
    "valentine": ("2026-10-07 18:30", "Al Capone và thảm sát Valentine 1929: sát thủ mặc đồng phục cảnh sát",
                  "Al Capone và vụ thảm sát ngày Valentine 1929 ở Chicago: những kẻ nổ súng mặc đồng phục cảnh sát, "
                  "nên nạn nhân ngoan ngoãn quay mặt vào tường. Đến nay chưa ai bị kết án.",
                  "#Shorts #AlCapone #mafia #vụáncóthật"),
    "sheppard": ("2026-10-08 07:00", None,
                 "Vượt ngục 4 lần trong một năm: Jack Sheppard, tên trộm London thế kỷ 18, thoát cả xiềng xích lẫn tường đá, "
                 "rồi bình thản nhập vào đám đông đang đi tìm mình.",
                 "#Shorts #vượtngục #vụánlịchsử #hồsơvụán"),
    "leoloeb": ("2026-10-09 07:00", None,
                "Leopold và Loeb, hai sinh viên giàu có ở Chicago, tin rằng mình đã gây ra tội ác hoàn hảo năm 1924. "
                "Kế hoạch sụp đổ vì một cặp kính có bản lề hiếm, chỉ ba người ở Chicago từng mua.",
                "#Shorts #vụáncóthậtởmỹ #hồsơvụán #vụánlịchsử"),
    "nedkelly": ("2026-10-09 21:30", "Ned Kelly: tên cướp mặc áo giáp làm từ lưỡi cày",
                 "Ned Kelly, tên cướp nổi tiếng nhất nước Úc, bước vào trận đánh cuối năm 1880 trong bộ áo giáp tự rèn từ lưỡi cày. "
                 "Đạn bật ra khỏi ngực hắn, nhưng hai chân thì không được che.",
                 "#Shorts #NedKelly #vụánlịchsử #hồsơvụán"),
    "vidocq": ("2026-10-10 07:00", "Vidocq: kẻ vượt ngục khét tiếng nhất nước Pháp lập ra sở điều tra đầu tiên",
               "Vidocq từng là kẻ vượt ngục khét tiếng nhất nước Pháp, rồi chính hắn lập ra Sûreté, sở cảnh sát điều tra đầu tiên trên thế giới. "
               "Người hiểu tội phạm nhất là người từng là tội phạm.",
               "#Shorts #vượtngục #vụánlịchsử #hồsơvụán"),
    "rasputin": ("2026-10-10 18:30", "Rasputin là ai? Ăn bánh tẩm xyanua mà không chết?",
                 "Rasputin là ai, và có thật ông ăn bánh tẩm xyanua mà không chết? Câu chuyện nổi tiếng chủ yếu đến từ hồi ký "
                 "của chính kẻ giết ông, còn biên bản khám nghiệm tử thi kể một chuyện khác.",
                 "#Shorts #Rasputin #bíẩnlịchsử #hồsơvụán"),
    "hauser": ("2026-10-11 07:00", "Kaspar Hauser: cậu bé bí ẩn ở Nuremberg, 196 năm sau ADN mới có câu trả lời",
               "Kaspar Hauser xuất hiện ở Nuremberg năm 1828, gần như không biết nói, tay cầm một lá thư bí ẩn. "
               "Người ta đồn cậu là hoàng tử bị đánh tráo. Gần hai thế kỷ sau, ADN mới có câu trả lời.",
               "#Shorts #bíẩn #vụánlịchsử #hồsơvụán"),
    "bonnieclyde": ("2026-10-11 18:30", "Bonnie và Clyde: cuộn phim bỏ quên biến họ thành huyền thoại",
                    "Bonnie và Clyde chỉ là một băng cướp nhỏ ở miền Trung nước Mỹ, cho tới khi cảnh sát tìm thấy một cuộn phim bỏ quên năm 1933. "
                    "Những bức ảnh trong đó biến họ thành huyền thoại.",
                    "#Shorts #BonnieandClyde #vụáncóthậtởmỹ #hồsơvụán"),
    "dillinger": ("2026-10-11 21:30", "John Dillinger vượt ngục bằng khẩu súng gỗ, gục ngã sau một buổi xem phim",
                  "John Dillinger vượt ngục năm 1934 bằng một khẩu súng tự khắc từ gỗ. "
                  "Bốn tháng sau, kẻ thù số 1 của nước Mỹ gục ngã trước cửa rạp chiếu phim Biograph ở Chicago.",
                  "#Shorts #vượtngục #FBI #vụáncóthật"),
}


def headers():
    creds = json.loads(channels.creds_path("CL").read_text(encoding="utf-8"))
    return {"Authorization": f"Bearer {publish.access_token(creds)}"}


def get(H, ids):
    out = {}
    for i in range(0, len(ids), 50):
        r = requests.get(API, params={"part": "snippet,status", "id": ",".join(ids[i:i + 50])}, headers=H, timeout=60)
        r.raise_for_status()
        out.update({it["id"]: it for it in r.json()["items"]})
    return out


def put(H, part, body):
    r = requests.put(API, params={"part": part}, headers={**H, "Content-Type": "application/json"}, json=body, timeout=60)
    if r.status_code >= 300:
        raise SystemExit(f"PUT {part} {body['id']}: {r.status_code} {r.text[:300]}")


def status_body(st, publish_at):
    # PUT status ghi đè toàn bộ: luôn gửi lại embeddable/publicStatsViewable/license; publishAt=None để gỡ lịch
    return {"privacyStatus": "private", "publishAt": publish_at, "embeddable": st.get("embeddable", True),
            "publicStatsViewable": st.get("publicStatsViewable", True), "license": st.get("license", "youtube"),
            "selfDeclaredMadeForKids": st.get("madeForKids", False)}


def main():
    dry = "--dry" in sys.argv
    H = headers()
    with store.connect() as c:
        rows = c.execute("SELECT slug, video_id FROM item WHERE channel='CL' AND slug LIKE 'cl-hs-%' "
                         "AND video_id IS NOT NULL AND video_id!=''").fetchall()
    vid = {r["slug"][6:]: r["video_id"] for r in rows}
    missing = [s for s in WEEK if s not in vid]
    if missing:
        raise SystemExit(f"thiếu video_id trong store: {missing}")
    items = get(H, list(vid.values()))
    snapf = ROOT / "output/analysis/cl_week_before_2026-10-04.json"
    if not dry and not snapf.exists():
        snap = {s: {"id": v, "title": items[v]["snippet"]["title"], "description": items[v]["snippet"]["description"],
                    "publishAt": items[v]["status"].get("publishAt"), "privacy": items[v]["status"]["privacyStatus"]}
                for s, v in vid.items() if v in items}
        snapf.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")
    week_ids = {vid[s] for s in WEEK}
    n = 0
    for s, v in sorted(vid.items()):
        it = items.get(v)
        if not it or v in week_ids or it["status"]["privacyStatus"] != "private" or not it["status"].get("publishAt"):
            continue
        n += 1
        print(f"GỠ LỊCH  {s:14s} {v}  (đang hẹn {it['status']['publishAt']})")
        if not dry:
            put(H, "status", {"id": v, "status": status_body(it["status"], None)})
    print(f"-- gỡ lịch {n} video ngoài tuần test")
    for s, (vn, title, lead, tags) in WEEK.items():
        v = vid[s]
        it = items[v]
        if it["status"]["privacyStatus"] != "private":
            print(f"BỎ QUA {s}: đã {it['status']['privacyStatus']}")
            continue
        sn = it["snippet"]
        src = next((ln for ln in sn["description"].split("\n") if ln.startswith("Nguồn:")), "")
        desc = "\n\n".join(x for x in [lead, src, SRC, tags] if x)
        t = (title or sn["title"])[:100]
        print(f"{vn} VN  {s:12s} {v}  {t}" + ("" if title is None else "   [tiêu đề mới]"))
        if dry:
            continue
        snip = {"title": t, "description": desc[:5000], "tags": sn.get("tags", []), "categoryId": sn["categoryId"]}
        for k in ("defaultLanguage", "defaultAudioLanguage"):
            if sn.get(k):
                snip[k] = sn[k]
        put(H, "snippet", {"id": v, "snippet": snip})
        put(H, "status", {"id": v, "status": status_body(it["status"], utc(vn))})


if __name__ == "__main__":
    main()
