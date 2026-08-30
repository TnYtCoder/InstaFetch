#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║  InstaFetch  —  Clean Instagram Intelligence & Profile Inspector         ║
║  Author      :  TnYtCoder                                                ║
║  Version     :  3.5                                                      ║
║  Powered by  :  Rich & ScrapeCreators API                                ║
╚══════════════════════════════════════════════════════════════════════════╝

★ QUICK SETUP — PASTE YOUR API KEY HERE (easiest method)
  Get a free key (10,000 free credits) at https://app.scrapecreators.com
  Documentation: https://docs.scrapecreators.com
"""

# ══════════════════════════════════════════════════════════════════════════
#  👉  PASTE YOUR SCRAPECREATORS API KEY HERE (Optional if using ENV / CLI)
# ══════════════════════════════════════════════════════════════════════════
API_KEY = "YOUR_API_KEY_HERE"  # e.g. API_KEY = "sc_live_abc123..."

import argparse
import json
import os
import re
import sys
import time
import webbrowser
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# ── Terminal Encoding & Environment Configuration ───────────────────────
if sys.platform == "win32":
    try:
        os.system("")
    except Exception:
        pass
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ── Third-Party UI & Networking ──────────────────────────────────────────
try:
    import requests
except ImportError:
    print("\n[!] Error: 'requests' is required. Install it using: pip install requests\n")
    sys.exit(1)

try:
    from rich import box
    from rich.align import Align
    from rich.columns import Columns
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.prompt import Confirm, Prompt
    from rich.rule import Rule
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("\n[!] Error: 'rich' is required. Install it using: pip install rich\n")
    sys.exit(1)

# ── Branding & Constants ────────────────────────────────────────────────
TOOL_NAME = "InstaFetch"
AUTHOR    = "TnYtCoder"
VERSION   = "3.5"
API_BASE  = "https://api.scrapecreators.com"

ENDPOINTS = {
    "profile":          "/v1/instagram/profile",
    "basic_profile":    "/v1/instagram/basic-profile",
    "posts":            "/v2/instagram/user/posts",
    "reels":            "/v1/instagram/user/reels",
    "tagged":           "/v1/instagram/user/tagged-posts",
    "highlights":       "/v1/instagram/user/highlights",
    "highlight_detail": "/v1/instagram/user/highlight/detail",
}

console = Console(legacy_windows=False if sys.platform == "win32" else None)

# ── Master ASCII Art ────────────────────────────────────────────────────
ASCII_BANNER_HTML = """<span style="color:#FFFFFF">██</span><span style="color:#AAAAAA">                             </span><span style="color:#FFFFFF">██▀▀██</span><span style="color:#AAAAAA">                            </span>
<span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF">██████</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF">██▀▀██</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">██</span><span style="color:#AAAAAA">     </span><span style="color:#5555FF;background-color:#0000AA">██</span><span style="color:#5555FF">▀▀██</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#FFFFFF">▄▄</span><span style="color:#AAAAAA">   </span><span style="color:#5555FF">██▀▀██</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">██</span><span style="color:#AAAAAA">     </span><span style="color:#5555FF">██▀▀██</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF">██</span><span style="color:#AAAAAA">  </span><span style="color:#5555FF">██</span>
<span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#AAAAAA">  </span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#5555FF">▄▄▄</span><span style="color:#AAAAAA">  </span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#5555FF">▄▄▄▄</span><span style="color:#AAAAAA">  </span><span style="color:#5555FF">▄▄▄</span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA">     </span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#AAAAAA">  </span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#5555FF">▄▄▄▄</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#AAAAAA">  </span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#5555FF">▄▄</span><span style="color:#5555FF;background-color:#0000AA">▓▓</span>
<span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">▒▒</span><span style="color:#AAAAAA">  </span><span style="color:#5555FF;background-color:#0000AA">▒▒</span><span style="color:#AAAAAA">    </span><span style="color:#0000AA">▐</span><span style="color:#5555FF;background-color:#0000AA">▒</span><span style="color:#5555FF">▌</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">▒▒</span><span style="color:#AAAAAA">     </span><span style="color:#5555FF">▐</span><span style="color:#5555FF;background-color:#0000AA">▒</span><span style="color:#0000AA">▌</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">▒▒</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA">     </span><span style="color:#5555FF;background-color:#0000AA">▒▒</span><span style="color:#AAAAAA">  </span><span style="color:#5555FF;background-color:#0000AA">▒▒</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">▒▒</span><span style="color:#AAAAAA">     </span><span style="color:#5555FF;background-color:#0000AA">▒▒</span><span style="color:#AAAAAA">     </span><span style="color:#5555FF;background-color:#0000AA">▒▒</span><span style="color:#AAAAAA">  </span><span style="color:#5555FF;background-color:#0000AA">▒▒</span>
<span style="color:#0000AA">▄▄</span><span style="color:#AAAAAA"> </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA">  </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA"> </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA">  </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA"> </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA">  </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA"> </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA">  </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA"> </span><span style="color:#0000AA">▄▄</span><span style="color:#AAAAAA">     </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA">  </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA"> </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA">  </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA"> </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA">     </span><span style="color:#0000AA">▀▀</span><span style="color:#AAAAAA">  </span><span style="color:#0000AA">▀▀</span>
<span style="color:#5555FF;background-color:#0000AA">░░</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">░░</span><span style="color:#AAAAAA">     </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA">     </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">░░</span>
<span style="color:#5555FF;background-color:#0000AA">▒▒</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">▒▒</span><span style="color:#AAAAAA">     </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF">▐</span><span style="color:#FFFFFF;background-color:#AAAAAA">▒</span><span style="color:#AAAAAA">▌ </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA">     </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▒▒</span>
<span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF;background-color:#0000AA">▓▓</span><span style="color:#AAAAAA">     </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#FFFFFF">▀▀</span><span style="color:#AAAAAA">   </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA">     </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF;background-color:#AAAAAA">▓▓</span>
<span style="color:#5555FF">██</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF">██</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF">██</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF">██████</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF">██████</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF">██████</span><span style="color:#AAAAAA"> </span><span style="color:#5555FF">██</span><span style="color:#AAAAAA">     </span><span style="color:#FFFFFF">██▄▄██</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF">██████</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF">██▄▄██</span><span style="color:#AAAAAA"> </span><span style="color:#FFFFFF">██</span><span style="color:#AAAAAA">  </span><span style="color:#FFFFFF">██</span>"""

