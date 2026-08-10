# Contributing

Thank you for improving Echo Affiliate. This is a public, proprietary infrastructure project:
contributions are welcome for review, but repository visibility does not grant a general use or
redistribution license.

## Development path

1. Open an issue describing the affiliate/referral behavior being changed.
2. Create a focused branch from current `main`.
3. Add a failing test before changing authentication, rate limiting, or payout/commission logic.
4. Validate before opening a pull request:

   ```powershell
   npm install
   npm test
   ```

5. Open a pull request using the repository template and include exact test output.

## Pull-request requirements

- No secrets (`ECHO_API_KEY`), real affiliate ref codes, or affiliate/customer financial data
  are included.
- No stubs, placeholders, skipped security checks, or self-asserted readiness.
- Changes to the authentication boundary or to any rate limit are called out explicitly in the
  pull request description.
