# R03 playtest follow-up: source delivery and user playtest

Updated 2026-10-31 (Asia/Bangkok). Owner: Codex for source/offline validation; user for gameplay. User explicitly authorizes code changes and removes all agent-run game testing. This supersedes the earlier investigation-only plan, no-code HOLD and agent native-test queue. No game is launched as part of this plan.

## Scope

1. Prevent stale host pending-role 0 overriding a new co-op guest character.
2. Exclude demonstrated Cleric Beast/Gascoigne transient combat bits from collected/replayed durable progress.
3. Remove ordinary-enemy automatic compensation and its notice, preserving manual ground pickup and boss rewards.

[Original investigation](../../handoff/R03-PLAYTEST-LEADS.md) records evidence and uncertainty. [Source delivery/checks](../../handoff/R03-PLAYTEST-SOURCE-FIX.md) records changes, hashes, commands and limitations. Gascoigne key/Echoes were received; reward loss is not an active finding. General crash diagnosis and unrelated R03 acceptance remain outside this bounded delivery.

## Agent execution queue

| Done | ID / status | Work | Acceptance / evidence |
| --- | --- | --- | --- |
| [x] | PT00 / DONE | Review supplied logs, source and user corrections | Original investigation and confirmed guest ground-loot report. No single-enemy duplication claim. |
| [x] | PT01 / DONE for source inputs | Establish matching source in isolated directory | Frozen Echoes source preserved; matching source/DLL attribution recorded. No native profile preparation required. Friend binary identity remains unverified. |
| [x] | PT02 / DONE for source guard | Guard the observed stale pending-role consumer | Only pending0 with co-op sign -1/session6 is discarded at reload finish before native character creation; valid phantom/invader overrides unchanged in actual-function checks. Exact upstream writer remains unproved. |
| [x] | PT03 / DONE for bounded source correction | Filter known transient combat bits | Six event-derived flags filtered at collection and merge, including old pending journals. Completion, adjacent progress and existing own-world live state retained in fixtures. Broader maps/late event scheduling remain unqualified. |
| [x] | PT04 / DONE for removal | Retire ordinary-enemy automatic grants and notice | Queue/producer/consumer/helper and RNG removed; ground pickup and boss reward paths retained; shared GUEST_ITEMS switch unchanged. |
| [x] | PT05 / DONE | Review scoped implementation | No forced role tick loop, group-wide clearing, global item disable or currency adjustment. Tracked integrated patch contains the changes. |
| [x] | PT06 / DONE | Apply source changes | Isolated source, tests and integrated four-destination patch; other three runtime source destinations unchanged. |
| [x] | PT07 / DONE | Offline verification/build | 12 BBSC fixtures + 2 native-header tests PASS without skips; prior-source merge regression fails; DLL build exits0; patch apply/reverse checks and normalized source comparison pass. |
| [ ] | PT08 / USER PLAYTEST | User plays with friend using matching new DLL | Await real gameplay feedback/logs; not an agent-run test or offline acceptance requirement. |
| [ ] | PT09 / PENDING USER EVIDENCE | Review returned logs and update outcome | Record PASS/FAIL/INCONCLUSIVE per issue; do not infer gameplay success from source checks. |

## User playtest handoff

Local package task PK01 DONE (2026-10-31): user separately authorizes packaging the corrected version. [Ready package and validation](../../handoff/R03-PLAYTEST-PACKAGE.md): verified base with new DLL/notices, revised instructions and manifest; 1,186 entries pass integrity/hash/content/private-path checks. ZIP remains local pending user distribution; no game launch or release upload.

This is a compact observation list for the user's normal playtest, not a requirement to run staged automated game cases:

- Both clients use the same new DLL. Check host -> guest after host death/respawn/session close: role, cooperator count, repeated bells, leave menu/animation and unexplained Insight gains.
- After a completed Cleric Beast/Gascoigne visit and any naturally occurring disconnect/restart, check solo boss gauge and retained completion/progress. Confirm an unfinished boss still fights/transforms normally.
- Guest should receive ordinary-enemy goods by manual pickup, without the automatic add notice; check rare material drops if encountered. Boss rewards and item persistence after return/restart should continue working.
- Return the same mod logs, timelines and captures from both clients. Report which player was host, approximate incident time and observed symptom. No need to send account secrets or original saves into Git.

## Evidence/checkpoint rules

Record source commit, source/patch/DLL hashes, effective settings, exact offline commands/exits, fixture versus gameplay evidence and limitations. Raw logs/assets/saves/credentials stay private. Update this queue and the shared tracker at each source or user-playtest checkpoint and push normally to origin/seamless. The user-authorized local ZIP is recorded in PK01; release upload, live-server deployment and original-profile mutation remain outside this plan.

| Date | Checkpoint | Result | Next action |
| --- | --- | --- | --- |
| 2026-10-30 | Original log/static investigation | Leads found; no verified gameplay fix | Source scope defined |
| 2026-10-31 | User clarification | Guest ground loot works; compensation considered redundant | Remove only compensation |
| 2026-10-31 | Authorized source delivery | Three scoped changes, 14 offline tests and DLL build pass | User playtest; review feedback |

Source delivery is complete for the bounded changes. Gameplay acceptance and broad R03 completion remain open.
