# Hồ sơ S-tier: kỹ năng dựng motion graphic cho Short hình sự

Mỗi video là một vụ án có thật, kể trong khoảng 28–36 giây. Hình ảnh là tư liệu gốc thuộc phạm vi công cộng, không dùng ảnh AI. Chuyển động bám theo mốc thời gian của **từng chữ** trong giọng đọc.

Một vụ án = **một file spec JSON**. Mọi thứ còn lại (giọng, mốc từ, ảnh, bản đồ, HTML, âm thanh, render, ghép tiếng) chạy tự động. Mỗi video mất khoảng 2 phút trên máy 12 nhân.

Video mẫu làm tay: `motion/hf/compositions/monalisa.html` (vụ trộm Mona Lisa 1911). Engine chung là bản tổng quát hoá của file này.

## Ngôn ngữ hình ảnh (xu hướng 2026 đã nghiên cứu)

**Nên làm:**
- **Cắt dán hồ sơ lưu trữ.** Giấy cũ, ảnh in viền trắng, băng dính, con dấu đỏ, vạch đen che tên.
- **Chữ động là hình chính.** Chữ lớn đập vào đúng lúc chữ đó được đọc.
- **Ngữ pháp phim tài liệu tiết chế.** Dùng ngày tháng số lật, bản đồ tự vẽ, máy quay lia trên trang báo.
- **Một màu nhấn duy nhất** (đỏ son `--red`). Phụ đề trắng 2–4 chữ, chữ quan trọng tô đỏ.
- **Âm thanh.** Nền trầm liên tục. Tiếng đập chỉ đặt ở khoảnh khắc lật. **Lặng hẳn** trước câu chốt (cảnh `question`).
- **Kết vòng lặp.** Cảnh cuối trùng cảnh đầu (`hero` + `loop`) để người xem xem lại.

**Tránh (đã thành sáo mòn):** bảng dây đỏ, glitch/VHS tràn lan, phụ đề kiểu Hormozi.

**Tránh lặp khuôn (chính sách "inauthentic content" của YPP, 07/2025):** mỗi vụ phải đổi thứ tự và loại cảnh.

## Các file

| File | Vai trò |
|---|---|
| `motion/hf/assets/engine/casefile.js` | Engine: 19 loại cảnh, dựng từ `window.CASE`. Tất định: không Math.random/Date/fetch. |
| `motion/hf/assets/engine/casefile.css` | Toàn bộ style (khung 1080x1920). |
| `motion/stier/build.py` | spec → TTS → mốc từng từ (hf_align) → tải ảnh PD → bản đồ (hf_geo) → data.js + HTML → sfx → render → ghép tiếng. |
| `motion/stier/sfx.py` | Âm thanh tổng hợp bằng numpy, đặt đúng các mốc của từng loại cảnh. |
| `motion/stier/research.py` | Lấy bài Wikipedia EN + ảnh Commons **chỉ giữ Public domain/CC0**. Kèm bảng ảnh đánh số để chọn bằng mắt. |
| `motion/stier/find.py`, `grab.py`, `peek.py` | Tìm ảnh PD, trích đoạn quanh từ khoá để đối chiếu dữ kiện. |
| `motion/stier/w.py`, `count.py` | Ghi spec và đếm số từ (mục tiêu ≤ 130 âm tiết ≈ 35 giây). |
| `motion/stier/queue2.sh` | Hàng đợi dựng nền. Chạy nhiều luồng song song, mỗi spec khoá bằng `mkdir`. |
| `data/stier/specs/*.json` | Spec từng vụ (nội dung đã viết). |

## Spec

```json
{
 "title": "...", "description": "...", "tags": ["..."],
 "kicker": "HỒ SƠ 1911", "sub": "VỤ TRỘM MONA LISA",
 "acc": ["chữ", "tô", "đỏ"],
 "lines": ["Mỗi phần tử là MỘT câu đọc.", "..."],
 "imgs": {"key": "File:Tên file trên Commons.jpg"},
 "map": {"countries": [], "context": [], "labels": {}, "bbox": [], "pins": [{"name": "", "lon": 0, "lat": 0, "label": ""}]},
 "scenes": [ {"type": "hero", "img": "key", "intro": true, "head": "TIÊU ĐỀ"}, {"type": "date", "at": 2, "...": "..."} ],
 "sources": ["link bài gốc"]
}
```

**Mốc thời gian.** Dùng cho `at`, `until`, `reveal`, `strike`, `swap`, `plusAt`, `dayAt`, `headAt`, `signAt`, `labelAt`, `imgAt`, `dimAt`, `groupAt[]`, `headTimes[]`:

