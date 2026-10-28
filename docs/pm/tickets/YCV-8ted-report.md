# Báo cáo YCV-8ted: Vì sao lượt xem CK 7 ngày giảm 78%?

**Nguồn dữ liệu (chốt đến 26/10/2026, xuất 28/10/2026):**
- `CK/`: `output/webauto/studio/UCseQ5p0-e0_DW35M__d_oHg/2026-10-28/` (`summary.md`, `summary.json`, `videos.csv`, `raw/<báo cáo>__<kỳ>/{table,chart}.csv`)
- `MIM/`: `output/webauto/studio/UCb1WzhRnuTEsW8QhF7WdCQw/2026-10-28/` (cùng cấu trúc)
- Lịch đăng & bối cảnh: `output/webauto/studio/upload_log_ck_mim.csv`, `docs/pm/2026-10-28-pilot-short-hook.md` (mục 1–3, 6, 8)

## 1. Mức giảm: Thời điểm, Short vs Long và so với MIM

Theo `summary.json` (`daily.28d.last_7d`, `prev_7d`, `change_7d_pct`) và `raw/content_type__28d/chart.csv` (cột `Date`, `Content type`, `Views`):

| Chỉ số / Phân tách | CK 13–19/10 (`prev_7d`) | CK 20–26/10 (`last_7d`) | Thay đổi CK | MIM 13–19/10 (`prev_7d`) | MIM 20–26/10 (`last_7d`) | Thay đổi MIM | Nguồn & cột |
|---|---:|---:|---:|---:|---:|---:|---|
| **Tổng Views** | 28.203 | 6.154 | **-22.049 (-78,2%)** | 35.799 | 21.586 | **-14.213 (-39,7%)** | `summary.json` (`daily.28d`) |
| **Giờ xem (`watch_h`)** | 72,6 | 19,8 | **-52,8h (-72,7%)** | 66,9 | 58,7 | **-8,2h (-12,3%)** | `summary.json` (`daily.28d`) |
| **Sub mới (`subs`)** | 18 | 7 | **-11 (-61,1%)** | 19 | 17 | **-2 (-10,5%)** | `summary.json` (`daily.28d`) |
| **Views Short** | 28.109 | 6.016 | **-22.093 (-78,6%)** | 35.676 | 20.796 | **-14.880 (-41,7%)** | `content_type__28d/chart.csv` (`Views`) |
| **Views Long (`Videos`)** | 94 | 138 | **+44 (+46,8%)** | 123 | 790 | **+667 (+542,3%)** | `content_type__28d/chart.csv` (`Views`) |
| **Trung vị view Short** | 573,0 (28d) | 3,0 (7d) | **-99,5%** (cả 52 bài) | 832,0 (28d) | 48,5 (7d) | **-94,2%** (cả 76 bài) | `summary.json` (`by_format.{28d,7d}`) |

**Diễn biến theo ngày** (`raw/daily__28d/table.csv` cột `Date`, `Views` & `raw/content_type__28d/chart.csv` cột `Views`):

| Ngày | 13/10 | 14/10 | 15/10 | 16/10 (Đỉnh) | 17/10 | 18/10 | 19/10 (Vách) | 20/10 (Đáy CK) | 21/10 | 22/10 | 23/10 | 24/10 | 25/10 | 26/10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **CK Tổng** | 2.702 | 5.052 | 6.451 | **6.498** | 4.099 | 2.709 | **692** | **320** | 595 | 1.181 | 1.282 | 1.498 | 740 | 538 |
| **CK Short** | 2.702 | 5.043 | 6.440 | **6.457** | 4.072 | 2.703 | **692** | **316** | 584 | 1.178 | 1.272 | 1.474 | 710 | 482 |
| **MIM Tổng** | 4.507 | 5.245 | 5.829 | **5.937** | 5.332 | 4.948 | 4.001 | 3.767 | **1.933** | 2.608 | 3.690 | 3.803 | 2.930 | 2.855 |

