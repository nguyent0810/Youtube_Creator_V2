@echo off
rem Run by Task Scheduler "YT-CL-Monitor" daily 08:00 (approved by user 2026-10-04).
cd /d C:\Tools\Youtuber\yt-factory
set PYTHONIOENCODING=utf-8
rem Create the log folder before redirecting output into it (only monitor.py creates it).
if not exist output\analysis\monitor mkdir output\analysis\monitor
"C:\Users\Admin\AppData\Local\Programs\Python\Python311\python.exe" motion\stier\monitor.py --quiet >> output\analysis\monitor\task.log 2>&1
