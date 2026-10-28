"""Sign-in handling shared by every tool.

Rule: webauto never types a password, never solves a captcha / "verify you are human" check and never
tries to get around one. When a site is not signed in (or shows such a check) the tool says so, keeps the
browser window open, and waits for the OWNER to sign in or solve it there; then it carries on by itself.

`--wait-login SECONDS` (global, default 120) sets how long to wait; 0 means fail at once with the hint.
"""
import asyncio
import time

WAIT_LOGIN = 120  # set by cli.main from --wait-login


class LoginRequired(SystemExit):
    """Raised (as a clean exit with a message) when a site needs the owner to sign in."""


def configure(wait_s):
    global WAIT_LOGIN
    WAIT_LOGIN = wait_s


def hint(site, url):
    return (f"{site}: not signed in (or blocked by a human check). Sign in / solve it yourself in the Chrome "
            f"window at {url}, then run again, or use --wait-login SECONDS so webauto waits for you. "
            "webauto never enters passwords or solves captchas.")


async def ensure(check, site, url, wait_s=None, poll=3, say=print):
    """Return once `await check()` is True; otherwise wait up to wait_s for the owner, then raise LoginRequired."""
    wait_s = WAIT_LOGIN if wait_s is None else wait_s
    if await check():
        return
    if wait_s <= 0:
        raise LoginRequired(hint(site, url))
    say(f"{site}: not signed in. Sign in in the open Chrome window ({url}); waiting up to {wait_s}s ...")
    deadline = time.time() + wait_s
    while time.time() < deadline:
        await asyncio.sleep(poll)
        if await check():
            say(f"{site}: signed in, continuing.")
            return
    raise LoginRequired(hint(site, url) + f" (waited {wait_s}s)")


def ensure_sync(check, site, url, wait_s=None, poll=3, say=print):
    """Same for the Playwright tools; `check` is a plain function."""
    wait_s = WAIT_LOGIN if wait_s is None else wait_s
    if check():
        return
    if wait_s <= 0:
        raise LoginRequired(hint(site, url))
    say(f"{site}: not signed in. Sign in in the open Chrome window ({url}); waiting up to {wait_s}s ...")
    deadline = time.time() + wait_s
    while time.time() < deadline:
        time.sleep(poll)
        if check():
            say(f"{site}: signed in, continuing.")
            return
    raise LoginRequired(hint(site, url) + f" (waited {wait_s}s)")


# ---- page-text heuristics (pure, tested) ------------------------------------------------------------------

def chatgpt_signed_out(text):
    """Logged-out chatgpt.com shows Log in / Sign up in the header; a Cloudflare check shows 'verify you are human'."""
    t = text.lower()
    if "verify you are human" in t or "just a moment" in t:
        return True
    return ("log in" in t and "sign up" in t) or "đăng nhập" in t and "đăng ký" in t


def url_is_login(url):
    u = (url or "").lower()
    return any(x in u for x in ("accounts.google.com", "/login", "/signin", "/sign-in", "servicelogin"))
