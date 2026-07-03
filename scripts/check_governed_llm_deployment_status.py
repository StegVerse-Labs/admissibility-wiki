#!/usr/bin/env python3
"""Check governed LLM deployed-page status without mutating state.

This script distinguishes local Site wiring from deployed GitHub Pages status. It
performs HTTP HEAD requests against the expected public pages and reports PASS
only when each page returns a successful response.
"""

from __future__ import annotations

from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PAGES = (
    "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-reconstructive-search",
    "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-activation-map",
    "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-overview",
    "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-verification",
    "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-site-verification",
    "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-deployment-status",
    "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-archive-handoff",
)


def check_url(url: str) -> tuple[bool, str]:
    request = Request(url, method="HEAD")
    try:
        with urlopen(request, timeout=15) as response:
            status = getattr(response, "status", None) or response.getcode()
    except HTTPError as exc:
        return False, "{} -> HTTP {}".format(url, exc.code)
    except URLError as exc:
        return False, "{} -> {}".format(url, exc.reason)
    except TimeoutError:
        return False, "{} -> timeout".format(url)

    if 200 <= int(status) < 400:
        return True, "{} -> HTTP {}".format(url, status)
    return False, "{} -> HTTP {}".format(url, status)


def main() -> int:
    failures = []
    for url in PAGES:
        ok, message = check_url(url)
        print(message)
        if not ok:
            failures.append(message)

    if failures:
        print("GOVERNED LLM DEPLOYMENT: PENDING - deployed pages not fully confirmed")
        return 1

    print("GOVERNED LLM DEPLOYMENT: PASS - deployed pages reachable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
