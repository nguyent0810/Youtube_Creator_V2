# Audio retention: kỹ năng giữ chân người nghe cho video dài (kênh Hình Sự)

Bộ quy tắc rút ra từ việc **đo và mổ xẻ** bản Long thành công nhất của kênh
("Hội Tam Hoàng", 50:05, 8.4K view, gấp ~23 lần Long thứ hai). File này chỉ ghi
**kỹ thuật**; không một câu văn nào của bản gốc được dùng lại. Bản chép lời chỉ để
phân tích, nằm ở `output/long/ref/`, gitignored.

Công cụ đo: `motion/long/transcribe.py` (faster-whisper large-v3-turbo, mốc từng từ).

---

## 1. Số đo bản tham chiếu

| Chỉ số | Giá trị | Nhận xét |
|---|---|---|
| Thời lượng | 50:05 | Dài là lợi thế: watch-time tuyệt đối cao |
| Tốc độ đọc | **208 âm tiết/phút**, dao động 193–225 theo từng 5 phút | Gần như phẳng. Không có đoạn nào đọc chậm lại để nhấn |
| Khoảng lặng > 0.8s | 23 lần / 50 phút | Có chỗ nghỉ ở ranh giới chương, gần như không có nghỉ kịch tính |
| Khoảng lặng > 2s | 4 lần | Chỉ có ở chỗ nối file |
| Câu hỏi tu từ | gần như không có | Cơ hội bị bỏ lỡ |

**Kết luận:** bản Tam Hoàng thắng nhờ **chủ đề + cấu trúc + chi tiết lạ**, không nhờ
giọng đọc. Nhịp phẳng, đọc cả tiêu đề mục ("Các hoạt động tội phạm chủ yếu…"),
liệt kê tên dài. Nghĩa là còn nhiều dư địa tăng retention bằng kỹ thuật audio.

## 2. Những gì bản gốc làm ĐÚNG (giữ lại, viết theo cách của mình)

1. **Lời hứa lộ trình ngay phút đầu.** Liệt kê trước những thứ người nghe sẽ nhận
   (lịch sử, cấp bậc, nghi lễ, ông trùm, cuộc chiến với cảnh sát). Người nghe
   biết "còn nhiều thứ hay phía trước" nên không thoát.
2. **Cung biến chất (A → B) làm xương sống.** Từ hội kín yêu nước thành đế chế
   tội phạm. Cả video là câu trả lời cho "chuyện gì đã xảy ra ở giữa?".
   Mỗi chủ đề băng đảng đều có một cung như vậy: tìm nó trước khi viết.
3. **Giải mã mật mã.** Các con số cấp bậc được "giải" từng bước (cộng, nhân ra ý
   nghĩa). Não người nghe thích được trao chìa khóa. Đây là đoạn giàu chi tiết
   nhất và cũng là đoạn đọc nhanh nhất (225 âm tiết/phút).
4. **Nghi lễ kể bằng giác quan.** Hương khói, rượu pha máu, bước qua gươm, đốt lời
   thề. Cụ thể, nhìn thấy được, không trừu tượng.
5. **Con số gây sốc có đối chiếu.** "Giá ở nguồn X, ra đường phố Y". Luôn đặt hai
   con số cạnh nhau để tạo tỷ lệ.
6. **Chân dung ông trùm có cảnh hành động.** Không chỉ nói "khét tiếng", mà dựng
   cảnh cụ thể: giờ, địa điểm, chiếc xe, số người.
7. **Hình ảnh ẩn dụ lặp lại (motif).** Con rắn nhiều đầu, chặt đầu này mọc đầu
   khác. Xuất hiện ở giữa rồi quay lại ở phần kết, tạo cảm giác trọn vẹn.
8. **"Bài học" sau mỗi phần.** Một câu khái quát rút ra từ chương vừa kể. Người
   nghe thấy mình được nhiều hơn là thông tin.
9. **Chương văn hóa đại chúng gần cuối.** Phim ảnh là phần người nghe biết sẵn,
   nên đây là "phần thưởng" giữ họ qua đoạn phân tích khô.
10. **Kết mở.** Không kết luận dứt khoát mà đặt câu hỏi về tương lai.

## 3. Những gì bản gốc làm SAI (sửa trong bản mới)

| Lỗi | Hậu quả | Cách sửa |
|---|---|---|
| Mở bằng "Kính thưa quý vị…", giọng thuyết trình | Người lướt không có lý do ở lại 30 giây đầu | **Cold open**: mở bằng một cảnh cụ thể, căng nhất, rồi mới chào |
| Đọc to tiêu đề mục | Nghe như đọc tài liệu | Chuyển chương bằng **câu móc**; tiêu đề chỉ hiện trên màn hình |
| Nhịp đều 208 âm tiết/phút | Buồn ngủ ở phút 15–25 | Đổi nhịp có chủ đích (mục 5) |
| Liệt kê 6–10 tên liền nhau | Người nghe mất dấu | Tối đa **3 mục** mỗi danh sách; phần còn lại cho lên màn hình |
| Lặp nội dung giữa các chương | Cảm giác độn | Mỗi sự kiện chỉ kể một lần, nhắc lại chỉ bằng **callback** ngắn |
| Không có câu hỏi, không có vòng mở | Không có lực kéo sang phút sau | Mỗi chương mở ít nhất 1 vòng, đóng ở chương sau |
| 10 phút cuối là phân tích xã hội khô | Tụt retention ở đuôi | Giữ **cảnh mạnh thứ hai** cho 20% cuối |

