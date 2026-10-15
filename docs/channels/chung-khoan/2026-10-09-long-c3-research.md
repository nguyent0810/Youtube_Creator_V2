# Hồ sơ dữ kiện — Video dài C3 ("Chứng khoán từ số 0", bài 3): "Biểu đồ nến: một cây nến kể gì về một phiên?"

Ngày lập: 09/10/2026. Phạm vi: **đọc biểu đồ nến cho người mới hoàn toàn** — bốn giá O/H/L/C → một cây nến; thân và bóng; màu nến so
với màu bảng giá; đọc một tuần VN-Index thật (09–13/03/2026, gọi lại C2); khung thời gian ngày/tuần; và **điều nến KHÔNG nói được** —
kênh tự đếm các mẫu nến phổ biến trên VN-Index 2018–2026 so với tỉ lệ nền, đối chiếu nghiên cứu học thuật. Gộp tập 5 (một phần), 6, 7
của giáo trình (`2026-10-06-research.md` mục 3). Mong muốn gốc của chủ kênh: dạy MA, nến, Ichimoku sao cho ai cũng hiểu, không khô như
sách — bài này là viên gạch "nến"; MA ở bài sau.

Luật cứng (`2026-10-06-positioning.md` mục 1) áp dụng: **giáo dục, không khuyến nghị, không dự báo, không tín hiệu giao dịch, không nêu
tên mã / công ty chứng khoán / ứng dụng.** Mọi phép đếm là tần suất **quá khứ** trên **chỉ số** (không mua bán trực tiếp được), chưa tính
phí/thuế.

**Nhãn:** **[bằng chứng]** = đã mở trang/tệp gốc · **[SECONDARY]** = báo chí/tóm tắt qua công cụ tìm kiếm/trang thứ cấp, hoặc trang chặn
truy cập · **[CHƯA KIỂM]** · **[kênh tự tính]** = từ `data/ck/vnindex_1d.csv` bằng `data/long/ck-c3-bieu-do-nen/analysis.py` (tái lập
được, kết quả ở `results.json` cùng thư mục) · *[suy luận]* = diễn giải của kênh. `[n]` = nguồn cuối file; `[C2-n]` = nguồn trong hồ
sơ C2 (`2026-10-07-long-c2-research.md`).

> **Lưu ý mạng khi lập hồ sơ:** nhiều trang (vndirect.com.vn, pinetree.vn, bsc.com.vn, sagepub, cxoadvisory) trả lỗi DNS/403 trong
> phiên làm việc → các số báo chí dưới đây phần lớn là **[SECONDARY — tóm tắt qua công cụ tìm kiếm]**, trừ Thời báo Tài chính 10/03 (đã
> mở). Fact-checker nên mở lại.

## Tóm tắt — các con số chính

| # | Dữ kiện | Nhãn | Nguồn |
|---|---|---|---|
| 1 | Một cây nến = 4 giá của một phiên: mở cửa (O), cao nhất (H), thấp nhất (L), đóng cửa (C). Thân = O→C; bóng (râu) = tới H và L | kiến thức chuẩn | [1] |
| 2 | Steve Nison đưa nến sang phương Tây (sách 1991); sau này (*Beyond Candlesticks*) viết "khó có chuyện Homma dùng nến", nhiều khả năng ra đời đầu thời Minh Trị (cuối thế kỷ 19) | [SECONDARY — Wikipedia trích Nison] | [1] |
| 3 | Màu nến (thông lệ biểu đồ): đóng > mở = xanh/rỗng, đóng < mở = đỏ/đặc. Màu **bảng giá** VN: so với **tham chiếu** (= đóng cửa phiên trước); vàng tham chiếu, tím trần, xanh lơ sàn | [1] + [C2-19, SECONDARY] | |
| 4 | **09/03/2026**: O 1.757,73 = H · L 1.650,75 · C 1.652,79 (−115,05; −6,51%) — nến đỏ dài, không bóng trên | [kênh tự tính] khớp báo (C2) | [C2-7][C2-8] |
| 5 | **10/03**: **O mâu thuẫn giữa nguồn** — 1.664,52 (VCI, nguồn thứ ba) vs 1.697,87 (CafeF; bản tin thị trường "gap tăng 45.08") → màu nến và "bóng trên 3,27× thân" (chỉ đúng với O của VCI) **không dùng**. Chắc chắn: H 1.716,62 · L 1.651,29 · C 1.676,73 (+23,94; +1,45%) → **H − C ≈ 39,9 điểm**; báo: "phục hồi ngay đầu phiên… lên vùng giá 1.720 điểm sau đó chịu áp lực rung lắc" | [kênh tự tính] + [bằng chứng] | [9] |
| 6 | **11/03**: O 1.675,87 ≈ L · C 1.728,34 ≈ H (+3,08%) — nến xanh dài gần như không bóng | [kênh tự tính] | |
| 7 | **13/03**: O 1.697,72 · H 1.716,75 · L 1.688,67 · C 1.696,24 (−13,37; −0,78%) — **doji** (thân 1,48 / biên 28,08 = 5,3%) | [kênh tự tính] khớp báo | [11] |
| 8 | **Nến tuần 09–13/03**: O 1.757,73 · H 1.757,73 · L 1.650,75 · C 1.696,24 → −4,05% so với đóng cửa 06/03; thân đỏ, bóng dưới 45,5 điểm | [kênh tự tính] | |
| 9 | **24/03**: tham chiếu 1.591,17 (đóng cửa thấp nhất 2026) · O 1.626,34 · C 1.614,77 → **chỉ số +23,60 (+1,48%) nhưng nến ĐỎ** | [kênh tự tính] + báo (đóng cửa) | [12][13] |
| 10 | Nến đỏ mà chỉ số tăng: 216 phiên; nến xanh mà chỉ số giảm: 86 → **15,2%** số phiên (≈ 1/7) | [kênh tự tính] | |
| 11 | 2026 (01/01–06/10): **186 nến ngày, 39 nến tuần** | [kênh tự tính] | |
| 12 | **Tỉ lệ nền:** ngày bất kỳ → chỉ số cao hơn sau 5 phiên **58,5%**, sau 20 phiên **59,2%** (VN-Index 996,12 → 1.759,08, +76,6% trong giai đoạn) | [kênh tự tính] | |
| 13 | **Cây búa đúng sách**: 35 lần; cao hơn sau 5 phiên **51,4%** (nền cùng bối cảnh 56,3%), sau 20 phiên **55,9%** (59,7%) | [kênh tự tính] | |
| 14 | **Doji**: 201 lần; đổi hướng 5 phiên **42,8%** vs ngày thường **45,0%** | [kênh tự tính] | |
| 15 | **Ba chàng lính trắng đúng sách**: **5 lần** trong 8 năm, **0 lần** từ 2023 | [kênh tự tính] | |
| 16 | Học thuật: Mỹ (DJIA 1992–2002), Nhật (1975–2004), Thái Lan (SET50 2006–2016), Việt Nam (2013–2018): **không thấy giá trị/không dự báo được**; Đài Loan, Trung Quốc, S&P 500 1992–96: **vài mẫu có giá trị trong vài điều kiện** | [bằng chứng] / [SECONDARY] | [2]–[8][14][15] |

