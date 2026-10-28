# Hai repo viết kịch bản: kỹ thuật nào mình CHƯA có (nghiên cứu ngày 15/10/2026)

Câu hỏi: trong hai repo dưới đây, kỹ thuật viết kịch bản nào **chưa có** trong hệ thống của mình và **đáng lấy** cho kịch bản
**chỉ có lời đọc** (TTS tiếng Việt): Short 20–60 giây và video dài 9–30 phút?

- Repo 1: `Spotlight-Revenue/short-form-video-script-writer`, commit `a1057e0` (28/06/2026). 3 file: `SKILL.md` (422 dòng),
  `references/quick-reference.md`, `README.md`.
- Repo 2: `3h0ll7/scriptforge-ai`, commit `07f5342` (10/10/2026). Ứng dụng web React + Supabase. Toàn bộ "tri thức kịch bản"
  nằm trong **một** system prompt: `supabase/functions/generate-script/index.ts`, cộng một bản mẫu giả `src/lib/mockScript.ts`.

Chỉ đọc file gốc trong repo (clone vào scratchpad, không chạy code, không cài gói). Số dòng trích là số dòng trong file của repo
ở đúng commit trên. Trích dẫn tiếng Anh giữ nguyên, mỗi đoạn dưới 15 từ.

---

## 1. Tóm tắt

- Phần lớn kỹ thuật của hai repo **mình đã có, và thường chặt hơn**: hook ≤12 từ, vòng lặp mở/đóng, CTA cụ thể, tối đa 3 mục
  liệt kê, chương + cold open + re-hook giữa video (`motion/long/RETENTION.md`, `motion/stier/script_lint.py`).
- Thứ **thật sự thiếu**: (a) **re-hook sớm ở giây 5–7** của Short (mình chỉ kiểm re-hook ở 30–75%); (b) **đo tự động** khoảng
  cách giữa các pattern interrupt ở video dài (luật 45–90 giây mới nằm trong checklist tay).
- Thiếu một phần: menu **khung kịch bản thay thế** (BAB, PSP), **cặp đối lập** và **nhượng bộ "nhưng"** như kỹ thuật có tên,
  và **ghi kiểu hook vào tín hiệu** để vòng phản hồi so được kiểu nào thắng.
- Xung đột với luật đạo đức `factory/hooks.py:12-15`: FOMO, "Agitate" của PAS, hook `shocking_stat`/`controversy`, mẫu CTA
  "Part 2 drops tomorrow". Không lấy.
- Repo 2 gần như không có luật đo được ngoài "pattern interrupt mỗi 30–60 giây"; phần còn lại là khung JSON và văn mẫu.
  Không repo nào có "viral score" tự chấm; fluff chủ yếu là số liệu không nguồn và ghi chú retention do chính LLM tự viết.

---

## 2. Hệ thống hiện có

Yêu cầu chỉ nêu `factory/`, nhưng luật kịch bản thật đang nằm ở **cả** `motion/`. Đọc cả hai mới so đúng được.

### 2.1 `factory/script_craft.py` (khung Short + bộ chấm)

- Công thức 6 vai trò: `Hook -> Context -> Tension -> Value -> Payoff -> CTA` (`script_craft.py:12-17`), "sáu VAI TRÒ, không phải
  sáu câu". **Chỉ một khung.**
- 10 kỹ năng (`:26-37`): hook, story, copy, retention, voice, rhythm, psychology, visual, compression, cta.
- Lint: hook ≤14 từ (`:54`), câu ≤22 từ (`:53`), cụm văn viết `BOOKISH` (`:44-49`), chênh dài/ngắn ≥6 từ (`:96-101`), câu cuối
  vọng lại hook (`:103-108`).

### 2.2 `factory/hooks.py` (thư viện hook + ranh giới đạo đức)

- Ranh giới: giữ chân bằng tò mò, sự thật cảm xúc… "KHÔNG BAO GIỜ từ sợ hãi, gây sốc rỗng, cảm giác tội lỗi hay sự cấp bách
  giả tạo" (`hooks.py:12-15`); mở vòng rồi đóng tử tế là hợp lệ, giấu thông tin để câu view thì không (`:17-19`).
