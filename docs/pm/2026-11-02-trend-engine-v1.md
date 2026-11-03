# Trend Intelligence Engine V1: MIM/CK (thiết kế, 02/11/2026)

Chủ kênh duyệt triển khai 02/11/2026. Đầu vào: `docs/pm/2026-11-02-audit-trend.md`.

Ràng buộc:
- Không API trả phí, ít LLM.
- Không phụ thuộc yt-dlp. Không đo được thì ghi `COMPETITOR_UNKNOWN`.
- Không dùng Google autocomplete khi chấm điểm.
- RSS chỉ dùng sau khi rà điều khoản.
- Giữ nguyên `hf_batch_render`.
- Không tự upload, không đổi lịch, không merge khi chưa qua QA và cổng duyệt.

## Luồng

```
nguồn (đã rà ToS) ─► trend_scan (3 h/lần) ─► gom sự kiện ─► lọc nguồn độc lập ─► báo cáo read-only        [P0]
                                                    │
                                                    ▼
                         dedupe toàn kho ─► factcheck (sơ cấp + kiểm chứng độc lập)
                         ─► Event Score  +  Video Opportunity Score (riêng từng kênh) ─► thẻ ứng viên        [P1]
                                                    │
                                                    ▼  chủ kênh duyệt thẻ
                         Grok packaging (title/hook 3 s) ─► Codex spec ─► agy render ─► QA ─► chủ kênh duyệt
                         ─► upload vào slot làn nóng; đo phát hiện→đăng, 24 h / 72 h                          [P2]
```

## P0: Scanner (read-only)

**File mới** (Codex): `factory/trend/` gồm:
- `sources.json`: mỗi nguồn có `url`, `kind` (rss/json/api), `owner_group`, `lang`, `tos_status` (`ok`/`pending`/`blocked`), `tos_note`;
- `scan.py`: chỉ đọc nguồn có `tos_status=ok`;
- `cluster.py`;
- `independence.py`;
- `report.py`.

**Thư viện:** urllib + xml.etree, không thêm dependency.

**Lưu trữ:** `data/trend/trend.sqlite` (gitignore), gồm các bảng `article`, `event`, `run`. Chỉ lưu tiêu đề, URL, giờ đăng, nguồn và vài dòng tóm tắt RSS. Không lưu toàn văn.

**Gom sự kiện:** nhóm các bài trong cửa sổ 48 h theo thực thể (tên riêng, mã, số tiền, tên sản phẩm), với token Jaccard ≥ ngưỡng. Thực thể chuẩn hóa không dấu, ghép alias. Thuật toán tất định, không LLM.

**Lọc nguồn độc lập:**
- các bài cùng `owner_group` (cùng tòa soạn hoặc cùng hệ sinh thái) tính là 1 nguồn;
- bài dẫn lại nhau (URL hoặc tiêu đề gần trùng) gộp lại;
- trường `independent_sources` đếm số nhóm sở hữu khác nhau.

**Báo cáo:** `output/trend/<ngày>/<giờ>.md`, top sự kiện kèm số nguồn độc lập, tốc độ (số bài trong 3 h so với 24 h) và giờ thấy lần đầu. Không ghi gì ra kênh.

**Lịch chạy:** 3 h/lần bằng Windows Task Scheduler. Lead tạo tác vụ sau khi P0 qua nghiệm thu. Tác vụ là cấu hình bền nên báo chủ kênh trước khi tạo.

**Nguồn ứng viên:** Grok rà ToS trước, chưa rà thì không bật.
- RSS báo VN: VnExpress, Tuổi Trẻ, Dân Trí, CafeF, VnEconomy, GenK. Ghi chú 05/10: miễn phí cho cá nhân và tổ chức phi lợi nhuận; kênh có kiếm tiền thì cần xác nhận.
- Google News RSS theo từ khóa kênh.
- Google Trends daily RSS VN.
- Hacker News API.
- Reddit `.json` công khai.
- Wikipedia pageviews: tái dùng `HttpPageviews` trong `factory/demand.py`.
- Giá SJC và tỷ giá công khai (CK).

**Nguồn P0 (chủ kênh chốt 02/11: bật một phần):**
- Thử nghiệm nội bộ: Thanh Niên Công nghệ, Thanh Niên Kinh tế, GenK. Chỉ bật sau khi kiểm điều khoản, robots.txt và giới hạn truy cập.
- VietNamNet: tiếp tục rà. CafeF: giữ `pending`.
- Không tự động truy cập nguồn có điều khoản cấm bot hay khai thác tự động.
- Được thử thêm nguồn quốc tế cho phép sử dụng, lọc theo tác động tới Việt Nam.

