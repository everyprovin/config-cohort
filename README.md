# ConfigCohort

ConfigCohort is an AI-assisted, MIT-licensed prototype for explaining the smallest weighted change that makes a declared Boolean feature policy consistent. GenLayer fetches a commit-pinned public policy, verifies exact source bytes, independently enumerates all assignments and records an owner-confirmed result. The inputs are synthetic feature flags; no real infrastructure, production configuration or personal data is modified.

## Recorded live result

The application is [https://everyprovin.github.io/config-cohort/](https://everyprovin.github.io/config-cohort/); the existing contract is `0x5f2D1d6515659DD53A19f4BEea2F25d24333c3df` on **GenLayer Studio, chain61999**. Using public frontend revision**002**, commit `471f86a06729d5ed6ba2835267ffd376abe17b1b`, one operator completed **Lock -> Derive -> Confirm** through the normal wallet workflow. Record **ConfigH1022A** is **CONFIRMED, revision2**.

The exact result is **SAT**, assignment `audit=false, cache=true, preview=false, telemetry=false`, bits **0100**, minimum flip cost **3**, changes **cache and preview**. There are **7** satisfying models among **16** complete assignments. Clause witnesses are **cache**, **!preview**, **!telemetry**, **!telemetry**. The certificate is `7b27227609082251795cdce809268f85fb09668a458807e5e6be713d214c1b87`.

| Operation | Original transaction hash |
| --- | --- |
| lock_source | `0x584c4a196073749e8243ba696ee32b267d8734b94bb089560c786a67522f978f` |
| derive | `0xd0bdb3c8eef05f78946b4d4d485cbcb7a6154d869827643e471db942dc3801a6` |
| confirm | `0x534bdcfbcaf4c16631b5abe91660f6ed78e804630b609b6972f2ecaf2071aeeb` |

All three transactions were FINALIZED with NORMAL consensus, MAJORITY_AGREE and one successful leader. [LIVE_WALKTHROUGH.md](LIVE_WALKTHROUGH.md) gives the three-step read-only path. [Main workflow evidence](evidence/live/main-workflow.json), individual [lock](evidence/live/lock.json), [derive](evidence/live/derive.json) and [confirm](evidence/live/confirm.json) records, and [independent confirm verification](evidence/live/independent-confirm.json) contain selected public proof and domain fields. No full node configuration, private keys or VM output is published in these records.

## Exact model and source

The original [596-byte synthetic policy](https://raw.githubusercontent.com/everyprovin/config-cohort/05a9edf0d3c19e7be82d56a24f1e11f0f34f6d4f/profile05/projects/config-cohort/fixtures/policy.json) has SHA256 `5ce7d89a51a58d62ab6dd8d3cdd743e5187caeb0282116176f35db1d6a643ff0`. The complete Boolean baseline and positive integer flip weights are checked against every clause. Among satisfying assignments, total weighted flip cost is minimized; equal costs choose the lexicographically smallest false-first vector in ASCII variable order. The source namespace and byte hash are fixed, and each transition fetches a fresh complete snapshot for independent verification.

The baseline violates clauses0 and1. With audit=false, consistency requires cache=true, preview=false and telemetry=false: the cost is2+1=3. Any audit=true model costs at least5. This explains the recommendation without claiming that declared preferences or feature meanings describe a real system.

The contract source remains SHA256 `9cee2f6a7c660df44831919cea9b8e1ede60e58b3492c58780c4973e5b90db54`. The original constructor transaction is `0x5042ed889243387ea6f2534fc87c4f00995612947993285de972090a05a59821`; it is separate from the three business transactions above. Its original saved record remains [public and byte-identical](https://raw.githubusercontent.com/everyprovin/config-cohort/471f86a06729d5ed6ba2835267ffd376abe17b1b/evidence/constructor-deployment-record-001.json). [deployment.json](deployment.json) preserves all nine original public root field names; former null fields are populated from the actual constructor, source, hosting and recorded main-flow evidence.

## Scope, safety and current snapshot

This demonstrates one operator and a synthetic public policy. Revoke is implemented and locally tested but was not exercised live. No independent adoption, production use, infrastructure modification, funding, award or accepted contribution is claimed. The user manually handled observed wallet warnings and confirmed the business transactions. No automated warning override was clicked, and no independent origin-clearance claim is made. Unknown outcomes retain the original pending context/hash and must never be blindly resent.

At snapshot **2026-10-21T19:45:48.175072+00:00**, Portal **submitted=false** and **accepted=false**. Public source/hosting, this demonstrated wallet flow and Portal submission are separate facts. The new documentation commit is recorded only after actual publication and byte verification. [LIVE_STATUS.json](LIVE_STATUS.json) contains the timestamped scope. [HISTORICAL_README_FRONTEND002.md](HISTORICAL_README_FRONTEND002.md) preserves the exact README from verified frontend commit `471f86a06729d5ed6ba2835267ffd376abe17b1b` as history; older constructor-only or warning-blocked statements in historical records describe their earlier observation times.

Contract, fixtures and frontend code/assets are unchanged by this evidence documentation update.