- 6 kiểu hook (`:39-94`): `pain_question`, `counterintuitive` (cấm ở BUD), `number_result`, `hidden_secret`, `story_open`,
  `empathy`; mỗi kiểu có cơ chế, cách viết, ví dụ đúng ngách, cách hỏng.
- `prompt_block()` (`:105-124`): chọn ĐÚNG MỘT kiểu, câu đầu ~12 từ, không mở bằng mệnh đề phụ.

### 2.3 `factory/script_signals.py` (tín hiệu, chỉ ghi)

- Ghi `first_sentence_words`, `hook_is_question`, `first_answer_sec`, `max_sentence_words`, `digits`, `est_seconds` (170–200
  từ/phút) (`script_signals.py:13-33`). Cố ý không chấm điểm vì chưa có dữ liệu retention (`:3-6`).
- **Không ghi kiểu hook, không ghi khung kịch bản.**

### 2.4 `factory/sameness.py` (độ lặp khuôn)

- Đo tỉ lệ câu trùng KHUÔN với video khác cùng dòng trong 28 ngày, lấy trung vị (`sameness.py:12-14`, `:28`); kèm tỉ lệ nhạc nền
  và bộ từ khoá B-roll phổ biến nhất (`:60-61`). Đo, không chặn (`:8-10`).

### 2.5 `factory/pillars/check.py` (4 pillar)

- 65–90 từ (`check.py:23`), hook ≤22 từ + phải có dấu hiệu nghịch lý/câu hỏi (`:24`, `:41-42`), câu chốt ≤14 từ và phải mời
  tương tác (`:24`, `:146-151`), mở bài 5 từ không trùng 400 bài gần nhất (`:25-29`, `:158-162`), góc không trùng 2 bài gần nhất
  (`:33`), cấm câu tuyệt đối/suy đoán (`:36-38`), mọi câu trần thuật phải có Claim (`:106-114`).

### 2.6 Ngoài `factory/`: luật thật cho Short BUD và video dài

- `motion/stier/script_lint.py` (10 luật, 14/10/2026): R1 hook ≤12 từ, không mở bằng chào, 2 chữ đầu không trùng 10 bài gần
  nhất (`:65-72`); **R2 re-hook ở đoạn 30–75%** bằng danh sách `REHOOK` ("nhưng", "thật ra", "phép thử"…) (`:13-14`, `:77-79`);
  R4 câu cuối gọi lại hook (`:91-94`); R5 câu cuối là câu hỏi, cấm "Bình luận nhé" chung chung (`:95-99`); R6 nhịp 2,6–3,8 từ/giây,
  mệnh đề ≤14 từ (`:100-109`); R7 lỗi TTS (ngoặc, viết tắt, "Trước:/Sau:") (`:110-117`); R8 cụm 3 từ lặp (`:118-122`).
- `motion/long/RETENTION.md`: kiến trúc cold open 40–70s → lộ trình → chương 3–6 phút → **re-hook ~50%** → **cảnh mạnh thứ hai
  ~75%** → callback + câu hỏi (`:63-74`); lộ trình đổi hình thức mỗi video (`:76-92`); khuôn chương 6 bước kết bằng câu cầu nối
  (`:94-102`); **pattern interrupt mỗi 45–90 giây** (`:120-122`); quy tắc số ba (`:125`); tối đa 3 mục liệt kê (`:58`); checklist
  tay (`:142-153`).
- `motion/long/studio_lint.py`: LỖI câu >35 tiếng; CẢNH BÁO thiếu câu ngắn ≤6 tiếng, liệt kê >3 mục (`:8-16`). **Không đo khoảng
  cách giữa các pattern interrupt.**
- `motion/long/RESEARCH-million-views.md:163-180`: 30 giây đầu, chapter (00:00, ≥3 mốc, ≥10 giây), end screen 5–20 giây cuối.
- Kịch bản dài thực tế (`data/long/mim-ai-hallucinate/script.md`): 9 chương `## CHnn`, mục "Cấu trúc giữ chân" ghi rõ cold open,
  hình thức lộ trình "Cảnh hẹn trước", 8 vòng mở có điểm đóng, 3 mô-típ, cảnh mạnh thứ hai ~72% (`:15-21`); CTA chỉ ở câu cuối
  ("Kể ở phần bình luận nhé", `:214`).