**Nghiệm thu P0 (sửa 02/11):**
- 3 lần chạy liên tiếp không lỗi. Mỗi lần ≤ 5 phút; nguồn lỗi thì ghi vào `run` và chạy tiếp.
- ≥ 10 **ứng viên liên quan** mỗi kênh trong 72 h, mỗi ứng viên có ≥ 1 URL mở được. Không đòi ≥ 10 tin NÓNG.
- Báo cáo đếm riêng 4 số: bài, sự kiện hợp lệ, sự kiện nóng, cơ hội sản xuất.
- Tỷ lệ phát hiện đo trên bộ benchmark sự kiện nóng độc lập do Grok lập. Không lấy kết quả scanner làm đáp án.
- Gom sự kiện: trên bộ test 40 bài gán nhãn tay, precision ≥ 0,8.
- `independent_sources` không đếm trùng cùng `owner_group`.
- Không nguồn nào `tos_status != ok` bị gọi; có test chứng minh.
- `pytest` của module xanh. Không đụng `state.sqlite`, không đụng lịch.

## P1: Dedupe, factcheck, chấm điểm

**Dedupe toàn kho** (`dedupe.py`):
- **Nguồn so:**
  - spec Short `data/stier/specs/*.json` của cả MIM và CK;
  - `data/long/*`;
  - `state.sqlite` `item`;
  - `data/channel_titles/*.json`. File này dừng cập nhật từ 20/10, nên P1 thêm lệnh làm mới bằng Data API `playlistItems`. Lệnh này miễn phí trong quota và do Lead chạy.
- **Cách so:** theo thực thể và theo tiêu đề. Tái dùng `factory/lines/novelty.py` và `factory/sameness.py`.
- **Kết quả:** `NEW` / `NEAR <slug>` / `DUP <slug>`. Riêng cùng sự kiện ở hai kênh thì ghi `CROSS-CHANNEL-OK`, vì hai góc khác nhau được phép.

**Factcheck** (`verify.py`): một sự kiện chỉ thành ứng viên khi có:
- ≥ 1 **nguồn sơ cấp**: văn bản cơ quan, công bố của công ty hoặc nhân vật, hồ sơ, dữ liệu gốc;
- và ≥ 1 **nguồn kiểm chứng độc lập** khác `owner_group`.

Mỗi số hoặc tên trong hook phải có trong một trong hai nguồn này. Kiểm bằng regex, giống cách `factcheck_lint`. Thiếu thì gắn `UNVERIFIED`, không vào hàng render. Bước tìm nguồn sơ cấp giao Grok; code chỉ kiểm cấu trúc và độ khớp.

**Event Score** (0–100, độ nóng của sự kiện, không phụ thuộc kênh):

| Thành phần | Điểm |
|---|---|
| Nguồn độc lập trong 24 h | 35 |
| Tốc độ: bài 3 h so với trung bình 24 h | 25 |
| Độ mới: giờ từ lúc thấy lần đầu, giảm tuyến tính tới 72 h | 20 |
| Có nguồn sơ cấp | 10 |
| Tín hiệu ngoài báo: HN/Reddit/Wikipedia pageviews tăng | 10 |

**Video Opportunity Score** (0–100, tính riêng MIM và CK):

| Thành phần | Điểm |
|---|---|
| Hợp kênh: từ khóa trụ cột của kênh, góc MIM = cơ chế, góc CK = tiền và tác động | 25 |
| Hook kiểu thắng tuần 44: tên người, hoặc cặp số đối nghịch có trong nguồn đã kiểm | 25 |
| Dedupe: NEW 15, NEAR 5, DUP 0 | 15 |
| Có tư liệu hình hợp lệ (ảnh/clip tự do, hoặc dựng được bằng đồ họa) | 15 |
| Khoảng trống đối thủ (`COMPETITOR_UNKNOWN` = 7,5 trung tính) | 10 |
| Lead time: còn kịp lên sóng trước khi sự kiện quá 72 h | 10 |

Vào thẻ ứng viên khi Event ≥ 60, VOS ≥ 65 và đã `VERIFIED`. Trọng số là giả định ban đầu, chỉnh lại sau P2.

**Thẻ ứng viên** (`output/trend/cards/<event_id>.md`): sự kiện, nguồn, hai góc (MIM / CK / chỉ một kênh), các điểm thành phần, cờ dedupe và factcheck.

**Nghiệm thu P1:**
- Dedupe bắt đúng 10/10 ca trùng đã biết (Nvidia, luật sư ChatGPT, AI giọng nói, cụm nhà ở CK…) và không báo nhầm 10 ca mới đã biết (keo pizza, Tay, Mars Orbiter, Reddit…).
- Sự kiện chỉ có một nguồn hoặc cùng `owner_group` thì không bao giờ `VERIFIED`; có test chứng minh.
- Hai điểm số được tính và ghi tách riêng; có test cho từng thành phần.
- Đối thủ không đo được thì ghi `COMPETITOR_UNKNOWN`, không làm lỗi lần chạy.
- Không gọi autocomplete. Có test chặn import hay gọi endpoint autocomplete.

## P2: Pilot 3–5 tin nóng

