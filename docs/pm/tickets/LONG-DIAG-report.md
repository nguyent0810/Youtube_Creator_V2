# YCV-cimp · Vì sao Long MIM và CK ít lượt xem

Số liệu Studio xuất 28/10/2026, tới 26/10. CK = Biểu Đồ Biết Nói `UCseQ5p0-e0_DW35M__d_oHg`. MIM = Mind in the Machine `UCb1WzhRnuTEsW8QhF7WdCQw`. Long public = slug `long-` trong `output/webauto/studio/upload_log_ck_mim.csv` có `publish_at` ≤ 26/10/2026 và có dòng trong Studio. Mỗi kênh 8 video. Với cả 16 video, cột views, watch_h, impressions, ctr, subs, avp của `lifetime`, `28d` và `365d` trong `videos.csv` trùng nhau. Tám Long CK = 238 views, MIM = 917 views. Kỳ 28 ngày, `raw/content_type__28d/table.csv` cột Views, Videos/Total: CK 240/36.550 (0,66%), MIM 920/63.901 (1,44%). Phần lệch là video dài cũ (mục 4).

## Ngưỡng phân loại (tự đặt)

Repo không có mốc CTR hay impressions cho Long. `docs/pm/2026-10-12-shorts-analysis.md` cũng ghi ngưỡng Short là tự đặt. Áp lên lifetime của 16 Long:

- **(a) ít hiển thị:** `Thumbnail impressions` < 1.000.
- **(b) CTR thấp:** impressions ≥ 1.000 và CTR < 2,0%. Mốc 2% nằm trên trung vị CTR Short 28d khi impressions ≥ 50: CK 1,78% (n=12), MIM 1,50% (n=16), cột `28d_ctr` của `videos.csv`.
- **(c) giữ chân kém:** Views ≥ 30 và `Average view duration` < 3:00. Mốc 3 phút neo vào đoạn mở trong `docs/codex/long-rules.md` (hook 0–30 giây, bối cảnh đến phút 2). Views < 30: không đủ dữ liệu cho (c). Một video có thể dính hai lớp.

## 1. Long đã public

Nguồn từng dòng: `raw/videos__lifetime/table.csv`. Impr = Thumbnail impressions. CTR = Thumbnail click-through rate (%). AVD = Average view duration. %xem = Average percentage viewed (%). Sub = Subscribers. Duration trong file là giây, bảng ghi phút:giây. Ngày = Video publish time, năm 2026. Traffic theo từng video: không có file.

### CK (238 views, 7.759 impressions, 1 sub)

| Đăng | Video | Dài | Impr | CTR | Views | AVD | %xem | Sub | Lớp |
|---|---|---|---|---|---|---|---|---|---|
| 10/10 | FgMmFrlBDmA | 10:52 | 525 | 0,76 | 10 | 1:41 | 15,56 | 0 | a |
| 14/10 | a45PR7ejNgk | 9:44 | 855 | 2,46 | 82 | 2:43 | 28,05 | 0 | a+c |
| 16/10 | rLhHogv4Dp8 | 7:27 | 438 | 1,6 | 12 | 4:12 | 56,43 | 0 | a |
| 17/10 | tD8htQq5Spk | 12:26 | 228 | 0 | 13 | 5:49 | 46,87 | 0 | a |
| 21/10 | xIfNPP1PLl8 | 8:03 | 1.843 | 0,71 | 23 | 4:55 | 61,27 | 0 | b |
| 23/10 | qvspAECVABY | 12:38 | 2.061 | 1,6 | 69 | 3:53 | 30,83 | 1 | b |
| 25/10 | An95weKtrPA | 8:03 | 1.412 | 0,64 | 15 | 3:29 | 43,32 | 0 | b |
| 26/10 | S_oMZt36W60 | 12:05 | 397 | 1,26 | 14 | 7:38 | 63,31 | 0 | a |

`tD8htQq5Spk` có CTR 0 và 13 views: 13 views không đi qua thumbnail. `S_oMZt36W60` đăng 26/10 13:00 UTC (`publish_at`), `age_days` = 2. Sáu trong tám Long CK có dưới 30 views: (c) chỉ chốt được ở `a45PR7ejNgk`, và AVD 2:43 chỉ dưới mốc 17 giây.

