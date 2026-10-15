"""Dựng lại THẾ CỜ THẬT từ biên bản ván đấu (SGF) của trận AlphaGo – Lee Sedol, 03/2016.

Biên bản: sgf/g1.sgf … g5.sgf, tải 13/10/2026 từ kho của Andries Brouwer (homepages.cwi.nl/~aeb/go/games/games/AlphaGo/LeeSedol/).
Đã đối chiếu: số nước 186 / 211 / 176 / 180 / 280 khớp tường thuật; ván 2 nước 37 = "oj" (P10, đường thứ năm); ván 4 nước 78 = "ki" (L11).

    position(game, upto)  -> danh sách [x, y, "B"|"W"] các quân CÒN trên bàn sau `upto` nước, theo thứ tự đặt (x: cột từ trái, y: hàng từ trên, 0..18)
    move(game, n)         -> [x, y, màu] của nước thứ n (đếm từ 1)
"""
import re
from pathlib import Path

D = Path(__file__).resolve().parent / "sgf"
N = 19


def moves(game: int) -> list[tuple[str, int, int]]:
    s = (D / f"g{game}.sgf").read_text(encoding="utf-8", errors="replace")
    out = []
    for c, xy in re.findall(r";([BW])\[([a-s]{2})?\]", s):
        if xy:                                   # nước bỏ lượt (rỗng) không có trong 5 ván này
            out.append((c, ord(xy[0]) - 97, ord(xy[1]) - 97))
    return out


def _group(board, x, y):
    c, seen, libs, todo = board[(x, y)], {(x, y)}, set(), [(x, y)]
    while todo:
        a, b = todo.pop()
        for p in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
            if not (0 <= p[0] < N and 0 <= p[1] < N):
                continue
            if p not in board:
                libs.add(p)
            elif board[p] == c and p not in seen:
                seen.add(p)
                todo.append(p)
    return seen, libs


def position(game: int, upto: int) -> list[list]:
    board, order = {}, {}
    for k, (c, x, y) in enumerate(moves(game)[:upto], 1):
        board[(x, y)] = c
        order[(x, y)] = k
        for p in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):      # bắt quân đối phương hết khí
            if p in board and board[p] != c:
                grp, libs = _group(board, *p)
                if not libs:
                    for q in grp:
                        del board[q]
                        del order[q]
    return [[x, y, board[(x, y)]] for (x, y), _ in sorted(order.items(), key=lambda kv: kv[1])]


def move(game: int, n: int) -> list:
    c, x, y = moves(game)[n - 1]
    return [x, y, c]


if __name__ == "__main__":
    for g, n in ((1, 186), (2, 211), (3, 176), (4, 180), (5, 280)):
        assert len(moves(g)) == n, (g, len(moves(g)))
    assert move(2, 37) == [14, 9, "B"] and move(4, 78) == [10, 8, "W"]
    print("ok", {g: len(position(g, 999)) for g in range(1, 6)})
