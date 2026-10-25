# R03 B06: reject stale world snapshots

2026-10-25, continuation of scheduled18:11 resumption. R03 remains IN_PROGRESS. This checkpoint fixes the demonstrated receiver cache ordering gap only. Custom managed application/shared progress remainOFF; experimental own-world recovery remainsOFF by default and was enabled only on copied profiles.

## Task and gap justification

Task/dependencies/acceptance were recorded IN_PROGRESS before editing. Starting repository checkpoint a96d1a9, pinned BBSC reference4f11faf88b6ba658ebde6fe5fbefdadedba4fa41; B03 receiver source/patch protected privately. CL03 C3 and CL04 B39/A37 identify an actual unguarded receiver: completedN can replace completedN+1, and delayed chunks can reset a newer assembly. Existing settings cannot impose ordering. The smallest shared fix is at OnBbscWorldFlagsPacket, used by both existing transports; no sender, wire format, progress filter, event hook, epoch framework or new runtime option is needed. Acceptance is actual-function RED/GREEN, valid maps/Dream/chunks/wrap/reset preservation, DLL build and bounded copied native regression. Native C3 callback/earning proof is separate.

The source adds14 lines: reject equal/older counters against the latest completed cache for the same map, and reject older chunks against the active same-map assembly. Unsigned serial arithmetic accepts UINT32_MAX-to-zero wrap and rejects the ambiguous half-range. Equal-counter chunks still complete an unfinished assembly; duplicate completed input cannot refresh its bytes/completion time. Existing ClearBbscHostWorldSnapshots resets all ordering state; whether every real party boundary invokes the correct lifecycle remains a C4 question. Existing validation/mutex/other systems are preserved. No claim of sender authentication or jointly earned-event admission is added.

## Fixture and build evidence

Retained tests/test_bbsc_world_ordering.py compiles the actual receiver, state, reset function and packet header from the prepared pinned reference. Clock/map/switch dependencies are controlled at the preagreed native seam; receiver logic is not copied into the test.

- First compile failed due to a wrong include root; corrected to emulator/src. This was setup failure, not RED.
- RED1: completed22/new bytes followed by21/old bytes fails snapshot==22 on B03. Completed-cache guard makes it GREEN.
- RED2: partial24 followed by23 resets the active assembly on the first candidate. Active-assembly guard makes it GREEN.
- Final fixture also covers duplicates, independent maps, Dream, null/size/version/chunk/map validation, explicit reset, counter wrap and ambiguous half-range. PASS.
- C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p 'test_bbsc_*.py':3PASS. Same command with test_native_bbsc.py:2PASS.
- Same Python, -m unittest discover -s tests:160 tests,1 failure,8 errors,48 skips, exit1. Existing Windows symlink/shell and packaged Vulkan/Nix test categories remain failing; the full suite is not PASS. Exact names/logs are private in full-suite.log. No source changed afterward.
- PATH prefixed with C:/msys64/clang64/bin; same Python tools/build_bbsc_mod.py .superpowers/reference/BBSC .superpowers/r03-b06/ordered-dll: waited exit0. Local DLL only, no release EXE/ZIP.
- Complete tracked patch retains its four existing destinations; git apply --reverse --check against the prepared reference passes. Inline Standards/Spec review finds no new blocking issue in the bounded14-line fix. Broader C3/C4 and existing G2 gaps remain.

## Bounded native evidence

Copied host A8968/Kaori0/Cathedral uses B03 DLL96e398b2; fresh guest B16404/U-I-AHH3 uses candidate DLLfaf8227f. This is baseline-host/candidate-guest compatibility, not a same-build pair or a positive/negative earning pair. Both use existing1280x720 test settings; actual low frame rates remain. Candidate module path/hash verified,160/160 hooks installed,52 byte patch writes; Dream/guest-items/Spectate/Timeline ON, shared progress and extra WarpJoin OFF. Original profiles were never launched.

First claim19:31:59 precedes a later retry. Actual guest state4/6 and host-world load occur; world copy19:33:15 uses snapshot232, age226ms,30 groups/9 differing bytes plus12 other blocks/38 bytes. Host SummonSuccess_White19:33:27; guest placement/load-cover fade19:33:31. Guest loading0/type1/own0 in Cathedral; measured separation0.849996m. No actual stale-packet reorder was injected, so this only checks normal native compatibility.

No boss kill, combat, death or NPC interaction occurred. Short guest movement stayed inside the chapel. Normal Parting Blank use19:40:14, LuaOnLeaveMagic19:40:15, state0 by19:40:23, Central area19:40:30 and alone19:40:31. Immediate returned1250 groups equal prejoin exactly; same-PID snapshot SHA256497423c21841d7947d9880e1b2cd12a30bc599df9cd78986568c4b4b103ea1d1. Returned map0x18010000/lamp2412950/heading0.065716 and point(-190.181320,-50.627991,170.588699) match the accepted own-world journal exactly, distance0.0. The earlier pre-bell point was about4.1m away; do not confuse that older observation with accepted admission origin.

