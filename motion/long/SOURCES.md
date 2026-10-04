# Nguồn hình và video dùng tự do lâu dài cho kênh Hình Sự (đã kiểm tra ngày 04/10/2026)

**Nguyên tắc:** kênh có bật kiếm tiền, nên mọi tư liệu phải cho phép **dùng thương mại** và **cho phép chỉnh sửa** (cắt khung, Ken Burns, phủ chữ, đổi màu).

| Được dùng | Không dùng |
|---|---|
| Public domain / PDM, CC0, CC BY, CC BY-SA (có ghi công) | NC (cấm thương mại) |
| Giấy phép riêng cho phép thương mại: Pexels, Pixabay, Mixkit "Free License" | ND (cấm chỉnh sửa) |
| | "Fair use", ảnh không rõ nguồn |

**Ghi công:**
- `build_long` và `describe.py` tự in credit vào mô tả cho các ảnh lấy bằng `research_long.py` (Commons) và `media_search.py` (các kho khác).
- Giữ nguyên file `.json` cạnh từng ảnh. Đây là bằng chứng giấy phép nếu bị khiếu nại.

## 1. Ảnh tư liệu: đang dùng hoặc đã tích hợp sẵn

| Nguồn | Giấy phép | Mạnh ở mảng | Công cụ |
|---|---|---|---|
| **Wikimedia Commons** | PD / CC0 / CC BY / BY-SA tùy file | Mọi chủ đề, nguồn chính | `research_long.py` |
| **Wellcome Collection** | PDM / CC0 / CC BY 4.0 | Lịch sử thuốc phiện, y học, Trung Hoa và Ấn Độ thế kỷ 19 (tiệm hút, xưởng thuốc phiện Patna) | `media_search.py --src wellcome` |
| **Openverse** (tổng hợp Flickr CC, bảo tàng, Commons) | Lọc sẵn CC0 / PDM / BY / BY-SA | Ảnh đời thường châu Á, địa điểm hiện nay | `--src openverse` |
| **Art Institute of Chicago** | CC0 (tác phẩm public domain) | Ảnh và tranh thế kỷ 19 (Hồng Kông, Trung Hoa, Nhật). Tìm bằng từ khóa cụ thể, từ khóa chung trả kết quả nhiễu | `--src artic` |
| **Europeana** (`reusability=open`) | PDM / CC0 / CC BY / BY-SA | Ảnh thời thuộc địa ở châu Á (KITLV, Tropenmuseum, Nationaal Archief) | `--src europeana`. Nên đăng ký khóa miễn phí (`EUROPEANA_KEY`), hiện đang dùng khóa demo |
| **Sentinel-2** qua Microsoft Planetary Computer | Dữ liệu Copernicus: dùng thương mại tự do, **bắt buộc** ghi "Contains modified Copernicus Sentinel data [năm]" | Ảnh vệ tinh 10 m làm cảnh định vị (ngã ba sông Mekong, đặc khu sòng bạc, một khu phố…) | `media_search.py sat` |

**Lưu ý với Openverse:** ảnh từ Flickr có thể bị "rửa giấy phép" (người đăng không phải tác giả). Chỉ dùng khi tài khoản đăng ảnh là người chụp, hoặc là một tổ chức. Tuyệt đối không dùng ảnh người nổi tiếng chụp chuyên nghiệp lấy từ Flickr.

## 2. Ảnh tư liệu: nên thêm sau

Các nguồn này cần đăng ký khóa API miễn phí, hoặc phải tìm bằng tay.

| Nguồn | Giấy phép | Mạnh ở mảng | Ghi chú |
|---|---|---|---|
| **NARA**, Lưu trữ Quốc gia Mỹ | Tác phẩm của chính phủ liên bang Mỹ là public domain | Ảnh và phim của FBI, DEA, quân đội Mỹ, Chiến tranh Việt Nam, Tam Giác Vàng thời CIA | API cần khóa, phải gửi email xin |
| **Library of Congress** (bộ "Free to Use and Reuse", "no known restrictions") | PD | Ảnh báo chí Mỹ, vụ án Mỹ đầu thế kỷ 20 | Trang chặn truy cập tự động (Cloudflare). Phần lớn ảnh đã có bản sao trên Commons, nên tìm qua Commons trước |
| **DVIDS** (quân đội Mỹ) | PD, được dùng thương mại | Ảnh và video quân sự hiện đại, chống ma túy | API cần khóa miễn phí; vẫn có thể bị Content ID nhận nhầm |
| **Smithsonian Open Access** | CC0 | Hiện vật, ảnh lịch sử Mỹ | Khóa api.data.gov miễn phí. Ít hợp chủ đề tội phạm, phần lớn là mẫu vật |
| **Met Museum**, **Rijksmuseum**, **NYPL Public Domain** | CC0 / PD | Tranh, ảnh cổ, bản đồ | Rijksmuseum có nhiều ảnh Đông Nam Á thời thuộc địa |
| **NDL Image Bank**, Thư viện Quốc hội Nhật | PD, được dùng thương mại không cần xin phép (chỉ xin ghi nguồn) | Tranh ukiyo-e, ảnh Nhật thời Minh Trị, phù hợp chủ đề Yakuza | Tìm bằng tay |
| **Lưu trữ Quốc gia Đài Loan**, **Bảo tàng Cố cung Đài Bắc** | Open Government Data License, tương đương CC BY | Quốc Dân Đảng, Đài Loan thế kỷ 20, rất hợp tập Tam Giác Vàng | Tìm bằng tay, ghi công đầy đủ |
| **Flickr Commons** (NKCR, "No known copyright restrictions") | Các tổ chức tự xác nhận không còn bản quyền | Ảnh lưu trữ của các thư viện lớn | Nhiều ảnh đã có trên Commons |

