"""TikTok Studio: list / create / update / delete posts through the user's real Chrome (Browsentic).

This acts on a LIVE channel, so (see CLAUDE.md: never publish, schedule or delete without the owner's say):
  - create  defaults to private ("Only you"); a non-private post needs --allow-public. The caption is
            prefixed with --marker so a test post is easy to find. It never schedules.
  - delete  needs --id; refuses a post that is not "Only me" without --allow-public, and refuses unless
            exactly one loaded row matches the id. TikTok keeps deleted posts 30 days (Activity center >
            Recently deleted).
  - update  is NOT verified end to end, see `update`.

`create` hands the video to the page through Browsentic: a throwaway local http server +
page_captureDownload gives Browsentic a copy, and page_attachFile can only attach files Browsentic
already holds. Needs guardrail `file-download` (and `file-upload` if it is gated) = Allow.
"""
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

from .browsentic import browser, run

CONTENT = "https://www.tiktok.com/tiktokstudio/content"
UPLOAD = "https://www.tiktok.com/tiktokstudio/upload"
EDIT = "https://www.tiktok.com/tiktokstudio/upload/post/{id}?from=creator_center"
CAPTION = "div[contenteditable=true]"
PRIVACY = {"public": "Everyone", "friends": "Friends", "private": "Only you"}


def check_create(privacy, allow_public):
    if privacy != "private" and not allow_public:
        raise SystemExit(f"refused: privacy '{privacy}' needs --allow-public (default is private)")


def check_delete(rows, post_id, allow_public):
    """Return the one row to delete, or exit with the reason. `rows` come from list_rows()."""
    hit = [r for r in rows if post_id in r["id"]]
    if len(hit) != 1 or not hit[0].get("more_selector"):
        raise SystemExit(f"refused: {len(hit)} loaded rows match id {post_id} (need exactly 1)")
    if hit[0]["privacy"] != "Only me" and not allow_public:
        raise SystemExit(f"refused: post is '{hit[0]['privacy']}', not 'Only me' (use --allow-public to override)")
    return hit[0]


async def list_rows(b):
    """Rendered rows of the Posts table: [{id, title, privacy, more_selector}].

    The table is virtualised, so only the posts near the top of the viewport come back. Browsentic
    masks long digit runs in results as `⟦card:…⟧`, so some ids may arrive masked and cannot be used
    with --id; identify those by title.
    """
    await b.call("page_navigate", url=CONTENT)
    await b.call("page_waitForElement", target={"selector": "a[href*='/video/']"})
    await asyncio.sleep(2)
    ui = (await b.call("page_getPageInfo", maxPerKind=200, geometry=True))["interactive"]
    links = [x for x in ui["links"] if "/video/" in x.get("href", "")]
    # the three-dots button is the icon-only button at the far right of each row (34 px wide)
    mores = sorted((x for x in ui["buttons"] if not x.get("text") and x.get("bounds", {}).get("width") == 34
                    and x["bounds"]["x"] > 1300), key=lambda x: x["bounds"]["y"])
    priv = sorted((x for x in ui["buttons"] if x.get("text") in ("Everyone", "Only me", "Friends")),
                  key=lambda x: x["bounds"]["y"])
    return [{
        "id": re.search(r"/video/(.+)$", link["href"]).group(1),
        "title": link["text"][:80],
        "privacy": priv[i]["text"] if i < len(priv) else "?",
        "more_selector": mores[i]["selector"] if i < len(mores) else None,
    } for i, link in enumerate(links)]


async def list_posts(a):
    async with browser() as b:
        for r in await list_rows(b):
            print(json.dumps({k: v for k, v in r.items() if k != "more_selector"}, ensure_ascii=False))


async def delete_post(a):
    async with browser() as b:
        row = check_delete(await list_rows(b), a.id, a.allow_public)
        print("deleting:", row["id"], row["title"], "|", row["privacy"])
        await b.call("page_clickElement", target={"selector": row["more_selector"]})
        bd = (await b.call("page_waitForElement", target={"selector": "[role=dialog]"}))["element"]["bounds"]
        # menu = Pin to top / Download / Delete. Clicking the dialog element itself lands on the middle
        # item, Download, so click inside the bottom third.
        await b.call("page_trustedClick", point={"x": bd["x"] + 60, "y": bd["y"] + int(bd["height"] * 0.79)})
        await b.call("page_waitForElement", target={"text": "Delete post?"})
        await b.call("page_clickElement", target={"selector": "#tux-portal-container button", "text": "Delete"})
        await asyncio.sleep(3)
        print("deleted" if all(a.id not in r["id"] for r in await list_rows(b)) else "STILL PRESENT - check Studio")


