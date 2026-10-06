# Thiết kế bước 4: một hợp đồng Bundle + một kho cho mọi format (đề xuất 2 của audit)

Chốt sau phản biện Claude ↔ Grok (thiết kế) và review triển khai. Liên quan:
[`2026-10-05-audit.md`](2026-10-05-audit.md) mục 2, [`2026-10-05-channel-design.md`](2026-10-05-channel-design.md).

## Vấn đề

| Format | Trước bước 4 |
|---|---|
| Short thường (FS/BUD/CL) | Bundle → `item` → `run_batch` → `publish_batch` |
| Hồ sơ S-tier (CL `cl-hs-`) | Bundle **lách validate** bằng `broll_queries=["hyperframes-casefile"]` |
| Video dài (`motion/long`) | **Không có Bundle, không có hàng `item`** -- chỉ `output/long/<topic>/pub/result.json` |
| Hai worker TTS/dựng | `next_batch` không giành gì: hai worker nhận cùng lô, làm hai lần |
| MIM (project chưa audit) | Upload API bị khoá private vĩnh viễn -- cần đường upload tay mà sổ vẫn thấy |

## Thiết kế

1. **Bundle.render** -- trường tuỳ chọn `{"engine", "spec"}`; `schema_version` vẫn là 1 (bundle cũ đọc được,
   thiếu khoá = `assemble`). `ENGINES = assemble | casefile | casewide`. Engine khác `assemble` bắt buộc có
   `render.spec` và không cần `broll_queries`. Kênh hợp lệ đọc từ `channels.CHANNELS` (MIM được nhận).
2. **Cột `item.engine`** -- lần đầu thêm cột thì suy từ slug cho hàng cũ (`cl-hs-%` → casefile, `long-%` →
   casewide, còn lại assemble). `next_batch(engine=...)` lọc; `publish_batch` không lọc (đăng mọi engine).
3. **`store.claim` / `release`** -- giành MỘT hàng trong `BEGIN IMMEDIATE`, lease 30 phút
   (`claimed_by`, `lease_until`). Mọi cách kết thúc hàng (`mark`, `bump_attempt`, `reject`, `defer`,
   `requeue_failed`) thả lease. `run_batch` giành từng hàng (engine `assemble`), thả khi dừng giữa chừng.
4. **Video dài vào kho** -- `publish_long.long_bundle()` dựng Bundle `long-<topic>` (engine `casewide`, spec
   `data/long/<topic>/spec.json`, lời đọc = câu của mọi chương); `register()` lưu Bundle (giữ bản đầu -- bất biến)
   + enqueue + `assembled`. `result.json` có `video_id` → `published`.
5. **Kênh upload tay** -- `channels.CHANNELS[ch]["upload"] = "manual"` (MIM). `Channel.upload` ném
   `ManualChannel` cho MỌI đường đăng; `publish_batch probe/run` thoát sớm (không để lô đếm là hỏng).
   - `scripts/export_manual.py` → `output/manual/<CH>/<slug>/{<slug>.mp4, meta.txt, thumbnail.*}`; meta.txt có
     tiêu đề, mô tả (y như đường API, + `#Shorts`, + dòng cuối token), tag (+ token), giờ VN gợi ý.
   - Người upload qua Studio (Private + Schedule).
   - `scripts/adopt_manual.py` → `list_uploads(50)` (channels + playlistItems + videos.list = 3 unit, không
     `search.list`) → khớp token → `Channel.adopt` ghi `upload_log` → item `published`.

## Quyết định

