# yt-factory

Xưởng nội dung YouTube cho ba kênh: **Phong Thủy (FS)**, **Phật Giáo (BUD)**, **Hình Sự (CL)**.

Viết lại từ đầu. Không kế thừa code của v1.

---

## Tư tưởng: HIT & RUN

v1 nặng **26.000 dòng** — nhưng phần lớn không phải logic nội dung. Đó là lớp phòng thủ dựng quanh những thứ không đáng tin: quota Codex/agy, PATH tối giản của launchd, Google Drive làm database, registry JSON + `flock`, fallback ba tầng nhà cung cấp.

v2 bỏ hết, bằng cách cắt pipeline đúng ở chỗ **thật sự cần trí tuệ**:

```
PHA SINH  — trong chat, Claude tự viết và tự phản biện
            ↓  Bundle: kịch bản + SEO + chữ thumbnail + giờ đăng
PHA SẢN XUẤT — chạy nền, KHÔNG có LLM nào
            ↓  TTS → dựng video → thumbnail → upload
```

**Nạp đạn trong chat, bắn tự động ngoài đời.**

Không Codex. Không agy. Không API key cho pha sản xuất. Không bước nào chờ người bấm nút.

---

## Luật bất di bất dịch

> **Pha sản xuất không được phép cần LLM.**

Mọi thứ cần ngôn ngữ — tiêu đề, mô tả, tag, chữ thumbnail, từ khoá B-roll — phải nằm sẵn trong Bundle.

Nếu một trường nào đó "để lúc sản xuất tự sinh", kiến trúc này sụp: pha sản xuất lại cần API key, lại có quota, lại cần fallback — và ta quay về đúng v1.

`Bundle.validate()` cưỡng chế luật này. Thiếu `voice` hay `broll_queries` là lỗi **cứng**, không phải cảnh báo.

---

## Bundle — hợp đồng giữa hai pha

Một file JSON đọc được bằng mắt, review được trong git diff.

```
bundles/<channel>/<slug>.json   ← Claude sinh. BẤT BIẾN.
state.sqlite                    ← máy làm gì với nó. Đổi liên tục.
```

Tách hai kho có chủ đích: Bundle cần **đọc được và sửa tay được**; trạng thái sản xuất cần **truy vấn được**. Gộp chung thì mất một trong hai.

v1 gộp vào `registry.json` rải rác theo kênh và trả giá đúng ở đây — mỗi câu hỏi vận hành ("tuần sau còn thiếu mấy slot?") lại phải viết code mới để quét file, còn ghi đồng thời thì phải dựng `flock` + backup rotation + production-write guard, khoảng 500 dòng chỉ để một file JSON không hỏng. SQLite làm sẵn việc đó, đúng, và chạy được trên Windows.

---

## Dùng thế nào

### Trong chat (pha sinh)

```python
from factory.bundle import Bundle, make_slug
from factory import store

b = Bundle(
    channel="FS", kind="short", slug=make_slug("Mệnh Kim hợp màu gì"),
    script="Mệnh Kim hợp màu gì? Trắng, bạc và ánh kim là nhóm màu bản mệnh. ...",
    title="Mệnh Kim hợp màu gì?",
    description="Màu bản mệnh và màu tương sinh cho mệnh Kim.",
    tags=["phong thuy", "menh kim"],
    thumbnail_text="",                      # Long mới cần
    publish_at="2026-10-01T23:00:00Z",      # BẮT BUỘC có Z
    voice="Phạm Tuyên",
    bgm="asian_drums.mp3",
    broll_queries=["silver metal texture", "white minimal interior"],
)
store.save_bundle(b)                        # validate rồi mới ghi
```

### Ngoài đời (pha sản xuất)

