"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM "SIRI ngoài đời thật: Susan Bennett".

    python data/long/mim-siri-susan-bennett/gen_scenes.py   # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md và factcheck.md. Pha 1: chỉ viết file; chưa dựng, chưa tải ảnh/clip (imgs ghi tên File: Commons, giấy phép đã đọc qua
Commons API 23/10/2026, phải đọc lại ở pha 2). Clip Pexels chỉ mới TÌM (pexels.py search), chưa tải: TRƯỚC KHI DỰNG phải chạy
motion/long/clip_sheet.py và loại mọi clip lộ logo / tên hãng / máy có logo táo (đặc biệt clip điện thoại và màn hình phần mềm âm thanh).
KHÔNG logo Apple/Siri, KHÔNG ảnh chụp màn hình iPhone: hai cảnh "chat" là khung kênh tự vẽ, gắn nhãn MÔ PHỎNG.
Lộ trình dạng "tua ngược cuộn băng": timeline năm ở CH00 (hứa), CH04 (đáy 2003), CH05 (tua xuôi); chapter.sub ghi "◀◀ KIM CHỈ NĂM: …";
engine chưa có cảnh cuộn băng riêng (không sửa motion/), nên mô-típ dùng timeline + date lật số + ảnh/clip cuộn băng.
Susan Bennett còn sống: mọi chữ trên màn hình về bà đều ghi "THEO CNN" / "VOA"; Apple chưa xác nhận (ghi ở CH00, CH01, CH06).
Mọi neo [dòng, "từ"] chỉ dùng chữ nằm trong lời đọc; không neo vào chữ số hay chữ có trong bảng "say".
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"siri": "Xi-ri", "susan": "Xu-dần", "bennett": "Ben-nét", "apple": "Áp-pồ", "iphone": "Ai-phôn", "4s": "bốn ét",
       "cupertino": "Cu-pơ-ti-nô", "california": "Ca-li-phoóc-ni-a", "macrumors": "Mác-ru-mơ", "scott": "Xcốt", "forstall": "Pho-xtôn",
       "atlanta": "Át-lan-ta", "cnn": "Xi-en-en", "steve": "Xtiv", "jobs": "Gióp", "=The": "Đờ", "verge": "Vơ-giơ", "ed": "Ét",
       "primeau": "Pri-mô", "scansoft": "Xcan-xóp", "gm": "Gi-em", "voices": "Voi-xịt", "voa": "Vi-ô-ây", "nuance": "Niu-ần",
       "kyoto": "Ki-ô-tô", "andrew": "En-đriu", "hunt": "Hăn", "alan": "A-lần", "black": "Bờ-lách", "darpa": "Đác-pa", "pal": "Pan",
       "calo": "Ca-lô", "sri": "ét-a-ai", "techcrunch": "Téc-crăn", "cameron": "Ca-mơ-rần", "ios": "ai-ô-ét", "taxi": "tắc-xi"}
VM = "ẢNH MINH HỌA"
VV = "VIDEO MINH HỌA"
MOCK = "MÔ PHỎNG CỦA KÊNH · KHÔNG PHẢI GIAO DIỆN THẬT"
SELF = "TỰ TÍNH"
ACC = "#f472b6"
CH = {}

IMGS = {
    "bennett": "File:Susan Bennett VOA D0AD28DF-EAC6-49AB-8FA2-D8DC8B0CB5E0 w1023 n r0 s.jpg",             # Public domain (Voice of America, 09/05/2018)
    "bennettc": "File:Susan Bennett VOA D0AD28DF-EAC6-49AB-8FA2-D8DC8B0CB5E0 w1023 n r0 s (cropped).jpg",  # Public domain (Voice of America, bản cắt dọc)
    "jobs": "File:Steve Jobs with the Apple iPad no logo (cropped).jpg",                                     # CC BY 2.0 (Matt Buchanan, 27/01/2010; bản "no logo")
    "atlanta": "File:Atlanta Skyline from Mableton.jpg",                                                     # CC0 (Brandon Walker)
    "cassette": "File:Noname blank compact cassette, loose tape (1).jpg",                                    # CC BY 2.0 (Tim Reckmann; băng không nhãn hiệu)
    "mic": "File:Close up view of a microphone set up in a recording studio.jpg",                            # CC BY 2.0 (Shixart1985) — pha 2: soi tên hãng trên micro
    "spectro": "File:Spectrogram of I owe you.png",                                                          # Public domain (Jonas.kluk) — ảnh nhỏ 436px, chỉ dùng trong print
}
# Ứng viên clip Pexels (đã TÌM 23/10/2026, CHƯA tải; chạy clip_sheet.py trước khi dựng):
#   35451425 diễn giả trước khán phòng · 6952886 phụ nữ thu âm micro · 6892725 dải âm trên màn hình (soi tên phần mềm)
#   7643472 phụ nữ nói điện thoại (soi logo máy) · 5102361 băng từ rối · 12321388 cuộn băng quay (soi nhãn hiệu)