### MIM (917 views, 21.325 impressions, 4 sub)

| Đăng | Video | Dài | Impr | CTR | Views | AVD | %xem | Sub | Lớp |
|---|---|---|---|---|---|---|---|---|---|
| 12/10 | LeckrmjPkdI | 13:13 | 930 | 4,3 | 157 | 4:01 | 30,42 | 1 | a |
| 13/10 | hFOWYmGjrsA | 8:15 | 1.125 | 2,76 | 44 | 3:55 | 47,52 | 1 | — |
| 15/10 | 1cbPxR6WkVY | 6:44 | 353 | 0,85 | 8 | 1:36 | 23,99 | 0 | a |
| 19/10 | sP0ch8-NYec | 14:05 | 928 | 2,16 | 56 | 5:16 | 37,51 | 1 | a |
| 22/10 | CAYQtYA1NJA | 8:55 | 5.865 | 0,77 | 162 | 3:42 | 41,5 | 0 | b |
| 23/10 | sywk-F-yW7k | 13:06 | 7.834 | 1,51 | 404 | 4:37 | 35,33 | 0 | b |
| 25/10 | nbNu6xYtoYg | 20:07 | 1.616 | 1,24 | 45 | 6:10 | 30,7 | 1 | b |
| 26/10 | H9nlRjxfmPw | 13:26 | 2.674 | 0,6 | 41 | 5:49 | 43,31 | 0 | b |

`hFOWYmGjrsA` không chạm (a), (b) hay (c): 1.125 impressions sau 15 ngày, sát sàn. `H9nlRjxfmPw` đăng 26/10 13:00 UTC, `age_days` = 2, nhưng đã có 2.674 impressions nên CTR đọc được. `1cbPxR6WkVY` có 8 views: không đủ dữ liệu cho (c); AVD 1:36 chỉ là tín hiệu.

Slug ↔ id nằm ở `upload_log_ck_mim.csv`. Ngoài bảng: CK 17 slug `long-` có `publish_at` sau 26/10; MIM 20 slug và 4 bản cũ (`publish_at` trống, tiêu đề chờ xoá) không có trong Studio. `long-ck-b1-mua-hay-thue` (`pXKfIo_nyVM`, hẹn 30/10) vẫn có 1 view và 0,23 giờ trong `videos.csv`.

## 2. Gộp lớp

| Lớp | CK | MIM |
|---|---|---|
| (a) impressions < 1.000 | 5 video, trong đó a45 kèm (c) | 3 video: Leck, Flappy, ai-jobs |
| (b) đã ≥ 1.000 impressions, CTR < 2% | 3: nợ thẻ, vàng, trả góp | 4: captcha, voice, alphago, hallucinate |
| (c) đã đủ 30 views và AVD < 3:00 | 1: a45 (2:43) | 0 |
| Không chạm ngưỡng | 0 | 1: mã QR |

Ở cả 16 video, Views > impressions × CTR / 100. Ví dụ `sywk-F-yW7k`: 7.834 × 1,51% ≈ 118, thực tế 404 views. Không có cột clicks. Phần chênh không gán được cho một nguồn.

## 3. So với Short cùng kênh

`raw/content_type__28d/table.csv`:

| Kênh | Loại | Views | Giờ xem | AVD | %xem | Sub |
|---|---|---|---|---|---|---|
| CK | Shorts | 36.310 | 85,6235 | 0:21 | 76,33 | 25 |
| CK | Videos | 240 | 10,5122 | 4:14 | 40,33 | 1 |
| MIM | Shorts | 62.981 | 105,4934 | 0:17 | 62,41 | 33 |
| MIM | Videos | 920 | 33,8494 | 4:33 | 36,52 | 4 |

CTR không có trong bảng content type. Trung vị `28d_ctr` khi impressions ≥ 50, và trung vị `28d_avp` khi views ≥ 100, từ `videos.csv`:

