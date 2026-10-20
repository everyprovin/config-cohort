# ConfigCohort Implementation Plan

> Execute inline in the authorized exclusive package directory, use TDD; root performs the independent final review.

**Goal:** Exhaustive Boolean CNF search with weighted Hamming distance and ASCII-variable lexicographic tie breaking.

**Architecture:** exact pinned zero-constructor GenLayer contract, independent immutable-source recomputation, separate browser domain preview and live wallet workflow.

**Spec:** DESIGN.md

**Global constraints:** GenVM v0.2.12 runner1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6; post-download 32768 bytes; no private keys; own project fixture namespace; null deployment/publication/live state.

**Review focus:** unknown and duplicate schema fields; tie order; hostile validator packet and fresh byte mismatch; unauthorized/stale state transitions; finalized failed or unknown wallet execution.

- [x] Write SDK tests with literal independently checked results; run against empty API and preserve RED evidence.
- [x] Implement strict schema, deterministic complete algorithm, independently recomputed source binding and owner lock/derive/confirm/revoke API; run actual SDK GREEN suite.
- [x] Write frontend domain and wallet boundary tests; observe missing implementation RED; implement actual controls/visuals/transactions and observe GREEN.
- [x] Run official semantic/lint/schema checks plus TypeScript and Vite; inspect output and preserve exact source SHA.
- [x] Package via explicit file allowlist, validate ZIP CRC and per-file SHA; submit frozen candidate for independent review, with null unverified deployment state.