# ---------------------------------------------------------------- CH00: câu hỏi đầu tiên (cold open)
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "CÂU HỎI ĐẦU TIÊN"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "date", "day": "CUPERTINO · BUỔI RA MẮT IPHONE 4S", "date": "04.10.2011",
     "sub": {"text": "10:00 SÁNG GIỜ CALIFORNIA · THEO GHI CHÉP CỦA MACRUMORS", "at": 2}},
    {"type": "broll", "at": 3, "vid": "8515272", "veil": 0.55, "illus": VV,   # 23/10: đèn sân khấu, không người (không gắn tên người thật lên người lạ)
     "kin": [{"text": "SÂN KHẤU · TRÌNH DIỄN SIRI", "at": 3, "acc": True}, {"text": "câu hỏi đầu tiên", "at": [4, "câu"], "sm": True}]},
    {"type": "chat", "at": 4, "head": "MÔ PHỎNG · CÂU HỎI THỜI TIẾT (THEO MACRUMORS)", "msgs": [
        {"who": "u", "text": "Hôm nay thời tiết thế nào?", "at": 4},
        {"who": "m", "text": "Đây là dự báo cho hôm nay…", "at": [5, "đáp"]}]},
    {"type": "slam", "at": 6, "text": "GIỌNG NỮ", "sub": "TRẢ LỜI TRƯỚC KHÁN PHÒNG · 04.10.2011"},
    {"type": "photo", "at": 7, "img": "atlanta", "tone": "color", "move": "in", "veil": 0.5, "illus": VM,
     "kin": [{"text": "NGOẠI Ô ATLANTA", "at": 7, "acc": True}, {"text": "Susan Bennett · diễn viên lồng tiếng", "at": [7, "diễn"], "sm": True}],
     "label": {"k": "ATLANTA, BANG GEORGIA", "v": "ẢNH: BRANDON WALKER · CC0", "at": 7}},
    {"type": "kinetic", "at": 8, "items": [{"text": "MỘT THƯ ĐIỆN TỬ", "at": 8, "acc": True},
                                           {"text": "từ một đồng nghiệp · theo CNN", "at": [8, "đồng"], "sm": True}]},
    {"type": "quote", "at": 9, "text": "Hey, we've been playing around with this new Apple phone. Isn't this you?",
     "by": "MỘT ĐỒNG NGHIỆP VIẾT CHO SUSAN BENNETT · THEO CNN, 04.10.2013", "lbl": "TRÍCH DỊCH", "qline": 9, "typeAt": [9, "đây"]},
    {"type": "broll", "at": 10, "vid": "6892725", "veil": 0.55, "illus": VV,
     "kin": [{"text": "BÀ MỞ VIDEO GIỚI THIỆU", "at": 10, "acc": True}, {"text": "rồi nghe", "at": [10, "nghe."], "sm": True}]},
    {"type": "print", "at": 11, "img": "bennettc", "tone": "color", "illus": "ẢNH: VOA · 2018 · CÔNG CỘNG",
     "side": {"k": "SUSAN BENNETT", "h": "Diễn viên lồng tiếng\nAtlanta", "lines": [{"text": "Kể với *CNN* · 2013", "at": [11, "kể"]}]}},
    {"type": "quote", "at": 12, "text": "Oh, I knew. It's obviously me. It's my voice.", "by": "SUSAN BENNETT · CNN, 04.10.2013",
     "lbl": "TRÍCH DỊCH", "qline": 12, "typeAt": [12, "rõ"]},
    {"type": "ledger", "at": 13, "title": "AI XÁC NHẬN?", "srcnote": "VOA 09.05.2018 · CNN 04.10.2013",
     "rows": [{"k": "APPLE THUÊ BÀ?", "v": "KHÔNG · THEO LỜI BÀ", "at": 13}, {"k": "THỬ GIỌNG?", "v": "KHÔNG CÓ BUỔI NÀO", "at": [13, "thử"]},
              {"k": "APPLE", "v": "TỪ CHỐI BÌNH LUẬN", "at": 14}]},
    {"type": "question", "at": 15, "text": "Giọng trong chiếc điện thoại ấy,\nthật ra là của ai?"},
    {"type": "timeline", "at": 16, "bg": "cassette", "label": {"k": "CUỘN BĂNG · ◀◀ TUA NGƯỢC", "v": "MỖI CHƯƠNG LÙI MỘT NẤC", "at": 16},
     "items": [{"year": "2011", "text": "*buổi ra mắt*", "at": [17, "năm", 0]},
               {"year": "2005", "text": "*phòng thu*", "at": [17, "thu"]},
               {"year": "2003", "text": "*phòng thí nghiệm*", "at": [17, "nghiệm"], "color": ACC},
               {"year": "▶ HÔM NAY", "text": "rồi *tua xuôi*", "at": [18, "xuôi"]}]},
    {"type": "photo", "at": 19, "img": "cassette", "tone": "color", "move": "in", "veil": 0.55, "illus": VM,
     "kin": [{"text": "Ở CUỐI CUỘN BĂNG", "at": 19, "sm": True}, {"text": "VÌ SAO GIỌNG ẤY GIỐNG NGƯỜI", "at": [19, "giống"], "acc": True}],
     "label": {"k": "CUỘN BĂNG", "v": "ẢNH: TIM RECKMANN · CC BY 2.0", "at": 19}},
]}

