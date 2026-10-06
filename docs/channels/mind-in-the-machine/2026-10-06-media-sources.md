# Nguồn tư liệu hình và clip cho Mind in the Machine (MIM), kiểm tra ngày 06/10/2026

**Phạm vi:** kiểm lại các công cụ tìm tư liệu cộng đồng (ảnh và clip có giấy phép mở) trong hai codebase, rồi đề xuất phần dùng lại, phần cần sửa và nguồn nên thêm cho Short 9:16 của MIM. MIM có hai dòng nội dung: *AI giải thích* (LLM, ảo giác, deepfake, token, GPU, thuật toán gợi ý…) và *công nghệ đã thay đổi thế giới* (ARPANET 1969, YouTube 2005–06, iPod 2001, mã QR 1994, transistor 1947, pin Li-ion, GPS, điện thoại 1876, truyền hình 1926, Edison, anh em Wright…).

**Phương pháp:**
- Đọc code v2 (`Youtube_Creator_V2`, bản đang có trên đĩa, gồm cả thay đổi chưa commit) và v1 (`vietneu-tts`, nhánh `origin/feat/content-hub-backend`).
- Gửi khoảng 31 truy vấn API công khai, không cần khóa, giãn cách khoảng 1 giây. User-Agent: `yt-factory-research/1.0 (https://github.com/nguyent0810/Youtube_Creator_V2)`.
- Đọc điều khoản trên trang chính thức của từng nguồn.
- Không tải file media, không đăng ký tài khoản, không dùng khóa API.

**Không sửa file nào khác.** Chỗ nào chưa chắc đều ghi **(chưa chắc)**. Tài liệu này không phải tư vấn pháp lý.

---

## 1. Tóm tắt

1. **Wikimedia Commons vẫn là nguồn chính cho dòng *công nghệ đã thay đổi thế giới*, nhưng chỉ mạnh với đồ vật trước khoảng năm 1990.**
   - Ảnh Public domain hoặc CC0 trong 40 kết quả tìm đầu tiên:
     - Điện thoại Bell 1876: 30
     - Wright Flyer 1903: 29
     - Vệ tinh GPS: 21
     - Máy hát Edison: 19
     - ARPANET: 18
   - Với đồ vật hiện đại thì gần như không có ảnh PD:
     - iPod: 3 trên 32 ảnh raster
     - GPU: 4 trên 36
     - Trung tâm dữ liệu: 2 trên 33
     - Pin Li-ion: 5 trên 37
   - Ở các chủ đề hiện đại này, phần lớn ảnh là **CC BY-SA**.
2. **Đường dựng Short (`motion/stier/build.py` `fetch_img`) đang chỉ nhận PD/CC0 và không lưu tác giả hay giấy phép.** Hai điểm liên quan:
   - Đường video dài (`build_long.fetch_img` cùng `describe.py`) và v1 (`hf_commons.fetch(allow_by=True)`) **đã có sẵn** cơ chế nhận CC BY và ghi công tự động. Chỉ cần đưa cơ chế này sang đường Short.
   - Mô tả video MIM (`enqueue_mim.py`) hiện **không có dòng ghi công ảnh nào**.
3. **Đề xuất cho MIM:**
   - Nhận thêm **CC BY**, có lưu tác giả, giấy phép và đường dẫn, rồi tự in vào mô tả.
   - Mặc định **không nhận CC BY-SA**. Chỉ cho vào khi người duyệt bật cờ cho từng file (lý do ở mục 6).
4. **Clip video cho nền 9:16:**
   - Pexels đã có code nhưng đang bị khóa cứng ở khổ ngang và đọc khóa từ `../video-editor/.env`. **File này không tồn tại trên máy này**, nên `pexels.py` lỗi ngay khi import.
   - Cần thêm `orientation=portrait` và chọn file dọc.
   - Pixabay (cần khóa miễn phí) là nguồn dự phòng. v1 đã có code ảnh Pexels/Pixabay khổ dọc (`stock_image.py`).
5. **Nên thêm NASA Image and Video Library:**
   - Không cần khóa. Phần lớn tư liệu không bị bảo hộ bản quyền ở Mỹ, có cả **video**.
   - Hợp chủ đề GPS, siêu máy tính, máy tính Apollo, vệ tinh.
   - Phải tránh logo NASA và không được ngụ ý NASA bảo trợ.
6. **Không dùng:**
   - Ảnh của Computer History Museum lấy từ trang của họ: dùng thương mại phải xin phép bằng văn bản.
   - Nhãn giấy phép trên Internet Archive: chúng tôi thấy chính mắt một đoạn *CBS News 1985* bị gắn "Public Domain Mark".
   - Ảnh "deepfake" trên Commons: phần lớn là ảnh AI có người thật, ví dụ Giáo hoàng mặc áo phao.
7. **Lỗi nhỏ phát hiện trong v2 `media_search.py`:**
   - Openverse ẩn danh từ chối `page_size=30` (lỗi 401, giới hạn là 20), nên nguồn này đang hỏng.
   - AIC xin ảnh 1686px mà không gửi `AIC-User-Agent`. v1 đã ghi nhận AIC trả 403 trong trường hợp này và đã sửa.

---

## 2. Nguyên tắc giấy phép cho MIM (kênh có kiếm tiền, video 9:16 có chỉnh sửa)

