"""Giao một ticket cho Codex, có chụp nhanh trước khi chạy và rollback khi Codex hết quota hoặc chết giữa chừng (26/10/2026).

    python scripts/codex_ticket.py <ticket.md> <topic> [--resume] [--effort high] [--min-syl 1900]
    python scripts/codex_ticket.py --restore <topic> <snapshot_dir>      # khôi phục tay

Luồng:
1. Chụp nhanh `data/long/<topic>/` và `motion/long/thumbs/<topic>_t*.html` vào `output/codex_snapshots/<topic>/<giờ>/`.
2. Chạy `codex --search exec`. Sandbox workspace-write, có mạng, reasoning effort theo `--effort`. Với `--resume`, dùng `exec resume --last` để giữ ngữ cảnh vòng trước.
3. Nếu Codex hết quota, bị giới hạn tốc độ, hoặc thoát lỗi:
   - chép phần Codex làm dở sang `<snapshot>_partial/` để tham khảo;
   - khôi phục thư mục topic về bản chụp nhanh;
   - ghi cờ `CODEX_FALLBACK` cạnh ticket;
   - thoát mã 3. Từ đó Claude làm chính.
4. Nếu Codex chạy xong thì chạy `scripts/long_gate.py`. Đạt thì thoát 0, trượt thì thoát 2 (giao lại kèm lỗi của cổng).
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
# Chỉ dòng ERROR thật của Codex ("ERROR: You've hit your usage limit…"). 26/10/2026: regex cũ khớp "429" trong id clip
# Pexels 7490429 ở báo cáo -> rollback nhầm cả một vòng đã xong (mã thoát 0).
QUOTA = re.compile(r"^ERROR:.*(usage limit|rate limit|quota|too many requests|hit your (usage )?limit|insufficient_quota|"
                   r"exceeded your|\b429\b)", re.I | re.M)


def topic_paths(topic: str) -> list[Path]:
    return [ROOT / "data" / "long" / topic] + sorted((ROOT / "motion" / "long" / "thumbs").glob(f"{topic}_t*.html"))


def snapshot(topic: str) -> Path:
    snap = ROOT / "output" / "codex_snapshots" / topic / time.strftime("%Y%m%d-%H%M%S")
    snap.mkdir(parents=True)
    for p in topic_paths(topic):
        if p.is_dir():
            shutil.copytree(p, snap / "data" / p.name)
        elif p.exists():
            (snap / "thumbs").mkdir(exist_ok=True)
            shutil.copy2(p, snap / "thumbs" / p.name)
    return snap


def restore(topic: str, snap: Path) -> None:
    for p in topic_paths(topic):                     # phần Codex làm dở: giữ để tham khảo rồi gỡ
        part = snap.with_name(snap.name + "_partial")
        if p.is_dir():
            shutil.copytree(p, part / "data" / p.name, dirs_exist_ok=True)
            shutil.rmtree(p)
        elif p.exists():
            (part / "thumbs").mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, part / "thumbs" / p.name)
            p.unlink()
    if (snap / "data" / topic).exists():
        shutil.copytree(snap / "data" / topic, ROOT / "data" / "long" / topic)
    for f in (snap / "thumbs").glob("*.html") if (snap / "thumbs").exists() else []:
        shutil.copy2(f, ROOT / "motion" / "long" / "thumbs" / f.name)


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from factory.console import utf8_console
    utf8_console()
    ap = argparse.ArgumentParser()
    ap.add_argument("ticket", nargs="?")
    ap.add_argument("topic", nargs="?")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--search", action="store_true", help="bật web search (chỉ cho ticket nghiên cứu)")
    ap.add_argument("--min-syl", type=int, default=1900)
    ap.add_argument("--restore", nargs=2, metavar=("TOPIC", "SNAPSHOT"))
    a = ap.parse_args()
    if a.restore:
        restore(a.restore[0], Path(a.restore[1]))
        print(f"đã khôi phục {a.restore[0]} từ {a.restore[1]}")
        return 0
    ticket = Path(a.ticket)
    tdir = ticket.parent
    stem = ticket.stem.split("-")[0]
    log = tdir / f"codex_run_{stem}.log"
    snap = snapshot(a.topic)
    print(f"chụp nhanh: {snap}", flush=True)
    prompt = (f"Làm ticket {ticket.as_posix()} từ đầu đến cuối. Tuân thủ AGENTS.md (đã nạp sẵn), nhất là 'Cấm tuyệt đối' "
              f"và 'chỉ đọc đúng các file ticket chỉ định, không khám phá repo'. "
              f"Trước khi báo xong phải chạy `python scripts/long_gate.py {a.topic} --min-syl {a.min_syl}` và nó phải in ĐẠT "
              f"(trừ khi ticket nói là ticket nghiên cứu). Viết báo cáo vào file kết quả mà ticket chỉ định. Tiếng Việt.")
    exe = shutil.which("codex") or "codex"
    cmd = [exe] + (["--search"] if a.search else []) + ["exec"]
    if a.resume:                                     # `exec resume` không nhận -s/-C: đặt sandbox bằng -c, thư mục bằng cwd
        cmd += ["resume", "--last", "-c", 'sandbox_mode="workspace-write"']
    else:
        cmd += ["-s", "workspace-write", "-C", str(ROOT)]
    cmd += ["-c", "sandbox_workspace_write.network_access=true", "-c", f'model_reasoning_effort="{a.effort}"',
            "-o", str(tdir / f"codex_last_{stem}.txt"), prompt]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    env.pop("YT_CREDS_DIR", None)                    # Codex không bao giờ thấy credential YouTube
    with open(log, "w", encoding="utf-8") as fh:
        r = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, env=env, cwd=ROOT)
    full = log.read_text(encoding="utf-8", errors="replace")
    tail = full[-6000:]
    m = re.findall(r"tokens used\s*\n\s*([\d,\.]+)", full)
    tokens = m[-1].replace(",", "").replace(".", "") if m else "?"
    with open(ROOT / "docs" / "pm" / "tickets" / "codex_tokens.csv", "a", encoding="utf-8") as fh:   # đo token từng vòng
        fh.write(f"{time.strftime('%Y-%m-%d %H:%M')},{ticket.name},{a.topic},{a.effort},{int(a.search)},"
                 f"{int(a.resume)},{r.returncode},{tokens}\n")
    print(f"token Codex: {tokens}", flush=True)
    if r.returncode != 0 or QUOTA.search(tail):
        restore(a.topic, snap)
        flag = tdir / "CODEX_FALLBACK"
        flag.write_text(f"{time.strftime('%d/%m/%Y %H:%M')} Codex dừng (mã {r.returncode}); "
                        f"đã rollback {a.topic} về {snap}; phần dở ở {snap.name}_partial. Claude làm chính.\n",
                        encoding="utf-8")
        print(f"CODEX DỪNG (mã {r.returncode}) -> rollback về {snap}, Claude làm chính. Xem {log}")
        return 3
    g = subprocess.run([sys.executable, str(ROOT / "scripts" / "long_gate.py"), a.topic, "--min-syl", str(a.min_syl)],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    print(g.stdout.strip())
    return 0 if g.returncode == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