async def type_caption(b, text):
    """The caption editor ignores fillInput (the value reverts on submit); it needs real key events."""
    await b.call("page_focusInput", target={"selector": CAPTION}, caret="all")
    await b.call("page_pressKey", key="Backspace")
    await b.call("page_typeText", text=text, clear=False, speed="natural")


async def update_post(a):
    """NOT verified end to end. In the one live test the edit page took the typed text (its character
    counter followed it) and Save returned to the list, but the caption stayed unchanged on the server.
    TikTok allows one caption edit per post per day, so an earlier Save may have used the day's edit."""
    async with browser() as b:
        await b.call("page_navigate", url=EDIT.format(id=a.id))
        await b.call("page_waitForElement", target={"selector": CAPTION})
        await type_caption(b, a.caption)
        await b.call("page_clickElement", target={"role": "button", "text": "Save"})
        await asyncio.sleep(3)
        print("saved; verify on the Posts page (see the note in update_post)")


async def create_post(a):
    check_create(a.privacy, a.allow_public)
    video = Path(a.video).resolve()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8899", "--bind", "127.0.0.1"], cwd=video.parent,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    async with browser() as b:
        try:
            await asyncio.sleep(1.5)
            dl = await b.call("page_captureDownload", url=f"http://127.0.0.1:8899/{video.name}")
        finally:
            srv.terminate()
        await b.call("page_navigate", url=UPLOAD)
        await b.call("page_waitForElement", target={"text": "Select video"})
        await b.call("page_attachFile", target={"selector": "input[type=file]"}, downloadId=dl["downloadId"])
        await b.call("page_waitForElement", target={"selector": CAPTION})
        await asyncio.sleep(3)
        await type_caption(b, f"{a.marker} {a.caption}".strip())
        # privacy: the 'Who can see this post' combobox shows 'Everyone'; open it and pick the option
        await b.call("page_clickElement", target={"text": "Everyone"})
        await asyncio.sleep(1)
        await b.call("page_clickElement", target={"text": PRIVACY[a.privacy], "selector": "[role=option]"})
        await asyncio.sleep(1)
        text = (await b.call("page_extractText", maxLength=3000))["content"]
        if f"Who can see this post\n{PRIVACY[a.privacy]}" not in text:  # last check before the irreversible click
            raise SystemExit("refused to post: privacy is not " + PRIVACY[a.privacy])
        await b.call("page_clickElement", target={"role": "button", "text": "Post"})
        await asyncio.sleep(5)
        print("posted (check the list); privacy =", a.privacy)


def add_parser(sub):
    ap = sub.add_parser("tiktok", help="TikTok Studio posts: list / create / update / delete (live channel, guarded)")
    s = ap.add_subparsers(dest="cmd", required=True)
    s.add_parser("list").set_defaults(func=lambda a: run(list_posts(a)))
    c = s.add_parser("create")
    c.add_argument("--video", required=True)
    c.add_argument("--caption", default="")
    c.add_argument("--privacy", choices=list(PRIVACY), default="private")
    c.add_argument("--allow-public", action="store_true", help="required for friends/public posts")
    c.add_argument("--marker", default="TEST-CRUD", help="caption prefix so test posts are findable")
    c.set_defaults(func=lambda a: run(create_post(a)))
    u = s.add_parser("update", help="edit a caption (not verified end to end)")
    u.add_argument("--id", required=True)
    u.add_argument("--caption", required=True)
    u.set_defaults(func=lambda a: run(update_post(a)))
    d = s.add_parser("delete")
    d.add_argument("--id", required=True)
    d.add_argument("--allow-public", action="store_true", help="also allow deleting a non-private post")
    d.set_defaults(func=lambda a: run(delete_post(a)))