Nhận xét phụ (không từ repo): ngưỡng hook của mình **không thống nhất**: 12 từ (`hooks.py:119`, `script_lint.py:66`), 14 từ
(`script_craft.py:54`), 22 từ (`pillars/check.py:24`).

---

## 3. Repo 1: `short-form-video-script-writer`

Một skill cho Claude, viết bằng tiếng Anh, nhắm presenter/AI avatar, ví dụ duy nhất là quảng bá công cụ ClickUp. Đầu ra "spoken-word
only" (`SKILL.md:10`), tức cùng loại sản phẩm với mình.

| Kỹ thuật | Vị trí | Luật đo được |
|---|---|---|
| 6 khung: Hook-Value-CTA, PAS, BAB, PSP, AIDA, PASTOR | `SKILL.md:117-128` | Không; chỉ gợi ý "khung nào cho khán giả nào" |
| Hook trong 1,5–3 giây | `SKILL.md:134` | "Target: 65%+ 3-second hold rate" (không nguồn) |
| 4 kiểu hook: Bold Statement, Question, Pattern Interrupt, Proof-First | `SKILL.md:136-147` | Bold statement phải được chứng minh trong 10–15 giây (`:138`); câu hỏi không được là có/không (`:141`) |
| Trộn tối đa 2 kiểu hook; payoff đóng vòng "at the same intensity" | `SKILL.md:149` | Không |
| **Re-hook ở giây 5–7** | `SKILL.md:153-166` | Vị trí: ngay sau hook, trước thân bài (`:164`). Ba cách: đổi góc lời hứa, thêm chi tiết nâng mức cược, micro-loop "But here's where it gets interesting" (`:160-162`) |
| Cặp đối lập (contrast pair) | `SKILL.md:180-181` | Ví dụ "Not access. Operation." |
| Quy tắc số ba | `SKILL.md:183-184` | 3 mục |
| Nhượng bộ "but" như tín hiệu trung thực | `SKILL.md:189-190` | Nêu giới hạn trước payoff |
| Identity alignment, FOMO, specificity as authority | `SKILL.md:174-187` | Không |
| Loại vòng lặp: story loop (macro), segment loop (micro), moment loop (câu một chữ) | `SKILL.md:196-205` | Không |
| Một ý mỗi video; "Show don't list" | `SKILL.md:209-215` | Không |
| Bảng thời lượng ↔ số từ | `SKILL.md:219-230` | 30s = 60–75 từ … 60s = 125–150 từ; "~2 words/second" (tiếng Anh) |
| Điều chỉnh cho AI avatar: câu ngắn sau câu dài = nhấn; tránh mỉa mai/ẩn ý; chuyển ý bằng chữ, không bằng giọng | `SKILL.md:104-110` | Không |
| Khán giả theo 4 mức hiểu biết → kiểu hook | `SKILL.md:73-84` | Không |
| Tìm góc: "Hook Test", 10–15 góc rồi lọc | `SKILL.md:48-49`, `:69` | 10–15 góc |
| Xoay 6 định dạng (tip, myth-busting, case study…) | `SKILL.md:61-67` | Không |
| Series: premise cố định, chủ đề đổi; tập nào cũng đứng một mình; "format identifier" trong hook; kết bằng sợi chỉ chưa buộc | `SKILL.md:234-248` | Lên kế hoạch ≥5 tập trước tập 1 (`:243`) |
| CTA tự nhiên, không "engagement bait" | `SKILL.md:283-291` | Không |
| Vòng đo: 3s hold, completion, save, comment "khi nào có tập sau" | `SKILL.md:311-346` | 65% / 40% (`:318-320`); debrief sau mỗi 3–5 video (`:334`, `:340`) |
| Đầu ra không có nhãn cảnh, không `[B-roll]` | `SKILL.md:372-376` | Mỗi đoạn = một hơi thở |

Không có gì cho video dài: không chương, không timestamp, không nhịp theo phút. Không có code, không lint; mọi "luật" là văn bản
cho LLM tự theo.

---