```python
from pathlib import Path
from factory import speak, store

with store.connect() as conn:
    store.sync_from_disk(conn)              # nạp bundle mới vào hàng đợi

    engine = speak._load_engine()           # nạp model MỘT lần cho cả lô
    for row in store.next_batch(conn, "pending", limit=50, channel="FS"):
        b = store.load_bundle(row["channel"], row["slug"])
        try:
            res = speak.speak_bundle(b, Path("output"), engine=engine)
            store.mark(conn, b.id, "spoken",
                       wav_path=res["wav_path"], timing_path=res["timing_path"])
        except Exception as exc:
            store.bump_attempt(conn, b.id, str(exc))
```

---

## Vì sao không có Whisper

TTS xuất timing **trong lúc** tổng hợp, không đoán lại bao giờ.

v1 để video-editor chạy Whisper phiên âm ngược từ audio — tốn ~13 giây mỗi short, và tệ hơn, Whisper đoán sai dấu tiếng Việt nên phụ đề lệch với lời đọc. Vô lý: ta có sẵn văn bản gốc chính xác 100%, vì chính ta vừa đọc nó ra.

Kết quả đo thật trên máy Windows (i5-12400F, CPU/ONNX):

```
5 câu · 10,16 giây audio · phụ đề khớp từng câu
```

Nạp model mất ~7 giây một lần; trong lô, engine tái dùng nên chi phí thật mỗi short còn khoảng **3–4 giây**.

TTS chạy **CPU**, không GPU — có chủ đích. Tài liệu upstream nói thẳng GPU chỉ thắng khi có lô lớn để lấp, còn văn bản ngắn thì CPU/ONNX nhanh hơn. Để GPU rảnh cho encode video, đó mới là chỗ nó tạo khác biệt.

---

## Tình trạng

| Thành phần | |
|---|---|
| `bundle.py` — hợp đồng + validate | ✅ |
| `store.py` — bundle trên đĩa + hàng đợi SQLite | ✅ |
| `speak.py` — TTS + timing + phụ đề | ✅ chạy thật |
| `assemble.py` — dựng video 9:16 | ✅ chạy thật |
| `thumbnail.py` — khung hình + chữ | ✅ |
| `publish.py` — YouTube API, hẹn giờ | ✅ chưa chạy thật |
| CLI gói lại | ⬜ sau cùng |

```bash
python -m pytest tests -q
```

### Demo đã dựng thật

```
Short 9:16 · 10,16s · 2 cảnh · 15,3 MB · dựng trong 25,4s
B-roll Pexels + caption karaoke khớp từng câu + nhạc nền
```

Ba thứ video-editor buộc phải đoán, ta đã biết trước nên vá đi:

| Nó đoán gì | Ta biết gì |
|---|---|
| Whisper phiên âm ngược từ audio | `speak.py` đã ghi timing lúc tổng hợp |
| Dịch máy từ khoá VI→EN tìm B-roll | `Bundle.broll_queries` viết sẵn bằng tiếng Anh |
| Nạp ~500 MB model Whisper | Không bao giờ dùng tới |

Vá 2 xoá một lớp lỗi thật của v1: câu *"cũng không phải hình phạt của một đấng thần linh"* (đang **phủ định**) bị dịch chữ-đúng-chữ thành *"punishment of a deity"*, và Pexels trả về ảnh linh mục Công giáo — cho một video Phật giáo. Không phải sửa bản dịch cho khéo hơn; là xoá cả bước đoán.

### An toàn khi đăng

`publish.py` luôn đặt `privacyStatus = "private"` kèm `publishAt`. Video tự chuyển public đúng giờ. **Không bao giờ đăng public ngay** — một lần nhầm là công khai thật, không rút lại được.

Chống đăng trùng bằng `playlistItems.list` (1 đơn vị quota) chứ không `search.list` (chỉ 100 lần/ngày cho cả project).

---

24 test, tất cả đạt. Mỗi test khoá lại một cách hỏng thật — hoặc đã xảy ra ở v1, hoặc là giả định mà cả kiến trúc dựa vào.
