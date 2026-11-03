# Audit workflow tìm và chọn hot trend cho MIM / CK (02/11/2026)

Phạm vi: MIM (Mind in the Machine), CK (Biểu Đồ Biết Nói). Chỉ đọc code/dữ liệu, không chạy API, không đọc credentials, không sửa gì khác ngoài file này.

Quy ước nhãn: **[ĐO]** = thấy trực tiếp trong code/dữ liệu/log (kèm file:dòng hoặc truy vấn); **[SUY]** = suy luận của người audit, chưa kiểm.

## 0. Kết luận một đoạn

Hệ thống hiện **không có bước phát hiện trend theo tin tức**. Chủ đề đến từ (a) bảng chủ đề cố định/danh sách do chủ kênh dán vào phiên Lead, (b) bản đo "nhu cầu" hằng tuần chạy tay (từ khoá kênh đã có + Wikipedia pageviews + dán tay tab Trends của Studio), (c) kết quả thắng/thua của chính kênh. Hàng chờ MIM đã kín tới 04/12 nên một tin nóng hôm nay chưa thể lên sóng trong 24–72 h nếu không có cơ chế chen. CK còn nhiều slot trống nên chen được ngay về mặt lịch, nhưng chưa có quy trình/cổng nhanh.

---

## 1. Sơ đồ luồng hiện tại (chữ + bảng)

```
[Nguồn ý tưởng]                     [Đo / chấm]                      [Kiểm chứng]            [Sản xuất & lịch]
Chủ kênh dán danh sách 30 chủ đề    Không chấm điểm hot             Fact file tay theo lô    spec JSON -> build.py
 (docs/pm/2026-11-02-*-30-chu-de)    (title/hook "nháp, chưa đo")    (pilot-short/*-factcheck)  -> enqueue_*.py -> state.sqlite
Bảng chủ đề cố định/pillars         feedback_loop.py (TAY, theo tuần)  Long: factcheck.md +      -> upload private + publishAt
 (factory/pillars/*, cases.tsv)      -> demand.py: từ khoá kênh,        long_gate.py             -> lưới 5 slot/ngày
Thắng/thua tuần (retro, so-that-bai)  Wikipedia vi pageviews, dán Trends  Lịch(CL): factcheck.py
```

| # | Bước | Làm gì | File:dòng | Loại |
|---|---|---|---|---|
| 1 | Chọn đề tài | Chủ kênh dán danh sách 30 chủ đề/kênh vào phiên Lead; title/hook ghi rõ "nháp: chưa đo tìm kiếm, chưa kiểm trùng, chưa factcheck" | `docs/pm/2026-11-02-mim-30-chu-de.md:3`, `docs/pm/2026-11-02-ck-30-chu-de.md:3` | [ĐO] thủ công |
| 2 | Chọn đề tài (cũ) | "Dòng chưa dùng tiếp theo trong bảng cố định" | `factory/demand.py:3-4` (docstring tự nhận) | [ĐO] |
| 3 | Đo nhu cầu (A): từ khoá YT_SEARCH đã dẫn người xem tới kênh, top 25 | Analytics API của chính kênh | `factory/demand.py:50-72` | [ĐO] (nhu cầu đã đáp ứng, không phải khoảng trống: `demand.py:130`) |
| 4 | Đo nhu cầu (B): Wikipedia vi pageviews, trung vị 28 ngày + so cùng kỳ năm trước | Danh sách theo dõi `data/demand/MIM.json` (20 chủ đề), `CK-*.json` | `factory/demand.py:75-190` (HttpPageviews 165-190) | [ĐO] |
| 5 | Đo nhu cầu (C): "khoảng trống" = người dán tay tab Research/Trends của YouTube Studio | không có API | `factory/demand.py:215-230` | [ĐO] thủ công |
| 6 | Gom lại thành brief | `feedback_loop.py` chạy tay, ghi `data/briefs/<KÊNH>.md`; "chuyển nhu cầu thành chủ đề là việc của Claude khi viết pack trong chat" | `scripts/feedback_loop.py:1-14,34-55`; `factory/demand.py:19-20` | [ĐO] |
| 7 | Chấm kết quả đã đăng | scoreboard (EVR, từ khoá) | `factory/scoreboard.py` (557 dòng) | [ĐO], đo bài đã đăng, không đo ý tưởng mới |
| 8 | Nghiên cứu tư liệu | Wikipedia EN + ảnh Commons PD (Short); thêm Openverse/Wellcome/Europeana/NASA/Smithsonian (Long) | `motion/stier/research.py:1-10`, `motion/long/research_long.py:1-8`, `motion/long/media_search.py:1-8` | [ĐO] là nghiên cứu ảnh/bài nền, không phải tin |
| 9 | Kiểm trùng chủ đề | So tiêu đề với danh sách video **cùng kênh** (`data/channel_titles/<KÊNH>.json`) | `factory/lines/novelty.py:63,82-90` | [ĐO] |
| 10 | Đo độ lặp khuôn | Tỉ lệ câu trùng khuôn theo dòng nội dung, **đo không chặn**, mỗi kênh riêng | `factory/sameness.py:1-20,49-50,116` | [ĐO] |
| 11 | Kiểm chứng Short | Fact file tay theo lô (nguồn mở được, nhãn SƠ CẤP/SECONDARY, "CHƯA KIỂM ĐƯỢC -> không nói") | `docs/pm/pilot-short/mim-pilot-1318-factcheck.md:1-30`, `ck-pilot-0811-1211-factcheck.md` | [ĐO] thủ công, theo lô pilot |
| 12 | Kiểm chứng Long | `factcheck.md` ≥ 8 URL, năm trong kịch bản phải có trong factcheck | `scripts/long_gate.py:168-185`; `motion/long/factcheck_lint.py:1-8` | [ĐO] |
| 13 | Xếp lịch | spec -> enqueue -> `state.sqlite` -> upload private + `publishAt`; slot 5/ngày | `motion/stier/enqueue_mim.py`, `enqueue_ck.py`; `data/shorts_slots.json:1-6`; `scripts/shorts_grid.py:28-50` | [ĐO] |
| 14 | Đổi lịch bài đã up | `Channel.reschedule` chỉ cho video **đang private** (videos.update, 50 đơn vị quota) | `factory/channel.py:297-308`; `scripts/reschedule.py` | [ĐO] |

