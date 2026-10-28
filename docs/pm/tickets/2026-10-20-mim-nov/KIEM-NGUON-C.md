# KIEM-NGUON-C: kiểm nguồn gốc nhóm chỉ số 15-21 (22/10/2026)

Phạm vi: game-dendi-2017, deepface-2014, game-khan-gia-chon-tuong, joy-buolamwini-mat-na-trang, facebook-xoa-mot-ti-mau, game-mana, game-alpha-red. Không sửa spec, không gọi API YouTube, không sửa state.sqlite.

Hạn chế môi trường: openai.com, about.fb.com, thecvf.com (html), qz.com, engadget, archive.org đều trả 403 / không phân giải / bị chặn khi mở trực tiếp. Chỗ mở được bản gốc ghi "MỞ"; chỗ nguồn gốc chỉ thấy qua đoạn trích trong kết quả tìm kiếm ghi "TRÍCH" (tin cậy thấp hơn MỞ, nhưng đã đối chiếu thêm từ 2 nguồn độc lập trở lên).

Kết luận chung: cả 7 bài SẠCH, không bài nào LỆCH, không cần gỡ. Không bắt buộc sửa; có vài gợi ý tuỳ chọn (cosmetic, theo quy tắc không thay bài đã upload nếu chỉ cosmetic).

## 15. mim-game-dendi-2017: SẠCH
| Khẳng định | KQ | Nguồn / trích |
|---|---|---|
| Tháng 8/2017, TI, Dendi thua bot 1v1 | KIỂM ĐƯỢC | MỞ Entrepreneur https://www.entrepreneur.com/article/298717 (bot thắng 2 ván, Dendi dừng; bài 14/8, trận thứ Sáu 11/8); MỞ Wikipedia OpenAI Five (thắng Dendi trong trận 1v1 trực tiếp) |
| Dendi người Ukraine | KIỂM ĐƯỢC | MỞ Wikipedia Dendi ("Ukrainian esports player", Danil Ishutin) |
| Bot tự chơi với chính mình, không ai dạy | KIỂM ĐƯỢC | MỞ Entrepreneur ("trained entirely through self-play") |
| Trước đó trong tuần bot thắng SumaiL và Arteezy | KIỂM ĐƯỢC (TRÍCH) | OpenAI https://openai.com/index/dota-2 (403), đoạn trích qua tìm kiếm: "Over the past week, our bot was undefeated against many top professionals including SumaiL ... and Arteezy"; Guinness (trích) ghi trận SumaiL 10/8, Dendi 11/8 |
| Một năm sau OpenAI Five (năm cỗ máy) | KIỂM ĐƯỢC | MỞ Wikipedia OpenAI Five (2018 đội năm bot) |

Chữ màn hình (2017, THÁNG TÁM, SUMAIL/ARTEEZY THUA BOT, OPENAI FIVE 2018): khớp. Lưu ý: ý SumaiL/Arteezy chỉ từ lời OpenAI; mô tả đã ghi "theo OpenAI và báo chí", ổn.

## 16. mim-deepface-2014: SẠCH
| Khẳng định | KQ | Nguồn / trích |
|---|---|---|
| Bốn triệu ảnh, hơn 4.000 người | KIỂM ĐƯỢC | MỞ PDF bài báo (bản TU Delft): "four million facial images belonging to more than 4,000 identities" |
| Nhóm Taigman (Taigman, Yang, Ranzato, Wolf) | KIỂM ĐƯỢC | cùng PDF (Facebook AI Group, Tel Aviv University) |
| DeepFace 97,35% | KIỂM ĐƯỢC | MỞ https://mlanthology.org/cvpr/2014/taigman2014cvpr-deepface (bản CVPR chính thức): "accuracy of 97.35% on the Labeled Faces in the Wild". Bản nháp TU Delft ghi 97.25% / 25%; bản CVPR cuối là 97.35% / 27%, khớp video |
| Giảm lỗi hơn 27% | KIỂM ĐƯỢC | cùng mlanthology: "reducing the error ... by more than 27%" |
| Người thật 97,53% | KIỂM ĐƯỢC | MỞ PDF bài báo, Table 3: "Human, cropped 0.9753"; MIT Technology Review (trích): "Humans scored 97.53%". Không chỉ từ Wikipedia |
| Máy kém người chưa tới 1 điểm | KIỂM ĐƯỢC | 97,53 - 97,35 = 0,18 điểm |

Gợi ý tuỳ chọn (cosmetic): nhãn màn hình "NGƯỜI THẬT (THEO WIKIPEDIA)" có thể đổi thành "NGƯỜI THẬT (THEO BÀI BÁO)"; số người thật là trên ảnh đã cắt (cropped). Không bắt buộc.

