#!/bin/sh
# Hàng đợi dựng nền, chạy SONG SONG được: mỗi spec khoá bằng mkdir (nguyên tử) trước khi dựng.
cd /c/Tools/Youtuber/yt-factory
PY=/c/Tools/Youtuber/vietneu-tts/.venv/Scripts/python.exe
W=${1:-A}
while [ ! -f output/stier/STOP2 ]; do
  did=0
  for f in data/stier/specs/*.json; do
    s=$(basename "$f" .json); [ "$s" = monalisa ] && continue
    fin=output/stier/$s/final.mp4
    if [ ! -f "$fin" ] || [ "$f" -nt "$fin" ]; then
      [ -f output/stier/$s/FAILED ] && [ ! "$f" -nt output/stier/$s/FAILED ] && continue
      mkdir -p output/stier/$s
      # LOCK bỏ lại bởi build bị giết giữa chừng (quá 3 giờ) -> gỡ, có ghi log.
      # Bản cũ: spec đó bị bỏ qua vĩnh viễn mà không một dòng log nào.
      if [ -n "$(find output/stier/$s/LOCK -maxdepth 0 -mmin +180 2>/dev/null)" ]; then
        echo "[$(date +%H:%M:%S)] $W gỡ LOCK cũ (>3h) của $s"; rmdir output/stier/$s/LOCK
      fi
      mkdir output/stier/$s/LOCK 2>/dev/null || continue
      trap 'rmdir "output/stier/$s/LOCK" 2>/dev/null; exit 1' INT TERM
      echo "[$(date +%H:%M:%S)] $W build $s"
      if PYTHONIOENCODING=utf-8 $PY motion/stier/build.py "$s" > output/stier/$s.log 2>&1; then
        echo "[$(date +%H:%M:%S)] $W OK $s"; rm -f output/stier/$s/FAILED
      else
        echo "[$(date +%H:%M:%S)] $W FAIL $s: $(tail -2 output/stier/$s.log | tr '\n' ' ')"; touch output/stier/$s/FAILED
      fi
      rmdir output/stier/$s/LOCK
      did=1
    fi
  done
  [ $did = 0 ] && sleep 30
done