### Tần suất và lần chạy gần nhất (câu hỏi 2) [ĐO]

- **Không có tác vụ tự động nào cho phát hiện trend.** `schtasks /query` trên máy này không có tác vụ nào chứa YT/youtube/factory/monitor. File `motion/stier/monitor_daily.cmd:1-4` nhắc Task Scheduler "YT-CL-Monitor" nhưng trỏ `C:\Tools\Youtuber\yt-factory` (thư mục cũ, kênh CL, tuần test 05–11/10): đã lỗi thời.
- `feedback_loop.py` (đo + nhu cầu) chạy **tay**. Dấu vết: `data/briefs/` chỉ còn `MIM.md` (mtime 20/10 07:54, **không có CK.md**); `data/demand/MIM.json` 05/10 (chưa sửa từ đó), `CK-2026-10-23.json` 23/10, `CK-2026-10-27.json` 27/10. Tức lần đo nhu cầu gần nhất cho CK là 27/10 (6 ngày trước), cho MIM là 20/10 (13 ngày trước).
- `CK-2026-10-27.json` dùng **Google autocomplete** (`method: "Google autocomplete ds=yt hl=vi gl=vn; Wikipedia vi"`), do một lần chạy tay ngoài code `factory/` (không có hàm tương ứng trong repo). Chính `docs/audit/2026-10-05-demand-sources-research.md:1` khuyên **tránh** `suggestqueries.google.com` (API không chính thức). Đây là điểm cần chủ kênh quyết, xem mục 4.
- yt-dlp chỉ xuất hiện ở một script phân tích một lần `output/analysis/week44/fetch.py`, chạy 02/11; `-J` từng video thất bại 166/166 (yt-dlp 2025.05.22 cũ): `docs/pm/2026-11-02-thang-thua-tuan-44.md` mục 0. Chưa có `ytsearch` dùng để dò đối thủ.

### Chấm điểm độ hot (câu hỏi 3) [ĐO]

- **Không có điểm hot cho ý tưởng.** Không file nào trong `factory/`, `motion/`, `scripts/` tính điểm theo số nguồn tin, tốc độ tin, search volume hay view đối thủ. Grep các từ trending/rss/google news/pytrends/hacker news trong `*.py` (loại `.ref`) chỉ ra `demand.py` (nhắc tên nguồn trong docstring) và tài liệu.
- Số thật đang dùng: Wikipedia pageviews (mức quan tâm, trễ 1–2 ngày: `demand.py:106` `FRESH = 2`, và chậm vì `THROTTLE = 1.0 s/request`: `demand.py:36`), từ khoá YT_SEARCH của kênh, EVR/view của video đã đăng.
- Tiêu chí chọn hook thực tế là **mẫu thắng/thua nội bộ** (tuần 44): CK = cặp số tiền đối nghịch ở câu đầu (bài có chữ số câu đầu trung vị 701,5 vs 211; n nhỏ); MIM = người có tên làm điều trái kỳ vọng (cụm Lee Sedol trung vị 830). `docs/pm/2026-11-02-thang-thua-tuan-44.md` mục 2; phân loại hàng chờ `docs/pm/2026-11-02-hang-cho-short-mau-thua.md:3-12` (MIM 10 thắng-mẫu / 53 trung tính / 42 thua-mẫu, CK 0/6/9; **phỏng đoán theo mẫu n nhỏ**, tự ghi như vậy).

