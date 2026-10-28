"""TikTok Studio: list / create / update / delete posts through the user's real Chrome (Browsentic).

This acts on a LIVE channel, so (see CLAUDE.md: never publish, schedule or delete without the owner's say):
  - create  defaults to private ("Only you"); a non-private post needs --allow-public. The caption is
            prefixed with --marker so a test post is easy to find (pass --marker "" for a real post).
            --schedule "YYYY-MM-DD HH:MM" schedules instead of posting now: the time is read in the
            timezone TikTok Studio shows (--tz, default GMT+7), must be 20 min to 10 days ahead and a
            multiple of 5 minutes. Before the irreversible click it re-reads date, time, timezone,
            privacy and caption from the page and refuses on any mismatch. --dry-run does every step
            but the final click, then discards the draft.
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
from datetime import datetime, timedelta, timezone
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


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
SCHEDULE_MIN, SCHEDULE_MAX = timedelta(minutes=20), timedelta(days=10)   # TikTok Studio: up to 10 days ahead


def tz_of(label):
    """'GMT+7' / '+7' / 'GMT-3:30' -> tzinfo. The schedule is read in the timezone the Studio page shows."""
    m = re.fullmatch(r"(?:GMT|UTC)?([+-])(\d{1,2})(?::(\d{2}))?", label.strip())
    if not m:
        raise SystemExit(f"refused: cannot read timezone {label!r} (use e.g. GMT+7)")
    sign = 1 if m.group(1) == "+" else -1
    return timezone(sign * timedelta(hours=int(m.group(2)), minutes=int(m.group(3) or 0)))


def check_schedule(text, tz, now=None):
    """Parse 'YYYY-MM-DD HH:MM' in `tz` and refuse a time the Studio picker cannot hold or should not get."""
    try:
        when = datetime.strptime(text.strip(), "%Y-%m-%d %H:%M").replace(tzinfo=tz)
    except ValueError:
        raise SystemExit(f"refused: --schedule {text!r} is not 'YYYY-MM-DD HH:MM'")
    if when.minute % 5:
        raise SystemExit("refused: the Studio minute picker only has multiples of 5")
    now = now or datetime.now(tz)
    if when - now < SCHEDULE_MIN:
        raise SystemExit(f"refused: {when:%Y-%m-%d %H:%M} is less than 20 minutes ahead")
    if when - now > SCHEDULE_MAX:
        raise SystemExit(f"refused: {when:%Y-%m-%d %H:%M} is more than 10 days ahead (TikTok limit)")
    return when


def ordinal(n):
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def day_label(d):
    """aria-label fragment of a calendar day button: 'November 5th, 2026'."""
    return f"{MONTHS[d.month - 1]} {ordinal(d.day)}, {d.year}"


def shown_date(d):
    """How the date field shows a day: 'Nov 5, 2026'."""
    return f"{MONTHS[d.month - 1][:3]} {d.day}, {d.year}"


def settings_ok(text, when, privacy_label, ai_label=False):
    """The page text must show exactly what we asked for; returns the list of problems (empty = ok).
    The timezone selector's label is not part of the page text, so --tz cannot be read back here: it is
    the zone the date/time are entered in (Studio shows '(GMT+7) Local Time' for this channel's Chrome)."""
    bad = []
    if when is not None:
        if f"Schedule\n{shown_date(when)}\n{when:%H:%M}" not in text:
            m = re.search(r"Schedule\n([^\n]*)\n([^\n]*)", text)
            seen = f" (page shows {m.group(1)} {m.group(2)})" if m else ""
            bad.append(f"date/time is not {shown_date(when)} {when:%H:%M}{seen}")
    if ai_label and "Creator labeled as AI-generated" not in text:
        bad.append("AI-generated label is off")
    if f"Who can see this post\n{privacy_label}" not in text:
        bad.append(f"privacy is not {privacy_label}")
    return bad


def same_caption(typed, want):
    """Compare captions ignoring whitespace runs (the editor turns newlines into blocks)."""
    norm = lambda x: re.sub(r"\s+", " ", x).strip()  # noqa: E731
    return norm(typed) == norm(want)


def check_delete(rows, post_id, allow_public):
    """Return the one row to delete, or exit with the reason. `rows` come from list_rows()."""
    # exact match only: a substring match let a short or partial id pick some other single post
    hit = [r for r in rows if r["id"] == post_id]
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
    priv = [x for x in ui["buttons"] if x.get("text") in ("Everyone", "Only me", "Friends")]
    return pair_rows(links, priv, mores)


ROW_TOL = 30   # px: a row's link, privacy button and "…" button sit on the same horizontal band


def _mid_y(x):
    b = x.get("bounds") or {}
    return b["y"] + b.get("height", 0) / 2 if "y" in b else None


def pair_rows(links, priv, mores):
    """One dict per post link, with the privacy and "…" button on the SAME row (nearest centre-y within ROW_TOL).

    Pairing by list index (the first version) shifts every later row as soon as one row lacks a button,
    so delete could open the menu of a different post. A row with no button close enough gets "?" / None,
    which check_delete then refuses."""
    def near(y, items):
        best = min(items, key=lambda x: abs(_mid_y(x) - y), default=None) if y is not None else None
        return best if best is not None and abs(_mid_y(best) - y) <= ROW_TOL else None
    priv = [x for x in priv if _mid_y(x) is not None]
    mores = [x for x in mores if _mid_y(x) is not None]
    out = []
    for link in links:
        y = _mid_y(link)
        p, m = near(y, priv), near(y, mores)
        out.append({"id": re.search(r"/video/(.+)$", link["href"]).group(1), "title": link["text"][:80],
                    "privacy": p["text"] if p else "?", "more_selector": m["selector"] if m else None})
    return out


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


async def type_caption(b, text, default=""):
    """Write the caption with real key events (the editor ignores fillInput; the value reverts on submit).

    Traps found on Studio 28/10/2026:
      - typing into an EMPTY editor (after select-all + Backspace, or after deleting the prefilled file
        name first) crashes the upload page ("Something went wrong"). So the caption is typed AFTER the
        prefilled file name, and only then the name is selected and deleted: the editor is never empty;
      - the hashtag autocomplete mangles fast typing ("#phatgiao#phatgia#…"), and a tag typed without a
        space in front can be swallowed. Each tag is typed as " #tag" at natural speed."""
    await b.call("page_focusInput", target={"selector": CAPTION}, caret="end")
    parts = [p for p in re.split(r"\s*(#\w+)\s*", text) if p]
    for i, part in enumerate(parts):
        lead = " " if (i == 0 and default) or part.startswith("#") else ""
        speed = "natural" if part.startswith("#") else "instant"
        await b.call("page_typeText", text=lead + part, clear=False, speed=speed)
        if part.startswith("#"):
            await asyncio.sleep(1.2)
            await b.call("page_pressKey", key="Escape")   # close the suggestion list without picking
    if default:   # selecting the name with page_selectText deleted the wrong characters; walk from the start
        await b.call("page_focusInput", target={"selector": CAPTION}, caret="start")
        for _ in range(len(default) + 1):   # the file name and the space after it
            await b.call("page_pressKey", key="Delete")


async def update_post(a):
    """NOT verified end to end. In the one live test the edit page took the typed text (its character
    counter followed it) and Save returned to the list, but the caption stayed unchanged on the server.
    TikTok allows one caption edit per post per day, so an earlier Save may have used the day's edit."""
    async with browser() as b:
        await b.call("page_navigate", url=EDIT.format(id=a.id))
        await b.call("page_waitForElement", target={"selector": CAPTION})
        current = (await b.call("page_extractText", target={"selector": CAPTION})).get("content", "")
        await type_caption(b, a.caption, current.strip())
        await b.call("page_clickElement", target={"role": "button", "text": "Save"})
        await asyncio.sleep(3)
        print("saved; verify on the Posts page (see the note in update_post)")


async def viewport_point(b, bounds):
    """Centre of `bounds` in viewport coordinates. Browsentic reports element bounds in PAGE coordinates
    (a narrow window scrolls the Studio page sideways), while page_trustedClick takes viewport ones."""
    vp = (await b.call("page_getPageInfo", maxPerKind=1)).get("viewport") or {}
    return {"x": bounds["x"] + bounds["width"] / 2 - vp.get("scrollX", 0),
            "y": bounds["y"] + bounds["height"] / 2 - vp.get("scrollY", 0)}


async def click_at(b, selector):
    """Scroll an element into view and click its centre with a real (trusted) mouse event.
    The Studio hour wheel ignores synthetic clicks (the minute wheel does not), and it keeps gliding for a
    moment after scrollTo, so the bounds are measured only once it has settled."""
    await b.call("page_scrollTo", target={"selector": selector})
    await asyncio.sleep(0.8)
    el = (await b.call("page_waitForElement", target={"selector": selector}, state="visible"))["element"]
    await b.call("page_trustedClick", point=await viewport_point(b, el["bounds"]))


async def pick_wheel(b, kind, value, part):
    """Pick `value` in the 'Hours' or 'Minutes' wheel and confirm it on the time field; retry if a neighbour
    was hit (seen 28/10/2026: asked 06, got 05). `part` = 0 (hour) or 1 (minute) of the shown 'HH:MM'."""
    sel = (f'button.TimePicker__item[aria-label="{kind} {value:02d}"], '
           f'button.TimePicker__item[aria-label="{kind} {value}"]')
    for _ in range(3):
        await click_at(b, sel)
        await asyncio.sleep(0.6)
        m = re.search(r"Schedule\n[^\n]*\n(\d{2}):(\d{2})", await b.text())
        if m and int(m.group(part + 1)) == value:
            return
    raise SystemExit(f"refused: could not set {kind.lower()} to {value:02d}")


def schedule_points(ui):
    """Click points of the schedule row's date and time pickers.

    Neither picker is exposed as an interactive element (they are plain divs, no accessible text, and raw
    HTML is off-limits under Browsentic's policy). The row is anchored by two things that are exposed: the
    'Now' radio (left edge of the row) and the timezone combobox (right end). Measured on Studio 28/10/2026:
    the date field spans ~0-46 % and the time field ~50-96 % of the gap between them; their centres sit at
    ~23 % and ~73 %. A wrong click is caught later: the date and time are read back before anything is posted."""
    now = next((x for x in ui.get("fields", []) if x.get("role") == "radio" and x.get("text") == "Now"), None)
    radio = next((x for x in ui.get("fields", []) if x.get("role") == "radio" and x.get("text") == "Schedule"), None)
    if not now or not radio or "bounds" not in now or "bounds" not in radio:
        raise SystemExit("refused: cannot locate the schedule row on the page")
    top = radio["bounds"]["y"]
    tz = [x for x in ui.get("buttons", []) if x.get("role") == "combobox" and "bounds" in x
          and top < x["bounds"]["y"] < top + 80]
    if not tz:
        raise SystemExit("refused: no timezone selector next to the schedule date/time")
    tzb = tz[0]["bounds"]
    x0, gap, y = now["bounds"]["x"], tzb["x"] - now["bounds"]["x"], tzb["y"] + tzb["height"] / 2
    return (x0 + gap * 0.23, y), (x0 + gap * 0.73, y)


async def open_field(b, index):
    """Open the date (0) or time (1) picker of the schedule row with a real click.
    page_getPageInfo gives page coordinates; page_trustedClick wants viewport coordinates. The form scrolls
    in its own container, so the row is brought into view first; the click is retried once if the picker
    did not open (date: weekday header 'Sun Mon …'; time: the hour wheel)."""
    opened = (lambda t: "Sun\nMon" in t or "Su\nMo" in t) if index == 0 else (lambda t: "\n00\n" in t and "\n23\n" in t)
    for _ in range(2):
        await b.call("page_scrollTo", target={"text": "Schedule", "selector": "label"})
        await asyncio.sleep(0.5)
        info = await b.call("page_getPageInfo", maxPerKind=300, geometry=True)
        vp = info.get("viewport") or {}
        x, y = schedule_points(info["interactive"])[index]
        await b.call("page_trustedClick", point={"x": x - vp.get("scrollX", 0), "y": y - vp.get("scrollY", 0)})
        await asyncio.sleep(1)
        if opened(await b.text()):
            return
    raise SystemExit(f"refused: the {'date' if index == 0 else 'time'} picker did not open")


async def set_schedule(b, when):
    # the caption editor can scroll the page and leave a hashtag popup open: close it, bring the row into view
    await b.call("page_pressKey", key="Escape")
    for _ in range(4):
        try:
            await b.call("page_clickElement", target={"text": "Schedule", "selector": "label"})
            break
        except RuntimeError:
            await b.call("page_scrollTo", direction="down")
            await asyncio.sleep(0.5)
    else:
        raise SystemExit("refused: cannot find the 'Schedule' option")
    await asyncio.sleep(1)
    await open_field(b, 0)
    for _ in range(12):   # walk the calendar to the right month
        text = await b.text()
        if f"{MONTHS[when.month - 1]}\n{when.year}" in text or f"{MONTHS[when.month - 1]} {when.year}" in text:
            break
        await b.call("page_clickElement", target={"selector": 'button.DatePicker__nav[aria-label="Next month"]'})
        await asyncio.sleep(0.5)
    await b.call("page_clickElement", target={"selector": f'button.DatePicker__day[aria-label*="{day_label(when)}"]'})
    await asyncio.sleep(1)
    await open_field(b, 1)
    await pick_wheel(b, "Hours", when.hour, 0)
    await pick_wheel(b, "Minutes", when.minute, 1)
    await b.call("page_pressKey", key="Escape")


AI_LABEL_ON = "Creator labeled as AI-generated"   # text the page adds once the switch is on


async def set_ai_label(b):
    """Turn on Settings > Show more > 'AI-generated content'.

    Neither 'Show more' (a div) nor the switch is exposed to Browsentic, and raw HTML is off-limits, so
    both are clicked at offsets from the 'Who can see this post' combobox, the nearest exposed element.
    Measured on Studio 28/10/2026 (CSS px from the combobox's top-left): 'Show more' (+381, +146),
    the AI switch (+171, +286); the 'Disclose post content' switch is 67 px above it. The form scrolls
    inside its own container, so it is scrolled to the bottom (the Discard button) before the switch
    click. The page then shows AI_LABEL_ON, which is checked here and again before posting."""
    async def combobox():
        info = await b.call("page_getPageInfo", maxPerKind=300, geometry=True)
        box = next((x["bounds"] for x in info["interactive"].get("buttons", [])
                    if x.get("role") == "combobox" and x.get("text") in PRIVACY.values()), None)
        if not box:
            raise SystemExit("refused: cannot find the 'Who can see this post' selector")
        return box, info.get("viewport") or {}
    if AI_LABEL_ON in await b.text():
        return
    if "Show less" not in await b.text():
        await b.call("page_scrollTo", target={"text": "Discard", "role": "button"})
        await asyncio.sleep(0.6)
        box, vp = await combobox()
        await b.call("page_trustedClick", point={"x": box["x"] + 381 - vp.get("scrollX", 0),
                                                 "y": box["y"] + 146 - vp.get("scrollY", 0)})
        await asyncio.sleep(1)
        if "Show less" not in await b.text():
            raise SystemExit("refused: could not open Settings > Show more")
    await b.call("page_scrollTo", target={"text": "Discard", "role": "button"})
    await asyncio.sleep(0.6)
    box, vp = await combobox()
    await b.call("page_trustedClick", point={"x": box["x"] + 171 - vp.get("scrollX", 0),
                                             "y": box["y"] + 286 - vp.get("scrollY", 0)})
    await asyncio.sleep(1)
    text = await b.text()
    if AI_LABEL_ON not in text:
        raise SystemExit("refused: the AI-generated label did not turn on")
    if "Your brand" in text or "Branded content" in text:
        raise SystemExit("refused: the click hit 'Disclose post content' instead of the AI label")


async def upload_tab(b):
    """Switch to an open TikTok Studio upload tab (one showing a clean 'Select video' screen if there is
    one), or open a new one. Never navigates: see create_post."""
    tabs = [t for t in (await b.call("page_switchTab")).get("tabs", []) if "tiktokstudio/upload" in t.get("url", "")]
    for t in tabs:
        await b.call("page_switchTab", tabId=t["tabId"])
        if "When to post" not in await b.text():
            return
    if tabs:
        await b.call("page_switchTab", tabId=tabs[0]["tabId"])
    else:
        await b.call("page_openTab", url=UPLOAD)


async def discard(b):
    await b.call("page_clickElement", target={"role": "button", "text": "Discard"})
    await b.call("page_waitForElement", target={"text": "Discard this post?"})
    await b.call("page_clickElement", target={"selector": "[role=dialog] button", "text": "Discard"})
    await asyncio.sleep(2)


async def create_post(a):
    check_create(a.privacy, a.allow_public)
    tz = tz_of(a.tz)
    when = check_schedule(a.schedule, tz) if a.schedule else None
    caption = f"{a.marker} {a.caption}".strip()
    video = Path(a.video).resolve()
    async with browser() as b:
        # Reuse ONE upload tab and never navigate away from it or close it. The upload page keeps a
        # beforeunload handler even after Discard, so leaving it (navigate, reload, close) raises Chrome's
        # native "Leave site?" dialog, which blocks the tab: Browsentic cannot answer it.
        await upload_tab(b)
        try:
            if "When to post" in await b.text():   # a draft from an interrupted run is still open in this tab
                await discard(b)
            await b.call("page_waitForElement", target={"text": "Select video"}, timeoutMs=30000)
            # a draft left by an earlier closed tab comes back as "A video you were editing wasn't saved.
            # Continue editing? Discard | Continue": drop it, never continue someone else's draft
            if "Continue editing?" in await b.text():
                await b.call("page_clickElement", target={"text": "Discard"})
                await asyncio.sleep(1)
            # start the local file server only once the browser is up, so a failed connect never leaves it running
            srv = subprocess.Popen([sys.executable, "-m", "http.server", "8899", "--bind", "127.0.0.1"], cwd=video.parent,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                await asyncio.sleep(1.5)
                dl = await b.call("page_captureDownload", url=f"http://127.0.0.1:8899/{video.name}")
            finally:
                srv.terminate()
            await b.call("page_attachFile", target={"selector": "input[type=file]"}, downloadId=dl["downloadId"])
            a.default_caption = video.stem   # Studio prefills the caption with the file name
            try:
                await _fill_and_submit(b, a, when, caption)
            except BaseException as e:
                print(e if isinstance(e, SystemExit) else f"error: {e}")
                # never leave a half-filled draft behind: TikTok may keep it
                try:
                    await discard(b)
                    print("draft discarded after an error")
                except Exception:  # noqa: BLE001
                    print("could not discard the draft - check TikTok Studio")
                raise
        finally:
            pass   # keep the tab: see above


async def _fill_and_submit(b, a, when, caption):
    # the editor appears only after the upload is accepted; the tool caps one wait at 30 s
    for _ in range(4):
        try:
            await b.call("page_waitForElement", target={"selector": CAPTION}, timeoutMs=30000)
            break
        except RuntimeError:
            continue
    else:
        raise SystemExit("refused: the caption editor never appeared (upload not accepted?)")
    # typing while the video is still "Uploading..." is not safe; wait for it to finish
    for _ in range(60):
        if "Uploading" not in await b.text():
            break
        await asyncio.sleep(2)
    else:
        raise SystemExit("refused: the video is still uploading after 2 minutes")
    await type_caption(b, caption, a.default_caption)
    # privacy: the 'Who can see this post' combobox shows 'Everyone'; open it and pick the option
    if a.privacy != "public":
        await b.call("page_clickElement", target={"text": "Everyone"})
        await asyncio.sleep(1)
        await b.call("page_clickElement", target={"text": PRIVACY[a.privacy], "selector": "[role=option]"})
        await asyncio.sleep(1)
    if when:
        await set_schedule(b, when)
    if a.ai_label:
        await set_ai_label(b)
    # last checks before the irreversible click: everything is read back from the page
    text = await b.text()
    typed = (await b.call("page_extractText", target={"selector": CAPTION}, maxLength=5000)).get("content", "")
    bad = settings_ok(text, when, PRIVACY[a.privacy], a.ai_label)
    if not same_caption(typed, caption):
        bad.append(f"caption on the page differs: {typed[:120]!r}")
    if bad:
        raise SystemExit("REFUSED: " + "; ".join(bad))
    if a.dry_run:
        print("DRY RUN ok: all settings read back as asked")
        await discard(b)
        print("draft discarded")
        return
    button = "Schedule" if when else "Post"
    await b.call("page_clickElement", target={"role": "button", "text": button})
    await asyncio.sleep(6)
    print(f"{'scheduled for ' + when.strftime('%Y-%m-%d %H:%M') + ' ' + a.tz if when else 'posted'}"
          f" (check the Posts list); privacy = {a.privacy}")


def add_parser(sub):
    ap = sub.add_parser("tiktok", help="TikTok Studio posts: list / create / update / delete (live channel, guarded)")
    s = ap.add_subparsers(dest="cmd", required=True)
    s.add_parser("list").set_defaults(func=lambda a: run(list_posts(a)))
    c = s.add_parser("create")
    c.add_argument("--video", required=True)
    c.add_argument("--caption", default="")
    c.add_argument("--privacy", choices=list(PRIVACY), default="private")
    c.add_argument("--allow-public", action="store_true", help="required for friends/public posts")
    c.add_argument("--marker", default="TEST-CRUD", help="caption prefix so test posts are findable; \"\" for a real post")
    c.add_argument("--schedule", default=None, help="'YYYY-MM-DD HH:MM' in --tz; 20 min to 10 days ahead, minutes in 5s")
    c.add_argument("--tz", default="GMT+7", help="timezone TikTok Studio shows next to the schedule (checked on the page)")
    c.add_argument("--ai-label", action="store_true", help="turn on the 'AI-generated content' label")
    c.add_argument("--dry-run", action="store_true", help="do every step except the final click, then discard the draft")
    c.set_defaults(func=lambda a: run(create_post(a)))
    u = s.add_parser("update", help="edit a caption (not verified end to end)")
    u.add_argument("--id", required=True)
    u.add_argument("--caption", required=True)
    u.set_defaults(func=lambda a: run(update_post(a)))
    d = s.add_parser("delete")
    d.add_argument("--id", required=True)
    d.add_argument("--allow-public", action="store_true", help="also allow deleting a non-private post")
    d.set_defaults(func=lambda a: run(delete_post(a)))
