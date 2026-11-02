# GH-23 — báo cáo cổng tham số cảnh Long

## Đã làm

- Thêm `motion/long/scene_params.py`: kiểm hợp đồng tham số không phụ thuộc render, có CLI audit chỉ-đọc.
- `build_long.py do_html` chạy kiểm tham số nguồn trước khi tải asset; sau khi `plan()` đổi neo thành `t0/t1`, chạy lại để chặn A7/A9. Lỗi dừng bằng `SystemExit` với dạng `chNN#i type: ...`.
- A4: `late_first` chặn phần tử con thứ hai của cảnh nhiều phần tử khi trễ quá 1,0 giây. `late_report` giữ chế độ baseline cho dữ liệu HTML cũ; mọi HTML mới bị chặn ở `do_html`.
- A9: `ledger_overflow` kiểm cả số dòng `rows + total`, không chỉ độ rộng.
- Thêm `tests/test_scene_params.py`, bổ sung regression A4 vào `tests/test_late_first.py`.

Không sửa `data/long/**`, engine, lịch, state, YouTube hoặc Git. Không render/TTS.

## Hợp đồng key casewide

Key chung do compiler/engine đọc: `type, at, t0, t1, tr, fade, nocaps, label, tag, credit, illus, srcnote, stamp, film, focus, bg, vid, ms, loop, sfx, tone, veil, pan, z0, z1`.
`focus` phải là `[x, y]` hai số; `pos` phải là chuỗi CSS. `maxW/maxH` là pixel và phải >= 50.

| Type | Key riêng hợp lệ | `casewide.js` |
|---|---|---:|
| chapter | `no,k,title,sub,titleAt,num,classic` | 125 |
| broll | `kin,align` | 145 |
| photo | `img,focus,frame,circles,move,reveal,zoom,kin,align` | 171 |
| print | `img,right,maxW,maxH,pos,caption,circles,rot,side` (+ `head` chỉ được giữ nếu đã có `side.h`) | 202 |
| file | `img,pos,cap,name,k,desc,rows` | 232 |
| kinetic | `items,align,accent` | 262 |
| slam | `text,fx,sub,white` | 269 |
| brand / endcard / question | `name,sub` / `sub` / `text,showAt` | 316 / 334 / 346 |
| counter / bars | `from,to,prefix,suffix,year,countAt,until,calls,sub,label` / `title,unit,max,items,calls` | 353 / 378 |
| myth / source / units | các key nội dung và mốc đúng renderer | 404 / 421 / 437 |
| timeline / map / quote / org | `items`; `geo,routes,pins,zoom,zoomK`; `text,at,typeDur,by,dy,lbl,radio,voiceAt,voiceEnd,qline`; `nodes,y0` | 453 / 469 / 500 / 520 |
| ledger / split / date / cards | `title,rows,total`; `title,a,b,sign,signAt`; `day,dayAt,date,groupAt,sub`; `cards,flips,reads,readAt,sum,sumAt,zero,zeroAt` | 539 / 551 / 564 / 587 |
| evidence / seismo / saint | `img,maxW,maxH,callouts`; `read,hit,hitAt`; `img,pos,burnAt,burnDur,burnTo,kin,align` | 604 / 626 / 656 |
| paper / pizzini / dots / board | `mast,date,ed,head,vi,img`; `notes,cipher`; `total,cols,gh,y0,appearDur,title,groups`; `pins,links` | 680 / 699 / 715 / 732 |
| memorial / calendar / sticker / sketch | `title,names,fs`; `from,days,endAt,label,months`; `items`; `art,drawDur,title` | 749 / 768 / 785 / 1103 |

Type của `lab.js`/`chart.js` không được đoán từ `casewide.js`: cổng in cảnh báo có lý do thay vì báo sai. Key lạ của type đã có trong bảng là lỗi A1.

`print.head` có nội dung nhưng không có `side.h` bị chặn vì engine chỉ vẽ `side.k`, `side.h`, `side.lines`. `head` rỗng/legacy hoặc dư thừa cùng `side.h` không làm mất tiêu đề nên không làm hỏng các bài đã sửa tay, gồm Jobs 1985.

## Ngưỡng mới