**Câu chốt cho kịch bản** *[suy luận]*: một cây nến là **biên bản** của một phiên đã qua — rất giỏi kể ai thắng, giằng co ra sao; nó
**không phải lời tiên tri**. Trên chính VN-Index 8 năm, các mẫu "báo đáy / báo đảo chiều" quen tên không làm tốt hơn một ngày bất kỳ;
và mốc để so **không phải 50%** mà là ~59% (vì chỉ số đi lên trong giai đoạn đo).

---

## 1. Một cây nến là gì

- **Bốn giá** của một khoảng thời gian (phiên, tuần, giờ…): mở cửa, cao nhất, thấp nhất, đóng cửa (OHLC). **Thân** = khoảng giữa mở và
  đóng cửa; **bóng / râu** (shadow, wick) = đường mảnh tới giá cao nhất và thấp nhất [1].
- **Biểu đồ đường** trên báo thường chỉ nối **giá đóng cửa** — mất ba giá còn lại *[suy luận phổ thông; C1/C2 dùng đường đóng cửa]*.
- **Phép so sánh cho người mới** *[suy luận]*: nhiệt độ một ngày — sáng mở cửa, lúc nóng nhất, lúc mát nhất, tối về. Chỉ ghi nhiệt độ tối
  = biểu đồ đường; ghi đủ bốn = cây nến. (Giáo trình gốc đề xuất "biên bản trận đấu"; nhiệt độ dễ hơn vì "tỉ số lúc bắt đầu" luôn 0–0.)
- **Nguồn gốc:** thường được kể là do Munehisa Homma (thương nhân gạo, thế kỷ 18) nghĩ ra. Wikipedia trích Nison (*Beyond
  Candlesticks*): "based on my research, it is unlikely that Homma used candle charts… more likely… developed in the early part of the
  Meiji period in Japan (in the late 1800s)" [1] [SECONDARY — chưa mở sách]. Kịch bản dùng như **motif "chuyện đẹp ≠ chuyện thật"**.
- **Tên mẫu** (Việt hoá phổ biến): cây búa (hammer), doji, ba chàng lính trắng (three white soldiers), nhấn chìm tăng (bullish
  engulfing), sao băng (shooting star), ba con quạ đen (three black crows).

## 2. Màu: nến vs bảng giá

- **Màu nến** (thông lệ biểu đồ): đóng cửa ≥ mở cửa → xanh (hoặc thân rỗng); đóng < mở → đỏ (hoặc thân đặc) [1]. Cảnh `candles` của
  engine cũng tô theo `close >= open` (`chart.js`, `B.candles`).
- **Màu bảng giá VN**: theo **giá tham chiếu** = giá đóng cửa ngày giao dịch gần nhất (QĐ 22/QĐ-HĐTV Điều 31 khoản 2, C2): xanh lá tăng,
  đỏ giảm, vàng = tham chiếu, tím = trần, xanh lơ = sàn [C2-19, SECONDARY — quy ước hiển thị, không phải quy định].
- **Hai mốc khác nhau → có ngày lệch màu.** Kênh tự đếm (1.990 phiên hợp lệ có phiên trước): nến đỏ mà chỉ số tăng **216**, nến xanh mà
  chỉ số giảm **86** → **302 phiên = 15,2%**. Lệch về phía "nến đỏ mà tăng" nhiều hơn vì VN-Index hay **mở cửa cao hơn** đóng cửa hôm
  trước (gap trung vị +0,08%, 75% phân vị +0,32%) rồi trôi xuống.
