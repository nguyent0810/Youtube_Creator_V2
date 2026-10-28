"""Muse AI (muse.ai): ask a list of research questions and save every answer in one markdown file.

Uses the user's signed-in Chrome through Browsentic. Questions go into ONE new side chat (Chats
panel > "+" next to "Side chats") so they do not mix with the owner's main chat and each answer can
build on the previous one.

How an answer is read: the chat list only renders bubbles near the viewport, so on a long answer the
question drops out of the page text and text parsing fails. Instead, once the conversation has been
quiet for a while, open the newest bubble's "..." menu, click Copy and read the Windows clipboard.
"""
import asyncio
import time
from pathlib import Path

from .browsentic import browser, clear_clipboard, clipboard, run
from .common import UNVERIFIED_NOTE, parse_blocks, write_md

URL = "https://muse.ai/"
COMPOSER = ["textarea"]
SEND = ["body > div:nth-of-type(2) > div > div > div > div > div:nth-of-type(1) > div > div:nth-of-type(3) > div > div > div:nth-of-type(3) > div > div > div:nth-of-type(3) > div > div > span > button",
        "button[aria-label*='Send']"]
NEW_SIDE_CHAT = "nav section > div:nth-of-type(1) > span > button"
MORE = "#hatch-chat-scroll button[aria-label='More options']"


async def copy_last_bubble(b):
    info = await b.call("page_getPageInfo", maxPerKind=300)
    n = sum(1 for x in info.get("interactive", {}).get("buttons", []) if x.get("text") == "More options")
    if not n:
        return ""
    clear_clipboard()  # so a failed copy cannot return the previous clipboard content
    await b.call("page_clickElement", target={"selector": MORE, "nth": n - 1})
    await asyncio.sleep(1)
    await b.call("page_trustedClick", target={"role": "menuitem", "text": "Copy"})
    await asyncio.sleep(1)
    return clipboard()


async def ask(b, question, wait_s, poll=10, stable=9, min_chars=1500, send=True):
    if send:
        await b.first("page_fillInput", COMPOSER, value=question)
        await asyncio.sleep(1.5)
        await b.first("page_trustedClick", SEND)
    deadline, last, same = time.time() + wait_s, None, 0
    while time.time() < deadline:
        await asyncio.sleep(poll)
        sig = hash(await b.text())
        same = same + 1 if sig == last else 0
        last = sig
        if same >= stable:  # quiet for ~stable*poll seconds
            # the newest bubble may still be Muse's short "I'm checking..." note: accept only a long one
            text = await copy_last_bubble(b)
            if len(text) >= min_chars:
                return text
            same = 0
    raise TimeoutError("Muse did not finish replying in time")


async def research(questions, wait_s=900, adopt_first=False, min_chars=1500):
    """Return one answer per question. `adopt_first` reuses the Muse tab/side chat already open and
    only reads the answer to question 1 (already sent by hand), then sends the rest."""
    answers = []
    async with browser() as b:
        tab_id = None
        if not adopt_first:
            tab_id = (await b.call("page_openTab", url=URL)).get("tabId")
        try:
            if not adopt_first:
                await asyncio.sleep(6)
                await b.call("page_clickElement", target={"text": "Chats"})
                await asyncio.sleep(3)
                await b.call("page_clickElement", target={"selector": NEW_SIDE_CHAT})
                await b.call("page_waitForElement", target={"text": "New side chat"})
                await asyncio.sleep(3)
            for i, q in enumerate(questions, 1):
                print(f"[{i}/{len(questions)}] asking...", flush=True)
                answers.append(await ask(b, q, wait_s, min_chars=min_chars, send=not (adopt_first and i == 1)))
                print(f"[{i}/{len(questions)}] got {len(answers[-1])} chars", flush=True)
        finally:
            if tab_id:
                try:
                    await b.call("page_closeTab", tabId=tab_id)
                except Exception:
                    pass
    return answers


def add_parser(sub):
    ap = sub.add_parser("muse", help="Muse AI (muse.ai): research questions -> one markdown file")
    s = ap.add_subparsers(dest="cmd", required=True)
    r = s.add_parser("research")
    r.add_argument("--questions", required=True, help="blocks separated by a blank line, '#' comments")
    r.add_argument("--out", required=True, help="markdown file for agents to read")
    r.add_argument("--title", default="Research từ Muse AI")
    r.add_argument("--wait", type=int, default=900, help="max seconds per answer")
    r.add_argument("--min-chars", type=int, default=1500, help="shorter newest bubbles are treated as 'still working'")
    r.add_argument("--adopt-first", action="store_true",
                   help="use the Muse tab/side chat already open; question 1 was already sent, only read its answer")
    r.set_defaults(func=_run_research)


def _run_research(a):
    qs = parse_blocks(a.questions)
    answers = run(research(qs, a.wait, a.adopt_first, a.min_chars))
    body = "\n".join(f"## Câu hỏi {i}\n\n> {q}\n\n### Trả lời của Muse\n\n{ans}\n" for i, (q, ans) in enumerate(zip(qs, answers), 1))
    write_md(Path(a.out), a.title, {"Nguồn": "Muse AI (muse.ai), hỏi qua side chat riêng"},
             UNVERIFIED_NOTE + " Số sub, lượt xem, tần suất đăng và tên kênh có thể sai hoặc lỗi thời.", body)
    print(f"saved {a.out}")