| # | Quyết định | Vì sao |
|---|---|---|
| 1 | `render` là trường tuỳ chọn, **không** tăng `schema_version` | 347 bundle trên đĩa vẫn đọc được; tăng version buộc migrate hàng loạt mà không thêm an toàn nào |
| 2 | Category giữ ở `Upload` (đọc `spec["youtube"]`), không vào Bundle | Chỉ video dài cần; thêm trường bắt buộc vào hợp đồng cho một format là sai chỗ |
| 3 | Claim từng hàng một, lease 30 phút, không heartbeat | Một item TTS/dựng short < vài phút; worker chết thì 30 phút sau hàng tự trở lại |
| 4 | Upload tay nhận diện bằng **token `yf-<slug>`** (tag, rồi dòng cuối mô tả), **không bằng tiêu đề** | Người hay sửa tiêu đề trong Studio; hai video có thể trùng tiêu đề. Token phải khớp NGUYÊN tag/dòng: `yf-mim-a` không khớp `yf-mim-a-2` |
| 5 | Hai video cùng token → báo, **không đoán**; token không có item chờ → báo "lạ" | Ghi nhầm sổ làm sai giãn nhịp và vòng phản hồi; người xoá bản thừa hoặc `--slug --video-id` |
| 6 | `adopt` **không** kiểm trùng tiêu đề | Video đã nằm trên kênh; kiểm trùng chỉ có nghĩa trước khi upload |
| 7 | Giờ upload trong sổ = `snippet.publishedAt` nếu ≤ bây giờ, không thì bây giờ; **không bao giờ** `status.publishAt` | Giãn nhịp tính theo giờ UPLOAD; Studio đặt lịch có thể đẩy `publishedAt` sang giờ lên sóng |
| 8 | Đọc tag bằng `videos.list` theo lô 50 | `playlistItems` không trả tags |
| 9 | `publish_long` chạy lại **không bao giờ** hạ `published` về `assembled` | Chạy lại để thêm playlist mà hạ stage thì `export_manual`/`publish_batch` coi như video đang chờ đăng |
| 10 | Token nằm cả trong tag lẫn dòng cuối mô tả (người xem thấy dòng này) | Quên dán tag là lỗi thường gặp nhất khi upload tay; dòng ngắn, vô hại |
| 11 | `export` không đổi stage | Item chỉ thành `published` khi máy THẤY video trên kênh |
| 12 | Bundle cũ không có `render` → engine suy từ slug (cùng luật với migration), cả lúc `enqueue` | Review: 91 bundle `cl-hs-` trên đĩa không có `render`; nạp vào DB mới thì `run_batch` tìm B-roll cho "hyperframes-casefile" |
| 13 | Nhiều video cùng token → luôn báo, **kể cả khi đã nhận một bản** | Review: upload trùng sau lần adopt đầu thì bản thừa tự công khai mà không ai biết |
| 14 | `adopt_one` chỉ nhận video nằm trong upload gần đây của CHÍNH kênh | Review: `videos.list` trả cả video công khai của kênh khác; gõ nhầm id là ghi sổ video người khác |
| 15 | `export` từ chối gói khi tag + token > 500 hoặc mô tả + token > 5000 | Review: token thêm SAU validate; Studio cắt đúng phần cuối -- chính là token |
| 16 | `Channel.adopt` kiểm + ghi trong một `BEGIN IMMEDIATE` (HTTP trước, ngoài transaction) | Review: hai lần adopt chồng nhau có thể gán một video cho hai slug |
| 17 | `publish_long` chạy lại với `result.json` có `video_id` → `Channel.adopt` ghi cả `upload_log` | Grok: trước đó chỉ đổi `item`; video dài upload trước khi có sổ không bao giờ vào vòng phản hồi |

## Đã kiểm

- 242 test xanh (7 lỗi cũ vnlunar, không liên quan), gồm test hai kết nối cùng `claim`.
- Grok nghi `run_batch._claimed` thả lease SAU khi đóng kết nối khi Ctrl+C: thử thật trên CPython 3.13 thì
  generator đóng (thả lease) TRƯỚC `conn.close()` -- vòng lặp `for` nhả iterator khi khung hàm thoát. Giữ nguyên. Kiểm đột biến: 11 đột biến, đều bị bắt (một đột biến sống
  sót ở `adopt_one` → thêm test; một điều kiện thừa trong `_tokens_of` → bỏ).
- Chạy thật trên MIM (chỉ đọc): `adopt_manual.py` gọi `list_uploads` OK; `publish_batch run --channel MIM` từ chối.
- 6 chủ đề dài có sẵn (`golden`, `kowloon`, `mafia`, `ripper`, `shanghai`, `yakuza`) đều dựng được Bundle hợp lệ.

## Chưa làm

- `run_batch` mới giành việc cho engine `assemble`; casefile/casewide vẫn dựng bằng script riêng (`motion/stier`,
  `motion/long/build_long.py`) -- chuyển sang `claim` khi có máy dựng thứ hai.
- Bundle video dài sinh lúc **đăng**, không phải lúc sinh kịch bản; pha sinh (chat) viết Bundle trước là bước sau.