**Quy trình mỗi tin:** thẻ ứng viên → chủ kênh duyệt → Grok packaging (3 title, hook 3 s, chữ khung đầu, kiểm hook ≤ 9 từ, có tên hoặc số) → Codex viết spec → `script_lint` + factcheck → agy render (`hf_batch_render` giữ nguyên) → tờ soát (QA) → chủ kênh duyệt → Lead upload vào slot làn nóng.

**Đo:** mỗi tin ghi các mốc giờ phát hiện → duyệt → render xong → upload → lên sóng, và view sau 24 h / 72 h. So với mốc tuần 44: CK 72 h ≥ 514, MIM 72 h ≥ 745.

**Nghiệm thu P2:**
- ≥ 3 tin lên sóng.
- Trung vị phát hiện → lên sóng ≤ 72 h.
- 0 lỗi dữ kiện bị bình luận chỉ ra.
- Có bảng so sánh với bài thường cùng tuần.
- Báo cáo đề xuất chỉnh trọng số.

**Slot:**
- **CK:** dùng slot trống trong lưới. Theo `shorts_grid --free` 03–16/11 còn 53 slot, gồm 3–4/ngày tới 12/11 và 5/ngày từ 13/11. Không tăng tần suất.
- **MIM:** thay từng đợt 5–10 bài yếu trong nhóm 51, không tăng tần suất. Đợt 1 ở dưới.

### MIM đợt 1: 7 slot đề xuất thay

Các bài dưới đây được phân loại "không sửa được bằng hook" (không tên, không số; `docs/pm/2026-11-02-hang-cho-short-mau-thua.md`). Từ 09/11 thì kịp render. Bài cũ chỉ gỡ lịch về private, không xóa. Chỉ làm sau khi chủ kênh duyệt danh sách này.

| Giờ VN | Bài hiện tại | Lấp bằng |
|---|---|---|
| 09/11 17:00 | `mim-hoc-bang-hoi-tiec` | pilot #29 (evergreen) |
| 09/11 19:00 | `mim-to-bip-bang-toan` | pilot #29 |
| 09/11 21:30 | `mim-va-3-lo-hong-moi-dem` | pilot #29 |
| 10/11 11:30 | `mim-chia-bai-doi-xung` | làn nóng (tin P2) hoặc pilot #29 |
| 12/11 11:30 | `mim-telex-tu-dien-tin` | làn nóng hoặc pilot #29 |
| 12/11 19:00 | `mim-watson-tieng-chuong` | làn nóng hoặc pilot #29 |
| 12/11 21:30 | `mim-pluribus-khong-doc-vi` | làn nóng hoặc pilot #29 |

Các bài thua mẫu lên sóng 03–08/11 để nguyên vì không kịp render. 19 bài còn lại (cũng không sửa được bằng hook) và các bài sửa được bằng hook để sang đợt 2, sau khi đo được 72 h của đợt 1.

## Phân công agent

| Việc | Agent | Lý do |
|---|---|---|
| Rà ToS nguồn, danh sách nguồn, nguồn sơ cấp, packaging title/hook | Grok (dự phòng agy) | Chủ kênh giao Grok phụ trách nghiên cứu; không chuyển sang Claude |
| Code P0/P1 + test | Codex | Code, spec, test; hạn mức còn tốt (lỗi treo stdin đã sửa 02/11) |
| Spec Short P2 | Codex | — |
| Render, QA khung hình P2 | agy | Codex không render được trong sandbox |
| Review, nghiệm thu, upload, lịch | Claude (Lead) | Agent không bao giờ upload hay đổi lịch |
| Gemini | — | **Máy chưa cài Gemini CLI**, `agent_ticket.py` chưa hỗ trợ. Cần chủ kênh quyết có cài không |

## Phụ thuộc

1. Grok rà ToS → P0 mới được bật nguồn (`tos_status=ok`).
2. P0 nghiệm thu → Lead tạo tác vụ 3 h (báo chủ kênh).
3. P1 dedupe cần làm mới `channel_titles`: Lead chạy, cần credential (`YT_CREDS_DIR`).
4. P2 upload và thay lịch cần credential, cùng điều kiện đang chặn việc thay 3 Short C2 (#28).
5. P2 đợt MIM cần chủ kênh duyệt danh sách slot ở trên.

## Rủi ro

- **Tin giả, tin chưa xác nhận:** chặn bằng bắt buộc nguồn sơ cấp cộng nguồn độc lập.
- **Bản quyền ảnh, clip báo:** không dùng. Chỉ dùng đồ họa, tư liệu tự do, ảnh AI theo luật kênh.
- **Nội dung tài chính (CK):** không khuyến nghị mua bán, giữ câu miễn trừ.
- **ToS nguồn:** chỉ đọc tiêu đề và URL làm tín hiệu nội bộ, không đăng lại nội dung.
- **Quá tải upload:** CK tối đa khoảng 10/ngày, không tăng tần suất.