# ---------------------------------------------------------------- CH01: nấc thứ nhất, năm 2011 (và bài CNN 2013)
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "NẤC THỨ NHẤT: NĂM 2011"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "NẤC THỨ NHẤT\nNĂM 2011", "sub": "◀◀ KIM CHỈ NĂM: 2011", "bg": "cassette",
     "titleAt": [0, "kim"]},
    {"type": "source", "at": 1, "source": "APPLE NEWSROOM · 04.10.2011", "ref": "THÔNG CÁO RA MẮT IPHONE 4S",
     "snippet": "Siri là [[một trợ lý thông minh, giúp bạn làm việc chỉ bằng cách hỏi]]", "hlAt": [1, "giúp"],
     "seal": "DỊCH TỪ THÔNG CÁO", "sealAt": 2},
    {"type": "ledger", "at": 3, "title": "SIRI BẢN ĐẦU · GẮN NHÃN BETA", "srcnote": "APPLE NEWSROOM · 04.10.2011",
     "rows": [{"k": "TIẾNG ANH", "v": "MỸ · ANH · ÚC", "at": [3, "anh"]}, {"k": "TIẾNG PHÁP", "v": "✓", "at": [3, "pháp"]},
              {"k": "TIẾNG ĐỨC", "v": "✓", "at": [3, "đức"]}],
     "total": {"k": "NHÃN", "v": "THỬ NGHIỆM", "at": [3, "nhãn"]}},
    {"type": "print", "at": 4, "img": "jobs", "tone": "bw", "illus": "ẢNH: MATT BUCHANAN · CC BY 2.0 · 2010",
     "side": {"k": "STEVE JOBS", "h": "Qua đời\n05.10.2011", "lines": [{"text": "Thông cáo của *Hội đồng quản trị* Apple", "at": [4, "hội"]}]}},
    {"type": "date", "at": 5, "day": "CHIẾC ĐIỆN THOẠI CÓ SIRI LÊN KỆ", "date": "14.10.2011",
     "sub": {"text": "MỸ · ÚC · CANADA · PHÁP · ĐỨC · NHẬT · ANH · THEO APPLE", "at": [5, "kệ."]}},
    {"type": "kinetic", "at": 6, "items": [{"text": "GIỮ KÍN", "at": 6, "acc": True},
                                           {"text": "không chắc muốn nổi tiếng", "at": [7, "nổi"], "sm": True},
                                           {"text": "không chắc về mặt pháp lý · theo CNN", "at": [7, "pháp"], "sm": True}]},
    {"type": "counter", "at": 8, "from": 0, "to": 2, "suffix": " NĂM", "until": [8, "năm."], "label": "IM LẶNG · 10.2011 → 10.2013", "tag": SELF,
     "sub": {"text": "TỪ BUỔI RA MẮT TỚI BÀI CỦA CNN", "at": 8}},
    {"type": "kinetic", "at": 9, "items": [{"text": "THE VERGE · 09.2013", "at": 9, "acc": True},
                                           {"text": "một video về cách Siri có giọng nói", "at": [9, "video"], "sm": True}]},
    {"type": "myth", "at": 10, "mythLab": "NHIỀU NGƯỜI TƯỞNG", "myth": "CÔ ẤY LÀ SIRI", "truthLab": "CÔ ẤY LÊN TIẾNG",
     "truth": "TUYỆT ĐỐI KHÔNG PHẢI", "strikeAt": [11, "vội"], "truthAt": [11, "tuyệt"]},
    {"type": "broll", "at": 12, "vid": "7643472", "veil": 0.55, "illus": VV,
     "kin": [{"text": "MỘT PHÓNG VIÊN ĐOÁN RA TRƯỚC", "at": 12, "acc": True},
             {"text": "phỏng vấn về giọng nói ở sân bay Atlanta", "at": [13, "phỏng"], "sm": True}]},
    {"type": "chat", "at": 14, "head": "CUỘC PHỎNG VẤN · THEO CNN · DIỄN Ý", "msgs": [
        {"who": "u", "text": "Bà có phải là Siri không?", "at": 14},
        {"who": "m", "text": "(bà sững người)", "at": [15, "sững"]}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "BÀ CHỦ ĐỘNG LIÊN LẠC LẠI", "at": 16}, {"text": "SẴN SÀNG KỂ", "at": 17, "acc": True}]},
    {"type": "date", "at": 18, "day": "CNN ĐĂNG BÀI CỦA JESSICA RAVITZ", "date": "04.10.2013",
     "sub": {"text": "TRÒN HAI NĂM SAU BUỔI RA MẮT", "at": [18, "tròn"]}},
    {"type": "ledger", "at": 19, "title": "BẰNG CHỨNG · THEO CNN", "srcnote": "CNN · 04.10.2013",
     "rows": [{"k": "APPLE", "v": "TỪ CHỐI BÌNH LUẬN", "at": 20}, {"k": "CHUYÊN GIA", "v": "ED PRIMEAU · 30 NĂM NGHỀ", "at": [21, "chuyên"]},
              {"k": "CÁCH LÀM", "v": "SO TỪNG PHỤ ÂM, ĐẶT CẠNH NHAU", "at": 22}]},
    {"type": "bars", "at": 23, "title": "ĐỘ CHẮC CỦA CHUYÊN GIA · %", "unit": "CNN · 04.10.2013", "max": 100,
     "items": [{"k": "GIỌNG NÓI THƯỜNG", "v": 70, "lbl": "≈ 70", "at": 23},
               {"k": "ĐỌC ĐÚNG CHỮ CỦA SIRI", "v": 100, "lbl": "100", "at": [24, "đọc"], "acc": True}]},
    {"type": "quote", "at": 25, "text": "They are identical – a 100% match.", "by": "ED PRIMEAU · CHUYÊN GIA PHÁP Y ÂM THANH · THEO CNN",
     "lbl": "TRÍCH DỊCH", "qline": 25, "typeAt": [25, "chúng"]},
    {"type": "kinetic", "at": 26, "items": [{"text": "MỘT CHỖ RẤT LẠ", "at": 26, "acc": True},
                                            {"text": "thu từ tám năm trước", "at": [27, "tám"], "sm": True},
                                            {"text": "khi chiếc điện thoại còn chưa ra đời", "at": [27, "chưa"], "sm": True}]},
    {"type": "question", "at": 28, "text": "Năm 2005,\nbà thu âm cho ai?"},
]}

# ---------------------------------------------------------------- CH02: nấc thứ hai, phòng thu năm 2005
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "NẤC THỨ HAI: PHÒNG THU NĂM 2005"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "NẤC THỨ HAI\nPHÒNG THU NĂM 2005", "sub": "◀◀ KIM CHỈ NĂM: 2005", "bg": "mic",
     "titleAt": [0, "tua"]},
    {"type": "ledger", "at": 1, "title": "AI NỐI VỚI AI", "srcnote": "CNN · 04.10.2013",
     "rows": [{"k": "SCANSOFT", "v": "CÔNG TY PHẦN MỀM · TÌM GIỌNG", "at": [1, "tìm"]},
              {"k": "GM VOICES", "v": "ATLANTA · GIỌNG MÁY TỰ ĐÁP", "at": 2},
              {"k": "ĐƯỢC CHỌN", "v": "GIỌNG SUSAN BENNETT", "at": [3, "ưng"]}]},
    {"type": "date", "at": 4, "day": "BÀ BENNETT KÝ HỢP ĐỒNG VỚI SCANSOFT", "date": "06.2005",
     "sub": {"text": "GIỌNG VÀO MỘT KHO DỮ LIỆU ĐỂ DỰNG LỜI NÓI · THEO CNN", "at": 5}},
    {"type": "broll", "at": 6, "vid": "6952886", "veil": 0.55, "illus": VV,
     "kin": [{"text": "THÁNG 7 · NGÀY NÀO CŨNG THU", "at": 6, "acc": True},
             {"text": "bốn tiếng mỗi ngày · buồng thu tại nhà", "at": [6, "bốn"], "sm": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "KHÔNG ĐỌC TRUYỆN", "at": 7}, {"text": "KHÔNG ĐỌC TIN", "at": [7, "tin."]}]},
    {"type": "slam", "at": 8, "text": "CÂU VÔ NGHĨA", "sub": "HÀNG GIỜ LIỀN · THEO CNN VÀ VOA"},
    {"type": "print", "at": 9, "img": "bennettc", "tone": "bw", "illus": "ẢNH: VOA · 2018 · CÔNG CỘNG",
     "side": {"k": "SUSAN BENNETT", "h": "Phỏng vấn VOA\n09.05.2018", "lines": [{"text": "Kể lại *một câu mẫu*", "at": [9, "câu"]}]}},
    {"type": "quote", "at": 10, "text": "cow hoist in the tub today", "by": "CÂU MẪU BÀ BENNETT KỂ VỚI VOA · 09.05.2018",
     "lbl": "TRÍCH DỊCH", "qline": 10, "typeAt": [10, "bò"]},
    {"type": "ledger", "at": 11, "title": "TỪ CÂU VÔ NGHĨA, KỸ SƯ RÚT RA", "srcnote": "CNN · 04.10.2013",
     "rows": [{"k": "1", "v": "NGUYÊN ÂM", "at": [11, "nguyên"]}, {"k": "2", "v": "PHỤ ÂM", "at": [11, "phụ"]},
              {"k": "3", "v": "ÂM TIẾT", "at": [11, "tiết,"]}],
     "total": {"k": "RỒI CHỈNH", "v": "ĐỘ CAO · TỐC ĐỘ", "at": [11, "chỉnh"]}},
    {"type": "kinetic", "at": 12, "items": [{"text": "TRẢ THEO GIỜ", "at": 12, "acc": True},
                                            {"text": "bà đoán: tổng đài điện thoại của các công ty", "at": 13, "sm": True}]},
    {"type": "date", "at": 14, "day": "SCANSOFT MUA LẠI NUANCE · LẤY LUÔN TÊN", "date": "10.2005", "sub": {"text": "THEO CNN", "at": [14, "lấy"]}},
    {"type": "source", "at": 15, "source": "CNN · 04.10.2013", "ref": "NUANCE VÀ SIRI",
     "snippet": "Nuance là công ty [[được nhiều người cho là đã cung cấp cho Apple công nghệ đứng sau Siri]]", "hlAt": [15, "nhiều"],
     "seal": "NUANCE: “KHÔNG BÌNH LUẬN VỀ APPLE”", "sealAt": [16, "không"]},
    {"type": "photo", "at": 17, "img": "atlanta", "tone": "bw", "move": "out", "veil": 0.55, "illus": VM,
     "kin": [{"text": "NHỮNG NĂM 1970", "at": [18, "những"], "acc": True}, {"text": "một buổi hát nhạc quảng cáo", "at": [18, "hát"], "sm": True}],
     "label": {"k": "ATLANTA", "v": "ẢNH: BRANDON WALKER · CC0", "at": 17}},
    {"type": "kinetic", "at": 19, "items": [{"text": "NGƯỜI LỒNG TIẾNG KHÔNG ĐẾN", "at": 19, "acc": True},
                                            {"text": "“không có giọng địa phương, đọc thử đi” · theo CNN", "at": 20, "sm": True}]},
    {"type": "slam", "at": 21, "text": "MÁY RÚT TIỀN", "sub": "GIỌNG QUẢNG CÁO TRÊN ĐÀI VÀ TIVI · THEO CNN"},
    {"type": "quote", "at": 22, "text": "I began my career as a machine many years ago.", "by": "SUSAN BENNETT · CNN, 04.10.2013",
     "lbl": "TRÍCH DỊCH", "qline": 22, "typeAt": [22, "tôi"]},
    {"type": "question", "at": 23, "text": "Một kho câu vô nghĩa,\nlàm sao thành câu có nghĩa?"},
    {"type": "photo", "at": 24, "img": "cassette", "tone": "color", "move": "in", "veil": 0.5, "illus": VM,
     "kin": [{"text": "KÉO CUỘN BĂNG RA KHỎI VỎ", "at": 24, "acc": True}],
     "label": {"k": "CUỘN BĂNG", "v": "ẢNH: TIM RECKMANN · CC BY 2.0", "at": 24}},
]}