- **Ngày bắt đầu giảm:** Cả hai kênh đạt đỉnh ngày **16/10**. CK bắt đầu giảm từ **17–18/10** (-36,9% rồi -33,9%), **rơi thẳng đứng ngày 19/10** (còn 692 views, -74,5% so với 18/10) và chạm đáy **20/10** (320 views), sau đó hồi nhẹ lên 1.181–1.498 (22–24/10) rồi lùi về 538 (26/10). MIM giảm thoai thoải hơn, chạm đáy ngày 21/10 (1.933) rồi giữ mức 2.608–3.803.
- **Giảm ở Short hay Long:** 100% mức giảm của CK nằm ở **Short** (-22.093 views, -78,6%), trong khi **Long tăng +46,8%** (từ 94 lên 138 views, đóng góp 8,0/19,8 giờ xem 7d theo `summary.json` -> `by_format.7d.long`).

## 2. Nguồn lưu lượng (Traffic source)

- **Giới hạn kỳ xuất của bảng tổng hợp (`table.csv`):** Studio chỉ xuất `raw/traffic_source__28d/table.csv` và `raw/traffic_source__lifetime/table.csv` (không có `traffic_source__7d`), nên **không tách riêng được 7 ngày cho giờ xem (`Watch time`) và `% xem TB` (`AVP`)**.
- **Tách riêng 7 ngày về `Views`:** Dùng chuỗi ngày trong `raw/traffic_source__28d/chart.csv` (cột `Date`, `Traffic source`, `Views`) cộng 13–19/10 và 20–26/10 (khớp 100% tổng 28.203 và 6.154):

| Nguồn (`Traffic source`) | CK `28d` Views (%) | CK `lifetime` Views (%) | Chênh ngoài 28d | CK 13–19/10 (`chart.csv`) | CK 20–26/10 (`chart.csv`) | Chênh 7d (`Views` / %) | Tỷ trọng trong mức giảm |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Shorts feed** | 35.506 (97,1%) | 35.564 (95,8%) | 58 | 27.510 | 5.859 | **-21.651 (-78,7%)** | **98,20%** |
| **YouTube search** | 471 (1,3%) | 527 (1,4%) | 56 | 327 | 121 | **-206 (-63,0%)** | 0,93% |
| **Other YT features** | 142 (0,4%) | 162 (0,4%) | 20 | 113 | 15 | **-98 (-86,7%)** | 0,44% |
| **Channel pages** | 144 (0,4%) | 152 (0,4%) | 8 | 115 | 25 | **-90 (-78,3%)** | 0,41% |
| **Browse features** | 132 (0,4%) | 344 (0,9%) | 212 | 77 | 46 | **-31 (-40,3%)** | 0,14% |
| **Suggested videos** | 69 (0,2%) | 169 (0,5%) | 100 | 11 | 58 | **+47 (+427,3%)** | -0,21% (tăng) |
| **External + Khác** | 86 (0,2%) | 213 (0,6%) | 127 | 50 | 30 | **-20 (-40,0%)** | 0,09% |
| **Tổng cộng** | **36.550 (100%)** | **37.131 (100%)** | **581** | **28.203** | **6.154** | **-22.049 (-78,2%)** | **100,00%** |

- **Shorts feed mất nhiều nhất:** Mất **21.651 views (-78,7%)**, chiếm **98,2%** tổng lượt xem sụt giảm của kênh. Tìm kiếm giảm 206 views (-63,0%), Trang kênh giảm 90 views (-78,3%), trong khi Đề xuất (`Suggested videos`) tăng +47 views nhờ các bài Long mới.

## 3. Short mới (7–10 ngày gần nhất), views 3 ngày đầu và lịch `upload_log`

