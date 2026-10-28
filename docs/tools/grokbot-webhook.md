# Hướng dẫn gọi Grok Bot (Flow) từ CLI / Script qua Webhook

Tài liệu này dành cho CLI agent (như Codex CLI, Claude Code, hoặc script Python/PowerShell) đọc và tự động gửi yêu cầu sang cho trợ lý **Flow (Grok Bot)** thực hiện các tác vụ cần trình duyệt hoặc tạo ảnh trên ChatGPT.

---

## 1. Lấy Webhook URL và Sender Key (chỉ cần làm 1 lần)

1. Mở ứng dụng **Grok Bot**, vào cuộc trò chuyện với **Flow**.
2. Bấm vào tên **Flow** ở thanh tiêu đề trên cùng (hoặc nhấn `Cmd+Shift+I` / mở tab **Routines** ở thanh bên phải).
3. Trong mục **Routines**, chọn routine tên **`CLI Trigger`**.
4. Sao chép **Webhook URL** và **Sender Key** (khóa xác thực), rồi lưu vào biến môi trường trên máy Windows của bạn (hoặc file `.env`):
   - `GROKBOT_WEBHOOK_URL`: URL webhook của routine `CLI Trigger`
   - `GROKBOT_WEBHOOK_KEY`: Sender key của routine `CLI Trigger`

*(Mẹo: Bạn có thể lưu cố định vào User Environment Variables trên Windows bằng PowerShell:)*
```powershell
[Environment]::SetEnvironmentVariable("GROKBOT_WEBHOOK_URL", "https://...", "User")
[Environment]::SetEnvironmentVariable("GROKBOT_WEBHOOK_KEY", "your-sender-key", "User")
```

---

## 2. Cách gửi yêu cầu từ CLI (PowerShell / CMD / Python)

Khi CLI cần nhờ **Flow** làm việc (ví dụ: đọc file `ai_prompts.md`, tạo ảnh bằng ChatGPT trên trình duyệt, chuẩn hóa 1920x1080 và lưu vào thư mục chỉ định trên máy `DESKTOP-2JA218A`), chỉ cần gửi một HTTP `POST` tới Webhook URL kèm header xác thực `Authorization: Bearer <GROKBOT_WEBHOOK_KEY>` (hoặc `X-Webhook-Secret: <GROKBOT_WEBHOOK_KEY>`).

### Cách A: Gọi bằng PowerShell
```powershell
$url = $env:GROKBOT_WEBHOOK_URL
$key = $env:GROKBOT_WEBHOOK_KEY

$payload = @{
    task = "generate_images"
    prompt_file = "D:\Tools\Youtube Creator v2\Youtube_Creator_V2\data\long\mim-katherine-johnson\ai_prompts.md"
    output_dir  = "D:\Tools\Youtube Creator v2\Youtube_Creator_V2\motion\hf\assets\long\mim-katherine-johnson\img\ai"
    instructions = "Đọc file prompt_file, tạo đủ các ảnh minh họa 16:9 cỡ 1920x1080 bằng ChatGPT (không chữ, không số, không logo, không lộ mặt người) và lưu vào output_dir."
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri $url -Method Post `
    -Headers @{
        "Authorization"    = "Bearer $key"
        "X-Webhook-Secret" = $key
    } `
    -ContentType "application/json; charset=utf-8" `
    -Body ([System.Text.Encoding]::UTF8.GetBytes($payload))
```

### Cách B: Gọi bằng `curl` (trong CMD hoặc Git Bash)
```bash
curl -X POST "$GROKBOT_WEBHOOK_URL" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Authorization: Bearer $GROKBOT_WEBHOOK_KEY" \
  -H "X-Webhook-Secret: $GROKBOT_WEBHOOK_KEY" \
  -d "{\"task\":\"generate_images\",\"prompt_file\":\"D:\\\\Tools\\\\Youtube Creator v2\\\\Youtube_Creator_V2\\\\data\\\\long\\\\mim-katherine-johnson\\\\ai_prompts.md\",\"output_dir\":\"D:\\\\Tools\\\\Youtube Creator v2\\\\Youtube_Creator_V2\\\\motion\\\\hf\\\\assets\\\\long\\\\mim-katherine-johnson\\\\img\\\\ai\",\"instructions\":\"Tạo đủ ảnh 1920x1080 theo prompt_file và lưu vào output_dir\"}"
```

### Cách C: Gọi từ Python (`gen_scenes.py` hoặc script tự động)
```python
import os
import json
import urllib.request

def trigger_grokbot(task_instructions: str, prompt_file: str = "", output_dir: str = ""):
    url = os.environ["GROKBOT_WEBHOOK_URL"]
    key = os.environ["GROKBOT_WEBHOOK_KEY"]
    data = json.dumps({
        "instructions": task_instructions,
        "prompt_file": prompt_file,
        "output_dir": output_dir,
    }, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {key}",
            "X-Webhook-Secret": key,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, resp.read().decode("utf-8", errors="replace")
```

---

## 3. Luồng hoạt động và cách CLI kiểm tra kết quả

1. Ngay khi nhận `POST`, routine **`CLI Trigger`** sẽ đánh thức **Flow (Grok Bot)** chạy ngầm.
2. **Flow** sẽ tự đọc file yêu cầu trên máy `DESKTOP-2JA218A`, điều khiển trình duyệt ChatGPT (đã đăng nhập sẵn), tạo ảnh, chuẩn hóa kích thước `1920x1080` PNG và ghi trực tiếp vào thư mục đích `output_dir`.
3. Vì quá trình tạo 6 ảnh trên ChatGPT mất khoảng **4–6 phút**, CLI agent sau khi bắn Webhook có thể:
   - Theo dõi thư mục `output_dir` (poll mỗi 15–30 giây) chờ đủ các file `ai_01.png` … `ai_NN.png` xuất hiện.
   - Hoặc người dùng xem thông báo hoàn tất trực tiếp trong cửa sổ chat Grok Bot.