def parse_html_to_rich(html: str) -> List[Text]:
    """Convert HTML ASCII spans into styled Rich Text objects."""
    lines = html.strip().split("\n")
    rich_lines: List[Text] = []
    span_regex = re.compile(r'<span style="([^"]+)">([^<]*)</span>')
    for line in lines:
        t = Text()
        matches = span_regex.findall(line)
        for style_str, content in matches:
            fg = None
            bg = None
            for prop in style_str.split(";"):
                prop = prop.strip()
                if prop.startswith("color:"):
                    fg = prop.split(":")[1].strip()
                elif prop.startswith("background-color:"):
                    bg = prop.split(":")[1].strip()

            style_spec = ""
            if fg and fg != "#AAAAAA":
                style_spec += f"{fg}"
            if bg and bg != "#AAAAAA":
                style_spec += f" on {bg}" if style_spec else f"on {bg}"
            if fg == "#AAAAAA" and not bg:
                style_spec = "dim"

            t.append(content, style=style_spec if style_spec else None)
        rich_lines.append(t)
    return rich_lines


# ── Helper Functions ────────────────────────────────────────────────────
def clear_screen():
    """Clear terminal screen safely across operating systems."""
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass


def clean_handle(handle: Optional[str]) -> str:
    """Normalize Instagram handles or URLs to a pure username."""
    if not handle:
        return ""
    h = handle.strip()
    if "instagram.com" in h:
        try:
            if not h.startswith("http://") and not h.startswith("https://"):
                h = "https://" + h
            from urllib.parse import urlparse
            pr = urlparse(h)
            parts = [p for p in pr.path.strip("/").split("/") if p]
            if parts and parts[0] not in ("p", "reel", "reels", "stories", "explore"):
                h = parts[0]
        except Exception:
            pass
    if h.startswith("@"):
        h = h[1:]
    return h.split("?")[0].split("/")[0].strip().lower()


def fmt_num(n: Any) -> str:
    """Format large numbers into human-readable shorthand (e.g. 1.2M)."""
    try:
        n = int(n)
        if n >= 1_000_000_000:
            return f"{n / 1_000_000_000:.1f}B"
        if n >= 1_000_000:
            return f"{n / 1_000_000:.1f}M"
        if n >= 1_000:
            return f"{n / 1_000:.1f}K"
        return f"{n:,}"
    except Exception:
        return str(n) if n is not None else "—"


def fmt_num_full(n: Any) -> str:
    """Format numbers into combined shorthand and exact integer value."""
    try:
        n = int(n)
        short = fmt_num(n)
        return f"{short} ({n:,})" if n >= 1000 else f"{n:,}"
    except Exception:
        return "—"


def fmt_date(ts: Any) -> str:
    """Convert a timestamp into a compact date string."""
    try:
        if not ts:
            return "—"
        ts = int(ts)
        dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone()
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return str(ts)[:10] if ts else "—"


def get_deep(data: Any, path: str, default: Any = None) -> Any:
    """Safely traverse nested dictionary keys via dot notation."""
    cur = data
    for p in path.split("."):
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return default
    return cur


def load_api_key(cli_key: Optional[str] = None) -> Optional[str]:
    """Retrieve API key with clear priority."""
    if API_KEY and API_KEY.strip() and API_KEY.strip() != "YOUR_API_KEY_HERE":
        return API_KEY.strip()
    if cli_key and cli_key.strip():
        return cli_key.strip()
    for env_var in ("SCRAPECREATORS_API_KEY", "SCRAPE_CREATORS_API_KEY", "SC_API_KEY"):
        val = os.getenv(env_var)
        if val and val.strip():
            return val.strip()
    config_paths = [
        os.path.expanduser("~/.config/scrapecreators/config.json"),
        os.path.expanduser("~/.config/scrapecreators/config"),
        os.path.expanduser("~/.scrapecreators.json"),
    ]
    for cp in config_paths:
        try:
            if os.path.exists(cp):
                with open(cp, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    for k in ("apiKey", "api_key", "api-key", "key"):
                        if k in d and d[k]:
                            return str(d[k]).strip()
        except Exception:
            pass
    return None


# ── Network Engine ──────────────────────────────────────────────────────
class InstaClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.api_key,
            "Accept": "application/json",
            "User-Agent": f"{TOOL_NAME}/{VERSION} (by {AUTHOR})",
        })

    def request(self, endpoint_key: str, params: Dict[str, Any], verbose: bool = False) -> Tuple[Dict[str, Any], int, str]:
        if endpoint_key not in ENDPOINTS:
            raise ValueError(f"Unknown endpoint: {endpoint_key}")
        url = f"{API_BASE}{ENDPOINTS[endpoint_key]}"
        cleaned_params = {k: v for k, v in params.items() if v is not None}

        if verbose:
            console.print(f"[dim]→ GET {url} params={cleaned_params}[/dim]")

        t0 = time.time()
        try:
            resp = self.session.get(url, params=cleaned_params, timeout=35)
            elapsed_ms = (time.time() - t0) * 1000

            if verbose:
                console.print(f"[dim]✓ HTTP {resp.status_code} in {elapsed_ms:.0f}ms[/dim]")

            if resp.status_code == 401:
                raise RuntimeError("Invalid or missing API key (HTTP 401). Get a free key at https://app.scrapecreators.com")
            elif resp.status_code == 402:
                raise RuntimeError("API account is out of credits (HTTP 402). Recharge at https://app.scrapecreators.com")
            elif resp.status_code == 404:
                raise RuntimeError("Requested resource or user was not found on Instagram (HTTP 404).")
            elif resp.status_code == 429:
                raise RuntimeError("Rate limit exceeded (HTTP 429). Please wait a moment before trying again.")
            elif not resp.ok:
                try:
                    err_json = resp.json()
                    msg = err_json.get("message") or err_json.get("error") or resp.text
                except Exception:
                    msg = resp.text or f"HTTP {resp.status_code}"
                raise RuntimeError(f"API Error ({resp.status_code}): {msg}")

            data = resp.json()
            return data, resp.status_code, resp.url

        except requests.exceptions.Timeout:
            raise RuntimeError("Request timed out after 35 seconds. Instagram or API server took too long to respond.")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Network connection error. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"HTTP Request failed: {e}")

    def get_profile(self, handle: str, trim: bool = False, cache_max_age: Optional[str] = None, verbose: bool = False):
        p = {"handle": clean_handle(handle)}
        if trim:
            p["trim"] = "true"
        if cache_max_age:
            p["cache_max_age"] = cache_max_age
        return self.request("profile", p, verbose)

    def get_basic_profile(self, user_id: str, verbose: bool = False):
        return self.request("basic_profile", {"userId": str(user_id)}, verbose)

    def get_posts(self, handle: str, verbose: bool = False):
        return self.request("posts", {"handle": clean_handle(handle)}, verbose)

    def get_reels(self, handle: str, verbose: bool = False):
        return self.request("reels", {"handle": clean_handle(handle)}, verbose)

    def get_tagged(self, user_id: str, verbose: bool = False):
        return self.request("tagged", {"user_id": str(user_id)}, verbose)

    def get_highlights(self, handle: str, verbose: bool = False):
        return self.request("highlights", {"handle": clean_handle(handle)}, verbose)

    def get_highlight_detail(self, highlight_id: str, verbose: bool = False):
        return self.request("highlight_detail", {"id": str(highlight_id)}, verbose)