### Kiểm chứng (câu hỏi 4)

- `factory/factcheck.py` + `factory/claims.py`: **chỉ cho kênh Lịch (CL)**: đối chiếu sao/trực/ngày với `vnlunar` (`factcheck.py:1-25`, `claims.py:1-35`), được gọi từ `scripts/check_lich.py:13`, `scripts/make_lich_month.py:26`. Không dùng được cho tin MIM/CK. [ĐO]
- `motion/long/factcheck_lint.py` + `scripts/long_gate.py:168-185`: **chỉ Long**, và chỉ kiểm "số/ngày/trích có dấu vết trong factcheck.md", không suy sự thật từ mạng (`factcheck_lint.py:1-8`). [ĐO]
- **Short MIM/CK: không có cổng tự động về dữ kiện.** `motion/stier/script_lint.py:129-133` chỉ kiểm có trường `sources` (R10), không kiểm nội dung nguồn. Fact file Short là tài liệu viết tay theo lô (mục 11 bảng trên), 28/10 cho pilot 13–18/11. [ĐO]
- Rủi ro đã có trong repo: `scripts/long_gate.py:30` có danh sách `BANNED_PUBLIC` (CẦN, cần kiểm, factcheck, agent...) vì từng lọt ghi chú nội bộ ra mô tả công khai (memory: no-internal-notes). Short chưa có cổng tương đương trong `enqueue_mim.py` (sao chép `spec["sources"]` thẳng vào mô tả, `enqueue_mim.py:~38`). [ĐO về hành vi copy; SUY về rủi ro với tin nóng]

### Độ trễ và hàng chờ (câu hỏi 5) [ĐO, truy vấn `state.sqlite` chỉ đọc 02/11]

| | MIM | CK |
|---|---|---|
| Short đã hẹn giờ từ 02/11 | 106 | 19 |
| Ngày hẹn xa nhất (Short) | **04/12/2026 11:30 VN** (04:30Z) | 12/11/2026 19:00 VN |
| Slot/ngày đã có (tuần 03–09/11) | 5/5 mọi ngày (không còn slot trống) | 1–2/5 mỗi ngày: **22 slot trống** trong 03–09/11 (`shorts_grid.py`) |
| Chênh `publish_at` − `updated_at` (ngày), Short tương lai | nhỏ nhất 15, **trung vị 25**, lớn nhất 44 | 10 / **13** / 26 |
| Long hẹn giờ từ 02/11 | 18 bài tới 01/12 | tới 22/11 |

- `updated_at` là mốc cập nhật hàng gần nhất, dùng làm xấp xỉ ngày vào kho [SUY: có thể bị đẩy muộn hơn ngày tạo spec]. Mới nhất: MIM 29/10 14:08Z, CK 28/10 02:48Z.
- Hệ quả [SUY từ số trên]: nếu một sự kiện xảy ra hôm nay, đường hiện tại đưa Short MIM lên sóng **sau ≥ 32 ngày** (slot trống đầu tiên sau 04/12), CK **vài ngày** (slot trống 03/11 nếu kịp dựng). Thời gian dựng + QA một Short chưa đo được từ dữ liệu này; mô tả trong `docs/pm` chưa có số giờ/Short.
- **Không có cơ chế chen bài nóng.** Không có khái niệm slot dự phòng/ưu tiên trong `data/shorts_slots.json:1-6` (chỉ `target` + giờ từng kênh); `shorts_grid.py:50` xếp bài vào slot gần nhất còn trống, bài thừa thành khoá `+HH:MM`. Chen một bài vào ngày đã kín nghĩa là phải đẩy bài khác: bài đã `stage='published'` (upload private + hẹn giờ) chỉ đổi được qua `Channel.reschedule` từng video (50 đơn vị quota/lần, `channel.py:297`), và chính sách nội bộ "chỉ thay video đã upload khi lỗi đổi nghĩa, hỏi chủ kênh trước" (`hang-cho-short-mau-thua.md:30`).
- Ràng buộc upload: pacing MIM/CK = (1 phút, 90/24 giờ) nhưng giới hạn thật là quota GCP chung project CL ~92 upload/ngày (`factory/channels.py:49-52`); CK từng bị khoá sau ~10 upload/ngày trong >18 giờ (memory: youtube-channel-upload-limit). Một tin nóng 1–2 bài không chạm trần này.

### Góc riêng theo kênh và kiểm trùng chéo (câu hỏi 6) [ĐO]

