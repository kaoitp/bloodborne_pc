# R03-B02 boss reward delivery checkpoint

2026-10-25, Codex inline. Base 4c612b85d61de0803cda7e6fb7d161388c55c655 on seamless. Parent [plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md), [tracker](../WINDOWS-PROGRESS.md), prior [B01 preservation](R03-B01-PERSONAL-FLAGS.md).

## Scope and correction

Goal: retain a queued boss reward through temporary native delivery failure and give it only to its original character. The original TickBbscBossRewards emptied the queue before checking the item/event managers, marked an event given before the add succeeded and fell through from a failed known-goods add to an unconfirmed popup award. Queue and given entries held only an event number. Configuration cannot fix those ordering/ownership errors.

The existing finite reward tables, NoteBbscBossRewardEvent, TickBbscBossRewards and save-slot helper are the responsible producer/consumer. Entries now hold the existing user/slot owner and the first selected lot. Delivery waits for a loaded, living character with ready managers and a fresh matching save-slot observation; failure retains the entry. Known direct-goods failure does not invoke the popup fallback. Only successful direct delivery, the existing zero-lot/completed path, or the unchanged native non-goods dispatch enters the given list. Duplicate queued entries are checked again before delivery. The fight-area check moves to enqueue so an entry can finish after departure to a different map. Retry is limited to once per second and an empty queue returns immediately.

This is delivery correctness, not proof that an event was earned together. The original player-type-wait admission and full-host-history collection are not fixed here. No new event catalogue, transport, journal/save codec, managed application, launcher or renderer work. Custom managed application remains OFF; experimental home recovery remains OFF by default and is opted in only on copied test profiles.

## Source and artifacts

Pinned reference HEAD remains 4f11faf88b6ba658ebde6fe5fbefdadedba4fa41. The complete tracked patch retains HTTP/mod/relay/bloodborne_re destinations; reverse check passed. The two existing reward tables are unchanged.

| Input | SHA256 |
|---|---|
| Modified reference bloodborne_re.cpp | 84ed81a47aa58f885a50764230ba93708601c9a9dc4c0d1350e4d27b2eafe452 |
| Complete tracked BBSC patch | 211a3245b707f543aa42169a04739fa57e638fe0a8fc07da1ced80fbc61be4e0 |
| Frozen local DLL | 2fed10b3bd1a2c035a9521c18ea0dd43b376ad92cfcddf5b7bfd777ec25e0cf1 |
| Source-built probe | 6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14 |
| Existing injector | c7fbaa406d972324645153bb8cc8bdad17fcd7db2f05026d67e3ba68f34750c1 |

Build command: PATH includes C:/msys64/clang64/bin; python tools/build_bbsc_mod.py .superpowers/reference/BBSC .superpowers/r03-b02/frozen-dll; waited exit 0. Native Windows module inspection confirms A15092/HWND4653632 and B5844/HWND263988 both loaded that exact frozen DLL path. Both installed 160/160 hooks. This removes the prior mixed diagnostic pair limitation for this bounded join regression, not all R03 acceptance.

## Fixture evidence

The retained test [test_bbsc_reward_delivery.py](../../tests/test_bbsc_reward_delivery.py) compiles the actual pinned-reference producer/consumer bodies with controlled native dependencies. It requires the locally prepared source and clang++; otherwise explicitly skips. No game assets, saves or live process are used. This is fixture evidence, not gameplay.

- Initial actual-function RED: unavailable item manager empties the queue; assertion fails. An earlier missing CLANG64 runtime PATH was setup failure and excluded.
- A second RED caught duplicate queued delivery after moving confirmation later. A third RED caught a failed first-lot add being reinterpreted as a repeat/zero lot after the flag changed while waiting. Both are corrected in frozen source.
- Final retained test: python -m unittest discover -s tests -p test_bbsc_reward_delivery.py -v; 1 PASS. Cases cover unavailable item/event state, loading, death, add failure/no popup fallback, unavailable owner, different user/slot, return to the original owner, once-only success, duplicate entries, frozen lot through flag change, completed zero lot, unknown/wrong-area event, enqueue de-duplication and delivery after changing area.
- Existing focused headers: python -m unittest discover -s tests -p test_native_bbsc.py -v; 2 PASS.
- Frozen full suite: python -m unittest discover -s tests; 158 tests, 1 failure, 8 errors, 48 skips, exit 1. Same Windows symlink/shell/tool and packaged Vulkan/Nix limitations; no full-suite PASS. The final whitespace-only C++ fixture formatting was recompiled by the focused test and passed.