- **Short mới có được hiển thị không?** **Có.** Theo `CK/videos.csv` (cột `published`, `7d_views`, `28d_views`), cả **24 Short đăng từ 18–26/10** (tuổi 2–10 ngày) và 1 Short ngày 27/10 (`8I_pkrLc9sA`, 93 views) đều phát sinh view (từ **51 đến 1.026 views**, không bài nào 0 view). Theo `2026-10-28-pilot-short-hook.md` (mục 2–3), **97–98% view** của nhóm 18–25/10 vẫn đến từ `Shorts feed`. *(Lưu ý: cột `impressions` trong `videos.csv` là hiển thị thumbnail ở tìm kiếm/duyệt xem, không phải lượt hiển thị trên Shorts feed).*
- **So views 3 ngày đầu với các Short đăng 14–20/10:**
  - Theo `raw/videos__28d/chart.csv` và `raw/videos__7d/chart.csv` (cột `Date`, `Views`), **92%–100% tổng view của một Short CK rơi vào đúng 3 ngày đầu** rồi tắt: nhóm 13–16/10 có `WpC17_WurUs` đạt **3.159/3.210** (98,4%), `_aIZGZ-uhI0` đạt **2.095/2.264** (92,5%), `bvu1mv8-_X4` đạt **1.270/1.273** (99,8%), `rcNHdVdPMCo` đạt **1.332/1.358** (98,1%), `ZLbrN-CXnsQ` đạt **1.192/1.447** (82,4%) trong 3 ngày đầu; nhóm 22–25/10 có `Rj9NAGSMP34` **927/927** (100%), `JGuGew0Lyws` **899/912** (98,6%), `utTm1-rDRfw` **865/869** (99,5%), `dSuFp1rtMrU` **694/694** (100%), `Gy31ReYpvIM` **570/573** (99,5%).

| Giai đoạn đăng (`CK/videos.csv`) | Số Short | Tổng `28d_views` | Tổng `7d_views` (20–26/10) | TB `28d_views`/bài | Trung vị `28d_views` | Min – Max | Số bài ≥ 1.000 views |
|---|---:|---:|---:|---:|---:|---:|---:|
| **14–17/10** (`age_days` 11–14) | 20 | 21.032 | 121 (99,4% ở 14–19/10) | 1.051,6 | **1.187,0** | 11 – 3.210 | 13/20 (65%) |
| **18–20/10** (`age_days` 8–10) | 11 | 2.499 | 267 (89,3% ở 18–19/10) | 227,2 | **189,0** | 51 – 1.026 | 1/11 (9%) |
| **Gộp 14–20/10** (`age_days` 8–14) | **31** | **23.531** | **388** | **759,1** | **966,0** | **11 – 3.210** | **14/31 (45%)** |
| **21–25/10** (`age_days` 3–7, đủ 2–3 ngày) | 11 | 5.338 | 5.338 (100% ở 21–26/10) | 485,3 | **322,0** | 142 – 927 | 0/11 (5 bài 573–927) |
| **26–27/10** (`age_days` 1–2, chưa đủ 3 ngày) | 3 | 276 | 276 | 92,0 | **93,0** | 79 – 104 | 0/3 |

- **Lịch đăng theo `upload_log_ck_mim.csv` (cột `channel`, `slug`, `publish_at` UTC) và hiện tượng đăng dồn:**

