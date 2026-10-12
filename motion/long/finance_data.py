"""Dữ liệu tài sản cho kênh Biểu Đồ Biết Nói (so sánh kênh đầu tư). Ghi CSV vào data/ck/ -- engine chỉ vẽ.

    python motion/long/finance_data.py sjc 2026-01-02 2026-10-06 [--monthly 2018-10 2025-12]
    python motion/long/finance_data.py btc [usd|vnd]  # 365 ngày gần nhất (CoinGecko, API công khai)

- Vàng SJC: vnstock.explorer.misc.gold_price.sjc_gold_price(date) -> trang SJC, mỗi ngày 1 lượt gọi (có từ 02/01/2016).
  Lấy giá "Vàng SJC 1L, 10L, 1KG" tại Hồ Chí Minh (mua/bán). Ghi nguồn: "Giá vàng: SJC (sjc.com.vn), qua Vnstock".
  Gọi chậm (3,4 s/lượt, dưới hạn mức vnstock) để không làm phiền trang nguồn; CSV có sẵn ngày nào thì bỏ qua ngày đó (chạy lại vô hại).
- Bitcoin: CoinGecko /coins/bitcoin/market_chart?vs_currency=vnd&days=365 (giá đóng cửa ngày). Ghi nguồn:
  "Dữ liệu Bitcoin: CoinGecko".
"""
from __future__ import annotations

import csv
import json
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "ck"
PAUSE = 3.4   # vnstock bản Cộng đồng chưa đăng ký khoá: ~20 lượt/phút; vượt là vnai tự kết thúc tiến trình


def _read(p: Path) -> dict[str, dict]:
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return {r["time"]: r for r in csv.DictReader(f)}


def _write(p: Path, rows: dict[str, dict], cols: list[str]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for k in sorted(rows):
            w.writerow({c: rows[k][c] for c in cols})


def sjc(days: list[str]) -> Path:
    from vnstock.explorer.misc.gold_price import sjc_gold_price
    p = DATA / "sjc_1d.csv"
    rows = _read(p)
    for d in days:
        if d in rows:
            continue
        time.sleep(PAUSE)                            # MỌI lượt gọi đều tính hạn mức, kể cả ngày trống
        try:
            df = sjc_gold_price(d)
        except Exception as e:                       # ngày nghỉ / trang lỗi tạm: bỏ qua, chạy lại sau
            print(d, "bỏ qua:", str(e)[:80], flush=True)
            continue
        if df is None or df.empty:
            continue
        r = df[df["name"].str.contains("SJC 1L", na=False) & (df["branch"] == "Hồ Chí Minh")]
        if r.empty:
            continue
        rows[d] = {"time": d, "buy": int(r.iloc[0]["buy_price"]), "sell": int(r.iloc[0]["sell_price"])}
        _write(p, rows, ["time", "buy", "sell"])     # lưu từng ngày: vnai DỪNG cả tiến trình khi vượt hạn mức
    _write(p, rows, ["time", "buy", "sell"])
    return p


def btc(cur: str = "usd") -> Path:
    """Giá USD là mặc định: chuỗi VND của CoinGecko có tỷ giá ngầm định đi ngược tỷ giá thật (kiểm chứng 06/10/2026)."""
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency={cur}&days=365&interval=daily"
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "bieu-do-biet-noi/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        prices = json.load(r)["prices"]
    rows = {}
    for ms, v in prices:
        d = datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
        rows[d] = {"time": d, "close": round(v, 2)}
    p = DATA / f"btc_{cur}_1d.csv"
    _write(p, rows, ["time", "close"])
    return p


def weekdays(a: str, b: str) -> list[str]:
    d0, d1 = date.fromisoformat(a), date.fromisoformat(b)
    return [(d0 + timedelta(k)).isoformat() for k in range((d1 - d0).days + 1) if (d0 + timedelta(k)).weekday() < 5]


def weekly(a: str, b: str) -> list[str]:
    """Thứ Hai mỗi tuần (làm dày chuỗi thưa để lọc ngày giả chính xác hơn -- retro D1 07/10/2026)."""
    d0, d1 = date.fromisoformat(a), date.fromisoformat(b)
    d0 = d0 + timedelta((7 - d0.weekday()) % 7)
    return [(d0 + timedelta(7 * k)).isoformat() for k in range((d1 - d0).days // 7 + 1)]


def month_starts(a: str, b: str) -> list[str]:
    """Ngày làm việc đầu tiên mỗi tháng (thử 1..5 cho tới khi có giá -- sjc() tự bỏ ngày trống)."""
    y, m = map(int, a.split("-"))
    y1, m1 = map(int, b.split("-"))
    out = []
    while (y, m) <= (y1, m1):
        out += [date(y, m, k).isoformat() for k in (1, 2, 3, 4, 5) if date(y, m, k).weekday() < 5][:2]
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


if __name__ == "__main__":
    import pathlib, sys  # noqa: E401
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    a = sys.argv[1:]
    if a[0] == "sjc":
        days = weekdays(a[1], a[2])
        if "--weekly" in a:
            i = a.index("--weekly")
            days = weekly(a[i + 1], a[i + 2]) + days
        if "--monthly" in a:
            i = a.index("--monthly")
            days = month_starts(a[i + 1], a[i + 2]) + days
        print(sjc(days))
    elif a[0] == "btc":
        print(btc(a[1] if len(a) > 1 else "usd"))
