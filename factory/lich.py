"""Dựng Bundle Lịch cho MỘT ngày từ dữ kiện đã đối chiếu kép.

Dùng chung cho scripts/make_lich_month.py (sinh mới) và scripts/replace_lich.py
(thay bản sai N1): hai nơi phải ra đúng một bundle cho cùng một ngày, nếu không
bản "thay" sẽ khác bản "sinh" và kiểm chéo lô mất ý nghĩa.
"""
from __future__ import annotations

from factory.bundle import Bundle
from factory.compose import script_for
from factory.factcheck import report
from factory.vocab import broll_for

CHANNEL = "FS"
VOICE = "Anh Khôi"
BGM = "asian_drums.mp3"

# B-roll theo THẾ của ngày, không theo từng ngày: thế quyết định tông của
# kịch bản (siết / mở / cùng thuận / cùng đóng) nên hình cũng nên theo đó.
BROLL = {
    "sao_mo_truc_siet": ["calm vietnamese home interior", "wooden door closed detail",
                         "morning light through window", "quiet traditional house"],
    "sao_du_truc_mo":   ["open road sunrise vietnam", "busy market morning",
                         "hands counting money", "wooden gate opening"],
    "cung_dong":        ["repairing wall plaster hands", "closed wooden shutters",
                         "cement trowel work detail", "quiet empty room"],
    "cung_thuan":       ["vietnamese shop opening morning", "sunrise over rice field",
                         "incense smoke altar close up", "warm home interior daylight"],
}


def build_bundle(f) -> tuple[Bundle | None, str, str]:
    """(bundle, báo cáo đối chiếu, thế của ngày).

    Bundle là None khi kịch bản KHÔNG qua bộ đối chiếu: fail-closed, thà thiếu
    một ngày còn hơn đăng một ngày sai, vì người xem làm theo."""
    sc = script_for(f)
    ok, text = report(sc["script"], f, f.publish_at, label=str(f.target))
    if not ok:
        return None, text, sc["the"]
    b = Bundle(
        channel=CHANNEL, kind="short", slug=f.slug,
        script=sc["script"],
        title=sc["title"],
        description=(
            f"Lịch ngày {f.target.strftime('%d/%m/%Y')} — âm lịch {f.lunar_day}/{f.lunar_month}, "
            f"ngày {f.can_chi_day}, sao {f.god_name}, {f.truc_name}.\n"
            f"Nên làm: {', '.join(f.truc_good_for)}.\n"
            f"Kiêng: {', '.join(f.truc_bad_for)}.\n\n"
            "Ghi chép theo lịch pháp truyền thống, để tham khảo."
        ),
        tags=["phong thuy", "lich van nien", "ngay tot", "lich am"],
        thumbnail_text="",
        publish_at=f.publish_at,
        voice=VOICE, bgm=BGM,
        # Hình bám DANH MỤC VIỆC THẬT của ngày, không bám thế: chỉ có 4
        # thế nên 61 video trước đó dùng chung đúng 4 bộ từ khoá.
        broll_queries=broll_for(f.truc_good_for, BROLL[sc["the"]], offset=f.target.day),
        source_note=(f"lịch {f.target}: {f.can_chi_day}, sao {f.god_name}, {f.truc_name} "
                     f"(tính độc lập + vnlunar, khớp)"),
    )
    b.validate()
    return b, text, sc["the"]
