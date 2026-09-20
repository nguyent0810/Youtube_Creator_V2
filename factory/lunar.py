"""Sự thật lịch — dữ liệu tính toán được, KHÔNG BAO GIỜ do model nghĩ ra.

Đây là ranh giới quan trọng nhất của kênh Phong Thủy: ngày âm, Can Chi,
Hoàng Đạo/Hắc Đạo, giờ tốt, hướng tốt đều là dữ kiện KHÁCH QUAN. Sai là sai
thật, và người xem làm theo thì ảnh hưởng thật.

Nên chúng đi qua vnlunar, không qua trí nhớ của bất kỳ ai. Pha sinh kịch bản
chỉ được DIỄN GIẢI các con số này cho hấp dẫn, tuyệt đối không thêm bớt.

ĐĂNG TRƯỚC MỘT NGÀY: nội dung của ngày D lên lúc 6h sáng ngày D-1. Biết giờ
tốt/hướng tốt vào đúng buổi sáng hôm đó thì đã muộn để sắp xếp công việc.
Kéo theo một ràng buộc BẮT BUỘC về câu chữ: kịch bản phải xưng "ngày mai",
không phải "hôm nay" -- lùi lịch mà giữ câu chữ cũ thì người xem làm theo
giờ tốt vào SAI NGÀY.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

# 6h sáng ICT = 23:00 UTC ngày hôm trước.
# Sáu sao hoàng đạo trong hệ 12 sao. Còn lại là hắc đạo.
AUSPICIOUS_GODS = frozenset({"Thanh Long", "Minh Đường", "Kim Quỹ",
                             "Ngọc Đường", "Thiên Đức", "Tư Mệnh"})

PUBLISH_UTC_HOUR, PUBLISH_UTC_MINUTE = 23, 0
LEAD_DAYS = 1


@dataclass(frozen=True)
class DayFacts:
    """Sự thật lịch của MỘT ngày. Mọi trường đều từ vnlunar."""
    target: date
    lunar_day: int
    lunar_month: int
    can_chi_day: str
    day_type: str          # "Hoàng Đạo" | "Hắc Đạo"
    god_name: str          # sao của ngày, vd "Kim Quỹ", "Thiên Đức"
    truc_name: str         # vd "Trực thành"
    truc_good_for: tuple
    truc_bad_for: tuple
    star_name: str         # 12 trực tinh, vd "Định"
    star_desc: str
    mansion_name: str      # nhị thập bát tú, vd "Khuê"
    mansion_good: bool

    @property
    def publish_at(self) -> str:
        """ISO UTC. 6h ICT ngày (target - LEAD_DAYS) = 23:00 UTC ngày trước đó."""
        day = self.target - timedelta(days=1 + LEAD_DAYS)
        return datetime(day.year, day.month, day.day, PUBLISH_UTC_HOUR,
                        PUBLISH_UTC_MINUTE, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @property
    def is_auspicious_star(self) -> bool:
        """Dựa trên SAO, không dựa trên `day_type`.

        vnlunar có hai trường và chúng mâu thuẫn ở 3/7 ngày đầu tháng 10:
        day_type nói Hắc Đạo trong khi sao là Kim Quỹ (hoàng đạo), v.v.
        Trường `12_gods` tự nhất quán (auspicious luôn đi với "Sao tốt -
        Hoàng Đạo") và khớp truyền thống, nên nó là trường đáng tin. Cố ý
        KHÔNG expose day_type ra ngoài để không ai lỡ dùng nhầm."""
        return self.god_name in AUSPICIOUS_GODS

    @property
    def slug(self) -> str:
        return f"lich-{self.target.strftime('%Y%m%d')}"


def facts_for(target: date) -> DayFacts:
    import vnlunar
    info = vnlunar.get_full_info(target.day, target.month, target.year)
    truc = info.get("12_constructions") or {}
    gods = info.get("12_gods") or {}
    stars = info.get("12_stars") or {}
    mansion = info.get("28_mansions") or {}
    return DayFacts(
        target=target,
        lunar_day=info["lunar"]["day"],
        lunar_month=info["lunar"]["month"],
        can_chi_day=info["can_chi"]["day"],
        day_type=(info.get("day_type") or {}).get("type", ""),
        god_name=gods.get("name", ""),
        truc_name=truc.get("name", ""),
        truc_good_for=tuple(truc.get("good_for") or ()),
        truc_bad_for=tuple(truc.get("bad_for") or ()),
        star_name=stars.get("name", ""),
        star_desc=stars.get("description", ""),
        mansion_name=mansion.get("name", ""),
        mansion_good=bool(mansion.get("good")),
    )


def facts_range(start: date, days: int) -> list[DayFacts]:
    return [facts_for(start + timedelta(days=i)) for i in range(days)]
