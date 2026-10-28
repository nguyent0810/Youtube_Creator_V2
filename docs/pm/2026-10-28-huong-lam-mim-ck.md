# Hướng làm MIM và CK, 28/10/2026 (tóm tắt để xin phản biện)

## Hai kênh

- **MIM** ("Mind in the Machine"): AI và công nghệ, giải thích cho người Việt.
- **CK** ("Biểu Đồ Biết Nói"): tài chính cá nhân bằng biểu đồ. Luật riêng của CK:
  - không nêu tên ngân hàng hay mã cổ phiếu;
  - không nói "nên mua/bán";
  - số liệu tự giả định thì ghi "VÍ DỤ GIẢ ĐỊNH".

Mục tiêu chung: 1.000 sub và đủ giờ xem để vào Chương trình Đối tác YouTube. Hiện CK có 39 sub, MIM có 50 sub.

## Số liệu Studio 28/10 (tính tới 26/10)

| | 28 ngày: views | 28 ngày: sub | 7 ngày gần nhất so với 7 ngày trước |
|---|---|---|---|
| CK | 36.550 (Short chiếm 99%) | 27 | views −78% |
| MIM | 63.901 (Short chiếm 98%) | 38 | views −40% |

**Phân tích vì sao CK giảm:**
- 98% phần lượt xem mất đi là ở Shorts feed.
- Khoảng 60% mức giảm đến từ việc CK đăng ít Short hơn: 35 bài tuần trước, 14 bài tuần này. 92–100% lượt xem của một Short CK nằm trong 3 ngày đầu.
- Phần còn lại: lượt xem mỗi bài cũng giảm từ 18/10, và MIM cũng giảm như vậy dù vẫn đăng đều 5 bài/ngày.

**Sub trên 1.000 views:**
- Short khoảng 0,5–0,7.
- Long khoảng 4. Nhưng Long gần như không có lượt xem: CK 240 views trong 28 ngày, MIM 919.

## Quyết định đang chạy

1. **CK quay lại 5 Short/ngày.** Chủ kênh quyết ngày 28/10. Cần dựng thêm khoảng 54 Short cho giai đoạn 29/10–12/11.
2. **Pilot hook A/B cho Short.** Biến thử duy nhất là câu mở 2 giây:
   - **A:** dữ kiện có ngày về thế giới bên ngoài.
   - **B:** tình huống của chính người xem, nói với "bạn", có số cụ thể.

   Lịch: CK 07–12/11 lúc 19:00, MIM 13–18/11 lúc 15:00. Mỗi kênh 3 cặp. Đo ở mốc 48 giờ và 7 ngày bằng tỉ lệ "xem / lướt qua" trong Studio. Ngưỡng thắng: B hơn A ít nhất 5 điểm ở 2/3 cặp. Không tự mở rộng khi có kết quả.
3. **Short không phải trailer của Long.** Có hai loại Short:
   - **S:** trả lời trọn một ý, để kéo sub.
   - **L:** trả lời một phần hữu ích, để lại một câu hỏi mà Long thật sự trả lời.
4. **Long:** 5 Long mỗi tuần, dài 10–15 phút, kể chuyện trước. Kịch bản của 6 Long tiếp theo đang chờ duyệt.

## Cách vận hành mới

- **Ticket:** việc được ghi thành ticket markdown, dùng công cụ `tk`.
- **Điều phối:** một AI điều phối (Claude) viết brief cho từng ticket. Các agent CLI trên máy làm việc:
  - **Codex:** viết spec, code, test;
  - **agy và Grok:** phân tích dữ liệu và render video.
- **Fallback:** agent hết quota thì việc tự chuyển sang agent kế tiếp. Hết cả danh sách thì subagent của Claude nhận.
- **Review:** Claude chỉ review cuối, để tiết kiệm token.
- **Tự sinh ticket:** đọc báo cáo của agent xong, Claude được tự tạo ticket mới cho việc phân tích, công cụ, dựng nháp.
- **Phải chờ chủ kênh duyệt:** đăng, đặt lịch, thay video, đổi kế hoạch.

## Câu hỏi xin phản biện

1. Với kênh dưới 100 sub, có nên **quay lại 5 Short/ngày** ở CK không? Có rủi ro bị coi là nội dung sản xuất hàng loạt, hay làm giảm lượt xem trên từng bài?
2. Pilot hook A/B với **3 cặp mỗi kênh** có đủ để kết luận gì không? Có biến nhiễu nào bị bỏ sót?
3. Short có tỉ lệ sub trên 1.000 views thấp (0,5–0,7), còn Long thì không có lượt xem. Nên **ưu tiên** cái gì để lên 1.000 sub nhanh nhất?
4. Mô hình **một AI điều phối, nhiều agent làm** có điểm yếu nào cần chốt chặn thêm?
5. Nếu chỉ được làm **3 việc** trong 2 tuần tới, nên làm gì?
