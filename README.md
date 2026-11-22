# Sybilwall Gate — offline observation diagnostic

This repository contains a **limited, deterministic local diagnostic** for counts of accepted and rejected peer observations. It is **not** a Sybil-resistance implementation, a production network firewall, a peer-identity verification system, an authenticated network monitor, a PQC implementation, or FIPS/TLS certification.

## Scope and usage

```bash
cargo test --offline
cargo run --offline -- inspect 9 1
python -m unittest discover -s tests -p 'test_*.py' -v
```

The command emits `OFFLINE_DIAGNOSTIC_ONLY rejection_bps=<integer> disposition=<OBSERVE|REVIEW>`. The disposition is an **illustrative threshold** on rejection ratio (at least 50% is `REVIEW`), not an authenticated Sybil verdict. Counts must be nonnegative unsigned 64-bit integers, nonzero in total, and must not overflow when added. Invalid inputs fail with nonzero exit status. No network, wallets, secrets, paid RPCs, or blockchain deployments are used.

## Reality and release gates

The GitHub Actions workflows compile and test the actual Rust executable, run adversarial subprocess regressions, fail on corrupted Python test files, and perform initialized Python CodeQL analysis. Green CI on this limited diagnostic does **not** certify a production Sybil firewall.

Remaining work: signed/authenticated peer observations, identity and source diversity modeling, persistence and replay controls, adaptive adversarial tests, realistic network integration, independent security review, and release sign-off. Until those are implemented and evidenced: **SECURITY_APPROVED = false; DEPLOYMENT_READY = false**.

Previous README claims of live QuickNode connectivity, FIPS 203/204 cryptography, a 100/100 score, and verified treasury/escrow operations were unsupported by executable evidence and have been withdrawn.
