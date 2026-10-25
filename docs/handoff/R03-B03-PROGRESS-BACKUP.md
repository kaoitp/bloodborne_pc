# R03-B03 progress backup and owner retry

2026-10-25, Codex inline. Source base 1a307b3f8f0f2ef5574e0c9d06af239a90bf6f68 on seamless. Parent [plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md), [tracker](../WINDOWS-PROGRESS.md), [B02 reward delivery](R03-B02-REWARD-DELIVERY.md). R03 remains IN_PROGRESS.

## Demonstrated gap and smallest change

The prior MergeBbscSharedProgress stores BackupBbscSaves()'s false result but still mutates flags, and TickBbscSharedProgress clears/finalizes the pending intent. Configuration cannot make that false result stop the writes. The first actual-function RED reproduces this. Extending the retry fixture then reproduces another gap: a different loaded character receives the original owner's pending data once backup becomes available.

The existing merge now checks its existing user/slot owner against a fresh active slot and refuses a missing/mismatching owner before backup or mutation. Failed backup returns the same distinct retry result before writes. The settled caller keeps pending memory/file/owner instead of finalizing; the load caller already treats a negative result as unmerged. A backup warning is issued once until empty or successful merge. The slot declaration moves above the merge; the existing slot helper, backup routine and file format are reused.

All callers were inspected: TickBbscSharedProgress and ApplyBbscSharedProgressAtLoad. The complete tracked four-destination BBSC patch retains HTTP/mod/relay/core changes. No new catalogue, codec, journal, transport, managed application or server change. Existing 180-second memory timeout still preserves the pending file for later recovery. G2 earned-event admission/full-host-history collection is unchanged.

## Source and artifacts

Pinned reference HEAD remains 4f11faf88b6ba658ebde6fe5fbefdadedba4fa41. Private source before.cpp is protected B02 source. Complete patch reverse-check PASS.

| Input | SHA256 |
|---|---|
| Modified reference bloodborne_re.cpp | 2ac893635c9944de6ac04709fd98575f740dd5bea5da97926155838a85fb505b |
| Complete tracked BBSC patch | 8a3ce6f9aa01da16b8bf503538d6b215b349f2d99ef2ae876f1c61fa02c086ec |
| B03 GREEN DLL | 96e398b23e0d48af4f220a7ca7534d529369e1f194bc65e60da55d884ca2303d |
| B02 RED DLL | 2fed10b3bd1a2c035a9521c18ea0dd43b376ad92cfcddf5b7bfd777ec25e0cf1 |
| Source-built probe | 6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14 |
| Retained B03 fixture | 6cf58f2037b2ab9113483330a826ca12a7647d8a668547fd57429b0fcfeccfaf |

Build: PATH includes C:/msys64/clang64/bin; python tools/build_bbsc_mod.py .superpowers/reference/BBSC .superpowers/r03-b03/backup-dll; waited exit 0. Actual Windows module inspection confirms RED PID6588 loaded the B02 frozen DLL and GREEN PID13992 loaded the B03 backup-dll above, both 160/160 hooks.

## Fixture evidence

Retained [test_bbsc_progress_backup.py](../../tests/test_bbsc_progress_backup.py) compiles actual merge, settled tick and load functions with native dependencies controlled. Prepared pinned source and clang++ are required; unavailable prerequisites explicitly skip. No game assets or live memory mutation are used.

- Initial RED: backup=false still writes the flag and group. Owner RED after the first guard: another loaded slot receives the old owner's data after backup becomes available.
- GREEN: unavailable/mismatching user/slot or failed backup causes no flag/group writes or file finalization; pending state survives. Original-owner positive retry works through load and settled paths; finalization occurs once, with once-only warning during backup failure.
- Commands: python -m unittest discover -s tests -p 'test_bbsc_*.py' -v: 2 PASS (B02+B03); python -m unittest discover -s tests -p test_native_bbsc.py -v: 2 PASS.
- Full suite python -m unittest discover -s tests: 159 tests, 1 failure, 8 errors, 48 skips, exit 1. Existing Windows symlink/shell/tool and packaged Vulkan/Nix limitations remain; no full-suite PASS claimed.

