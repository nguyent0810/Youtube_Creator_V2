# Grok Bot: chay build.py bo qua render lock (user da dong y render song song). Khong sua code repo.
import sys, os, runpy, contextlib, time
ROOT = r"D:\Tools\Youtube Creator v2\Youtube_Creator_V2"
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "motion", "stier"))
sys.path.insert(0, ROOT)
import factory.render_lock as rl
rl.render_lock = lambda *a, **k: contextlib.nullcontext()
slug = sys.argv[1]
print("START", slug, time.strftime("%H:%M:%S"), flush=True)
sys.argv = [os.path.join(ROOT, "motion", "stier", "build.py"), slug] + sys.argv[2:]
try:
    runpy.run_path(sys.argv[0], run_name="__main__")
    print("END", slug, "OK", time.strftime("%H:%M:%S"), flush=True)
except SystemExit as e:
    print("END", slug, "EXIT", e, time.strftime("%H:%M:%S"), flush=True)
