# PR17 revision 3 validation

2026-10-29 (Asia/Bangkok), Codex. Target PR #17 head `5e709263072c873900b375fcf4af4e232d2fcec2`, base `56bed5ee11e8e78ba1d548a1d03168a86977531e`. This run supersedes the earlier inconclusive revision-2 attempts for the cases actually completed below. Product source/defaults are unchanged; no merge, packaging or server redeployment.

## Scope and composition

Task completed for the bounded repeated-Amelia guard, consumption/restart and never-beaten positive control. Dependencies: pinned BBSC source, tracked four-destination candidate patch, existing compiler/probe, distinct existing accounts, fresh copied profiles. Private evidence is in `.superpowers/pr17-v3-validation` in the f0eb worktree; it is not a portable game installation.

| Input | SHA256 |
|---|---|
| Reconstructed `bloodborne_re.cpp` | `fa3863e5498e92a3ea8049cd557de7c86a60470b16ae617ca6faae239e126c0e` |
| Candidate patch | `3503272f07997b708804ed67e114099de82a482cac72a20bfdb7813b92b6aeb1` |
| Locally built `bbsc.dll` | `122973f353cca1c35a16464f950876c869d752f6ec9713e777ccb95879621510` |
| Existing source-built `bb-probe.exe` | `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14` |

All four patch destinations reconstructed from pinned `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`; full reverse apply-check exit 0. Existing fmt/xbyak dependencies reused. DLL compiled with the existing CLANG64 C++23 shared-library recipe, exit 0. Mandatory LICENSE/NOTICE/SUPPORTERS files included before either game launched. This local DLL hash differs from the author's build; only the local hash above is attributed to this native run.

Effective copied-profile configuration: `SHADPS4_BBSC_REWARD_DEDUP=1`, `REWARD_ONCE=0`, existing shared progress/guest items/Dream ON, spectate OFF, experimental/home recovery OFF, existing no-death ON. Existing self-hosted account/service configuration reused. No custom managed admission/progress switches enabled.

## Fixtures

`C:/msys64/clang64/bin/python.exe .superpowers/pr17-v3-validation/validate.py` with CLANG64 first on PATH and workspace TEMP/TMP: **12 tests PASS, no skips, 31.910s**. Actual producer/consumer, reward-once/dedup/owed ledger, own-world ownership, party progress, backup refusal, reorder/receiver, remote visibility and native header checks. Two existing macro-redefinition compiler warnings. Missing fixtures were not treated as passes.

`validate.py` initially stopped on an existing empty dependency destination, then an incorrect reverse-check after re-extraction; corrected dependency copy/reapply sequence completed. These were harness setup failures before the successful fixture run. Full platform suite not repeated; no claim of a green full suite or CI.

## Native repeated kill and restart

1. Fresh copies of native01 host and native04 guest, PIDs host13812/guest7020. Read-only snapshots: host Amelia12401800 OFF; guest ON, Gold Pendant4001 x1 in slot84. Complete native mod composition observed: image verified, 50 patch sites; correctly named bells and kit visible.
2. Ordinary Hunt/Kin Bell use. Guest prejoin journal captured01:27:31.842; placed01:27:52.175, party collector baseline01:27:56.632. Own-world journal independently parsed with its bounded BBOW header/record layout: 981 entries, Amelia ON, SHA256 `e16b6bb54379a0d8f7a84be783e319c0df677868d4b633f1041702559dc41835`. Guest entered host map0x18000000, own_world0/type1. No guest position, flag or inventory writes by helpers.
3. Existing guarded native warp staged only copied host at `(51.90,35.71,312.30)`; normal stick movement triggered Amelia's introduction. Live gauge: boss502000/type7/HP8051 of8051. Existing guarded `native-aid.py 13812 kill` wrote only that boss HP to0 and confirmed readback. Initial staging invocation from the worktree failed its executable-path guard before a write; rerun from required primary directory succeeded.
4. Guest01:30:14.389: `event 12401800 - user sd1 slot 3 has beaten this boss in its own world - not again`. No queued/add/finished reward lines. Automatic return restored exact prejoin map0x18010000, lamp2412950, position and rotation; own_world1/type0.
5. Ordinary inventory use consumed old Pendant01:31:24; Gold Blood Gem x1 visibly awarded. Read-only Pendant count0 immediately and again01:32:59, over90 seconds later. No replacement or owed file for this rejected obligation.
6. Both saved through Exit Game and returned to title, then their verified test processes closed normally, runner exits0. Fresh guest PID13460 loaded same profile and candidate: Pendant0, zero fresh reward log lines, exact original map/lamp/position/rotation. Normal save/title/close repeated.

**Bounded result: repeated-kill rejection, consumption/no replacement and fresh-process Pendant persistence PASS.** This was a command-assisted party kill, not an unassisted combat test. Initial fresh flag snapshot and a later snapshot differ as loading settles; post-consumption versus later fresh snapshot differs in group12404 (13 bits), not yet classified. Full flag/save integrity is not claimed from reward persistence.

## Native never-beaten control

Separate fresh copies of native01 profiles, host24772/guest21732; same candidate DLL and configuration. Both settled Amelia bits OFF, guest Pendant0; loaded guest module hash verified against the table above. Prejoin journal independently parsed: Amelia OFF. Host staged with the same guarded warp; guest placed01:42:23.221, new-progress baseline01:42:28.646. Native coordinates stayed valid despite the host view rendering mainly sky/missing geometry; graphics were not diagnosed or qualified.

Normal stick movement triggered the introduction. Live Amelia lookup again502000/type7/HP8051 of8051; guarded HP-zero confirmed. Guest01:44:51.074 queued12401800 for sd1/3;01:44:51.076 added goods4001 x1 in slot84 with confirmation true;01:44:51.081 finished lot50000001. Read-only inventory confirms Pendant1; no owed-sd1-3.txt remains after delivery. The brief owed-file creation itself was not observed, so its creation is fixture evidence, not a native file-watch PASS. Guest automatically returned to exact origin/map/lamp/rotation, own_world1/type0. The early returned snapshot still has Amelia OFF; it preceded the01:45:25.813 merge log (2 boss flags newly set), so it is not a settled progress assertion. Both saved normally through Exit Game.

**Bounded positive first reward PASS.** A further fresh-process persistence run for this positive control was not repeated; the negative control's restart above is separate evidence.

## Integrity and limits

`C:/msys64/clang64/bin/python.exe .superpowers/pr17-v3-validation/assert-result.py` exit0 asserts negative guard/no queue/no grant, Pendant0 after consumption/wait/restart, exact origin return/reload and all original3171 paths/hashes unchanged. Final cleanup/integrity verification is recorded below. Test helpers initially needed elevated process-read access; a denied read was rerun successfully and was not interpreted as a missing item.

Native deferred delivery/restart and disk-write/removal faults are not qualified by this run. The PR's two documented ledger I/O risks remain open, and dedup remains opt-in/default OFF. Broad R03 acceptance, full flag integrity (the group12404 difference above) and graphics qualification remain open. Next action: use these paired native cases for the opt-in candidate decision; preserve the shared-progress/owed-ledger protocol gates before any default enablement.

Final cleanup: all three initial/reload runners and both positive-control runners exited0 after normal save/title/close; no test game remains running. Final assert-result.py exit0 includes the positive one-grant/cleared-ledger/exact-origin assertions and final original3171 path/hash equality. Positive early-return boss-bit assertion was rejected as premature: capture preceded the merge; only collection/merge logs are attributed, not a settled/restarted positive flag PASS. Usage at checkpoint14%/56% remaining; no further test expansion.