- Không có cấu trúc "một sự kiện, hai góc". Mỗi kênh có danh sách chủ đề và prefix riêng (`factory/channels.py:52,57`).
- `novelty.duplicate_on_channel(ch, title)` nạp **chỉ** `data/channel_titles/<ch>.json` (`novelty.py:63,82-90`); `sameness.py` đo theo `channel` (`sameness.py:68,116`). **Không có kiểm trùng chéo MIM↔CK.** Hai file tiêu đề được làm mới lần cuối 20/10 10:13 (`ls` mtime): 13 ngày trước, nên bài đăng từ 20/10 chưa chắc nằm trong đó [SUY: cần xác nhận script làm mới].
- Kiểm trùng là theo tiêu đề/bigram (`novelty.py:49-54`), không theo thực thể ("Binance", "Fed"): chính `research.py:8-9` ghi "trùng tiêu đề chưa chắc bắt được trùng nhân vật".

---

## 2. Bảng điểm yếu và nguy cơ bỏ lỡ trend

| # | Điểm yếu | Bằng chứng | Mức | Nguy cơ bỏ lỡ trend |
|---|---|---|---|---|
| 1 | Không có bước phát hiện tin/trend tự động; mọi đề tài là chọn tay hoặc bảng cố định | `demand.py:3-4`; grep không thấy RSS/Google News/Trends trong code; không có tác vụ lịch | Cao | Mọi sự kiện nóng chỉ vào được nếu chủ kênh nhớ và dán vào phiên |
| 2 | Hàng chờ MIM kín tới 04/12, trung vị 25 ngày từ lúc vào kho đến lúc đăng; không có làn nóng | truy vấn `state.sqlite`; `shorts_grid.py` MIM 5/5 mọi ngày | Cao | Tin nóng MIM trễ ≥ 32 ngày = mất giá trị hoàn toàn |
| 3 | Không có điểm hot đo được (nguồn tin/tốc độ/đối thủ/search volume) | không có hàm chấm trong repo; title/hook "nháp chưa đo" (`mim-30-chu-de.md:3`) | Cao | Chọn nhầm đề đã nguội, bỏ đề đang lên |
| 4 | Đo nhu cầu chạy tay, thưa, và đã lệch ngày: không có `CK.md` brief; MIM đo gần nhất 20/10; Wikipedia trễ 1–2 ngày | mtime `data/briefs`, `data/demand`; `demand.py:36,106` | Trung bình-Cao | Wikipedia pageviews phản ánh tin sau 1–2 ngày: quá chậm cho "tin nóng 24 h" |
| 5 | Factcheck Short là tay, theo lô; không có cổng tự động trước enqueue; `factcheck.py/claims.py` chỉ cho Lịch | `script_lint.py:129-133`; `factcheck.py:1-25` | Cao với tin nóng (tin chưa xác nhận, số liệu đổi theo giờ) | Rủi ro đăng tin sai/chưa xác minh nếu rút ngắn quy trình mà không có cổng |
| 6 | Kiểm trùng chéo kênh không có; kiểm trùng theo tiêu đề, danh sách tiêu đề cũ từ 20/10 | `novelty.py:63,82`; mtime `data/channel_titles` | Trung bình | Cả hai kênh cùng đề một sự kiện cùng giờ, hoặc trùng bài đã đăng sau 20/10 |
| 7 | Chưa dò đối thủ YouTube VN; yt-dlp bản cũ, `-J` lỗi 166/166 | `thang-thua-tuan-44.md` mục 0; chỉ `output/analysis/week44/fetch.py` dùng yt-dlp | Trung bình | Không biết khoảng trống đối thủ; có thể làm đề đã có 20 video |
| 8 | Chu kỳ bài hôm nay đã cũ: CK dư slot nhưng không có đề nóng để đổ vào (CK 22/35 slot trống tuần tới) | `shorts_grid.py` CK 03–09/11 | Trung bình | CK là kênh duy nhất chen được ngay, nhưng đang thiếu nguồn đề |
| 9 | Script nhắc lịch/giám sát đã lỗi thời | `monitor_daily.cmd:2-4` trỏ `C:\Tools\Youtuber\yt-factory` | Thấp | Không phải trend, nhưng ví dụ không có tác vụ lịch đang chạy |
| 10 | Rủi ro riêng với tin nóng: ảnh/clip tin tức (bản quyền) đang không có kho hợp lệ | Short chỉ dùng Commons PD/Pexels/CC (`research.py:1-10`) | Cao nếu tự động hoá | Tin nóng thiếu ảnh hợp lệ -> dùng chữ+đồ hoạ (khung 0 đã hỗ trợ chữ lớn, `thang-thua-tuan-44.md` mục 2) |