- **Ví dụ 2026** (`results.json → colour.examples_2026_red_up`): 12/01 (+0,50%), 27/02, 18/03, **24/03 (+1,48%)**, **01/04 (+1,70%)**,
  07/04, 10/04, 09/06, 15–16/06, 23/06, 20/08, 25/08, 28/08. Nến xanh mà giảm: 21/01, 30/03, 11/06, 17/06, 24/07, 03/09.
- **Chưa kiểm:** ở Trung Quốc đại lục, quy ước màu ngược (đỏ = tăng) — *không dùng trong lời đọc* vì chưa có nguồn mở được.

## 3. Tuần 09–13/03/2026 và ngày 24/03 — dữ liệu + đối chiếu báo chí

| Phiên | O | H | L | C | ± so hôm trước | Thân / biên | Bóng trên / dưới | Đọc *[suy luận]* |
|---|---|---|---|---|---|---|---|---|
| 06/03 (T6) | 1.801,08 | 1.807,31 | 1.767,84 | 1.767,84 | −2,25% | 84% | 6,2 / 0 | (tham chiếu tuần) |
| **09/03 (T2)** | 1.757,73 | 1.757,73 | 1.650,75 | 1.652,79 | −6,51% | 98% | 0 / 2,0 | Bên bán thắng trọn phiên |
| **10/03 (T3)** | 1.664,52 *(VCI; CafeF 1.697,87 — mâu thuẫn)* | 1.716,62 | 1.651,29 | 1.676,73 | +1,45% | 19% (VCI) | 39,9 / 13,2 (VCI) | Bị đẩy lùi từ trên cao (H − C 39,9); màu nến phụ thuộc nguồn |
| **11/03 (T4)** | 1.675,87 | 1.729,67 | 1.675,17 | 1.728,34 | +3,08% | 96% | 1,3 / 0,7 | Bên mua giữ tới cuối |
| **12/03 (T5)** | 1.716,62 | 1.725,52 | 1.701,59 | 1.709,61 | −1,08% | 29% | 8,9 / 8,0 | Mở thấp hơn đóng hôm trước, đỏ nhỏ |
| **13/03 (T6)** | 1.697,72 | 1.716,75 | 1.688,67 | 1.696,24 | −0,78% | **5,3%** | 19,0 / 7,6 | **Doji** |
| Tuần 09–13/03 | 1.757,73 | 1.757,73 | 1.650,75 | 1.696,24 | −4,05% (vs 06/03) | 57% | 0 / 45,5 | Tuần giảm, có hồi từ đáy |
| 23/03 (T2) | 1.630,11 | 1.636,27 | 1.586,44 | **1.591,17** | −3,44% | — | — | Đóng cửa (và đáy trong phiên) thấp nhất 2026 tới 06/10 |
| **24/03 (T3)** | **1.626,34** | 1.630,63 | 1.602,92 | **1.614,77** | **+1,48%** | — | — | **Nến đỏ, chỉ số tăng** |

**Đối chiếu báo chí** (retro 2, quy trình mục 1: ≥ 3 mốc):
1. 10/03 đóng cửa **1.676,73, +23,94** — Thời báo Tài chính [9] **[bằng chứng]** ✓ (báo ghi +1,46%; kênh +1,45% — làm tròn).
2. 10/03 **đỉnh trong phiên**: báo "lên vùng giá 1.720 điểm sau đó chịu áp lực rung lắc" [9] vs H 1.716,62 ✓ (xác nhận bóng trên dài).
3. 10/03 khối lượng: báo 1.539,91 triệu cp [10, SECONDARY] vs dữ liệu 1.537,51 triệu (lệch 0,16% — có thể do phạm vi khớp lệnh/thoả thuận).
4. 13/03 đóng cửa **1.696,24, −13,37 (−0,78%)** [11, SECONDARY] ✓.
5. 24/03 đóng cửa **1.614,77, +23,60 (+1,48%)**, 273 tăng / 59 giảm [12][13, SECONDARY] ✓. "Mở cửa trong sắc xanh" [13, SECONDARY]
   — mức mở 1.626,34: đã xác nhận ở mục 9 dưới đây (fact-check).
6. 09/03 (C2): đóng cửa, −115,05, KL 1,38 tỷ cp ✓ [C2-7][C2-8].
7. *(Fact-check 09/10)* 10/03: VnExpress "có thời điểm VN-Index tăng hơn 63 điểm, đạt 1.715 điểm" [16]; Công Luận "vượt mốc 1.716" [17]
   → đỉnh trong phiên ✓. Bản tin PDF 10/03 của một CTCK ghi đóng cửa "1.672,27, +19,48" — **sai** (ngược 4 nguồn khác), không dùng.
   Giá mở 10/03: VCI 1.664,52 vs CafeF 1.697,87 (bản tin thị trường "gap tăng mạnh 45.08") — **chưa giải quyết**.