# ---------------------------------------------------------------- CH03: kéo cuộn băng ra, những mảnh âm (re-hook ở cuối)
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "KÉO CUỘN BĂNG RA: NHỮNG MẢNH ÂM"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "KÉO CUỘN BĂNG RA\nNHỮNG MẢNH ÂM", "sub": "TỔNG HỢP GHÉP ĐƠN VỊ", "bg": "cassette",
     "titleAt": [0, "hãy"]},
    {"type": "broll", "at": 1, "vid": "5102361", "veil": 0.55, "illus": VV,
     "kin": [{"text": "MỘT DẢI BĂNG RẤT DÀI", "at": 1, "sm": True}, {"text": "CẮT THÀNH RẤT NHIỀU MẢNH", "at": [1, "cắt"], "acc": True}]},
    {"type": "units", "at": 2, "title": "MỖI MẢNH: NGẮN HƠN MỘT ÂM TIẾT · CÓ KHI CHỈ NỬA ÂM", "total": 12, "cols": 12, "lit": 12,
     "litAt": [2, "nửa"], "unitLabel": "MẢNH · MINH HỌA"},
    {"type": "ledger", "at": 3, "title": "NHÃN DÁN TRÊN MỖI MẢNH", "srcnote": "HUNT & BLACK 1996 · APPLE ML JOURNAL 2017",
     "rows": [{"k": "1", "v": "ÂM GÌ", "at": 3}, {"k": "2", "v": "CAO HAY THẤP", "at": [3, "cao"]}, {"k": "3", "v": "ĐỨNG CẠNH ÂM NÀO", "at": [3, "cạnh"]}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "MUỐN NÓI CÂU MỚI", "at": 4, "sm": True}, {"text": "MÁY ĐI LỤC KHO", "at": [4, "lục"], "acc": True}]},
    {"type": "slam", "at": 5, "text": "GHÉP ĐƠN VỊ", "sub": "UNIT SELECTION · TỔNG HỢP TIẾNG NÓI BẰNG CÁCH GHÉP"},
    {"type": "source", "at": 6, "source": "ICASSP-96 · ATR, KYOTO · 1996 · TR. 373", "ref": "HUNT & BLACK · “UNIT SELECTION…”",
     "snippet": "chọn và ghép các đơn vị từ [[một kho tiếng nói lớn của một người đọc]]", "hlAt": [6, "mô"],
     "seal": "ĐÃ ĐỌC BÀI GỐC", "sealAt": 7},
    {"type": "ledger", "at": 8, "title": "HAI CÁI GIÁ", "srcnote": "HUNT & BLACK 1996 · “TARGET COST” / “CONCATENATION COST”",
     "rows": [{"k": "GIÁ 1", "v": "GIỐNG ÂM CẦN NÓI ĐẾN ĐÂU", "at": 8}, {"k": "GIÁ 2", "v": "NỐI CÓ ÊM · CÓ LỘ VẾT CẮT?", "at": 9}],
     "total": {"k": "MÁY CHỌN", "v": "ĐƯỜNG TỔNG GIÁ THẤP NHẤT", "at": [10, "thấp"]}},
    {"type": "timeline", "at": 11, "bg": "spectro", "label": {"k": "MINH HỌA CỦA KÊNH", "v": "KHÔNG PHẢI DỮ LIỆU THẬT", "at": 11},
     "items": [{"year": "BUỔI SÁNG", "text": "*phần đầu* · câu A", "at": [12, "đầu"]},
               {"year": "LÚC TRƯA", "text": "*phần giữa* · câu B", "at": [13, "giữa"]},
               {"year": "CHIỀU MUỘN", "text": "*phần cuối* · câu C", "at": [14, "cuối"], "color": ACC}]},
    {"type": "slam", "at": 15, "text": "MỘT CHỮ LIỀN MẠCH", "sub": "GHÉP TỪ BA CÂU KHÁC NHAU · MINH HỌA"},
    {"type": "print", "at": 16, "img": "spectro", "tone": "color", "illus": "ẢNH MINH HỌA · PHỔ ÂM CÂU “I OWE YOU” (CÔNG CỘNG)",
     "side": {"k": "HUNT & BLACK · 1996", "h": "Kho càng lớn\nlời càng tự nhiên", "lines": [{"text": "đủ *cao độ*, đủ *âm sắc*", "at": [16, "cao"]}]}},
    {"type": "kinetic", "at": 17, "items": [{"text": "CẦN RẤT NHIỀU GIỜ THU", "at": 17, "acc": True},
                                            {"text": "câu chưa từng đọc vẫn nói được", "at": 18, "sm": True}]},
    {"type": "photo", "at": 19, "img": "mic", "tone": "color", "move": "in", "veil": 0.55, "illus": VM,
     "kin": [{"text": "BỐN TIẾNG LIỀN", "at": 19, "sm": True}, {"text": "RẤT DỄ CHÁN", "at": [20, "chán"], "acc": True}],
     "label": {"k": "MICRO TRONG PHÒNG THU", "v": "ẢNH: SHIXART1985 · CC BY 2.0", "at": 19}},
    {"type": "quote", "at": 21, "dy": True, "text": "Đôi khi Siri nghe hơi có thái độ: những âm ấy có thể được thu trong mười lăm phút cuối của bốn tiếng.",
     "by": "SUSAN BENNETT KỂ VỚI CNN · 2013", "lbl": "DIỄN Ý", "typeAt": [21, None, 0, 0.05], "typeDur": 3.0},
    {"type": "kinetic", "at": 22, "items": [{"text": "MỖI MẢNH ÂM", "at": 22, "sm": True},
                                            {"text": "MỘT KHOẢNH KHẮC THẬT", "at": [22, "khoảnh"], "acc": True}]},
    {"type": "slam", "at": 23, "text": "NHỮNG CÂU CHƯA TỪNG NÓI", "sub": "GIỜ THÌ BẠN ĐÃ HIỂU VÌ SAO"},
    {"type": "kinetic", "at": 24, "items": [{"text": "GIỌNG NÓI = CÁI MIỆNG", "at": [24, "miệng."], "acc": True}]},
    {"type": "question", "at": 25, "text": "Còn cái đầu:\nai dạy chiếc máy hiểu câu bạn hỏi?"},
]}

