"""Thin client for the Browsentic MCP server (drives the user's real, signed-in Chrome).

Why Browsentic and not a script-launched browser: some sites (chatgpt.com) put a Cloudflare check in
front of automated Chrome that keeps coming back; the user's real Chrome is not challenged.

Browsentic keeps its own guardrails (it asks before form submits, uploads, downloads). From an MCP
client those prompts cannot be answered, so a gated action is refused until the owner sets the rule
to Allow in Browsentic > Guardrails. webauto never tries to get around that.
"""
import asyncio
import json
import os
import re
import subprocess
import sys
from contextlib import asynccontextmanager
from pathlib import Path

DOWNLOAD_DIR = Path.home() / "browsentic" / "download"


def server_params():
    from mcp import StdioServerParameters

    custom = os.environ.get("WEBAUTO_BROWSENTIC_CMD")  # e.g. "browsentic mcp"
    if custom:
        parts = custom.split()
        return StdioServerParameters(command=parts[0], args=parts[1:])
    if sys.platform == "win32":
        return StdioServerParameters(command="cmd", args=["/c", "npx", "-y", "browsentic@latest", "mcp"])
    return StdioServerParameters(command="npx", args=["-y", "browsentic@latest", "mcp"])


def parse_payload(text):
    """Tool results come wrapped in an 'untrusted page content' envelope; return the JSON inside."""
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0)) if m else {}


class Browser:
    def __init__(self, session):
        self.s = session

    async def call(self, tool, **args):
        res = await self.s.call_tool(tool, args)
        text = "".join(c.text for c in res.content if getattr(c, "text", None))
        # mcp đổi tên trường: isError (bản cũ) -> is_error (bản mới, 2026)
        if getattr(res, "is_error", None) or getattr(res, "isError", False):
            raise RuntimeError(f"{tool}: {text[:300]}")
        return parse_payload(text)

    async def first(self, tool, selectors, **args):
        """Try each selector in turn; raise the last error if none works."""
        last = None
        for sel in selectors:
            try:
                return await self.call(tool, target={"selector": sel}, **args)
            except RuntimeError as e:
                last = e
        raise last

    async def text(self, **target):
        """Whole rendered text of the page (or of `target`), following the read cursor."""
        parts, cursor = [], None
        while True:
            args = {"maxLength": 100000, **target}
            if cursor:
                args["cursor"] = cursor
            data = await self.call("page_extractText", **args)
            parts.append(data.get("content", ""))
            cursor = data.get("cursor")
            if not cursor:
                return "".join(parts)


@asynccontextmanager
async def browser():
    from mcp import ClientSession
    from mcp.client.stdio import stdio_client

    async with stdio_client(server_params()) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            yield Browser(session)


def run(coro):
    return asyncio.run(coro)


def clipboard():
    if sys.platform == "darwin":   # macOS: pbpaste (PowerShell only exists on Windows)
        r = subprocess.run(["pbpaste"], capture_output=True, encoding="utf-8")
    else:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "[Console]::OutputEncoding=[Text.Encoding]::UTF8; Get-Clipboard -Raw"],
            capture_output=True, encoding="utf-8")
    return (r.stdout or "").rstrip("\r\n")


def clear_clipboard():
    if sys.platform == "darwin":
        subprocess.run(["pbcopy"], input="", text=True, capture_output=True)
    else:
        subprocess.run(["powershell", "-NoProfile", "-Command", "Set-Clipboard -Value ''"], capture_output=True)


def newest_download(since):
    """Newest file Browsentic wrote since `since` (epoch s). Do not trust the `savedTo` it returns:
    long digit runs in a path are masked as a fake card number (`⟦card:…⟧`)."""
    fresh = [p for p in DOWNLOAD_DIR.glob("*") if p.is_file() and p.stat().st_mtime >= since]
    return max(fresh, key=lambda p: p.stat().st_mtime) if fresh else None
