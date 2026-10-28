# MIM Long 20–30 phút: "Dịch máy: lời hứa 'vài năm nữa' từ 1954 tới Google Dịch" (`mim-dich-may`) — hồ sơ nghiên cứu

Người lập: subagent T2, 20/10/2026. Pha 1: chỉ viết file (không dựng, không đăng, không sửa `state.sqlite`). Hẹn đăng dự kiến: T2 07/12/2026 20:00 VN, riêng tư + hẹn giờ. Đầu ra: `data/long/mim-dich-may/{script.md, factcheck.md, ch00..ch11.json, gen_scenes.py, spec.json}`.

## 1. Góc và hình thức

- Cold open: 07/01/1954, cô nhân viên không biết tiếng Nga gõ câu đầu tiên vào IBM 701; báo đưa tin "vài năm nữa".
- Lộ trình dạng **"cuốn sổ lời hứa"**: mỗi lần có người hứa (hoặc can) về dịch máy, ghi một dòng; CH11 tất toán. Không dùng "trả lời ba câu hỏi"; khác các hình thức đã dùng ở MIM #1–#12.
- Mô-típ lặp: cuốn sổ, toà tháp của Weaver (CH02 → CH09 → CH11), cái cũi "pen" của Bar-Hillel (CH04 → CH08 → CH10 → CH11), cặp "not ↔ ne … pas" (CH07 → CH09).
- Re-hook ~45% = CH07 (IBM 1990 dịch hỏng hơn một nửa nhưng vẫn là cái mốc). Cảnh mạnh ~75% = CH09 (máy học nhìn lại; Google tự thú lỗi).

## 2. Độ dài

| Cách đo | Kết quả |
|---|---|
| Chữ (tách theo khoảng trắng, `script_lines.py`) | **4.466 chữ**, 265 câu, 12 chương |
| Ticket (~150 chữ/phút) | **29,8 phút** |
| Đo thật ở ba Long 20–30 phút đã dựng (Watson, Máy chơi game, AlphaGo): 213–217 chữ/phút gồm nghỉ | **~20,8 phút** |

Hai thước chênh nhau vì mốc 150 chữ/phút của ticket thấp hơn tốc độ thật của giọng hiện dùng. 4.466 chữ nằm trong 20–30 phút ở cả hai thước, nhưng sát đáy theo tốc độ thật. **Cần kiểm sau TTS (pha 2):** nếu `build_long.py tts` cho tổng < 20:30 thì không độn; bổ sung bằng một chương thật (gợi ý ở mục 6), không kéo giãn nhịp. Theo từng chương: CH00 ~292 · CH01 ~431 · CH02 ~492 · CH03 ~227 · CH04 ~361 · CH05 ~420 · CH06 ~295 · CH07 ~428 · CH08 ~232 · CH09 ~511 · CH10 ~352 · CH11 ~425.

## 3. Chống trùng

- Short `mim-transformer-2017` (15/10) và Long `mim-ai-70` (CH06) đã kể Transformer qua: "tám nhà nghiên cứu của Google", tên bài "Attention Is All You Need", "nhìn cả câu cùng lúc rồi cân chữ nào chú ý chữ nào", "ba ngày rưỡi trên tám GPU", "nền móng chatbot". CH10 **không dùng** các câu này. Góc riêng: Transformer là **bài thi dịch** (Anh–Đức, Anh–Pháp), bỏ vòng lặp và tích chập, so dữ liệu 117 nghìn cặp (IBM 1990) với 4,5/36 triệu cặp, hình "making … more difficult", cỗ máy có hai nửa (đọc/viết), GPT đầu tiên chỉ giữ nửa viết. Không nêu 3,5 ngày, 8 GPU, tám tác giả, số 41,8.
- Quét từ khoá trong 17 Long và 160 Short MIM (T1): không có dịch máy, Georgetown, Weaver, ALPAC. Không trùng góc với `mim-ai-voice` (giọng nói) hay `mim-ai-hallucinate`.

## 4. Nguồn

Chi tiết từng dòng ở `data/long/mim-dich-may/factcheck.md` (57 dòng, có URL và mục/trang). Đã mở và đọc thật (20/10): Hutchins (slide Georgetown–IBM 1954; ALPAC 1996; Fifty Years; huyền thoại 1995), Weaver 1949, Bar-Hillel 1960, ALPAC 1966 (32.000 chữ), Brown 1990, Google Developers Blog 04/2012, blog Google 04/2016, arXiv 1409.3215, 1409.0473, 1609.08144, 1611.04558, 1706.03762, blog Google Research 09/2016, GPT-1 (OpenAI). Đủ ≥ 6 nguồn sơ cấp.

Sửa so với T1: (a) "Wiener trả lời 'rất sớm'" thực là "very premature" → "quá sớm"; (b) "40 giờ và 1.000 máy" của Google 2006 **không có trong nguồn mở được** → bỏ; (c) bài Google 04/2012 gốc không tải được, số lấy từ Developers Blog cùng tuần; (d) JPRS 16 USD tính theo 1.000 từ **tiếng Anh**, ba giá kia theo từ Nga; (e) Vaswani: phần chữ ghi 41,0 BLEU Anh–Pháp, bảng/abstract ghi 41,8 → không dùng số này.

## 5. Hình (điểm yếu số 1) — trạng thái và rủi ro

**Không có ảnh hay phim buổi trình diễn 1954 có giấy phép rõ.** Không dùng, không dựng lại bằng ảnh giả. Cảnh buổi trình diễn kể bằng thẻ chữ, bảng, trích dẫn và ảnh minh hoạ gắn nhãn. Bản ghi nhớ Weaver (chú "Reproduced by permission of the Rockefeller Foundation Archives") và báo cáo ALPAC: **không chiếu ảnh trang**, chỉ trích ngắn bằng cảnh quote. Không có ảnh giao diện Google Dịch.