8. *(Fact-check 09/10)* 13/03: Nhân Dân "giảm 13,37 điểm (-0,78%), xuống mức 1.696,24 điểm" [18] ✓; gap mở −11,89 khớp bản tin.
9. *(Fact-check 09/10)* 24/03: Người Lao Động — phiên sáng +31,52 lên 1.622,69, đóng cửa 1.614,77 (+23,60) [19]; Vietnambiz "VN-Index
   hồi phục hơn 30 điểm đầu phiên" [20]; bản tin thị trường "gap tăng mạnh 35.17" = O 1.626,34 ✓ (3 nguồn dữ liệu cùng ghi).

**Cảnh hẹn — sau cây doji 13/03:** 20/03 (5 phiên sau) C 1.647,81 → **−2,86%**; 23/03 C 1.591,17 (thấp nhất năm); 10/04 (20 phiên sau)
C 1.750,00 → **+3,17%**. Cùng một cây nến, "báo giảm" hay "báo tăng" đều tìm được bằng chứng khi nhìn lại *[suy luận]*.

## 4. Kênh tự tính — cách làm (tái lập: `python data/long/ck-c3-bieu-do-nen/analysis.py`)

**Dữ liệu:** `data/ck/vnindex_1d.csv` (vnstock/VCI), **08/10/2018 → 06/10/2026, 1.995 phiên**. Có 13 khoảng nghỉ > 4 ngày (Tết, lễ) — bình
thường. **4 nến lỗi** (H < max(O, C) hoặc L > min(O, C)): 24, 25, 26/06/2019 (giá mở đứng yên 949,48) và 23/08/2021 → loại khỏi việc
nhận diện mẫu, vẫn dùng giá đóng cửa.

**Ký hiệu:** R = H − L; B = |C − O|; U = H − max(O, C); D = min(O, C) − L.

**Định nghĩa mẫu** (đơn giản hoá từ mô tả phổ thông — Nison; định nghĩa định lượng kiểu Marshall, Young & Rose 2006 [2] dùng xu hướng
trước tín hiệu):
- **Bối cảnh "vừa giảm"**: C(t−1) < C(t−6) (5 phiên trước tín hiệu đi xuống); "vừa tăng": ngược lại. Độ nhạy: "dưới MA10" (C(t−1) < SMA10(t−1)).
- **Doji**: B ≤ 0,1·R.
- **Cây búa**: B > 0, D ≥ 2·B, U ≤ 0,1·R; **đúng sách** = thêm "vừa giảm". Độ nhạy: U ≤ B (lỏng hơn).
- **Ba chàng lính trắng**: 3 nến xanh liền, đóng cửa cao dần, mỗi nến mở **trong thân** nến trước (O(t−1) ≤ O(t) ≤ C(t−1)), bóng trên ≤ 0,3·R;
  **đúng sách** = thêm "vừa giảm" trước nến đầu. Độ nhạy "ba nến xanh liền" = bỏ điều kiện mở trong thân và bối cảnh.
- **Nhấn chìm tăng**: hôm trước đỏ, hôm nay xanh, O(t) ≤ C(t−1), C(t) ≥ O(t−1), vừa giảm.
- **Sao băng** (đối xứng của búa, vừa tăng) và **ba con quạ đen** (đối xứng) — đo % lần **thấp hơn**.
- **Nến dài**: B ≥ 2 × trung vị B của 20 phiên trước.

**Đo:** lợi suất C(t+h)/C(t) − 1, h = 5 và 20 phiên (tín hiệu chỉ biết khi phiên t đóng cửa). Tỉ lệ "cao hơn" (mẫu giảm: "thấp hơn") so
với **tỉ lệ nền cùng bối cảnh** (mẫu có điều kiện "vừa giảm" so với mọi ngày "vừa giảm"). Khoảng tin cậy Wilson 95%; p-value nhị thức
(xấp xỉ chuẩn); **kiểm tra ngày ngẫu nhiên**: rút ngẫu nhiên đúng n ngày cùng bối cảnh × 20.000 lần (seed 20261009), p hai phía. Chia
hai giai đoạn 10/2018–12/2022 và 01/2023–10/2026.

**Hạn chế (ghi rõ trong video):** cửa sổ 20 phiên chồng nhau → quan sát không độc lập, p thật lớn hơn; chỉ số không mua trực tiếp được;
chưa tính phí (≤ 0,45%/chiều, thường ~0,15%) + thuế bán 0,1% (C2); 27 phép so → kỳ vọng vài kết quả "đẹp" do may (đa kiểm định);
định nghĩa mẫu có nhiều phiên bản (đã thử độ nhạy). **Thêm (fact-check 09/10):** định nghĩa "open" của VCI không nhất quán theo thời
gian — năm 2021 có 133/250 phiên O = đóng cửa hôm trước (2019: 15, 2020: 19, 2022: 19, 2023–2026: 0–1); giá mở/cao/thấp lệch với
nguồn dữ liệu thứ ba ở 259/1.995 phiên. Chạy lại trên nguồn thứ ba: cây búa 35 lần, 42,9% vs 56,4% (5 phiên) nhưng 61,8% vs 59,7%
(20 phiên); doji 189 lần, 41,3% vs 45,0%; ba chàng lính trắng đúng sách 2 lần; màu nến ngược màu bảng giá 16,4%.

## 5. Kết quả

**Tỉ lệ nền** (mọi phiên hợp lệ):