def extract_user_id(profile_data: Dict[str, Any]) -> Optional[str]:
    """Extract numeric Instagram user ID from profile data structures."""
    if not profile_data or not isinstance(profile_data, dict):
        return None
    payload = profile_data.get("data", profile_data)
    user = payload.get("user") if isinstance(payload, dict) else None
    if not user and isinstance(payload, dict) and ("id" in payload or "pk" in payload or "username" in payload):
        user = payload
    if isinstance(user, dict):
        return str(user.get("id") or user.get("pk") or "") or None
    return str(profile_data.get("id") or profile_data.get("pk") or "") or None


# ── Visual Components & UI Rendering ────────────────────────────────────

def show_banner():
    """Render the master InstaFetch ASCII art banner."""
    banner_lines = parse_html_to_rich(ASCII_BANNER_HTML)

    sub_bar = Text()
    sub_bar.append(f"v{VERSION}", style="bold color(214)")
    sub_bar.append("  •  ", style="dim")
    sub_bar.append("Clean Instagram Intelligence & OSINT Inspector", style="italic color(252)")
    sub_bar.append("  •  ", style="dim")
    sub_bar.append(f"Author: {AUTHOR}", style="bold color(207)")

    content = []
    for bl in banner_lines:
        content.append(Align.center(bl))
    content.append(Text(""))
    content.append(Align.center(sub_bar))

    panel = Panel(
        Align.center(Group(*content)),
        box=box.ROUNDED,
        border_style="color(207)",
        padding=(0, 1),
    )
    console.print(panel)


def show_disclaimer():
    """Display compact disclaimer notice."""
    info = Text()
    info.append("ℹ  ", style="bold cyan")
    info.append("Uses ScrapeCreators API (docs.scrapecreators.com). Research & OSINT only. Respect Instagram ToS.", style="dim")
    console.print(Align.center(info))
    console.print()


def show_detailed_disclaimer():
    """Display comprehensive line-by-line legal and usage policy disclaimer."""
    tbl = Table(box=box.ROUNDED, show_header=True, header_style="bold color(214)", border_style="color(207)", expand=True)
    tbl.add_column("Section / Policy", style="bold cyan", width=22)
    tbl.add_column("Detailed Breakdown & Terms", style="white")

    tbl.add_row(
        "1. API Provider Attribution",
        "• InstaFetch interfaces with the ScrapeCreators third-party API engine (https://docs.scrapecreators.com).\n"
        "• InstaFetch is an independent client tool and is not owned, operated, or maintained by ScrapeCreators.\n"
        "• All API data processing, rate allocations, uptime, and availability are subject to ScrapeCreators terms and quotas."
    )
    tbl.add_row(
        "2. Meta Non-Affiliation",
        "• InstaFetch and its author (TnYtCoder) are NOT affiliated, associated, authorized, endorsed by,\n"
        "  or in any official way connected with Instagram, Meta Platforms, Inc., or any of their subsidiaries.\n"
        "• The official Instagram website can be accessed at https://www.instagram.com."
    )
    tbl.add_row(
        "3. Public Data & Privacy",
        "• This tool only queries publicly accessible account information indexed and served via the API.\n"
        "• InstaFetch does NOT bypass private account protections, decrypt credentials, or access unauthorized data.\n"
        "• No user search history or personal data is collected or tracked by InstaFetch."
    )
    tbl.add_row(
        "4. Permitted Usage & ToS",
        "• InstaFetch is created strictly for academic research, OSINT investigations, authorized security testing,\n"
        "  and educational purposes.\n"
        "• Users are solely responsible for ensuring compliance with Instagram's Terms of Service and applicable privacy laws (e.g. GDPR, CCPA).\n"
        "• Automated scraping or bulk harassment using this tool is strictly prohibited."
    )
    tbl.add_row(
        "5. API Keys & Credentials",
        "• Your ScrapeCreators API key is kept locally on your machine and only sent via HTTPS to the official API endpoint.\n"
        "• No credentials are ever sent to third-party telemetry servers or external databases."
    )
    tbl.add_row(
        "6. Limitation of Liability",
        "• This software is provided 'AS-IS' without warranty of any kind, express or implied.\n"
        "• Under no circumstances shall the author (TnYtCoder) be held liable for any damages, rate limits, account actions,\n"
        "  or legal consequences resulting from the use or misuse of this tool."
    )

    console.print(Panel(tbl, title="[bold color(207)]📜 InstaFetch — Comprehensive Disclaimer & Usage Policy[/bold color(207)]", box=box.ROUNDED, border_style="color(207)"))
    console.print()