# ---------------------------------------------------------------- CH04: đáy cuộn băng, phòng thí nghiệm năm 2003
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "ĐÁY CUỘN BĂNG: PHÒNG THÍ NGHIỆM NĂM 2003"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "ĐÁY CUỘN BĂNG\nPHÒNG THÍ NGHIỆM 2003", "sub": "◀◀ KIM CHỈ NĂM: 2003", "bg": "cassette",
     "titleAt": [0, "kim"]},
    {"type": "timeline", "at": 1, "label": {"k": "CUỘN BĂNG", "v": "◀◀ CHẠM ĐÁY", "at": 1},
     "items": [{"year": "2011", "text": "*ra mắt*", "at": 1}, {"year": "2005", "text": "*phòng thu*", "at": [1, "là"]},
               {"year": "2003", "text": "*đáy cuộn băng*", "at": [1, "đáy"], "color": ACC}]},
    {"type": "ledger", "at": 2, "title": "AI · Ở ĐÂU", "srcnote": "DARPA · SRI INTERNATIONAL",
     "rows": [{"k": "DARPA", "v": "CƠ QUAN NGHIÊN CỨU QUỐC PHÒNG MỸ", "at": 2},
              {"k": "PAL", "v": "TRỢ LÝ CÁ NHÂN BIẾT HỌC", "at": [2, "trợ"]},
              {"k": "CALO", "v": "DỰ ÁN DO SRI DẪN DẮT", "at": [3, "dự"]}]},
    {"type": "counter", "at": 4, "from": 0, "to": 5, "suffix": " NĂM", "until": [4, "bắt"], "label": "DỰ ÁN CALO · BẮT ĐẦU TỪ 2003",
     "sub": {"text": "THEO SRI", "at": 4}},
    {"type": "kinetic", "at": 5, "items": [{"text": "HƠN 300 NHÀ NGHIÊN CỨU", "at": 5, "acc": True},
                                           {"text": "từ 22 viện và trường · theo SRI", "at": [5, "viện"], "sm": True}]},
    {"type": "chat", "at": 7, "head": "TRANG CỦA SRI HÌNH DUNG · TRÍCH DỊCH", "msgs": [
        {"who": "u", "text": "Này CALO, xếp giúp tôi một phòng họp nhé?", "at": 7}]},
    {"type": "source", "at": 8, "source": "DARPA · INNOVATION TIMELINE", "ref": "PERSONAL ASSISTANT THAT LEARNS (PAL)",
     "snippet": "thành quả của PAL dùng cho quân đội, và [[cho việc trò chuyện bằng giọng nói trên thiết bị cầm tay dân sự]]",
     "hlAt": [9, "trò"], "seal": "DỊCH TỪ TRANG DARPA", "sealAt": [9, "dân"]},
    {"type": "date", "at": 10, "day": "SRI TÁCH RA CÔNG TY SIRI", "date": "2007", "sub": {"text": "THEO DARPA VÀ SRI", "at": [10, "đặt"]}},
    {"type": "kinetic", "at": 11, "items": [{"text": "MỘT CHI TIẾT ĐÁNG ĐỂ Ý", "at": 11, "acc": True},
                                            {"text": "phòng thí nghiệm: phần hiểu câu hỏi, làm việc giúp bạn", "at": 12, "sm": True}]},
    {"type": "myth", "at": 13, "mythLab": "DỄ NGHĨ", "myth": "GIỌNG CŨNG TỪ ĐÂY", "truthLab": "THEO CNN", "truth": "SCANSOFT → NUANCE",
     "strikeAt": [13, "không"], "truthAt": [14, "đường"]},
    {"type": "ledger", "at": 15, "title": "HAI SỢI BĂNG", "srcnote": "SRI · DARPA · CNN",
     "rows": [{"k": "SỢI 1", "v": "CÁI ĐẦU · PHÒNG THÍ NGHIỆM", "at": 16}, {"k": "SỢI 2", "v": "GIỌNG NÓI · BUỒNG THU Ở ATLANTA", "at": 17}]},
    {"type": "slam", "at": 18, "text": "ĐÁY CUỘN BĂNG", "sub": "▶ GIỜ TUA XUÔI", "white": True},
    {"type": "broll", "at": 19, "vid": "11124043", "veil": 0.55, "illus": VV,
     "kin": [{"text": "▶ TUA XUÔI", "at": 19, "acc": True}, {"text": "hai sợi gặp nhau thế nào?", "at": [19, "gặp"], "sm": True}]},
]}