Ảnh dự kiến (Wikimedia Commons; `spec.imgs`; giấy phép lấy từ API Commons ngày 20/10; `build_long` tự ghi credit, giữ `.json` cạnh ảnh):

| Khoá | File | Giấy phép | Dùng ở | Nhãn |
|---|---|---|---|---|
| ibm701, ibm701f | IBM 701console.jpg; IBM 701 frame.jpg (Flickr "Dan", chụp hiện vật) | CC BY 2.0; CC BY-SA 2.0 | CH00, CH01 | ẢNH MINH HỌA · MÁY CÙNG LOẠI |
| healy | Georgetown University, Healy Hall & Statue of John Carroll.jpg | Public domain | CH01 (nền thẻ chương) | ẢNH MINH HỌA · HIỆN NAY |
| nuremberg | German War Crimes Trials, NARA 292602.jpg | PD (NARA) | CH01 | không phải ông Dostert |
| weaver | Warren Weaver.jpg (NARA, 1940) | PD | CH02, CH07 | |
| wiener | Norbert Wiener.webp (M.I.T. archives) | CC0 | CH02 | **kiểm lại webp mở được; dự phòng `Norbert Wiener.png` CC0** |
| babel | Bruegel, Tower of Babel (Vienna).jpg | PD | CH02, CH09, CH11 | TRANH MINH HỌA |
| ibm7090 | IBM 7090 computer.jpg (NASA Ames, 1961) | PD | CH05 | máy cùng thời |
| pierce | John Robinson Pierce.jpg | PD (NASA) | CH05 | |
| parliament | West Block, Parliament of Canada (April 2019).jpg | CC BY-SA 4.0 | CH07 | chụp 2019, không phải 1990 |
| gdc | Google Data Center, Council Bluffs Iowa.jpg (Chad Davis) | CC BY 2.0 | CH08 | minh hoạ |
| bengio | Yoshua Bengio 2019 cropped.jpg (Maryse Boyce) | CC BY 4.0 | CH09 | |

Clip Pexels (12 clip, đã tải về `output/long/mim-dich-may/broll/`, **đã chạy `clip_sheet.py`**, tờ soát `output/long/mim-dich-may/qa_clips.jpg`): máy chữ 33068304, máy in báo 38826405, quả địa cầu 6909831 và 7606810, bản đồ-sách-nến 10480415, chữ Scrabble 5651577, từ điển 7918125, thiết bị cũ 8058350, cáp mạng 1085656, ổ cứng 38496190, mạng sáng 35008786, trang sách 13617608. Đã loại hai clip (phố Istanbul: biển hiệu cửa hàng; bản đồ ghim: biển có ký hiệu và mã QR). Các clip còn lại không thấy logo, mã cổ phiếu, tên công ty đọc được. **Còn phải soát lại sau khi chọn khung ms**: clip 8058350 có chữ Hán/Nhật treo và đồ chơi robot (không phải logo, nhưng hợp ý "thiết bị cũ" ở mức lỏng — có thể thay).

**Rủi ro hình, nói thẳng:** (1) ~12 ảnh tĩnh + 12 clip minh hoạ cho 21+ phút; phần lớn thời lượng là thẻ chữ, bảng, số đếm, trích dẫn. Dễ thành "nói trên chữ" nếu nhịp dựng đều → cần soi % ở lại sau khi đăng. (2) Không có chân dung Dostert, Hurd, Bar-Hillel, Brown, Sutskever (không tìm được ảnh có giấy phép rõ; Sutskever có ảnh CC BY ở ai-gpu nhưng đã dùng ở Long khác). (3) Ảnh IBM 701 là hiện vật bảo tàng, không phải 1954 → nhãn minh hoạ bắt buộc. (4) Chưa chạy `research_long.py`/`media_search.py` (ghi vào `output`); ảnh chỉ mới lập danh sách, chưa tải: pha 2 phải tải, soát từng mô tả Commons, rồi mới dựng. (5) Nếu pha 2 xem sheet thấy hình quá nghèo, phương án trong SOURCES.md: thêm ảnh NASA/Smithsonian CC0 (`media_search.py --src smithsonian,nasa`) cho IBM 701/7090; hoặc hoán sang GPS như T1 đề xuất.

## 6. Chỗ cần kiểm và đề xuất bổ sung

1. Ngày 7/1/1954 (xem factcheck "Còn mở" 1). 2. Số Google 04/2012 (bài gốc). 3. Độ dài sau TTS (mục 2). 4. Nhu cầu: vẫn chưa có Studio Research; bài vi.wikipedia "Dịch máy" không tồn tại → tiêu đề cuối nên thử với từ khoá "Google Dịch" và "dịch máy". 5. Lint: `studio_lint.py --strict` 0 lỗi, 4 cảnh báo (CH00, CH03, CH05, CH09 ít câu ngắn). 6. Chưa chạy `build_long.py ... html` (có thể bắt lỗi neo mà bộ kiểm tra riêng của mình — `scratchpad/chk.py`, 0 lỗi — không thấy). 7. Chương dự phòng nếu thiếu thời lượng và có nguồn: lịch sử Systran (cần thêm nguồn), hoặc phỏng vấn/hồi ký của người trong cuộc (chưa có). Không độn.
8. Chủ đề dự phòng nếu hình bị chủ kênh từ chối: GPS (T1 mục 5).

## 7. Giọng và nhạc

Thanh Bình (dẫn), Ngọc Huyền (lời trích `»`). Spec `look: amber` (gợi ý của `variety.py next-look`); nhạc theo mood: mystery, curious, calm, dark, upbeat, warm (picker tự chọn, kiểm `variety.py audit` ở pha 2).