def render_profile(data: Dict[str, Any]):
    """Render comprehensive profile dashboard."""
    payload = data.get("data", data)
    user = payload.get("user") if isinstance(payload, dict) else None
    if not user and isinstance(payload, dict) and "username" in payload:
        user = payload

    if not user:
        console.print(Panel("[bold red]⚠ No user data found in response.[/bold red]", box=box.ROUNDED))
        return

    username = get_deep(user, "username", "—")
    full_name = get_deep(user, "full_name", "") or "—"
    bio = get_deep(user, "biography", "") or ""
    bio_links = get_deep(user, "bio_links", []) or []
    external_url = get_deep(user, "external_url") or ""
    followers = get_deep(user, "edge_followed_by.count", 0)
    following = get_deep(user, "edge_follow.count", 0)
    posts_cnt = get_deep(user, "edge_owner_to_timeline_media.count", 0)
    is_verified = get_deep(user, "is_verified", False)
    is_private = get_deep(user, "is_private", False)
    is_business = get_deep(user, "is_business_account", False)
    is_pro = get_deep(user, "is_professional_account", False)
    category = get_deep(user, "category_name") or ""
    uid = get_deep(user, "id", "—")
    pic = get_deep(user, "profile_pic_url_hd") or get_deep(user, "profile_pic_url") or "—"
    business_addr = get_deep(user, "business_address_json") or {}
    timeline = get_deep(user, "edge_owner_to_timeline_media", {}) or {}
    related = get_deep(user, "edge_related_profiles.edges", []) or []
    credits_rem = data.get("credits_remaining")
    cached = data.get("cached")

    # Header Badges
    header_text = Text()
    header_text.append(f" @{username} ", style="bold white on color(207)")
    header_text.append(" ")
    if is_verified:
        header_text.append(" [✔ VERIFIED] ", style="bold white on cyan")
        header_text.append(" ")
    if is_private:
        header_text.append(" [🔒 PRIVATE] ", style="bold white on color(208)")
        header_text.append(" ")
    else:
        header_text.append(" [PUBLIC] ", style="bold white on green")
        header_text.append(" ")
    if is_business:
        header_text.append(" [BUSINESS] ", style="bold white on magenta")
        header_text.append(" ")
    if is_pro:
        header_text.append(" [PRO] ", style="bold white on blue")

    # Metrics Table
    metrics_tbl = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold color(214)", expand=True)
    metrics_tbl.add_column("Followers", justify="center", style="bold cyan")
    metrics_tbl.add_column("Following", justify="center", style="bold green")
    metrics_tbl.add_column("Posts / Media", justify="center", style="bold yellow")
    metrics_tbl.add_column("Account Type", justify="center", style="bold magenta")

    acc_type = "Business" if is_business else ("Creator/Pro" if is_pro else "Standard")
    metrics_tbl.add_row(
        fmt_num_full(followers),
        fmt_num_full(following),
        fmt_num_full(posts_cnt),
        acc_type
    )

    # Details Table
    details_tbl = Table(box=box.MINIMAL, show_header=False, expand=True)
    details_tbl.add_column("Key", style="bold color(250)", width=16, no_wrap=True)
    details_tbl.add_column("Value", style="white")

    details_tbl.add_row("Full Name", f"[bold]{full_name}[/bold]" + (f" [dim]({category})[/dim]" if category else ""))
    details_tbl.add_row("User ID (PK)", f"[cyan]{uid}[/cyan]")
    details_tbl.add_row("Profile Link", f"[link=https://instagram.com/{username}]https://instagram.com/{username}[/link]")

    if bio.strip():
        details_tbl.add_row("Biography", bio.strip())
    else:
        details_tbl.add_row("Biography", "[dim]No biography available[/dim]")

    if external_url:
        details_tbl.add_row("External URL", f"[blue underline]{external_url}[/blue underline]")

    if bio_links:
        links_str = " | ".join([f"[blue underline]{lk.get('url') or lk.get('title') or 'Link'}[/blue underline]" for lk in bio_links])
        details_tbl.add_row("Bio Links", links_str)

    if business_addr and any(business_addr.values()):
        city = business_addr.get("city_name") or business_addr.get("address_street") or ""
        if city:
            details_tbl.add_row("Location", f"📍 {city}")

    if pic and pic != "—":
        details_tbl.add_row("Profile Picture", f"[dim]{pic[:75]}...[/dim]")

    # Main Profile Panel
    profile_panel = Panel(
        Group(
            header_text,
            Text(""),
            metrics_tbl,
            Text(""),
            details_tbl
        ),
        title=f"[bold color(207)]Profile Overview — @{username}[/bold color(207)]",
        box=box.ROUNDED,
        border_style="color(207)",
        padding=(1, 2),
    )
    console.print(profile_panel)

    # Recent Posts Snapshot
    edges = timeline.get("edges", []) if isinstance(timeline, dict) else []
    if edges:
        posts_tbl = Table(
            title=f"📸 Recent Timeline Posts ({len(edges)} previewed)",
            box=box.ROUNDED,
            header_style="bold color(214)",
            border_style="dim",
            expand=True
        )
        posts_tbl.add_column("#", justify="center", width=3, style="dim")
        posts_tbl.add_column("Type", justify="center", width=11)
        posts_tbl.add_column("Shortcode", style="bold cyan", width=11)
        posts_tbl.add_column("Likes ♥", justify="right", style="bold red", width=8)
        posts_tbl.add_column("Cmts 💬", justify="right", style="bold yellow", width=8)
        posts_tbl.add_column("Views ▶", justify="right", style="bold blue", width=8)
        posts_tbl.add_column("Date", justify="center", style="dim", width=10)
        posts_tbl.add_column("Caption Preview", style="white")

        for idx, edge in enumerate(edges[:6], 1):
            n = edge.get("node", {}) if isinstance(edge, dict) else {}
            code = get_deep(n, "shortcode", "—")
            raw_type = get_deep(n, "__typename", "").replace("Graph", "").upper()
            typ = "🎬 VIDEO" if "VIDEO" in raw_type or "REEL" in raw_type else ("📚 CAROUSEL" if "SIDE" in raw_type else "📷 PHOTO")
            likes = get_deep(n, "edge_liked_by.count") or get_deep(n, "edge_media_preview_like.count") or 0
            cmts = get_deep(n, "edge_media_to_comment.count", 0)
            views = get_deep(n, "video_view_count", None)
            taken = get_deep(n, "taken_at_timestamp", None)
            cap_edges = get_deep(n, "edge_media_to_caption.edges", []) or []
            cap = get_deep(cap_edges[0], "node.text", "") if cap_edges else ""
            cap_clean = cap.replace("\n", " ").strip()
            if len(cap_clean) > 35:
                cap_clean = cap_clean[:32] + "…"

            posts_tbl.add_row(
                str(idx),
                typ,
                f"[link=https://instagram.com/p/{code}/]{code}[/link]",
                fmt_num(likes),
                fmt_num(cmts),
                fmt_num(views) if views else "—",
                fmt_date(taken),
                cap_clean or "[dim]—[/dim]"
            )
        console.print(posts_tbl)

    # Related Profiles
    if related:
        rel_text = Text("👥 Related Profiles: ", style="bold color(214)")
        rel_items = []
        for r in related[:6]:
            nd = r.get("node", {}) if isinstance(r, dict) else {}
            un = nd.get("username")
            if un:
                rel_items.append(f"[bold cyan]@{un}[/bold cyan]")
        if rel_items:
            rel_text.append(", ".join(rel_items))
            console.print(Panel(rel_text, box=box.ROUNDED, border_style="dim", padding=(0, 2)))

    # Footer Metadata
    footer_text = Text()
    if credits_rem is not None:
        footer_text.append(f"Credits Remaining: {credits_rem:,} ", style="bold green")
    if cached:
        footer_text.append(" • [Cached response]", style="dim yellow")
    if str(footer_text):
        console.print(Align.right(footer_text))
    console.print()