# ---------------------------------------------------------------- CH05: tua xuôi 2007 → 2013 (cảnh mạnh ~75%)
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "TUA XUÔI: TỪ 2007 TỚI 2013"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "TUA XUÔI\nTỪ 2007 TỚI 2013", "sub": "▶ KIM CHỈ NĂM CHẠY XUÔI", "bg": "cassette",
     "titleAt": [0, "kim"]},
    {"type": "counter", "at": 1, "from": 0, "to": 24, "suffix": " TRIỆU USD", "until": [1, "vòng"], "label": "CÔNG TY SIRI GỌI VỐN · HAI VÒNG",
     "sub": {"text": "THEO SRI", "at": 1}},
    {"type": "date", "at": 2, "day": "ỨNG DỤNG SIRI LÊN KHO ỨNG DỤNG IPHONE", "date": "04.02.2010",
     "sub": {"text": "THEO TECHCRUNCH · KHUYÊN DÙNG CHO IPHONE 3GS", "at": [2, "kho"]}},
    {"type": "chat", "at": 3, "head": "MÔ PHỎNG · ỨNG DỤNG NĂM 2010 LÀM ĐƯỢC GÌ (THEO TECHCRUNCH)", "msgs": [
        {"who": "u", "text": "Tìm một nhà hàng Pháp gần đây", "at": 3},
        {"who": "u", "text": "Đặt bàn", "at": [3, "đặt"]},
        {"who": "u", "text": "Gọi taxi", "at": [3, "gọi"]}]},
    {"type": "date", "at": 4, "day": "APPLE MUA LẠI CÔNG TY SIRI", "date": "04.2010", "sub": {"text": "CHƯA ĐẦY BA THÁNG SAU · THEO SRI", "at": [4, "mua"]}},
    {"type": "timeline", "at": 5, "bg": "mic", "label": {"k": "CUỘN BĂNG", "v": "▶ TUA XUÔI", "at": 5},
     "items": [{"year": "2007", "text": "*công ty Siri*", "at": 5}, {"year": "2010", "text": "*ứng dụng · Apple mua*", "at": [5, "buổi"]},
               {"year": "2011", "text": "*đúng chỗ ta bắt đầu*", "at": 6, "color": ACC}]},
    {"type": "print", "at": 7, "img": "bennettc", "tone": "color", "illus": "ẢNH: VOA · 2018 · CÔNG CỘNG",
     "side": {"k": "SUSAN BENNETT", "h": "Chưa có\nchiếc điện thoại đó", "lines": [{"text": "Con trai: *Cameron* · theo CNN", "at": [8, "con"]}]}},
    {"type": "kinetic", "at": 9, "items": [{"text": "GIỌNG MẸ CẤT LÊN", "at": [9, "giọng"], "acc": True},
                                           {"text": "từ phần chỉ đường", "at": [9, "chỉ"], "sm": True}]},
    {"type": "slam", "at": 10, "text": "“MẸ, THÔI ĐI!”", "sub": "CAMERON BENNETT · THEO CNN"},
    {"type": "kinetic", "at": 11, "items": [{"text": "LẦN ĐẦU NÓI CHUYỆN VỚI CHÍNH MÌNH", "at": [11, "lần"], "acc": True},
                                            {"text": "hơi hoảng · theo CNN", "at": [11, "hoảng."], "sm": True}]},
    {"type": "quote", "at": 13, "dy": True, "text": "Choáng ngợp vì được góp phần vào một kỳ công công nghệ.", "by": "SUSAN BENNETT · THEO CNN, 2013",
     "lbl": "DIỄN Ý", "typeAt": [13, None, 0, 0.05], "typeDur": 2.0},
    {"type": "kinetic", "at": 14, "items": [{"text": "CHƯA BAO GIỜ QUÁT SIRI", "at": [14, "quát"], "acc": True}]},
    {"type": "quote", "at": 15, "text": "But I never yell at her – very bad karma.", "by": "SUSAN BENNETT · CNN, 04.10.2013",
     "lbl": "TRÍCH DỊCH", "qline": 15, "typeAt": [15, "nghiệp"]},
    {"type": "kinetic", "at": 16, "items": [{"text": "MỖI NGÀY BỊ CHỬI BAO NHIÊU LẦN?", "at": [16, "chửi"], "acc": True},
                                            {"text": "lời bà đùa · diễn ý theo CNN", "at": 16, "sm": True}]},
    {"type": "source", "at": 17, "source": "APPLE NEWSROOM · 10.06.2013", "ref": "APPLE GIỚI THIỆU IOS 7",
     "snippet": "Siri [[có giọng nam và giọng nữ mới]]", "hlAt": [18, "giọng"], "seal": "DỊCH TỪ THÔNG CÁO", "sealAt": [18, "mới."]},
    {"type": "ledger", "at": 19, "title": "THỜI CỦA MỘT GIỌNG NÓI", "srcnote": "CNN · 04.10.2013",
     "rows": [{"k": "2011", "v": "GIỌNG SIRI Ở MỸ · THEO CNN", "at": 19}, {"k": "IOS 7", "v": "GIỌNG MỚI · DẦN KHÉP LẠI", "at": [19, "khép"]},
              {"k": "BÀ BENNETT", "v": "HƠI TIẾC · QUEN CÔNG NGHỆ ĐỔI", "at": 20}]},
    {"type": "question", "at": 21, "text": "Giọng mới được làm thế nào,\nvà vì sao nghe giống người hơn?"},
]}