- A7: mọi scene, gồm `chapter` và `endcard`, phải trong `[2,5s, 9,0s]`; không có ngoại lệ trong `long-rules.md`.
- A4: con thứ hai của `org`, `timeline`, `rows`, `items`, `callouts` và các cảnh đa phần tử tương tự phải xuất hiện <= 1,0s từ `t0`. Dòng `kinetic` được loại vì đó là nhịp chữ tuần tự có chủ đích, không phải hai đối tượng độc lập.
- A8: mỗi key ảnh dùng <= 3 lần (cổng tồn tại khác giữ ngưỡng này); mọi key `spec.imgs` không xuất hiện ở bất kỳ `img/bg` lồng nhau nào là lỗi.
- A9: từ CSS: ledger bắt đầu y=150, padding dọc 46/54; hàng thường 76px (96px ở lab/chart); phụ đề `#caps` y=930 (noir y=1004). Dành 72px tiêu đề + 18px margin, giới hạn bảo thủ `rows + total`: default 7, noir 8, lab/chart 6. Công thức lab/chart: `150 + 46 + 72 + 18 + N×96 + 54 <= 930`, nên N=6.

## Lệnh và kết quả

```text
python -m pytest -q tests/test_scene_params.py tests/test_late_first.py tests/test_long_scene_rules.py
29 passed, 1 warning in 1.54s

python motion/long/scene_params.py mim-jobs-1985
A1=0, A7=0, A8=0, A9=0

python motion/long/scene_params.py --all --cl yakuza mafia shanghai ripper kowloon golden
```

`python -m pytest -q tests/` không hoàn tất được trong sandbox: pytest bị `PermissionError` khi tạo/đọc temporary directory `pytest-of-Tung-QA`; thử `--basetemp .pytest-gh23-first` cũng bị sandbox từ chối truy cập thư mục đó. Đây là lỗi môi trường test, không phải assertion của GH-23. Test phạm vi và regression cũ liên quan đều xanh như trên. Pytest cũng cảnh báo không ghi được `.pytest_cache`.

## Bảng hồi quy chỉ-đọc

`planned` là số chương có `output/.../data.js` để đo A7/A9. Sáu CL chuẩn không có data.js/timing, nên A7=0 ở các dòng đó nghĩa là **chưa đo được**, không phải đạt.