| Bối cảnh | n (5 phiên) | Cao hơn sau 5 phiên | TB 5 phiên | Cao hơn sau 20 phiên | TB 20 phiên |
|---|---|---|---|---|---|
| Mọi ngày | 1.986 | **58,5%** | +0,19% | **59,2%** | +0,82% |
| Vừa giảm 5 phiên | 817 | 56,3% | −0,02% | 59,7% | +0,68% |
| Vừa tăng 5 phiên | 1.163 | 60,2% | +0,34% | 59,1% | +0,95% |

**Mẫu nến** (cột "nền" = cùng bối cảnh; mẫu giảm đo % lần THẤP hơn):

| Mẫu | Số lần (2026) | Sau 5 phiên [KTC 95%] | Nền | p | Sau 20 phiên [KTC 95%] | Nền | p | Hai giai đoạn (5 phiên) |
|---|---|---|---|---|---|---|---|---|
| **Cây búa đúng sách** | 35 (2) | **51,4%** [35,6–67,0] | 56,3% | 0,68 | **55,9%** [39,5–71,1] | 59,7% | 0,78 | 42,9% (n14) / 57,1% (n21) |
| Hình cây búa (không bối cảnh) | 86 (8) | 55,8% | 58,5% | 0,69 | 55,3% | 59,2% | 0,53 | 42,4% / 64,2% — **không ổn định** |
| **Doji** (cao hơn) | 201 (19) | 60,7% [53,8–67,2] | 58,5% | 0,58 | 65,7% [58,9–71,9] | 59,2% | 0,07 (ngẫu nhiên 0,049) | 59,4% / 62,1% |
| **Doji — đổi hướng 5 phiên** | 201 | **42,8%** | 45,0% | 0,58 | — | — | — | — |
| **Ba chàng lính trắng đúng sách** | **5** (0) | 80% [37,6–96,4] | 56,3% | 0,54 | 40% [11,8–76,9] | 59,7% | 0,66 | 5 lần đều trước 2023 |
| Hình ba chàng lính trắng | 10 (0) | 90% [59,6–98,2] | 58,5% | 0,09 | 60% | 59,2% | 1,0 | 10 lần đều trước 2023 |
| Nhấn chìm tăng | 44 (4) | 70,5% [55,8–81,8] | 56,3% | 0,08 (ngẫu nhiên 0,06) | 65,1% | 59,7% | 0,57 | 70,0% / 71,4% |
| Sao băng (thấp hơn) | 35 (2) | 48,6% | 39,8% | 0,38 | 51,4% | 40,9% | 0,27 | 46,2% / 55,6% |
| Ba con quạ đen (thấp hơn) | 2 (0) | — | — | — | — | — | — | quá ít |

**Độ nhạy / phép so phụ:**

| Phép so | n | Sau 5 phiên | Nền | p | Sau 20 phiên | Nền | p |
|---|---|---|---|---|---|---|---|
| Búa, bối cảnh "dưới MA10" | 37 | 45,9% (TB −1,42%) | 56,4% | 0,26 | 50,0% | 61,0% | 0,24 |
| Búa lỏng (U ≤ B) | 44 | 52,3% | 56,3% | 0,70 | 60,5% | 59,7% | 1,0 |
| "Ba nến xanh liền" (lỏng) | 69 | **71,0%** (TB +0,88%) | 58,5% (TB +0,19%) | **0,047** | 69,6% (TB +2,18%) | 59,2% (TB +0,82%) | 0,10 |
| Nến xanh dài | 217 | 64,1% | 58,5% | 0,08 (ngẫu nhiên) | 59,5% | 59,2% | 0,94 |
| Nến đỏ dài | 220 | 54,5% | 58,5% | — | 58,8% | 59,2% | — |

**Đọc kết quả** *[suy luận của kênh]*:
1. Các mẫu **đảo chiều** quen tên mà người mới hay nghe (cây búa "báo đáy", doji "sắp đảo chiều") **không tốt hơn** một ngày bất kỳ cùng
   bối cảnh trên VN-Index 2018–2026 — cây búa sau 20 phiên "kém hơn chút ít" theo VCI nhưng **nhỉnh hơn** theo nguồn thứ ba (61,8% vs
   59,7%) → chỉ nói "không hơn mốc"; hình cây búa cho kết quả ngược nhau giữa hai giai đoạn.
2. **Ba chàng lính trắng đúng sách quá hiếm** (5 lần theo VCI, 2 lần theo nguồn thứ ba / 8 năm, 0 lần từ 2023) — không thể nói gì, kể cả điều tốt.
3. Có vài kết quả **"đẹp"** nhưng đều thuộc kiểu **đà tăng ngắn hạn** (ba nến xanh liền, nến xanh dài, nhấn chìm tăng) — phù hợp với hiện
   tượng tự tương quan dương ngắn hạn của chỉ số (một phần do cổ phiếu nhỏ giao dịch thưa, giá "trễ" — *[suy luận, CHƯA KIỂM nguồn cho
   VN-Index]*). p ≈ 0,05–0,10 trên **27 phép so**, cửa sổ chồng nhau → **không qua** ngưỡng thống kê sau hiệu chỉnh đa kiểm định
   (Bonferroni 0,05/27 ≈ 0,002). Chênh lợi suất TB 5 phiên ~0,7 điểm % ≈ cỡ chi phí một vòng mua–bán. **Không trình bày như tín hiệu;**
   Fact-check: chỉ giữ tín hiệu cách nhau ≥ h phiên → p chính xác 0,11–0,24. Lời đọc (PM 09/10): "vài kết quả thoạt nhìn trông đẹp
   hơn mốc… không kết quả nào còn đứng vững sau khi tính tới việc thử nhiều mẫu cùng lúc"; mô tả chỉ có cách đếm, không bảng tỉ lệ.