---

## 3. Đề xuất: chuỗi tự động hoá phát hiện → chấm điểm → title/hook 3 s → kiểm trùng → factcheck → hàng render nhanh

Nguyên tắc: ít LLM (LLM chỉ viết hook/title ở bước 3 và chạy phiên Lead), **không API trả phí**, dùng nguồn công khai miễn phí; việc ĐĂNG/LỊCH luôn do chủ kênh duyệt. **Mọi nguồn dưới đây là gợi ý, chưa được chạy hay kiểm giấy phép trong audit này.**

Lưu ý bản quyền nguồn (từ `docs/audit/2026-10-05-demand-sources-research.md:1`, mục TL;DR): RSS VnExpress/Tuổi Trẻ/Dân Trí ghi miễn phí cho "cá nhân và tổ chức phi lợi nhuận", **kênh kiếm tiền không nằm trong phạm vi**; chỉ dùng làm tín hiệu nội bộ (đếm tiêu đề, không sao chép nội dung), hoặc xin phép; Thanh Niên yêu cầu ghi nguồn; GDELT hợp lệ cho tin pháp luật. Google Trends: RSS "Trending now" geo=VN có nút Export chính thức; **tránh** `pytrends` và `suggestqueries` theo chính tài liệu đó. [ĐO nội dung tài liệu; SUY về tuân thủ cho từng nguồn mới như Hacker News/Reddit/Wikipedia pageviews top: cần chủ kênh xác nhận]

| Bước | Tái dùng | Thêm mới | Tần suất | Ngưỡng | Người duyệt |
|---|---|---|---|---|---|
| **1. Phát hiện** | `HttpPageviews` (UA + lùi 429) làm mẫu client HTTP: `demand.py:165-190`; `factory/console.py` | `scripts/trend_scan.py`: lấy tiêu đề từ Google News RSS theo từ khoá kênh, RSS tên miền báo (chỉ tiêu đề + URL + giờ), Google Trends daily RSS VN, Hacker News Algolia/Reddit JSON công khai (MIM), bảng giá vàng/tỷ giá công khai (CK). Ghi `data/trend/<ngày>.jsonl` mỗi dòng: `{nguồn, tiêu đề, url, giờ}` | 2 giờ/lần giờ làm việc, bằng Task Scheduler (một tác vụ mới, **cần chủ kênh bật**) | Không lọc ở bước này | Không |
| **2. Gộp & chấm điểm** | `novelty._tokens/syllables/bigrams` (`novelty.py:38-54`) để gom tiêu đề gần nhau thành một "sự kiện" | `scripts/trend_score.py`: cụm tiêu đề -> sự kiện; điểm theo công thức mục 4; xuất `data/trend/hot_<ngày>.md` (top 10 mỗi kênh) | Sau mỗi lần quét | Điểm ≥ 60/100 vào danh sách chờ duyệt | Chủ kênh/Lead nhìn top 10, chọn ≤ 2 sự kiện/ngày |
| **3. Title/hook 3 s** | Mẫu thắng tuần 44 (`thang-thua-tuan-44.md` mục 2, 4): CK = cặp số tiền đối nghịch, MIM = người có tên + kết quả đảo kỳ vọng; `factory/lines/script_craft.py`/`script_signals.py` nếu phù hợp [SUY: chưa đọc kỹ] | Một khung prompt cố định cho phiên Lead: input = sự kiện + 3 số/tên đã trích; output = title ≤ 100 ký tự + câu mở ≤ 3 s + chữ khung 0; tự kiểm bằng regex: có chữ số hoặc tên riêng trong câu 1 (mẫu thắng) | Khi duyệt xong bước 2 | Hook phải chứa ≥ 1 số thật hoặc tên người/tổ chức từ nguồn | Lead soạn, chủ kênh xem |
| **4. Kiểm trùng** | `novelty.duplicate_on_channel` (`novelty.py:82`), `sameness.py` | `scripts/trend_dedupe.py`: (a) trùng với kho cả hai kênh (gộp `data/channel_titles/MIM.json` + `CK.json`, **làm mới trước khi chạy**); (b) trùng thực thể (tên riêng trích từ tiêu đề) với specs trong `data/stier/specs/*.json`; (c) cờ "đã dùng cùng sự kiện ở kênh kia trong 72 giờ" | Mỗi lần có ứng viên | Trùng bigram ≥ ngưỡng `novelty.similar` -> loại; trùng chéo kênh -> yêu cầu góc khác | Không (tự loại), chủ kênh xem lý do |
| **5. Factcheck** | `factory/claims.py` (mô hình: thống kê tự đếm / diễn giải phải khai căn cứ / suy đoán cấm: `claims.py:12-30`), `long_gate.py:168-185` (năm/số phải có trong factcheck), `script_lint.py:129-133` (R10 sources) | `scripts/hot_factcheck.py`: yêu cầu file `data/trend/<slug>/facts.md` có ≥ 2 nguồn độc lập, 1 nguồn **sơ cấp** (cơ quan/doanh nghiệp), mỗi số/tên trong spec phải khớp một dòng trong facts.md (theo `factcheck_lint.py` mở rộng cho Short); thêm cờ "tin chưa xác nhận": cấm từ khẳng định, dùng "theo [nguồn]" | Trước render | Không đạt 2 nguồn -> **không vào làn nóng** | **Bắt buộc người duyệt dữ kiện** (tin giả/pháp lý/thị trường) |
| **6. Hàng render nhanh** | `enqueue_mim.py`/`enqueue_ck.py`, `build.py`, `run_chain.py`, `shorts_grid.py --free` | Làn nóng (mục 5) + `scripts/hot_enqueue.py` chọn slot làn nóng và gọi enqueue sẵn có; quét `BANNED_PUBLIC` như `long_gate.py:30` trên mô tả trước khi upload | Theo yêu cầu | Render + QA trong ≤ 4 giờ làm việc [SUY: chưa đo thời gian thật] | **Chủ kênh duyệt video cuối và giờ lên lịch** |

