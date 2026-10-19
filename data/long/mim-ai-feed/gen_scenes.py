"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #5 "Thuật Toán Đề Xuất: Vì Sao TikTok Và YouTube Biết Bạn Thích Gì?".

    python data/long/mim-ai-feed/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md (bản 2, đã kiểm chứng) + factcheck.md. Dữ kiện + nguồn: docs/channels/mind-in-the-machine/2026-10-09-long-05-research.md.
Ảnh: chỉ PD / CC0 / CC BY (kênh MIM không nhận BY-SA — build_long kiểm lại lúc tải). Clip: Pexels (ngang), mọi clip gắn
"VIDEO MINH HỌA"; tải bằng `python motion/long/pexels.py get mim-ai-feed <id> ...`.
Quy tắc riêng của video này (factcheck mục 2 + 5):
  - Pexels 14377165 (lướt bảng tin TikTok thật) KHÔNG dùng; cũng loại các clip lộ màn hình app (6943542, 9785300, 6756650):
    BANNED bên dưới, file này tự dừng nếu cảnh nào dùng tới.
  - Bảng xếp hạng Netflix Prize dựng bằng chữ, KHÔNG ghi giờ:phút (bảng gốc chưa đọc được): "24 phút trước giờ chốt" / "20 phút sau".
    Nguồn: Feuerverger, He & Khatri, Statistical Science 2012 + thông cáo Netflix 21/09/2009.
  - Thí nghiệm bot (Hosseinmardi et al., PNAS 2024) = 60 video học chung -> 1 bot đối chứng + 3 bot phản thực tế
    (up next / ngẫu nhiên trong 30 video đầu cột bên / ngẫu nhiên trong 15 video đầu trang chủ). Sơ đồ HAI bot chỉ ở ch08 (quên ~30 video).
  - Menu app = "MÔ PHỎNG GIAO DIỆN" dựng bằng chữ (thẻ file), không logo, không chép giao diện thật; nhãn đúng nguyên văn trang trợ giúp:
    "Không quan tâm", "Không đề xuất kênh này", "Tạm dừng lưu nhật ký xem",
    "Cài đặt và quyền riêng tư → Tùy chọn nội dung → Làm mới bảng tin Đề xuất", "Quản lý chủ đề", "Lọc từ khóa".
  - Số liệu của hãng (Netflix 75%, YouTube −70%, "đề xuất > đăng ký/tìm kiếm") gắn thẻ "TỰ CÔNG BỐ".
  - Câu "Video này dài hơn…" là chữ Việt gốc của TikTok: nhãn "TRÍCH", không "TRÍCH DỊCH".
  - Dòng số ngắn trong kinetic/kin tự gắn "fx": "rise" (tránh "scramble" mặc định khi at sát đầu cảnh) — xem fix_fx().