## Native regression evidence

Original 3171-file manifest and both copied save trees were protected before launching. Initial B14840 stopped during Cathedral loading, before join, with GPU Wrong PM4 type 1. Suspect copied saves and logs are preserved under .superpowers/r03-b02/failed-startup-b; only copied B was restored from preflight. No renderer change. Preliminary review builds were normally saved/closed before swapping versions and are not frozen-source join proof.

Frozen pair A15092/B5844: distinct authorized accounts, existing same nonempty word, separate copied profiles/ports, shared progress OFF, guest items ON, Discord OFF, experimental home recovery ON only in this test. Actual native join/adjacent blue guest succeeded. Guest settled own=0/type=1/loading=0/map 0x15000000; guest (-8.229970,-7.004732,-21.623533) beside host (-9.080694,-7.031137,-21.623533). Actual journal copied before departure. No boss reward event fired in this Dream visit, so this run does not natively prove reward failure/retry or jointly-earned progress.

Normal Parting Blank observed/confirmed; return restored Cathedral map 0x18000000, lamp 2402950, point (14.028195,-9.508328,105.312050), heading -0.868897. Settled independent 1250-group snapshot equals prejoin exactly, zero differing bits; both same-PID JSON snapshots SHA256 06fad8d8c3d6d6305ffa15ab5db9e3352749888daaab3f63039acfb180c8c4a7. No NPC dialog, purchase, boss or story reward was earned. Some menu frames lagged input; selections were re-observed rather than confirming an unexpected consumable. Inventory-wide equality is not claimed.

Actual Quit/title/Play Online/Continue retains all 1250 prejoin groups exactly and the returned point/lamp/heading. Independent assert-final.py PASS: all prejoin/settled/reloaded groups, all 53 present journal keys, returned/reloaded origin and original 3171-file path/hash set unchanged. Both test clients then Quit Game, reached visually confirmed title and CloseMainWindow=True/WaitForExit=True; no remaining bb-probe process. Ignored evidence: .superpowers/r03-b02/native-frozen, frozen-hashes.json, *-red.log, retained-final-test.log, frozen-suite.log and frozen-build.log. Raw logs, credentials, saves and assets stay out of Git.

## Eligibility lead and remaining gates

Actual frozen join timeline: host rings claim 12:49:54; member count becomes 2 at 12:50:01; host progress summary with 16 flags reaches guest 12:50:04.474; host SummonSuccess_White runs 12:50:12 (caller 0x015BCCF7); guest reports loading=0/type=1/Dream and 2 hunters at 12:50:12, with load-cover fade/adjacent placement at 12:50:15. Thus members=2 and the first summary precede playable completion. Neither can authorize earned events. Existing WriteLuaSessionEvent already observes the success callback, so investigate its precise member/attempt binding and the native completion producer before adding a separate framework. Read-only partial caller disassembly is only an unvalidated lead; no new offset/hook or eligibility rule was adopted from it.

G2 remains REPRODUCED-GAP: full-host-summary union and bulk kind-1 OR are unchanged. A naive first-received-snapshot delta still fails late old history, first eligible kill folded into baseline, reordering and death/loading continuity. Old-host-history exclusion, relevant owned/consumed item de-duplication, durable reward confirmation through crash/restart and eligibility must be implemented and natively verified. Non-goods native popup awards still lack confirmation (explicit shortcut comment); this patch does not extend retries to them. The queue is in memory only, and same-run user/slot ownership is not a new durable character/NG ledger.

Locked-own-map, remaining stale/failed candidate, complete required-service routing and recovery enablement gates remain open. Actual successful self-hosted join is stronger than an open port; stored TCP connections alone are not a complete route proof. No all-map sweep, new account/server action, packaging/deployment or audit-owned edit. Inline Standards/Spec review and final publication are recorded in the tracker. R03 stays IN_PROGRESS.