## 17. mim-game-khan-gia-chon-tuong: SẠCH
| Khẳng định | KQ | Nguồn / trích |
|---|---|---|
| 05/08/2018, San Francisco, OpenAI Five Benchmark | KIỂM ĐƯỢC (TRÍCH) | OpenAI results (403); trích tìm kiếm: lên lịch 12:30 PT ngày 5/8 ở SF, bài OpenAI đề 6/8 "yesterday"; Liquipedia (trích) |
| Năm người chơi, có Blitz | KIỂM ĐƯỢC (TRÍCH) | trích OpenAI: "Blitz, Cap, Fogged, Merlini, MoonMeander", "99.95th percentile" |
| Khoảng 100.000 người xem trực tiếp | KIỂM ĐƯỢC (TRÍCH) | trích OpenAI: "100,000 concurrent livestream viewers" |
| Máy thắng 2 ván đầu; ván ba khán giả chọn tướng cho máy; người thắng; tổng 2-1 | KIỂM ĐƯỢC (TRÍCH) | trích OpenAI: "the audience adversarially selected Five's heroes"; Liquipedia (trích): Five thắng 2-1, đội hình ván 3 do khán giả chọn |

Không có LỆCH. Mức tin cậy: không mở trực tiếp được trang OpenAI/Liquipedia/techxplore (403/451), dựa trên trích dẫn và các nguồn trùng khớp. "Họ cố ý chọn đội hình dở" khớp "adversarially selected".

## 18. mim-joy-buolamwini-mat-na-trang-2018: SẠCH
| Khẳng định | KQ | Nguồn / trích |
|---|---|---|
| Ở MIT, phần mềm không thấy mặt cô, đeo mặt nạ trắng thì thấy | KIỂM ĐƯỢC | MỞ Ford Foundation (video bài nói của chính cô) https://www.fordfoundation.org/news-and-stories/videos/joy-buolamwini-fighting-the-coded-gaze-how-we-make-artificial-intelligence-benefit-all-public-interest-tech : thạc sĩ MIT Media Lab, dự án Aspire Mirror, phần mềm nhận ra chiếc mặt nạ không khó khăn; NPR (trích): không nhận diện được mặt cô cho tới khi đeo mặt nạ trắng; Boston Globe (trích): phần mềm không "thấy" cô |
| 2018, cùng Timnit Gebru, Gender Shades | KIỂM ĐƯỢC | MỞ https://proceedings.mlr.press/v81/buolamwini18a.html |
| Ba hệ thống thương mại, đoán nam/nữ | KIỂM ĐƯỢC | cùng PMLR (3 commercial gender classification systems) |
| Đàn ông da sáng, sai tệ nhất 0,8% | KIỂM ĐƯỢC | PMLR: maximum error rate for lighter-skinned males was 0.8% |
| Phụ nữ da sẫm, sai tệ nhất 34,7% | KIỂM ĐƯỢC | PMLR: error rates of up to 34.7% |
| Đoán giới tính, không phải nhận ra danh tính | KIỂM ĐƯỢC | PMLR: gender classification |

Chuyện mặt nạ không còn chỉ từ Wikipedia: có nguồn chính cô kể (Ford Foundation/TED, NPR). Gợi ý tuỳ chọn: mô tả đang ghi "(nguồn: Wikipedia)"; có thể bổ sung "bài nói của cô / Ford Foundation" khi có dịp (không cần thay video).

## 19. mim-facebook-xoa-mot-ti-mau-khuon-mat-2021: SẠCH
| Khẳng định | KQ | Nguồn / trích |
|---|---|---|
| Tháng 11/2021 Facebook thông báo tắt nhận diện khuôn mặt | KIỂM ĐƯỢC | MỞ SBS https://www.sbs.com.au/news/facebook-to-shut-down-facial-recognition-system-and-delete-faceprints-of-one-billion-users/7a566af8-65f1-45ec-a779-f0f3cac9c251 ; AP (trích): công bố 2/11/2021 |
| Xoá hơn một tỉ mẫu khuôn mặt | KIỂM ĐƯỢC | SBS: "facial recognition templates" của hơn một tỉ người; MỞ Wikipedia DeepFace |
| Jerome Pesenti là người viết | KIỂM ĐƯỢC | SBS: Pesenti, VP AI, viết bài blog |
| Chuyển sang cách dùng hẹp như xác thực chính chủ | KIỂM ĐƯỢC | SBS: "limiting the use of facial recognition to a narrow set of use cases" (mở khoá tài khoản/thiết bị) |
| Người đang bật không còn được tự nhận diện/gắn tên trong ảnh, video | KIỂM ĐƯỢC | SBS: hệ thống tự nhận diện người trong ảnh/video bị tắt; alt text không còn nêu tên người |