## 3. Video B-roll

| Nguồn | Giấy phép | Ghi chú |
|---|---|---|
| **Pexels** (đang dùng) | Giấy phép Pexels: thương mại, không bắt buộc ghi công | Kiểm tra HDR (`color_transfer`) trước khi render. Hiếm khi bị Content ID |
| **Pixabay** | Content License: thương mại, không bắt buộc ghi công | Cần khóa API miễn phí. Một số clip/nhạc bị gắn Content ID; nếu bị claim thì dùng "License Certificate" của Pixabay để kháng nghị |
| **Mixkit** | Chỉ những clip mang **Free License** | Có loại Restricted License chỉ cho dùng phi thương mại, nên phải xem từng clip |
| **Coverr** | Miễn phí cho thương mại | Kho nhỏ, mạnh về cảnh thành phố |
| **Prelinger Archives / phim thời sự trong NARA** (archive.org) | Phần lớn là PD | **Rủi ro Content ID:** nhiều công ty gắn Content ID lên phim PD (ví dụ Archive Farms). Chỉ dùng đoạn ngắn, bỏ tiếng gốc, giữ link nguồn để kháng nghị. Nhãn `licenseurl` trên archive.org không đáng tin vì có bản tải lại từ YouTube bị gắn nhầm "public domain" |
| **NASA / DVIDS video** | PD | Cảnh không gian, quân sự |

## 4. Bản đồ, âm thanh, nhạc

| Loại | Nguồn | Giấy phép |
|---|---|---|
| Bản đồ vector | Natural Earth (đang dùng) | PD |
| Bản đồ chi tiết | OpenStreetMap | ODbL, ghi "© OpenStreetMap contributors" |
| Nhạc nền | Kevin MacLeod / incompetech (đang dùng) | CC BY 4.0, ghi công tự động |
| Nhạc nền | YouTube Audio Library | Miễn phí khi dùng trên YouTube, chú ý cột yêu cầu ghi công |
| Hiệu ứng âm thanh | Freesound | Chỉ lấy CC0 hoặc CC BY |
| Hiệu ứng âm thanh | Pixabay SFX | Thương mại tự do |

## 5. KHÔNG dùng (đã kiểm tra)

| Nguồn | Lý do |
|---|---|
| EOX Sentinel-2 cloudless (s2maps / EOxCloudless) | Chỉ CC BY-NC-SA, muốn dùng thương mại phải mua giấy phép |
| Gallica / BnF (Pháp) | Ảnh public domain nhưng dùng thương mại (kể cả video có kiếm tiền) phải xin phép và trả phí |
| Government Records Service Hồng Kông (PRO) | Ngoài mục đích học tập, nghiên cứu thì phải xin phép bằng văn bản |
| British Pathé, AP Archive, Reuters, Getty, CriticalPast | Trả phí |
| Videvo | Lẫn nhiều giấy phép khác nhau, dễ dùng nhầm clip không được phép |
| Ảnh hoặc cảnh trích từ phim, ảnh chụp màn hình bản tin truyền hình | Không có giấy phép |
| Ảnh AI | Kênh không dùng, và đã có file AI lẫn trong kết quả Commons, ví dụ file "Stable diffusion…" |

## 6. Nếu bị Content ID claim

1. Mở YouTube Studio, vào mục Nội dung, chọn "Xem chi tiết" ở claim, rồi bấm "Kháng nghị". Lý do: có giấy phép hoặc tư liệu thuộc phạm vi công cộng.
2. Dán link trang gốc của tư liệu (`page` trong file `.json` của ảnh, `slug` trong `broll/index.json` của Pexels) và tên giấy phép.
3. Bên claim có 30 ngày để trả lời. Trong thời gian kháng nghị, doanh thu được giữ lại và trả cho bên thắng.
