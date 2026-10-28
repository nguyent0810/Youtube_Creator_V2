# Ticket YCV-im1r vòng 2 · sửa spec p2–p6 theo mẫu p1 đã duyệt

Chủ kênh đã duyệt bài mẫu p1 (`data/stier/specs/mim-p1-quang-cao-giong-gia.json`, bản 2) ngày 28/10. Bài mẫu được sửa theo một review bên ngoài. Hãy áp cùng bài học cho 5 spec còn lại:
- `mim-p2-tin-nhan-thoai`
- `mim-p3-nghe-nhap-lieu`
- `mim-p4-ilo-2023-van-phong`
- `mim-p5-recsys-2016`
- `mim-p6-feed-cua-ban`

**Chỉ sửa spec. Không render.** Sandbox không chạy được npm; Claude sẽ render.

## Bài học từ p1

Đọc kỹ spec p1 trước.

1. **Hook ngay câu đầu: nói ra điều bất ngờ hoặc điều đang bị đe doạ.** Câu nền để xuống câu 2.
   - Ví dụ p1: câu đầu nói luôn "giọng giả … Cô chưa từng nhận lời". Con số "22 giây" chuyển xuống câu 2.
   - **Giữ đúng loại hook của từng bài:**
     - **A** = dữ kiện có ngày về thế giới bên ngoài: p4, p5.
     - **B** = tình huống của chính người xem, nói với "bạn", có số cụ thể: p2, p3, p6.

     Đây là biến duy nhất của pilot, không được đổi loại.
   - Chữ trên hình ở cảnh 0 phải nêu ý chính ngay từ giây 0. Không mở bằng nhãn trung tính.
2. **Ít cảnh chữ tĩnh trên nền tối.**
   - Cảnh chữ (kinetic, slam, quote) nên có `clip` nền. Riêng `quote` để nguyên.
   - Chỗ nào là một quá trình thì thay bằng `board` có mũi tên. Ví dụ p1: giọng thật → AI bắt chước → quảng cáo.
3. **Câu kết là một câu chốt đắt, quay về ý mở, dễ nhớ.**
   - Ví dụ p1: "AI sao chép được giọng nói. Nhưng nó không tự tạo ra được sự đồng ý."
   - Không kêu gọi hành động. Không đặt câu hỏi.
4. **Clip:**
   - **Không dùng clip có mặt người rõ** ở cảnh nói về một người thật hay một nghề cụ thể, để người xem không tưởng đó là nhân vật.
   - Ưu tiên tay, thiết bị, màn hình. Kiểm bằng bảng poster: `python motion/stier/clips.py search ... --src pexels`.
   - Không dùng clip trừu tượng trông như sinh vật, ví dụ pexels:39687575.
5. **Từ trong `acc`:** không đưa từ phủ định như "không" vào. Từ đó bị đóng khung riêng trên chữ kinetic.

## Ràng buộc giữ nguyên

- Mọi số và dữ kiện phải có trong `docs/pm/pilot-short/mim-pilot-1318-factcheck.md`. Không thêm số mới.
  - p2: không nói "3 giây là đủ cho kẻ gian". Đó là mô hình nghiên cứu, chưa mở cho công chúng.
  - p3: 0,70 không bao giờ thành "70%".
  - p6: số do hãng tự công bố phải ghi "THEO YOUTUBE · 2021" / "THEO TIKTOK · 2020".
- Mỗi bài 55–135 chữ và 25–35 s. Chênh trong cặp p1/p2, p3/p4, p5/p6 không quá ±3 s. p1 hiện dài 31,8 s.
- Tiêu đề tối đa 60 ký tự.
- Luật phối cảnh trong `motion/stier/build.py`, hàm `mix_lint`: phải có cảnh M, D và G; chữ không quá 35% thời lượng; không có 3 cảnh liền cùng kiểu.
- Sau mỗi spec, chạy `python motion/stier/build.py <slug> --no-render` cho tới khi sạch. Lệnh này không gọi npm.
- Không đăng, không enqueue, không commit.

## Báo cáo

Ghi vào `docs/pm/tickets/YCV-im1r-r2-report.md`. Với mỗi slug:
- câu mở cũ và mới;
- câu kết cũ và mới;
- cảnh đã đổi, clip đã đổi;
- số chữ và thời lượng giọng;
- chênh thời lượng trong từng cặp.