## 4. Kiến trúc một video dài 30–40 phút

```
0:00  COLD OPEN (40–70s)   Cảnh căng nhất, kể thì hiện tại, dừng ở đỉnh điểm, chưa giải thích
      TITLE STING           Tên video + câu hứa ("để hiểu cảnh này, phải quay lại 300 năm")
      LỘ TRÌNH (20s)        3 câu hỏi lớn video sẽ trả lời (open loop chính)
CH1   GỐC RỄ                Nơi cung A → B bắt đầu
CH2…  CÁC CHƯƠNG            Mỗi chương 3–6 phút (xem khuôn chương)
~50%  RE-HOOK GIỮA VIDEO    Quay lại cold open: "giờ bạn đã hiểu vì sao…" (đóng 1 vòng, mở vòng mới lớn hơn)
~75%  CẢNH MẠNH THỨ HAI     Vụ án / cuộc chiến kịch tính nhất còn lại
KẾT   CALLBACK + CÂU HỎI    Đóng vòng chính, trả motif, để lại một câu hỏi thật
```

### Khuôn một chương (3–6 phút)

1. **Móc vào** (1–2 câu): một chi tiết lạ, hoặc câu hỏi, hoặc con số.
2. **Bối cảnh** ngắn: ai, ở đâu, năm nào.
3. **Leo thang**: 2–3 nhịp, mỗi nhịp một chi tiết cụ thể hơn.
4. **Đỉnh**: một câu ngắn, một khoảng lặng, rồi hiện ảnh hoặc con số lên màn hình.
5. **Ý nghĩa**: một câu "bài học" bằng lời của mình.
6. **Cầu nối**: câu mở vòng sang chương sau ("Nhưng thứ nuôi sống họ lại không phải
   cờ bạc…"). Tuyệt đối không kết chương bằng câu tóm tắt.

## 5. Kỹ thuật audio (TTS Anh Khôi)

- **Tốc độ nền** ~220 âm tiết/phút là nhịp tự nhiên của Khôi.
  - Đoạn giải mã hoặc liệt kê nhanh: câu ngắn, dồn dập.
  - Đoạn đỉnh: câu rất ngắn (3–6 âm tiết), tách dòng riêng.
- **Độ dài câu:** trung bình 12–18 âm tiết, xen câu 3–6 âm tiết mỗi 4–6 câu.
  Không để câu nào quá 35 âm tiết (TTS hụt hơi, người nghe mất mạch).
- **Khoảng lặng có chủ đích** (chèn khi ghép audio, không nhờ dấu câu):

  | Vị trí | Độ dài |
  |---|---|
  | Sau câu đỉnh | 0.9–1.3s |
  | Giữa chương | 1.6–2.2s, kèm sting SFX |
  | Sau câu hỏi tu từ | 0.6s |
  | Câu thường | 0.25–0.4s |

- **Pattern interrupt mỗi 45–90 giây:** một câu hỏi tu từ, một con số lớn đọc tách,
  một câu "nhưng", một đoạn trích tài liệu, hoặc đổi cảnh hình mạnh. Không để quá
  90 giây chỉ là kể liền mạch.
- **Nói với người nghe:** dùng "bạn". Bản gốc dùng "quý vị" (xa cách); kênh cần
  giọng kể chuyện, không phải hội thảo.
- **Quy tắc số ba:** liệt kê 3 thứ, mục thứ ba là mục bất ngờ nhất.
- **Tên nước ngoài:** mỗi tên phải đi kèm một mô tả ngắn ở lần đầu ("Taoka, đứa
  trẻ mồ côi ở bến cảng Kobe"). Lần sau chỉ gọi mô tả hoặc họ.
- **Con số:** đọc số tròn, luôn đặt cạnh một mốc so sánh quen thuộc.
- **Nhạc nền:** giảm nhạc khi vào câu đỉnh, tắt hẳn 1 giây trước câu cao trào,
  vào lại khi sang chương.

## 6. Tính trung thực (luật cứng của kênh)

- Chỉ kể sự kiện có nguồn (Wikipedia EN/JA, báo chí được trích trong đó). Số liệu
  ghi kèm năm.
- Cảnh "dựng lại" phải là tường thuật sự kiện có thật, không bịa lời thoại.
  Lời diễn ý phải gắn nhãn **DIỄN Ý** trên màn hình.
- Không dùng ảnh gây hiểu nhầm (ảnh người A chú thích là người B). Ảnh minh họa
  không liên quan trực tiếp → gắn nhãn "ẢNH MINH HỌA".
- Không tôn vinh bạo lực hay tổ chức tội phạm. Mỗi chương "bài học" nêu cái giá phải trả.

## 7. Checklist trước khi thu âm

- [ ] 30 giây đầu có cảnh cụ thể + câu hỏi chưa trả lời?
- [ ] Có ≥3 open loop được đóng ở các chương sau?
- [ ] Mỗi chương kết bằng câu cầu nối, không phải câu tóm tắt?
- [ ] Không có đoạn >90s thiếu pattern interrupt?
- [ ] Không danh sách nào >3 mục trong lời đọc?
- [ ] Motif xuất hiện ≥3 lần (đầu, giữa, kết)?
- [ ] 20% cuối có một cảnh mạnh?
- [ ] Mọi con số có nguồn và năm?
- [ ] Tổng ≥ 6.800 âm tiết (≈ 31 phút ở 220 âm tiết/phút + lặng)?
