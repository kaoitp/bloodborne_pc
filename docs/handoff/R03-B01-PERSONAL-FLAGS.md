# R03-B01 personal common-event flags

2026-10-25, Codex inline, source base f956f2bdd19eac1f137910b2a80c799e35cd322e. B01 bounded preservation PASS; R03 remains IN_PROGRESS. [Parent plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md), [tracker](../WINDOWS-PROGRESS.md), [A04 admission evidence](R03-A04-ADMISSION.md).

## Demonstrated gap and smallest correction

Actual A04 independent prejoin/returned/reloaded native captures show exactly 29 group-9 flags false -> true despite shared progress disabled. Existing Dream restore keeps bits changed after its host write; that also retained guest-side personal event completion. Read-only inspection of actual retained DLL own/written group-9 buffers found all 29 false while returned live bits were true. Actual common EMEVD initializers account for 27 as event+slot completions (9040/9100); common event 50 initializes the other two, 9722/9723. Their script bodies test character 10000/type 0 and end for guests before reward/quest mutation. The existing player-type hook preserves vanilla common.emevd answers. This supports completion-without-award as the cause; NPC interactions were not performed in this test.

Extend only the existing BbscDreamShopUnlockFlags table from 130 to 159 entries. Keep all original entries unchanged. The existing KeepBbscOwnDreamShopFlags helper copies each selected bit from the original own snapshot, preserving both true and false values, in both host application and return restoration. No new merge algorithm, whole-group rollback, inventory injection, protocol, event framework or shared-progress policy. Original shop-stock/purchase handling remains in the existing helper.

The demonstrated added flags are 9042, 9045, 9046, 9048, 9049, 9050, 9051, 9052, 9054, 9055, 9056, 9057, 9059, 9060, 9061, 9062, 9063, 9064, 9071, 9073, 9075, 9076, 9077, 9100, 9101, 9102, 9104, 9722, 9723. Actual asset inspection and native captures remain ignored under .superpowers/r03-a04 and .superpowers/r03-b01.

## Source and artifact attribution

Pinned reference HEAD remains 4f11faf88b6ba658ebde6fe5fbefdadedba4fa41. The tracked BBSC patch still has all four destinations (HTTP, mod, relay, bloodborne_re); reverse-apply check passed.

| Input | SHA256 |
|---|---|
| Modified reference bloodborne_re.cpp | 2aaf0537a34d66b52b8470a40e35c57fde3ea02bf963aa58c89a816da5c08985 |
| Complete tracked BBSC patch | 81f18b897e3bb5cc9061570fbbdada36e481bfbb0475846aa571b369a0c52b40 |
| Local B01 guest DLL | 390fe83fdd8f242c23949d980b720ed8fb41d9dc3c59d753edc6e62b6d536b43 |

Build: PATH with C:/msys64/clang64/bin, python tools/build_bbsc_mod.py .superpowers/reference/BBSC .superpowers/r03-b01/personal-dll; exit 0. Source-built probe and original injector are unchanged from A04. Native guest 8344/HWND 264222 loaded the B01 DLL with 160/160 hooks. Host 19980/HWND 67340 still used the earlier A04 wait-candidate DLL fe255e63e83453893c5df7022be4417395004f5cd25b97900dedd3b77e2f31a2; its changed guest-only wait path does not run while hosting. This mixed diagnostic pair is not a final pair/release gate. No release package or deployment.

## Fixture and native results