# ---------------------------------------------------------------- CH06: cuối cuộn băng, vì sao giống người
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "CUỐI CUỘN BĂNG: VÌ SAO GIỐNG NGƯỜI"}, "bgm": {"mood": "calm", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "CUỐI CUỘN BĂNG\nVÌ SAO GIỐNG NGƯỜI", "sub": "▶ KIM CHỈ NĂM: 2017", "bg": "mic",
     "titleAt": [0, "kim"]},
    {"type": "source", "at": 1, "source": "APPLE MACHINE LEARNING JOURNAL · 08.2017", "ref": "“DEEP LEARNING FOR SIRI’S VOICE”",
     "snippet": "từ iOS 10, [[giọng Siri dựa trên học sâu]]", "hlAt": [2, "dựa"], "seal": "ĐÃ ĐỌC BÀI GỐC", "sealAt": [2, "sâu."]},
    {"type": "kinetic", "at": 3, "items": [{"text": "NỀN MÓNG VẪN LÀ", "at": 3, "sm": True}, {"text": "CẮT VÀ GHÉP", "at": [3, "cắt"], "acc": True}]},
    {"type": "ledger", "at": 4, "title": "MỘT GIỌNG SIRI CẦN GÌ", "srcnote": "APPLE ML JOURNAL · 08.2017",
     "rows": [{"k": "THU ÂM", "v": "10–20 GIỜ · PHÒNG THU CHUẨN", "at": 4},
              {"k": "KỊCH BẢN", "v": "SÁCH NÓI · CHỈ ĐƯỜNG · CÂU ĐÙA", "at": 5},
              {"k": "IOS 11", "v": "GIỌNG NỮ MỚI · HƠN 20 GIỜ", "at": [6, "giọng"]}]},
    {"type": "broll", "at": 7, "vid": "6892725", "ms": 12, "veil": 0.6, "illus": VV,
     "kin": [{"text": "THỨ THAY ĐỔI", "at": 7, "sm": True}, {"text": "CÁCH CHỌN MẢNH", "at": [7, "chọn"], "acc": True}]},
    {"type": "ledger", "at": 8, "title": "MẠNG NƠ-RON ĐOÁN HAI CÁI GIÁ", "srcnote": "APPLE ML JOURNAL 2017 · “DEEP MIXTURE DENSITY NETWORK”",
     "rows": [{"k": "GIÁ 1", "v": "HỢP VỚI ÂM CẦN NÓI", "at": [8, "hợp"]}, {"k": "GIÁ 2", "v": "NỐI VÀO CHO ÊM", "at": [8, "nối"]}],
     "total": {"k": "VẪN LÀ", "v": "HAI CÁI GIÁ CỦA NĂM 1996", "at": 9}},
    {"type": "kinetic", "at": 10, "items": [{"text": "NGHE THỬ TỪNG CẶP", "at": 10, "sm": True},
                                            {"text": "NGƯỜI NGHE THÍCH GIỌNG MỚI", "at": [10, "thích"], "acc": True}]},
    {"type": "question", "at": 11, "text": "Lý do giọng ấy\ngiống người là gì?"},
    {"type": "slam", "at": 12, "text": "VÌ NÓ VỐN LÀ NGƯỜI", "sub": "Ở CUỐI CUỘN BĂNG", "white": True},
    {"type": "photo", "at": 13, "img": "mic", "tone": "bw", "move": "out", "veil": 0.55, "illus": VM,
     "kin": [{"text": "MỖI MẢNH ÂM", "at": 13, "sm": True}, {"text": "TỪNG DO MỘT NGƯỜI THẬT NÓI RA", "at": [13, "người"], "acc": True}],
     "label": {"k": "MICRO TRONG PHÒNG THU", "v": "ẢNH: SHIXART1985 · CC BY 2.0", "at": 13}},
    {"type": "kinetic", "at": 14, "items": [{"text": "MÁY KHÔNG NGHĨ RA GIỌNG", "at": 14},
                                            {"text": "CHỈ HỌC CHỌN VÀ GHÉP", "at": 15, "acc": True}]},
    {"type": "slam", "at": 16, "text": "GIỌNG BẠN ĐANG NGHE", "sub": "CŨNG LÀ GIỌNG TỔNG HỢP · DO MÁY TẠO RA"},
    {"type": "kinetic", "at": 17, "items": [{"text": "XEM THÊM: VIDEO VỀ GIỌNG NÓI AI", "at": [17, "kể"], "acc": True}]},
    {"type": "photo", "at": 18, "img": "bennett", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "MỘT DỰ ĐOÁN · 2013", "at": [18, "dự"], "acc": True}],
     "label": {"k": "SUSAN BENNETT", "v": "ẢNH: VOA · 2018 · CÔNG CỘNG", "at": 18}},
    {"type": "quote", "at": 19, "text": "I really see a time when you'll probably be able to put your own voice on your phone and have your own voice talk back to you.",
     "by": "SUSAN BENNETT · CNN, 04.10.2013", "lbl": "TRÍCH DỊCH", "qline": 19, "typeAt": [19, "tôi"]},
    {"type": "quote", "at": 20, "text": "Which I'm used to, but maybe you aren't.", "by": "SUSAN BENNETT · CNN, 04.10.2013",
     "lbl": "TRÍCH DỊCH", "qline": 20, "typeAt": [20, "tôi"]},
    {"type": "question", "at": 21, "text": "Giọng trong chiếc điện thoại năm ấy\nlà của ai?"},
    {"type": "ledger", "at": 22, "title": "CÂU TRẢ LỜI Ở CUỐI CUỘN BĂNG", "srcnote": "THEO BẰNG CHỨNG CNN GOM ĐƯỢC · APPLE KHÔNG BÌNH LUẬN",
     "rows": [{"k": "GIỌNG", "v": "MỘT NGƯỜI THẬT", "at": [22, "người"]}, {"k": "MÁY", "v": "CẮT THÀNH MẢNH · GHÉP THÀNH CÂU", "at": [22, "cắt"]}],
     "total": {"k": "NHỮNG CÂU", "v": "BÀ CHƯA TỪNG NÓI", "at": [22, "chưa"]}},
    {"type": "question", "at": 23, "text": "Thu giọng cho một cỗ máy,\nkhông biết nó sẽ nói gì: bạn có nhận?"},
    {"type": "kinetic", "at": 24, "items": [{"text": "VIẾT CHO MÌNH", "at": 24}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [24, "phần"], "acc": True}]},
]}

TITLES = ["SIRI Ngoài Đời Thật: Susan Bennett, Người Nói Mình Là Giọng Siri",
          "SIRI Ngoài Đời Thật: Người Phụ Nữ Nghe Thấy Giọng Mình Trong iPhone Mà Không Hề Biết Trước",
          "SIRI Ngoài Đời Thật: Susan Bennett Và Một Tháng Đọc Những Câu Vô Nghĩa Cho Một Cỗ Máy"]