## 4. Repo 2: `scriptforge-ai`

Sản phẩm web (form → gọi LLM → JSON). README hứa "timestamps, B-roll, CTA and SEO tags" (`README.md:22`), nhưng phần quy tắc
chỉ có 7 dòng trong system prompt.

| Kỹ thuật | Vị trí | Luật đo được |
|---|---|---|
| Hook trong 3 giây đầu, không intro trước hook | `generate-script/index.ts:28` | 3 giây |
| **Pattern interrupt mỗi 30–60 giây** | `generate-script/index.ts:29` | 30–60 giây |
| Viết cho lời nói, câu ngắn | `generate-script/index.ts:30` | Không |
| Ít nhất một open loop | `generate-script/index.ts:31` | ≥1 |
| CTA hợp văn hoá nền tảng | `generate-script/index.ts:32` | Không |
| 5 kiểu hook: `question`, `shocking_stat`, `story`, `controversy`, `pain_point` | `generate-script/index.ts:81-84` | Enum |
| Khung đoạn: `hook, intro, point_1..3, climax, cta, outro`, mỗi đoạn có `timestamp` MM:SS, `dialogue`, `visualDirection`, `bRollSuggestion` | `generate-script/index.ts:88-104` | Dạng dữ liệu, không có luật thời lượng mỗi đoạn |
| 3 phương án tựa | `generate-script/index.ts:72-76` | 3 |
| `estimatedWordCount`, `retentionStrategyNotes` do LLM tự điền | `generate-script/index.ts:111-115` | Tự khai, không kiểm |
| Bản mẫu: open loop "point #3 is the real game-changer" ở 00:05 | `src/lib/mockScript.ts:28` | Không |
| CTA đặt sau "maximum value" | `src/lib/mockScript.ts:80` | Không |

Thời lượng chỉ là nhãn chọn trong form (30s → "15min+", `src/lib/ideaTemplates.ts:35-134`); prompt chỉ bảo "Adapt script length
to the target duration" (`index.ts:34`). Không có kiến trúc video dài.

---

## 5. Bảng so sánh

HAVE = mình đã có ngang hoặc chặt hơn · PARTIAL = có một phần / chỉ trong checklist tay · MISSING = chưa có.

