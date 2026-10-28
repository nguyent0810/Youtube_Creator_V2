"""chatgpt.com through the user's real Chrome (Browsentic): render images, or ask / review and save the reply.

Not Playwright: chatgpt.com puts a Cloudflare "verify you are human" check in front of automated
Chrome that returns after every solve. Do not try to get around it; use the real, signed-in Chrome.

Needs Browsentic guardrail `file-download` = Allow for `images` (the image is saved through the
page's own Download button).
"""
import asyncio
import shutil
import time
from pathlib import Path

from . import auth
from .browsentic import browser, newest_download, run
from .common import UNVERIFIED_NOTE, default_out, parse_prompts, write_md

URL = "https://chatgpt.com/"
COMPOSER = ["#prompt-textarea", "div[contenteditable=true]", "textarea"]
SEND = ["button[data-testid=send-button]", "button[aria-label*='Send']"]
IMAGE = "img[alt*='Generated image']"
DOWNLOAD = "button[aria-label*='ownload']"
MARK = "ChatGPT said:"  # heading before each assistant message in the rendered text
FOOTER = ("ChatGPT can make mistakes", "Latest response")
REVIEW_INSTRUCTION = (
    "Hãy review tài liệu dưới đây như một người phản biện độc lập. Trả lời bằng tiếng Việt, Markdown, "
    "ngắn gọn: (1) nhận định chung 2-3 câu; (2) các khuyến nghị cụ thể, đánh số, sắp theo mức ưu tiên, "
    "mỗi khuyến nghị nêu lý do và cách làm; (3) điểm còn thiếu hoặc rủi ro chưa được nhắc tới. "
    "Chỉ dựa vào nội dung tài liệu, đừng bịa thêm dữ kiện."
)


async def ensure_login(b):
    """Logged-out chatgpt.com (or a Cloudflare human check) -> wait for the owner; never type credentials."""
    await asyncio.sleep(3)

    async def ok():
        try:
            return not auth.chatgpt_signed_out(await b.text(target={"selector": "body"}))
        except RuntimeError:
            return False

    await auth.ensure(ok, "ChatGPT", URL)


async def _send(b, text):
    await b.call("page_waitForElement", target={"selector": ",".join(COMPOSER)})
    await b.first("page_fillInput", COMPOSER, value=text)
    await asyncio.sleep(1.5)
    await b.first("page_trustedClick", SEND)  # clicking works; pressing Enter is treated as a form submit and refused


async def render_image(b, prompt, dest, wait_s):
    tab = await b.call("page_openTab", url=URL)
    try:
        await ensure_login(b)
        await _send(b, f"Create an image: {prompt}")
        deadline = time.time() + wait_s
        while True:
            try:
                await b.call("page_waitForElement", target={"selector": IMAGE})
                break
            except RuntimeError:
                if time.time() > deadline:
                    raise TimeoutError("no image appeared")
        await asyncio.sleep(4)  # let the render finish loading
        await b.call("page_clickElement", target={"selector": IMAGE})  # opens the viewer with a download button
        await asyncio.sleep(2)
        t0 = time.time() - 2
        await b.call("page_captureDownload", target={"selector": DOWNLOAD})
        got = newest_download(t0)
        if not got:
            raise RuntimeError("download not found in Browsentic's download folder")
        shutil.copyfile(got, dest)
        return dest
    finally:
        if tab.get("tabId"):
            try:
                await b.call("page_closeTab", tabId=tab["tabId"])
            except Exception:
                pass


async def images(prompts, out, wait_s=240, gap=5):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    saved = []
    async with browser() as b:
        for i, (stem, prompt) in enumerate(prompts, 1):
            dest = out / f"{stem}.png"
            if dest.exists():
                print(f"[{i}/{len(prompts)}] skip (exists) {dest.name}")
                continue
            try:
                await render_image(b, prompt, dest, wait_s)
                saved.append(dest)
                print(f"[{i}/{len(prompts)}] saved {dest}")
            except Exception as e:
                print(f"[{i}/{len(prompts)}] FAILED {stem}: {e}")
            await asyncio.sleep(gap)
    return saved


