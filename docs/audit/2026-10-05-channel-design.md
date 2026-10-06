# Thiết kế Channel module (đề xuất 1 của audit 05/10/2026)

Chốt sau 3 vòng phản biện Claude ↔ Grok (grok-4.7, chỉ đọc repo). Grok sign-off ở vòng 3.
Vòng 4–5 (Grok review code) và review hai trục Standards/Spec thêm quyết định 16–20.
Các quyết định dưới đây là những thứ review sau **không nên mở lại** nếu không có bằng chứng mới.

## Mục tiêu

Mọi lần ghi lên YouTube đi qua MỘT module, để:

1. không đường nào đăng dồn được (sự cố CL 30/09: 61 video/ngày, ~53 trong 47 phút);
2. không bao giờ upload trùng hay gán nhầm `video_id` (sự cố 9 ngày Lịch, `scripts/repair_titles.py`);
3. sửa video an toàn (`videos.update` ghi đè cả part);
4. test được mà không cần mạng.

## Interface

```python
# factory/channel.py — chính sách: giãn nhịp, sổ upload, bất biến, merge
Channel(code, api, conn, *, now=..., pacing=..., channel_titles=None)
Channel.open(code, conn, *, channel_titles=None)        # creds thật + HttpYouTube (token lấy lười)
.upload(Upload, *, unscheduled=False) -> Uploaded
.reschedule(video_id, publish_at | None)                # None = gỡ lịch
.edit(video_id, **snippet_changes)                       # không bao giờ đụng status
.set_thumbnail(video_id, jpg)
.next_upload_at() -> datetime
.resolve(slug, video_id | None)                          # người xử lý UploadInDoubt

# factory/youtube_api.py — port + adapter HTTP
insert_video(meta, path, *, resume_uri, on_session) -> video_id
get_video(video_id, parts) -> dict | None
update_video(part, body)
set_thumbnail(video_id, jpg)

# factory/youtube_fake.py — adapter thứ hai, in-memory, cho test
```

Lỗi: `PacingHold(until)`, `QuotaExceeded`, `RateLimited`, `DuplicateTitle(video_id)`,
`UploadInterrupted`, `UploadInDoubt`, `PublishError`. `QuotaExceeded` giữ nguyên lớp cũ của
`publish.py` (không có `retry_after`): caller tự tính mốc bằng `publish.next_quota_reset()`. Không lỗi nào trong số đó (trừ `PublishError`)
được phép đi vào `store.bump_attempt`: hoặc hoãn (`store.defer`), hoặc chờ người.

## Quyết định