| | CTR Short | n | %xem Short | n | CTR 8 Long | %xem 8 Long |
|---|---|---|---|---|---|---|
| CK | 1,78% | 12 | 62,98% | 44 | 1,01% | 45,10% |
| MIM | 1,50% | 16 | 57,68% | 72 | 1,375% | 36,42% |

%xem Long thấp hơn Short; AVD Long là vài phút, AVD Short là 17–21 giây. Trung vị `28d_impressions` của Short: CK 18 (n=53), MIM 20,5 (n=84). Cùng file, views/impressions 28d: Short CK 36.310/1.708 = 21,3 và MIM 62.982/2.974 = 21,2; tám Long CK 238/7.759 = 0,031 và MIM 917/21.325 = 0,043.

`raw/traffic_source__28d/table.csv` và `traffic_source__lifetime/table.csv` của cả hai kênh không có dòng `Shorts` hay `SHORTS_CONTENT_LINKS`. Có dòng `Shorts feed`: CK 28d 35.506 views, AVD 0:21; MIM 61.110 views, AVD 0:17. AVD này trùng AVD content type Shorts. Không tách được theo video. Trên file này, Long không nhận lượt xem từ Short.

## 4. Giờ xem Long trong 365 ngày, so với 4.000 giờ

Cột `365d_watch_h` của `videos.csv`, `format` = long (Duration > 180 giây). Kỳ 365d là cửa sổ xuất Studio. Không có `content_type__365d`. Đây là giờ xem Analytics, không phải bộ đếm Earn. Mốc 4.000 giờ xem long-form public / 12 tháng, và giờ Shorts feed không tính: `docs/pm/2026-10-13-ypp-monetization-research.md` mục 3, theo YouTube Help 72851. Cùng file: từ 01/02/2027 bậc đầy đủ với creator mới là 8.000 giờ.

| Kênh | format=long | Trừ video chưa public | Còn lại | % của 4.000 | Giờ Short, không cộng |
|---|---|---|---|---|---|
| CK | 11,0498 giờ (253 views, 1 sub) | 0,23 giờ của pXKfIo_nyVM | 10,8198 giờ | 0,27% | 85,6906 giờ Short |
| MIM | 37,7899 giờ (1.110 views, 4 sub) | 0 | 37,7899 giờ | 0,94% | 111,2663 giờ Short |

CK 10,8198 = 10,1335 giờ của 8 Long public + 0,6863 giờ video dài cũ đã có ngày đăng. MIM 37,7899 = 33,8044 giờ của 8 Long + 3,9855 giờ của 5 video dài cũ (một video Robot Framework, `KLjBMwB4JRM`, đăng 17/01/2025, chiếm 3,8119 giờ trong 365 ngày). Lifetime, content type Videos của MIM là 49,0328 giờ so với 45,7877 giờ format=long: 3,25 giờ thuộc video ≤ 180 giây mà YouTube không gọi là Shorts. Không có cách tách phần đó trong cửa sổ 365 ngày, nên không cộng vào mốc.

Tổng sub lifetime, dòng Total, `raw/content_type__lifetime/table.csv` cột Subscribers: CK 38, MIM 50.

Ba nguồn 28d có AVD dài (`traffic_source__28d`, cột Watch time (hours), Average view duration, Average percentage viewed):

| Nguồn 28d | CK views | CK giờ | CK AVD | CK %xem | MIM views | MIM giờ | MIM AVD | MIM %xem |
|---|---|---|---|---|---|---|---|---|
| Browse features | 132 | 2,2169 | 2:56 | 33,39 | 573 | 7,4509 | 3:33 | 29,34 |
| Suggested videos | 69 | 3,0824 | 2:45 | 27,41 | 236 | 13,3061 | 3:29 | 28,96 |
| External | 59 | 4,3998 | 5:44 | 87,73 | 107 | 11,4045 | 7:51 | 87,12 |

Browse + Suggested = 5,2993 giờ (CK) và 20,7570 giờ (MIM). External có %xem khoảng 87% trên vài chục đến hơn trăm views. Không có bảng giao với content type, nên không trừ External khỏi giờ Videos.

## 5. Ba giả thuyết