| Kỹ thuật | Nguồn (repo) | Trạng thái (mình) | Phù hợp audio tiếng Việt? | Đề xuất |
|---|---|---|---|---|
| Hook trong 3 giây | R1 `SKILL.md:134`; R2 `index.ts:28` | HAVE: ≤12 từ ≈ 3,6s ở 3,3 từ/giây (`script_lint.py:66`), `hooks.py:119` | Có | Giữ. Thống nhất ngưỡng 12/14/22 |
| **Re-hook ở giây 5–7** | R1 `SKILL.md:153-166` | **MISSING**: R2 chỉ tìm re-hook ở 30–75% (`script_lint.py:77-79`) | Rất hợp: người nghe không có hình để "níu" | **Lấy** (ưu tiên 1) |
| Re-hook giữa video dài ~50%, cảnh mạnh ~75% | (repo không có) | HAVE: `RETENTION.md:71-72` | Có | Giữ |
| **Pattern interrupt định kỳ** | R2 `index.ts:29` (30–60s) | PARTIAL: luật 45–90s ở `RETENTION.md:120-122`, checklist tay `:148`; không lint | Có; với TTS phẳng càng cần | **Lấy** phần đo (ưu tiên 2) |
| Open loop: macro / segment / moment | R1 `SKILL.md:196-205`; R2 `index.ts:31` | HAVE: vòng mở có điểm đóng ghi trong kịch bản (`mim-ai-hallucinate/script.md:18`), mỗi chương mở ≥1 vòng (`RETENTION.md:60`), câu đỉnh 3–6 âm tiết (`:108`) | Có | Giữ |
| Đóng vòng ở câu cuối | R1 `SKILL.md:149`, `:304` | HAVE: `script_craft.py:103-108`, `script_lint.py:91-94` | Có | Giữ |
| Kiểu hook | R1 `SKILL.md:136-147`; R2 `index.ts:83` | HAVE (6 kiểu, `hooks.py:39-94`). "Proof-First" ≈ `number_result`; "Bold statement" ≈ `counterintuitive` | Có | Lấy luật "chứng minh trong 10–15 giây" vào `trap` của `counterintuitive` (đã có ý "giải thích ngay", `hooks.py:53`) |
| Hook `shocking_stat`, `controversy` | R2 `index.ts:83` | Cố ý không có | **Xung đột** `hooks.py:12-15` (gây sốc rỗng) | Bỏ |
| Menu khung (PAS, BAB, PSP, AIDA, PASTOR) | R1 `SKILL.md:117-128` | PARTIAL: một khung duy nhất (`script_craft.py:12-17`) | BAB, PSP hợp; AIDA/PASTOR là khung bán hàng | Lấy BAB + PSP làm khung thay thế (ưu tiên 4) |
| PAS: bước "Agitate" | R1 `SKILL.md:122` | — | **Xung đột**: khuếch đại nỗi đau = sợ hãi/tội lỗi | Chỉ dùng dạng "gọi tên đúng nỗi đau" (đã có `pain_question`), không khuếch đại |
| Cặp đối lập | R1 `SKILL.md:180-181` | PARTIAL: chỉ là dấu hiệu hook ("không phải", "mới là", `pillars/check.py:41-42`) | Rất hợp: "Không phải X. Mà là Y." đọc lên rõ nhịp | Lấy làm kỹ thuật thân bài (ưu tiên 5) |
| Nhượng bộ "nhưng" trước payoff | R1 `SKILL.md:189-190` | PARTIAL: tinh thần trung thực có (`RETENTION.md:132-140`), chưa thành kỹ thuật viết | Hợp, và hợp đạo đức | Lấy (ưu tiên 5) |
| Quy tắc số ba | R1 `SKILL.md:183-184` | HAVE: `RETENTION.md:125` (mục thứ ba bất ngờ nhất, chặt hơn) | Có | Giữ |
| Show don't list | R1 `SKILL.md:212-215` | HAVE: tối đa 3 mục (`RETENTION.md:58`), lint `studio_lint.py:13` | Có | Giữ |
| Một ý mỗi video | R1 `SKILL.md:209`, `:299` | PARTIAL: kỹ năng `compression` (`script_craft.py:35`) | Có cho Short; không áp cho video dài | Không cần luật mới |
| Tránh mỉa mai/ẩn ý; chuyển ý bằng chữ | R1 `SKILL.md:104-110` | PARTIAL: "voice", "rhythm" (`script_craft.py:31-32`); R7 lỗi TTS (`script_lint.py:110-117`) | Rất hợp: TTS không diễn được mỉa mai | Thêm 1 dòng vào `SKILLS` (ưu tiên 5) |
| Thời lượng ↔ số từ | R1 `SKILL.md:219-230` | HAVE, đúng cho tiếng Việt: 3,3 từ/giây, nhịp 2,6–3,8 (`script_lint.py:3`, `:102`), 65–90 từ (`pillars/check.py:23`), 200–220 âm tiết/phút (`RETENTION.md:106`) | Số của repo là tiếng Anh (~2 từ/giây), **không chuyển được** | Bỏ bảng của repo |
| Khán giả 4 mức → kiểu hook | R1 `SKILL.md:73-84` | PARTIAL: `avoid_on` theo kênh (`hooks.py:25-27`) | Trung tính | Không ưu tiên |
| Personalization "your" tạo urgency | R1 `SKILL.md:55` | HAVE phần "bạn" (`RETENTION.md:123`) | Phần "urgency": **xung đột** | Giữ "bạn", bỏ lý do urgency |
| FOMO framing | R1 `SKILL.md:177-178` | Cố ý không có | **Xung đột** (cấp bách giả tạo) | Bỏ |
| Tìm góc: Hook Test, 10–15 góc rồi lọc | R1 `SKILL.md:48-49`, `:69` | PARTIAL: luật góc không trùng (`pillars/check.py:33`); không có bước "nói được hook 3 giây chưa" | Có | Có thể thêm 1 câu vào `prompt_block()`, chi phí thấp |
| Xoay định dạng | R1 `SKILL.md:61-67` | HAVE theo chức năng: đo độ lặp khuôn (`sameness.py`), lộ trình đổi hình thức (`RETENTION.md:76-92`) | Có | Giữ |
| Series: format identifier trong hook | R1 `SKILL.md:245` | — | **Va chạm** R1 "2 chữ đầu không trùng 10 bài" (`script_lint.py:70-72`) và `sameness.py` | Bỏ câu nhận diện cố định; giữ "tập nào cũng đứng một mình" |
| Series: kết bằng sợi chỉ chưa buộc | R1 `SKILL.md:246` | PARTIAL: "Kết mở" bằng câu hỏi (`RETENTION.md:49`) | Hợp nếu vòng chính đã đóng; nếu không, xung đột `hooks.py:17-19` | Giữ cách hiện tại |
| Chương, timestamp | R2 `index.ts:93` | HAVE: `## CHnn`, luật chapter YouTube (`RESEARCH-million-views.md:173-174`) | — | Giữ |
| Ghi chú hình / B-roll cạnh lời | R2 `index.ts:99-100` | HAVE: lời ở `script.md`, hình ở `chNN.json`/`gen_scenes.py`, `Draft.broll` (`pillars/check.py:70`), đo lặp B-roll (`sameness.py:61`) | Đúng hướng R1 `SKILL.md:374`: lời không chứa nhãn cảnh | Giữ |
| CTA tự nhiên, cụ thể | R1 `SKILL.md:283-291` | HAVE, chặt hơn: R5 (`script_lint.py:95-99`), chốt ≤14 từ (`pillars/check.py:24`) | Có | Giữ |
| Vị trí CTA video dài | R2 `index.ts:96` (`cta` trước `outro`) | HAVE: CTA cuối + end screen 5–20s (`RESEARCH-million-views.md:175-177`) | — | Giữ; không chèn CTA giữa video |
| Vòng đo: kiểu hook nào thắng → thành mặc định; debrief 3–5 video | R1 `SKILL.md:332-346` | PARTIAL: retro sau mỗi lô, `scoreboard.py` xếp hạng `engagedViews` trong tuần (`scoreboard.py:8-15`); nhưng `signals()` không ghi kiểu hook/khung (`script_signals.py:16-33`) | Có | **Lấy** phần ghi nhãn (ưu tiên 3) |
| Ngưỡng 3s hold 65% / 40% | R1 `SKILL.md:318-320` | — | Không nguồn, không chắc YouTube Analytics API trả số này cho Shorts (chưa kiểm chứng) | Không dùng làm ngưỡng |

