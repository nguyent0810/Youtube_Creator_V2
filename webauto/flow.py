"""Google Flow (flow.google.com): generate images or videos (text-to-video, image-to-video) and download them.

Drives a Playwright persistent Chrome profile kept in ~/.webauto/profiles/flow (log in once with
`webauto flow login`). Google does not challenge it, unlike chatgpt.com.

Selectors are English-UI selectors; the dedicated profile keeps Flow in English. Flow has no public
API, so these selectors are the fragile part: when the UI changes, fix them here.
"""
import re
import time
from pathlib import Path

from . import auth
from .common import default_out, parse_prompts, profile_dir

FLOW_URL = "https://flow.google.com/"
EDITOR = "flow-rich-text-editor div[role=textbox]"
GENERATE = "flow-generate-icon-button button"
SETTINGS = "button[aria-label='Settings trigger']"
DEFAULT_MODEL = {"image": "Nano Banana Pro", "video": "Omni 1.1 Flash"}
NEW_PROJECT = re.compile("Dự án mới|New project")
VIDEO_DONE = "flow-video-tile img[alt='Generated video thumbnail']"


def launch(p, headless=False):
    return p.chromium.launch_persistent_context(
        str(profile_dir("flow")), channel="chrome", headless=headless, accept_downloads=True,
        viewport={"width": 1400, "height": 900}, args=["--disable-blink-features=AutomationControlled"])


