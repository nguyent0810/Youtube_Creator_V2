#!/bin/sh
# Bảng khung hình kiểm tra: sheet.sh <video> <out.png> [cột] — 20 khung rải đều
F=/c/Tools/Youtuber/video-editor/vendor/ffmpeg
V="$1"; O="$2"
D=$($F/ffprobe.exe -v error -show_entries format=duration -of csv=p=0 "$V")
N=$(python -c "print(int(float('$D')*30))")
STEP=$(python -c "print(max(1,$N//20))")
$F/ffmpeg.exe -v error -y -i "$V" -vf "select='not(mod(n\,$STEP))',scale=300:533,tile=10x2:padding=4" -frames:v 1 "$O"