def render_posts(data: Dict[str, Any], handle: str):
    """Render full posts feed in an elegant table."""
    payload = data.get("data", data)
    items = payload.get("items") if isinstance(payload, dict) and "items" in payload else None
    if items is None and isinstance(payload, dict):
        for v in payload.values():
            if isinstance(v, dict) and "items" in v:
                items = v["items"]
                break
    if not items:
        if isinstance(payload, list):
            items = payload
        else:
            items = []

    if not items:
        console.print(Panel(f"[yellow]No public posts found for @{handle} or account is private.[/yellow]", box=box.ROUNDED))
        return

    table = Table(
        title=f"📸 Posts Feed — @{handle} ({len(items)} posts retrieved)",
        box=box.ROUNDED,
        header_style="bold color(214)",
        border_style="color(207)",
        expand=True
    )
    table.add_column("#", justify="center", width=3, style="dim")
    table.add_column("Type", justify="center", width=11)
    table.add_column("Shortcode", style="bold cyan", width=11)
    table.add_column("Likes ♥", justify="right", style="bold red", width=8)
    table.add_column("Cmts 💬", justify="right", style="bold yellow", width=8)
    table.add_column("Plays ▶", justify="right", style="bold blue", width=8)
    table.add_column("Date", justify="center", style="dim", width=10)
    table.add_column("Caption", style="white")

    total_likes = 0
    total_comments = 0

    for idx, item in enumerate(items, 1):
        code = get_deep(item, "code") or get_deep(item, "shortcode") or "—"
        likes = get_deep(item, "like_count", 0)
        cmts = get_deep(item, "comment_count", 0)
        views = get_deep(item, "play_count") or get_deep(item, "view_count") or get_deep(item, "ig_play_count", None)
        taken = get_deep(item, "taken_at", None)
        cap = get_deep(item, "caption.text") or get_deep(item, "caption", "") or ""
        if isinstance(cap, dict):
            cap = cap.get("text", "")
        cap_clean = str(cap).replace("\n", " ").strip()
        if len(cap_clean) > 40:
            cap_clean = cap_clean[:37] + "…"

        mt = get_deep(item, "media_type", 1)
        typ = "🎬 VIDEO" if mt == 2 else ("📚 CAROUSEL" if mt == 8 else "📷 PHOTO")

        total_likes += (likes if isinstance(likes, int) else 0)
        total_comments += (cmts if isinstance(cmts, int) else 0)

        table.add_row(
            str(idx),
            typ,
            f"[link=https://instagram.com/p/{code}/]{code}[/link]",
            fmt_num(likes),
            fmt_num(cmts),
            fmt_num(views) if views else "—",
            fmt_date(taken),
            cap_clean or "[dim]—[/dim]"
        )

    console.print(table)

    avg_likes = total_likes // max(1, len(items))
    avg_cmts = total_comments // max(1, len(items))
    summary_text = Text()
    summary_text.append(f"Feed Averages:  ♥ {avg_likes:,} avg likes  •  💬 {avg_cmts:,} avg comments per post", style="bold cyan")
    console.print(Panel(Align.center(summary_text), box=box.ROUNDED, border_style="dim", padding=(0, 2)))
    console.print()


def render_reels(data: Dict[str, Any], handle: str):
    """Render reels catalog with metrics."""
    payload = data.get("data", data)
    items = payload.get("items") if isinstance(payload, dict) and "items" in payload else None
    if items is None and isinstance(payload, dict):
        for v in payload.values():
            if isinstance(v, dict) and "items" in v:
                items = v["items"]
                break
    if items is None and isinstance(payload, list):
        items = payload
    if not items:
        items = []

    if not items:
        console.print(Panel(f"[yellow]No reels found for @{handle} or account is private.[/yellow]", box=box.ROUNDED))
        return

    table = Table(
        title=f"🎬 Reels & Short Videos — @{handle} ({len(items)} reels retrieved)",
        box=box.ROUNDED,
        header_style="bold color(214)",
        border_style="color(207)",
        expand=True
    )
    table.add_column("#", justify="center", width=3, style="dim")
    table.add_column("Reel Code", style="bold cyan", width=12)
    table.add_column("Plays ▶", justify="right", style="bold green", width=9)
    table.add_column("Likes ♥", justify="right", style="bold red", width=9)
    table.add_column("Cmts 💬", justify="right", style="bold yellow", width=8)
    table.add_column("Duration", justify="center", style="dim", width=9)
    table.add_column("Caption", style="white")

    for idx, item in enumerate(items, 1):
        code = get_deep(item, "code", "—")
        likes = get_deep(item, "like_count", 0)
        cmts = get_deep(item, "comment_count", 0)
        views = get_deep(item, "play_count") or get_deep(item, "view_count", 0)
        duration = get_deep(item, "video_duration", None)
        dur_str = f"{float(duration):.1f}s" if duration else "—"
        cap = get_deep(item, "caption.text") or get_deep(item, "caption", "") or ""
        if isinstance(cap, dict):
            cap = cap.get("text", "")
        cap_clean = str(cap).replace("\n", " ").strip()
        if len(cap_clean) > 40:
            cap_clean = cap_clean[:37] + "…"

        table.add_row(
            str(idx),
            f"[link=https://instagram.com/reel/{code}/]{code}[/link]",
            fmt_num(views),
            fmt_num(likes),
            fmt_num(cmts),
            dur_str,
            cap_clean or "[dim]—[/dim]"
        )

    console.print(table)
    console.print()


def render_tagged(data: Dict[str, Any], handle: str):
    """Render tagged posts catalog."""
    payload = data.get("data", data)
    posts = payload.get("posts") if isinstance(payload, dict) and "posts" in payload else None
    if posts is None:
        if isinstance(payload, dict) and "items" in payload:
            posts = payload["items"]
        elif isinstance(payload, list):
            posts = payload
        else:
            posts = []

    if not posts:
        console.print(Panel(f"[yellow]No tagged posts found for @{handle} or account is private.[/yellow]", box=box.ROUNDED))
        return

    table = Table(
        title=f"🏷️ Tagged Posts — @{handle} ({len(posts)} tagged media)",
        box=box.ROUNDED,
        header_style="bold color(214)",
        border_style="color(207)",
        expand=True
    )
    table.add_column("#", justify="center", width=3, style="dim")
    table.add_column("Posted By", style="bold cyan", width=18)
    table.add_column("Shortcode", style="bold white", width=14)
    table.add_column("Likes ♥", justify="right", style="bold red", width=9)
    table.add_column("Cmts 💬", justify="right", style="bold yellow", width=8)
    table.add_column("Instagram Link", style="blue underline")

    for idx, p in enumerate(posts, 1):
        code = get_deep(p, "code") or get_deep(p, "shortcode", "—")
        likes = get_deep(p, "like_count", 0)
        cmts = get_deep(p, "comment_count", 0)
        owner = get_deep(p, "user.username") or get_deep(p, "owner.username", "—")

        table.add_row(
            str(idx),
            f"@{owner}",
            code,
            fmt_num(likes),
            fmt_num(cmts),
            f"https://instagram.com/p/{code}/" if code != "—" else "—"
        )

    console.print(table)
    console.print()