| Loại | MIM dùng? | Lý do / điều kiện |
|---|---|---|
| Public domain, PDM, CC0 | ✅ | Nên ghi nguồn cho minh bạch, dù luật không bắt buộc. Vẫn còn các quyền khác ngoài bản quyền: nhãn hiệu, quyền hình ảnh cá nhân ([Commons: Reusing content](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia)) |
| Tác phẩm của chính phủ liên bang Mỹ (NASA, NOAA, Không quân Mỹ vận hành GPS…) | ✅ | Không có bản quyền theo 17 U.S.C. §105 ([copyright.gov](https://www.copyright.gov/title17/92chap1.html#105)). NASA có thêm điều kiện riêng (mục 5) |
| CC BY 2.0–4.0 | ✅, phải ghi công | Ghi tác giả, tên giấy phép, link. Theo CC BY-SA 4.0 §3(a)(2), ghi công "in any reasonable manner based on the medium" là đủ ([legalcode](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en)). CC BY có cùng điều khoản này ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en)), nên ghi trong mô tả video là hợp lý |
| CC BY-SA | ⚠️ chỉ khi bật cờ cho từng file | Xem mục 6 |
| Pexels, Pixabay, Unsplash (giấy phép riêng) | ✅ | Được dùng thương mại và chỉnh sửa, không bắt buộc ghi công. Không đặt người nhận diện được vào ngữ cảnh xấu (mục 5) |
| NC, ND, "fair use", ảnh không rõ nguồn, ảnh báo chí, ảnh chụp màn hình phim hoặc TV | ❌ | Giống `motion/long/SOURCES.md` |
| Ảnh do AI tạo | ❌ (luật kênh) | Kể cả khi Commons ghi là "PD". Riêng tập deepfake: xem mục 7 |

---

## 3. Kiểm kê nguồn hiện có

### 3.1. v2: `Youtube_Creator_V2`