| Giai đoạn (`publish_at` UTC) | CK: Số bài/ngày (Short + Long) | Tổng CK | MIM: Số bài/ngày (Short + Long) | Tổng MIM |
|---|---|---:|---|---:|
| **08–12/10** (5 ngày đầu) | 09/10: 1S · 10/10: 1L · 11/10: 1S · 12/10: 0 | 2S + 1L | 08–11/10: 1S/ngày · 12/10: 2S + 1L | 6S + 1L |
| **13–19/10** (`prev_7d`) | **5 Short/ngày** cả 7 ngày + 1 Long vào 14, 16, 17/10 (**5–6 bài/ngày**) | **35S + 3L** | **5 Short/ngày** cả 7 ngày + 1 Long vào 13, 15, 19/10 | **35S + 3L** |
| **20–26/10** (`last_7d`) | 20/10: **1S** · 21, 23, 26/10: **2S+1L** · 22, 24/10: **2S** · 25/10: **3S+1L** | **14S + 4L** | **5 Short/ngày** cả 7 ngày + 1 Long vào 22, 23, 25, 26/10 | **35S + 4L** |
| **27–28/10** | 27/10: 2S · 28/10: 2S + 1L | 4S + 1L | 27/10: 3S · 28/10: 4S + 1L | 7S + 1L |

  1. **Giảm 60% số Short đăng mới ở CK:** Tuần 13–19/10 CK đăng **35 Short** (5 bài/ngày), nhưng tuần 20–26/10 chỉ đăng **14 Short** (trung bình 2 bài/ngày; riêng 20/10 chỉ 1 bài), trong khi MIM giữ nguyên **35 Short/tuần**.
  2. **Đăng dồn theo giờ và theo cụm chủ đề:** Giai đoạn 13–19/10, CK đăng **5–6 bài/ngày** (khung `10:30Z–15:00Z` tức 17:30–22:00 VN dồn 3–4 bài cách nhau chỉ 1,5–2 giờ); ngày 25/10 đăng dồn 4 bài (3S+1L). Về nội dung, ngày **16–17/10** dồn 8 Short về *Lãi kép / Mua đều*, và ngày **18–19/10** dồn **8/10 Short** về *Nợ thẻ tín dụng / Trả góp 0%* (trung vị cụm này tụt xuống **134,5 views**).

## 4. Bài kéo view: Đợt viral đầu tháng hay trở về bình thường?

Trích `CK/videos.csv` (cột `age_days`, `28d_views`, `7d_views`) và `CK/summary.json` (`by_age`, `distribution`):
- **Nhóm tuổi `8-28d` (42 video, đăng 09–20/10) giữ 84,3% (30.813/36.550) views 28d**, nhưng sang `7d_views` (20–26/10) chỉ còn **382 views** (6,2% của 6.154). Ngược lại, **nhóm `0-7d` (18 video, đăng 21–27/10) tạo ra 5.735 views**, chiếm **93,2%** tổng view 7 ngày qua.
- **Không phải chỉ "vài bài viral" kéo tuần trước:** Trong `summary.json` (`distribution`), 10% video đứng đầu chỉ chiếm **29,6%** view 28d (Top 1 `WpC17_WurUs` 3.210 views = 8,8%; Top 2 `_aIZGZ-uhI0` 2.264 views = 6,2%). Trong 25 Short đăng 13–17/10, có tới **16/25 bài đạt 1.076–3.210 views** (tổng 26.196 views 28d, chỉ còn 128 views ở 7d). Tức tuần 13–19/10 là **mặt bằng phân phối cao đồng loạt (~1.184 views/bài) cộng với tần suất đăng 5 Short/ngày**.
- **Phép tách nhân tử mức giảm -78,6% của Short CK (từ 28.109 xuống 6.016 views, còn 21,4%):**
  $$\text{Tỷ lệ view tuần này / tuần trước} \approx 0,40 \text{ (số Short mới giảm từ 35 xuống 14)} \times 0,53 \text{ (view TB/bài giảm từ 803 xuống 425)} = 21,2\% \text{ (-78,8\%)}$$

## 5. Xếp hạng 5 giả thuyết theo bằng chứng

