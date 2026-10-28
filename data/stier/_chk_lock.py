from pathlib import Path
import subprocess, time
lock = Path(r"D:/Tools/Youtube Creator v2/Youtube_Creator_V2/output/.render.who")
print("lock:", lock.read_text(encoding="utf-8"))
print("lock_mtime", time.ctime(lock.stat().st_mtime))
r = subprocess.run(["tasklist", "/FI", "PID eq 22116"], capture_output=True, text=True)
print(r.stdout)
out = Path(r"D:/Tools/Youtube Creator v2/Youtube_Creator_V2/output")
items = sorted(out.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)[:30]
for p in items:
    kind = "DIR" if p.is_dir() else "FIL"
    size = p.stat().st_size if p.is_file() else 0
    print(time.ctime(p.stat().st_mtime), kind, p.name, size)
