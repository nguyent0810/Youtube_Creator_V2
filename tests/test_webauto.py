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


# ---- đăng nhập: chờ chủ máy tự đăng nhập, không bao giờ tự nhập mật khẩu -----------------------------------

def test_auth_da_dang_nhap_thi_di_tiep():
    import asyncio
    from webauto import auth
    said = []
    asyncio.run(auth.ensure(lambda: _async(True), "Site", "https://x", wait_s=5, say=said.append))
    assert said == []


async def _async(v):
    return v


def test_auth_cho_den_khi_dang_nhap_roi_tiep_tuc():
    import asyncio
    from webauto import auth
    calls, said = [], []

    async def check():
        calls.append(1)
        return len(calls) >= 3  # lần 1 chưa, lần 2 chưa, lần 3 đã đăng nhập

    asyncio.run(auth.ensure(check, "Site", "https://x", wait_s=5, poll=0, say=said.append))
    assert len(calls) == 3
    assert "not signed in" in said[0] and "continuing" in said[-1]


def test_auth_wait_0_bao_loi_ngay_va_noi_ro_khong_tu_nhap_mat_khau():
    import asyncio
    from webauto import auth
    with pytest.raises(auth.LoginRequired) as e:
        asyncio.run(auth.ensure(lambda: _async(False), "ChatGPT", "https://chatgpt.com/", wait_s=0))
    msg = str(e.value)
    assert "ChatGPT" in msg and "https://chatgpt.com/" in msg and "never enters passwords" in msg
    assert isinstance(e.value, SystemExit)  # thoát gọn với thông báo, không in traceback


def test_auth_het_gio_cho_thi_bao_loi():
    import asyncio
    from webauto import auth
    with pytest.raises(auth.LoginRequired) as e:
        asyncio.run(auth.ensure(lambda: _async(False), "Muse", "https://muse.ai/", wait_s=0.05, poll=0.01, say=lambda m: None))
    assert "waited" in str(e.value)


def test_auth_sync_cho_playwright():
    from webauto import auth
    n = []

    def check():
        n.append(1)
        return len(n) >= 2

    auth.ensure_sync(check, "Flow", "https://flow.google.com/", wait_s=5, poll=0, say=lambda m: None)
    assert len(n) == 2
    with pytest.raises(auth.LoginRequired):
        auth.ensure_sync(lambda: False, "Flow", "https://flow.google.com/", wait_s=0)


def test_auth_nhan_biet_chua_dang_nhap():
    from webauto import auth
    assert auth.chatgpt_signed_out("ChatGPT Log in Sign up for free Ask ChatGPT")
    assert auth.chatgpt_signed_out("Just a moment... Verify you are human")  # Cloudflare: chủ máy tự xử lý
    assert not auth.chatgpt_signed_out("New chat Library Recents Create Coffee Image Plus")
    assert auth.url_is_login("https://accounts.google.com/v3/signin/identifier")
    assert auth.url_is_login("https://www.tiktok.com/login?redirect=x")
    assert not auth.url_is_login("https://studio.youtube.com/channel/UCabc")


def test_cli_wait_login_toan_cuc(monkeypatch):
    from webauto import auth
    p = cli.build_parser()
    assert p.parse_args(["tiktok", "list"]).wait_login == auth.WAIT_LOGIN
    assert p.parse_args(["--wait-login", "30", "tiktok", "list"]).wait_login == 30
    seen = {}
    monkeypatch.setattr(auth, "configure", lambda s: seen.setdefault("w", s))
    monkeypatch.setattr("webauto.tiktok.list_posts", lambda a: None)
    monkeypatch.setattr("webauto.tiktok.run", lambda coro: None)
    cli.main(["--wait-login", "7", "tiktok", "list"])
    assert seen["w"] == 7