- RED before edit: assert-personal.py against actual A04 prejoin/return found all 29 differences, AssertionError/exit 1.
- Finite-set self-check: original 130 entries unchanged, exactly the demonstrated 29 additions, 159 unique; PASS. Both helper call sites reviewed; original-true behavior established from existing mask semantics, not a new NPC gameplay case.
- Focused native-header tests (python -m unittest discover -s tests -p test_native_bbsc.py -v): 2 PASS. Full suite once on B01 source (python -m unittest discover -s tests): 157 tests, 1 failure, 8 errors, 48 skips, exit 1. The Windows symlink/shell/tool and packaged Vulkan/Nix fixture limitations remain; this is not a full-suite PASS. Logs and exit records are ignored in .superpowers/r03-b01.
- Protected A04 saves before resetting only copied B from the preserved source; independent fresh prejoin captured 1250 groups. Original manifest freshly captured 3171 files.
- Actual host claim delivery required retries before native JoinSession_White at 07:50:58.712; summoned reload completed 07:51:10.041. No claim alone counted as join. Independent settled guest own=0/type=1/map 0x15000000 and coordinates (-7.947823, -6.825601, -20.010328) equal the selected host. Blue cooperator visible in the subsequent Blank confirmation.
- Copied journal matched all 53 present members of the existing 57 Dream keys; four absent. No new key catalogue.
- Normal Blank began 07:52:36.639; native return restored Cathedral original point and lamp. An early sample while the return sequence was still settling differed in map-script groups and global 2020/2021; retained as guest-returned-world.json and explicitly excluded from settled acceptance. Inputs sent too early during that load triggered a blood-bullet action on the copied guest; this was not a reward test.
- Settled native guest-settled-world.json equals prejoin in all 1250 groups, zero differing bits, including all 29 personal flags. Both snapshots have SHA256 e62c19dd3e14f5ea70d96da8ed8aa829b0c5a5523247ea900a731d6635104839.
- Actual Quit Game -> title -> Play Online -> Continue; guest-reloaded-world.json again equals prejoin in all 1250 groups. Returned/reloaded own=1/type=0/loading=0, Cathedral map 0x18000000, lamp 2402950, position (14.028195, -9.508328, 105.312050), heading -0.868897 match. The baseline captured before ringing was (15.770329, -9.511212, 103.839012); bell animation moved the guest before the actual admission snapshot. The journal origin, not the earlier standing point, defines this return.
- assert-final.py verifies exact prejoin/settled/reloaded flag equality, return/reload point/lamp equality, all 53 journal keys and original 3171-file set/hashes unchanged; PASS. assert-personal.py returned []/exit 0 for return and reload. compare-world.py settled/reload output {} / exit 0.
- Both test clients Quit Game and title was visually observed, then verified PID/path/HWND CloseMainWindow=True and WaitForExit=True; no remaining bb-probe process. No original save was played or modified.

Representative commands (C:/msys64/clang64/bin/python.exe): .superpowers/r03-close/read-position.py PID OUT; read-world.py PID OUT; .superpowers/r03-a03/compare-world.py BEFORE AFTER DELTA; .superpowers/r03-b01/assert-personal.py BEFORE AFTER; .superpowers/r03-b01/assert-final.py; check-set.py. All quoted GREEN assertions actually ran. Input used existing BB_PAD_FILE with observed menu confirmations; private atomic pad helper uses 110 ms direction / 300 ms action pulses, empty clears and 1000 ms gaps. Wait for loads/commands to finish before input or acceptance snapshots.

## Review and remaining R03 gates

Inline Standards review against AGENTS and existing code: bounded table-only delta, existing helper reused, all prior patch destinations preserved, no new blocker in this change. Inline Spec review: B01 personal completion leak corrected in the demonstrated non-interacting Dream visit. No claim of full R03/G2 completion. User representative-map waiver remains; do not launch an all-map sweep.

Shared progress and Discord are disabled in this diagnostic harness; experimental home recovery is explicitly opted in only on copied profiles, OFF by default. This run did not earn a boss/story reward together or exercise NPC dialog/purchases, old-host-history exclusion, duplicate/consumed rewards, or eligibility across death/loading. G2 production snapshot/reward behavior remains a demonstrated gap; do not substitute a naive first-packet delta for event eligibility (late history, first eligible kill, reordering and continuity remain unresolved). Locked-own-map, stale/failed candidate, complete required-service routing and remaining recovery enablement/final-pair checks stay open. Next: implement the smallest evidence-backed G2 event/reward correction and verify its bounded earned-event cases, then remaining candidate/routing/recovery gates. No managed application enablement.

Latest usage at checkpoint preparation: 11% primary / 24% secondary remaining. Complete publication; stop new work if either drops below 10%. Preserve FSR-Vulkan submodule dirt and external audit-owned documents.