---

## 6. Đề xuất ưu tiên

Theo tinh thần `script_signals.py:3-6`: luật mới vào **tín hiệu/cảnh báo trước**, chỉ thành lỗi khi số liệu thật ủng hộ.

1. **Re-hook sớm cho Short.** File: `factory/script_craft.py` (`review()`: thêm một Check) và `motion/stier/script_lint.py`
   (luật mới, cảnh báo trước). Luật đề xuất: trong câu bắt đầu ở khoảng từ thứ 12–25 (≈ giây 4–8 ở 3,3 từ/giây) phải có một
   dấu `REHOOK` (`script_lint.py:13-14`) **hoặc** một chi tiết mới cụ thể (con số, tên). Cơ sở: `SKILL.md:153-166`. Lý do: R2
   hiện chỉ nhìn 30–75%; với giọng đọc không mặt, câu thứ hai là chỗ dễ mất người nghe nhất. Ghi kèm `rehook_early: bool` trong
   `factory/script_signals.py` để sau này so với retention.
2. **Đo khoảng trống pattern interrupt ở video dài.** File: `factory/script_signals.py` (thêm `max_interrupt_gap_syll`) và
   `motion/long/studio_lint.py` (cảnh báo). Đếm âm tiết giữa hai "interrupt" liên tiếp: câu hỏi, câu bắt đầu "Nhưng", câu có số,
   dòng trích `»`/`[TRÍCH DỊCH]`, ngừng `‖`. Ngưỡng cảnh báo: > 330 âm tiết ≈ 90 giây ở 220 âm tiết/phút (`RETENTION.md:106`,
   `:120-122`). Biến một mục checklist tay (`RETENTION.md:148`) thành số đo. Repo 2 dùng 30–60s (`index.ts:29`), nhưng không có
   căn cứ; giữ 45–90s của mình vì có đo trên bản tham chiếu (`RETENTION.md:12-24`).
