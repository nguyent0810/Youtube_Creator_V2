#!/bin/sh
# In ra các spec chưa có final.mp4 mới hơn spec (không tính spec FAILED)
cd /c/Tools/Youtuber/yt-factory
for f in data/stier/specs/*.json; do s=$(basename "$f" .json); [ "$s" = monalisa ] && continue
  fin=output/stier/$s/final.mp4
  if [ ! -f "$fin" ] || [ "$f" -nt "$fin" ]; then
    if [ -f output/stier/$s/FAILED ] && [ ! "$f" -nt output/stier/$s/FAILED ]; then echo "FAILED $s"; else echo "$s"; fi
  fi
done
