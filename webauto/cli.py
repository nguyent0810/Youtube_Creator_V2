"""`python -m webauto <tool> <command>`: one entry point for every browser-automation tool."""
import argparse
import sys

from . import auth, chatgpt, flow, muse, studio, tiktok

TOOLS = (flow, chatgpt, muse, tiktok, studio)


def build_parser():
    ap = argparse.ArgumentParser(
        prog="python -m webauto",
        description="Browser automation without an LLM in the loop: replay fixed steps on sites that have no API.")
    ap.add_argument("--wait-login", type=int, default=auth.WAIT_LOGIN, metavar="SECONDS",
                    help="if a site is not signed in, wait this long for YOU to sign in in the open Chrome window, "
                         "then continue (default %(default)s; 0 = fail at once). webauto never types passwords or solves captchas")
    sub = ap.add_subparsers(dest="tool", required=True)
    for t in TOOLS:
        t.add_parser(sub)
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    auth.configure(args.wait_login)
    try:
        args.func(args)
    except BaseExceptionGroup as eg:  # anyio wraps errors raised inside the MCP session
        for e in _leaves(eg):
            if isinstance(e, SystemExit):  # a deliberate refusal: show just its message
                raise e
        raise


def _leaves(eg):
    for e in eg.exceptions:
        yield from _leaves(e) if isinstance(e, BaseExceptionGroup) else (e,)


if __name__ == "__main__":
    main()
