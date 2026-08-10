## Objective

Describe the affiliate/referral behavior this change adds or fixes.

## Evidence

- Exact source revision:
- Test output (`npm test`):
- Negative paths exercised (missing/invalid key, rate-limit boundary):
- Hosted CI run:

## Security and release impact

- [ ] No secrets (`ECHO_API_KEY`), real affiliate ref codes, or affiliate/customer financial
      data are included.
- [ ] The `X-Echo-API-Key`/Bearer authentication boundary is unchanged, or the change is called
      out explicitly.
- [ ] Any change to a rate limit (`/go/`, `/apply`, `/convert`, `/dashboard/:refCode`) is called
      out explicitly.
- [ ] Staging-first deployment and rollback implications are documented.