| Hạng & Giả thuyết | Số liệu ủng hộ (File & cột) | Số liệu phản bác (File & cột) | Cần thêm gì để kiểm chứng |
|---|---|---|---|
| **1. Lịch đăng (`upload_log`: cắt 60% số bài & dồn lịch 13–19/10)** | - `upload_log_ck_mim.csv` (`publish_at`): CK giảm từ **35 Short** (13–19/10, 5S/ngày) xuống **14 Short** (20–26/10, 1–3S/ngày) = **-60% số bài**.<br>- Vì 92–100% view nằm ở 3 ngày đầu (`videos__28d/chart.csv`), giảm 60% số bài mới trực tiếp làm mất ~60% tổng view tuần.<br>- Đăng 5–6 bài/ngày (13–19/10) trùng khớp thời điểm rơi gãy ngày 19/10. | - `upload_log_ck_mim.csv` & `MIM/summary.json` (`daily.28d`): MIM giữ nguyên **35 Short/tuần** (5S/ngày) nhưng tổng view 7d vẫn giảm **-39,7%** (35.799 → 21.586). Lịch đăng không giải thích được phần giảm view trên từng bài. | - Số `Shown in feed` theo từng khung giờ đăng (`00:00Z`–`15:00Z`) trong Studio để kiểm tra hiện tượng tự cạnh tranh khi đăng 5 bài/ngày. |
| **2. Phân phối Short mới giảm (Hạ trần seed từ vách 18/10)** | - `CK/videos.csv` (`28d_views`): Trung vị Short giảm từ **1.184** (25 bài 13–17/10, 16 bài >1k) xuống **189** (18–20/10) và **322** (21–25/10, 0 bài >1k).<br>- Xảy ra đồng thời ở MIM từ 18/10: trung vị giảm **1.215 → 722** (`pilot-short-hook.md` mục 2).<br>- Giữ chân không sập: EVR proxy CK chỉ giảm 28% → 26%; nhiều bài `28d_avp` >118–189% (`-97RNTK2rZc`, `3NG1EmJmgzQ`) vẫn chỉ đạt 139–287 views. | - `CK/videos.csv` (`7d_views`): Giai đoạn 21–25/10 vẫn có **5/11 Short đạt 573–927 views**, cao hơn hẳn đáy 18–20/10.<br>- `pilot-short-hook.md` (mục 2–3): 97–98% view vẫn từ `Shorts feed`. | - Chỉ số Studio chưa xuất được: **Lượt hiển thị trên feed (`Shown in feed`)** và **Xem / lướt qua (`Stayed to watch %`)** trước và sau 18/10. |
| **3. Hết đợt viral / vòng đời Short ngắn** | - `CK/videos.csv` (`28d_views`, `7d_views`): Top 2 bài (`WpC17_WurUs` 3.210, `_aIZGZ-uhI0` 2.264) đóng góp 5.474 views đợt trước nhưng chỉ còn **37 views** trong 7d; toàn bộ 38 Short đăng ≤20/10 chỉ còn **382 views** trong 7d.<br>- `videos__28d/chart.csv`: 92–100% view dồn vào 3 ngày đầu. | - `CK/summary.json` (`distribution`): Top 10% video chỉ giữ **29,6%** view 28d; tuần 13–17/10 có tới **16/25 bài >1.000 views** (mặt bằng chung cao, không phải ăn may 1–2 bài cá biệt). | - Theo dõi `chart.csv` của các bài ~900 views (`Rj9NAGSMP34`, `JGuGew0Lyws`) sau 14 ngày xem có nhịp phân phối thứ hai từ Search không. |
| **4. Đổi chủ đề hoặc khuôn** | - `CK/videos.csv` & `pilot-short-hook.md` (mục 1, 3): Cụm 8/10 bài *Nợ thẻ/Trả góp* dồn ngày 18–19/10 có trung vị chỉ **134,5 views**, trong khi 2 bài khuôn *Bảng tự dò* (23/10: `JGuGew0Lyws` 912, `Gy31ReYpvIM` 573) gấp **2,8× và 1,8×** trung vị cùng kỳ (322). | - Cùng ngày 17–19/10, chủ đề *Mua đều* (`D9FPfmMxJlI` 78 views) và *Quỹ khẩn cấp* (`IgaHaMjujlw` 51 views) cũng tụt sâu dù bài cùng chủ đề ngày 15/10 và 18/10 đạt 1.273 và 1.026 views.<br>- EVR proxy cụm nợ/trả góp vẫn đạt 26% (bằng mức chung). | - Tách biến chủ đề khỏi biến đăng dồn bằng `Shown in feed` và `Stayed to watch` trong Studio của cụm 18–19/10, và kết quả pilot 3 cặp A/B. |
| **5. Hạn chế hoặc giới hạn upload** | - `CK/videos.csv` & `MIM/videos.csv` (`28d_views`): Có 2 bài cá biệt view cực thấp và tỷ lệ feed thấp (`o75eN6_1enI` 11 views, 45% feed; `AVDmUn0nEXU` 8 views, 12% feed). | - `upload_log_ck_mim.csv` (`state`): Toàn bộ hàng chờ đến 04/12 đều `done` (không bị chặn upload).<br>- `pilot-short-hook.md` (mục 3): API xác nhận 22/22 bài CK <300 views đều `public, processed, embeddable`; Long mới vẫn nhận 1.412–2.061 `7d_impressions` (`CK/videos.csv`). | - Kiểm trực tiếp cột **Restrictions** trên giao diện Studio cho 22 bài CK <300 views (ưu tiên `o75eN6_1enI` và `AVDmUn0nEXU`). |

