# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Security

- Replaced the raw `apiKey === expected || bearer === expected` comparison in `authOk` with a
  constant-time `timingSafeEqual` helper on both paths, closing a timing side-channel on the
  auth check guarding every admin/data-management endpoint (`/programs`, `/affiliates`,
  `/links`, `/payouts`, `/analytics/*`, `/export`, `/activity`, etc.).
- Added rate limiting (30 req/min per IP) to `GET /dashboard/:refCode`, which was previously
  unlimited despite being unauthenticated and returning an affiliate's name, financial balances,
  and recent conversions/links keyed only by an 8-character ref code -- closing a brute-force
  enumeration path onto affiliate PII and financial data.
- Untracked `.wrangler/cache/wrangler-account.json` (a local Cloudflare account-id cache file
  that had been committed despite `.wrangler/` already being in `.gitignore` -- git does not
  retroactively ignore an already-tracked path).

### Added

- `package.json` and `tsconfig.json` (neither existed; the repository had no dependency
  manifest, so `tsc`/`npm test` could not previously run at all).
- `tests/pure-functions.test.mjs`: 9 real unit tests, importing and executing `sanitize`,
  `timingSafeEqual`, and `ipHash` directly from `src/index.ts` via Node's native TypeScript
  support (Node >= 22.6; CI pins Node 24).
- `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`.
- Hosted CI (`.github/workflows/ci.yml`): runs `npm test` (typecheck + unit tests) on every push
  and pull request.
- Issue templates (bug report, feature request) and a pull-request template.
- `.echo/{apps.json,certification.json,sdk.json}` for ECHO Certification Forge and GitHub App
  Suite enrollment; `sdk.json` declares the 12 real `echo.affiliate.*` capabilities already
  registered in `arcanum_sdk.sdk_capabilities`. `scripts/certforge_journey.py` critical journey
  (structural integrity via count-based bracket balance -- deliberately not a full tokenizer,
  since template-literal interpolation false-failed a string-state version of the check during
  development -- plus regression guards on both security fixes above; verified locally by
  deliberately reintroducing each bug and confirming the journey fails, then restoring the fix).
- This CHANGELOG and a README (the repository previously had no README at all).

## [Prior history]

- Add `ctx.waitUntil()` to prevent silent data loss from fire-and-forget async work.
- Repair two dead-code corruption bugs in the route handler.
- Add a global error handler for unhandled exceptions.
- Add an unauthenticated root route handler.
- Auth hardening, D1 error handling, service bindings.
- Add structured logging (`slog()`).
- Add Bearer token support, fail-closed auth.