### Gợi ý nguồn miễn phí (chưa chạy)

RSS: VnExpress, Tuổi Trẻ, CafeF, VnEconomy, GenK (chỉ đọc tiêu đề + giờ); Google News RSS theo từ khoá (`news.google.com/rss/search?q=...&hl=vi&gl=VN`); Google Trends RSS daily VN; YouTube `ytsearch` qua yt-dlp **sau khi cập nhật yt-dlp** (hiện `-J` lỗi, flat-playlist còn chạy: `thang-thua-tuan-44.md:mục 0`); Hacker News và Reddit JSON công khai; bảng giá SJC/tỷ giá công khai; Wikipedia Pageviews (đã có client). [SUY: mọi URL/giới hạn tốc độ/ToS cần xác nhận khi cài]

## 4. Công thức chấm điểm đề xuất (0–100, đơn giản, đo được)

```
điểm = 25*S + 20*V + 20*H + 15*G + 10*F + 10*D        (mỗi thành phần chuẩn hoá về 0..1)
```

| Ký hiệu | Tín hiệu đo được | Cách tính | Trọng số |
|---|---|---|---|
| S | Số nguồn độc lập đưa tin trong 24 h | số domain khác nhau trong cụm tiêu đề; S = min(n,6)/6 | 25 |
| V | Tốc độ tăng | (số bài 3 giờ gần nhất) / (số bài 3 giờ trước đó), chặn trên 3; V = min(r,3)/3; nếu có trong Google Trends VN +0,3 | 20 |
| H | Hook kiểu thắng tuần 44 | có số cụ thể trong nguồn sơ cấp (+0,5) và tên người/tổ chức nhận ra được (+0,5) | 20 |
| G | Khoảng trống đối thủ YouTube VN | `ytsearch` theo từ khoá; số video ≤ 72 giờ, G = 1 − min(n,10)/10; thiếu dữ liệu -> 0,5 | 15 |
| F | Phù hợp kênh | từ khoá khớp danh sách pillar/watchlist của kênh (`data/demand/*.json`, pillars): có = 1, không = 0; CK trừ 0,5 nếu bản chất là khuyến nghị mua/bán | 10 |
| D | Không trùng kho | 1 − độ trùng lớn nhất (bigram, `novelty.similar`) với kho **hai kênh**; trùng chéo trong 72 giờ -> D = 0 | 10 |

Ngưỡng: ≥ 70 vào làn nóng (chủ kênh duyệt); 50–69 đưa vào kho thường (slot dư, ví dụ CK); < 50 bỏ. Trọng số là khởi đầu **[SUY]**, không có dữ liệu hiệu chỉnh nội bộ: sau 4 tuần so điểm với view 72 giờ thật rồi chỉnh (bảng điểm có sẵn: `scoreboard.py`). Lưu ý nội bộ: mọi Short hiện dừng trần ~1.000 view (`thang-thua-tuan-44.md` mục 1), nên chưa có bằng chứng "bài nóng sẽ vượt trần"; cần thử, không hứa trước.

## 5. Cơ chế "làn nóng"