3. **Ghi kiểu hook và khung vào tín hiệu.** File: `factory/script_signals.py` (nhận `hook_key`, `frame` từ spec) và
   `factory/hooks.py` (`BY_KEY` làm danh mục hợp lệ). Cơ sở: `SKILL.md:344`, "If a hook type consistently outperforms, make it the
   default". Hiện chỉ có `hook_is_question` (`script_signals.py:26`), nên `scoreboard.py` không thể trả lời "kiểu hook nào thắng".
   So theo lô 3–5 video (`SKILL.md:340`), khớp nhịp retro sau mỗi lần đăng.
4. **Thêm BAB và PSP làm khung thay thế.** File: `factory/script_craft.py` (bên cạnh công thức `:12-17`). BAB (Trước → Sau →
   Cầu nối) hợp case study tài chính CK; PSP (Pattern interrupt → Story → Payoff) hợp MIM kể chuyện. Lợi thêm: một khung duy nhất
   dễ làm câu trùng khuôn tăng (`sameness.py:3-6`). **Không** lấy PAS nguyên bản: bước "Agitate" (`SKILL.md:122`) phạm
   `hooks.py:12-15`.
5. **Ba kỹ thuật câu chữ có tên.** File: `factory/script_craft.py` (`SKILLS`) và `factory/hooks.py` (`prompt_block()`):
   (a) cặp đối lập "Không phải X. Mà là Y." (`SKILL.md:180-181`); (b) nhượng bộ "nhưng" nêu giới hạn trước payoff
   (`SKILL.md:189-190`), hợp luật trung thực; (c) không viết câu cần giọng mỉa mai hay ẩn ý, chuyển ý bằng chữ
   (`SKILL.md:107-110`), vì TTS không diễn được. Chỉ là hướng dẫn, không lint.

---

## 7. Bỏ qua

- **Số liệu không nguồn** trong Repo 1: "lose 20–30% of viewers" (`SKILL.md:155`), "Series follow rates are 3–5x higher"
  (`:247`), ngưỡng 65% hold rate (`:134`, `:318`), "Series hit their stride at episodes 5–8" (`:248`). Không trích nguồn nào.
- **Bảng số từ tiếng Anh** (`SKILL.md:223-230`, "~2 words/second"): tiếng Việt đơn âm, mình đã có số đo riêng.
- **Ghi chú do LLM tự viết**: `retentionStrategyNotes` và `estimatedWordCount` (`index.ts:111-115`) là mô hình tự khai về chính
  nó, không ai kiểm. Không có "viral score" ở cả hai repo (grep `viral|score`: chỉ thấy nhãn UI `useAppSettings.tsx:58`, thẻ SEO
  `mockScript.ts:72`, và câu `SKILL.md:247`).
- **Văn mẫu câu view** trong `src/lib/mockScript.ts`: "costing them everything" (`:14`, sợ hãi), "Stick around because point #3"
  (`:28`, hứa suông), "smash that subscribe button" (`:57`), "Part 2 drops tomorrow" (`:67`, cấp bách giả tạo). Phạm
  `hooks.py:12-15`.
- **FOMO, Agitate, `shocking_stat`, `controversy`**: xem bảng mục 5.
- **Caption theo nền tảng TikTok/Reels, giới hạn 840 ký tự** (`SKILL.md:260-279`, `:230`): mình chỉ đăng YouTube; tựa dạng câu
  tìm kiếm đã có (`mim-ai-hallucinate/script.md:220-221`).
- **Prompt dựng video AI** (`enhance-prompt/index.ts:19-23`): mình không dùng text-to-video.
- **Persona/voice profile** (`SKILL.md:92-113`): giọng TTS đã cố định theo kênh; "signature patterns" lặp lại đi ngược
  `sameness.py`.

---

## 8. Quyết định 15/10/2026 (grilling với chủ kênh)