def render_highlights(data: Dict[str, Any], handle: str):
    """Render highlights & story albums."""
    payload = data.get("data", data)
    hls = payload.get("highlights") if isinstance(payload, dict) and "highlights" in payload else None
    if hls is None and isinstance(payload, dict):
        for v in payload.values():
            if isinstance(v, list) and v and isinstance(v[0], dict) and "title" in v[0]:
                hls = v
                break
    if not hls:
        hls = []

    if not hls:
        console.print(Panel(f"[yellow]No story highlights found for @{handle}.[/yellow]", box=box.ROUNDED))
        return

    table = Table(
        title=f"🌟 Story Highlights — @{handle} ({len(hls)} albums)",
        box=box.ROUNDED,
        header_style="bold color(214)",
        border_style="color(207)",
        expand=True
    )
    table.add_column("#", justify="center", width=3, style="dim")
    table.add_column("Highlight Title", style="bold color(214)", width=22)
    table.add_column("Highlight ID", style="cyan", width=18)
    table.add_column("Media Count", justify="center", style="green", width=12)
    table.add_column("Cover Image URL", style="dim")

    for idx, hl in enumerate(hls, 1):
        title = get_deep(hl, "title", "Untitled")
        hid = get_deep(hl, "id", "—")
        count = get_deep(hl, "media_count", "—")
        cover = get_deep(hl, "cover_media.cropped_image_version.url") or get_deep(hl, "cover_media_crop_rect") or "—"
        cover_preview = f"{str(cover)[:45]}..." if cover != "—" else "—"

        table.add_row(
            str(idx),
            f"✨ {title}",
            str(hid),
            str(count),
            cover_preview
        )

    console.print(table)
    console.print()


def render_basic(data: Dict[str, Any]):
    """Render fast lightweight basic profile card."""
    payload = data.get("data", data)
    user = payload
    if isinstance(payload, dict) and "username" not in payload:
        for v in payload.values():
            if isinstance(v, dict) and "username" in v:
                user = v
                break

    username = get_deep(user, "username", "—")
    full = get_deep(user, "full_name", "—")
    foll = get_deep(user, "follower_count", 0)
    foll2 = get_deep(user, "following_count", 0)
    posts = get_deep(user, "media_count", 0)
    verified = get_deep(user, "is_verified", False)
    priv = get_deep(user, "is_private", False)
    bio = get_deep(user, "biography", "")

    header = Text()
    header.append(f"@{username}", style="bold cyan")
    header.append(f" ({full}) ", style="bold white")
    if verified:
        header.append("[✔ VERIFIED] ", style="bold cyan")
    if priv:
        header.append("[🔒 PRIVATE] ", style="bold yellow")
    else:
        header.append("[PUBLIC] ", style="bold green")

    stats = Table(box=box.SIMPLE, show_header=True, expand=True)
    stats.add_column("Followers", justify="center", style="bold cyan")
    stats.add_column("Following", justify="center", style="bold green")
    stats.add_column("Posts", justify="center", style="bold yellow")
    stats.add_row(fmt_num_full(foll), fmt_num_full(foll2), fmt_num_full(posts))

    content = Group(
        header,
        Text(""),
        Text(f"Bio: {bio}" if bio else "No bio.", style="italic"),
        Text(""),
        stats
    )

    console.print(Panel(content, title="⚡ Basic Profile Summary", box=box.ROUNDED, border_style="cyan", padding=(1, 2)))
    console.print()


# ── Interactive Prompts & Exporters ─────────────────────────────────────

def prompt_save_data(data: Dict[str, Any], handle: str):
    """Prompt user with option to save retrieved data to JSON."""
    try:
        should_save = Confirm.ask("[bold yellow]💾 Would you like to export this data to a JSON file?[/bold yellow]", default=False)
        if not should_save:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"{handle}_instafetch_{timestamp}.json"
        filename = Prompt.ask("Enter output filename", default=default_filename).strip() or default_filename

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        console.print(f"[bold green]✓ Successfully exported to:[/bold green] [cyan]{filename}[/cyan]\n")
    except Exception as e:
        console.print(f"[bold red]✗ Failed to export file: {e}[/bold red]\n")


def display_menu():
    """Render interactive main menu with clean modern styling."""
    menu_table = Table(box=box.MINIMAL, show_header=False, expand=True, padding=(0, 1))
    menu_table.add_column("Option", style="bold color(214)", width=6, justify="center")
    menu_table.add_column("Action", style="bold white", width=22)
    menu_table.add_column("Description", style="dim")

    menu_table.add_row("[1]", "👤 Profile Overview", "Full metadata, bio, badges, metrics & recent feed")
    menu_table.add_row("[2]", "⚡ Basic Profile", "Fast, lightweight summary card")
    menu_table.add_row("[3]", "📸 Posts Feed", "Comprehensive timeline posts & engagement")
    menu_table.add_row("[4]", "🎬 Reels Catalog", "Short videos, play counts & durations")
    menu_table.add_row("[5]", "🏷️ Tagged Posts", "Photos & videos user is tagged in")
    menu_table.add_row("[6]", "🌟 Story Highlights", "Saved story albums & cover previews")
    menu_table.add_row("[7]", "🚀 Full Suite", "Complete multi-module deep inspection")
    menu_table.add_row("[8]", "📜 Disclaimer & Policy", "Full legal, privacy & API guidelines breakdown")
    menu_table.add_row("[9]", "🌐 Open in Browser", "Open Instagram profile directly in browser")
    menu_table.add_row("[10]", "🔑 Update API Key", "Change active ScrapeCreators credentials")
    menu_table.add_row("[0]", "🚪 Exit", "Quit InstaFetch")

    console.print(Panel(menu_table, title="[bold color(207)]⚡ InstaFetch Action Menu[/bold color(207)]", box=box.ROUNDED, border_style="color(207)"))


# ── Main Interactive Flow ───────────────────────────────────────────────