1. **Slot dự phòng**: đặt trong `data/shorts_slots.json` thêm khoá `"hot": {"MIM": ["12:30","20:30"], "CK": ["08:30","20:30"]}` (ví dụ, giờ VN, lệch các slot hiện có), `target` giữ 5; `shorts_grid.py` đọc thêm khoá này (cần sửa code: **giao Codex theo quy trình**, không làm trong audit). Hiện CK có sẵn 22 slot trống/7 ngày nên làn nóng CK dùng ngay không cần chen.
2. **Chen MIM kín lịch** (cần chủ kênh quyết): ba phương án: (a) dành 2 trong 5 slot/ngày cho làn nóng từ nay (bỏ 2 bài khuôn thua ở cuối hàng; `hang-cho-short-mau-thua.md` đã liệt kê 42 bài MIM thua-mẫu để rút); (b) đẩy lùi theo `reschedule.py` (50 đơn vị/bài, tốn quota, chỉ bài private); (c) thay bài thua-mẫu bằng bài nóng, cùng giờ (đây là "thay video đã upload": cần hỏi chủ kênh theo ngưỡng thay thế, vì mỗi bài đã upload private).
3. **Hạn dùng**: mỗi ứng viên nóng có `expires_at` (mặc định 72 giờ); quá hạn tự bỏ khỏi hàng, không dồn vào kho thường.
4. **Ngân sách**: tối đa 1 bài nóng/ngày/kênh lúc đầu; đo EVR 24h/72h như quy ước kiểm tra Long (memory long-form strategy).

## 6. Ví dụ chạy tay trên giấy: "Binance bị hack" (giả định, không phải tin có thật)

Giả định: 09:00 sáng có 6 báo (VnExpress, Tuổi Trẻ, CafeF, VnEconomy, GenK, 1 trang quốc tế) đưa tin một sàn tiền mã hoá lớn bị tấn công, nêu một số tiền thiệt hại và công bố từ chính sàn.

| Cổng | Kết quả giấy |
|---|---|
| Phát hiện | trend_scan thấy 6 domain trong 3 giờ, có trên Trends daily VN |
| Chấm điểm | S = 1 (≥ 6 nguồn), V ≈ 0,8, H = 1 (số thiệt hại + tên sàn), G ≈ 0,7 (ít video VN trong 72 giờ), F: MIM 0,5 (kỹ thuật), CK 0,5 (tiền); D = 1. Điểm ≈ 25+16+20+10,5+5+10 = 86,5. Vào làn nóng cả hai kênh |
| Hai góc | **CK = tác động tài chính**: giá, người dùng VN, cái gì chưa biết; **không khuyến nghị mua/bán** (quy tắc kênh, `channels.py:54-56`; chính sách YouTube về nội dung tài chính: cần chủ kênh xem lại trước khi làm làn nóng CK). **MIM = cơ chế kỹ thuật**: hacker vượt qua bằng cách nào (khoá riêng, ví nóng/lạnh, cầu nối), giải thích bằng đồ hoạ; tránh suy đoán thủ phạm khi chưa có kết luận |
| Hook 3 s | CK: "[số tiền] bị rút trong [vài phút]. Số dư của người dùng thì sao?" (số lấy từ nguồn sơ cấp, nếu chưa chốt thì dùng khoảng và ghi "theo [nguồn]"). MIM: "Không ai phá mật mã. Họ chỉ cần một chữ ký." (CHỈ nếu nguồn xác nhận cơ chế; nếu chưa, đổi sang hook mô tả sự kiện có số) |
| Kiểm trùng | quét kho hai kênh theo thực thể "Binance/sàn/hack"; nếu CK đăng trước, MIM phải khác góc (cơ chế) và lệch giờ ≥ 4 giờ; không dùng cùng thumbnail/khung 0 |
| Factcheck | ≥ 2 nguồn độc lập; ít nhất 1 sơ cấp (thông báo của sàn hoặc cơ quan); mỗi số/tên/ngày trong kịch bản có dòng nguồn; dữ liệu giá lấy từ bảng giá công khai kèm giờ; từ "bị hack" chỉ dùng khi nguồn xác nhận, không thì "bị tấn công/sự cố, theo ..." |
| Hàng nhanh | CK slot làn nóng gần nhất; MIM làn nóng nếu chủ kênh chọn phương án 5.2(a) |
| Người duyệt | chủ kênh duyệt (1) chủ đề, (2) factcheck, (3) video cuối, (4) giờ lên lịch |

Thời gian mục tiêu [SUY, chưa đo]: phát hiện 09:00, duyệt 10:00, kịch bản + factcheck 12:00, render/QA 15:00, lên lịch 17:00–20:30. Phụ thuộc vào thời gian dựng một Short, chưa có số đo.

## 7. Lộ trình

