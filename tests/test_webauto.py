"""webauto: phần logic thuần (parse file, luật chặn, dựng prompt, CLI). Không mở trình duyệt, không mạng.

Phần chạm trình duyệt (Flow, ChatGPT, Muse, TikTok) chỉ kiểm bằng tay, vì phụ thuộc giao diện trang.
"""
import json

import pytest

from webauto import chatgpt, cli, common, flow, muse, tiktok
from webauto.browsentic import parse_payload


def test_slug_bo_dau_va_chu_d():
    assert common.slug("Đức Phật dạy") == "duc-phat-day"
    assert common.slug("!!!") == "item"
    assert len(common.slug("a" * 100)) == 40


def test_parse_prompts_ten_va_danh_so(tmp_path):
    f = tmp_path / "p.txt"
    f.write_text("# ghi chú\n\nfox | red fox in snow\nA lighthouse at dusk\nname |\n", encoding="utf-8")
    got = common.parse_prompts(f)
    assert got[0] == ("fox", "red fox in snow")
    assert got[1] == ("002_a-lighthouse-at-dusk", "A lighthouse at dusk")
    assert got[2][1] == "name |"  # "tên |" không có prompt thì cả dòng là prompt


def test_parse_blocks_gom_dong_va_bo_chu_thich(tmp_path):
    f = tmp_path / "q.txt"
    f.write_text("# c\nmột\nhai\n\nba\n\n\nbốn", encoding="utf-8")
    assert common.parse_blocks(f) == ["một hai", "ba", "bốn"]


def test_write_md_co_ghi_chu_chua_kiem_chung(tmp_path):
    p = common.write_md(tmp_path / "sub" / "r.md", "Tiêu đề", {"Nguồn": "x"}, common.UNVERIFIED_NOTE, "nội dung")
    t = p.read_text(encoding="utf-8")
    assert t.startswith("# Tiêu đề")
    assert "chưa được kiểm chứng" in t and "- Nguồn: x" in t and t.rstrip().endswith("nội dung")


def test_parse_payload_lay_json_trong_phong_bi():
    text = 'Untrusted page content follows.\n<<<x>>>\n{"a": 1, "b": {"c": "}"}}\n<<<y>>>'
    assert parse_payload(text) == {"a": 1, "b": {"c": "}"}}
    assert parse_payload("không có json") == {}


def test_last_reply_cat_phan_chan_trang():
    full = "x\nChatGPT said:\ncũ\nYou said:\nhỏi\nChatGPT said:\nTrả lời mới\nChatGPT can make mistakes. Check.\nLatest response"
    assert chatgpt.last_reply(full) == "Trả lời mới"
    assert chatgpt.last_reply("chưa có trả lời") == ""


def test_build_review_prompt_co_ten_va_khung_code():
    p = chatgpt.build_review_prompt("Hãy review", "retro.md", "# Tiêu đề")
    assert p.startswith("Hãy review") and "retro.md" in p and "```markdown\n# Tiêu đề\n```" in p


ROWS = [
    {"id": "1111", "title": "a", "privacy": "Only me", "more_selector": "#b1"},
    {"id": "2222", "title": "b", "privacy": "Everyone", "more_selector": "#b2"},
    {"id": "⟦card:x⟧…3333", "title": "c", "privacy": "Only me", "more_selector": None},
    {"id": "11112", "title": "d", "privacy": "Only me", "more_selector": "#b4"},
    {"id": "4444", "title": "e", "privacy": "Only me", "more_selector": "#b5"},
]


def test_delete_chi_xoa_bai_rieng_tu_khop_dung_mot_dong():
    assert tiktok.check_delete(ROWS, "4444", False)["title"] == "e"
    assert tiktok.check_delete(ROWS, "2222", True)["title"] == "b"  # công khai chỉ khi có --allow-public