Nhạc: chốt tay trong output/long/mim-ai-feed/bgm_picks.json (ghi bởi file này) — 5 bài MIM: ice_flow, digital_lemonade, fluidscape,
hyperfun, clean_soul. Jaccard: mim-ai-70 2/9, mim-ai-jobs 3/11, mim-ai-voice 1/9, mim-ai-hallucinate 0/10 (ngưỡng variety 35%).
"""
import json
import re
from pathlib import Path

D = Path(__file__).resolve().parent
OUT = D.parents[2] / "output" / "long" / D.name

IMGS = {
    "centre2009": "File:Centre Court (26 June 2009, Wimbledon).jpg",   # CC BY 2.0 · Squeaky Knees · 26.06.2009 · ẢNH MINH HỌA
    "ythq": "File:YouTube HQ 1.JPG",                                    # CC BY 3.0 · BrokenSphere · 09.08.2010 (không phóng to logo)
    "berlaymont": "File:Berlaymont building in Brussels.jpg",           # CC0 · almathias · 07.05.2016
}

SAY = {   # chữ hiển thị -> cách đọc (phụ đề giữ chữ gốc); "=X" = khớp đúng hoa/thường. Khoá viết thường, NFC.
    "=B": "bê",
    "netflix": "Nét-phlích", "bellkor's": "Ben-co", "pragmatic": "Prắc-ma-tích", "chaos": "Kê-ọt", "the": "Đơ", "ensemble": "An-xam-bồ",
    "tiktok": "Tíc-tóc", "youtube": "Diu-túp", "jazz": "Giát", "wimbledon": "Uim-bồn-đần", "cristos": "Crít-tốt", "goodrow": "Gút-râu",
    "google": "Gu-gồ", "recsys": "Réc-xít", "imdb": "Ai-em-đi-bi", "manoel": "Ma-nu-eo", "horta": "Óc-ta", "ribeiro": "Ri-bây-rô",
    "pnas": "Pi-en-ây-ét", "meta": "Mê-ta", "facebook": "Phây-búc", "instagram": "In-xta-gram", "science": "Xai-ần",
    "texas": "Tếch-xát", "brazil": "Bra-xin", "follow": "phô-lô",
    "bot": "bót", "link": "linh", "view": "viu", "blog": "bờ-lóc",
}

VM = "VIDEO MINH HỌA"
SELF = {"text": "TỰ CÔNG BỐ"}                 # số liệu do chính công ty công bố
MOCK = {"text": "MÔ PHỎNG GIAO DIỆN"}         # menu dựng bằng chữ theo trang trợ giúp, không phải ảnh chụp app
HELP = "THEO TRANG TRỢ GIÚP (VI), ĐỌC 09.10.2026 · GIAO DIỆN CÓ THỂ KHÁC THEO PHIÊN BẢN"
NPZ = "FEUERVERGER, HE & KHATRI · STATISTICAL SCIENCE 2012"
BANNED = {"14377165", "6943542", "9785300", "6756650"}

BGM_PICKS = {"ch00.0": "ice_flow.mp3", "ch01.0": "digital_lemonade.mp3", "ch02.0": "fluidscape.mp3", "ch03.0": "hyperfun.mp3",
             "ch04.0": "ice_flow.mp3", "ch05.0": "clean_soul.mp3", "ch06.0": "fluidscape.mp3", "ch07.0": "digital_lemonade.mp3",
             "ch08.0": "clean_soul.mp3"}

CH = {}

# ---------------- CH00 · Hai mươi phút, một triệu đô ----------------
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HAI MƯƠI PHÚT, MỘT TRIỆU ĐÔ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "NETFLIX PRIZE · NGÀY CUỐI CÙNG", "date": "26.07.2009"},
    {"type": "broll", "at": 1, "vid": "3694918", "ms": 1, "veil": 0.5, "illus": VM,
     "kin": [{"text": "GIẢI THƯỞNG: 1.000.000 USD", "at": 1},
             {"text": "NETFLIX · TREO TỪ 2006", "at": [1, "netflix"], "acc": True},
             {"text": "khi hãng còn chỉ cho thuê đĩa phim qua bưu điện", "at": [1, "khi"], "sm": True}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "ĐỀ BÀI", "at": 2, "sm": True},
                                          {"text": "KHÁCH SẼ CHẤM PHIM MẤY SAO?", "at": [2, "đoán"], "acc": True}]},
    {"type": "slam", "at": 3, "text": "CHÍNH XÁC HƠN 10%", "sub": "SO VỚI HỆ THỐNG CỦA CHÍNH NETFLIX · SAI SỐ RMSE 0,9525 → ≤ 0,8572"},
    {"type": "counter", "at": 4, "from": 0, "to": 40000, "prefix": "> ", "suffix": " ĐỘI", "label": "TỪ 186 QUỐC GIA ĐÃ NỘP BÀI",
     "sub": {"text": "THÔNG CÁO NETFLIX · 21.09.2009", "at": 4}},
    {"type": "kinetic", "at": 5, "items": [{"text": "NGÀY CUỐI", "at": 5, "sm": True},
                                          {"text": "HAI LIÊN MINH CÙNG VƯỢT VẠCH 10%", "at": [5, "hai"], "acc": True}]},
    {"type": "file", "at": 6, "k": "NỘP BÀI NGÀY CUỐI · DỰNG LẠI BẰNG CHỮ", "name": "26.07.2009", "desc": "Không ghi giờ:phút — bảng xếp hạng gốc chưa đọc được",
     "rows": [{"k": "BELLKOR'S PRAGMATIC CHAOS", "v": "*24 phút* trước giờ chốt", "at": [6, "bellkor's"]},
              {"k": "THE ENSEMBLE", "v": "*20 phút* sau", "at": 7}],
     "label": {"k": "NGUỒN", "v": "THÔNG CÁO NETFLIX 21.09.2009 · " + NPZ, "at": [7, "ensemble"]}},
    {"type": "ledger", "at": 8, "title": "BẢNG CÔNG KHAI", "srcnote": "SAI SỐ RMSE: THẤP HƠN = TỐT HƠN · " + NPZ,
     "rows": [{"k": "ENSEMBLE", "v": "0,8553", "at": [8, "ensemble"]}, {"k": "BELLKOR", "v": "0,8554", "at": [8, "nhỉnh"]}]},
    {"type": "ledger", "at": 9, "title": "PHẦN DỮ LIỆU GIỮ KÍN", "srcnote": "LUẬT: LÀM TRÒN 4 CHỮ SỐ · " + NPZ,
     "rows": [{"k": "BELLKOR", "v": "0,8567", "at": [9, "giữ"]}, {"k": "ENSEMBLE", "v": "0,8567", "at": [10, "bằng"]}],
     "total": {"k": "→", "v": "HOÀ", "at": [10, "thứ"]}},
    {"type": "kinetic", "at": 11, "items": [{"text": "VÀI TUẦN KIỂM TRA LẠI", "at": 11},
                                           {"text": "LUẬT: BÀI NỘP TRƯỚC THẮNG", "at": [11, "theo"], "acc": True}]},
    {"type": "slam", "at": 12, "text": "20 PHÚT = 1 TRIỆU ĐÔ"},
    {"type": "kinetic", "at": 13, "items": [{"text": "CHI TIẾT LẠ NHẤT", "at": 13, "sm": True},
                                           {"text": "NETFLIX NHẬN CỖ MÁY THẮNG GIẢI", "at": 14},
                                           {"text": "KHÔNG ĐƯA VÀO CHẠY THẬT", "at": [14, "không"], "acc": True}]},
    {"type": "broll", "at": 15, "vid": "7408006", "veil": 0.5, "illus": VM,
     "kin": [{"text": "HÔM NAY: TIKTOK · YOUTUBE", "at": 15, "sm": True},
             {"text": "HIẾM KHI HỎI BẠN CHẤM SAO", "at": [15, "hiếm"], "acc": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "VẬY MÀ VẪN CÓ CẢM GIÁC", "at": 16, "sm": True},
                                           {"text": "“SAO NÓ BIẾT MÌNH THÍCH GÌ?”", "at": [16, "chúng"], "acc": True}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "ĐƯỢC CHẤM ĐIỂM CẨN THẬN → BỊ CẤT ĐI", "at": 17},
                                           {"text": "HIẾM KHI HỎI → LƯỚT MỖI NGÀY", "at": 18, "acc": True}]},
    {"type": "slam", "at": 19, "text": "NGHỊCH LÝ", "sub": "VIDEO NÀY ĐI TÌM LỜI GIẢI"},
    {"type": "kinetic", "at": 20, "items": [{"text": "CUỐI VIDEO", "at": 20, "sm": True},
                                           {"text": "DẠY LẠI BẢNG TIN CỦA CHÍNH BẠN", "at": [20, "dạy"], "acc": True}]},
    {"type": "brand", "at": 21, "sub": "KHÔNG CẦN HIỂU BẠN · CHỈ CẦN NGƯỜI GIỐNG BẠN"},
]}

# ---------------- CH01 · Những người giống bạn ----------------
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "NHỮNG NGƯỜI GIỐNG BẠN"}, "bgm": {"mood": "curious", "gain": 0.13}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "NHỮNG NGƯỜI\nGIỐNG BẠN", "sub": "NETFLIX PRIZE · LỌC CỘNG TÁC", "vid": "5028622",
     "illus": VM, "titleAt": [0, "trao"]},
    {"type": "counter", "at": 1, "from": 0, "to": 100480507, "suffix": " LƯỢT CHẤM", "label": "CỦA 480.189 KHÁCH HÀNG · CHO 17.770 BỘ PHIM",
     "sub": {"text": "10.1998 – 12.2005 · " + NPZ, "at": 1}},
    {"type": "ledger", "at": 2, "title": "MỖI DÒNG CHỈ GHI", "srcnote": "THÔNG CÁO NETFLIX 2009: CHỈ TÊN PHIM, SỐ SAO, NGÀY",
     "rows": [{"k": "AI", "v": "MỘT KHÁCH HÀNG", "at": [2, "khách"]}, {"k": "PHIM", "v": "MỘT BỘ PHIM", "at": [2, "phim"]},
              {"k": "SAO", "v": "1 – 5", "at": [2, "sao"]}, {"k": "NGÀY", "v": "NGÀY CHẤM", "at": [2, "ngày"]}]},
    {"type": "dots", "at": 3, "total": 100, "cols": 20, "title": "XẾP THÀNH BẢNG: CỨ 100 Ô", "appearDur": 0.8,
     "groups": [{"from": 0, "n": 99, "cls": "ghost", "label": "99 Ô BỎ TRỐNG", "at": [3, "chín"]},
                {"from": 99, "n": 1, "cls": "red", "label": "1 Ô CÓ ĐIỂM", "at": [3, "bỏ"]}],
     "srcnote": "LÀM TRÒN · CHÍNH XÁC 98,8% TRỐNG · " + NPZ, "label": {"k": "KHÁCH × PHIM", "v": "MỖI Ô = MỘT LƯỢT CHẤM", "at": 3}},
    {"type": "kinetic", "at": 4, "items": [{"text": "ĐỀ BÀI, THỰC CHẤT", "at": 4, "sm": True},
                                          {"text": "ĐIỀN VÀO Ô TRỐNG", "at": [4, "điền"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "LỌC CỘNG TÁC", "at": 5, "acc": True},
                                          {"text": "collaborative filtering", "at": [5, "lọc"], "sm": True},
                                          {"text": "TÌM NHỮNG NGƯỜI GIỐNG BẠN", "at": [5, "tìm"]}]},
    {"type": "ledger", "at": 6, "title": "VÍ DỤ CỦA TIKTOK", "srcnote": "TRANG TRỢ GIÚP TIKTOK · ĐỌC 09.10.2026",
     "rows": [{"k": "A", "v": "1 · 2 · 3 · _ · _", "at": 7}, {"k": "B", "v": "1 · 2 · 3 · 4 · 5", "at": 8}],
     "total": {"k": "ĐOÁN", "v": "A CŨNG THÍCH 4 · 5", "at": [9, "đoán"]}},
    {"type": "kinetic", "at": 10, "items": [{"text": "YOUTUBE KỂ: BẠN HAY XEM QUẦN VỢT", "at": 10},
                                           {"text": "người thích đúng những video ấy", "at": [10, "những"], "sm": True},
                                           {"text": "CŨNG THÍCH NHẠC JAZZ", "at": [10, "jazz"], "acc": True}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "GỢI Ý CHO BẠN: JAZZ", "at": 11, "acc": True},
                                           {"text": "dù bạn chưa từng xem video jazz nào", "at": [11, "dù"], "sm": True}]},
    {"type": "slam", "at": 12, "text": "AI GIỐNG AI", "sub": "MÁY KHÔNG CẦN BIẾT JAZZ LÀ GÌ · VÍ DỤ CỦA YOUTUBE (GOODROW, 2021)"},
    {"type": "kinetic", "at": 13, "items": [{"text": "2007 · GIẢI TIẾN BỘ", "at": 13},
                                           {"text": "TRỘN 107 THUẬT TOÁN", "at": [13, "trộn"], "acc": True},
                                           {"text": "đội dẫn đầu sau một năm thi · blog Netflix 2012", "at": [13, "đội"], "sm": True}]},
    {"type": "broll", "at": 14, "vid": "1085656", "veil": 0.55, "illus": VM,
     "kin": [{"text": "NETFLIX CHỌN 2 THUẬT TOÁN MẠNH NHẤT", "at": 14},
             {"text": "ĐƯA VÀO HỆ THỐNG THẬT", "at": [14, "đưa"], "acc": True},
             {"text": "phân rã ma trận (SVD) · máy Boltzmann giới hạn (RBM)", "at": [14, "hệ"], "sm": True}]},
    {"type": "ledger", "at": 15, "title": "BẢN ĐỒ KHẨU VỊ", "srcnote": "MINH HỌA ĐƠN GIẢN HOÁ · KHÔNG PHẢI SỐ THẬT",
     "rows": [{"k": "BẠN", "v": "0,8  −0,2  0,5", "at": [15, "người"]}, {"k": "PHIM", "v": "0,7  −0,1  0,6", "at": [15, "phim"]}],
     "total": {"k": "GẦN", "v": "GU GẦN NHAU", "at": 16}},
    {"type": "timeline", "at": 17, "items": [{"year": "2006", "text": "Cuộc thi *mở*", "at": 17},
                                            {"year": "2007", "text": "Giải *tiến bộ* đầu tiên", "at": [17, "hai"]},
                                            {"year": "2009", "text": "*3 đội gộp lại* · vượt 10%", "at": [17, "ba"]}]},
    {"type": "broll", "at": 18, "vid": "5473801", "veil": 0.5, "illus": VM,
     "kin": [{"text": "KHI BÀI THẮNG GIẢI TỚI TAY", "at": 18, "sm": True},
             {"text": "NETFLIX ĐÃ ĐỔI KHÁC", "at": [18, "đổi"], "acc": True}]},
]}

# ---------------- CH02 · Một triệu đô không dùng tới ----------------
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "MỘT TRIỆU ĐÔ KHÔNG DÙNG TỚI"}, "bgm": {"mood": "calm", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "MỘT TRIỆU ĐÔ\nKHÔNG DÙNG TỚI", "sub": "NETFLIX TECHBLOG · 06.04.2012", "vid": "35002190",
     "illus": VM, "titleAt": [0, "blog"]},
    {"type": "quote", "at": 1, "text": "We evaluated some of the new methods offline but the additional accuracy gains that we measured did not seem "
                                      "to justify the engineering effort needed to bring them into a production environment.",
     "by": "X. AMATRIAIN, J. BASILICO · NETFLIX TECHBLOG, 06.04.2012", "lbl": "TRÍCH DỊCH", "qline": 1},
    {"type": "kinetic", "at": 2, "items": [{"text": "MỘT LÝ DO · THEO CHÍNH BÀI ẤY", "at": 2, "sm": True},
                                          {"text": "TRỰC TUYẾN", "at": [2, "trực"], "acc": True}]},
    {"type": "timeline", "at": 3, "items": [{"year": "2006", "text": "Cuộc thi *bắt đầu*", "at": 3},
                                           {"year": "2007", "text": "Netflix mở *xem phim trực tuyến*", "at": [3, "netflix"]}]},
    {"type": "broll", "at": 4, "vid": "6975845", "veil": 0.5, "illus": VM,
     "kin": [{"text": "VỚI PHIM TRỰC TUYẾN", "at": 4, "sm": True},
             {"text": "HÃNG THẤY ĐIỀU SỐ SAO KHÔNG NÓI", "at": [4, "hãng"], "acc": True}]},
    {"type": "quote", "at": 5, "text": "…we can observe viewing statistics such as whether a video was watched fully or only partially.",
     "by": "AMATRIAIN, BASILICO · NETFLIX TECHBLOG, 06.04.2012", "lbl": "TRÍCH DỊCH", "qline": 5},
    {"type": "counter", "at": 6, "from": 0, "to": 75, "prefix": "≈ ", "suffix": "%", "label": "NHỮNG GÌ NGƯỜI TA XEM ĐẾN TỪ ĐỀ XUẤT", "tag": SELF,
     "sub": {"text": "NETFLIX TỰ CÔNG BỐ · TECHBLOG 2012", "at": 6}},
    {"type": "date", "at": 7, "day": "HÔM TRAO GIẢI · CÔNG BỐ CUỘC THI THỨ HAI", "date": "21.09.2009"},
    {"type": "kinetic", "at": 8, "items": [{"text": "ĐOÁN GU CẢ NHỮNG NGƯỜI HIẾM KHI CHẤM SAO", "at": 8},
                                          {"text": "DỰA VÀO HÀNH VI", "at": [8, "dựa"], "acc": True}]},
    {"type": "slam", "at": 9, "text": "KHÔNG BAO GIỜ DIỄN RA", "white": True},
    {"type": "file", "at": 10, "k": "NARAYANAN & SHMATIKOV · 2006–2008", "name": "Đại học Texas", "desc": "Dữ liệu “ẩn danh” của cuộc thi thứ nhất",
     "rows": [{"k": "KẾT QUẢ", "v": "*có thể bị lần ngược*", "at": [10, "lần"]},
              {"k": "ĐỐI CHIẾU", "v": "lời chấm phim công khai trên *IMDb*", "at": 11},
              {"k": "LỘ RA", "v": "sở thích *có thể nhạy cảm*, như quan điểm chính trị", "at": 12}]},
    {"type": "file", "at": 13, "k": "NĂM 2010 · CUỘC THI THỨ HAI", "name": "Bị huỷ", "desc": "Netflix huỷ kế hoạch “Prize 2”",
     "rows": [{"k": "VỤ KIỆN", "v": "*Doe v. Netflix* · toà liên bang, California · 17.12.2009", "at": [13, "vụ"]},
              {"k": "CƠ QUAN MỸ", "v": "*FTC* gửi thư nêu lo ngại · 03.11.2009", "at": [13, "câu"]},
              {"k": "KHÉP HỒ SƠ", "v": "thư FTC · *12.03.2010*", "at": [13, "huỷ"]}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "BÀI HỌC ĐẦU TIÊN", "at": 14, "sm": True},
                                           {"text": "DẤU VẾT XEM NÓI NHIỀU HƠN SỐ SAO", "at": [14, "dấu"], "acc": True},
                                           {"text": "và cũng riêng tư hơn", "at": [14, "riêng"], "sm": True}]},
    {"type": "broll", "at": 15, "vid": "36392510", "veil": 0.4, "illus": VM,
     "kin": [{"text": "MỘT CÔNG TY KHÁC", "at": 15, "sm": True},
             {"text": "HỌC QUA NHỮNG CÚ NHẤP CHUỘT", "at": [15, "qua"], "acc": True}]},
]}

# ---------------- CH03 · Cú nhấp biết nói dối ----------------
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "CÚ NHẤP BIẾT NÓI DỐI"}, "bgm": {"mood": "upbeat", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "CÚ NHẤP\nBIẾT NÓI DỐI", "sub": "YOUTUBE · 2008 — 2016", "vid": "4973409",
     "illus": VM, "titleAt": [0, "goodrow"]},
    {"type": "print", "at": 1, "img": "ythq", "tone": "color", "maxH": 560, "maxW": 700, "caption": "TRỤ SỞ YOUTUBE, SAN BRUNO · ẢNH 2010",
     "side": {"k": "YOUTUBE · 2008", "h": "Xếp theo\nđộ phổ biến", "lines": [
         {"text": "Một trang *Thịnh hành* chung cho mọi người", "at": [1, "thịnh"]},
         {"text": "Rồi: *bấm vào = muốn xem*", "at": 2}]}},
    {"type": "kinetic", "at": 3, "items": [{"text": "2011", "at": 3, "sm": True},
                                          {"text": "BẤM VÀO ≠ ĐÃ THẬT SỰ XEM", "at": [3, "bấm"], "acc": True}]},
    {"type": "photo", "at": 4, "img": "centre2009", "tone": "color", "move": "in", "veil": 0.45, "illus": "ẢNH MINH HỌA",
     "kin": [{"text": "BẠN TÌM VIDEO TRẬN ĐẤU Ở WIMBLEDON", "at": 4}],
     "label": {"k": "SÂN TRUNG TÂM WIMBLEDON", "v": "26.06.2009", "at": 4}},
    {"type": "kinetic", "at": 5, "items": [{"text": "ẢNH + TIÊU ĐỀ: CẢNH TRẬN ĐẤU", "at": 5},
                                          {"text": "BẤM VÀO: MỘT NGƯỜI NGỒI BÌNH LUẬN", "at": [5, "bấm"], "acc": True},
                                          {"text": "ví dụ của Goodrow · YouTube Blog, 15.09.2021", "at": [5, "phòng"], "sm": True}]},
    {"type": "slam", "at": 6, "text": "THỜI GIAN XEM", "sub": "YOUTUBE ĐƯA VÀO HỆ THỐNG · 2012"},
    {"type": "file", "at": 7, "k": "RECSYS 2016 · BA KỸ SƯ GOOGLE", "name": "Covington,\nAdams, Sargin",
     "desc": "“Deep Neural Networks for YouTube Recommendations”",
     "rows": [{"k": "HỘI NGHỊ", "v": "*RecSys* · 15–19.09.2016", "at": [7, "recsys"]},
              {"k": "HỌ VIẾT THẲNG", "v": "về *tỉ lệ nhấp*", "at": 8}]},
    {"type": "quote", "at": 9, "text": "Ranking by click-through rate often promotes deceptive videos that the user does not complete "
                                      "(“clickbait”) whereas watch time better captures engagement.",
     "by": "COVINGTON, ADAMS, SARGIN · RECSYS 2016, §4", "lbl": "TRÍCH DỊCH", "qline": 9},
    {"type": "ledger", "at": 10, "title": "DẠY MÔ HÌNH BẰNG GÌ?", "srcnote": "COVINGTON ET AL. 2016 · §3",
     "rows": [{"k": "THÍCH", "v": "CÓ NÚT", "at": [10, "thích"]}, {"k": "KHẢO SÁT", "v": "CÓ", "at": [10, "khảo"]}],
     "total": {"k": "CHỦ YẾU", "v": "VIỆC XEM", "at": [10, "việc"]}},
    {"type": "kinetic", "at": 11, "items": [{"text": "XEM HẾT = MỘT VÍ DỤ TÍCH CỰC", "at": 11, "acc": True},
                                           {"text": "dấu vết xem nhiều hơn cú bấm chủ động gấp bội · “orders of magnitude”", "at": [11, "vì"], "sm": True}]},
    {"type": "bars", "at": 12, "title": "HAI VÒNG LỌC", "unit": "VẼ LẠI THEO HÌNH 2, COVINGTON ET AL. 2016 · KHÔNG THEO TỈ LỆ", "max": 100,
     "items": [{"k": "KHO VIDEO", "v": 100, "lbl": "HÀNG TRIỆU", "at": 12},
               {"k": "SAU VÒNG 1", "v": 38, "lbl": "VÀI TRĂM", "at": [13, "vài"]},
               {"k": "SAU VÒNG 2", "v": 12, "lbl": "VÀI CHỤC", "at": [14, "vài"], "acc": True}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "MỘT CHI TIẾT BẤT NGỜ", "at": 15, "acc": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "YOUTUBE HỎI LẠI", "at": 16, "sm": True},
                                           {"text": "CHẤM TỪ 1 ĐẾN 5 SAO", "at": [16, "chấm"], "acc": True}]},
    {"type": "ledger", "at": 17, "title": "KHẢO SÁT SAU KHI XEM", "srcnote": "GOODROW · YOUTUBE BLOG, 15.09.2021",
     "rows": [{"k": "4–5 SAO", "v": "XEM CÓ GIÁ TRỊ", "at": [17, "bốn"]}, {"k": "1–3 SAO", "v": "KHÔNG TÍNH", "at": [17, "giá"]}],
     "total": {"k": "IM LẶNG", "v": "MÁY ĐOÁN HỘ", "at": [17, "ai"]}},
    {"type": "slam", "at": 18, "text": "NGÔI SAO\nLÙI XUỐNG LÀM GIÁM KHẢO"},
    {"type": "broll", "at": 19, "vid": "6968278", "veil": 0.5, "illus": VM,
     "kin": [{"text": "CÒN Ở TIKTOK", "at": 19, "sm": True},
             {"text": "NGÓN TAY CÁI CỦA BẠN", "at": [19, "ngón"], "acc": True}]},
]}

# ---------------- CH04 · Bạn chưa nói gì ----------------
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "BẠN CHƯA NÓI GÌ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "BẠN\nCHƯA NÓI GÌ", "sub": "TIKTOK NEWSROOM · 18.06.2020", "vid": "7339512",
     "illus": VM, "titleAt": [0, "tiktok"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "MỚI VÀO: CHỌN VÀI CHỦ ĐỀ", "at": 1},
                                          {"text": "như thú cưng hay du lịch", "at": [1, "như"], "sm": True}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "BỎ QUA CŨNG ĐƯỢC", "at": 2},
                                          {"text": "→ NHỮNG VIDEO ĐANG PHỔ BIẾN", "at": [2, "những"], "acc": True}]},
    {"type": "ledger", "at": 3, "title": "MỌI THỨ THÀNH TÍN HIỆU", "srcnote": "TIKTOK NEWSROOM 2020 · TRANG TRỢ GIÚP 2026",
     "rows": [{"k": "1", "v": "THÍCH VIDEO NÀO", "at": [3, "thích"]}, {"k": "2", "v": "XEM HẾT VIDEO NÀO", "at": [3, "xem"]},
              {"k": "3", "v": "LƯỚT QUA VIDEO NÀO", "at": [3, "lướt"]}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "TÍN HIỆU NẶNG NHẸ KHÁC NHAU", "at": 4, "acc": True},
                                          {"text": "theo lời của chính TikTok", "at": [4, "khác"], "sm": True}]},
    {"type": "quote", "at": 5, "text": "A strong indicator of interest, such as whether a user finishes watching a longer video from beginning to end, "
                                      "would receive greater weight than a weak indicator, such as whether the video's viewer and creator are both in the same country.",
     "by": "TIKTOK NEWSROOM · 18.06.2020 · LỜI CỦA HÃNG", "lbl": "TRÍCH DỊCH", "qline": 5},
    {"type": "quote", "at": 6, "typeAt": 7, "text": "For most users, user interactions, which may include the time spent watching a video, "
                                                   "are generally weighted more heavily than others.",
     "by": "TIKTOK SUPPORT · “HOW TIKTOK RECOMMENDS CONTENT” · ĐỌC 09.10.2026", "lbl": "TRÍCH DỊCH", "qline": 7},
    {"type": "file", "at": 8, "k": "TIKTOK · CÁC BƯỚC THEO TRANG TRỢ GIÚP (VI)", "name": "Vì sao bài này\nhiện ra?", "tag": MOCK,
     "rows": [{"k": "BƯỚC 1", "v": "Nhấn nút *Chia sẻ*", "at": [8, "chia"]},
              {"k": "BƯỚC 2", "v": "*Tại sao đăng bài này hiển thị*", "at": [8, "tại"]}],
     "srcnote": HELP},
    {"type": "quote", "at": 9, "text": "Video này dài hơn và có vẻ như bạn thích những video dài hơn.",
     "by": "TRANG TRỢ GIÚP TIKTOK (TIẾNG VIỆT) · “ĐỀ XUẤT” · LÝ DO MẪU, NGUYÊN VĂN", "lbl": "TRÍCH", "qline": 9},
    {"type": "slam", "at": 10, "text": "BẠN CHƯA NÓI GÌ", "sub": "CHƯA BẤM GÌ"},
    {"type": "kinetic", "at": 11, "items": [{"text": "BẠN CHỈ DỪNG LẠI XEM", "at": 11},
                                           {"text": "ĐÃ LÀ MỘT CÂU TRẢ LỜI", "at": [11, "đã"], "acc": True}]},
    {"type": "question", "at": 12, "text": "Đó là lời của chính hãng.\nAi kiểm tra từ bên ngoài?"},
    {"type": "file", "at": 13, "k": "WWW ’22 · BOEKER & URMAN", "name": "Đại học Zurich", "desc": "Tài khoản tự động trên TikTok (bản web) · thử từng yếu tố",
     "rows": [{"k": "YẾU TỐ", "v": "ngôn ngữ · vị trí", "at": [14, "ngôn"]},
              {"k": "YẾU TỐ", "v": "follow · thả tim", "at": [14, "follow"]},
              {"k": "YẾU TỐ", "v": "thời gian xem", "at": [14, "thời"]}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "YẾU TỐ NÀO CŨNG", "at": 15, "sm": True},
                                           {"text": "LÀM BẢNG TIN THAY ĐỔI", "at": [15, "làm"], "acc": True}]},
    {"type": "ledger", "at": 16, "title": "MẠNH NHẤT → YẾU HƠN", "srcnote": "BOEKER & URMAN · WWW 2022",
     "rows": [{"k": "1", "v": "FOLLOW", "at": [16, "follow"]}, {"k": "2", "v": "THẢ TIM", "at": [16, "thả"]},
              {"k": "3", "v": "TỈ LỆ XEM", "at": [16, "tỉ"]}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "KHÔNG ĐƠN GIẢN LÀ", "at": 17, "sm": True},
                                           {"text": "“CỨ XEM LÂU LÀ XONG”", "at": [17, "cứ"], "fx": "strike", "strikeAt": [17, "xong"]}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "YOUTUBE: KHÔNG CÓ “SÁCH CÔNG THỨC”", "at": 18},
                                           {"text": "mỗi tín hiệu nặng nhẹ tuỳ từng người · “recipe book” · Goodrow 2021", "at": [18, "mỗi"], "sm": True}]},
    {"type": "kinetic", "at": 19, "items": [{"text": "CÔNG BỐ: NGUYÊN LIỆU", "at": 19},
                                           {"text": "KHÔNG CÔNG BỐ: CÔNG THỨC", "at": [19, "họ"], "acc": True}]},
]}

# ---------------- CH05 · Lời giải của nghịch lý ----------------
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "LỜI GIẢI CỦA NGHỊCH LÝ"}, "bgm": {"mood": "warm", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "LỜI GIẢI\nCỦA NGHỊCH LÝ", "sub": "QUAY LẠI 26.07.2009", "vid": "30293430",
     "illus": VM, "titleAt": [0, "quay"]},
    {"type": "ledger", "at": 1, "title": "SAI SỐ · 6 CHỮ SỐ", "srcnote": NPZ,
     "rows": [{"k": "BELLKOR", "v": "0,856704", "at": [1, "hai"]}, {"k": "ENSEMBLE", "v": "0,856714", "at": [1, "lệch"]}],
     "total": {"k": "LỆCH", "v": "0,00001", "at": [1, "một"]}},
    {"type": "kinetic", "at": 2, "items": [{"text": "CẢ THẾ GIỚI ĐUA NHAU", "at": 2, "sm": True},
                                          {"text": "ĐOÁN NHỮNG NGÔI SAO", "at": [2, "đoán"], "acc": True}]},
    {"type": "slam", "at": 3, "text": "NGÔI SAO = ĐIỀU BẠN NÓI"},
    {"type": "kinetic", "at": 4, "items": [{"text": "MÁY DỰA VÀO NHIỀU NHẤT", "at": 4, "sm": True},
                                          {"text": "theo chính lời các hãng", "at": [4, "theo"], "sm": True},
                                          {"text": "ĐIỀU BẠN LÀM", "at": [4, "làm"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "XEM GÌ", "at": 5}, {"text": "XEM BAO LÂU", "at": [5, "bao"]},
                                          {"text": "LƯỚT QUA GÌ", "at": [5, "lướt"], "acc": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "LỜI GIẢI CỦA NGHỊCH LÝ", "at": 6, "sm": True},
                                          {"text": "VIỆC XEM ĐÃ TRẢ LỜI THAY", "at": [6, "việc"], "acc": True},
                                          {"text": "Netflix cũng bỏ thang 5 sao · “Goodbye Stars, Hello Thumbs” · 05.04.2017", "at": [6, "trả"], "sm": True}]},
    {"type": "ledger", "at": 7, "title": "LƯỢT XEM ĐẾN TỪ ĐÂU?", "tag": SELF, "srcnote": "YOUTUBE TỰ CÔNG BỐ · GOODROW, 15.09.2021",
     "rows": [{"k": "1", "v": "ĐỀ XUẤT", "at": [7, "đề"]}, {"k": "↓", "v": "KÊNH ĐÃ ĐĂNG KÝ", "at": [7, "kênh"]},
              {"k": "↓", "v": "TÌM KIẾM", "at": [7, "tìm"]}]},
    {"type": "broll", "at": 8, "vid": "29109432", "veil": 0.45, "illus": VM,
     "kin": [{"text": "CỨ ĐI THEO CHỖ BẠN DỪNG LẠI LÂU", "at": 8, "sm": True},
             {"text": "MỘT CÂU HỎI ĐÁNG LO HƠN", "at": [8, "câu"], "acc": True}]},
    {"type": "question", "at": 9, "text": "Nó có kéo bạn, từng video một,\nxuống một cái hang thỏ không?"},
]}

# ---------------- CH06 · Hang thỏ ----------------
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "HANG THỎ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "HANG THỎ", "sub": "YOUTUBE · 2019 — 2024", "vid": "29109378",
     "illus": VM, "titleAt": [0, "hang"]},
    {"type": "file", "at": 1, "k": "FAT* 2020 · ARXIV 22.08.2019", "name": "Horta Ribeiro\nvà cộng sự", "desc": "EPFL (Thuỵ Sĩ) · UFMG (Brazil)",
     "rows": [{"k": "VIDEO", "v": "*330.925* video · 349 kênh", "at": 2},
              {"k": "BÌNH LUẬN", "v": "*hơn 72 triệu*", "at": 3},
              {"k": "THẤY", "v": "người dùng đi từ *ôn hoà* sang *cực đoan* hơn", "at": [3, "đều"]}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "BÌNH LUẬN KHÓ CHO BIẾT", "at": 4, "sm": True},
                                          {"text": "TỰ TÌM ĐẾN", "at": [4, "tự"]},
                                          {"text": "HAY ĐƯỢC MÁY DẪN ĐẾN?", "at": [4, "hay"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "2019 · YOUTUBE GIẢM ĐỀ XUẤT", "at": 5, "sm": True},
                                          {"text": "NỘI DUNG “SÁT LẰN RANH”", "at": [5, "sát"], "acc": True},
                                          {"text": "chưa vi phạm quy định, nhưng gần vi phạm", "at": [5, "chưa"], "sm": True}]},
    {"type": "counter", "at": 6, "from": 0, "to": 70, "prefix": "−", "suffix": "%", "tag": SELF,
     "label": "THỜI GIAN XEM LOẠI NÀY QUA ĐỀ XUẤT · MỸ", "sub": {"text": "YOUTUBE TỰ CÔNG BỐ · ĐỀ XUẤT TỪ KÊNH CHƯA ĐĂNG KÝ", "at": 6}},
    {"type": "counter", "at": 7, "from": 0, "to": 1181, "suffix": " NGƯỜI", "label": "TÌNH NGUYỆN · THEO DÕI TRONG NĂM 2020",
     "sub": {"text": "CHEN ET AL. · SCIENCE ADVANCES, 30.08.2023", "at": 7}},
    {"type": "kinetic", "at": 8, "items": [{"text": "TẬP TRUNG Ở MỘT NHÓM NHỎ", "at": 8, "acc": True},
                                          {"text": "vốn đã mang nặng ác cảm về giới và chủng tộc", "at": [8, "vốn"], "sm": True},
                                          {"text": "TỰ ĐĂNG KÝ · BẤM LINK TỪ NƠI KHÁC", "at": [8, "họ"]}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "NGƯỜI KHÔNG ĐĂNG KÝ", "at": 9, "sm": True},
                                          {"text": "HIẾM KHI ĐƯỢC DẪN TỚI", "at": [9, "hiếm"], "acc": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "THÍ NGHIỆM KHÉO NHẤT", "at": 10, "acc": True}]},
    {"type": "file", "at": 11, "k": "PNAS · 13.02.2024", "name": "Bot phản thực tế", "desc": "Hosseinmardi, Ghasemian, Rivera-Lanas, Horta Ribeiro, West, Watts",
     "rows": [{"k": "BOT", "v": "tài khoản tự động, *đăng nhập*", "at": [11, "bot"]},
              {"k": "PHẠM VI", "v": "Mỹ · máy tính · thí nghiệm *đầu 2023*", "at": [11, "phản"]}]},
    {"type": "org", "at": 12, "y0": 170, "nodes": [
        {"id": "L", "t": "60 VIDEO ĐẦU", "s": "4 BOT · LỊCH SỬ THẬT", "cls": "top", "at": 12},
        {"id": "c", "p": "L", "t": "BOT ĐỐI CHỨNG", "s": "60 VIDEO TIẾP CỦA NGƯỜI ẤY", "at": [12, "lặp"]},
        {"id": "u", "p": "L", "t": "“UP NEXT”", "s": "LUÔN BẤM VIDEO ĐẦU CỘT BÊN", "cls": "acc", "at": [13, "rồi"]},
        {"id": "s", "p": "L", "t": "CỘT BÊN", "s": "NGẪU NHIÊN 1/30 VIDEO ĐẦU", "cls": "acc", "at": [13, "bấm"]},
        {"id": "h", "p": "L", "t": "TRANG CHỦ", "s": "NGẪU NHIÊN 1/15 VIDEO ĐẦU", "cls": "acc", "at": [13, "đề"]}],
     "label": {"k": "HOSSEINMARDI ET AL. · PNAS 2024", "v": "1 ĐỐI CHỨNG + 3 BOT PHẢN THỰC TẾ", "at": [13, "ba"]}},
    {"type": "kinetic", "at": 14, "items": [{"text": "KẾT QUẢ · TRUNG BÌNH", "at": 14, "sm": True},
                                           {"text": "BOT CHỈ NGHE ĐỀ XUẤT", "at": [14, "bot"]},
                                           {"text": "XEM ÍT NỘI DUNG THIÊN LỆCH HƠN", "at": [14, "ít"], "acc": True},
                                           {"text": "rõ nhất với người vốn xem rất nhiều nội dung thiên lệch", "at": [14, "người"], "sm": True}]},
    {"type": "quote", "at": 15, "text": "…at least since the algorithm changes that YouTube implemented in 2019, individual consumption patterns mostly "
                                       "reflect individual preferences, where algorithmic recommendations play, if anything, a moderating role.",
     "by": "HOSSEINMARDI ET AL. · PNAS, 13.02.2024", "lbl": "TRÍCH DỊCH"},
    {"type": "slam", "at": 17, "text": "CHƯA NÊN KẾT LUẬN VỘI", "white": True},
    {"type": "counter", "at": 18, "from": 0, "to": 100000, "suffix": " TÀI KHOẢN GIẢ", "label": "TRÊN YOUTUBE",
     "sub": {"text": "HAROON ET AL. · PNAS, 05.12.2023", "at": 18}},
    {"type": "ledger", "at": 19, "title": "HAROON ET AL. 2023", "srcnote": "100.000 TÀI KHOẢN GIẢ · YOUTUBE · MỸ",
     "rows": [{"k": "→", "v": "QUAN ĐIỂM SẴN CÓ", "at": [19, "nghiêng"]},
              {"k": "SÂU", "v": "RÕ HƠN: THIÊN HỮU", "at": [19, "càng"]},
              {"k": "≠", "v": "CỰC ĐOAN DẦN LÊN", "at": [19, "dù"]}]},
    {"type": "bars", "at": [19, "cực"], "title": "ĐỀ XUẤT TỪ KÊNH “CÓ VẤN ĐỀ”",
     "unit": "HAROON ET AL. 2023 · TỈ LỆ TĂNG DẦN THEO ĐỘ SÂU", "max": 50,
     "items": [{"k": "ĐỀ XUẤT (TỐI ĐA)", "v": 2.5, "lbl": "2,5%"}, {"k": "TÀI KHOẢN TỪNG GẶP", "v": 36.1, "lbl": "36,1%", "acc": True}]},
    {"type": "timeline", "at": 20, "items": [{"year": "2019", "text": "Ribeiro · *bình luận*", "at": 20},
                                            {"year": "2020", "text": "Chen · *1.181 người*", "at": [20, "năm"]},
                                            {"year": "2023", "text": "Haroon · *tài khoản giả*", "at": [20, "cách"]},
                                            {"year": "2024", "text": "Hosseinmardi · *bot*", "at": [20, "youtube"]}],
     "label": {"k": "PHẦN LỚN", "v": "YOUTUBE · MỸ", "at": [20, "mỹ"]}},
    {"type": "kinetic", "at": 21, "items": [{"text": "HANG THỎ CÓ THỂ CÓ", "at": 21},
                                           {"text": "KHÔNG PHẢI AI CŨNG BỊ KÉO XUỐNG", "at": [21, "nhưng"], "acc": True}]},
    {"type": "kinetic", "at": 22, "items": [{"text": "THUẬT TOÁN KHÔNG PHẢI LỰC DUY NHẤT", "at": 22}]},
    {"type": "question", "at": [22, "vậy"], "text": "Nếu tắt hẳn thuật toán đi thì sao?"},
]}

# ---------------- CH07 · Tắt thuật toán đi ----------------
CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "TẮT THUẬT TOÁN ĐI"}, "bgm": {"mood": "curious", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "TẮT\nTHUẬT TOÁN ĐI", "sub": "META · SCIENCE 2023", "vid": "30607101",
     "illus": VM, "titleAt": [0, "người"]},
    {"type": "date", "at": 1, "day": "BẦU CỬ MỸ · THÍ NGHIỆM CÙNG META", "date": "24.09.2020",
     "sub": {"text": "ĐẾN 23.12.2020 · BA THÁNG", "at": [1, "ba"]}},
    {"type": "ledger", "at": 2, "title": "BẢNG TIN THEO THỜI GIAN", "srcnote": "GUESS ET AL. · SCIENCE, 27.07.2023",
     "rows": [{"k": "AI", "v": "FACEBOOK · INSTAGRAM", "at": 2}, {"k": "↑", "v": "BÀI MỚI NHẤT LÊN ĐẦU", "at": [2, "bài"]},
              {"k": "0", "v": "THUẬT TOÁN XẾP HẠNG", "at": [2, "không"]}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "SCIENCE · 27.07.2023", "at": 3, "sm": True},
                                          {"text": "BA ĐIỀU ĐÁNG CHÚ Ý", "at": [3, "ba"], "acc": True}]},
    {"type": "file", "at": 4, "k": "GUESS ET AL. · FACEBOOK/INSTAGRAM · MỸ · 3 THÁNG · 2020", "name": "Bảng tin\ntheo thời gian",
     "rows": [{"k": "1", "v": "dùng ứng dụng *ít hẳn đi*", "at": 4},
              {"k": "2", "v": "*nhiều hơn*: nội dung chính trị, nguồn kém tin cậy", "at": 5}]},
    {"type": "kinetic", "at": [5, "so"], "items": [{"text": "SO VỚI THUẬT TOÁN THỜI ĐIỂM ĐÓ", "at": [5, "so"], "acc": True},
                                                  {"text": "thư góp ý trên Science, 09.2024: Meta có 63 thay đổi khẩn cấp quanh bầu cử 2020", "at": [5, "thuật"], "sm": True},
                                                  {"text": "nhóm tác giả: kết quả là so với thuật toán Facebook lúc nghiên cứu", "at": [5, "đó"], "sm": True}]},
    {"type": "slam", "at": 6, "text": "PHÂN CỰC: KHÔNG ĐỔI ĐÁNG KỂ", "sub": "SAU BA THÁNG · GUESS ET AL., SCIENCE 2023"},
    {"type": "kinetic", "at": 7, "items": [{"text": "KHÔNG TỰ ĐỘNG SẠCH HƠN", "at": 7},
                                          {"text": "CHỈ KHÁC ĐI", "at": [7, "nó"], "acc": True}]},
    {"type": "photo", "at": 8, "img": "berlaymont", "tone": "color", "move": "in", "veil": 0.5, "illus": "ẢNH MINH HỌA",
     "kin": [{"text": "CHÂU ÂU · TỪ 08.2023", "at": 8, "sm": True},
             {"text": "TẮT CÁ NHÂN HOÁ TRÊN TIKTOK", "at": [8, "tắt"], "acc": True},
             {"text": "theo Đạo luật Dịch vụ số (DSA)", "at": [8, "theo"], "sm": True}],
     "label": {"k": "ỦY BAN CHÂU ÂU (BERLAYMONT), BRUSSELS", "v": "ẢNH 2016", "at": 8}},
    {"type": "kinetic", "at": 9, "items": [{"text": "CHỈ CÒN VIDEO ĐANG PHỔ BIẾN", "at": 9, "acc": True},
                                          {"text": "ở nơi bạn sống và trên thế giới · TikTok Newsroom, 04.08.2023", "at": [9, "ở"], "sm": True}]},
    {"type": "ledger", "at": 10, "title": "NÚT NÀY CÓ Ở ĐÂU?", "srcnote": "TRANG TRỢ GIÚP TIKTOK · ĐỌC 09.10.2026",
     "rows": [{"k": "CÓ", "v": "EU · KAZAKHSTAN", "at": [10, "liên"]}, {"k": "CÓ", "v": "EEA · ANH · THUỴ SĨ", "at": [10, "vài"]}],
     "total": {"k": "KHÔNG", "v": "VIỆT NAM", "at": [10, "không"]}},
    {"type": "broll", "at": 11, "vid": "31873137", "veil": 0.5, "illus": VM,
     "kin": [{"text": "Ở VIỆT NAM", "at": 11, "sm": True},
             {"text": "ĐÃ LÊN TỚI CƠ QUAN QUẢN LÝ", "at": [11, "đã"], "acc": True}]},
    {"type": "date", "at": 12, "day": "BỘ THÔNG TIN VÀ TRUYỀN THÔNG · HỌP BÁO", "date": "06.04.2023",
     "sub": {"text": "NÊU: THUẬT TOÁN TẠO XU HƯỚNG · NỘI DUNG GIẬT GÂN, CÂU VIEW", "at": [12, "tiktok"]}},
    {"type": "date", "at": 13, "day": "BỘ TT&TT CÔNG BỐ KẾT LUẬN KIỂM TRA", "date": "05.10.2023",
     "sub": {"text": "SAU HƠN 4 THÁNG KIỂM TRA TOÀN DIỆN", "at": [13, "sau"]}},
    {"type": "quote", "at": 14, "text": "Không sử dụng thuật toán để tạo xu hướng hoặc đề xuất đến người dùng các nội dung vi phạm pháp luật Việt Nam.",
     "by": "KẾT LUẬN KIỂM TRA TIKTOK · BÁO ĐIỆN TỬ CHÍNH PHỦ, 05.10.2023", "lbl": "TRÍCH"},
    {"type": "kinetic", "at": 15, "items": [{"text": "LUẬT VẠCH RA GIỚI HẠN", "at": 15}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "MỖI NGÀY, BẢNG TIN ĐƯỢC DẠY BỞI", "at": 16, "sm": True},
                                           {"text": "CHÍNH BẠN", "at": [16, "chính"], "acc": True}]},
]}

# ---------------- CH08 · Dạy lại bảng tin của bạn ----------------
CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "DẠY LẠI BẢNG TIN CỦA BẠN"}, "bgm": {"mood": "warm", "gain": 0.13}, "scenes": [
    {"type": "chapter", "no": "8", "k": "CHƯƠNG TÁM", "title": "DẠY LẠI\nBẢNG TIN CỦA BẠN", "sub": "BA VIỆC · THEO TRANG TRỢ GIÚP, 10.2026", "vid": "6951593",
     "ms": 30, "illus": VM, "titleAt": [0, "youtube"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "VIỆC 1", "at": 1, "sm": True},
                                          {"text": "NÓI “KHÔNG” CHO RÕ RÀNG", "at": [1, "nói"], "acc": True}]},
    {"type": "file", "at": 2, "k": "YOUTUBE · TUỲ CHỌN KHÁC (DẤU BA CHẤM CẠNH VIDEO)", "name": "YouTube", "tag": MOCK, "srcnote": HELP,
     "rows": [{"k": "CHỌN", "v": "*Không quan tâm*", "at": [2, "không"]},
              {"k": "HOẶC", "v": "*Không đề xuất kênh này*", "at": [2, "không", 1]}]},
    {"type": "file", "at": 3, "k": "TIKTOK · NHẤN GIỮ VIDEO", "name": "TikTok", "tag": MOCK, "srcnote": HELP,
     "rows": [{"k": "CHỌN", "v": "*Không quan tâm*", "at": [3, "không"]},
              {"k": "LƯỚT QUA NHANH", "v": "cũng là một tín hiệu (“skip”)", "at": 4}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "VIỆC 2", "at": 5, "sm": True},
                                          {"text": "DỌN LỊCH SỬ", "at": [5, "dọn"], "acc": True}]},
    {"type": "file", "at": 6, "k": "YOUTUBE · NHẬT KÝ XEM", "name": "YouTube", "tag": MOCK, "srcnote": HELP,
     "rows": [{"k": "XOÁ", "v": "từng video khỏi nhật ký xem", "at": [6, "xoá"]},
              {"k": "TẠM DỪNG", "v": "*Tạm dừng lưu nhật ký xem*", "at": 7},
              {"k": "XOÁ + TẮT HẾT", "v": "Trang chủ *không còn video đề xuất*", "at": 8}]},
    {"type": "file", "at": 9, "k": "TIKTOK · HỒ SƠ → MENU", "name": "TikTok", "tag": MOCK, "srcnote": HELP,
     "rows": [{"k": "BƯỚC 1", "v": "*Cài đặt và quyền riêng tư*", "at": [9, "cài"]},
              {"k": "BƯỚC 2", "v": "*Tùy chọn nội dung*", "at": [9, "tùy"]},
              {"k": "BƯỚC 3", "v": "*Làm mới bảng tin Đề xuất*", "at": [9, "làm"]},
              {"k": "LƯU Ý", "v": "làm mới rồi *không hoàn tác được*", "at": [10, "làm"]}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "VIỆC 3", "at": 11, "sm": True},
                                           {"text": "CHỦ ĐỘNG CHỌN", "at": [11, "chủ"], "acc": True}]},
    {"type": "file", "at": 12, "k": "TIKTOK · TÙY CHỌN NỘI DUNG", "name": "TikTok", "tag": MOCK, "srcnote": HELP,
     "rows": [{"k": "CHỦ ĐỀ", "v": "*Quản lý chủ đề* · kéo thanh trượt: nhiều hơn / ít hơn", "at": [12, "kéo"]},
              {"k": "VÍ DỤ", "v": "thể thao · ẩm thực", "at": [12, "thể"]},
              {"k": "TỪ KHOÁ", "v": "*Lọc từ khóa* · chặn video chứa chữ bạn không muốn thấy", "at": 13}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "KHÔNG ĐỔI HẲN SAU MỘT LẦN BẤM", "at": 14},
                                           {"text": "NHƯNG CŨNG KHÔNG NHỚ MÃI", "at": [14, "nhưng"], "acc": True}]},
    {"type": "org", "at": 15, "y0": 190, "nodes": [
        {"id": "p", "t": "BOT ĐỔI SANG ÔN HOÀ", "s": "TRƯỚC ĐÓ XEM THIÊN LỆCH", "cls": "top", "at": 15},
        {"id": "a", "p": "p", "t": "CỘT BÊN", "s": "QUÊN SAU ~30 VIDEO", "cls": "acc", "at": [15, "quên"]},
        {"id": "b", "p": "p", "t": "TRANG CHỦ", "s": "ĐỔI CHẬM HƠN", "at": 16}],
     "label": {"k": "HOSSEINMARDI ET AL. · PNAS 2024", "v": "THÍ NGHIỆM “QUÊN” · CÔNG BỐ 2024", "at": [15, "nghiên"]}},
    {"type": "kinetic", "at": 17, "items": [{"text": "NETFLIX TỪNG TRẢ 1 TRIỆU ĐÔ", "at": 17},
                                           {"text": "để đoán bạn chấm phim mấy sao", "at": [17, "để"], "sm": True}]},
    {"type": "slam", "at": 18, "text": "20 PHÚT", "sub": "QUYẾT ĐỊNH AI NHẬN GIẢI"},
    {"type": "kinetic", "at": 19, "items": [{"text": "NGÔI SAO KHÔNG PHẢI THỨ QUÝ NHẤT", "at": 19, "sm": True},
                                           {"text": "NHỮNG GIÂY BẠN DỪNG LẠI", "at": [19, "những", 1], "acc": True}]},
    {"type": "broll", "at": 20, "vid": "37478253", "veil": 0.5, "illus": VM,
     "kin": [{"text": "MÁY KHÔNG HIỂU BẠN NHƯ MỘT NGƯỜI BẠN", "at": 20, "sm": True},
             {"text": "BẠN GIỐNG AI · BẠN DỪNG Ở ĐÂU", "at": [20, "nó"], "acc": True}]},
    {"type": "slam", "at": 21, "text": "DỪNG LẠI ĐÚNG CHỖ", "sub": "KHÔNG CẦN GHÉT THUẬT TOÁN"},
    {"type": "question", "at": 22, "text": "Video gần nhất khiến bạn nghĩ\n“sao nó biết mình thích cái này”?"},
    {"type": "broll", "at": 23, "vid": "7339512", "ms": 12, "veil": 0.4, "illus": VM,
     "kin": [{"text": "KỂ Ở PHẦN BÌNH LUẬN", "at": 23, "acc": True}]},
]}


DIGIT_SHORT = 26


def fix_fx(ch: dict) -> None:
    """Dòng chữ ngắn có con số -> fx "rise" (mặc định "scramble" lộn ký tự khi at sát đầu cảnh; retro-2 checklist)."""
    for s in ch["scenes"]:
        if str(s.get("vid", "")) in BANNED:
            raise SystemExit(f"clip {s['vid']} bị loại (factcheck: lộ bảng tin/giao diện app thật)")
        for q in (s.get("items") if s["type"] == "kinetic" else []) + (s.get("kin") or []):
            if "fx" not in q and re.search(r"\d", q["text"]) and len(q["text"]) <= DIGIT_SHORT:
                q["fx"] = "rise"


for _c in CH.values():
    fix_fx(_c)

SPEC = {
    "title": "Thuật Toán Đề Xuất: Vì Sao TikTok Và YouTube Biết Bạn Thích Gì?",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True,
    "beat2": True,   # PM 10/10: QA final (engine cũ) 9 đoạn trống do sync hiện mờ chờ lời -> bật beat2 (pull_main, bố cục, từ nhấn) trước khi đăng
    "acc": ["netflix", "tiktok", "youtube", "đề", "xuất", "thuật", "toán", "sao", "bot", "dừng"],
    "say": SAY, "imgs": IMGS, "chapters": list(CH),
    "youtube": {
        "titles": ["Thuật Toán Đề Xuất: Vì Sao TikTok Và YouTube Biết Bạn Thích Gì?",
                   "AI Đoán Bạn Thích Gì Như Thế Nào? Từ Cuộc Thi 1 Triệu Đô Của Netflix Tới TikTok",
                   "Bạn Chưa Nói Gì, Thuật Toán Đã Đoán: Cách Dạy Lại Bảng Tin TikTok, YouTube"],
        "summary": "Năm 2009, cuộc thi Netflix Prize một triệu đô kết thúc bằng một trận hoà tới chữ số thập phân thứ tư — rồi Netflix "
                   "không đưa bản thắng giải vào chạy thật. Hôm nay TikTok và YouTube hiếm khi hỏi bạn chấm sao, vậy chúng đoán gu bạn "
                   "bằng gì? Lọc cộng tác, thời gian xem thay cho cú nhấp, các tín hiệu TikTok tự công bố, những nghiên cứu độc lập về "
                   "\"hang thỏ\" (bất đồng nhau), thí nghiệm tắt thuật toán trên Facebook/Instagram, và ba việc để dạy lại bảng tin của bạn.",
        "more": ["Số liệu của Netflix, YouTube, TikTok trong video là do chính các hãng tự công bố. Các nghiên cứu \"hang thỏ\" khác nhau về "
                 "năm, cách đo, và phần lớn chỉ xét YouTube ở Mỹ. Menu ứng dụng trong video là mô phỏng dựng bằng chữ theo trang trợ giúp "
                 "(đọc 09/10/2026), giao diện thật có thể khác theo phiên bản. Lời trích được đọc bằng giọng máy của kênh."],
        "ch00_title": "Netflix Prize: 20 phút, một triệu đô",
        "chapter_titles": {"ch00": "Mở đầu: cuộc thi Netflix Prize 1 triệu đô (2009)",
                           "ch01": "Lọc cộng tác: tìm những người giống bạn",
                           "ch02": "Vì sao Netflix không dùng bản thắng giải",
                           "ch03": "YouTube: cú nhấp và thời gian xem",
                           "ch04": "TikTok đoán gu bạn từ đâu?",
                           "ch05": "Lời giải: máy dựa vào điều bạn làm",
                           "ch06": "Hang thỏ: các nghiên cứu nói gì?",
                           "ch07": "Tắt thuật toán đi thì sao?",
                           "ch08": "3 cách dạy lại bảng tin TikTok, YouTube"},
        "sources": [
            "https://arxiv.org/abs/1207.5649",
            "https://www.asc.ohio-state.edu/statistics/statgen/joul_aut2009/NetflixAwardsOneMillionPrize2009.pdf",
            "https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429",
            "https://about.netflix.com/en/news/goodbye-stars-hello-thumbs",
            "https://www.ftc.gov/sites/default/files/documents/closing_letters/netflix-inc./100312netflixletter.pdf",
            "https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/",
            "https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf",
            "https://newsroom.tiktok.com/how-tiktok-recommends-videos-for-you?lang=en",
            "https://newsroom.tiktok.com/fulfilling-commitments-dsa-update?lang=en-150",
            "https://arxiv.org/abs/2201.12271",
            "https://arxiv.org/abs/1908.08313",
            "https://doi.org/10.1126/sciadv.add8080",
            "https://doi.org/10.1073/pnas.2213020120",
            "https://arxiv.org/abs/2308.10398",
            "https://doi.org/10.1126/science.abp9364",
            "https://arxiv.org/abs/2409.18393",
            "https://support.google.com/youtube/answer/6342839?hl=vi",
            "https://support.google.com/youtube/answer/95725?hl=vi",
        ],
        "hashtags": ["ThuatToan", "TikTok", "YouTube", "Netflix", "MindInTheMachine"],
        "tags": ["thuật toán đề xuất", "thuật toán TikTok", "thuật toán YouTube", "vì sao TikTok biết mình thích gì",
                 "Netflix Prize", "lọc cộng tác", "collaborative filtering", "hệ thống đề xuất", "recommendation system",
                 "hang thỏ YouTube", "rabbit hole", "làm mới bảng tin TikTok", "không quan tâm YouTube", "trí tuệ nhân tạo",
                 "bảng tin Đề xuất", "AI"],
        "category": "28", "thumb": "t3.jpg",   # t1/t2 tràn chữ mép phải (PM 09/10) -> retro: chặn tràn trong thumb.py
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels, dùng tự do"],
    },
}

if __name__ == "__main__":
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    pk = OUT / "bgm_picks.json"           # nhạc chốt tay: resolve_bgm dùng picks có sẵn, không tự chọn lại
    old = json.loads(pk.read_text(encoding="utf-8")) if pk.exists() else {}
    if old != BGM_PICKS:
        pk.parent.mkdir(parents=True, exist_ok=True)
        pk.write_text(json.dumps(BGM_PICKS, indent=1), encoding="utf-8")
    print(f"spec + {len(CH)} chương")