def login():
    """Open the profile so the owner can sign in to Google. Close the whole Chrome window when done:
    a Chrome left running keeps the profile locked and the next run cannot start."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx = launch(p)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(FLOW_URL)
        print("Sign in to Google in the opened window, then close it.")
        page.wait_for_event("close", timeout=0)
        ctx.close()


def new_project(page):
    page.goto(FLOW_URL)
    page.wait_for_timeout(3000)

    def signed_in():
        return not auth.url_is_login(page.url) and page.get_by_role("button", name=NEW_PROJECT).count() > 0

    # the window is the owner's to sign in to (Google may also ask for 2-step); webauto only waits
    auth.ensure_sync(signed_in, "Google Flow", FLOW_URL)
    page.get_by_role("button", name=NEW_PROJECT).click(timeout=60000)
    page.wait_for_url(re.compile(r"/project/"), timeout=30000)
    page.wait_for_selector(EDITOR, timeout=30000)


def apply_settings(page, mode, model=None, count=1, duration=6, ratio=None, res=None):
    """Open the settings popup and set mode / ratio / (resolution, duration) / model / count."""
    page.locator(SETTINGS).click()
    word = "Image" if mode == "image" else "Video"
    page.get_by_role("radio", name=re.compile(rf"^\s*(image|videocam)?\s*{word}\s*$")).click()
    if ratio:
        page.get_by_role("radio", name=re.compile(re.escape(ratio))).click()
    if mode == "video":
        if res:
            page.get_by_role("radio", name=re.compile(re.escape(res))).click()
        page.get_by_role("radio", name=re.compile(rf"^{duration}s$")).click()
    page.get_by_role("button", name="Select model family").click()
    page.get_by_role("menuitem", name=re.compile(re.escape(model or DEFAULT_MODEL[mode]))).click()
    page.get_by_role("radio", name=f"x{count}", exact=True).click()
    page.wait_for_timeout(500)
    print("settings:", page.locator(SETTINGS).inner_text().replace("\n", " "))
    page.keyboard.press("Escape")


def set_start_frame(page, image):
    """Video mode > Frames > Start slot > Upload media: use `image` as the first frame."""
    page.locator(SETTINGS).click()
    page.get_by_role("radio", name=re.compile("Frames")).click()
    page.keyboard.press("Escape")
    page.wait_for_timeout(800)
    page.get_by_role("button", name="Start", exact=True).click()
    with page.expect_file_chooser(timeout=30000) as fc:
        page.get_by_role("button", name="Upload media").click()  # get_by_text also matches a tooltip
    fc.value.set_files(str(image))
    # after the upload progress reaches 100% the asset is selected and "Add to prompt" turns enabled
    add = page.get_by_role("button", name="Add to prompt")
    for _ in range(90):
        if add.count() and add.first.is_enabled():
            break
        page.wait_for_timeout(1000)
    add.first.click()
    page.wait_for_selector("text=Select a frame image", state="detached", timeout=60000)
    page.wait_for_timeout(1500)


def media_srcs(page):
    """media-id -> signed CDN url of every generated image tile on the page."""
    return dict(page.eval_on_selector_all(
        "img[data-media-id], video[data-media-id]", "els => els.map(e => [e.dataset.mediaId, e.currentSrc || e.src])"))


def generate_images(page, prompt, out, tag, timeout_s=240):
    before = media_srcs(page)
    page.click(EDITOR)
    page.fill(EDITOR, prompt)
    page.click(GENERATE)
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if set(media_srcs(page)) - set(before):
            time.sleep(3)  # let the other variants settle
            new = {k: v for k, v in media_srcs(page).items() if k not in before}
            saved = []
            for n, (mid, url) in enumerate(new.items(), 1):
                resp = page.context.request.get(url)
                ext = ".jpg" if "jpeg" in resp.headers.get("content-type", "") else ".png"
                f = out / f"{tag}_{n}_{mid[:8]}{ext}"
                f.write_bytes(resp.body())
                saved.append(f)
            return saved
        time.sleep(2)
    raise TimeoutError("no new image appeared")


def generate_video(page, prompt, out, tag, quality="720p", timeout_s=900):
    """Videos have no direct URL: use the tile menu > Download > quality (720p is the original, free)."""
    before = page.locator(VIDEO_DONE).count()
    page.click(EDITOR)
    page.fill(EDITOR, prompt)
    page.click(GENERATE)
    deadline = time.time() + timeout_s
    while page.locator(VIDEO_DONE).count() <= before:
        if time.time() > deadline:
            raise TimeoutError("no new video appeared")
        time.sleep(5)
    time.sleep(2)
    saved = []
    for n in range(page.locator(VIDEO_DONE).count() - before):
        tile = page.locator("flow-video-tile").nth(n)  # newest tiles come first
        tile.hover()
        tile.get_by_role("button", name="More options").click()
        page.get_by_role("menuitem", name="Download").click()
        with page.expect_download(timeout=180000) as dl:
            page.get_by_role("menuitem", name=re.compile(rf"^{quality}")).click()
        f = out / f"{tag}_{n + 1}_{quality}.mp4"
        dl.value.save_as(str(f))
        saved.append(f)
    return saved


def generate(prompts, out, mode="image", model=None, count=1, duration=6, ratio=None, res=None,
             quality="720p", image=None, timeout=None, headless=False):
    """Generate for each (stem, prompt) in `prompts` inside one new Flow project; return saved files.

    `image` (video mode only) is uploaded once as the start frame, so every prompt animates that image.
    """
    if image and mode != "video":
        raise SystemExit("--image needs --mode video")
    from playwright.sync_api import sync_playwright

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    files = []
    with sync_playwright() as p:
        ctx = launch(p, headless)
        try:
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            new_project(page)
            apply_settings(page, mode, model, count, duration, ratio, res)
            if image:
                set_start_frame(page, Path(image).resolve())
            for stem, prompt in prompts:
                try:
                    if mode == "video":
                        got = generate_video(page, prompt, out, stem, quality, timeout or 900)
                    else:
                        got = generate_images(page, prompt, out, stem, timeout or 240)
                except TimeoutError:
                    (out / "fail.html").write_text(page.content(), encoding="utf-8")
                    try:
                        page.screenshot(path=str(out / "fail.png"), timeout=5000)  # can hang while a video plays
                    except Exception:
                        pass
                    raise
                print(f"{stem}: saved {len(got)} file(s)", *got, sep="\n  ")
                files += got
        finally:
            ctx.close()
    return files


def add_parser(sub):
    ap = sub.add_parser("flow", help="Google Flow: generate images / videos (Playwright)")
    s = ap.add_subparsers(dest="cmd", required=True)
    s.add_parser("login", help="sign in to Google once in the webauto profile").set_defaults(func=lambda a: login())
    g = s.add_parser("generate", help="generate and download")
    g.add_argument("--mode", choices=["image", "video"], default="image")
    src = g.add_mutually_exclusive_group(required=True)
    src.add_argument("--prompt")
    src.add_argument("--prompts-file", help="'name | prompt' per line, '#' comments")
    g.add_argument("--out", default=str(default_out("flow")))
    g.add_argument("--model", help="substring of the model name (default Nano Banana Pro / Omni 1.1 Flash)")
    g.add_argument("--count", type=int, choices=[1, 2, 3, 4], default=1, help="outputs per prompt")
    g.add_argument("--duration", type=int, choices=[4, 6, 8, 10], default=6, help="video seconds")
    g.add_argument("--ratio", choices=["16:9", "4:3", "1:1", "3:4", "9:16"])
    g.add_argument("--res", choices=["360p", "720p"], help="video generation resolution")
    g.add_argument("--quality", choices=["720p", "1080p", "4K"], default="720p", help="video download quality")
    g.add_argument("--image", help="video mode: start-frame image (image-to-video)")
    g.add_argument("--timeout", type=int, help="seconds per prompt (default 240 image / 900 video)")
    g.set_defaults(func=_run_generate)


def _run_generate(a):
    prompts = [("p1", a.prompt)] if a.prompt else parse_prompts(a.prompts_file)
    generate(prompts, a.out, a.mode, a.model, a.count, a.duration, a.ratio, a.res, a.quality, a.image, a.timeout)
