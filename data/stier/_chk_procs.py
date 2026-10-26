from pathlib import Path
import subprocess, time, json
# processes
for pat in ["python", "node", "ffmpeg", "chrome"]:
    r = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {pat}.exe"], capture_output=True, text=True)
    lines = [ln for ln in r.stdout.splitlines() if pat.lower() in ln.lower() or "Image" in ln or "===" in ln]
    print("---", pat, "---")
    print("\n".join(lines[:15]) if lines else "(none)")
stier = Path(r"D:/Tools/Youtube Creator v2/Youtube_Creator_V2/output/stier")
dirs = sorted([p for p in stier.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
print("--- recent project dirs ---")
for p in dirs[:25]:
    mp4s = list(p.glob("*.mp4")) + list(p.glob("final*.mp4")) + list((p/"final").glob("*.mp4") if (p/"final").exists() else [])
    has_final = any("final" in x.name.lower() or x.suffix==".mp4" for x in p.rglob("*.mp4") if "pexels" not in x.name and "full" not in x.name)
    finals = [x for x in p.rglob("*.mp4") if "pexels" not in x.name and ".full." not in x.name]
    print(time.ctime(p.stat().st_mtime), p.name, "finals", len(finals), [str(f.relative_to(p)) for f in finals[:3]])
# calendar rendered-v3 update
cal = json.loads(Path(r"D:/Tools/Youtube Creator v2/Youtube_Creator_V2/data/stier/tiktok_calendar_2026-11.json").read_text(encoding="utf-8"))
print("status counts", {s: sum(1 for e in cal["entries"] if e.get("status")==s) for s in set(e.get("status") for e in cal["entries"])})
print("rendered-v3", [e["n"] for e in cal["entries"] if e.get("status")=="rendered-v3"])