@pytest.mark.parametrize("pid,allow", [
    ("2222", False),   # bài công khai
    ("9999", False),   # không có dòng nào
    ("111", False),    # id thiếu số: trước đây khớp kiểu "chứa trong", nay phải khớp đúng
    ("3333", True),    # id bị che, không có nút "…"
])
def test_delete_tu_choi(pid, allow):
    with pytest.raises(SystemExit):
        tiktok.check_delete(ROWS, pid, allow)


def test_delete_khop_id_chinh_xac():
    assert tiktok.check_delete(ROWS, "1111", False)["title"] == "a"   # không lẫn với 11112


def _el(y, **kw):
    return {"bounds": {"x": 1400, "y": y, "width": 34, "height": 20}, **kw}


def test_ghep_dong_theo_toa_do_khong_theo_thu_tu():
    links = [_el(100, href="/video/1", text="a"), _el(200, href="/video/2", text="b"), _el(300, href="/video/3", text="c")]
    # dòng giữa thiếu cả nút quyền xem lẫn nút "…": ghép theo chỉ số sẽ đẩy nút của dòng 3 lên dòng 2
    priv = [_el(300, text="Everyone"), _el(100, text="Only me")]
    mores = [_el(102, selector="#m1"), _el(301, selector="#m3")]
    rows = tiktok.pair_rows(links, priv, mores)
    assert [(r["id"], r["privacy"], r["more_selector"]) for r in rows] == [
        ("1", "Only me", "#m1"), ("2", "?", None), ("3", "Everyone", "#m3")]
    with pytest.raises(SystemExit):
        tiktok.check_delete(rows, "2", True)


def test_create_mac_dinh_rieng_tu():
    tiktok.check_create("private", False)
    with pytest.raises(SystemExit):
        tiktok.check_create("public", False)
    tiktok.check_create("public", True)


def test_flow_image_can_mode_video():
    with pytest.raises(SystemExit):
        flow.generate([("a", "b")], "out", mode="image", image="x.png")


def test_cli_dung_duoc_moi_lenh():
    p = cli.build_parser()
    g = p.parse_args(["flow", "generate", "--prompt", "x"])
    assert (g.mode, g.count, g.duration, g.quality) == ("image", 1, 6, "720p")
    v = p.parse_args(["flow", "generate", "--mode", "video", "--image", "a.png", "--prompts-file", "f"])
    assert v.mode == "video" and v.image == "a.png"
    assert p.parse_args(["chatgpt", "images", "--prompts-file", "f"]).gap == 5
    assert p.parse_args(["chatgpt", "ask", "--file", "d.md"]).file == "d.md"
    assert p.parse_args(["muse", "research", "--questions", "q", "--out", "o"]).min_chars == 1500
    assert p.parse_args(["tiktok", "create", "--video", "v.mp4"]).privacy == "private"
    with pytest.raises(SystemExit):
        p.parse_args(["tiktok", "delete"])  # thiếu --id
    with pytest.raises(SystemExit):
        p.parse_args(["flow", "generate"])  # thiếu --prompt / --prompts-file


def test_browsentic_server_params_theo_bien_moi_truong(monkeypatch):
    pytest.importorskip("mcp")
    from webauto.browsentic import server_params
    monkeypatch.setenv("WEBAUTO_BROWSENTIC_CMD", "browsentic mcp")
    sp = server_params()
    assert (sp.command, sp.args) == ("browsentic", ["mcp"])


def test_home_theo_bien_moi_truong(monkeypatch, tmp_path):
    monkeypatch.setenv("WEBAUTO_HOME", str(tmp_path))
    assert common.profile_dir("flow") == tmp_path / "profiles" / "flow"
    assert (tmp_path / "profiles" / "flow").is_dir()


def test_nap_cli_khong_keo_mcp_va_playwright():
    """`python -m webauto --help` phải chạy trên máy chưa cài hai thư viện nặng: chỉ import khi dùng."""
    import subprocess
    import sys
    code = ("import sys, webauto.cli; "
            "sys.exit(1 if ('mcp' in sys.modules or 'playwright' in sys.modules) else 0)")
    assert subprocess.run([sys.executable, "-c", code]).returncode == 0
    assert muse.URL.startswith("https://") and json.loads("{}") == {}