| Nguồn / file | Là gì | Giấy phép trả về | Kiểm tra và ghi công | Khóa / giới hạn | Đánh giá cho MIM |
|---|---|---|---|---|---|
| **Wikimedia Commons**: `stier/research.py`, `find.py`, `grab.py` | Lấy ảnh trong bài Wikipedia EN, thêm kết quả tìm Commons (`srnamespace=6`), lấy `imageinfo` và `extmetadata`, dựng bảng ảnh đánh số | Lọc `PD = public domain\|^pd\|cc0\|no restrictions`. Bỏ logo, SVG, cờ… (`SKIP`), cạnh ngắn phải ≥ 400px | Chỉ lưu `license`, `date`, `desc` vào `data/stier/research/<slug>.json`. **Không lưu Artist** | Không cần khóa. Mỗi lời gọi API nghỉ 0,4 giây. Gặp 429 thì lùi dần. UA chung chung `yt-factory/1.0 (… contact via channel)` | **Tốt** cho lịch sử công nghệ (bảng mục 4). **Yếu** cho phần cứng hiện đại nếu chỉ nhận PD |
| **Commons trong lúc dựng**: `stier/build.py` `fetch_img` | Tải ảnh cho spec Short, xin ảnh thu nhỏ cỡ chuẩn 1920/1280/960/500/330 để tránh lỗi 429 của `upload.wikimedia.org` | **Chặn cứng** mọi giấy phép không phải PD/CC0 (`SystemExit`) | **Không ghi file `.json` cạnh ảnh.** Không có dữ liệu ghi công. `enqueue_mim.py` chỉ ghi nguồn bài viết và ghi công nhạc | Như trên | Dùng lại được, nhưng phải sửa thì MIM mới dùng được CC BY (mục 8) |
| **Commons cho video dài**: `long/research_long.py` và `build_long.fetch_img` | Như trên nhưng có nhận thêm giấy phép mở | `FREE` = PD/CC0/CC BY/CC BY-SA. `BAD` = NC/ND/fair use | Ghi `<key>.json {file, license, artist}`. `describe.py` gom credit theo giấy phép, chỉ tính ảnh thực sự có trong cảnh | Như trên | Mẫu tốt để chuyển sang Short |
| **Openverse**: `long/media_search.py --src openverse` | Kho tổng hợp ảnh CC: Flickr, Wikimedia, rawpixel… | API lọc `license=cc0,pdm,by,by-sa`, rồi kiểm lại bằng regex `OK_LIC` | Ghi `ext.json` và `<key>.json {license, artist, title, source, page}` | Không cần khóa, nhưng **ẩn danh tối đa 20 kết quả mỗi trang**. Code gửi `page_size=30` nên **trả 401** (đã thử: `"page_size may not exceed 20 for anonymous requests"`) ([Openverse throttling](https://docs.openverse.org/api/reference/authentication_and_throttling.html)) | **Trung bình.** "ARPANET" có 105 kết quả: bản đồ ARPANET 1973 (CC BY, Eric Fischer, Flickr), ảnh Teletype (BY-SA). "server room" và "circuit board macro" nhiều ảnh Flickr CC BY, rawpixel CC0. Openverse **không kiểm chứng giấy phép** ([ToS](https://docs.openverse.org/terms_of_service.html)), nên dễ gặp ảnh Flickr bị "rửa giấy phép" |
| **Wellcome Collection**: `--src wellcome` | Lịch sử y học | Lọc `locations.license=cc-0,cc-by,pdm` | Như trên | Không cần khóa | **Không liên quan.** Thử "telephone": 10 kết quả hợp lệ, toàn hóa đơn và tranh y học; bỏ bộ lọc thì phần lớn là "inc" (còn bản quyền). Thử "computer" kèm bộ lọc: không có kết quả |
| **Art Institute of Chicago**: `--src artic` | Tranh, ảnh nghệ thuật | `is_public_domain` → CC0 ([AIC Open Access](https://www.artic.edu/open-access/open-access-images)) | Như trên | Không cần khóa. IIIF nên dùng **843px** ([API docs](https://api.artic.edu/docs/)). v1 ghi nhận 1686px hoặc thiếu header `AIC-User-Agent` thì bị 403, **v2 chưa sửa** | **Không liên quan.** Thử "telephone": 8/8 kết quả không phải PD, đều là tác phẩm nghệ thuật hiện đại |
| **Europeana**: `--src europeana` | Bảo tàng châu Âu | `reusability=open` = CC0/PDM/CC BY/BY-SA ([Europeana "Can I use it?"](https://pro.europeana.eu/post/can-i-use-it)) | Đọc `rights`, map sang nhãn giấy phép | Code dùng khóa demo `api2demo`. **Chúng tôi không thử** để tuân thủ yêu cầu không dùng khóa | **Yếu, (chưa chắc).** Có thể có ảnh điện thoại hoặc truyền hình đời đầu từ bảo tàng kỹ thuật châu Âu. Đáng thử khi đã có khóa riêng |
| **Sentinel-2**: `media_search.py sat` | Ảnh vệ tinh qua Microsoft Planetary Computer | Dữ liệu Copernicus. Bắt buộc ghi câu "Contains modified Copernicus Sentinel data" | Tự ghi câu bắt buộc | Truy cập ẩn danh | **Không liên quan**, trừ khi có tập về vệ tinh hoặc bản đồ |
| **Pexels video**: `long/pexels.py` | B-roll | Pexels License: thương mại, chỉnh sửa, không bắt buộc ghi công ([license](https://www.pexels.com/license/)) | `broll/index.json` lưu `user`, `slug`. Mô tả ghi chung "Pexels" | Cần khóa, đọc từ `../video-editor/.env`. **File này không có trên máy này.** API: 200 request mỗi giờ, 20.000 mỗi tháng; quy định API yêu cầu "prominent link to Pexels" ([API docs](https://www.pexels.com/api/documentation/)) | **Tốt** cho clip nền khái niệm AI: điện thoại, người lướt mạng, chip, máy chủ. Nhưng code **khóa cứng `orientation=landscape`** và loại file dọc (`w >= h`). Phải sửa cho 9:16 |
| **Ghi công**: `long/describe.py` | Ghi công cho video dài | Phân biệt PD và CC, ghi đúng câu bắt buộc của Copernicus | Chỉ ghi ảnh có trong cảnh, gom theo giấy phép | | Logic dùng lại được cho `enqueue_mim.py` |

### 3.2. v1: `vietneu-tts`, nhánh `origin/feat/content-hub-backend`

Nhánh `main` không có code tìm tư liệu. Các file liên quan đều ở nhánh này.

| File | Là gì | Giấy phép và ghi công | Giá trị cho MIM |
|---|---|---|---|
| `hf_commons.py` | Port từ v2, **có tham số `allow_by`**: PD/CC0, thêm CC BY/BY-SA khi bật. Loại NC/ND. Có `article_images(title, lang="vi"/"en")` | `fetch()` ghi `.json {file, license, credit}`. Credit = tên file, Artist, giấy phép, "Wikimedia Commons" | **Dùng lại logic.** Đây là bản tốt nhất để chuyển `allow_by` và dòng credit vào `stier/build.py`. Tham số `lang="vi"` hữu ích: lấy ảnh từ bài vi.wikipedia "Mã QR", "Thomas Edison" |
| `hf_openverse.py` | Openverse, `page_size=min(limit,20)` (đúng giới hạn ẩn danh). `fetch()` **kiểm lại giấy phép theo id** trước khi tải. Nguồn gốc lỗi thì dùng ảnh thu nhỏ | Credit = tiêu đề, tác giả, giấy phép, nguồn, "via Openverse". Có lưu `landing` | **Dùng lại.** Đã sửa đúng lỗi 401 mà v2 đang mắc |
| `hf_extmedia.py` | Port `media_search.py`: Wellcome, AIC, Europeana. **AIC 843px, có `AIC-User-Agent`, lọc kết quả AIC theo từ khóa** (AIC trả danh sách mặc định khi từ khóa không khớp) | Credit có tác giả, giấy phép, kho | Chỉ lấy **bản sửa AIC** để vá v2. Nội dung các kho này không hợp MIM |
| `hf_museum.py` | The Met, AIC, Cleveland (CC0) | Chỉ CC0. Ghi chú trong code: Met search trả 410 | **Không liên quan** (tranh, tượng) |
| `stock_image.py` | **Ảnh** Pexels, dự phòng Pixabay. Có `orientation=portrait`. Lấy bản `original` vì `large2x` khổ dọc chỉ khoảng 867×1300, thiếu cho khung 1080×1920 | `.source.json {provider, page, author, id, query}`. `credit_line()` → "Ảnh: <tác giả> — Pexels (<link>)" | **Dùng lại** cho ảnh nền khái niệm AI 9:16. Đọc khóa từ `video_tool_clone/.env` |
| `asset_generation.py` (`get_or_fetch_stock_video`) | Gọi script video-editor qua một venv riêng để tải clip Pexels/Pixabay | Không ghi tác giả, chỉ ghi bản ghi an toàn | **Không dùng.** Phụ thuộc video-editor và ComfyUI; phần sinh ảnh AI trái luật kênh |
| `asset_safety.py` | File phụ `.safety.json` (safe / unsafe / review_required) cạnh tư liệu. Kiểm trước khi đưa vào dựng, kể cả khi lấy từ cache | Không liên quan giấy phép | **Lấy ý tưởng:** đánh dấu clip hoặc ảnh "đã duyệt bằng mắt" và chặn file chưa duyệt. Chưa cần chuyển cả module |
| `hf_media_sheet.py` | Bảng ảnh xem trước gộp Commons, Openverse, X (ext), bảo tàng | | v2 đã có bảng ảnh riêng. Chỉ lấy ý tưởng **gộp nhiều nguồn trong một bảng** |
| `generate_symbol_assets.py`, `assets/symbol_library/` | **Tự vẽ** sơ đồ (Bát quái, Ngũ hành) từ dữ liệu đã tra, vì AI vẽ sai và ảnh trên mạng không rõ giấy phép | Tự sở hữu hoàn toàn | **Nguyên tắc rất hợp với *AI giải thích*:** token, attention, GPU song song, vòng gợi ý của thuật toán nên vẽ bằng HTML/SVG trong HyperFrames, không cần ảnh |

---

## 4. Kết quả thử truy vấn (06/10/2026)

**Bảng 4.1. Wikimedia Commons.** `generator=search`, namespace File, 40 kết quả đầu, phân loại theo `LicenseShortName`.

| Truy vấn | PD/CC0 | CC BY | CC BY-SA | Không phải ảnh raster | Ví dụ dùng được |
|---|---:|---:|---:|---:|---|
| ARPANET | 18 | 1 | 13 | 8 | PD: `Arpanet logical map, march 1977.png`, `Arpanet Completion Report Figure 3.png`, `DARPA ARPANET plaque 20110517.jpg` |
| Interface Message Processor | 8 | 11 | 15 | 6 | PD: `1969 ARPANET BBN IMP.jpg`, `First-arpanet-imp-log.jpg`. BY: `BBN Interface Message Processor CHM.agr.jpg` (ảnh khách chụp tại CHM, giấy phép CC BY của người chụp) |
| first transistor Bell Labs | 11 | 1 | 3 | 25 | PD: `Replica-of-first-transistor.jpg`. BY: `The First Transistor ever made, built in 1947 - Bell Labs.jpg` |
| Bell telephone 1876 | 30 | 1 | 0 | 9 | PD: `Bell "iron box" telephone receiver 1876.jpg`, `Bell liquid telephone transmitter 1876.png` |
| Wright Flyer 1903 | 29 | 1 | 8 | 2 | PD: `First flight2.jpg`, `1903-12 Wright-Flyer-side-view.jpg` |
| Edison phonograph | 19 | 3 | 14 | 4 | PD: `Edison and phonograph edit1.jpg`, `Edison Home Phonograph 1901.jpg` |
| Baird televisor | 4 | 3 | 9 | 21 | PD: `John Logie Baird and television receiver.jpg`. BY: `Baird television, 1929.jpg` |
| GPS satellite | 21 | 1 | 6 | 12 | PD: `GPS satellite constellation.jpg`, `GPS Satellite NASA art-iif.jpg` |
| QR code | 7 | 11 | 11 | 11 | PD: ảnh bảng quảng cáo QR ở Shibuya. **Nên tự tạo mã QR bằng code** |
| iPod | 3 | 9 | 20 | 8 | PD: `Ipod-classic-6th-gen.jpg`. BY: `IPod family.jpg`, `IPod line as of 2014.png` |
| lithium-ion battery cell | 5 | 6 | 26 | 3 | PD: `18650 and 21700 lithium ion battery cell.jpg` |
| graphics processing unit | 4 | 5 | 27 | 4 | BY: `EVGA GeForce GTX 590.jpg`, `GPU blade with glycol cooling` |
| data center servers | 2 | 5 | 26 | 7 | PD: `Data center roof.jpg`. BY: `Facebook Data Center Server Board.jpg` |
| deepfake | 21 | 1 | 6 | 12 | ⚠️ Phần lớn "PD" là **ảnh do AI tạo**, có cả người thật (`Pope Francis in puffy winter jacket.jpg`, ảnh giả biển Hollywood). Không dùng làm tư liệu |

**Nhận xét:**
- Nhận thêm CC BY làm tăng số ảnh dùng được khoảng 15–40% ở các chủ đề hiện đại.
- CC BY-SA chiếm phần lớn ảnh của các chủ đề hiện đại (20–27 trên 40), nên chính sách BY-SA là quyết định lớn nhất.

**Các nguồn khác:**
- **NASA Images** (`images-api.nasa.gov`, không khóa):
  - "GPS satellite": 240 kết quả. Trang đầu có 85 ảnh và **15 video**.
  - "supercomputer": 67 kết quả, gồm ảnh "Discover Supercomputer" của GSFC và video siêu máy tính của Ames.
  - "Apollo guidance computer": chỉ 2 kết quả.
  - Đánh giá: **tốt** cho GPS, vệ tinh, siêu máy tính, chip, máy tính thời Apollo; có video để làm clip nền.
- **Library of Congress:** cả `loc.gov/pictures/search/?fo=json` và `loc.gov/photos/?fo=json` đều trả **403** với script. Trùng với ghi chú cũ trong `SOURCES.md` (bị Cloudflare chặn). Phải tìm bằng tay hoặc qua bản sao trên Commons.
- **Internet Archive** ("ARPANET", phim): 82 kết quả, nhãn giấy phép lẫn lộn:
  - `CBS News - Hacking Segment (August 1985)` gắn **Public Domain Mark**. Gần như chắc chắn sai, vì đây là bản tin CBS.
  - Một phim Prelinger gắn `publicdomain`.
  - Các mục khác gắn BY-NC-SA hoặc BY-NC, hoặc không ghi gì.
  - Kết luận: không tin `licenseurl` của IA.

---

## 5. Nguồn nên thêm hoặc cân nhắc

| Nguồn | Giấy phép (trang chính thức) | Dùng trong video kiếm tiền | Ghi công | Khóa / API | Mức hợp với MIM |
|---|---|---|---|---|---|
| **NASA Image and Video Library** | Tư liệu NASA "generally are not subject to copyright in the United States". Dùng thương mại **không được ngụ ý NASA bảo trợ**. Logo và insignia NASA **không** thuộc public domain. Ảnh có người nhận diện được có thể vướng quyền hình ảnh. Tư liệu bên thứ ba được ghi rõ chủ sở hữu ([NASA media guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/)) | ✅, tránh logo hoặc "meatball" làm hình chính | Ghi "Nguồn: NASA" (không bắt buộc ở Mỹ nhưng nên ghi). Ghi cả trung tâm (JSC, GSFC…) | **Không cần khóa**: `https://images-api.nasa.gov/search?q=…&media_type=image,video` ([API docs PDF](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf)) | **Cao** cho GPS, vệ tinh, siêu máy tính, AI trong khoa học. Có video. **(chưa chắc):** mục của JPL (Caltech vận hành) có chính sách dùng ảnh riêng; mục có `secondary_creator` hoặc tên ngoài NASA phải đọc kỹ mô tả |
| **Smithsonian Open Access** | CC0 cho tư liệu có file media mở. Hiện vật còn vướng quyền thì chỉ có metadata, không có ảnh ([si.edu/openaccess](https://www.si.edu/openaccess), [devtools](https://www.si.edu/openaccess/devtools)) | ✅ | Không bắt buộc, nên ghi "Smithsonian" | Cần khóa **api.data.gov** miễn phí ([đăng ký](https://api.data.gov/signup/)). Gốc API `https://api.si.edu/openaccess/api/v1.0`. **Chưa thử** vì không dùng khóa | **Cao, (chưa chắc).** National Museum of American History có điện thoại, đèn Edison, máy tính đời đầu. Cần thử để biết tỉ lệ có ảnh CC0. Trang si.edu chặn WebFetch (403), thông tin lấy từ trang devtools và kết quả tìm kiếm |
| **Library of Congress**, bộ "Free to Use and Reuse" | Tư liệu "no known copyright restrictions" ([loc.gov/free-to-use](https://www.loc.gov/free-to-use/), [blog LoC](https://blogs.loc.gov/loc/2018/02/free-to-use-and-reuse-making-public-domain-and-rights-clear-content-easier-to-find/)) | ✅ với từng bộ đã gắn nhãn. Các mục khác phải đọc "Rights and Access" của từng bộ sưu tập | Nên ghi "Library of Congress" và số hiệu | API JSON (`?fo=json`) bị **403** từ script hôm nay. Phải tìm bằng tay | **Trung bình.** Ảnh anh em Wright, Edison, Bell có nhiều trên LoC, phần lớn đã có bản sao trên Commons. **Tìm qua Commons trước** |
| **Flickr Commons** ("No known copyright restrictions") | Tổ chức tự xác nhận, **không bảo đảm**. Người dùng tự chịu trách nhiệm phân tích ([Flickr Foundation](https://www.flickr.org/programs/flickr-commons/no-known-copyright-restrictions-how-it-works/), [usage](https://www.flickr.com/commons/usage)) | ⚠️ dùng được, nhưng phải lưu link và tên tổ chức | Nên ghi tổ chức | Flickr API cần khóa. Bản sao thường đã có trên Commons hoặc Openverse **(chưa chắc Openverse có map NKCR thành `pdm` không)** | **Thấp đến trung bình** (ảnh lưu trữ cũ) |
| **Pixabay** (ảnh và **video**) | Pixabay Content License: thương mại, chỉnh sửa, không bắt buộc ghi công. Cấm bán lại nguyên dạng "standalone" ([license summary](https://pixabay.com/service/license-summary/)). Một số nội dung có thể bị Content ID nhận; gỡ claim bằng License Certificate ([blog Pixabay](https://pixabay.com/blog/posts/how-to-clear-a-youtube-content-id-claim-with-a-pix-190/)) | ✅ | Không bắt buộc. API yêu cầu cho người dùng biết nguồn ảnh khi hiển thị kết quả tìm | Cần khóa miễn phí. 100 request mỗi 60 giây, **cache kết quả 24 giờ**, cấm tải hàng loạt có hệ thống ([API docs](https://pixabay.com/api/docs/)). Trang license và docs trả 429 với WebFetch hôm nay, nội dung lấy từ kết quả tìm trên pixabay.com | **Trung bình đến cao** cho clip khái niệm (mạch điện, mã chạy, người dùng điện thoại). Chọn clip dọc bằng cách lọc `width < height` **(chưa chắc API video có tham số orientation)** |
| **Pexels video** (đã có code) | Như mục 3.1. Cấm đặt người nhận diện được vào ngữ cảnh xấu, cấm ngụ ý bảo trợ ([license](https://www.pexels.com/license/)) | ✅ | Không bắt buộc. API yêu cầu link Pexels; mô tả nên ghi "Video: <tác giả> / Pexels" | Có `orientation=portrait`, `size=medium` (Full HD) ([API docs](https://www.pexels.com/api/documentation/)) | **Cao** cho nền 9:16 của *AI giải thích*. **Cẩn thận:** cảnh người thật cầm điện thoại trong tập deepfake hoặc lừa đảo có thể thành "ngữ cảnh xấu" với người trong clip. Chọn clip không thấy rõ mặt |
| **Unsplash** (ảnh) | Unsplash License: thương mại, chỉnh sửa, không bắt buộc ghi công. Cấm bán nguyên dạng, cấm dựng dịch vụ cạnh tranh ([license](https://unsplash.com/license)) | ✅ | **Qua API thì bắt buộc** ghi "Photo by X on Unsplash" kèm link ([attribution guideline](https://help.unsplash.com/en/articles/2511315-guideline-attribution)) | Cần khóa. Demo 50 request mỗi giờ. API **bắt buộc hotlink** và gọi endpoint download ([docs](https://unsplash.com/documentation)) | **Trung bình.** Hợp ảnh tĩnh sản phẩm, máy chủ, chip. **(chưa chắc)** quy định hotlink có khớp với việc tải về để render video không. An toàn hơn: tìm và tải bằng tay trên web theo Unsplash License, hoặc gọi endpoint download và ghi công đầy đủ. Không có video |
| **Wikimedia Commons CC BY** | Phải ghi tác giả, giấy phép, link. Ghi tác giả gốc, không ghi người tải lên ([Commons reuse](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia)) | ✅ | Trường `Artist`, `LicenseShortName`, `LicenseUrl`, `AttributionRequired`, `Attribution` trong `extmetadata` | Như hiện tại | **Cao.** Bổ sung đồ vật hiện đại |
| **Wikimedia Commons CC BY-SA** | Xem mục 6 | ⚠️ | | | Nhiều ảnh nhất, nhưng rủi ro về điều kiện "chia sẻ tương tự" |
| **Computer History Museum** (trang computerhistory.org) | Dùng thương mại **phải có văn bản cho phép** ([CHM Terms](https://computerhistory.org/terms/)) | ❌ (trừ khi xin phép) | | | Không dùng ảnh từ trang CHM. **Được dùng** ảnh trên Commons do khách tham quan tự chụp hiện vật tại CHM, theo giấy phép của người chụp (ví dụ `BBN Interface Message Processor CHM.agr.jpg`, CC BY) |
| **Internet Archive / Prelinger** | IA không bảo đảm tình trạng bản quyền, người dùng tự chịu rủi ro ([help.archive.org rights](https://help.archive.org/help/rights/)) | ⚠️ chỉ phim Prelinger đã đối chiếu, đoạn ngắn, bỏ tiếng gốc | Ghi tên phim và link | Không cần khóa (advancedsearch) | **Thấp.** Nhãn sai thấy ngay trong kết quả thử. Rủi ro Content ID với phim PD (`SOURCES.md` mục 3) |
| **Mixkit, Coverr** (video) | Trong `SOURCES.md`; **không kiểm lại hôm nay** | ✅ nếu đúng "Free License" | | Không có API chính thức **(chưa chắc)** | Tìm tay khi Pexels và Pixabay thiếu clip dọc |

---

## 6. CC BY và CC BY-SA trong một Short motion graphic

- **CC BY:** ghi công trong mô tả là cách "reasonable based on the medium" ([CC BY-SA 4.0 §3(a)(2)](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en); [CC FAQ](https://creativecommons.org/faq/)). Không phát sinh nghĩa vụ đặt giấy phép cho video. → **Nhận cho MIM.**
- **CC BY-SA:** nếu bản dùng là "Adapted Material" (dịch, sửa, biến đổi theo cách cần xin phép, §1(a)) thì phần chuyển thể phải phát hành dưới BY-SA hoặc giấy phép tương thích (§3(b)). Engine MIM cắt khung, Ken Burns, phủ **tông màu theme** và chữ lên ảnh, nên khả năng cao bị coi là chuyển thể.
  - **(chưa chắc)** Một ảnh đặt nguyên trong video có thể chỉ là "collection" chứ không phải chuyển thể. Ranh giới này CC không nói rõ cho hình trong video.
  - YouTube chỉ cho chọn "Creative Commons – Attribution" cho video ([YouTube Help](https://support.google.com/youtube/answer/2797468), **không kiểm lại hôm nay**), nên không có cách nào gắn BY-SA trên nền tảng.
  - Quyết định #5 trong `2026-10-06-stier-design.md` đã chọn loại BY-SA vì lý do này.
- **Đề xuất:**
  - Mặc định **chặn BY-SA**.
  - Chỉ cho phép BY-SA cho **một ảnh chủ đạo không có thay thế** (ví dụ ảnh replica transistor), với điều kiện:
    1. Spec ghi `"by_sa_ok": true`.
    2. Hiển thị ảnh **không phủ màu** (khung "print").
    3. Mô tả ghi rõ tác giả, giấy phép, link, và câu "ảnh giữ nguyên giấy phép CC BY-SA".
  - Người duyệt cần quyết điều này một lần cho cả kênh.

---

## 7. Rủi ro riêng của chủ đề MIM

1. **Nhãn hiệu và logo** (Apple, iPod, YouTube, NVIDIA, NASA): giấy phép bản quyền của ảnh không phủ nhãn hiệu ([Commons reuse](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia)). Logo NASA không thuộc public domain ([NASA](https://www.nasa.gov/nasa-brand-center/images-and-media/)).
   - Không dùng logo làm hình chủ đạo hoặc thumbnail.
   - Nhắc tên sản phẩm trong lời là bình thường.
   - Bộ lọc `SKIP` hiện có đã loại file có "logo" trong tên.
2. **YouTube 2005–06:** "Me at the zoo" và ảnh chụp giao diện YouTube là nội dung có bản quyền hoặc nhãn hiệu. Dựng lại bằng HTML (khung trình phát cách điệu, không logo) và mốc thời gian. **Chưa thử truy vấn Commons cho chủ đề này.**
3. **Mã QR:** tự sinh mã bằng code (ví dụ mã trỏ tới link nguồn). Không cần ảnh.
4. **Deepfake:**
   - Ảnh "deepfake" trên Commons là ảnh AI có người thật (Giáo hoàng). Trái luật "không ảnh AI" của kênh, lại vướng quyền hình ảnh.
   - Nên minh họa bằng sơ đồ tự vẽ (khuôn mặt cách điệu, lưới điểm mốc) hoặc clip stock không thấy rõ mặt.
   - Nếu buộc phải chiếu một deepfake nổi tiếng làm ví dụ: đóng dấu "ẢNH GIẢ DO AI" trên khung và không cắt khung theo cách làm ảnh trông như thật.
5. **Ảnh do AI tạo bị gắn nhãn PD trên Commons:** thêm vào `SKIP` các từ "AI-generated", "deepfake", "Stable Diffusion", "Midjourney", "DALL-E", và kiểm cả `Category:AI-generated images` **(chưa chắc tên category)**.
6. **Rửa giấy phép trên Flickr/Openverse:** chỉ nhận ảnh khi tài khoản đăng là người chụp hoặc là tổ chức (luật đã có trong `SOURCES.md`). Với file Commons gốc từ Flickr, ưu tiên file có mẫu "Flickr review" đã qua kiểm duyệt **(chưa chắc tên mẫu hiện hành)**.
7. **Người thật trong clip stock:** Pexels cấm đặt người nhận diện được vào ngữ cảnh xấu ([Pexels](https://www.pexels.com/license/)). Tập lừa đảo hoặc deepfake dùng clip tay, màn hình, bóng người.

---

## 8. Kế hoạch theo thứ tự ưu tiên

### A. Dùng nguyên như hiện có
1. `stier/research.py`, `find.py`, `grab.py`: tìm ảnh PD trên Commons cho dòng *công nghệ đã thay đổi thế giới*: Bell 1876, Wright 1903, Edison, ARPANET/IMP, transistor replica, GPS.
2. Bảng ảnh đánh số để chọn bằng mắt.
3. Ghi công nhạc trong `enqueue_mim.py`.
4. Nguyên tắc trong `motion/long/SOURCES.md` (mục 3, 5, 6, 7) áp dụng nguyên cho MIM.

### B. Dùng lại, có sửa code
Sửa riêng theo theme `mim`, không đổi hành vi của CL.

1. **`stier/build.py` `fetch_img`: cho phép CC BY và ghi lại thông tin.**
   - Nhận tham số `allow_by` từ `themes.theme(spec)` (MIM bật, CL tắt) hoặc từ `spec["allow_by"]`.
   - Dùng regex `FREE`/`BAD` giống `build_long`. BY-SA chỉ được nhận khi `spec["by_sa_ok"]` chứa tên file đó.
   - Luôn ghi `<key>.json` cạnh ảnh với các trường `{file, license, license_url, artist (bỏ HTML), attribution_required, page: "https://commons.wikimedia.org/wiki/<file>"}`, lấy từ `extmetadata` các trường `LicenseShortName`, `LicenseUrl`, `Artist`, `AttributionRequired`, `Attribution`.
   - Giữ nguyên cách xin ảnh thu nhỏ 1920/1280/960 để tránh 429.
   - Mẫu code: `build_long.fetch_img` và v1 `hf_commons.fetch`.
2. **`enqueue_mim.py`: thêm khối "🖼 ẢNH / 🎬 VIDEO".**
   - Đọc `<key>.json` của các ảnh **có xuất hiện trong cảnh** (cách làm của `describe.py`).
   - Gom theo giấy phép. PD ghi gọn "và N ảnh phạm vi công cộng (Wikimedia Commons, NASA)".
   - Clip stock ghi "Video: <tác giả> / Pexels" kèm link.
3. **`stier/research.py`, `find.py`: thêm cờ `--by`** để hiện cả ảnh CC BY, gắn nhãn giấy phép trên bảng ảnh (v2 `media_search.sheet` đã có). Đổi UA sang chuỗi có URL repo như ở đầu tài liệu này.
4. **`media_search.py`:**
   - Openverse `page_size` 30 → **20** (sửa lỗi 401).
   - AIC: 1686 → **843** và thêm header `AIC-User-Agent` (theo v1 `hf_extmedia`).
   - Lọc kết quả AIC theo từ khóa.
   - Thêm `fetch` theo id có kiểm lại giấy phép (theo v1 `hf_openverse.fetch`).
5. **`long/pexels.py` → bản cho Short (`stier/pexels9x16.py` hoặc thêm tham số):**
   - Đọc `PEXELS_API_KEY` từ biến môi trường trước, `.env` sau. Không đọc được thì báo lỗi rõ ràng, không crash lúc import.
   - Dùng `orientation=portrait`, `size=medium`, chọn file `h > w` và `h ≤ 1920`. Thiếu thì lấy file ngang ≥ 1920 rồi crop giữa.
   - Kiểm HDR (`color_transfer`) như `SOURCES.md`.
   - Ghi `user.name`, `user.url`, `url` vào index để ghi công.
   - Giới hạn clip 3–6 giây, tắt tiếng, đặt sau lớp chữ động.
6. **Ảnh stock tĩnh:** chuyển v1 `stock_image.py` (Pexels, dự phòng Pixabay, khổ dọc, bản `original`, `.source.json`, `credit_line`) sang v2. Chỉnh đường khóa cho đúng v2.
7. **Ảnh landscape trên khung 9:16:** phần lớn ảnh Commons/NASA là ảnh ngang, thu nhỏ 1920 rộng chỉ cao khoảng 1280px.
   - Dùng khung thẻ hoặc "print" của theme MIM, không ép tràn khung.
   - Không xin `iiurlheight` cỡ lạ, vì cỡ không chuẩn dễ dính 429 **(chưa chắc)**.
8. **Bộ lọc:** thêm các từ khóa ảnh AI vào `SKIP` (mục 7.5).

### C. Thêm mới
1. **NASA Images** (`media_search.py --src nasa` và `get`):
   - Gọi `images-api.nasa.gov/search`, rồi `/asset/{nasa_id}` để lấy file `~medium`/`~large` hoặc mp4.
   - Ghi `{license: "NASA (không bảo hộ bản quyền tại Mỹ)", center, secondary_creator, page}`.
   - Chặn mục có tên chủ sở hữu bên thứ ba trong mô tả, đánh dấu cần xem mục của JPL.
   - Ưu tiên cao nhất vì không cần khóa và có video.
2. **Smithsonian Open Access** (sau khi người dùng tự đăng ký khóa api.data.gov):
   - Gọi `api.si.edu/openaccess/api/v1.0/search` với `q=…`, lọc `online_media_type:Images` **(chưa chắc tên trường lọc)**, chỉ nhận mục có media CC0.
   - Thử trước 5 chủ đề: telephone, Edison lamp, transistor, iPod, GPS receiver.
3. **Pixabay API** (khóa miễn phí, người dùng tự đăng ký): dự phòng cho clip và ảnh. Cache 24 giờ theo yêu cầu API. Lưu License Certificate khi có claim.
4. **Europeana với khóa riêng:** thử "telephone 1876", "television Baird", "transistor". Chỉ giữ nếu kết quả tốt.
5. **Thư viện sơ đồ tự vẽ cho *AI giải thích*** (theo tinh thần v1 `symbol_library`): token hóa câu tiếng Việt, xác suất từ tiếp theo, GPU song song so với CPU, vòng gợi ý của thuật toán, lưới điểm mốc khuôn mặt cho deepfake. Không vướng giấy phép và khác biệt giữa các video, giúp tránh rủi ro "inauthentic content".
6. **Tìm bằng tay** (không làm API): LoC Free to Use, Flickr Commons, Unsplash (ghi công theo hướng dẫn), Mixkit/Coverr cho clip dọc.

### Không làm
- Ảnh hoặc video lấy từ trang Computer History Museum.
- Dựa vào nhãn giấy phép của Internet Archive.
- Ảnh AI hoặc ảnh "deepfake" trên Commons.
- Ảnh chụp màn hình YouTube, Apple hoặc báo chí.
- Phần sinh ảnh AI trong `asset_generation.py` (ComfyUI).

---

## 9. Điều chưa chắc
- Một ảnh BY-SA đặt trong video có chỉnh màu hoặc crop là "collection" hay "adaptation". CC không trả lời rõ cho trường hợp này.
- Tỉ lệ hiện vật công nghệ có ảnh CC0 trên Smithsonian. Chưa thử vì cần khóa.
- Quy định hotlink của Unsplash API có khớp với việc tải về để render hay không.
- Pixabay video API có tham số orientation hay không.
- Chính sách dùng ảnh riêng của JPL.
- Cách Openverse map nhãn Flickr NKCR.
- LoC chặn script do User-Agent hay chặn mọi truy cập tự động.
- Các trang Pixabay, si.edu, loc.gov và openverse.org/terms trả 429 hoặc 403 với WebFetch hôm nay. Thông tin về các nguồn này lấy từ kết quả tìm kiếm trên chính tên miền đó hoặc từ tài liệu phụ chính thức (docs.openverse.org, si.edu/openaccess/devtools).

## 10. Nguồn
- Pexels License: https://www.pexels.com/license/ · Pexels API: https://www.pexels.com/api/documentation/
- Pixabay Content License: https://pixabay.com/service/license-summary/ · API: https://pixabay.com/api/docs/ · Content ID: https://pixabay.com/blog/posts/how-to-clear-a-youtube-content-id-claim-with-a-pix-190/
- Unsplash License: https://unsplash.com/license · API docs: https://unsplash.com/documentation · Attribution: https://help.unsplash.com/en/articles/2511315-guideline-attribution
- NASA media guidelines: https://www.nasa.gov/nasa-brand-center/images-and-media/ · API: https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf
- 17 U.S.C. §105: https://www.copyright.gov/title17/92chap1.html#105
- Smithsonian Open Access: https://www.si.edu/openaccess · https://www.si.edu/openaccess/devtools · https://api.data.gov/signup/
- Library of Congress: https://www.loc.gov/free-to-use/ · https://blogs.loc.gov/loc/2018/02/free-to-use-and-reuse-making-public-domain-and-rights-clear-content-easier-to-find/
- Flickr Commons: https://www.flickr.org/programs/flickr-commons/no-known-copyright-restrictions-how-it-works/ · https://www.flickr.com/commons/usage
- Computer History Museum Terms: https://computerhistory.org/terms/
- Internet Archive Rights: https://help.archive.org/help/rights/
- Openverse ToS: https://docs.openverse.org/terms_of_service.html · Throttling: https://docs.openverse.org/api/reference/authentication_and_throttling.html
- Art Institute of Chicago: https://www.artic.edu/open-access/open-access-images · https://api.artic.edu/docs/
- Europeana: https://pro.europeana.eu/post/can-i-use-it · https://www.europeana.eu/en/rights/terms-of-use
- Creative Commons: https://creativecommons.org/licenses/by-sa/4.0/legalcode.en · https://creativecommons.org/licenses/by/4.0/legalcode.en · https://creativecommons.org/faq/
- Wikimedia Commons reuse: https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia
- YouTube Creative Commons: https://support.google.com/youtube/answer/2797468 (không kiểm lại hôm nay)