| Mức | Việc | Tái dùng/Thêm | Kết quả kiểm |
|---|---|---|---|
| **1 ngày** | (a) Chủ kênh quyết nguồn được phép (RSS báo VN, Google News RSS, Trends RSS, HN/Reddit, giá vàng). (b) Viết `trend_scan.py` mức tối giản chạy tay, ghi `data/trend/<ngày>.jsonl`. (c) Làm mới `data/channel_titles/*.json` và chạy lại `feedback_loop.py` cho CK (không có brief). (d) Dùng 22 slot trống CK làm làn nóng thử, không cần sửa code | `demand.py:165-190` (mẫu HTTP), `shorts_grid.py --free` | Quét được ≥ 5 nguồn, không lỗi 429; danh sách top 10 đọc được |
| **1 tuần** | (a) `trend_score.py` + `trend_dedupe.py` (gộp kho 2 kênh). (b) `hot_factcheck.py` bản Short (mở rộng `factcheck_lint.py`: số/ngày/tên phải có trong facts.md). (c) Khoá `hot` trong `shorts_slots.json` + sửa `shorts_grid.py` (giao Codex). (d) Một tác vụ Task Scheduler 2 giờ/lần (chủ kênh bật) | `novelty.py`, `claims.py` (mô hình), `long_gate.py` BANNED_PUBLIC | Chạy thử 5 ngày, ghi vào bảng: số sự kiện phát hiện, số lọt qua cổng, thời gian từ phát hiện đến lịch |
| **2 tuần** | (a) Hiệu chỉnh trọng số theo view 24h/72h của các bài nóng đã đăng; (b) thêm `ytsearch` G (sau cập nhật yt-dlp); (c) quy tắc chen MIM (phương án 5.2) do chủ kênh chốt; (d) cổng cuối chặn `BANNED_PUBLIC` cho Short trong `enqueue_*` | `scoreboard.py` để đo | So điểm dự báo với view 72h; dừng nếu trung vị bài nóng ≤ trung vị kênh |

## 8. Rủi ro

| Rủi ro | Chi tiết | Giảm thiểu |
|---|---|---|
| Tin giả / chưa xác nhận | tin nóng thay đổi theo giờ, số liệu đầu hay sai; không có cổng tự động cho Short (mục 2 #5) | 2 nguồn + 1 sơ cấp bắt buộc; nhãn "theo [nguồn], chưa xác nhận"; người duyệt dữ kiện; cho phép sửa/gỡ nhanh |
| Bản quyền ảnh/clip tin tức | pipeline hiện chỉ dùng PD/CC/Pexels (`research.py:1-10`); ảnh báo chí và clip thời sự không dùng được | Khung 0 bằng chữ + đồ hoạ, biểu đồ tự vẽ; Commons PD cho chân dung; ghi nguồn |
| Chính sách YouTube nội dung tài chính | CK đã tự cấm khuyến nghị mua/bán (`channels.py:54-56`); tin sàn crypto dễ trượt sang khuyến nghị | Chỉ mô tả sự kiện và cơ chế; thêm miễn trừ; chủ kênh xem chính sách hiện hành (chưa kiểm trong audit) |
| ToS nguồn tin | RSS báo VN không cho kênh kiếm tiền (`demand-sources-research.md:TL;DR`); `suggestqueries`/`pytrends` bị khuyên tránh; CK-2026-10-27 đã dùng Google autocomplete | Chỉ lưu tiêu đề+URL+giờ làm tín hiệu nội bộ; không sao chép nội dung; xin phép nếu cần; chủ kênh quyết về autocomplete |
| Quá tải upload | CK từng bị khoá sau ~10 upload/ngày (>18 giờ); quota GCP chung ~92/ngày (`channels.py:49-52`) | Làn nóng ≤ 1–2 bài/ngày/kênh; Long trước Short khi gần trần |
| Trùng chéo/nội dung lặp | YouTube nhắm nội dung hàng loạt (`sameness.py:3-9`); hai kênh cùng một sự kiện | `trend_dedupe.py` gộp kho + cờ 72 giờ; mỗi kênh một góc |
| Hao hụt hiệu quả | Trần ~1.000 view/Short vẫn còn; chưa có bằng chứng bài nóng vượt trần | Thử nhỏ, đo 24h/72h/7 ngày; dừng nếu không hơn trung vị |

## 9. Điều chưa biết (ghi rõ để khỏi suy diễn)

- Thời gian dựng + QA một Short thực tế (giờ): chưa thấy số đo trong `docs/pm`.
- `updated_at` có phản ánh ngày vào kho thật không: chưa kiểm.
- Script nào làm mới `data/channel_titles/*.json` và có nên chạy trước dedupe: chưa tìm thấy trong repo (chỉ thấy tiêu đề docstring `novelty.py:18`).
- Điều kiện/ToS từng nguồn miễn phí đề xuất (trừ những gì `demand-sources-research.md` đã nêu): chưa kiểm.
- Không đọc credentials, không gọi API nào trong audit này.