Lưu ý: trang gốc about.fb.com không phân giải được; dùng SBS (mở được) + AP/CBS (trích) + Wikipedia. "Mỗi mẫu là một dãy số" là diễn giải phổ biến, không kèm số liệu nên rủi ro thấp. Vụ kiện Illinois trong mô tả: SBS không nhắc; AP/Wikipedia (BIPA) có, mô tả chỉ nói chung nên ổn.

## 20. mim-game-mana-thua-nam-van-roi-thang: SẠCH
| Khẳng định | KQ | Nguồn / trích |
|---|---|---|
| MaNa người Ba Lan, Protoss | KIỂM ĐƯỢC (TRÍCH) | PC Gamer / Synced / Vice (trích tìm kiếm): Polish, chuyên Protoss; MỞ TechCrunch: AlphaStar chỉ chơi Protoss vs Protoss |
| Tháng 12/2018 AlphaStar thắng 5-0 | KIỂM ĐƯỢC | MỞ DeepMind https://deepmind.google/discover/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/ : "AlphaStar again won by 5 games to 0", chơi 19/12; MỞ Wikipedia AlphaStar |
| Ván trực tiếp 24/01/2019: bản mới nhìn qua camera, luyện 7 ngày, MaNa thắng | KIỂM ĐƯỢC | MỞ DeepMind blog (camera interface, 7 ngày, MaNa thắng prototype); MỞ technews.tw: livestream DeepMind 24/01/2019, MaNa thắng bản retrain luyện 7 ngày; Engadget 24/01/2019 (trích); MỞ TechCrunch 24/01/2019 |
| Mười ván trước đều thuộc về máy | KIỂM ĐƯỢC | TLO 5-0 + MaNa 5-0 (Engadget "10-1", DeepMind) |
| MaNa nói giới hạn mới khiến ván đấu đáng xem; "chín tháng sau" (30/10/2019) | KIỂM ĐƯỢC | MỞ https://deepmind.google/discover/blog/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning/ : "The caps on the actions it can take and the camera view restrictions now make for compelling games"; 24/1 đến 30/10 là 9 tháng |

Ngày 24/01/2019 đã kiểm; lời đọc ghi "cuối tháng một" là đúng. Không cần sửa.

## 21. mim-game-alpha-red-tran-thang-dau: SẠCH
| Khẳng định | KQ | Nguồn / trích |
|---|---|---|
| Tháng 4/2019 OpenAI mở Arena cho mọi người | KIỂM ĐƯỢC | MỞ Vice https://vice.com/en/article/we-will-win-openais-dota-2-team-is-crushing-humans-online-but-players-are-not-giving-up : thử thách công khai 18-21/4/2019 |
| Năm ngày trước máy thắng OG (nhà vô địch) | KIỂM ĐƯỢC | Vice: vừa thắng OG; MỞ Wikipedia OpenAI Five (OG, TI 2018 champions); OG thua 13/4, đến 18/4 là 5 ngày |
| Alpha Red (Thái Lan), vài giờ sau thắng ván ~45 phút | KIỂM ĐƯỢC | Vice: "just hours after the test began", "around 45 minutes", 34-24 kills; MỞ OneEsports |
| Brockman: chiến thắng đầu tiên của con người | KIỂM ĐƯỢC | Vice nhúng tweet @gdb 19/4/2019: "First human victory!!" |
| Tuyển thủ Thụy Điển: máy không học nữa, còn chúng tôi thì có | KIỂM ĐƯỢC | Vice: Niklas "Wagamama" Hogstrom: "They are not learning, but we humans are." |
| Máy thắng 7.215 ván, thua 42 | KIỂM ĐƯỢC | MỞ OneEsports (tiêu đề 7,215; 42 thua; thân bài có 1 lỗi gõ 7,257), MỞ PC Games Insider ("7,215 games against 42 human wins", 99,4%), Engadget (trích): bài đăng OpenAI ghi 7,215 thắng / 42 thua; 99,4% = 7215/7257. Không dùng "42.729" (tổng gồm cả ván hợp tác, đúng ghi chú nội bộ) |

Lưu ý: trang OpenAI/tweet gốc chưa mở trực tiếp; 7.215/42 được ba nguồn báo chí độc lập xác nhận và khớp phép tính 99,4%. Mô tả ghi "Theo OpenAI qua Engadget" nên đúng nguồn.
