"""Giao một ticket `tk` cho agent CLI trên máy (Codex, agy, Grok), thử lần lượt, báo về cho Claude điều phối (28/10/2026).

    python scripts/agent_ticket.py <ticket-id> --brief docs/pm/tickets/<id>-<agent>.md --expect <file báo cáo>
                                   [--agents codex,agy,grok] [--effort high] [--timeout 5400]

Luồng:
1. Thử từng agent theo `--agents`. Mỗi lần chạy ghi log `docs/pm/tickets/<id>-<agent>.log`.
2. Một lần chạy là HỎNG khi: hết quota hoặc bị giới hạn tốc độ, thoát lỗi, quá thời gian, hay chạy xong mà không có file `--expect`.
   Hỏng thì ghi chú lý do vào ticket rồi thử agent kế tiếp.
3. Agent nào xong thì ghi chú "xong, chờ Claude review" vào ticket, thoát 0.
4. Cả danh sách đều hỏng thì ghi cờ `docs/pm/tickets/<id>.FALLBACK_CLAUDE`, thoát 3. Từ đó Claude giao cho subagent của mình.

Không agent nào được thấy `YT_CREDS_DIR`. Agent không được đăng, commit hay đổi lịch: brief phải ghi rõ, và Claude review trước mọi việc ra ngoài.
Codex có chụp nhanh và rollback riêng cho Long trong `scripts/codex_ticket.py`; script này dành cho ticket chung.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TICKETS = ROOT / "docs" / "pm" / "tickets"

# Chỉ bắt dòng lỗi thật, không bắt "429" trong id clip (bài học codex_ticket 26/10).
FAIL = re.compile(
    r"^(ERROR|Error|error|jetski)\b.*(usage limit|rate limit|quota|too many requests|hit your (usage )?limit|"
    r"insufficient_quota|exceeded your|out of credits|credit balance|\b429\b|no output produced|"
    r"not logged in|unauthori[sz]ed|permission)", re.I | re.M)


def command(agent: str, prompt: str, effort: str, last: Path) -> list[str]:
    exe = shutil.which(agent) or agent
    if agent == "codex":
        return [exe, "exec", "-s", "workspace-write", "-C", str(ROOT), "-c", "sandbox_workspace_write.network_access=true",
                "-c", f'model_reasoning_effort="{effort}"', "-o", str(last), prompt]
    if agent == "agy":  # headless agy không hỏi được quyền chạy lệnh -> tự duyệt (chủ kênh cho phép 28/10), terminal trong sandbox
        return [exe, "-p", prompt, "--sandbox", "--dangerously-skip-permissions",
                "--effort", effort if effort in ("low", "medium", "high") else "high", "--print-timeout", "90m"]
    if agent == "grok":
        return [exe, "-p", prompt, "--cwd", str(ROOT), "--always-approve"]  # headless tự duyệt (chủ kênh cho phép 28/10)
    raise SystemExit(f"agent lạ: {agent}")


def failed(code: int, out: str, expect: Path, started: float) -> str | None:
    """Lý do hỏng, hoặc None khi lần chạy được tính là xong."""
    m = FAIL.search(out)
    if m:
        return m.group(0).strip()[:160]
    if code != 0:
        return f"thoát mã {code}"
    if not expect.exists() or expect.stat().st_mtime < started:
        return f"không có {expect.relative_to(ROOT).as_posix()} mới"
    return None


def note(ticket: str, text: str) -> None:
    tk = ROOT / "tools" / "ticket" / "tk"
    bash = shutil.which("bash") if os.name != "nt" else str(Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Git" / "bin" / "bash.exe")
    try:
        subprocess.run([bash, str(tk), "add-note", ticket, text], cwd=ROOT, capture_output=True, timeout=30,
                       env={**os.environ, "TICKETS_DIR": (ROOT / ".tickets").as_posix()})
    except (OSError, subprocess.SubprocessError):
        print("không ghi được note vào ticket:", text)


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from factory.console import utf8_console
    utf8_console()  # console Windows cp1252 không in được tiếng Việt
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ticket")
    ap.add_argument("--brief", required=True)
    ap.add_argument("--expect", required=True, help="file báo cáo agent phải ghi; thiếu = hỏng")
    ap.add_argument("--agents", default="codex,agy,grok")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--timeout", type=int, default=5400)
    a = ap.parse_args()
    brief, expect = ROOT / a.brief, ROOT / a.expect
    if not brief.exists():
        raise SystemExit(f"thiếu brief {brief}")
    prompt = (f"Làm ticket {a.ticket} theo brief {a.brief} (thư mục hiện tại là repo). Đọc brief trước, làm đúng phạm vi, "
              f"không đăng, không commit, không đổi lịch. Kết thúc bằng việc ghi {a.expect}.")
    env = {k: v for k, v in os.environ.items() if k != "YT_CREDS_DIR"}
    env["PYTHONIOENCODING"] = "utf-8"
    for agent in [x.strip() for x in a.agents.split(",") if x.strip()]:
        log = TICKETS / f"{a.ticket}-{agent}.log"
        started = time.time()
        print(f"[{a.ticket}] {agent} ...", flush=True)
        try:
            with open(log, "w", encoding="utf-8") as fh:
                r = subprocess.run(command(agent, prompt, a.effort, TICKETS / f"{a.ticket}-{agent}.last.txt"), cwd=ROOT,
                                   stdout=fh, stderr=subprocess.STDOUT, env=env, timeout=a.timeout)
            code = r.returncode
        except subprocess.TimeoutExpired:
            code = -1
        except OSError as e:
            log.write_text(f"không chạy được {agent}: {e}\n", encoding="utf-8")
            code = -2
        out = log.read_text(encoding="utf-8", errors="replace")
        why = "quá thời gian" if code == -1 else failed(code, out[-20000:], expect, started)
        if why is None:
            note(a.ticket, f"{agent} xong ({int(time.time() - started)} s), báo cáo {a.expect}. Chờ Claude review.")
            print(f"[{a.ticket}] {agent} xong -> {a.expect}")
            return 0
        note(a.ticket, f"{agent} hỏng: {why}. Log {log.relative_to(ROOT).as_posix()}.")
        print(f"[{a.ticket}] {agent} hỏng: {why}", flush=True)
    flag = TICKETS / f"{a.ticket}.FALLBACK_CLAUDE"
    flag.write_text(f"{time.strftime('%Y-%m-%d %H:%M')} mọi agent ({a.agents}) đều hỏng; Claude giao subagent.\n", encoding="utf-8")
    note(a.ticket, "Mọi agent CLI hỏng: chuyển cho subagent của Claude.")
    print(f"[{a.ticket}] mọi agent hỏng -> {flag.relative_to(ROOT).as_posix()}")
    return 3


if __name__ == "__main__":
    sys.exit(main())