def interactive_session(initial_api_key: str):
    """Main interactive TUI loop."""
    current_key = initial_api_key
    client = InstaClient(current_key)
    last_handle = "instagram"

    while True:
        clear_screen()
        show_banner()
        show_disclaimer()
        display_menu()

        try:
            choice = Prompt.ask("\n[bold color(207)]Select an option [0-10][/bold color(207)]", default="1").strip()
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[dim]Bye — InstaFetch by {AUTHOR}[/dim]")
            break

        if choice == "0":
            console.print(f"\n[bold color(207)]Thank you for using InstaFetch by {AUTHOR}![/bold color(207)]\n")
            break

        if choice == "8":
            clear_screen()
            show_banner()
            show_detailed_disclaimer()
            try:
                Prompt.ask("[dim]Press Enter to return to main menu...[/dim]", default="")
            except (KeyboardInterrupt, EOFError):
                break
            continue

        if choice == "10" or choice.lower() == "k":
            new_key = Prompt.ask("[bold cyan]Paste new ScrapeCreators API Key[/bold cyan]").strip()
            if new_key:
                current_key = new_key
                client = InstaClient(current_key)
                console.print("[bold green]✓ API Key updated successfully![/bold green]")
                time.sleep(1)
            continue

        if choice not in ("1", "2", "3", "4", "5", "6", "7", "9"):
            console.print("[bold red]⚠ Invalid choice! Please select 0 to 10.[/bold red]")
            time.sleep(1)
            continue

        # Ask handle
        raw_handle = Prompt.ask(f"[bold cyan]Instagram Handle[/bold cyan]", default=last_handle).strip()
        handle = clean_handle(raw_handle)
        if not handle:
            console.print("[bold red]⚠ Invalid Instagram handle provided.[/bold red]")
            time.sleep(1.2)
            continue
        last_handle = handle

        if choice == "9":
            url = f"https://instagram.com/{handle}"
            console.print(f"[green]Opening {url} in your default browser...[/green]")
            try:
                webbrowser.open(url)
            except Exception as e:
                console.print(f"[red]Could not open browser: {e}[/red]")
            time.sleep(1.5)
            continue

        # Data collection
        clear_screen()
        show_banner()
        aggregated_data: Dict[str, Any] = {
            "handle": handle,
            "inspected_at": datetime.now(timezone.utc).isoformat(),
            "tool": TOOL_NAME,
            "version": VERSION,
            "author": AUTHOR,
        }

        try:
            if choice == "1":
                with console.status(f"[bold color(207)]Fetching full profile for @{handle}...[/bold color(207)]", spinner="dots"):
                    d, _, _ = client.get_profile(handle)
                aggregated_data["profile"] = d
                render_profile(d)
                prompt_save_data(aggregated_data, handle)

            elif choice == "2":
                # Basic profile needs numeric user ID
                with console.status(f"[bold cyan]Resolving user ID for @{handle}...[/bold cyan]", spinner="dots"):
                    prof, _, _ = client.get_profile(handle)
                    uid = extract_user_id(prof)

                if not uid:
                    raise RuntimeError(f"Could not resolve numeric User ID for @{handle}")

                with console.status(f"[bold cyan]Fetching basic profile stats...[/bold cyan]", spinner="dots"):
                    d, _, _ = client.get_basic_profile(uid)

                aggregated_data["basic"] = d
                render_basic(d)
                prompt_save_data(aggregated_data, handle)

            elif choice == "3":
                with console.status(f"[bold color(214)]Fetching posts feed for @{handle}...[/bold color(214)]", spinner="dots"):
                    d, _, _ = client.get_posts(handle)
                aggregated_data["posts"] = d
                render_posts(d, handle)
                prompt_save_data(aggregated_data, handle)

            elif choice == "4":
                with console.status(f"[bold magenta]Fetching reels for @{handle}...[/bold magenta]", spinner="dots"):
                    d, _, _ = client.get_reels(handle)
                aggregated_data["reels"] = d
                render_reels(d, handle)
                prompt_save_data(aggregated_data, handle)

            elif choice == "5":
                with console.status(f"[bold cyan]Resolving User ID for @{handle}...[/bold cyan]", spinner="dots"):
                    prof, _, _ = client.get_profile(handle)
                    uid = extract_user_id(prof)

                if not uid:
                    raise RuntimeError(f"Could not resolve numeric User ID for @{handle}")

                with console.status(f"[bold cyan]Fetching tagged posts...[/bold cyan]", spinner="dots"):
                    d, _, _ = client.get_tagged(uid)

                aggregated_data["tagged"] = d
                render_tagged(d, handle)
                prompt_save_data(aggregated_data, handle)

            elif choice == "6":
                with console.status(f"[bold yellow]Fetching story highlights for @{handle}...[/bold yellow]", spinner="dots"):
                    d, _, _ = client.get_highlights(handle)
                aggregated_data["highlights"] = d
                render_highlights(d, handle)
                prompt_save_data(aggregated_data, handle)

            elif choice == "7":
                # Full Suite
                with console.status(f"[bold color(207)]Running Full Suite inspection for @{handle}...[/bold color(207)]", spinner="dots"):
                    prof_data, _, _ = client.get_profile(handle)
                    aggregated_data["profile"] = prof_data
                    uid = extract_user_id(prof_data)

                render_profile(prof_data)

                # Posts
                try:
                    with console.status("[bold color(214)]Fetching timeline posts...[/bold color(214)]", spinner="dots"):
                        posts_data, _, _ = client.get_posts(handle)
                    aggregated_data["posts"] = posts_data
                    render_posts(posts_data, handle)
                except Exception as e:
                    console.print(f"[yellow]⚠ Posts module: {e}[/yellow]")

                # Reels
                try:
                    with console.status("[bold magenta]Fetching reels...[/bold magenta]", spinner="dots"):
                        reels_data, _, _ = client.get_reels(handle)
                    aggregated_data["reels"] = reels_data
                    render_reels(reels_data, handle)
                except Exception as e:
                    console.print(f"[yellow]⚠ Reels module: {e}[/yellow]")

                # Highlights
                try:
                    with console.status("[bold yellow]Fetching story highlights...[/bold yellow]", spinner="dots"):
                        hl_data, _, _ = client.get_highlights(handle)
                    aggregated_data["highlights"] = hl_data
                    render_highlights(hl_data, handle)
                except Exception as e:
                    console.print(f"[yellow]⚠ Highlights module: {e}[/yellow]")

                # Tagged
                if uid:
                    try:
                        with console.status("[bold cyan]Fetching tagged media...[/bold cyan]", spinner="dots"):
                            tag_data, _, _ = client.get_tagged(uid)
                        aggregated_data["tagged"] = tag_data
                        render_tagged(tag_data, handle)
                    except Exception as e:
                        console.print(f"[yellow]⚠ Tagged module: {e}[/yellow]")

                prompt_save_data(aggregated_data, handle)

        except RuntimeError as e:
            console.print(Panel(f"[bold red]Error:[/bold red] {e}", title="[bold red]Operation Failed[/bold red]", box=box.ROUNDED, border_style="red"))
        except Exception as e:
            console.print(Panel(f"[bold red]Unexpected Error:[/bold red] {e}", title="[bold red]Error[/bold red]", box=box.ROUNDED, border_style="red"))

        # Ask to return to menu
        try:
            Prompt.ask("[dim]Press Enter to return to main menu...[/dim]", default="")
        except (KeyboardInterrupt, EOFError):
            break