| Cách viết | Nghĩa |
|---|---|
| `3` | Đầu câu 3. |
| `[3, "chữ"]` | Lúc đọc chữ đó trong câu 3. |
| `[3, "chữ", 1]` | Lần xuất hiện thứ 2 của chữ đó. |
| `[3, "chữ", 0, -0.2]` | Lệch sớm 0,2 giây. |
| `[3, null, 0, 0.3]` | Đầu câu 3 cộng 0,3 giây. |

Viết sai chữ neo là **lỗi cứng**, build dừng ngay trước khi tốn thời gian render.

Riêng `at` ở cấp cảnh là thời điểm cảnh bắt đầu. Cảnh kéo dài tới khi cảnh sau bắt đầu.

## 19 loại cảnh

| Loại | Dùng cho | Tham số chính |
|---|---|---|
| `hero` | Mở / kết vòng | `img`, `frame` (gold/print), `intro`, `loop`, `head`, `strike`, `tape{text,at}`, `shatter{at,text}` |
| `date` | Ngày tháng số lật | `date`, `day`, `bg`, `groupAt[]`, `sub{text,at}`, `stamp{text,at}` |
| `doc` | Máy quay lia trang báo / tài liệu | `img`, `moves[{at,x,y,z}]`, `tag{text,hidden,reveal}`, `credit` |
| `photo` | Ảnh tràn khung / ảnh in, vòng khoanh đỏ | `img`, `mode` (full/print), `focus`, `circles[{x,y,at}]`, `label`, `stamp` |
| `counter` | Số đếm lớn | `to`, `from`, `prefix`, `suffix`, `until`, `label`, `sub`, `img` |
| `calendar` | N ô bị gạch | `n`, `unit`, `title` (`*nhấn*`) |
| `clock` | Kim quay, "+N" | `from`, `to`, `swap`, `plus`, `plusAt`, `turns` |
| `file` | Thẻ hồ sơ giấy, lật 3D + con dấu | `k`, `name`, `desc`, `img`, `stamp` |
| `crowd` | Đám đông bóng đen ngược sáng | `object`, `label` |
| `map` | Biên giới thật tự vẽ, ghim, tuyến đường (+ mugshot / song sắt) | `pins[]`, `routes[]`, `zoom`, `mug`, `stamp`, `bars`, `big` |
| `mug` | Ảnh hồ sơ tội phạm, gỡ vạch tên, con dấu, song sắt | `mug{img,name,at,reveal}`, `stamp`, `bars`, `big`, `ghost` |
| `question` | Câu hỏi trong **lặng** | `text` |
| `quote` | Trích dẫn gõ máy chữ | `text`, `by` |
| `kinetic` | Chữ lớn xếp tầng | `items[{text,at,acc,size,serif}]` |
| `evidence` | Tang vật dưới đèn | `img`, `tag`, `callouts[]` |
| `split` | Hai ảnh đối chiếu + dấu | `a`, `b`, `sign`, `title` |
| `timeline` | Mốc năm | `items[{year,text,at}]` |
| `ledger` | Sổ sách, bảng liệt kê | `title`, `rows[{k,v,at}]`, `total` |
| `slam` | Một dòng chữ đập mạnh | `text`, `sub`, `bg`, `white` |

## Quy tắc nội dung

1. Mọi dữ kiện (ngày tháng, con số, trích dẫn) phải đối chiếu được với bài nguồn trong `sources`. Chỗ nào là diễn ý thì ghi rõ "DIỄN Ý". Không bịa lời trích.
2. Ảnh chỉ lấy từ Public domain/CC0. `build.py` kiểm lại giấy phép lúc tải và dừng nếu không phải PD.
3. Không đưa ảnh thi thể hay ảnh gây sốc.
4. Không lặp chủ đề đã có trên kênh. Kiểm bằng `data/channel_titles/CL.json` và `factory/lines/novelty.py`.

## Chạy

```bash
python motion/stier/research.py <slug>          # tư liệu + bảng ảnh
python motion/stier/build.py <slug> --draft     # bản nháp
sh motion/stier/queue2.sh A &                   # dựng nền mọi spec chưa có final.mp4 (chạy thêm B, C… để song song)
```

**Yêu cầu:**
- Node ≥ 22. Nếu Node hệ thống cũ hơn thì dùng `npx -p node@22 -p hyperframes@0.8.75`.
- ffmpeg có trong PATH.
- vieneu TTS, giọng "Anh Khôi".

**Lưu ý khi tải ảnh:** upload.wikimedia.org **chặn tải bản gốc (lỗi 429)**. Phải xin ảnh thu nhỏ ở cỡ chuẩn 1920/1280/960 px nhỏ hơn bản gốc. `build.py` đã tự xử lý việc này.