4. Mốc so sánh **~59%, không phải 50%** — chính là bài học người mới cần nhất: "đúng 60% số lần" nghe ấn tượng nhưng chọn bừa một ngày
   cũng được ~59%.

## 6. Nghiên cứu học thuật về khả năng dự báo của nến

| Nghiên cứu | Thị trường / dữ liệu | Kết luận | Nhãn |
|---|---|---|---|
| Marshall, Young & Rose (2006), *J. Banking & Finance* 30(8): 2303–2323, doi 10.1016/j.jbankfin.2005.08.001 [2] | Cổ phiếu DJIA; kỳ dữ liệu **chưa thống nhất**: luận án "1992 - 2002", thứ cấp "01/01/1992–31/12/2001", 35 cổ phiếu; bootstrap tạo O/H/L/C ngẫu nhiên | **Câu trích thuộc luận án** [3] (fact-check đã mở PDF), không gán cho bài báo: "candlestick technical analysis does not have value"; "no evidence that a trader adhering to candlestick technical analysis would out-perform the market". Thứ cấp: 28 tín hiệu, giữ 10 ngày | Crossref [bằng chứng] (thông tin xuất bản); tóm tắt luận án [bằng chứng]; tóm tắt bài báo [CHƯA KIỂM — ScienceDirect chặn] |
| Marshall, Young & Cahan (2008), *Rev. Quant. Finance & Accounting* 31(2): 191–207 [4] | Nhật, 1975–2004; doi 10.1007/s11156-007-0068-1 (Crossref ✓) | "not profitable in the Japanese equity market"; không thêm giá trị trong cả 30 năm, 3 giai đoạn 10 năm, thị trường lên/xuống | [SECONDARY — tóm tắt qua tìm kiếm, trang IDEAS] |
| Tharavanij, Siraprapasiri & Rajchamaha (2017), *SAGE Open* 7(4) [5] | 50 cổ phiếu lớn SET (Thái Lan), 07/2006–06/2016; giữ 1/3/5/10 ngày | "mean returns of most patterns are not statistically different from zero"; bộ lọc chỉ báo không cải thiện; kiểm định nhị thức: không dự báo được hướng | [bằng chứng] (tóm tắt đầy đủ qua OpenAlex, fact-check 09/10) |
| Ngô Tùng Sơn, Lê Văn Thanh, Trần Quý Ban, Dương Xuân Hòa, Bùi Ngọc Anh (Đại học FPT) (2018), *IMMS '18* (ACM), tr. 89–93, doi 10.1145/3277139.3277161 [6] | Việt Nam, 02/01/2013–15/05/2018; mẫu đảo chiều, Pivot SMA | Mẫu đảo chiều "do not demonstrate the ability to predict the market trend", lợi nhuận thấp | Crossref (tác giả, hội nghị) [bằng chứng]; nội dung [bằng chứng — tóm tắt] (OpenAlex, fact-check 09/10); toàn văn chưa đọc. **Không nêu tên trường trong video** ("FPT" trùng mã HOSE / thương hiệu CTCK) |
| Lu (2014), *Pacific-Basin Finance Journal* 26: 65–78 [7] | Đài Loan, 1992–2009 | **4 mẫu có lợi nhuận sau phí**, vững qua bootstrap và ngoài mẫu | [bằng chứng — tóm tắt IDEAS] |
| Lu, Shiu & Liu (2012), *Review of Financial Economics* 21(2): 63–68 [15] | Quỹ Taiwan Top 50, 10/2002–12/2008 | 3 mẫu đảo chiều tăng 2 ngày có lợi nhuận | [SECONDARY] |
| Zhu, Atri & Yegen (2016), *Pacific-Basin Finance Journal* 37: 116–127 [8] | Trung Quốc, 1999–2008 | Hiệu quả **tuỳ loại cổ phiếu** (thanh khoản thấp / vốn hoá nhỏ thanh khoản cao) | [bằng chứng — tóm tắt IDEAS] |
| Caginalp & Laurent (1998), *Applied Mathematical Finance* 5(3–4): 181–205 [14] | Cổ phiếu S&P 500, 1992–1996 | Mẫu 3 ngày có ý nghĩa thống kê ngoài mẫu, ~1% trong 2 ngày | [SECONDARY] |

**Tóm lại** *[suy luận]*: bằng chứng **chia hai**; các nghiên cứu có kiểm soát (bootstrap, phí) trên cổ phiếu lớn Mỹ, Nhật, Thái và nghiên
cứu Việt Nam **không thấy giá trị**; một số nghiên cứu châu Á thấy **vài mẫu** có ích ở **vài loại cổ phiếu / giai đoạn**. Lời đọc dùng
đúng mức này ("tín hiệu rất mờ, không ổn định").

## 7. "Khi nào điều này KHÔNG đúng với bạn" (luật cứng số 4)

