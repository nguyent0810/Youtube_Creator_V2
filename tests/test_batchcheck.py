"""Khoá lớp kiểm chéo cả lô.

Mỗi test dựng lại một cách hỏng mà kiểm TỪNG bundle riêng lẻ không bao giờ
thấy — và cái đầu tiên đã gây hậu quả thật: 9 video không lên được kênh.
"""
from factory.batchcheck import check_batch
from factory.bundle import Bundle


def _b(**over) -> Bundle:
    base = dict(
        channel="FS", kind="short", slug="ngay-mot",
        script=("Ngày mai là ngày hoàng đạo, nhưng lịch chỉ cho làm ba việc. "
                "Sao là Kim Quỹ, thuộc nhóm hoàng đạo. Trực là Trực nguy. "
                "Danh mục nên làm gồm ba việc quanh chỗ nằm. "
                "Hoàng đạo không có nghĩa là muốn làm gì cũng được."),
        title="01/10 — Kim Quỹ gặp Trực nguy",
        description="mô tả", tags=["phong thuy"], thumbnail_text="",
        publish_at="2026-09-29T23:00:00Z", voice="Anh Khôi",
        bgm="asian_drums.mp3", broll_queries=["calm interior"],
    )
    base.update(over)
    return Bundle(**base)


def _fails(bundles) -> list[str]:
    return [i.msg for i in check_batch(bundles) if not i.ok]


def test_duplicate_titles_are_caught():
    """LỖI THẬT: tiêu đề sinh từ (sao, trực), mà cả hai đều chu kỳ 12 ngày
    nên cứ 12 ngày lặp một cặp. 9 cặp ngày trùng tiêu đề trong tháng 10, và
    bộ chống trùng của publish.py đã bỏ qua 9 lần upload — 9 ngày không có
    video, trong khi store ghi là đã đăng.

    Không phép kiểm đơn-bundle nào bắt được: từng bundle xét riêng đều hợp
    lệ hoàn toàn."""
    a = _b(slug="ngay-mot", publish_at="2026-09-29T23:00:00Z")
    b = _b(slug="ngay-hai", publish_at="2026-09-30T23:00:00Z")   # cùng title
    msgs = _fails([a, b])
    assert msgs and "TRÙNG TIÊU ĐỀ" in msgs[0]


def test_unique_titles_pass():
    # Phải đổi CẢ kịch bản, không chỉ tiêu đề: bộ kiểm còn soi trùng nguyên
    # văn và lặp khuôn mở bài. Bản đầu của test này chỉ đổi tiêu đề/slug nên
    # bị bắt đúng — lỗi nằm ở fixture, không nằm ở bộ kiểm.
    a = _b(slug="ngay-mot", title="01/10 — A", publish_at="2026-09-29T23:00:00Z",
           script=("Ngày mai là ngày hoàng đạo, nhưng lịch chỉ cho làm ba việc. "
                   "Sao là Kim Quỹ. Danh mục quanh chỗ nằm. Chốt của bản một."))
    b = _b(slug="ngay-hai", title="02/10 — B", publish_at="2026-09-30T23:00:00Z",
           script=("Sao xấu, mà ngày mai cửa vẫn mở khá rộng. "
                   "Sao là Bạch Hổ. Danh mục xoay quanh thu về. Chốt của bản hai."))
    assert not _fails([a, b])


def test_duplicate_publish_time_is_caught():
    """Hai video cùng giờ đăng thì lên cùng lúc, chồng nhau trong feed."""
    a = _b(slug="ngay-mot", title="01/10 — A")
    b = _b(slug="ngay-hai", title="02/10 — B")   # cùng publish_at
    assert any("trùng giờ đăng" in m for m in _fails([a, b]))


def test_identical_scripts_are_caught():
    a = _b(slug="ngay-mot", title="01/10 — A", publish_at="2026-09-29T23:00:00Z")
    b = _b(slug="ngay-hai", title="02/10 — B", publish_at="2026-09-30T23:00:00Z")
    assert any("trùng nguyên văn" in m for m in _fails([a, b]))


def test_formulaic_openings_are_caught():
    """Đây là thứ người dùng chỉ ra bằng mắt mà bộ chấm đơn-bundle cho qua
    hết: cả 7 kịch bản đều ĐẠT nhưng đều mở bằng 'Lịch cũ gọi ngày mai
    là...'. Từng bản hay, xem liên tiếp thì thấy ngay công thức."""
    bundles = []
    for i in range(10):
        bundles.append(_b(
            slug=f"ngay-{i}", title=f"{i:02d}/10 — X",
            publish_at=f"2026-10-{i + 1:02d}T23:00:00Z",
            script=(f"Lịch cũ gọi ngày mai là Trực số {i}. "
                    "Sao là Kim Quỹ, thuộc nhóm hoàng đạo. "
                    f"Danh mục nên làm có {i} việc. Chốt lại ở đây nhé bạn."),
        ))
    assert any("mở bài" in m for m in _fails(bundles))


def test_varied_openings_pass():
    opens = ["Ngày mai là ngày hoàng đạo", "Sao xấu mà cửa vẫn mở",
             "Cả ngày mai chỉ còn ba việc", "Ngày mai hai tầng không chỏi nhau",
             "Việc hôm trước lịch kiêng"]
    bundles = []
    for i in range(10):
        bundles.append(_b(
            slug=f"ngay-{i}", title=f"{i:02d}/10 — X",
            publish_at=f"2026-10-{i + 1:02d}T23:00:00Z",
            script=(f"{opens[i % len(opens)]} thứ {i}. "
                    "Sao là Kim Quỹ, thuộc nhóm hoàng đạo. "
                    f"Danh mục nên làm có {i} việc. "
                    f"Chốt riêng của bản số {i} nằm ở đây."),
        ))
    assert not any("mở bài" in m for m in _fails(bundles))


def test_single_item_batch_is_fine():
    assert not _fails([_b()])