def build_review_prompt(instruction, name, body):
    return f"{instruction}\n\nTài liệu: {name}\n\n```markdown\n{body}\n```"


def last_reply(full):
    """Text of the newest assistant message in the rendered chat text, without the page footer."""
    if MARK not in full:
        return ""
    reply = full.rsplit(MARK, 1)[1]
    for tail in FOOTER:
        reply = reply.split(tail, 1)[0]
    return reply.strip()


async def ask(text, wait_s=420, poll=6, stable=4, from_chat=None):
    """Send `text` in a new chat and return (reply, chat_url). `from_chat` reads an existing chat instead."""
    async with browser() as b:
        tab = await b.call("page_openTab", url=from_chat or URL)
        try:
            await ensure_login(b)
            if not from_chat:
                await _send(b, text)
            deadline, last, same = time.time() + wait_s, None, 0
            while time.time() < deadline:
                await asyncio.sleep(poll)
                try:
                    cur = last_reply(await b.text(target={"selector": "main"}))
                except RuntimeError:
                    continue
                same = same + 1 if (cur and cur == last) else 0  # done = non-empty and unchanged `stable` polls
                last = cur
                if same >= stable:
                    info = await b.call("page_getPageInfo", maxPerKind=1)
                    return last, info.get("document", {}).get("url", "")
            raise TimeoutError("ChatGPT reply did not finish in time")
        finally:
            if tab.get("tabId"):
                try:
                    await b.call("page_closeTab", tabId=tab["tabId"])
                except Exception:
                    pass


def add_parser(sub):
    ap = sub.add_parser("chatgpt", help="chatgpt.com via real Chrome: images, ask/review")
    s = ap.add_subparsers(dest="cmd", required=True)
    i = s.add_parser("images", help="render one image per prompt and save <stem>.png")
    i.add_argument("--prompts-file", required=True, help="'name | prompt' per line, '#' comments")
    i.add_argument("--out", default=str(default_out("chatgpt")))
    i.add_argument("--wait", type=int, default=240, help="seconds per image")
    i.add_argument("--gap", type=int, default=5, help="seconds between prompts")
    i.add_argument("--limit", type=int)
    i.set_defaults(func=lambda a: run(images(parse_prompts(a.prompts_file)[: a.limit], a.out, a.wait, a.gap)))

    k = s.add_parser("ask", help="send a prompt or review a file, save the reply as markdown for agents")
    src = k.add_mutually_exclusive_group(required=True)
    src.add_argument("--prompt")
    src.add_argument("--file", help="file to review (text/markdown); sent with --instruction")
    k.add_argument("--instruction", default=REVIEW_INSTRUCTION)
    k.add_argument("--out", help="default: <file>.chatgpt-review.md, or output/webauto/chatgpt/reply.md")
    k.add_argument("--wait", type=int, default=420)
    k.add_argument("--from-chat", help="URL of an existing chat: read its reply, send nothing")
    k.set_defaults(func=_run_ask)


def _run_ask(a):
    if a.file:
        src = Path(a.file)
        text = build_review_prompt(a.instruction, src.name, src.read_text(encoding="utf-8"))
        out = Path(a.out) if a.out else src.with_name(src.stem + ".chatgpt-review.md")
        title, origin = f"Review của ChatGPT cho `{src.name}`", src.as_posix()
    else:
        text, title, origin = a.prompt, "Trả lời của ChatGPT", "(prompt trực tiếp)"
        out = Path(a.out) if a.out else default_out("chatgpt") / "reply.md"
    reply, url = run(ask(text, a.wait, from_chat=a.from_chat))
    write_md(out, title, {"Nguồn được hỏi": f"`{origin}`", "Cuộc trò chuyện": url}, UNVERIFIED_NOTE, reply)
    print(f"saved {out} ({len(reply)} chars)")
