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
| **NASA Image and Video Library** (thêm 06/10/2026) | Ảnh NASA không có bản quyền ở Mỹ. **Không** dùng logo NASA, không gợi ý NASA bảo trợ; ảnh có bên thứ ba (xem mô tả) thì bỏ. [Hướng dẫn](https://www.nasa.gov/nasa-brand-center/images-and-media/) | Vệ tinh, GPS, không gian, máy tính thời Apollo, Trái Đất | `--src nasa` (không cần khóa) |
| **Smithsonian Open Access** (thêm 06/10/2026) | Chỉ nhận media `usage.access = CC0` | Hiện vật công nghệ: máy tính, điện thoại, máy nghe nhạc (cho kênh MIM) | `--src smithsonian`. Cần khóa miễn phí api.data.gov: `SI_API_KEY=` trong `.local.env` |
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

## 7. Quy tắc khi dùng tư liệu trong video có kiếm tiền (tra cứu ngày 04/10/2026)

Có ba lớp luật áp dụng cùng lúc:
1. Luật bản quyền: Mỹ (YouTube xử lý khiếu nại theo DMCA) và Việt Nam (Luật SHTT, Điều 25).
2. Hệ thống tự động Content ID.
3. Chính sách kiếm tiền YPP: "reused content" và "inauthentic content".

| Loại tư liệu | Dùng trong video có kiếm tiền? | Ghi chú |
|---|---|---|
| Public domain thật (Mỹ: xuất bản trước 1931; ảnh của chính phủ liên bang Mỹ; CC0/PDM) | ✅ | Riêng phim thời sự cũ vẫn có thể bị Content ID nhận nhầm (mục 3) |
| CC BY / CC BY-SA | ✅ ghi công | Không dùng NC/ND |
| Pexels, Pixabay, Mixkit Free | ✅ | Giữ link nguồn để kháng nghị |
| Ảnh của chính phủ nước khác (Hồng Kông, Thái, Trung Quốc, Việt Nam…) | ⚠️ | KHÔNG tự động là public domain như ảnh liên bang Mỹ. Chỉ dùng khi Commons đã xác nhận giấy phép |
| Trích dẫn văn bản ngắn (câu nói, công hàm, phát biểu) | ✅ trích dẫn hợp lý | Ngắn, đúng nguyên ý, ghi nguồn. Luật SHTT Điều 25 cho phép trích dẫn hợp lý để bình luận, minh họa trong phim tài liệu |
| Đọc lại nguyên văn bài viết hay sách của người khác | ❌ | YPP gọi là "exclusive readings of materials you didn't create". Kịch bản của kênh phải là lời viết mới dựa trên dữ kiện (dữ kiện không có bản quyền, câu chữ thì có) |
| Đoạn trích phim điện ảnh (Vây Thành, Dị Vực, American Gangster…), poster, ảnh still | ❌ cho kênh này | Về luật, có thể bào chữa là fair use (đoạn ngắn, có bình luận). Nhưng hãng phim gần như chắc chắn đã đăng ký Content ID, video sẽ bị chuyển doanh thu cho họ hoặc bị chặn ở một số nước. Chỉ nhắc tên phim |
| Đoạn trích bản tin truyền hình (CNN, BBC, VTV, TVB…) | ❌ | Rủi ro Content ID và khiếu nại cao nhất, kể cả đoạn vài giây. Ghi nguồn hay chú thích "không có ý vi phạm" đều không có tác dụng |
| Ảnh báo chí hiện đại (AP, Reuters, Getty, báo Việt Nam) | ❌ | Có thể bị gỡ hẳn video (strike), không chỉ bị claim |
| Nhạc thương mại | ❌ | Chỉ dùng Kevin MacLeod (CC BY), YouTube Audio Library, Pixabay |

**Content ID claim và gậy bản quyền (strike) khác nhau:**
- **Claim** là đối sánh tự động. Kênh không bị phạt; video có thể bị chia hoặc mất doanh thu, hoặc bị chặn ở một số nước. Có thể kháng nghị.
- **Strike** là khi chủ sở hữu gửi yêu cầu gỡ có giá trị pháp lý. Video bị gỡ; 3 strike trong 90 ngày thì kênh bị xóa. Ảnh báo chí và đoạn trích phim là hai nguồn strike phổ biến nhất.

**Chính sách kiếm tiền (YPP):**
- **Reused content:** đã cho phép dùng lại tư liệu nếu có "bình luận, chỉnh sửa đáng kể, hoặc giá trị giáo dục". Video của kênh (kịch bản riêng, dựng đồ họa, dẫn chuyện) đáp ứng điều này.
- **Inauthentic content** (cập nhật 15/07/2025): rủi ro thật nằm ở đây. Video đúc khuôn hàng loạt, ít khác biệt giữa các video sẽ bị loại khỏi kiếm tiền. Loạt Shorts S-tier đăng dồn ngày 30/09 thuộc đúng vùng rủi ro này. Cần giữ mỗi video có góc kể riêng và không đăng hàng loạt.

**Giọng AI:**
- Giọng TTS dẫn chuyện không bắt buộc gắn nhãn.
- Phải khai báo "nội dung đã chỉnh sửa hoặc tổng hợp" nếu khiến người thật trông như nói hoặc làm điều họ không làm, hoặc dựng cảnh thật như đã xảy ra.
- Lời trích của nhân vật thật đọc bằng giọng minh họa phải luôn gắn nhãn "GIỌNG ĐỌC MINH HỌA" (engine đã làm) và không giả giọng nhân vật.
