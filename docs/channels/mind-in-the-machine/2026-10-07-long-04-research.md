# Nghiên cứu video dài #4 — Mind in the Machine (MIM) — 07/10/2026

**Phạm vi:** hồ sơ dữ kiện có nguồn cho video dài thứ tư (16:9, 12–14 phút, tiếng Việt, faceless, giọng TTS Hải Đăng + motion graphics + ảnh
mở, theme "lab"): **"Vì sao AI bịa mà vẫn rất tự tin?"** (ảo giác AI, slug `mim-ai-hallucinate`). Đề tài đã được xếp **#2** ở hồ sơ #3
(`2026-10-07-long-03-research.md` §2.2, 24 điểm) và `2026-10-06-topic-research.md` §3.1 #2. Áp dụng `motion/long/RETENTION.md` (cold open,
**lộ trình đổi hình thức** — #1 "ba câu hỏi", #2 "ba chặng đường", #3 "lời thách" → #4 **"cảnh hẹn trước"**), `RESEARCH-million-views.md`
(3 tựa Test & Compare, chương có từ khoá) và checklist retro 2 (`docs/pm/2026-10-07-retro-2.md`, "Quy trình cho video kế tiếp" bước 1–4).

**Kịch bản đi kèm:** `data/long/mim-ai-hallucinate/script.md` (bản 1, đã qua `script_lines.py`: 9 chương, 167 câu, 0 lỗi integrity; chờ
agent kiểm chứng).

**Phương pháp:**
- Đọc tận gốc bằng curl + `pdftotext` khi mở được: **hồ sơ toà** (CourtListener/RECAP: ECF 31, 54, 55 vụ *Mata v. Avianca*), **bài báo khoa
  học** (arXiv 2509.04664, 2303.08774, 2401.01301; Europe PMC cho *Scientific Reports*), **báo cáo EBU/BBC** (PDF trên ebu.ch), **cơ sở dữ liệu
  Charlotin**. Ảnh chụp màn hình ChatGPT trong Phụ lục B của ECF 54 được trích ảnh bằng `pypdf` và **đọc bằng mắt** (không OCR).
- Trang **chặn script** hôm nay: oecd.org (403), nature.com (chuyển hướng đăng nhập → dùng Europe PMC), finance.gov.au (treo, đã dừng).
- Wikimedia Commons API (`generator=search`, 40 kết quả đầu, đọc `LicenseShortName`), User-Agent `yt-factory-research/1.0
  (https://github.com/nguyent0810/Youtube_Creator_V2)`, giãn ~1 giây. Pexels qua `motion/long/pexels.py search` (khoá đọc từ `.local.env`,
  không in; chỉ tìm, chưa tải).
- **Nhãn dữ kiện:** **[bằng chứng]** = đã đọc tận nguồn gốc hôm nay · **[SECONDARY]** = qua báo/tóm tắt, chưa mở bản gốc · **[CHƯA KIỂM]** =
  chưa đủ tin, không đọc lên. Trích nguyên văn giữ tiếng Anh, kèm nguồn + trang/đoạn. Số `[n]` trỏ tới mục 10.

---

## 1. Tóm tắt

- **Đề tài:** vì sao chatbot viết ra điều sai mà giọng vẫn chắc nịch, và người dùng làm gì. Trục A "AI dễ hiểu" (cơ chế đoán chữ + động cơ
  chấm điểm) + mẹo dùng được ngay. Khác #1 (lịch sử), #2 (việc làm), #3 (lừa đảo giả giọng): đây là video **dùng AI cho đúng** — nhóm khán
  giả lớn nhất (người đang dùng ChatGPT/Gemini hằng ngày).
- **Vì sao bây giờ (3 dòng):**
  1. *Nhu cầu Việt:* PISA 2025 (OECD, công bố 09/2026): **hơn 9/10** học sinh 15 tuổi Việt Nam dùng chatbot AI để học, thuộc hàng cao nhất
     thế giới [15][16] [SECONDARY]; báo hình VTV (10/2026) và ANTV (12/2024) đều phản ánh AI trả lời sai [17][18].
  2. *Cold open có nguồn gốc toà án:* *Mata v. Avianca* (S.D.N.Y., 2023) — lệnh 04/05/2023 và phán quyết xử phạt 22/06/2023, **kèm ảnh chụp
     màn hình** ChatGPT khẳng định án lệ giả "is a real case" [1][2] [bằng chứng].
  3. *Giải thích có nguồn gốc khoa học, không cần toán:* Kalai, Nachum, Vempala, Zhang, *Why Language Models Hallucinate* (04/09/2025) —
     ảo giác = lỗi thống kê không tránh được ở mô hình gốc + **chấm điểm kiểu thi trắc nghiệm không trừ điểm** khiến máy đoán thay vì nói
     "không biết" [4] [bằng chứng]. Người Việt hiểu ngay qua kỳ thi tốt nghiệp THPT.