# ── Entry Point & CLI Parser ────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME.lower(),
        description=f"{TOOL_NAME} v{VERSION} by {AUTHOR} — Clean Instagram Intelligence & Profile Inspector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python InstaFetch.py -u instagram
  python InstaFetch.py -u virat.kohli --all -o report.json
  python InstaFetch.py -u zuck --posts --reels --json
  python InstaFetch.py --disclaimer
  
Free API Keys & Documentation:
  https://app.scrapecreators.com (10k free credits)
        """
    )
    parser.add_argument("--handle", "-u", help="Target Instagram username or profile URL")
    parser.add_argument("--api-key", help="ScrapeCreators API key (overrides script key & ENV)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON to stdout instead of UI tables")
    parser.add_argument("--output", "-o", help="File path to save the JSON result")
    parser.add_argument("--trim", action="store_true", help="Trim response payload for lightweight output")
    parser.add_argument("--cache", help="Max cache age for responses (e.g. 1d, 3d, 7d)")
    parser.add_argument("--no-color", action="store_true", help="Disable rich ANSI color rendering")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print debug URLs and network latency")
    parser.add_argument("--posts", action="store_true", help="Include user's posts feed")
    parser.add_argument("--reels", action="store_true", help="Include user's reels")
    parser.add_argument("--tagged", action="store_true", help="Include tagged posts")
    parser.add_argument("--highlights", action="store_true", help="Include story highlights")
    parser.add_argument("--basic", action="store_true", help="Include basic profile metrics")
    parser.add_argument("--all", action="store_true", help="Fetch complete inspection suite (profile, posts, reels, tagged, highlights)")
    parser.add_argument("--disclaimer", action="store_true", help="Display comprehensive legal, privacy, and API disclaimer")
    parser.add_argument("--open-browser", action="store_true", help="Open profile in default browser")
    parser.add_argument("--version", action="version", version=f"{TOOL_NAME} v{VERSION} by {AUTHOR}")

    args = parser.parse_args()

    if args.no_color:
        console.no_color = True

    if args.disclaimer:
        clear_screen()
        show_banner()
        show_detailed_disclaimer()
        sys.exit(0)

    if args.all:
        args.posts = args.reels = args.tagged = args.highlights = args.basic = True

    api_key = load_api_key(args.api_key)

    # If handle provided on CLI -> Direct Headless / Scripting Mode
    if args.handle:
        handle = clean_handle(args.handle)
        if not api_key:
            console.print("[bold red]✗ No API key provided.[/bold red] Set API_KEY at top of script, use [cyan]--api-key[/cyan], or set [cyan]SCRAPECREATORS_API_KEY[/cyan] environment variable.")
            sys.exit(1)

        client = InstaClient(api_key)

        if args.open_browser:
            webbrowser.open(f"https://instagram.com/{handle}")

        try:
            aggregated: Dict[str, Any] = {
                "handle": handle,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "tool": TOOL_NAME,
                "version": VERSION,
                "author": AUTHOR,
            }

            # Profile is always fetched first
            profile_data, _, _ = client.get_profile(handle, trim=args.trim, cache_max_age=args.cache, verbose=args.verbose)
            aggregated["profile"] = profile_data
            uid = extract_user_id(profile_data)

            if args.posts:
                posts_data, _, _ = client.get_posts(handle, verbose=args.verbose)
                aggregated["posts"] = posts_data

            if args.reels:
                reels_data, _, _ = client.get_reels(handle, verbose=args.verbose)
                aggregated["reels"] = reels_data

            if args.highlights:
                hl_data, _, _ = client.get_highlights(handle, verbose=args.verbose)
                aggregated["highlights"] = hl_data

            if args.tagged and uid:
                tag_data, _, _ = client.get_tagged(uid, verbose=args.verbose)
                aggregated["tagged"] = tag_data

            if args.basic and uid:
                basic_data, _, _ = client.get_basic_profile(uid, verbose=args.verbose)
                aggregated["basic"] = basic_data

            # JSON Output Mode
            if args.json:
                json_str = json.dumps(aggregated, indent=2, ensure_ascii=False)
                if args.output:
                    out_path = args.output
                    if os.path.isdir(out_path):
                        out_path = os.path.join(out_path, f"{handle}.json")
                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(json_str)
                    console.print(f"[green]Saved JSON output to {out_path}[/green]")
                else:
                    print(json_str)
                return

            # Rich Visual CLI Mode
            clear_screen()
            show_banner()
            render_profile(profile_data)

            if args.posts and "posts" in aggregated:
                render_posts(aggregated["posts"], handle)

            if args.reels and "reels" in aggregated:
                render_reels(aggregated["reels"], handle)

            if args.highlights and "highlights" in aggregated:
                render_highlights(aggregated["highlights"], handle)

            if args.tagged and "tagged" in aggregated:
                render_tagged(aggregated["tagged"], handle)

            if args.basic and "basic" in aggregated:
                render_basic(aggregated["basic"])

            if args.output:
                out_path = args.output
                if os.path.isdir(out_path):
                    out_path = os.path.join(out_path, f"{handle}_instafetch.json")
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(aggregated, f, indent=2, ensure_ascii=False)
                console.print(f"[bold green]✓ Output successfully saved to:[/bold green] [cyan]{out_path}[/cyan]\n")

        except RuntimeError as e:
            console.print(f"[bold red]✗ {e}[/bold red]")
            sys.exit(1)

    else:
        # Interactive TUI Mode
        if not api_key:
            clear_screen()
            show_banner()
            show_disclaimer()
            console.print("[bold yellow]No ScrapeCreators API key detected.[/bold yellow]")
            console.print("[dim]Get your free 10,000 credits key at: https://app.scrapecreators.com[/dim]\n")
            try:
                api_key = Prompt.ask("[bold cyan]Paste your ScrapeCreators API Key (or press Enter to exit)[/bold cyan]").strip()
            except (KeyboardInterrupt, EOFError):
                sys.exit(0)
            if not api_key:
                sys.exit(0)

        interactive_session(api_key)


if __name__ == "__main__":
    main()