| Topic | Kênh | A1 | A7 | A8 | A9 |
|---|---|---:|---:|---:|---:|
| ck-2026-kenh-dau-tu | CK | 0 | 22 | 0 | 0 |
| ck-a2-luong-va-lam-phat | CK | 0 | 43 | 0 | 0 |
| ck-b1-mua-hay-thue | CK | 0 | 40 | 0 | 0 |
| ck-b2-lai-kep | CK | 2 | 20 | 0 | 0 |
| ck-b3-tra-gop-0 | CK | 2 | 23 | 0 | 0 |
| ck-b4-mua-xe | CK | 1 | 28 | 0 | 0 |
| ck-c1-vnindex-dung-yen | CK | 0 | 32 | 0 | 0 |
| ck-c2-phien-giao-dich | CK | 4 | 37 | 0 | 0 |
| ck-c3-bieu-do-nen | CK | 8 | 29 | 0 | 0 |
| ck-c4-duong-trung-binh | CK | 0 | 28 | 0 | 0 |
| ck-c5-co-tuc | CK | 3 | 20 | 0 | 0 |
| ck-c6-gia-tran-san-t2 | CK | 6 | 13 | 0 | 0 |
| ck-d1-vang-dinh | CK | 3 | 24 | 0 | 0 |
| ck-d2-fomo | CK | 0 | 25 | 0 | 0 |
| ck-d3-lo-khong-dam-ban | CK | 3 | 22 | 0 | 0 |
| ck-e1-mua-deu-moi-thang | CK | 0 | 27 | 0 | 0 |
| ck-e2-quy-khan-cap | CK | 2 | 24 | 0 | 0 |
| ck-e3-no-the-tin-dung | CK | 3 | 28 | 0 | 0 |
| ck-e4-bao-hiem-tien-gui | CK | 0 | 44 | 0 | 0 |
| ck-e5-thue-tncn-2026 | CK | 0 | 41 | 0 | 0 |
| ck-e6-luong-huu-rut-mot-lan | CK | 0 | 34 | 0 | 0 |
| ck-f1-tro-cap-that-nghiep | CK | 0 | 29 | 0 | 0 |
| ck-f2-vien-phi-bhyt | CK | 0 | 30 | 0 | 0 |
| ck-f3-tien-mung-cuoi | CK | 0 | 0 | 0 | 0 |
| ck-f4-vo-chong-chia-tien | CK | 0 | 23 | 0 | 0 |
| ck-i1-100-trieu-tiet-kiem-hay-vnindex | CK | 0 | 15 | 0 | 0 |
| golden | CL | 51 | 0* | 5 | 0 |
| kowloon | CL | 65 | 0* | 8 | 0 |
| mafia | CL | 102 | 0* | 1 | 0 |
| mim-ai-70 | MIM | 3 | 42 | 0 | 0 |
| mim-ai-chat-privacy | MIM | 0 | 19 | 0 | 0 |
| mim-ai-feed | MIM | 1 | 27 | 0 | 0 |
| mim-ai-gpu | MIM | 0 | 22 | 0 | 0 |
| mim-ai-hallucinate | MIM | 0 | 18 | 0 | 0 |
| mim-ai-jobs | MIM | 3 | 33 | 0 | 0 |
| mim-ai-khuon-mat | MIM | 3 | 22 | 0 | 0 |
| mim-ai-voice | MIM | 1 | 27 | 1 | 0 |
| mim-alphago-lee-sedol | MIM | 15 | 53 | 0 | 0 |
| mim-apollo-1202 | MIM | 10 | 32 | 0 | 0 |
| mim-captcha | MIM | 2 | 21 | 0 | 0 |
| mim-deep-blue-kasparov | MIM | 10 | 61 | 0 | 0 |
| mim-dich-may | MIM | 13 | 48 | 0 | 0 |
| mim-flappy-bird | MIM | 2 | 16 | 0 | 0 |
| mim-google-maps-kal007 | MIM | 7 | 27 | 1 | 0 |
| mim-jobs-1985 | MIM | 0 | 0 | 0 | 0 |
| mim-katherine-johnson | MIM | 2 | 23 | 0 | 4 |
| mim-ke-huy-diet-petrov | MIM | 23 | 66 | 0 | 4 |
| mim-ma-qr | MIM | 0 | 12 | 0 | 0 |
| mim-macintosh-1984 | MIM | 0 | 38 | 0 | 4 |
| mim-may-choi-game | MIM | 11 | 69 | 0 | 0 |
| mim-may-thang-poker | MIM | 9 | 49 | 0 | 0 |
| mim-moneyball | MIM | 0 | 40 | 0 | 4 |
| mim-oppenheimer-feynman | MIM | 12 | 64 | 0 | 0 |
| mim-qwerty | MIM | 2 | 25 | 0 | 0 |
| mim-siri-susan-bennett | MIM | 10 | 26 | 0 | 0 |
| mim-social-network | MIM | 0 | 33 | 0 | 4 |
| mim-turing-bombe | MIM | 0 | 27 | 0 | 0 |
| mim-watson-jeopardy | MIM | 6 | 59 | 0 | 0 |
| ripper | CL | 49 | 0* | 13 | 0 |
| shanghai | CL | 46 | 0* | 12 | 0 |
| yakuza | CL | 32 | 0* | 7 | 0 |
| **Tổng 61 topic** | — | **527** | **1700** | **48** | **24** |

## Chưa chắc / cần người phụ trách quyết định

1. `casewide.js` nạp thêm scene type từ `lab.js` và `chart.js`; ticket chỉ cho đọc casewide nên các type này được cảnh báo, không đoán bảng key. Cần ticket riêng hoặc cho phép đọc hai adapter để chuyển cảnh báo thành A1 chặn.
2. Sáu CL chuẩn không có output timing/data.js trong workspace; không thể đo duration A7 mà không TTS/render, cả hai đều ngoài phạm vi ticket.
3. Audit lỗi các video cũ là dữ liệu hồi quy để sửa từng bài, không sửa trong GH-23 theo phạm vi cấm `data/long/**`.

## QA hình/thumbnail

Không tạo clip sheet hay thumbnail vì ticket cấm render và không có topic video/thumbnail cần dựng. Không có đường dẫn clip sheet hoặc thumbnail mới.
