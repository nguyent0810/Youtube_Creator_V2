# Trạng thái 20/10/2026 13:30 (dừng vì hết hạn mức) — việc còn lại

Đã duyệt bởi chủ kênh: bài mẫu `mim-nvidia-quan-an-dem`; kế hoạch 40 Short khung truyện (01-KE-HOACH-TRINH-DUYET.md) + 4 quyết định (Elias, ẩn danh bệnh nhân, thay Mona Lisa → Patrascu, thay Short `mim-claudico-thua-2015`).

## Đang chạy nền (không phải subagent)
Chuỗi `output/chain_src/mim_nov_render.sh` (log `mim_nov_render.log`): dựng 40 Short theo `mim_nov_order.txt`; lúc 13:28 đã 30 OK. Tự dừng khi xong; bài đã có `final.mp4` thì bị bỏ qua khi chạy lại.

## Việc còn lại (theo thứ tự)
1. Khi chuỗi xong (`=== xong` trong log): xoá không cần; chạy lại cùng lệnh `python scripts/run_chain.py output/chain_src/mim_nov_render.sh --log ...` để dựng 6 bài chưa có final.mp4: `mim-cuda-canh-bac-2006`, `mim-tahoe-44-trieu-hinton` (lint chữ — đã thu nhỏ size), và 4 bài đã đổi clip/chữ (`lickel`, `nghin-may-chu-con-ba-2013`, `buoi-tap-kem-mot-nghin-do`, `chat-nguoi-la-20-3-2023`).
2. Soát bảng khung các bài còn lại (giống SOAT-LAN-1.md: logo/chữ đọc được, nhãn người thật đè lên người lạ, clip lệch nghĩa); sửa mục "SỬA NÊN" của SOAT-LAN-1.md.
3. Short cũ `mim-claudico-thua-2015` (video WU5Zv4PQdok, riêng tư, hẹn 09/11 23:30, 0 view): chủ kênh duyệt thay; dùng `mim-jason-les-ba-co-may` thay thế — chưa làm gì với video cũ (dùng unschedule/hide, không xoá).
4. Chốt lịch giờ bằng `scripts/shorts_grid.py`, `motion/stier/enqueue_mim.py`, rồi `publish_batch.py` (MIM đăng bằng API, riêng tư + hẹn giờ).
5. **Chủ kênh chưa trả lời:** 2 Long có lỗi (`mim-ai-chat-privacy` mốc Samsung tháng 3/2023; `mim-may-choi-game` phạm vi 99,4%) — dựng lại hay chỉ ghi chú đính chính. `mim-ai-gpu` đề nghị giữ nguyên. Cả 3 đang riêng tư, hẹn giờ, 0 view.
6. Long T2 (`mim-dich-may`, 07/12) và T3 (`mim-apollo-1202`, 10/12): script/factcheck đã xong, chưa dựng; T2 yếu về tư liệu hình có người (dự phòng GPS).
7. Retro bằng subagent sau mỗi đợt đăng; đo "ở lại xem" theo lane (dừng lane < 25% sau 6 bài).