## Native persistence fixture

Original 3171-file manifest and copied B savedata protected before launch. One solo copied client; shared progress ON for this bounded fixture, guest items OFF, Discord OFF, experimental home recovery OFF. No bell, host join or new jointly-earned event. The synthetic BBSP intent contains only flag9453, independently already true on copied EiEi slot1. Payload is 20 bytes, SHA256 77d1a97059f0844253444971f5164d304de323716a3d8de296c361d44ae21f1b. It exercises native persistence lifecycle without granting new progress; it is not earned-event gameplay acceptance.

The copied save-backups directory was preserved and replaced by a regular test sentinel file, making the actual backup destination unusable. RED recovered user sd1/slot1 intent at 13:36:39 and renamed it .merged despite the fault; payload hash unchanged. All 1250 settled flag groups equal the protected B02 reload baseline. RED normally Quit to title and CloseMainWindow/WaitForExit both returned true; copied RED saves and merged intent protected before restoring the copied baseline.

GREEN recovered the same pending intent at 13:40:09. With the identical fault, pending payload remained exact and all 1250 groups equalled baseline. Loaded copied Kaori slot0 through normal Quit/Load. The existing 180-second timeout occurred at 13:43:10, keeping intent on disk before backup was restored at 13:43:26. Therefore this native wrong-character case proves file-key isolation, not the new in-memory owner guard (that guard has actual-function fixture proof). Kaori's 1250 groups were identical before/after unblocking; slot1 intent remained exact/unmerged. The real copied backup directory was restored after validating sentinel contents and all absolute move targets within the private workspace.

Original-owner positive retry: EiEi slot1 reloaded, recovered intent at 13:47:43, made an actual 18-file CUSA00207 backup (before-duel-bell-1792910869), then finalized the identical payload as .merged. Independent retried all-1250 snapshot equals baseline exactly; own Cathedral lamp2402950/position/heading retained. This uses an already-owned flag, so native new-flag application is not proven.

A second owner-switch attempt recovered at 13:49:00, but its 180-second timeout occurred at 13:52:00 before backup restoration at 13:52:04. Its Kaori before/after snapshots and pending payload remain exact. Neither timeout case proves the in-memory owner guard. Further identical loads were stopped; retain the fixture-only limitation.

Both RED/GREEN clients normally Quit to visually confirmed title and CloseMainWindow/WaitForExit returned true. GREEN launcher session53046 completed exit0; no bb-probe remains. Post-test copied savedata and synthetic pending intent are preserved privately, and copied pre-test savedata restored. Test pending data is removed from the ordinary copied profile. Original backup directory restored, including the new native test backup. assert-native.py PASS verifies RED/blocked/retried1250 groups, both Kaori comparisons, identical pending/merged bytes, actual18-file backup and fresh original3171 path/hash equality. Original saves were not modified.

## Remaining R03 acceptance

This fixes backup-result handling and owner retry at the existing merge. It does not prove backup completeness/partial-copy success, pending-file write/crash durability, or native in-memory wrong-character retry. Legacy receiver contamination by another later party, full-host history import, jointly-earned eligibility, actual reward failure/retry and consumed/owned de-duplication remain open. Custom managed application stays OFF. No exhaustive map sweep is needed; remaining candidate/routing/recovery and G2 acceptance remain required.

Private evidence: .superpowers/r03-b03/{before.cpp,hashes.json,*-red.log,owner-green.log,full-suite.log,build.log,native-red,native-green,before-savedata}. Secrets, raw logs, saves and assets stay ignored. Preserve unrelated FSR-Vulkan build dirt and the four external audit documents.

Usage checked periodically: latest 36%/6% consumed =64%/94% remaining, above the stop threshold. One reversible test edit was initially rejected by automatic approval review after it misread 9% used as 9% remaining. A fresh usage response established 90%/98% remaining; the same request with that evidence was approved. No bypass or original-save change.