| # | Quyết định | Vì sao |
|---|---|---|
| 1 | Giãn nhịp đếm theo **giờ upload**, không phải giờ lên sóng | Cú phạt CL đến từ dồn upload video private hẹn giờ, không phải dồn giờ lên sóng. Giờ lên sóng vẫn do `_foreign_days` và `schedule_audit` lo |
| 2 | Đếm từ **sổ của mình** (`upload_log`), không từ playlist uploads | Playlist trả tối đa 50 mục/trang, và `snippet.publishedAt` của video private hẹn giờ không ổn định |
| 3 | Dòng `started` **chính là chỗ giữ slot**, ghi trong một `BEGIN IMMEDIATE` cùng phép kiểm, trước mọi HTTP | Hai tiến trình (`publish_batch` + `drip`) không cùng lọt qua trần |
| 4 | CL: `min_gap 3h`, `max_per_24h 8`. FS/BUD: `min_gap 0`, `max_per_24h 24` | CL theo chính sách sau sự cố (`drip.py`). FS/BUD: giãn 15 phút sẽ đụng timeout 2 giờ của `run_pipeline` khi chưa có lịch tự chạy `resume`; 24/ngày nhỏ hơn cú dồn đã làm CL dính |
| 5 | Định danh = `(channel, slug)`, **không bao giờ là tiêu đề** | Trùng tiêu đề với slug khác → `DuplicateTitle`, không âm thầm trả `video_id` của video khác |
| 6 | Lưu session URI của upload resumable **trước byte đầu tiên**; ghi `video_id` ngay khi có | Đứt giữa chừng thì hỏi lại phiên, không upload lại |
| 7 | Đã có session URI thì **không phản hồi chunk nào được xoá dòng** | 5xx/mất mạng ở chunk cuối có thể là video đã tạo xong (mất phản hồi 201). Lần sau hỏi phiên: 200/201 nhận id, 308 upload tiếp, 5xx/mạng → `UploadInterrupted`, 404 → `UploadInDoubt` (giữ slot, người `resolve`). Chỉ xoá khi hỏi phiên nhận 4xx vĩnh viễn khác 401/404/429 |
| 8 | Chưa có session URI (kể cả 429 lúc khởi tạo) → xoá dòng, trả slot | Chưa có gì trên YouTube |
| 9 | Phân loại theo **body trước status**: `rateLimitExceeded` thử lại trong adapter; `quotaExceeded`, `uploadLimitExceeded`, 429 không lý do → `QuotaExceeded` | 429 trần thật ở lượt 93 không nên thử lại 3 lần |
| 10 | `edit()` không đụng `status`; merge = giá trị hiện tại của **toàn bộ trường ghi được** + phần đổi | Ép `private` khi sửa sẽ gỡ video đang public; whitelist cũ làm rơi `defaultAudioLanguage`, `license`… |
| 11 | `private` chỉ ép khi đặt `publishAt` tương lai; từ chối `publishAt <= now`; `reschedule` từ chối video đã public | Mốc 30 phút của `upload_one` là chính sách của caller, để ở caller |
| 12 | Thumbnail là best-effort sau khi đã ghi `done` | Lỗi thumbnail mà ném ra thì caller ghi video đang sống là "hỏng" |
| 13 | `category` bắt buộc với `kind="long"`; short dùng mặc định của kênh (`"22"`) | Bỏ PUT sửa category lần hai của `publish_long` |
| 14 | `probe` = `upload(unscheduled=True)`; `run` sau đó cho cùng slug → dùng lại video và **gán lịch** | Bỏ trò vá `json.dumps` trong `publish_batch` |
| 15 | Fake ở mức thao tác YouTube; chi tiết HTTP (308, 401, chunk) test bằng stub riêng cho adapter HTTP | Lỗi đã từng ship là danh tính theo tiêu đề, ghi đè part và dồn upload, không phải HTTP |
| 16 | **Lease 3 giờ** trên dòng sổ: tiến trình đang upload giữ lease; tiến trình khác thấy lease còn hạn thì lùi (`UploadInterrupted`). Mọi cập nhật dòng gắn với `attempt` của mình | Grok vòng 4: không có lease, `drip` có thể xoá slot `publish_batch` vừa giữ (chưa kịp có URI) rồi mở phiên thứ hai → hai video cho một slug |
| 17 | Hỏi phiên: phân loại body trước; `rateLimitExceeded` lùi rồi thử lại, quota → `QuotaExceeded`; chỉ 4xx còn lại mới là `SessionDead`. Rate limit kéo dài → `RateLimited` (lỗi tạm, caller hoãn 15 phút) | Trước sửa: 403 rate limit lúc hỏi phiên bị coi là phiên chết → xoá sổ → upload lần hai |
| 18 | Mọi vòng lặp trong adapter có giới hạn: 401 làm mới token một lần, rate limit lùi 3 lần, 308 không tiến 3 lần | Tránh treo `drip` (không có timeout) |
| 19 | Backfill sổ lần đầu từ `item`: chỉ `stage='published'`, bỏ `video_id` dùng chung bởi 2 slug, lấy tiêu đề từ bundle | Không đóng băng 9 cặp Lịch dùng chung id, không gán lịch cũ cho video đã gỡ lịch |
| 20 | **Nhịp tim**: adapter gọi `on_progress()` sau mỗi chunk được nhận; Channel gia hạn lease, mất quyền thì dừng gửi. Có `video_id` mà dòng đã đổi chủ thì vẫn ghi `done` (có bằng chứng), trừ khi dòng đã `done` với video khác → báo người | Grok vòng 5: lease không gia hạn thì video dài upload > 3 giờ bị tiến trình khác giành dòng |

## Ngoài phạm vi lần này (cố ý)

- Đường đọc (`schedule_audit`, `verify_published`, `analytics_report`, `monitor`) vẫn dùng `publish.py`. Chuyển sau khi một tuần upload thật được kiểm bằng verifier cũ.
- Không đếm upload của nguồn khác (v1 trên Mac). FS/BUD đã giao cho nguồn kia (`scripts/unschedule.py`), nhưng nếu v2 lại đăng FS trong khi v1 cũng đăng thì trần **không thấy** cú dồn của v1. Đây là việc của điều phối nhiều máy (đề xuất 2).
- Không có analytics, tạo playlist, phụ đề trong Channel. Phụ đề và playlist của Long vẫn ở `publish_long.py`.
- Các script một lần có ngày cứng (`repair_titles.py`, `week_2026-10-05.py`) để nguyên. Chúng vẫn ghi thẳng
  `videos.update`, nên "mọi lần ghi đi qua Channel" đúng với mọi đường **chạy định kỳ**, chưa đúng với hai script này.
- `publish.py` còn lại phần ĐỌC; các hàm ghi cũ (`upload_video`, `publish_bundle`, `set_schedule`, `set_thumbnail`,
  `already_published`) đã xoá để không đường nào lách Channel.
- Giờ upload của dòng backfill lấy `item.updated_at`: script sửa lịch đóng dấu muộn hơn thì giãn nhịp chỉ chặt hơn
  (tối đa 24 giờ), không bao giờ lỏng hơn. Chấp nhận.
