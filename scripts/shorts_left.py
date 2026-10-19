"""In số Short đã dựng (stage 'assembled') còn chờ đăng của một kênh -- cho vòng lặp trong chuỗi đăng.

    python scripts/shorts_left.py MIM
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from factory.console import utf8_console  # noqa: E402
utf8_console()
c = sqlite3.connect(Path(__file__).resolve().parent.parent / "state.sqlite")
print(c.execute("SELECT COUNT(*) FROM item WHERE channel=? AND stage='assembled' AND kind!='long' AND slug NOT LIKE 'long-%'",
                (sys.argv[1],)).fetchone()[0])
