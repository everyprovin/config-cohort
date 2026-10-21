# ConfigCohort

## Deployment and frontend status

The original zero-argument contract deployment, public source fixture and GitHub Pages site exist. The constructor is recorded as finalized with successful execution; the wallet business lifecycle has **not** been verified live. This application remains an AI-assisted experimental prototype with synthetic public inputs, no real-world decision or adoption claim.

| Recorded public fact | Value |
| --- | --- |
| Network | GenLayer Studio, chain 61999 |
| Contract | `0x5f2D1d6515659DD53A19f4BEea2F25d24333c3df` |
| Constructor arguments | `[]` |
| Constructor transaction | `0x5042ed889243387ea6f2534fc87c4f00995612947993285de972090a05a59821` |
| Contract source SHA-256 | `9cee2f6a7c660df44831919cea9b8e1ede60e58b3492c58780c4973e5b90db54` |
| Repository | [https://github.com/everyprovin/config-cohort](https://github.com/everyprovin/config-cohort) |
| Earlier published repository commit | `ab25aabf511f5fca7a5d47fa3ebf05c0a60dbc2c` |
| Website | [https://everyprovin.github.io/config-cohort/](https://everyprovin.github.io/config-cohort/) |
| Exact public synthetic fixture | [Immutable source](https://raw.githubusercontent.com/everyprovin/config-cohort/05a9edf0d3c19e7be82d56a24f1e11f0f34f6d4f/profile05/projects/config-cohort/fixtures/policy.json) |
| Exact fixture SHA-256 | `5ce7d89a51a58d62ab6dd8d3cdd743e5187caeb0282116176f35db1d6a643ff0` |

The [constructor deployment record](evidence/constructor-deployment-record-001.json) preserves the original observed evidence and its field names. Constructor success and an existing hosted page do not establish lock → derive → confirm success, a current certificate, revocation, real users or an accepted contribution. No new constructor deployment is required by the frontend compatibility changes.

An exact minimum-change Boolean feature policy workbench with explicit CNF constraint witnesses.

This is one complete original GenLayer Project: contract, independent validator, interactive frontend, original MIT synthetic fixtures, tests and reproducible evidence. Do not count its bundled contract separately as an Intelligent Contract contribution.

## What the project does

The bundled four-feature policy has 7 satisfying models among 16 assignments. Its unique recommended bit vector is 0100 (audit=false, cache=true, preview=false, telemetry=false), weighted flip cost 3, changing cache and preview.

ConfigCohort exhaustively evaluates every assignment (at most 4096). It minimizes weighted Hamming distance from the complete baseline. Equal costs use false-before-true bits in sorted ASCII variable ID order. UNSAT has no assignment and cannot be confirmed. Manual assignments show exact violated clauses and true literal witnesses.

All feature names and point labels are fictional, non-PII and public. The application makes no real infrastructure changes and no claims about real people, similarity, roads or resource allocation. Source bytes and a deterministic derivation are the only certified facts.

## Contract API

The constructor takes **zero arguments**. Use GenVM **v0.2.12**, runner `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`. All writes require the original owner. Record identifiers are unique permanently.

| Method | Behavior |
| --- | --- |
| `lock_source(record_id, source_url, source_sha256)` | Fetch exact pinned bytes and validate full schema; store LOCKED revision 0. |
| `derive(record_id, expected_revision)` | Independently fetch and recompute; store DERIVED revision 1. |
| `confirm(record_id, expected_revision)` | Independently fetch and recompute again, compare complete source/result and bind a certificate to chain, contract, record, owner and source; store CONFIRMED revision 2. |
| `revoke(record_id, expected_revision, reason)` | Terminal revocation from any unrevoked stage, increments revision; does not need network access. |
| `get_record(record_id)` | Return an actual decoded dictionary containing stage, owner, revision, source, result and evidence. |
| `get_configuration()` | Return protocol and resource bounds. |
| `compare_assignment(record_id, assignment_json)` | Require every feature exactly once with Boolean values; return flip cost and per-clause witnesses. |

Source schema and bounds are specified in DESIGN.md. Unknown fields, duplicate keys and IDs, invalid types and resource bounds are rejected. Downloaded responses must be HTTP 200 and 1..32768 bytes, and byte SHA-256 must match. The byte bound is checked after download; it is not a bandwidth or redirect control. Validators independently fetch, validate and recompute the entire bound packet. They reject forged binding, result and changed-byte proposals. No LLM is used.

## Current frontend and verification

Frontend revision 002 uses the unchanged official `genlayer-js@1.1.8`, the Stable Studio method-key ABI and actual dictionary views. Writes use zero transaction value, the intended account, exact target and chain 61999. The application performs no hosted worker or automatic real-world action.

Public SDK/provider/RPC failures use fixed UNVERIFIED diagnostics rather than exception text. Receipt data is projected only after the complete original SDK/raw proof succeeds. Every supplied SDK leader list must contain exactly one successful leader; missing SDK fields remain missing and never replace the independent raw proof. A final provider-identity check prevents a replaced provider from being adopted during connection. Record, address or wallet context changes clear receipt display, and late callbacks cannot leave an old receipt beside a different loaded record.

The exact local revision passed **137 frontend tests**, TypeScript and Vite. The recorded pinned contract SDK suite passed **33 tests**. [Fresh independent peer review](evidence/frontend-stable-revision-002/independent-review.json) separately reran this package’s full frontend suite and rebuilt matching assets; across its four-package scope it also executed 112 focused boundary checks. These checks use fictional DOM/provider/RPC I/O and real production modules with the installed official SDK. They are offline verification, not live wallet or network consensus evidence. No real credentials were used.

The application preserves one underlying wallet mutation per submission. An unknown result, including an error before a hash is available, blocks another send. Public observation metadata stays in session storage; reconnect the original account and observe the original transaction, or attach its exact wallet-activity hash if it was missing. Only a confirmed first actual wallet rejection clears an unsubmitted intent. Removing browser storage or using another tab cannot preserve a local replay guard.

Earlier verification files and revision notes describe local checks at their recorded time. The original bundled `fixtures/source.json` still contains its test locator and a null `public_url`; that unchanged test metadata is not a claim that the separately published fixture above is absent. The UI intentionally starts without a deployment address. Enter the recorded contract and the exact pinned fixture URL/digest to inspect that deployment. Local edits and JSON export do not publish source or mutate chain state.

An earlier wallet attempt on this hosted origin was canceled after a security warning. Compatibility fixes and local peer review do not prove a warning false or constitute approval to bypass it. No completed live business wallet flow, live certificate/revocation, independent human operation, adoption, payment, award or accepted Project submission is claimed.

## Reproduce locally

From this package directory, install the pinned Python dependencies and run `python tools/verify.py`. This exercises the direct GenVM SDK, validators and schema/semantic checks with controlled public inputs. Then:

```powershell
Set-Location frontend
pnpm install --frozen-lockfile
pnpm test
pnpm build
pnpm dev
```

The Vite SDK bundle emits a size notice above 500 kB before compression. The prototype certifies only the declared synthetic source and deterministic model. Public web hosting, direct SDK tests, constructor execution and business lifecycle verification are distinct evidence categories.