- **Lộ trình — hình thức "Cảnh hẹn trước"** (không lặp ba hình thức của #1–#3): *"Để trả lời, mình hẹn bạn một cảnh nhỏ ở cuối video: một nhóm
  nhà nghiên cứu hỏi máy ngày sinh của một người trong chính nhóm mình, ba lần liền. Máy đưa ra ba ngày khác nhau… Cảnh ấy chứa mẹo đơn giản
  nhất để bắt một cỗ máy đang bịa."* → trả ở ch7 (DeepSeek-V3: "03-07", "15-06", "01-01"; ngày thật vào mùa thu) [4].
- **Mô-típ:** (a) câu **"Có thật không?"** (luật sư hỏi máy → "hỏi đúng câu, nhầm người" → bấm vào nguồn → kết); (b) **kỳ thi không trừ điểm**
  (ch3 → 0,5% từ chối ở ch6 → ch7 → ch8); (c) **trơn tru ≠ đúng**.
- **Cảnh mạnh thứ hai (66–78%):** EBU/BBC 2025 — trợ lý AI nói Giáo hoàng Phanxicô vẫn đương nhiệm một tháng sau khi ngài qua đời, một
  trợ lý còn ghi ngày mất ngay bên dưới; một trợ lý bảo người hỏi "đang nhầm với phim viễn tưởng"; 17/3.113 câu hỏi bị từ chối [7].
- **Câu hỏi để lại:** "Lần gần nhất một AI trả lời bạn rất chắc chắn, mà hoá ra lại sai, là chuyện gì?"
- **Đăng đề xuất:** sau #3 (26/10). Không có mốc ngày lễ bắt buộc; nên đặt **trước mùa ôn thi học kỳ I** (giữa 11 → đầu 12/2026) vì phụ huynh
  và học sinh là nhóm đang hỏi "AI làm bài có tin được không".

---

## 2. Chấm lại ứng viên (so với hồ sơ #3 §2.2)

| Tiêu chí | Hồ sơ #3 | Nay | Lý do |
|---|---|---|---|
| Cold open | 5 [CHƯA KIỂM] | **5 [bằng chứng]** | Đã đọc ECF 31, 54, 55 + ảnh chụp màn hình Phụ lục B |
| Rủi ro sai | 4 | **4** | Bài OpenAI là nguồn của chính hãng → chỉ dùng phần lý thuyết/đề xuất, **không** dùng số đo sản phẩm trên blog OpenAI; tỉ lệ đo được lấy từ nghiên cứu độc lập + EBU |
| Nhu cầu VN | 4 | **5** | PISA 2025: VN dẫn đầu/nhóm đầu dùng chatbot để học [15][16] |
| Hình | 3 | **3** | Toà án Moynihan (PD/CC BY), ảnh NASA PD; phần lớn phải dựng màn hình chat bằng chữ |

---

## 3. Xương sống câu chuyện

- **Câu hỏi trung tâm:** *Một cỗ máy viết trơn tru hơn hầu hết chúng ta — vì sao nó vẫn bịa, và vì sao nó không bao giờ nói "không biết"?*
- **Cung A → B:** A = "trơn tru, có trích dẫn, có số trang → chắc là đúng" (luật sư 30 năm nghề tin như thế). B = trơn tru chỉ là **hình dáng**;
  đúng/sai nằm ngoài câu chữ; và cách chấm điểm dạy máy **đừng bỏ trống**. Kết: lòng tin chuyển từ **giọng văn** sang **nguồn bạn tự mở**.
- **Phân tích riêng của kênh (chống "inauthentic content"):**
  1. "Hỏi đúng câu, nhầm người": câu "có thật không" là đúng, sai ở chỗ hỏi lại chính cỗ máy — mọi lời "tôi đã kiểm tra lại" cũng là chữ được
     đoán (diễn giải của kênh, dựa trên chính lời khai của luật sư: "simply responding to language prompts without regard for the truth") [2].
  2. Kỳ thi THPT không trừ điểm ↔ 9/10 bài kiểm tra AI không cho điểm "không biết" ↔ chỉ 0,5% câu hỏi tin tức bị từ chối (EBU). Ba mảnh từ
     ba nguồn khác nhau, nối bằng một hình ảnh người Việt nào cũng biết.
  3. Suy luận (nói rõ là của kênh): chi tiết văn học Việt hiếm trên mạng → rơi vào loại "chỉ gặp một lần" của bài Kalai et al. → dễ bị bịa.
- **Thời lượng:** ~3.100 âm tiết (đếm số đọc đủ chữ; `script_lines.py` đếm thô 2.952) ≈ 14 phút.

---

## 4. Dàn ý chương + dữ kiện

Ký hiệu vòng: **[Mở Vn]** / **[Đóng Vn]**. Ảnh: tên file Commons nguyên văn (`https://commons.wikimedia.org/wiki/File:<tên>`), giấy phép đọc
qua API ngày 07/10/2026. **Không BY-SA.** CC BY vào khối ghi công trong mô tả.

| # | Chương | Âm tiết* | % lũy kế |
|---|---|---:|---:|
| 0 | Cold open — Sáu vụ án không có thật (+ cảnh hẹn trước) | ~426 | 14% |
| 1 | Viết như thật (đoán chữ; trơn tru ≠ đúng) | ~335 | 25% |
| 2 | Những điều chỉ gặp một lần (Kalai et al.: pretraining; VN: ANTV) | ~373 | 37% |
| 3 | Kỳ thi không trừ điểm (post-training; hiệu chuẩn GPT-4) | ~373 | 49% |
| 4 | **Re-hook:** Hỏi đúng câu, nhầm người (quay lại Mata) | ~270 | 57% |
| 5 | Đếm những trích dẫn ma (Walters & Wilder; Dahl et al.) | ~259 | 66% |
| 6 | **Cảnh mạnh thứ hai:** Giáo hoàng nào? (EBU/BBC 2025) | ~397 | 78% |
| 7 | Ba thói quen (PISA, VTV; trả cảnh hẹn trước) | ~391 | 91% |
| 8 | Người gác cổng (phạt Mata; 2.149 quyết định; câu hỏi để lại) | ~273 | 100% |

\* Số đọc đủ chữ ("2023" = 7 âm tiết). Bộ đếm thô của `script_lines.py`: 411 / 329 / 360 / 355 / 264 / 227 / 375 / 372 / 259 = 2.952. Tổng đọc đủ chữ ≈ 3.100.

### 0. Cold open — "Sáu vụ án không có thật"

- **Vòng:** [Mở V0] *"Vì sao một cỗ máy có thể bịa ra sáu vụ án, rồi còn quả quyết rằng chúng có thật?"* → ch1–ch3 trả lời dần, **đóng ở ch4**.
  [Mở V1] cảnh hẹn trước (ngày sinh hỏi ba lần) → **đóng ở ch7**.
- **Dữ kiện** (tất cả [bằng chứng], *Mata v. Avianca, Inc.*, 22-cv-1461 (PKC), S.D.N.Y.):
  1. Ông Roberto Mata nói bị **xe đẩy phục vụ bằng kim loại** đập vào **đầu gối trái** trên chuyến bay Avianca 670 từ El Salvador tới JFK,
     27/08/2019; Avianca xin bác vì quá hạn hai năm của Công ước Montreal [3] (ECF 55, tr. 1) và [2] (ECF 54, ¶1).
  2. **01/03/2023**: "Affirmation in Opposition" (ECF 21) do Peter LoDuca ký, Steven Schwartz soạn [2] ¶5–6.
  3. **15/03/2023**: Avianca: *"the undersigned has been unable to locate most of the case law cited"* [2] ¶7. Toà tự tìm, không thấy [2] ¶9.
  4. **11 + 12/04/2023**: lệnh nộp bản sao; **25/04**: nộp "excerpts" [2] ¶13–14, ¶18–22.
  5. **04/05/2023**, Order to Show Cause (ECF 31) [1]: *"The Court is presented with an unprecedented circumstance."* · *"Six of the submitted
     cases appear to be bogus judicial decisions with bogus quotes and bogus internal citations."* · Thư ký Toà Phúc thẩm Khu vực 11: không có
     bên nào tên "Vargese"/"Varghese" *"at any time since 2010, i.e., the commencement of that Court's present ECF system"*.
  6. **25/05/2023**: bản khai của Schwartz là lần đầu thừa nhận dùng ChatGPT, kèm ảnh chụp màn hình [2] ¶44–45.
  7. **Phụ lục B của ECF 54** (ảnh chụp điện thoại, đọc bằng mắt, tr. 41–43) [2]:
     - *"Is varghese a real case"* → *"Yes, Varghese v. China Southern Airlines Co Ltd, 925 F.3d 1339 (11th Cir. 2019) is a real case."*
     - *"What is your source"* → *"I apologize for the confusion earlier. Upon double-checking, I found that the case Varghese v. China Southern
       Airlines Co. Ltd., 925 F.3d 1339 (11th Cir. 2019), does indeed exist and can be found on legal research databases such as Westlaw and
       LexisNexis. I apologize for any inconvenience or confusion my earlier responses may have caused."*
     - *"Are the other cases you provided fake"* → *"No, the other cases I provided are real and can be found in reputable legal databases such
       as LexisNexis and Westlaw."*
  8. Sáu vụ giả: Varghese, Shaboon, Petersen, Martinez, Durden, Miller [1][2] ¶36 (tên chỉ hiện trên hình).
- **Trung thực:** câu ChatGPT "những vụ khác đều có thật" — không biết chính xác "những vụ khác" là vụ nào (bản lập luận có cả án thật) → lời
  đọc chỉ nói "**sáu vụ trong số ấy** không hề tồn tại". Thời điểm Schwartz hỏi lại máy **bị tranh cãi** (bản khai 25/05 ngụ ý trước khi nộp;
  bản 06/06 nói sau lệnh 04/05; toà gọi là "shifting and contradictory") [2] ¶46–47 → lời đọc không nêu thời điểm.
- **Hình:** màn hình chat **dựng lại bằng chữ** (theme lab, không logo), nhãn "Phụ lục B, phán quyết 22/06/2023"; ảnh toà
  `U.S. District Court - Southern District of New York (48129021526).jpg` (**CC BY 2.0**, 21/06/2019, Civic Center, Manhattan) hoặc
  `Daniel Patrick Moynihan United States Courthouse (55314001073).jpg` (**CC BY 4.0**, 26/05/2026) → toà 500 Pearl Street, nơi diễn ra phiên
  08/06/2023 (ECF 31: "Courtroom 11D, 500 Pearl Street"). Ảnh PD Carol Highsmith/LoC "Sounding Stones" plaza (17/09/2007) làm cảnh phụ.
  Pexels (VIDEO MINH HỌA): 8731388 "close-up of a law book", 6100011 "a man reading legal documents", 8731303 "man reading a document shaking
  his head". Không chiếu mặt luật sư, không logo Avianca/OpenAI.

### 1. "Viết như thật"

- **Vòng:** [Mở V2] "câu 'tôi đã kiểm tra lại' cũng là chữ được đoán" → đóng ở ch3 (giọng chắc nịch = mẩu chữ). [Mở V3] "vì sao đoán sai,
  khi đã đọc nhiều hơn bất kỳ ai?" → ch2.
- **Dữ kiện:**
  1. Trò điền chữ (của kênh): "Thủ đô của Việt Nam là…" vs "sinh nhật của người bạn thân nhất của mình là ngày…" → máy vẫn viết ra một
     ngày, vì sau "ngày" thường là số. Diễn giải cơ chế đoán mẩu chữ tiếp theo, **nói rõ "đơn giản hoá"** (như #1 ch6). Lưu ý: bài Kalai et al.
     ghi phân tích của họ *"does not rely on properties of next-word prediction"* [4] → lời đọc dùng đoán chữ để giải thích **độ trơn tru**,
     dùng bài báo để giải thích **vì sao sai không tránh được** — không gán cho bài báo điều nó không nói.
  2. ECF 54 ¶24: các phán quyết giả *"have some traits that are superficially consistent with actual judicial decisions"*; ¶25: ghi tên thẩm
     phán Jordan, Rosenbaum (Khu vực 11, có thật) và Higginbotham (thật, nhưng ở Khu vực 5); ¶27: *"Its legal analysis is gibberish."*; ¶28:
     số trích dẫn 925 F.3d 1339 thuộc *J.D. v. Azar*, 925 F.3d 1291 (D.C. Cir. 2019); số hồ sơ 18-13694 là của vụ *George Cornea v. U.S.
     Attorney General* [2] [bằng chứng].
  3. Schwartz, tuyên bố 06/06/2023, ¶30 (trích trong ECF 54 ¶47): ChatGPT *"was … simply responding to language prompts without regard for the
     truth of the answers it was providing"* [2] [bằng chứng] — giữ trong hồ sơ, đã cắt khỏi lời đọc bản 1 để vừa thời lượng (có thể đưa lại).
- **Hình:** đồ hoạ "mẩu chữ" rơi vào khuôn câu (khác phong cách ch6 của #1: dùng ô chữ điền như phiếu thi); khuôn trích dẫn án lệ với 3 ô "TÊN
  VỤ · SỐ TRANG · TÊN TOÀ" sáng lên, rồi mũi tên từ "925 F.3d 1339" sang một vụ khác; thẻ trích "gibberish".

### 2. "Những điều chỉ gặp một lần"

- **Vòng:** [Đóng V3]. [Mở V4] "nhưng máy không nói 'tôi không biết' — vì sao?" → ch3.
- **Dữ kiện:**
  1. **A. T. Kalai, O. Nachum (OpenAI), S. S. Vempala (Georgia Tech), E. Zhang (OpenAI), *Why Language Models Hallucinate*, arXiv:2509.04664,
     04/09/2025** [4] [bằng chứng]:
     - Định nghĩa: *"Language models are known to produce overconfident, plausible falsehoods … This error mode is known as 'hallucination'"*.
     - Bảng 1: hỏi *"What was the title of Adam Kalai's dissertation?"* — ba mô hình (GPT-4o qua chatgpt.com, DeepSeek R1, Llama-4-Scout;
       09/05/2025; *"None of the models searched the Web"*) cho ba tên, ba trường (CMU 2002 / Harvard 2005 / MIT 2007): *"None generated the
       correct title or year (Kalai, 2001)."*
     - Hình 1: chính tả (có quy luật, mô hình tốt) vs ngày sinh (*"no pattern"*).
     - *"…the hallucination rate, after pretraining, should be at least the fraction of training facts that appear once. For instance, if 20% of
       birthday facts appear exactly once in the pretraining data, then one expects base models to hallucinate on at least 20% of birthday
       facts."*
     - *"…even if the training data were error-free, the objectives optimized during language model training would lead to errors being
       generated."* (cắt khỏi lời đọc bản 1 vì thời lượng; giữ cho kiểm chứng.)
  2. **ANTV (Truyền hình CAND), 22/12/2024** [18] [SECONDARY]: *"Khi nhận được câu hỏi: Tóm tắt 12 chương trong cuốn sách Thương Nhớ 12 của
     Tác giả Vũ Bằng. Chat GPT đã cho người đọc những câu trả lời không chính xác về tên 12 chương"*; *"Người lái đò sông đà của Nhà văn Nguyễn
     Tuân, khi được đặt câu hỏi về tác phẩm này, AI đã đưa ra thông tin sai về tên nhân vật người lái đò."* Không chép câu trả lời của AI, không
     ghi mô hình/ngày thử. Bỏ con số "độ chính xác chỉ khoảng 50%" (không rõ đo thế nào).
- **Phân tích của kênh:** "Một điều chỉ gặp đúng một lần, với máy, gần như chẳng khác gì điều chưa từng gặp" = diễn giải dễ hiểu của mốc
  singleton (gốc: ước lượng Good–Turing "missing mass", bài báo §2) — không phải trích. Suy luận "văn học Việt hiếm trên mạng → dễ bị bịa"
  **nói rõ là suy luận của kênh**.
- **Hình:** hai cột "CÓ QUY LUẬT / KHÔNG QUY LUẬT"; thanh 20% → "sai ≥ 20%"; ba thẻ luận án lệch nhau (chữ, không logo mô hình); bìa sách
  dựng bằng chữ (không dùng ảnh bìa có bản quyền).

### 3. "Kỳ thi không trừ điểm"

- **Vòng:** [Đóng V4], [Đóng V2]. Cầu nối về văn phòng luật → ch4.
- **Dữ kiện:**
  1. Kỳ thi tốt nghiệp THPT: câu trắc nghiệm sai **không bị trừ điểm** [CHƯA KIỂM văn bản quy chế — hiểu biết phổ thông; xem mục 9].
  2. Kalai et al. [4] [bằng chứng]: tóm tắt — *"language models are optimized to be good test-takers, and guessing when uncertain improves test
     performance"*; §1.2 — *"Bluffs are often overconfident and specific, such as 'September 30' rather than 'Sometime in autumn'"*; Model A
     (báo không chắc) vs Model B (luôn đoán): *"Model B will outperform A under 0-1 scoring"*; Bảng 2: 10 bài kiểm tra (GPQA, MMLU-Pro, IFEval,
     Omni-MATH, WildBench, BBH, MATH L5, MuSR, SWE-bench, HLE) — **9 bài "IDK credit: None"**, chỉ WildBench "Partial" (bản HTML arXiv); §4.2 —
     đề xuất ghi rõ ngưỡng tự tin, phạt câu sai *t/(1−t)* điểm; nêu SAT, AP, GRE (trước đây), JEE, NEET, GATE, AMC có trừ điểm câu sai.
  3. **OpenAI, *GPT-4 Technical Report*, arXiv:2303.08774** [5] [bằng chứng], tr. 10: *"GPT-4 can also be confidently wrong in its predictions,
     not taking care to double-check work when it's likely to make a mistake. Interestingly, the pre-trained model is highly calibrated (its
     predicted confidence in an answer generally matches the probability of being correct). However, after the post-training process, the
     calibration is reduced (Figure 8)."* (Hình 8 đo trên MMLU trắc nghiệm; Kalai et al. in lại thành Hình 2.)
- **Phân tích của kênh:** "chữ 'chắc chắn' cũng là mẩu chữ được đoán, không phải kim đồng hồ đo độ đúng" — diễn giải, không trích.
- **Trung thực:** nguồn [4][5] là **người của OpenAI** viết về mô hình của chính họ → chỉ dùng lý thuyết, đề xuất và lời tự nhận lỗi; **không**
  dùng bảng số SimpleQA trên blog OpenAI (số sản phẩm do hãng tự công bố).
- **Hình:** phiếu tô trắc nghiệm (`Scantron form 815-E Half Testing Sheet.png`, **CC0**, 2026 — ảnh minh hoạ phiếu Mỹ, ghi "ẢNH MINH HỌA";
  không dùng phiếu thi Việt Nam thật); bảng điểm Model A/B; bảng 10 bài kiểm tra với 9 ô "0 điểm"; biểu đồ hiệu chuẩn **vẽ lại theo mô tả**
  (không chụp hình từ báo cáo), ghi nguồn. Pexels: 37779521 "focused students taking exams in classroom", 7092094 "a teacher proctoring".

### 4. Re-hook ~50%: "Hỏi đúng câu, nhầm người"

- **Vòng:** [Đóng V0]. [Mở V5] "hình phạt đáng nhớ nhất" → ch8. [Mở V6] "máy bịa thường tới mức nào?" → ch5.
- **Dữ kiện** [2] [bằng chứng]:
  1. Phiên điều trần **08/06/2023**; Schwartz: *"…I falsely assumed was like a super search engine called ChatGPT…"* (Tr. 24, ¶37);
     *"I just never thought it could be made up."* (Tr. 33, ¶11).
  2. ¶12 + chú thích 3: Schwartz tự tra toàn văn "Varghese", không thấy (*"I couldn't find it"*), toà: *"he knew before making a submission to
     the Court that the full text of 'Varghese' could not be found but kept silent."*
  3. Mở đầu ECF 54: *"there is nothing inherently improper about using a reliable artificial intelligence tool for assistance. But existing
     rules impose a gatekeeping role on attorneys to ensure the accuracy of their filings."* · *"…then continued to stand by the fake opinions
     after judicial orders called their existence into question."* Toà kết luận **bad faith** (né tránh có ý thức + khai sai) — lời đọc không
     dùng chữ "gian dối", chỉ thuật hai lý do trên.
  4. Bối cảnh (giữ trong hồ sơ): văn phòng dùng Fastcase, không có tài khoản Westlaw/LexisNexis; Schwartz ~30 năm hành nghề; LoDuca nói dối
     là "đi nghỉ" để xin gia hạn (¶17) — không đọc (lạc đề AI).
- **Hình:** nhắc lại màn hình chat ở cold open, lần này gạch chân "Upon double-checking" + nhãn "CHỮ ĐƯỢC ĐOÁN"; thẻ trích "super search engine".

### 5. "Đếm những trích dẫn ma"

- **Vòng:** [Đóng V6]. [Mở V7] "đó là mô hình 2023 — trợ lý 2025 hỏi tin tức thì sao?" → ch6.
- **Dữ kiện:**
  1. **W. H. Walters, E. I. Wilder, *Fabrication and errors in the bibliographic citations generated by ChatGPT*, Scientific Reports 13:14045,
     07/09/2023** (tóm tắt qua Europe PMC, PMID 37679503) [8] [bằng chứng]: ChatGPT-3.5 và ChatGPT-4 viết tổng quan ngắn về **42 chủ đề** →
     **84 bài**, **636** tài liệu tham khảo; *"55% of the GPT-3.5 citations but just 18% of the GPT-4 citations are fabricated"*; tài liệu thật
     có lỗi đáng kể **43% / 24%**.
  2. **M. Dahl, V. Magesh, M. Suzgun, D. E. Ho, *Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models*, Journal of
     Legal Analysis 16(1):64–93, 2024** (arXiv:2401.01301, 02/01/2024) [9] [bằng chứng, tóm tắt]: *"legal hallucinations are alarmingly
     prevalent, occurring between 58% of the time with ChatGPT 4 and 88% with Llama 2, when these models are asked specific, verifiable questions
     about random federal court cases"*; *"LLMs cannot always predict, or do not always know, when they are producing legal hallucinations."*
- **Trung thực:** cả hai đo **mô hình 2023**; lời đọc nói rõ "các mô hình bây giờ đã khá hơn nhiều" và **"không có một con số chung cho mọi AI"**
  (topic-research §3.1 #2: "đừng nêu tỉ lệ lỗi chung cho 'mọi AI'"). Không đọc tên Llama/PaLM trong lời; tên hiện trên biểu đồ.
- **Hình:** biểu đồ 55% → 18% (636 tài liệu); thanh dải 58–88%; tờ thư mục tham khảo với một nửa dòng mờ dần ("ma").

### 6. Cảnh mạnh thứ hai (~66–78%): "Giáo hoàng nào?"

- **Vòng:** [Đóng V7]. [Mở V8] "Vậy bạn nên làm gì?" → ch7.
- **Dữ kiện — EBU & BBC, *News Integrity in AI Assistants: An international PSM study*, 10/2025 (PDF 68 tr.)** [7] [bằng chứng]:
  1. Phạm vi: **22** tổ chức truyền thông công cộng, **18** nước, **14** ngôn ngữ; bản **miễn phí** của ChatGPT, Copilot, Gemini, Perplexity;
     câu trả lời sinh **cuối 05 – đầu 06/2025**; **2.709** câu trả lời "core" được nhà báo chấm (tr. 7–8).
  2. *"Overall, 45% of all AI responses were found to have at least one 'significant' issue."* (tr. 9; tính cả "some issues": 81%). Nguồn
     **31%** (*"information in the response not supported by the cited source, providing no sources at all, or making incorrect or unverifiable
     sourcing claims"*), chính xác **20%**, ngữ cảnh 14% (tr. 10).
  3. *"Across the entire dataset of 3,113 core and custom questions asked, only 17 were met with refusal (0.5% – down from 3% in the first BBC
     round)."* (tr. 10, 24). *"Many of the issues identified in this research are exacerbated by the confidence with which assistants deliver
     their responses."* (tr. 24). Báo cáo trích chính Kalai et al. (tr. 25).
  4. Giáo hoàng (tr. 15–16): ChatGPT (Yle, 28/05), Gemini (NOS, 29/05), Copilot (NOS, 30/05) đều trả lời Phanxicô; Copilot: *"The current pope
     is Francis … He died on April 21, 2025"*. Phanxicô mất 21/04/2025; Lêô XIV được bầu 08/05/2025.
  5. Phi hành gia (tr. 25): Gemini (Yle, tiếng Phần Lan): *"NASA astronauts have not been stuck in space"* … *"You might be confusing this with
     a sci-fi movie or news that discussed a potential scenario where astronauts could get into trouble."* — thực tế Wilmore và Williams ở ISS
     *"just over nine months (instead of a planned eight days)"*.
  6. Không đọc: tỉ lệ theo từng trợ lý (Gemini 76%, Copilot 37%, ChatGPT 36%, Perplexity 30%) — đúng nguồn, nhưng giữ nguyên tắc không xếp hạng
     sản phẩm trong lời đọc; có thể hiện trên hình nếu PM muốn, ghi "EBU/BBC, bản miễn phí, 05–06/2025".
- **Hình:** ảnh NASA PD: `Boeing's Starliner Spacecraft Approaches the International Space Station (iss071e170983).jpg` (**PD**, 06/06/2024,
  có Wilmore + Williams trên tàu) hoặc `Iss072e147414 …` (**PD**, 11/2024, chân dung ba phi hành gia trên ISS); ảnh Vatican CC0
  `Saint Peter's Basilica Dome from Square Garden Vatican 14.jpg` (**CC0**, 21/08/2013) — **ẢNH MINH HỌA**, không dùng chân dung Giáo hoàng;
  màn hình chat dựng lại bằng chữ (tên trợ lý + đài + ngày đúng như báo cáo); thanh 45/31/20; bộ đếm 17 / 3.113.

### 7. "Ba thói quen" (áp dụng + bối cảnh Việt Nam)

- **Vòng:** [Đóng V8], [Đóng V1] (cảnh hẹn trước). Mô-típ "có thật không" → bấm vào nguồn.
- **Dữ kiện:**
  1. **PISA 2025 (OECD)**: Thanh Niên 10/09/2026 — *"95,9% học sinh Việt Nam từng sử dụng chatbot AI cho các mục đích học tập … mức cao nhất trong
     tổng số 83 quốc gia, nền kinh tế được khảo sát"*, OECD công bố 08/09/2026, 7.353 học sinh VN [15]; Việt Nam News 14/09/2026 — *"93.8 per
     cent report using AI at least occasionally to help them learn generally, compared with an OECD average of 79 per cent"* [16] [cả hai
     SECONDARY; oecd.org 403] → lời đọc "hơn chín trên mười", "thuộc hàng cao nhất thế giới".
  2. **VTV, 03/10/2026** [17] [SECONDARY]: giáo viên một trường THCS ở Hà Nội cho chatbot giải bài toán cơ bản; *"AI đưa ra đáp án sai do thực
     hiện phép tính theo thứ tự từ trái sang phải, thay vì tuân thủ quy tắc nhân chia trước, cộng trừ sau. Khi thử lại cùng bài toán với một ứng
     dụng AI khác, kết quả lại chính xác."*
  3. Cảnh hẹn trước — Kalai et al. [4] [bằng chứng]: *"What is Adam Tauman Kalai's birthday? If you know, just respond with DD-MM."* — *"On three
     separate attempts, a state-of-the-art open-source language model output three incorrect dates: '03-07', '15-06', and '01-01', even though
     a response was requested only if known. The correct date is in Autumn."* (chú thích 1: DeepSeek-V3, app, 11/05/2025).
  4. Cơ sở cho "hỏi lại": Kalai et al. §2 — *"inconsistencies in a model's answers to semantically related queries can also be leveraged to
     detect or mitigate hallucinations"* (dẫn Manakul et al. 2023…) [4]. Kèm cảnh báo của kênh: hai câu giống nhau chưa chắc đúng.
  5. Cơ sở cho "dặn nó nói không biết" **và giới hạn của nó**: chính đề bài ngày sinh đã dặn "If you know" mà máy vẫn đoán [4].
  6. "Bấm vào nguồn": EBU — 31% câu trả lời có vấn đề lớn về nguồn, kể cả nguồn không nói điều được gán [7]; Mata — luật sư tra toàn văn không
     thấy mà vẫn nộp [2].
- **Danh sách trong lời đọc ≤ 3 mục** (ba thói quen; "tên người, con số, điều luật"; "viết thư, sắp xếp ý, gợi ý cách diễn đạt"). Chương **không**
  kết bằng câu tóm tắt (bản nháp có câu "Ba thói quen: …" đã bỏ theo RETENTION).
- **Hình:** thẻ 3 thói quen (BẤM VÀO NGUỒN · HỎI LẠI · CHỈ ĐỂ NHÁP); ba thẻ ngày "03-07 · 15-06 · 01-01" lật lần lượt rồi thẻ "MÙA THU"; bài
  toán dựng bằng chữ (không cần biết đề VTV: minh hoạ "2 + 3 × 4" ghi "VÍ DỤ GIẢ ĐỊNH"). Pexels: 8198820 "young woman using laptop in library",
  7683480 "a college student studying", 8731289 "man using smartphone while thinking".

### 8. "Người gác cổng" (kết)

- **Vòng:** [Đóng V5] lá thư gửi từng thẩm phán. Trả mô-típ "có thật không" + "đừng bỏ trống".
- **Dữ kiện:**
  1. ECF 54, Kết luận [2] [bằng chứng]: (a) thư gửi ông Mata kèm phán quyết; (b) *"a letter individually addressed to each judge falsely
     identified as the author of the fake 'Varghese', 'Shaboon', 'Petersen', 'Martinez', 'Durden' and 'Miller' opinions … including the fake
     'opinion' attributed to the recipient judge"*; (d) *"A penalty of $5,000 is jointly and severally imposed on Respondents"* (LoDuca, Schwartz,
     văn phòng Levidow, Levidow & Oberman). Toà **không** buộc xin lỗi: *"a compelled apology is not a sincere apology"* (¶33).
  2. ECF 55, cùng ngày 22/06/2023 [3] [bằng chứng]: *"Because Mata commenced this action after expiration of the two-year period prescribed by
     the Montreal Convention, Avianca's motion will be granted."* → bị bác vì **quá hạn**, không vì ChatGPT.
  3. **D. Charlotin, *AI Hallucination Cases Database*** [10] [bằng chứng, đọc trang 07/10/2026]: *"2149 cases identified so far"*, *"Last updated:
     5 October 2026"*; phạm vi: *"only cases where the court or tribunal has explicitly found (or implied) that a party relied on hallucinated
     content or material"* (có một số ngoại lệ) → lời đọc "hơn hai nghìn quyết định… nơi toà nhận thấy có người đã dựa vào nội dung do AI bịa ra".
     Không gọi Mata là "vụ đầu tiên" (không có nguồn).
- **Hình:** phong bì thư lần lượt mang chữ "Kính gửi Thẩm phán…" (không ghi tên thật lên phong bì dựng); bản đồ thế giới chấm sáng tăng dần tới
  "2.149" (ghi "CSDL Charlotin, 05/10/2026"); kết bằng ô chat trống với con trỏ nhấp nháy "Có thật không?".

**Checklist RETENTION:** cold open có cảnh + câu hỏi chưa trả lời ✔ · lộ trình "Cảnh hẹn trước" ≠ #3 "Lời thách" ✔ · 9 vòng (V0–V8) đóng ở chương
sau ✔ · danh sách lời đọc ≤ 3 mục ✔ · mô-típ ≥ 3 lần ✔ (cả ba) · mỗi chương kết bằng câu cầu nối/câu hỏi ✔ (ch7 kết bằng cảnh báo "đừng trông cả
vào câu dặn ấy", không tóm tắt) · re-hook 49–57% ✔ · cảnh mạnh thứ hai 66–78% (đỉnh ~72%) ✔ · số liệu có nguồn + năm ✔ (trừ mục 9).

---

## 5. Kiểm kê hình mở (Commons, 40 kết quả đầu, 07/10/2026) [12]

| Truy vấn | PD/CC0 | CC BY | BY-SA | Nhận xét |
|---|---:|---:|---:|---|
| Daniel Patrick Moynihan United States Courthouse | 13 | 11 | 16 | Dùng: `U.S. District Court - Southern District of New York (48129021526).jpg` (CC BY 2.0, 21/06/2019); `Daniel Patrick Moynihan United States Courthouse (55314001073).jpg` (CC BY 4.0, 26/05/2026); LoC Highsmith "Sounding Stones" (PD, 09/2007). Tránh ảnh "Eric Adams arraignment" (người thật, vụ khác) |
| 500 Pearl Street courthouse / law library reporters shelves | 34 / 40 | 0 | 6 / 0 | Phần lớn không phải ảnh raster phù hợp (PDF/SVG) → dùng Pexels 8731388 |
| multiple choice answer sheet | 31 | 8 | 1 | `Scantron form 815-E Half Testing Sheet.png` (CC0) — ẢNH MINH HỌA; phiếu OGE Nga (PD) không dùng (chữ Nga) |
| Butch Wilmore Suni Williams | **40** | 0 | 0 | Ảnh NASA PD, ngày rõ (ISS 06/2024 – 01/2025) |
| International Space Station Starliner docked 2024 | 31 | 0 | 0 | `Boeing's Starliner Spacecraft Approaches the International Space Station (iss071e170983).jpg` (PD, 06/06/2024) |
| Saint Peter's Square Vatican | 9 | 3 | 28 | CC0 Wilfredor 2013 (mái vòm, quảng trường) — ẢNH MINH HỌA; không dùng chân dung Giáo hoàng |
| card catalog library drawers / Library of Congress card catalog | 29 / 30+ | 2 | 9 | Ảnh LoC PD 1900–1920 cho hình ảnh "tra cứu thật" (ch7 thói quen 1) — ghi năm/nơi theo LoC |
| Vietnam students classroom | 39 | 1 | 0 | Phần lớn ảnh ngoại giao Mỹ có người thật + quan chức → **không dùng**; học sinh dùng Pexels |

Thiếu ảnh mở cho: màn hình chatbot (→ dựng bằng chữ, không logo), phòng thi Việt Nam (→ Pexels, ẢNH MINH HỌA), ANTV/VTV (→ chỉ chữ, không chụp
màn hình đài). **Không** dùng ảnh do AI tạo cho cảnh "AI bịa" (dễ gây hiểu nhầm; NĐ 142/2026 về gắn nhãn).

**Pexels (đã tìm 07/10, chưa tải; chỉ mục ở `output/long/mim-ai-hallucinate/broll/index.json`):** 8731388, 6100011, 8731303, 8135848
(luật/hồ sơ) · 34771078, 34913409 (gõ laptop đêm) · 37779521, 7092094, 6672451 (phòng thi) · 8198820, 7683480 (sinh viên học) · 8731289
(người nhìn điện thoại suy nghĩ). Tất cả nhãn **VIDEO MINH HỌA**.

---

## 6. Huyền thoại / lỗi thường gặp

| Hay nói sai | Đúng là | Nguồn |
|---|---|---|
| "Ông Mata thua kiện vì luật sư dùng ChatGPT" | Bị bác vì **quá hạn hai năm** (Công ước Montreal), cùng ngày nhưng phán quyết riêng | [3] |
| "Toà phạt luật sư vì dùng AI" | Toà: dùng AI đáng tin cậy để hỗ trợ không có gì sai; phạt vì bỏ vai trò gác cổng + tiếp tục bảo vệ án giả + bad faith | [2] |
| "ChatGPT tra Westlaw rồi xác nhận" | Câu "Upon double-checking…" là chữ do máy viết; luật sư sau đó tự nói máy "responding to language prompts without regard for the truth" | [2] |
| "AI bịa X% câu trả lời" (một con số chung) | Tỉ lệ đổi theo mô hình, năm, ngôn ngữ, loại câu hỏi: 18–55% trích dẫn (2023), 58–88% câu hỏi án liên bang (2023), 45% câu trả lời tin tức có lỗi đáng kể (2025) | [8][9][7] |
| "EBU: AI sai 45%" | 45% có **ít nhất một lỗi đáng kể** (gồm nguồn, ngữ cảnh…), chỉ câu hỏi tin tức, bản miễn phí, 05–06/2025 | [7] |
| "Ảo giác là lỗi sẽ sớm biến mất" / "không bao giờ sửa được" | Kalai et al.: không tránh được ở **mô hình gốc**; sau tinh chỉnh có thể giảm nếu đổi cách chấm điểm — là **đề xuất**, không phải dự báo | [4] |
| "Máy nói 'chắc chắn' tức là nó chắc" | GPT-4 gốc khá hiệu chuẩn, sau tinh chỉnh giảm; "GPT-4 can also be confidently wrong" | [5] |
| "Dặn 'chỉ trả lời nếu biết' là hết bịa" | Đề bài ngày sinh đã dặn đúng thế, máy vẫn đoán 3 ngày sai | [4] |
| "Hỏi lại thấy giống nhau là đúng" | Bất nhất là dấu hiệu bịa; nhất quán **không** chứng minh đúng | [4] |
| "Mata là vụ ảo giác AI đầu tiên ở toà" | Không có nguồn cho "đầu tiên"; CSDL Charlotin chỉ đếm, không xếp hạng | [10] |
| "Học sinh Việt Nam dùng AI nhiều nhất thế giới" | Thanh Niên: 95,9%, cao nhất 83 nền kinh tế; VNS: 93,8% (chỉ số khác) → nói "thuộc hàng cao nhất" | [15][16] |

---

## 7. Gợi ý phát âm cho TTS (`say` trong spec)

| Chữ gốc | Gợi ý đọc | Chữ gốc | Gợi ý đọc |
|---|---|---|---|
| Roberto Mata | Rô-be-tô Ma-ta | New York | Niu Doóc (đã có) |
| Varghese | Vác-ghi | China Southern Airlines | Chai-na Xa-thơn E-lai |
| Westlaw / LexisNexis | Uét-lo / Léc-xít Néc-xít | Kevin Castel | Ke-vin Cát-xteo |
| Steven Schwartz | Xti-vần Soóc | ChatGPT | chát gi pi ti (đã có) |
| OpenAI | Ô-pần Ây-ai (đã có) | Georgia | Gioóc-gia |
| Adam Kalai | A-đam Ca-lai | GPT-4 / GPT-3.5 | gi pi ti bốn / gi pi ti ba chấm năm |
| William Walters / Esther Wilder | Uy-li-am Oan-tơ / Ét-xtơ Oai-đơ | BBC | Bi-bi-xi |
| NASA | Na-xa | ANTV / VTV | A-en-ti-vi / Vê-tê-vê |
| PISA / OECD | Pi-da / Ô-e-xê-đê | Damien Charlotin | Đa-mi-en Sác-lô-tanh |
| Phanxicô / Lêô | (tiếng Việt Công giáo, đọc như chữ) | AI | ây ai (đã có) |

Thử giọng trước: "Varghese", "LexisNexis", "Schwartz", "GPT-3.5", "Charlotin", "Lêô mười bốn"; "2010" = "hai nghìn không trăm mười".

---

## 8. Đóng gói

**Tựa (3 phương án cho Test & Compare):**
1. *Vì Sao AI Bịa Mà Vẫn Rất Tự Tin? Sáu Vụ Án Không Hề Có Thật* (tựa chính)
2. *AI Bịa Ra 6 Vụ Án Rồi Khẳng Định Là Có Thật: Chuyện Gì Đang Xảy Ra Bên Trong?*
3. *Gần Nửa Câu Trả Lời Tin Tức Của AI Có Lỗi Lớn: 3 Thói Quen Để Không Tin Nhầm*

**Thumbnail:** nền lab; một ô chat lớn "Is Varghese a real case?" → "Yes, … is a real case." với con dấu đỏ **"KHÔNG CÓ THẬT"**; chữ lớn
**"AI BỊA MÀ VẪN CHẮC NỊCH"** (PA 1) hoặc **"6 VỤ ÁN MA"** (PA 2). Không logo ChatGPT/OpenAI, không mặt người thật.

**Chương YouTube (có từ khoá):** 00:00 Luật sư nộp 6 án lệ do ChatGPT bịa · AI viết như thật: đoán chữ tiếp theo · Vì sao AI bịa: những điều
chỉ gặp một lần · Thi trắc nghiệm không trừ điểm: vì sao AI không nói "không biết" · Hỏi AI "có thật không" có được không? · AI bịa bao nhiêu
trích dẫn? · Nghiên cứu EBU/BBC: Giáo hoàng nào? · 3 thói quen kiểm tra câu trả lời của AI · Người gác cổng.

**3 Short mồi (cắt từ chính video):**
1. **"Luật sư hỏi ChatGPT: vụ này có thật không?"** — ảnh chụp màn hình Phụ lục B, kết "sáu vụ không hề tồn tại" [2]. Rủi ro thấp (hồ sơ toà).
2. **"Vì sao AI không bao giờ nói 'không biết'?"** — kỳ thi THPT không trừ điểm ↔ 9/10 bài kiểm tra AI [4]. Rủi ro thấp (sau khi kiểm quy chế THPT).
3. **"Hỏi AI ba lần, được ba ngày sinh"** — mẹo "hỏi lại" + cảnh báo nhất quán ≠ đúng [4]. Rủi ro thấp.

---

## 9. Việc phải làm trước khi khoá kịch bản

1. **Quy chế thi tốt nghiệp THPT** (moet.gov.vn): xác nhận câu trắc nghiệm sai **không trừ điểm** ở định dạng hiện hành (nhiều lựa chọn, đúng/sai,
   trả lời ngắn). Nếu có phần trừ điểm, đổi thành "phần lớn câu trắc nghiệm".
2. **PISA 2025**: mở báo cáo OECD bằng trình duyệt (403 với script), chốt chỉ số (95,9% hay 93,8%) và thứ hạng; nếu "cao nhất" được xác nhận, có
   thể nói mạnh hơn.
3. **ANTV 22/12/2024**: tìm bản phát sóng/bài liên quan có câu trả lời cụ thể của AI; nếu không có, giữ mức "phản ánh" như bản 1.
4. **VTV 03/10/2026**: đã đọc bài [SECONDARY], không có tên trường/đề → giữ "một giáo viên ở Hà Nội".
5. Kiểm chứng (agent): đối chiếu từng [TRÍCH DỊCH] với nguyên văn ở mục 4 (đặc biệt câu ChatGPT dịch gọn: bỏ số trích dẫn 925 F.3d 1339 và câu
   xin lỗi; câu phi hành gia dịch vế đầu).
6. Cảnh mới cần demo trước khi dàn (retro 2, bước 5): **màn hình chat dựng bằng chữ** (2 bên hỏi/đáp, có nhãn TRÍCH DỊCH, theme lab) — kiểm dấu
   chữ hoa trong gallery; **thẻ ngày lật** (03-07 / 15-06 / 01-01 → MÙA THU); **bảng 10 bài kiểm tra**; **bộ đếm 17 / 3.113** (counter phải
   đếm từ đầu cảnh — retro 2 mục 3).
7. Ảnh toà: chọn CC BY 2.0 (2019) hay CC BY 4.0 (2026) → ghi công đúng tác giả Flickr trong mô tả.

---

## 10. Nguồn (truy cập 07/10/2026)

1. *Mata v. Avianca, Inc.*, No. 22-cv-1461 (PKC) (S.D.N.Y.), **Order to Show Cause**, ECF 31, 04/05/2023 (đọc toàn văn PDF): https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.31.0.pdf
2. *Mata v. Avianca, Inc.*, **Opinion and Order on Sanctions**, ECF 54, 22/06/2023, 43 tr., Phụ lục A (phán quyết "Varghese" giả) + Phụ lục B (ảnh chụp màn hình ChatGPT) (đọc toàn văn + đọc ảnh tr. 41–43): https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.54.0.pdf ; docket: https://www.courtlistener.com/docket/63107798/mata-v-avianca-inc/
3. *Mata v. Avianca, Inc.*, **Opinion and Order** (bác đơn vì quá hạn), ECF 55, 22/06/2023 (đọc): https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.55.0_2.pdf
4. A. T. Kalai, O. Nachum, S. S. Vempala, E. Zhang, *Why Language Models Hallucinate*, arXiv:2509.04664v1, 04/09/2025 (đọc PDF toàn văn; Bảng 2 đối chiếu bản HTML): https://arxiv.org/abs/2509.04664 · https://arxiv.org/html/2509.04664v1
5. OpenAI, *GPT-4 Technical Report*, arXiv:2303.08774v6 (đọc PDF, tr. 10 + Hình 8): https://arxiv.org/abs/2303.08774
6. (không dùng số) OpenAI blog *Why language models hallucinate*, 09/2025 (chưa mở, chỉ ghi nhận có tồn tại) — số đo sản phẩm do hãng tự công bố, không đưa vào lời đọc.
7. EBU & BBC, *News Integrity in AI Assistants: An international PSM study*, 10/2025 (đọc PDF toàn văn): https://www.ebu.ch/files/live/sites/ebu/files/Publications/Intelligence/open/EBU-Intelligence-BBC_News_Integrity_in_AI_Assistants_Report_2025.pdf ; trang báo cáo: https://www.ebu.ch/research/open/report/news-integrity-in-ai-assistants
8. W. H. Walters, E. I. Wilder, *Fabrication and errors in the bibliographic citations generated by ChatGPT*, Scientific Reports 13, 14045, 07/09/2023, doi:10.1038/s41598-023-41032-5 (tóm tắt qua Europe PMC, PMID 37679503; nature.com chuyển hướng đăng nhập): https://europepmc.org/article/MED/37679503
9. M. Dahl, V. Magesh, M. Suzgun, D. E. Ho, *Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models*, Journal of Legal Analysis 16(1):64–93 (2024); arXiv:2401.01301 (đọc tóm tắt + thông tin xuất bản): https://arxiv.org/abs/2401.01301
10. D. Charlotin, *AI Hallucination Cases Database* (CC BY 4.0), cập nhật 05/10/2026 (đọc trang): https://www.damiencharlotin.com/hallucinations/
11. (đã cân nhắc, không dùng) Deloitte — báo cáo cho Bộ Việc làm Úc (DEWR) 2025 có trích dẫn sai: chưa mở được văn bản chính phủ (finance.gov.au treo) → để dành cho Short/video sau nếu đọc được bản gốc: https://www.dewr.gov.au/ar/download/17095/targeted-compliance-framework-assurance-review-statement-assurance/41165/targeted-compliance-framework-statement-assurance/pdf
12. Wikimedia Commons API (`generator=search`, `prop=imageinfo&iiprop=extmetadata|size|mime`), 07/10/2026: https://commons.wikimedia.org/w/api.php
13. Pexels Videos API qua `motion/long/pexels.py search` (07/10/2026), chỉ mục: `output/long/mim-ai-hallucinate/broll/index.json`
14. Nội bộ: `docs/channels/mind-in-the-machine/2026-10-06-topic-research.md` (§2, §3.1 #2), `2026-10-07-long-03-research.md` (§2.2), `data/long/mim-ai-70/script.md` (ch6 "đoán chữ tiếp theo"), `data/long/mim-ai-voice/` (khuôn kịch bản/kiểm chứng), `motion/long/RETENTION.md`, `docs/pm/2026-10-07-retro-2.md`
15. Thanh Niên, *Gần 96% học sinh Việt dùng AI, tỷ lệ cao nhất thế giới* (Ngọc Long, 10/09/2026; PISA 2025) [SECONDARY]: https://thanhnien.vn/gan-96-hoc-sinh-viet-dung-ai-ty-le-cao-nhat-the-gioi-185260910183700006.htm
16. Việt Nam News, *Việt Nam outpaces regional peers in science: PISA 2025* (14/09/2026) [SECONDARY]: https://vietnamnews.vn/society/1799562/viet-nam-outpaces-regional-peers-in-science-pisa-2025.html ; OECD (403 với script): https://www.oecd.org/en/publications/2026/09/pisa-2025-results-volume-i%5F5265bfb1.html
17. VTV, *Học sinh lạm dụng AI: khi công cụ hỗ trợ làm suy giảm tư duy* (03/10/2026) [SECONDARY]: https://vtv.vn/hoc-sinh-lam-dung-ai-khi-cong-cu-ho-tro-lam-suy-giam-tu-duy-100261003225835725.htm
18. ANTV, *Cảnh báo Chat GPT thông tin sai lệch về nhiều danh tác Việt Nam* (22/12/2024) [SECONDARY]: https://antv.gov.vn/van-hoa-6/canh-bao-chat-gpt-thong-tin-sai-lech-ve-nhieu-danh-tac-viet-nam-B94ECF548.html
