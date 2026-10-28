"""scripts/agent_ticket.py: nhận biết lần chạy agent hỏng (hết quota, thoát lỗi, thiếu báo cáo) để chuyển agent kế tiếp."""
import importlib.util
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("agent_ticket", ROOT / "scripts" / "agent_ticket.py")
at = importlib.util.module_from_spec(spec)
spec.loader.exec_module(at)


def report(tmp_path, age=0):
    p = tmp_path / "r.md"
    p.write_text("ok", encoding="utf-8")
    if age:
        t = time.time() - age
        os.utime(p, (t, t))
    return p


def test_xong_khi_co_bao_cao_moi(tmp_path, monkeypatch):
    monkeypatch.setattr(at, "ROOT", tmp_path)
    started = time.time() - 5
    assert at.failed(0, "đã ghi báo cáo", report(tmp_path), started) is None


def test_het_quota_codex_va_agy(tmp_path, monkeypatch):
    monkeypatch.setattr(at, "ROOT", tmp_path)
    r = report(tmp_path)
    assert "usage limit" in at.failed(0, "ERROR: You've hit your usage limit. Try again later.", r, 0)
    assert "no output produced" in at.failed(0, "jetski: no output produced — a tool required the \"command\" permission", r, 0)


def test_khong_bat_nham_429_trong_id_clip(tmp_path, monkeypatch):
    monkeypatch.setattr(at, "ROOT", tmp_path)
    assert at.failed(0, "dùng clip pexels:7490429 cho cảnh 3", report(tmp_path), 0) is None


def test_thoat_loi_hoac_thieu_bao_cao(tmp_path, monkeypatch):
    monkeypatch.setattr(at, "ROOT", tmp_path)
    assert at.failed(1, "", report(tmp_path), 0) == "thoát mã 1"
    old = report(tmp_path, age=3600)
    assert "không có" in at.failed(0, "xong", old, time.time() - 10)  # báo cáo cũ từ lần trước không tính
    assert "không có" in at.failed(0, "xong", tmp_path / "missing.md", 0)


def test_lenh_tung_agent_khong_lo_credential(monkeypatch):
    monkeypatch.setenv("YT_CREDS_DIR", "x")
    for agent in ("codex", "agy", "grok"):
        cmd = at.command(agent, "làm ticket", "high", Path("last.txt"))
        assert "làm ticket" in cmd and not any("YT_CREDS" in c for c in cmd)
    assert "workspace-write" in at.command("codex", "p", "high", Path("l"))