# --- tiktok create --schedule (28/10/2026) ---
from datetime import datetime  # noqa: E402

TZ7 = tiktok.tz_of("GMT+7")
NOW = datetime(2026, 10, 28, 12, 0, tzinfo=TZ7)


def test_hen_gio_hop_le_doc_theo_mui_gio_trang():
    w = tiktok.check_schedule("2026-11-05 19:45", TZ7, NOW)
    assert (w.year, w.month, w.day, w.hour, w.minute) == (2026, 11, 5, 19, 45)
    assert w.utcoffset().total_seconds() == 7 * 3600


@pytest.mark.parametrize("text", [
    "2026-11-05 19:47",     # phút không chia hết cho 5: bộ chọn không có
    "2026-10-28 12:10",     # dưới 20 phút
    "2026-11-08 12:05",     # quá 10 ngày (giới hạn TikTok)
    "05/11/2026 19:45",     # sai định dạng
])
def test_hen_gio_tu_choi(text):
    with pytest.raises(SystemExit):
        tiktok.check_schedule(text, TZ7, NOW)


def test_mui_gio():
    assert tiktok.tz_of("+7").utcoffset(None).total_seconds() == 7 * 3600
    assert tiktok.tz_of("GMT-3:30").utcoffset(None).total_seconds() == -(3 * 3600 + 1800)
    with pytest.raises(SystemExit):
        tiktok.tz_of("Asia/Ho_Chi_Minh")


def test_nhan_ngay_cua_lich():
    assert tiktok.day_label(datetime(2026, 11, 5)) == "November 5th, 2026"
    assert tiktok.day_label(datetime(2026, 11, 22)) == "November 22nd, 2026"
    assert tiktok.day_label(datetime(2026, 11, 13)) == "November 13th, 2026"
    assert tiktok.shown_date(datetime(2026, 11, 5)) == "Nov 5, 2026"


def test_doc_lai_cai_dat_truoc_khi_bam():
    w = datetime(2026, 11, 5, 19, 45, tzinfo=TZ7)
    page = "When to post\nNow\nSchedule\nNov 5, 2026\n19:45\n(GMT+7) Local Time\nWho can see this post\nEveryone\n"
    assert tiktok.settings_ok(page, w, "Everyone", "GMT+7") == []
    assert tiktok.settings_ok(page.replace("19:45", "12:45"), w, "Everyone", "GMT+7")
    assert tiktok.settings_ok(page.replace("GMT+7", "GMT+9"), w, "Everyone", "GMT+7")
    assert tiktok.settings_ok(page, w, "Only you", "GMT+7")


def test_so_caption_bo_qua_khoang_trang():
    assert tiktok.same_caption("Câu hỏi?\n\nGiải thích #phatgiao", "Câu hỏi? Giải thích #phatgiao")
    assert not tiktok.same_caption("Câu hỏi?", "Câu hỏi? #phatgiao")


def test_tim_o_ngay_gio_theo_toa_do():
    # đo thật 28/10/2026: radio Now x=133, Schedule y=434; ô múi giờ combobox x=517 y=462 cao 36
    ui = {"fields": [{"role": "radio", "text": "Now", "bounds": {"x": 133, "y": 434, "width": 16, "height": 16}},
                     {"role": "radio", "text": "Schedule", "bounds": {"x": 210, "y": 434, "width": 16, "height": 16}}],
          "buttons": [{"role": "combobox", "bounds": {"x": 517, "y": 462, "width": 220, "height": 36}},
                      {"role": "combobox", "bounds": {"x": 133, "y": 900, "width": 280, "height": 36}}]}
    (dx, dy), (tx, ty) = tiktok.schedule_points(ui)
    assert 200 < dx < 245 and 390 < tx < 435 and dy == ty == 480
    with pytest.raises(SystemExit):
        tiktok.schedule_points({"fields": [], "buttons": []})
