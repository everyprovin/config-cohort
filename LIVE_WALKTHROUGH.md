# ConfigCohort recorded live walkthrough

AI-assisted synthetic prototype, frontend revision002 at `471f86a06729d5ed6ba2835267ffd376abe17b1b`. One operator exercised the normal wallet path on GenLayer Studio61999: lock_source -> derive -> owner confirm. The record is **ConfigH1022A**, **CONFIRMED revision2**, certificate `7b27227609082251795cdce809268f85fb09668a458807e5e6be713d214c1b87`. Revoke was not exercised live. No independent adoption or real infrastructure change is claimed.

1. Open [https://everyprovin.github.io/config-cohort/](https://everyprovin.github.io/config-cohort/). Reading the demonstrated record needs no wallet connection or signature.
2. Enter `0x5f2D1d6515659DD53A19f4BEea2F25d24333c3df` in **Actual contract address**, enter `ConfigH1022A` in **Record ID**, and click **Load record**. Expand **Actual loaded chain record**; expect CONFIRMED/revision2 and the certificate above.
3. Inspect the complete result: **SAT**, bits **0100**, flip cost **3**, changes **cache and preview**, **7** satisfying models among **16** examined. Clause witnesses in order are cache, !preview, !telemetry and !telemetry. The locally available **Use minimum-change model** button changes only the manual preview; it does not send a transaction. Compare the record and the original transaction proofs below.

| Operation | Original transaction hash | Saved evidence |
| --- | --- | --- |
| lock_source | `0x584c4a196073749e8243ba696ee32b267d8734b94bb089560c786a67522f978f` | [lock.json](evidence/live/lock.json) |
| derive | `0xd0bdb3c8eef05f78946b4d4d485cbcb7a6154d869827643e471db942dc3801a6` | [derive.json](evidence/live/derive.json) |
| confirm | `0x534bdcfbcaf4c16631b5abe91660f6ed78e804630b609b6972f2ecaf2071aeeb` | [confirm.json](evidence/live/confirm.json) |

All three original transactions finalized with NORMAL consensus, MAJORITY_AGREE and one successful leader. The selected public raw/SDK fields bind each original hash, owner, target and value0. [Main workflow](evidence/live/main-workflow.json) and [independent confirm verification](evidence/live/independent-confirm.json) show the recorded scope. A certificate is generated only on confirmation from the canonical full confirm capture; the derived record had an empty certificate.

The original fixture is [https://raw.githubusercontent.com/everyprovin/config-cohort/05a9edf0d3c19e7be82d56a24f1e11f0f34f6d4f/profile05/projects/config-cohort/fixtures/policy.json](https://raw.githubusercontent.com/everyprovin/config-cohort/05a9edf0d3c19e7be82d56a24f1e11f0f34f6d4f/profile05/projects/config-cohort/fixtures/policy.json) (596 bytes, SHA256 `5ce7d89a51a58d62ab6dd8d3cdd743e5187caeb0282116176f35db1d6a643ff0`). Its baseline is audit=false, cache=false, preview=true, telemetry=false. Setting cache=true and preview=false costs2+1=3; every audit=true model costs at least5. These are declared synthetic flags, not real systems.

Wallet warnings were retained and handled manually by the user; no automated warning override was clicked. This does not assert independent clearance of the warned origin. An unknown new action must retain its original context/hash and must not be repeated. Portal submitted=false and accepted=false at snapshot `2026-10-21T19:45:48.175072+00:00`; later submission is recorded separately. This walkthrough asks for a read of the existing record, not another wallet transaction.