After normal Quit/title, same-process PlayOnline/Continue successfully reloads own map/lamp/point/heading. It is not an independent-process reload. The loaded world differs from prejoin only in group12705 at12705098,12705301,12705520,12705521,12705531,12705532. These six bits are UNCLASSIFIED: no quest-damage or harmless-transient conclusion, no full save/reload integrity PASS. Preserve all snapshots/after-saves and classify with a no-party reload control before attributing the difference to this receiver fix. B05's separate B03 independent-process reload is exact, but does not substitute for this candidate case.

Host and guest both normally Quit to startup/title and CloseMainWindow/WaitForExit return true; launcher sessions51480/76264 waited exit0. No third same-process host-character change was attempted: two previous B05 GPU PM4 failures remain the only evidence, G2-22(g) BLOCKED. Copied after-saves are retained; originals3171 paths/hashes verified exact after both close; copied after-saves protected. Earlier optional human boss-staging request no longer refers to an open game window.

## Bounded no-party reload control

Fresh candidate process3976 is launched with no host/peer, after protecting co-op after-saves and restoring only copied B savedata from native/before-b-savedata (same file set). The old journal is already .restored, no active admission recovery. Native fresh loaded map0x18010000/lamp2412950/pre-bell point matches the baseline. An early loading-cover snapshot differs at12705301 only; after the visible world settles, all1250 groups are exact to guest-before-world.json (compare-world result{}). This proves at least one listed bit changes transiently without co-op and a clean fresh baseline load is exact; it does not classify all six post-co-op bits or replace an independent reload of protected co-op after-saves. No bells, movement, combat or party in this control. Evidence .superpowers/r03-b06/solo-control, isolated launcher/logs and loaded/settled world snapshots. Control normally Quit/closed; helper50664 waited exit0. Copied B baseline restored and file hashes verified after preserving control after-saves; co-op after-saves remain native/after-b-savedata for next independent replay.

## Frozen attribution

| Input/artifact | SHA256 |
|---|---|
| Prepared bloodborne_re.cpp | 76287a320bec6ba63c959b38a9764331cd89a27eb4d17798fa463d1c81a87494 |
| Complete tracked four-destination patch | 6dec09c7497fe7f85efa8cc299412d6320e754baef265d53afd601e33e1c7f4c |
| B06 local bbsc.dll | faf8227f64137b50bbc54e076ad1f309bab7c20940370e1a277e9e2a8fdbac83 |
| Retained ordering test | 606347476f95b6ea6ef51c937f5029dbcdfeb3ec2b1cca86a882bd326ce1f731 |
| Unchanged source-built probe | 6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14 |

Private evidence .superpowers/r03-b06: before.cpp/patch, source-only.diff, RED/GREEN/focused/native-header/full-suite/build logs, ordered-dll, hashes.json and native snapshots/journal/before/after saves/launcher logs. Read-only native commands: .superpowers/r03-close/read-position.py PID OUTPUT and read-world.py PID OUTPUT; .superpowers/r03-a03/compare-world.py BEFORE AFTER DELTA; native/check-origin.py and assert-bounded.py PASS. No raw assets/saves/logs/credentials are tracked.

## Remaining acceptance / next action

B06 receiver-cache ordering is verified by fixture and normal native join/return regression. Full C3/G2-17 live reordered input versus native callback remains unproved: CL04 A37's defaultOFF bounded diagnostic control was not added. Do not convert the ordering fix, first received snapshot, member count, source mapping or boss gauge into earning proof. G2 actual joint kill/positive producer sensitivity, surviving/dead/loading delivery, first-playable/party epoch and history exclusion, valid pending original-owner obligations, same-host/new-party/character boundaries and remaining R03 gates stay open.

Next: classify six reload bits with a bounded no-party control and independent candidate reload, then stage Kaori0 near an alive boss for actual joint earning (fresh guest process per paired positive/negative run, CL04 readiness/throttle checks). Preserve original-owner retry and defaultOFF gates. Do not rerun R02/all maps, add a generic quest/epoch/storage framework, package or redeploy. Usage checked periodically: latest pre-checkpoint12%/71% remaining; below10% in either window stop new work and publish checkpoint.

## Final checkpoint checks

Inline Python final checks PASS: original3171 path/hash set exact, copied B baseline restored byte-exact after protecting both co-op/control after-saves,5 frozen source/patch/DLL/test/probe hashes,6UTF8/noBOM documents and91 local links, immediate-return/control1250group comparisons, all4 patch destinations/reverse-check. git diff --check --ignore-submodules exit0; no test process remains. Unrelated dirty FSR-Vulkan retained; four Claude audit documents untouched. Latest usage10%/70% remaining, reserve only checkpoint/publication work. Standards: no new blocking finding in the bounded source/test diff. Spec: bounded cache-ordering requirement verified; R03 earning/epoch/native reorder and candidate independent post-co-op reload requirements remain incomplete, not waived.