**1. Một số Long dừng dưới 1.000 impressions dù CTR ≥ 2% và AVD ≥ 3 phút.** Ủng hộ: `LeckrmjPkdI` 930 impressions, CTR 4,3%, AVD 4:01, sau 16 ngày vẫn 157 views; `sP0ch8-NYec` 928 impressions, CTR 2,16%, AVD 5:16, 56 views; `hFOWYmGjrsA` dừng ở 1.125 impressions sau 15 ngày dù CTR 2,76% và AVD 3:55. Phản bác: 8/16 Long đã có ≥ 1.000 impressions, gồm `sywk-F-yW7k` 7.834. Sub lifetime 38 và 50 là bối cảnh, file không chứng minh đó là nguyên nhân. Kiểm tra tới 11/11: với mỗi Long public đủ 7 ngày, đếm video có CTR ≥ 2% và AVD ≥ 3:00 nhưng impressions < 1.000.

**2. Long được đưa ra (≥ 1.000 impressions) thì CTR dưới 2%, nên tiêu đề hoặc thumbnail giới hạn views.** Ủng hộ: 7/8 video trong nhóm này có CTR < 2%. Thấp nhất `H9nlRjxfmPw` 0,6% trên 2.674 impressions; `CAYQtYA1NJA` 0,77% trên 5.865; `sywk-F-yW7k` 1,51% trên 7.834 mà vẫn là video nhiều views nhất (404). Phản bác: `LeckrmjPkdI` 4,3% và `hFOWYmGjrsA` 2,76% cho thấy có bài vượt 2%. Views còn cao hơn impressions × CTR, nên CTR không giải thích hết 404 hay 162 views. Kiểm tra: đổi một biến, tiêu đề hoặc thumbnail, trên đúng hai video đã public đó. Đo CTR sau khi có thêm ≥ 1.000 impressions. Lịch đã hẹn giữ nguyên ngày, tiêu đề và thumbnail (`docs/pm/2026-10-27-chien-luoc-long-45-ngay.md`, quyết định 27/10).

**3. AVD cả video đang được kéo lên bởi External; người đến từ Browse/Suggested ở sát hoặc dưới 3 phút.** Ủng hộ: chỉ 1/16 Long chạm (c). Bảy Long MIM có ≥ 30 views đều AVD ≥ 3:42. External 28d: CK 4,3998 giờ, AVD 5:44, %xem 87,73%; MIM 11,4045 giờ, AVD 7:51, %xem 87,12%. Phản bác: Browse và Suggested của MIM là 3:33 và 3:29, trên mốc 3 phút; của CK là 2:56 và 2:45. Đó là số cả kênh, không phải từng Long, và 6/8 Long CK chưa đủ 30 views để kết luận (c). Kiểm tra: xuất traffic source theo video cho `sywk-F-yW7k`, `CAYQtYA1NJA`, `LeckrmjPkdI`, `a45PR7ejNgk`. Nếu AVD của Browse < 3:00 tại video đã có ≥ 30 views từ Browse, giữ chân lạnh yếu. File này không có giữ chân 30 giây.

## Đề xuất cho 2 tuần tới

Không đổi lịch. Mỗi việc một chỉ số.

1. Ghi impressions, CTR và AVD lúc 24 giờ, 72 giờ và 7 ngày cho Long tới hạn, đúng mục đo trong chiến lược 45 ngày. Chỉ số: trong các Long đủ 7 ngày trước 11/11, bao nhiêu video có CTR ≥ 2% và AVD ≥ 3:00 nhưng impressions < 1.000.
2. Thử một biến trên `sywk-F-yW7k` (CTR 1,51%, 7.834 impressions) và `CAYQtYA1NJA` (CTR 0,77%, 5.865 impressions). Chỉ số: CTR trên ≥ 1.000 impressions phát sinh sau lần đổi, so với hai mức trên.
3. Xuất traffic source theo video cho bốn id ở giả thuyết 3. Chỉ số: views và AVD của Browse, Suggested, External, và views của dòng `Shorts` hoặc `SHORTS_CONTENT_LINKS` (ghi 0 nếu không có dòng).
