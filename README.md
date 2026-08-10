# Echo Affiliate

AI-powered affiliate and referral program management -- a Cloudflare Worker backed by D1
(database), KV (rate-limit/cache state), and service bindings to `echo-engine-runtime`,
`echo-shared-brain`, and `echo-email-sender`. Runs a daily scheduled analytics rollup via a
Worker Cron Trigger.

## Endpoints

| Access | Method | Path | Description |
|---|---|---|---|
| Public | GET | `/` , `/health` | Service info / health check |
| Public, rate-limited | GET | `/go/:slug` | Affiliate link click tracking + redirect |
| Public, rate-limited | GET | `/join/:slug` | Affiliate program signup landing page |
| Public, rate-limited | POST | `/apply` | Affiliate application |
| Public, rate-limited | POST | `/convert` | Record a conversion (webhook) |
| Public, rate-limited | GET | `/dashboard/:refCode` | An affiliate's own stats, keyed by ref code |
| Authenticated | GET/POST/PATCH/DELETE | `/programs`, `/affiliates`, `/links`, `/conversions`, `/payouts`, `/creatives`, `/fraud-rules`, `/analytics/*`, `/ai/insights`, `/export`, `/activity` | Program/affiliate/payout management and reporting |

## Authentication

Every endpoint below the `AUTH REQUIRED BELOW` marker in `src/index.ts` requires `X-Echo-API-Key`
or an `Authorization: Bearer` token, compared to `env.ECHO_API_KEY` in constant time. Public
endpoints (click tracking, applications, conversions, the per-affiliate dashboard) are
individually rate-limited per client IP via KV, since they take unauthenticated traffic by
design.

## Verify

```powershell
npm install
npm test
```

## Security

See [SECURITY.md](SECURITY.md) to report a vulnerability -- never as a public issue.
`GET /dashboard/:refCode` is public by design (an affiliate's own link to their own stats) and
is rate-limited rather than authenticated; it returns affiliate PII and financial balances, so
ref codes should be treated as bearer-adjacent secrets in practice.

## License

See [LICENSE](LICENSE). Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md).
