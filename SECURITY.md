# Security policy

Echo Affiliate is a Cloudflare Worker (D1 + KV + service bindings) that tracks affiliate clicks,
conversions, and commission payouts, and exposes affiliate PII and financial balances through an
unauthenticated per-affiliate dashboard endpoint keyed by a ref code. Admin/data-management
endpoints (`/programs`, `/affiliates`, `/links`, `/payouts`, `/analytics/*`, `/export`, etc.)
require `X-Echo-API-Key` or a Bearer token, checked in constant time.

## Supported version

Security fixes target the current `main` branch and the currently deployed Worker release.
Historical commits are retained for evidence and are not patched in place.

## Report a vulnerability

Do not open a public issue for a suspected vulnerability. Send a private report to
`security@echo-op.com` with:

- affected endpoint and exact revision;
- reproduction steps and expected impact;
- whether the `X-Echo-API-Key`/Bearer authentication boundary, the rate limits protecting
  `/go/`, `/apply`, `/convert`, and `/dashboard/:refCode` from abuse or enumeration, or payout
  calculation logic may be involved;
- safe contact details for follow-up.

Never include a live `ECHO_API_KEY`, a real affiliate ref code, or customer/affiliate financial
data in a report.
