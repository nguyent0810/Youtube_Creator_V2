"""Bộ kiểm pillar phải BẮT được lỗi, không chỉ cho qua bản đúng."""
import dataclasses

from factory.pillars import check as C
from factory.pillars import tables as T
from factory.pillars import topics as P


def _find(d, history=()):
    return {f.area + ":" + f.msg: f.ok for f in C.check(d, P.ALL_NAMES, list(history))}


def _failed(d, history=()):
    return [k for k, ok in _find(d, history).items() if not ok]


def test_every_fixed_topic_passes():
    """839 chủ đề cố định, không bài nào được trượt bộ kiểm."""
    n = 0
    for pillar in P.CANDIDATES:
        for d in P.all_drafts(pillar):
            assert not _failed(d), (d.key, _failed(d))
            n += 1
    assert n >= 800


def test_tables_are_internally_consistent():
    """64 quẻ khác nhau và mọi cặp Văn Vương đúng luật lật/đổi -- một lỗi gõ
    trong bảng quẻ sẽ làm sai luật này."""
    assert len({q.hao for q in T.QUE}) == 64
    for n in range(0, 64, 2):
        a, b = T.QUE[n], T.QUE[n + 1]
        assert b == (T.lat_nguoc(a) if T.lat_nguoc(a) != a else T.doi_am_duong(a))
    # Lục hại = xung với bạn hợp của mình, với MỌI chi.
    for c in T.CHI:
        hai = next(x.name for x in T.CHI if T.luc_hai(c.name, x.name))
        assert T.xung_partner(T.hop_partner(c.name)) == hai


def test_wrong_relation_is_caught():
    d = P.giap_xung("Tý")
    wrong = d.script.replace("Thủy khắc Hỏa", "Hỏa khắc Thủy")
    bad_claims = [dataclasses.replace(c, fragment=c.fragment.replace("Thủy khắc Hỏa", "Hỏa khắc Thủy"),
                                      verify=lambda: T.KHAC["Hỏa"] == "Thủy")
                  if "khắc" in c.fragment else c for c in d.claims]
    d2 = dataclasses.replace(d, script=wrong, claims=bad_claims)
    assert any("claim sai" in k for k in _failed(d2))


def test_invented_sentence_is_caught():
    d = P.dich_thai_bi()
    d2 = dataclasses.replace(d, script=d.script.replace(
        "Nên mới có", "Khổng Tử đọc quẻ này ba lần mỗi sáng. Nên mới có"))
    assert any("câu không có căn cứ" in k for k in _failed(d2))


def test_absolute_promise_is_caught():
    d = P.tru_thap_than("tai")
    d2 = dataclasses.replace(d, script=d.script + " Có Tài tinh là chắc chắn giàu.")
    assert any("tuyệt đối" in k for k in _failed(d2))


def test_doctrine_without_hedge_is_caught():
    d = P.tru_thap_than("an")
    d2 = dataclasses.replace(d, script=d.script.replace("Theo quan niệm truyền thống, ", ""))
    assert _failed(d2)


def test_stray_name_from_other_topic_is_caught():
    d = P.giap_xung("Tý")
    d2 = dataclasses.replace(d, script=d.script.replace("Nhà bạn có cặp", "Giống Dần, nhà bạn có cặp"))
    assert any("tên ngoài chủ đề" in k for k in _failed(d2))


def test_repeat_topic_and_opening_are_caught():
    d = P.dich_thai_bi()
    hist = [{"pillar": "dich", "key": d.key, "angle": d.angle, "script": d.script,
             "publish_at": "2026-09-30T12:00:00Z"}]
    f = _failed(d, hist)
    assert any("chủ đề đã làm" in k for k in f) and any("mở bài trùng" in k for k in f)


def test_rotation_skips_done_topics():
    hist = [{"pillar": "giap", "key": "xung-0", "angle": "", "script": "x", "publish_at": "z"}]
    d, _ = P.next_draft("giap", hist)
    assert d.key != "xung-0"


def test_exhausted_pillar_blocks_instead_of_inventing():
    """Hết chủ đề cố định và không có loại hằng ngày -> chặn, không bịa."""
    hist = [{"pillar": "dich", "key": d.key, "angle": "", "script": "x", "publish_at": "z"}
            for d in P.all_drafts("dich")]
    nd, why = P.next_draft("dich", hist)
    assert nd is None and "nguồn" in why[0]


def test_daily_kind_takes_over_when_fixed_topics_run_out():
    from datetime import date
    hist = [{"pillar": "giap", "key": d.key, "angle": "", "script": "x", "publish_at": "z"}
            for d in P.all_drafts("giap")]
    nd, _ = P.next_draft("giap", hist, date(2026, 10, 2))
    assert nd is not None and nd.angle.startswith("hằng ngày")


def test_nap_am_table_not_vnlunar():
    """vnlunar ghi sai nạp âm; bảng của kênh phải khớp nguồn chuẩn."""
    assert T.nap_am_of(T.year_index(1984)) == "Hải Trung Kim"          # Giáp Tý
    assert T.nap_am_of(T.can_chi_60_index("Bính Tý")) == "Giản Hạ Thủy"  # vnlunar ghi Lộ Bàng Thổ
    assert T.nap_am_of(T.can_chi_60_index("Ất Hợi")) == "Sơn Đầu Hỏa"    # vnlunar ghi Đại Lâm Mộc
    assert T.nap_am_of(T.year_index(2026)) == "Thiên Hà Thủy"          # Bính Ngọ


def test_tu_animals_override_vnlunar():
    """11 video Lịch đã đọc sai con vật của tú vì tin vnlunar."""
    from factory.lunar import _tu_animal
    assert _tu_animal("Đẩu", "Hề") == "Giải trãi"
    assert _tu_animal("Tỉnh", "Dẫn") == "Hãn"
    assert _tu_animal("Thâm", "Vượn") == "Vượn"      # vnlunar gọi Sâm là Thâm


def test_hexagram_derivations():
    assert T.ho_quai(T.QUE_BY["Càn"]) == T.QUE_BY["Càn"]
    assert T.bien_quai(T.QUE_BY["Càn"], 1).name == "Cấu"
    assert T.bien_quai(T.QUE_BY["Khôn"], 1).name == "Phục"


def test_menh_example_date_is_real():
    for name, _ in T.CUNG:
        d = P.menh_tue_sai(name)
        assert "ngày 31 tháng 9" not in d.script and "ngày 32" not in d.script