Sự thật kiểm lại trước khi chốt (sửa mục 6 ở chỗ trỏ sai file):
- `factory/script_craft.py` gần như chết: chỉ `scripts/dump_scripts.py` import. Cổng thật của Short là `motion/stier/script_lint.py`.
- `script_lint` **chỉ chạy cho theme `bud`** (`motion/stier/build.py:665`); 160 spec MIM + 62 spec CK chưa từng được lint.
- `motion/long/studio_lint.py` không được code nào gọi (chạy tay).
- Spec BUD có `hook_type` với tên riêng (`con-so`, `noi-dau`…); spec MIM không có. `Bundle.script` chỉ là lời ghép (`motion/stier/enqueue_mim.py:43`).

Quyết định:
| # | Câu hỏi | Chốt |
|---|---|---|
| Q1 | Luật mới nằm đâu | Nơi chạy thật: `script_lint` (Short), `studio_lint` (dài); hướng dẫn viết vào `hooks.prompt_block()`; dọn `script_craft` |
| Q2 | Mức nghiêm | Cảnh báo + ghi signals; lỗi chỉ khi số liệu ủng hộ |
| Q3 | Short hay dài trước | Short trước |
| Q4 | Ghi nhãn hook (#3) | Làm đầu tiên |
| Q5 | Ngưỡng hook | Short = 12 từ mọi nơi; pillar giữ 22 |
| Q6 | BAB/PSP (#4) | Hoãn tới khi có vài lô dữ liệu gắn nhãn; #5 (3 kỹ thuật câu chữ) làm kèm |
| Q7 | `script_lint` cho MIM/CK | Chạy mọi theme; MIM/CK chỉ cảnh báo; luật riêng BUD (`CITE`, `WHITE3`, `recent()` glob) tách theo theme |
| Q8 | Bộ tên kiểu hook | Key `hooks.py` (`BY_KEY`) là chuẩn; bảng quy đổi tên BUD cũ; không sửa spec cũ |
| Q9 | Đưa `hook_type` tới analytics | Trường mới trong `Bundle`, ghi lúc enqueue |
| Q10 | Spec mới thiếu `hook_type` | Cảnh báo trong `script_lint`, mọi kênh; video đã đăng không sửa |
| Q11 | `studio_lint` | Nối vào bước dựng/preflight video dài, chỉ cảnh báo |
| Q12 | `dump_scripts` khi bỏ `script_craft` | In kết quả `script_lint`; `BOOKISH` thành luật cảnh báo trong `script_lint`; `SKILLS` vào `hooks.prompt_block()` |
| Q13 | Định nghĩa re-hook sớm | Câu bắt đầu ở từ 12–25 có dấu `REHOOK` **hoặc** chi tiết mới (số, tên riêng); ghi `rehook_early`; xem tỉ lệ qua sau 1 lô rồi mới siết |
| Q14 | Nâng cảnh báo thành lỗi | Ở retro sau lô đăng, khi ≥ ~30 Short gắn nhãn và nhóm qua luật có `averageViewPercentage` cao hơn rõ nhóm trượt |
| Q15 | Lưu quyết định | Mục này |

Thứ tự làm (mỗi bước theo `/tdd`, dựa trên `test_ck_stier`, `test_mim_stier`, `test_lines`):
1. Ghi nhãn kiểu hook: `hook_type` vào `Bundle` lúc enqueue (BUD/MIM/CK), bảng quy đổi tên BUD → key `hooks.py`, cảnh báo thiếu nhãn.
2. Mở `script_lint` cho mọi theme (MIM/CK cảnh báo, luật BUD tách theo theme); ngưỡng hook Short = 12.
3. Re-hook sớm (#1): luật cảnh báo từ 12–25 + `rehook_early` trong signals.
4. Dọn `script_craft`: `BOOKISH` → `script_lint`; `SKILLS` + 3 kỹ thuật câu chữ (#5) → `hooks.prompt_block()`; `dump_scripts` dùng `script_lint`; xoá `script_craft.py`.
5. Khoảng trống pattern interrupt (#2): `max_interrupt_gap_syll` trong signals, cảnh báo `studio_lint` > ~330 âm tiết, nối `studio_lint` vào pipeline dài.
6. BAB/PSP (#4): hoãn.
