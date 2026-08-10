"""Critical journey for the ECHO Certification Forge.

The Forge runs this argv (declared in ``.echo/certification.json``) inside its
isolated ``python:3.12-alpine`` sandbox, against the exact acquired commit,
with no network and no project dependencies installed -- there is no Node
here, so the Worker itself cannot actually run. The full behavioural suite
(``npm test`` -- typecheck plus real unit tests, imported and executed
against the actual ``src/index.ts`` via Node's native TypeScript support)
runs in CI on this same commit; this journey proves the artifact the Forge
actually acquired is the intact, complete Worker source -- not that it
currently boots.

This repository is TypeScript-only (a single Cloudflare Worker); this
journey therefore checks structural and textual invariants rather than
parsing Python.

Checks:
  1. The critical surfaces exist -- the Worker entrypoint, its test file,
     the pinned Node dependency manifest, and the TypeScript config.
  2. ``src/index.ts``'s bracket counts are balanced -- a cheap, tokenizer-free
     corruption/truncation check. This counts raw characters rather than
     parsing tokens (so it does not attempt to special-case template-literal
     interpolation or regex-literal character classes correctly); it cannot
     prove the file is valid TypeScript, only that it was not truncated or
     grossly corrupted in transit. Real syntax validity is proven by `tsc
     --noEmit` in `npm test` (CI), which this sandbox cannot run.
  3. No install-lifecycle scripts have crept into ``package.json``
     (release-strict.v2 treats them as a supply-chain vector).
  4. No hardcoded secret-shaped literals in the acquired source.
  5. The auth check calls the constant-time comparison helper on both the
     API-key and Bearer paths, rather than a raw ``===`` -- a regression
     here reintroduces a timing side-channel on every request.
  6. The unauthenticated ``/dashboard/:refCode`` route (returns affiliate
     PII and financial balances keyed only by a guessable ref code) still
     calls ``rateLimit`` before querying the database -- a regression here
     reopens brute-force enumeration of affiliate data.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from typing import NoReturn

CRITICAL_SURFACES = (
    "src/index.ts",
    "tests/pure-functions.test.mjs",
    "package.json",
    "tsconfig.json",
)

INSTALL_LIFECYCLE_HOOKS = ("preinstall", "install", "postinstall", "prepare")

SECRET_LITERAL_PATTERN = re.compile(
    r'(?:api_key|secret|password|token)\s*=\s*["\'][a-zA-Z0-9_\-]{16,}["\']',
    re.IGNORECASE,
)

BALANCE_PAIRS = {"(": ")", "{": "}", "[": "]"}


def _fail(message: str) -> NoReturn:
    print(f"ECHO_AFFILIATE_CRITICAL_JOURNEY_FAILED: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_critical_surfaces() -> None:
    for surface in CRITICAL_SURFACES:
        if not pathlib.Path(surface).exists():
            _fail(f"missing critical surface: {surface}")


def _source_text() -> str:
    return pathlib.Path("src/index.ts").read_text(encoding="utf-8")


def check_index_ts_balanced() -> None:
    # Deliberately NOT a JS/TS tokenizer: template-literal interpolation and
    # regex-literal character classes make correct bracket-nesting detection
    # without a real parser unreliable (confirmed while writing this check --
    # a string-state version of this function false-failed on this file's
    # own template literals). Raw counts still catch the actual threat model
    # here (truncation/corruption of the acquired source in transit).
    text = _source_text()
    for open_ch, close_ch in BALANCE_PAIRS.items():
        opens, closes = text.count(open_ch), text.count(close_ch)
        if opens != closes:
            _fail(
                f"src/index.ts has mismatched '{open_ch}'/'{close_ch}' counts "
                f"({opens} vs {closes}) -- possible truncation or corruption"
            )


def check_no_install_hooks() -> None:
    manifest = pathlib.Path("package.json")
    try:
        scripts = json.loads(manifest.read_text(encoding="utf-8")).get("scripts", {})
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        _fail(f"package.json is not valid JSON: {exc}")
    present = sorted(hook for hook in INSTALL_LIFECYCLE_HOOKS if hook in scripts)
    if present:
        _fail(f"package.json reintroduced install-lifecycle script(s): {', '.join(present)}")


def check_no_hardcoded_secrets() -> None:
    match = SECRET_LITERAL_PATTERN.search(_source_text())
    if match:
        _fail(f"src/index.ts contains a hardcoded secret-shaped literal: {match.group(0)[:40]}...")


def check_constant_time_auth() -> None:
    text = _source_text()
    if "timingSafeEqual(apiKey" not in text or "timingSafeEqual(bearer" not in text:
        _fail("authOk no longer calls timingSafeEqual on both the API-key and Bearer paths")
    if re.search(r"apiKey\s*===\s*expected|bearer\s*===\s*expected", text):
        _fail("authOk regressed to a raw === comparison")


def check_dashboard_rate_limited() -> None:
    text = _source_text()
    match = re.search(r"p\.startsWith\('/dashboard/'\)\)\s*\{(.*?)\n    \}\n", text, re.DOTALL)
    if not match:
        _fail("could not locate the /dashboard/:refCode route handler to check its rate limit")
    if "rateLimit(env, `dash:" not in match.group(1):
        _fail("/dashboard/:refCode no longer rate-limits before returning affiliate PII/financial data")


def main() -> None:
    check_critical_surfaces()
    check_index_ts_balanced()
    check_no_install_hooks()
    check_no_hardcoded_secrets()
    check_constant_time_auth()
    check_dashboard_rate_limited()
    print(
        "ECHO_AFFILIATE_CRITICAL_JOURNEY_OK "
        f"critical_surfaces={len(CRITICAL_SURFACES)} "
        "install_hooks=0 hardcoded_secrets=0 constant_time_auth=1 dashboard_rate_limited=1"
    )


if __name__ == "__main__":
    main()