1. Phép đếm của kênh chỉ trên **VN-Index**, 8 năm, **chưa phí/thuế**; cổ phiếu riêng lẻ, khung giờ/phút, giai đoạn khác có thể khác
   (Zhu & cs. 2016: tuỳ loại cổ phiếu [8]).
2. **Cổ phiếu thanh khoản thấp**: một cây nến có thể chỉ phản ánh vài lệnh nhỏ → hình dạng ít thông tin *[suy luận]*.
3. **Giá mở cửa của cổ phiếu = giá khớp ATO** (C2; QĐ 22/QĐ-HĐTV) → có thể cách xa đóng cửa hôm trước (gap) — "mở trong thân nến trước"
   của sách nước ngoài ít khi đúng với VN.
4. **Giá điều chỉnh**: dữ liệu vnstock (và nhiều ứng dụng) điều chỉnh giá quá khứ sau cổ tức/thưởng cổ phiếu → nến cũ trên màn hình khác
   giá giao dịch thật lúc đó (C2 Ghi chú: `breadth_2026` là giá điều chỉnh). VN-Index không bị điều chỉnh kiểu này.
5. **Quy ước màu** khác nhau giữa biểu đồ (xanh/đỏ, rỗng/đặc) → luôn xem chú thích.

## 8. Huyền thoại vs sự thật (cho Short "Khái niệm 45 giây")

| Huyền thoại | Sự thật (nguồn) |
|---|---|
| "Nến xanh = nên mua" | Nến xanh chỉ nói đóng > mở **trong phiên**; ~15% phiên màu nến ngược màu bảng giá (kênh tự đếm) |
| "Thấy cây búa là đáy" | VN-Index 2018–2026: 35 lần, sau 5 phiên tăng 51% vs nền 56% (kênh tự đếm); Mỹ/Nhật/Thái/VN: không thấy giá trị [2]–[6] |
| "Doji = sắp đảo chiều" | Đổi hướng 43% vs ngày thường 45% (kênh tự đếm) |
| "Đúng 60% là giỏi" | Chọn bừa một ngày: ~59% sau 20 phiên VN-Index cao hơn (kênh tự đếm) |
| "Nến do Homma phát minh thế kỷ 18" | Chính Nison sau này nghi ngờ; có thể thời Minh Trị [1] |

## 9. Việc còn mở

- ~~Định nghĩa "open" của VN-Index trong dữ liệu VCI~~ — **đã xác nhận (fact-check 09/10):** giá trị chỉ số đầu tiên sau khớp ATO
  (gap trong bản tin 12/03, 13/03, 24/03 + 3 nguồn dữ liệu), **trừ 10/03** (VCI 1.664,52 vs CafeF 1.697,87 — còn mở; cần ảnh biểu đồ
  trong phiên của HOSE hoặc nguồn thứ tư). Tỉ lệ màu ngược: 15,2% (VCI) / 16,4% (nguồn thứ ba).
