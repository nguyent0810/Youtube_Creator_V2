"""Đo độ lặp khuôn theo dòng (bước 5, docs/audit/2026-10-05-variety-design.md).

Không phải cổng: không chặn gì. Ghi vào brief tuần để pha sinh (chat) thấy
dòng nào đang lặp khuôn trước khi viết lô mới.
"""
import json
from datetime import date

from factory import sameness
from factory.bundle import Bundle


def b(slug, script, day, *, channel="FS", bgm="a.mp3", broll=("x", "y")):
    return Bundle(channel=channel, kind="short", slug=slug, script=script, title=slug, description="d",
                  tags=["t"], thumbnail_text="", publish_at=f"2026-{day}T23:00:00Z", voice="Anh Khôi",
                  bgm=bgm, broll_queries=list(broll))


def test_a_sentence_differing_only_in_numbers_or_slot_names_is_the_same_shape():
    assert sameness.shape("Giờ tốt đầu tiên trong ngày là giờ Tý (23-1h).") == \
        sameness.shape("Giờ tốt đầu tiên trong ngày là giờ Dần (3-5h).")
    assert sameness.shape("Còn 5 ngày nữa là tới vía.") == sameness.shape("Còn 12 ngày nữa là tới vía.")
    assert sameness.shape("Sao mở, trực siết.") != sameness.shape("Sao thì mở, trực thì siết.")


def test_share_is_the_max_against_any_one_neighbour_then_the_median_across_videos():
    # Trung vị của MỌI cặp sẽ giấu đúng hàng xóm đáng sợ: bài nào cũng có một
    # bài gần như sinh đôi, nhưng đa số cặp thì khác nhau.
    same = "Câu một chung. Câu hai chung. Câu ba chung."
    words = ["táo", "cam", "lê", "mận"]          # chữ thường: tên riêng viết hoa bị gộp thành một khuôn
    bs = [b(f"lich-{i}", f"Mở bài {words[i]} riêng. {same}", f"11-{10 + i:02d}") for i in range(4)]
    bs += [b(f"lich-x{i}", f"Hoàn toàn khác {w}. Không trùng gì {w} cả.", f"11-{20 + i:02d}")
           for i, w in enumerate(["xanh", "đỏ"])]     # số bị gộp thành '#', nên dùng chữ
    st = sameness.line_stats(bs, channel="FS")
    lich = next(s for s in st if s.line == "lich-")
    assert lich.n == 6
    assert lich.median_share == 0.75          # 4 bài: 3/4 câu trùng một hàng xóm; 2 bài: 0


def test_lines_are_the_channel_prefixes_and_other_lines_never_count_as_neighbours():
    s = "Một câu y hệt nhau. Thêm một câu y hệt."
    st = sameness.line_stats([b("lich-1", s, "11-01"), b("giap-1", s, "11-02")], channel="FS")
    assert {x.line: x.median_share for x in st} == {"lich-": 0.0, "giap-": 0.0}


def test_the_window_is_the_last_28_days_of_each_line():
    s = "Một câu y hệt nhau. Thêm một câu y hệt."
    st = sameness.line_stats([b("lich-old", s, "09-01"), b("lich-new", s, "11-01"),
                              b("lich-new2", "Khác hẳn. Hoàn toàn.", "11-02")], channel="FS")
    assert next(x for x in st if x.line == "lich-").n == 2


def test_top_sentences_bgm_and_broll_sets():
    words = ["táo", "cam", "lê", "mận"]
    bs = [b(f"lich-{i}", f"Giờ tốt là giờ Tý ({i}-{i + 1}h). Câu riêng {words[i]}.", f"11-{10 + i:02d}",
            bgm="drums.mp3" if i < 3 else "flute.mp3", broll=("b", "a") if i % 2 else ("a", "b"))
          for i in range(4)]
    lich = sameness.line_stats(bs, channel="FS")[0]
    assert lich.top[0] == (sameness.shape("Giờ tốt là giờ Tý (1-2h)."), 4)
    assert lich.bgm_share == 0.75
    assert lich.broll_share == 1.0            # cùng BỘ hình, chỉ đổi thứ tự -> vẫn là lặp


def test_render_names_the_lines_that_repeat_most_first():
    rep = [b(f"menh-{i}", "Câu chung một. Câu chung hai. Câu chung ba.", f"11-{10 + i:02d}") for i in range(3)]
    ok = [b(f"giap-{i}", f"Riêng {w} hẳn. Không giống {w}.", f"11-{10 + i:02d}")
          for i, w in enumerate(["xanh", "đỏ", "tím"])]
    md = sameness.render(sameness.line_stats(rep + ok, channel="FS"))
    assert md.index("menh-") < md.index("giap-")
    assert "100%" in md


def test_brief_survives_a_broken_bundle_file(tmp_path):
    (tmp_path / "FS").mkdir()
    (tmp_path / "FS" / "lich-bad.json").write_text("{not json", encoding="utf-8")
    md = sameness.render_for("FS", base=tmp_path)
    assert "Độ lặp khuôn" in md and "lỗi" in md


def test_brief_section_reads_bundles_from_disk(tmp_path):
    (tmp_path / "FS").mkdir()
    for i in range(2):
        x = b(f"lich-{i}", "Một câu y hệt nhau. Thêm một câu y hệt.", f"11-0{i + 1}")
        (tmp_path / "FS" / f"{x.slug}.json").write_text(json.dumps(x.to_dict(), ensure_ascii=False), encoding="utf-8")
    assert "lich-" in sameness.render_for("FS", base=tmp_path)


def test_s_tier_and_long_have_no_bed_or_broll_to_compare():
    x = Bundle(channel="CL", kind="short", slug="cl-hs-a", script="Một câu đủ dài. Câu nữa.", title="t",
               description="d", tags=["t"], thumbnail_text="", publish_at="2026-11-01T23:00:00Z", voice="v",
               bgm="", broll_queries=["hyperframes-casefile"])
    st = sameness.line_stats([x], channel="CL")[0]
    assert (st.bgm_share, st.broll_share) == (None, None)
    assert "—" in sameness.render([st])


def test_a_channel_without_bundles_says_so():
    assert "chưa có bundle" in sameness.render([])