## 6. Ảnh hưởng tới pilot CK 07–12/11: Mốc so sánh nào còn dùng được?

1. **Các mốc phải loại bỏ:**
   - **Không dùng trung vị cả kỳ 28d (573 views trong `summary.json` / 723 views trong brief) và mốc 13–17/10 (1.184 views):** Đây là mức phân phối giai đoạn đầu kênh trước vách 18/10.
   - **Không dùng tổng view tuần của kênh:** Lịch pilot CK 07–12/11 chỉ đăng **1 Short/ngày** (6 bài/6 ngày, hàng chờ trống từ 07/11 theo `upload_log_ck_mim.csv`), chỉ bằng 50% sản lượng tuần 21–26/10 (2S/ngày) và 20% tuần 13–19/10 (5S/ngày).
2. **Các mốc so sánh còn dùng được cho pilot CK 07–12/11:**
   - **So sánh nội bộ theo cặp đối chứng A/B (chính):** Đọc trực tiếp **Hook B vs Hook A trong từng cặp (3 cặp = 6 bài, thứ tự B-A-A-B-B-A)** ở mốc **48 giờ và 7 ngày** sau bài cuối (do 92–100% view Short CK hoàn tất trong 3 ngày đầu).
   - **Chỉ số quyết định:** Tỷ lệ **"Xem / lướt qua" (`Stayed to watch %`)** trong Studio (hoặc `EVR proxy` baseline **26%** khi chưa mở được Studio, ngưỡng thắng: B hơn A **≥ 5 điểm** ở ít nhất 2/3 cặp), kèm `% xem TB` (baseline sau 18/10 là **47%** theo API / trung vị **50,5%** của 11 bài 21–25/10 trong `CK/videos.csv`), `sub / 1.000 views` (baseline 7d **1,0** theo `summary.json`), và lượt click sang Long qua "Video liên quan".
   - **Baseline mặt bằng view mỗi bài (Bước 0 kiểm tra phân phối):** Dùng trung vị của **11 Short đăng 21–25/10 là 322 views/bài** (khoảng tứ phân vị **183 – 869 views**, hoặc trung vị **229 views** của 23 Short 18–25/10 theo `pilot-short-hook.md` mục 2) và yêu cầu tỷ lệ view từ `Shorts feed` **≥ 80%**.
   - **Lưu ý biến nhiễu lịch đăng:** Trong `upload_log_ck_mim.csv`, có 3 bài Long CK lên sóng lúc `13:00Z` (20:00 VN, cách Short pilot 1 giờ) vào ngày **08/11** (`7K1zP3ZdabQ`), **09/11** (`Ss_unzSu7DY` — đều rơi vào ngày **Hook A**) và **11/11** (`dQ3HLAXf12U` — rơi vào ngày **Hook B**); cần ghi nhận khi đọc kết quả từng cặp.