- Mở **tóm tắt bài J. Banking & Finance 2006** (chốt số mẫu, kỳ dữ liệu) — câu trích đã xác nhận thuộc luận án [3].
- Mở bản PDF nghiên cứu Việt Nam [6] (ACM chặn) để kiểm "không dự báo được xu hướng".
- Mở *Beyond Candlesticks* hoặc nguồn sử Nhật cho giai thoại Homma.
- Tìm nguồn cho tự tương quan ngắn hạn của VN-Index (nếu sau này làm bài về "đà tăng") — không dùng trong C3.
- ~~Mô tả video có bảng kết quả kênh tự đếm~~ — **quyết định PM 09/10:** mô tả chỉ có khối phương pháp (factcheck mục 2: cách đếm + "không
  kết quả nào còn đứng vững sau khi tính tới việc thử nhiều mẫu cùng lúc, và chưa trừ phí"), **không** bảng tỉ lệ từng mẫu; lời đọc đã
  đổi thành "Cách kênh đếm, mình tóm tắt ở phần mô tả".

## Nguồn

1. Wikipedia, "Candlestick chart" (mục History; trích Nison, *Beyond Candlesticks*, 1994) — https://en.wikipedia.org/wiki/Candlestick_chart [SECONDARY]
2. Marshall, B. R., Young, M. R., Rose, L. C. (2006). Candlestick technical trading strategies: Can they create value for investors?
   *Journal of Banking & Finance* 30(8), 2303–2323. doi:10.1016/j.jbankfin.2005.08.001 — Crossref: https://api.crossref.org/works?query.bibliographic=Candlestick+technical+trading+strategies+Can+they+create+value+for+investors
3. Marshall, B. R. (2005). *Candlestick technical trading strategies: can they create value for investors?* Luận án PhD, Massey University —
   https://mro.massey.ac.nz/items/edc6c1cf-63d9-4c94-a13d-92ffe1a53481/full [bằng chứng, tóm tắt]
4. Marshall, B. R., Young, M. R., Cahan, R. (2008). Are candlestick technical trading strategies profitable in the Japanese equity market?
   *Review of Quantitative Finance and Accounting* 31(2), 191–207 — https://ideas.repec.org/a/kap/rqfnac/v31y2008i2p191-207.html [SECONDARY]
5. Tharavanij, P., Siraprapasiri, V., Rajchamaha, K. (2017). Profitability of Candlestick Charting Patterns in the Stock Exchange of
   Thailand. *SAGE Open* 7(4). doi:10.1177/2158244017736799 — https://ideas.repec.org/a/sae/sagope/v7y2017i4p2158244017736799.html
6. Ngo Tung Son, Le Van Thanh, Tran Quy Ban, Duong Xuan Hoa, Bui Ngoc Anh (2018). An analyze on effectiveness of candlestick reversal
   patterns for Vietnamese stock market. *Proceedings of IMMS '18*, ACM, 89–93. doi:10.1145/3277139.3277161 — https://api.crossref.org/works/10.1145/3277139.3277161 ;
   https://unpaywall.org/10.1145%2F3277139.3277161 [nội dung SECONDARY]
7. Lu, T.-H. (2014). The profitability of candlestick charting in the Taiwan stock market. *Pacific-Basin Finance Journal* 26, 65–78 —
   https://ideas.repec.org/a/eee/pacfin/v26y2014icp65-78.html
8. Zhu, M., Atri, S., Yegen, E. (2016). Are candlestick trading strategies effective in certain stocks with distinct features?
   *Pacific-Basin Finance Journal* 37, 116–127 — https://ideas.repec.org/a/eee/pacfin/v37y2016icp116-127.html
9. Thời báo Tài chính Việt Nam, "Chứng khoán ngày 10/3: VN-Index phục hồi mạnh nhưng rủi ro vẫn hiện hữu" (10/03/2026) —
   https://thoibaotaichinhvietnam.vn/chung-khoan-ngay-103-vn-index-phuc-hoi-manh-nhung-rui-ro-van-hien-huu-193453.html [bằng chứng]
10. VNDirect, Vietnam Daily Market Recap 10/03/2026 — https://www.vndirect.com.vn/cmsupload/beta/VIE_Vietnam_Daily_Market_Recap_March_10-1.pdf ;
    BSC Brief 10/03 — https://new.bsc.com.vn/en/report/report-detail/12767502 [SECONDARY]
11. VNDirect, Daily Market Recap 13/03/2026 — https://www.vndirect.com.vn/cmsupload/beta/VIE_Vietnam_Daily_Market_Recap_March_13.pdf ;
    Pinetree, Market brief 13/03/2026 — https://pinetree.vn/?p=98813 [SECONDARY]
12. VNDirect, Daily Market Recap 24/03/2026 — https://www.vndirect.com.vn/?p=96848 ; Pinetree, Market brief 24/03/2026 —
    https://pinetree.vn/en/post/20260324/market-brief-24-03-2026/ [SECONDARY]
13. Thời báo Tài chính Việt Nam, "Chứng khoán ngày 24/3: Hồi phục tích cực, VN-Index tăng điểm trở lại" —
    https://thoibaotaichinhvietnam.vn/chung-khoan-ngay-243-hoi-phuc-tich-cuc-vn-index-tang-diem-tro-lai-173089.html ; VNCSI bản tin 24/03 —
    https://vncsi.com.vn/upload_images/files/2026/03/24/ban-tin-thi-truong-ngay-24_03_2026.pdf [SECONDARY]
14. Caginalp, G., Laurent, H. (1998). The predictive power of price patterns. *Applied Mathematical Finance* 5(3–4), 181–205 —
    https://ideas.repec.org/a/taf/apmtfi/v5y1998i3-4p181-205.html [SECONDARY]
15. Lu, T.-H., Shiu, Y.-M., Liu, T.-C. (2012). Profitable candlestick trading strategies — The evidence from a new perspective. *Review of
    Financial Economics* 21(2), 63–68 — https://ideas.repec.org/a/wly/revfec/v21y2012i2p63-68.html [SECONDARY]
16. VnExpress 10/03/2026 — https://vnexpress.net/vn-index-tang-gan-24-diem-5048812.html (fact-check 09/10)
17. Công Luận 10/03/2026 — https://congluan.vn/chung-khoan-hom-nay-10-3-2026-hoi-phuc-manh-vn-index-tang-gan-24-diem-10332937.html
18. Nhân Dân 13/03/2026 — https://nhandan.vn/ocop/chung-khoan-ngay-133-co-phieu-dau-khi-bi-ban-manh-vn-index-giam-tiep-hon-13-diem-post948183.html
19. Người Lao Động 24/03/2026 — https://tuoitre.vn/nld/vn-index-phuc-hoi-gan-24-diem-co-phieu-ngan-hang-bat-dong-san-dan-song-196260324155859073.htm
20. Vietnambiz 24/03/2026 — https://vietnambiz.vn/vn-index-hoi-phuc-hon-30-diem-dau-phien-sac-xanh-lan-rong-20263249443760.htm
- Ghi chú: các bản tin của công ty chứng khoán ([10]–[13]) chỉ là tài liệu kiểm nội bộ — **không** dẫn trong video hay mô tả.
- Dữ liệu: `data/ck/vnindex_1d.csv` (HOSE, truy xuất qua vnstock/VCI) — mã: `data/long/ck-c3-bieu-do-nen/analysis.py`; kết quả:
  `results.json`; nến tuần 2026: `vnindex_1w_2026.csv`.
- Hồ sơ C2 (`2026-10-07-long-c2-research.md`): [C2-7] dữ liệu kênh, [C2-8] Nhân Dân 09/03/2026, [C2-19] màu bảng giá; QĐ 22/QĐ-HĐTV (giá
  tham chiếu, ATO).