SPEC = {
    "title": TITLES[0],
    "channel": "MIM", "theme": "lab", "accent": ACC, "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["giọng", "mảnh", "băng", "ghép", "người", "nấc", "cắt", "thật"],
    "say": SAY, "imgs": IMGS, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": TITLES,
        "summary": "Ngày 04/10/2011, Apple ra mắt iPhone 4S cùng trợ lý biết nói SIRI, và ở ngoại ô Atlanta, nữ diễn viên lồng tiếng Susan Bennett "
                   "nghe thấy giọng mình trong đó. Theo bài phỏng vấn của CNN năm 2013, bà thu âm từ tháng 7/2005 cho công ty ScanSoft, đọc hàng giờ những câu "
                   "vô nghĩa, và không hề biết chúng sẽ thành giọng Siri; Apple chưa từng công khai xác nhận. Video tua ngược cuộn băng: 2011, phòng thu 2005, phòng thí nghiệm "
                   "SRI năm 2003, rồi tua xuôi tới bài viết năm 2017 của Apple về giọng Siri, để thấy vì sao một giọng ghép từ hàng nghìn mảnh lại nghe giống người.",
        "more": ["Mọi điều về bà Susan Bennett trong video đều dựa trên lời bà kể, chủ yếu qua một bài của CNN (04/10/2013) và một bài của VOA (09/05/2018). "
                 "Apple chưa từng công khai xác nhận bà là giọng Siri; khi CNN hỏi, Apple từ chối bình luận, còn Nuance nói không bình luận về Apple. "
                 "Kết luận \"khớp 100%\" là của một chuyên gia pháp y âm thanh do CNN thuê. Giờ bắt đầu buổi ra mắt và câu hỏi thời tiết lấy từ ghi chép trực tiếp "
                 "của MacRumors; ngày ứng dụng Siri lên kho ứng dụng lấy từ TechCrunch. Ví dụ ghép ba mảnh âm ở chương ba là hình minh họa của kênh. "
                 "Giọng đọc của video này là giọng tổng hợp."],
        "chapter_titles": {"ch00": "Mở đầu: câu hỏi đầu tiên", "ch01": "Nấc thứ nhất: năm 2011", "ch02": "Nấc thứ hai: phòng thu năm 2005",
                           "ch03": "Kéo cuộn băng ra: những mảnh âm", "ch04": "Đáy cuộn băng: phòng thí nghiệm năm 2003",
                           "ch05": "Tua xuôi: từ 2007 tới 2013", "ch06": "Cuối cuộn băng: vì sao giống người"},
        "sources": [
            "https://edition.cnn.com/2013/10/04/tech/mobile/bennett-siri-iphone-voice/index.html",
            "https://www.voanews.com/a/siri-susan-bennett-iphone/4387109.html",
            "https://www.apple.com/newsroom/2011/10/04Apple-Launches-iPhone-4S-iOS-5-iCloud/",
            "https://www.apple.com/newsroom/2011/10/05Statement-by-Apples-Board-of-Directors/",
            "https://www.apple.com/newsroom/2013/06/10Apple-Unveils-iOS-7/",
            "https://machinelearning.apple.com/research/siri-voices",
            "https://www.ee.columbia.edu/~dpwe/e6820/papers/HuntB96-speechsynth.pdf",
            "https://www.sri.com/case-studies/siri/",
            "https://www.sri.com/75-years-of-innovation/75-years-of-innovation-calo-cognitive-assistant-that-learns-and-organizes/",
            "https://www.darpa.mil/about/innovation-timeline/personal-assistant-that-learns",
            "https://techcrunch.com/2010/02/04/siri-iphone-personal-assistant/",
            "https://www.macrumors.com/2011/10/04/live-coverage-of-apples-lets-talk-iphone-event/",
            "https://www.iclarified.com/entry/index.php?enid=9134",
        ],
        "hashtags": ["Siri", "SusanBennett", "GiọngNóiNhânTạo", "CôngNghệQuanhTa", "MindInTheMachine"],
        "tags": ["siri", "susan bennett", "giọng siri", "giọng nói siri là ai", "tổng hợp tiếng nói", "text to speech", "iphone 4s",
                 "lịch sử siri", "trợ lý ảo", "công nghệ quanh ta", "lịch sử công nghệ"],
        "category": "28", "thumb": "t1.jpg", "playlist": "Công Nghệ Quanh Ta", "publish_at": "2026-11-22T13:00:00Z",
        "video_credits": ["Ảnh Susan Bennett: Voice of America (phạm vi công cộng)",
                          "Ảnh Steve Jobs: Matt Buchanan, CC BY 2.0",
                          "Ảnh cuộn băng: Tim Reckmann, CC BY 2.0; ảnh micro: Shixart1985, CC BY 2.0; ảnh Atlanta: Brandon Walker, CC0; ảnh phổ âm: Jonas.kluk (phạm vi công cộng)",
                          "Video minh họa: Pexels"],
    },
    "sources_internal": "factcheck.md (mã nguồn CNN, VOA, AN11, AN11B, AN13, AML, HB96, SRI1, SRI2, DARPA, TC, MR, ICL). Clip Pexels: chạy clip_sheet.py trước khi dựng.",
}


def _norm(w):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w.lower()))


def _anchors(o, path=""):
    """Duyệt mọi mốc dạng int / [dòng, từ, n, lệch] để kiểm tra. Khoá nhận mốc: at, *At, until, hlAt..."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("at", "until", "titleAt", "hlAt", "sealAt", "typeAt", "qline") or k.endswith("At"):
                yield (path + "/" + k, v)
            else:
                yield from _anchors(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _anchors(v, path + f"[{i}]")


def check():
    """Kiểm neo với lines (sau script_lines.py): lỗi nếu dòng không có, hoặc từ neo không nằm trong dòng, hoặc từ neo nằm trong SAY / là chữ số."""
    bad = []
    say = {k.lstrip("=").lower() for k in SAY}
    for name, c in CH.items():
        f = D / f"{name}.json"
        if not f.exists():
            bad.append(f"{name}: chưa có {f.name} (chạy script_lines.py trước)")
            continue
        lines = json.loads(f.read_text(encoding="utf-8"))["lines"]
        text = [(x if isinstance(x, str) else x["t"]) for x in lines]
        for si, s in enumerate(c["scenes"]):
            for p, v in _anchors(s):
                if isinstance(v, bool) or not isinstance(v, (int, list)):
                    continue
                cands = v if (isinstance(v, list) and v and isinstance(v[0], list)) else [v]
                for a in cands:
                    i = a if isinstance(a, int) else (a[0] if a else None)
                    if not isinstance(i, int) or isinstance(i, bool) or not (0 <= i < len(text)):
                        bad.append(f"{name} cảnh {si} {p}: dòng {a!r} ngoài phạm vi 0..{len(text) - 1}")
                        continue
                    if isinstance(a, list) and len(a) > 1 and isinstance(a[1], str):
                        w = _norm(a[1])
                        if w in say or w.isdigit():
                            bad.append(f"{name} cảnh {si} {p}: chữ neo {a[1]!r} nằm trong SAY hoặc là chữ số")
                        toks = [_norm(t) for t in text[i].split()]
                        n = a[2] if len(a) > 2 else 0
                        if toks.count(w) <= n:
                            bad.append(f"{name} cảnh {si} {p}: dòng {i} không có chữ {a[1]!r} (lần {n}): {text[i]}")
    return bad


def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương")
    bad = check()
    if bad:
        print("NEO LỖI:\n  " + "\n  ".join(bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
