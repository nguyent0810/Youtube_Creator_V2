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
      mkdir output/stier/$s/LOCK 2>/dev/null || continue
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
