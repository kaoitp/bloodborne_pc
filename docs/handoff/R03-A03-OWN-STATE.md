# R03-A03 ownership and own-state recovery checkpoint

Status: IN_PROGRESS, 2026-10-24/25 (Asia/Bangkok). R03 remains open. This record supersedes A02 only for the bounded observations below; it does not enable experimental recovery or qualify G2.

## Source and scope

Primary checkout `C:/Projects/bloodborne_pc`, `seamless`, starting HEAD `3ff3057cec333251799e585da3ab518263545e1d`. Pinned BBSC reference remains `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`. Existing FSR-Vulkan build dirt is preserved. Five-part justifications and IN_PROGRESS markers preceded each edit in [the tracker](../WINDOWS-PROGRESS.md).

Three demonstrated boundaries changed, within the existing DLL path:

1. Pending recovery must accept one requested ordinary load, then cancel on another load before replay. The ordinary respawn hook replaces reliance on the unobserved title callback. Save ownership candidates must have been written after the current load, rather than merely after process startup.
2. Capture the existing 57 Dream groups before the join resets them; initialize the existing Dream-own buffer from that kept copy. No new progress catalogue or group import.
3. Normal return must restore the recorded supported lamp alongside the existing original map/position/rotation. P02 returned to Cathedral but kept the host Dream lamp even after save/reload.

Custom managed admission/application stays OFF. New durable-origin recovery remains OFF unless exactly `SHADPS4_BBSC_EXPERIMENTAL_HOME_RECOVERY=1`. Private test harnesses opt in, disable shared progress and Discord for isolation; those settings are not changed product defaults. No release EXE/ZIP, server deployment, new account, system configuration or audit-owned document change.

## Fixture and build evidence

- Actual production-header ownership regression: unrequested load is rejected without mutation; one requested load accepted; repeated load rejected; a fresh request can accept again. RED assertion was observed against unconditional acceptance before the helper correction. Existing codec/invalid-position checks retained.
- `python -m unittest discover -s tests -p test_native_bbsc.py -v`: 2 PASS, CLANG64 clang++ on PATH. This compiles the real production headers; it does not prove gameplay.
- `python -m unittest discover -s tests -p test_run_bbsc.py -v`: 5 PASS.
- Full suite (initial run and final rerun after P03/temporary-candidate rollback, same results): `python -m unittest discover -s tests`, 157 tests, 1 failure, 8 errors, 48 skips, exit 1. Unchanged Windows symlink/shell and packaged Vulkan/Nix fixture categories; raw reports are ignored `.superpowers/r03-a03/full-suite.log` and `final-suite.log`. No full-suite PASS claim.
- `python tools/build_bbsc_mod.py .superpowers/reference/BBSC <output>` uses existing CLANG64, pinned fmt/xbyak and existing loader; all mandatory notices copied. Initial P02 compilation failed declaration order; helper return value fixed it, later build exited 0. No failed attempt is native PASS evidence.
- Tracked four-file reference patch reverse apply-check passes. A transient regeneration omitted two existing files; corrected before final publication. Complete patch still contains bbsc_http.cpp, bbsc_mod.cpp, bbsc_relay.cpp and bloodborne_re.cpp.

| Artifact | SHA256 | Native attribution |
|---|---|---|
| Source probe | `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14` | unchanged A02 shader correction |
| Original loader | `c7fbaa406d972324645153bb8cc8bdad17fcd7db2f05026d67e3ba68f34750c1` | reused |
| Ownership DLL | `ae205288879518b5a464ce6b06e0d255dbf97b76a6f16deb29a74a5fb3167d0a` | PID 13088 |
| P02 own-state DLL | `3ade8047fbdfec4b5aee4a7c23cf49361f4a6c9ca890bdf3a4b1da3b6bdf347f` | A 17012 / B 6408 |
| P03 return-lamp DLL | `5a360d76f61d2ff91971904ac66c894c4eaacf044d651478bc41f6e350ac8416` | A 8940 / B 6524, restart 2444 |

Build logs/exit files and versioned local DLL directories are ignored under `.superpowers/r03-a03`. Do not substitute older official DLL hashes for these test compositions.

## Native ownership gate

Ownership DLL, PID 13088/HWND 1509232, copied B, 159/159 hooks. Valid EiEi slot-1 journal SHA256 `9bcc9639fa3889f8cc4bd11bfccb0ad348f7ea6544bd4c0fd368823cd606a91d` held behind a completion-rename blocker. Actual requested return at 23:48:14; actual title observed after confirmed YES at 23:50:12, then blocker removed.

Loading Kaori slot 0 at 23:53:07 canceled pending replay before old flags were applied. The EiEi file retained its exact hash. Independent read-only memory snapshot: all 1,250 Kaori groups equal the A02 pre-search baseline, zero differences. The later no-join baseline differed only in its bell-search bit, so it is not substituted for this control.

Quit/Load EiEi slot 1 recovered its retained journal at 00:03:01; ordinary load at 00:03:03, finalization at 00:03:15. Independent own world 1/type 0/loading 0, map `0x18000000`, lamp 2402950, position `(15.770329, -9.511212, 103.839012)`, heading -0.868897. Normally closed afterward.

First setup attempt used too-short Cross and did not actually reach title; completion happened before the blocker step. Excluded from PASS. Observe title rather than assuming the input succeeded.

## P02 actual visit, return and host loss

Private evidence `.superpowers/r03-a03/native-own`; A 17012/HWND 329708, B 6408/HWND 264258. Fresh copied B selected EiEi slot 1. Before join, independent 1,250 groups and original position/lamp captured. Both clients used matching nonempty passwords. Native startup/image validation, 52 patch writes and 159/159 hooks observed.

- Cathedral -> host Dream join at 00:19:18: adjacent blue guest visibly observed. Actual durable journal exactly equals the pre-join capture for all 53 present members of the existing 57 Dream keys (four absent from native table). Groups 2/70000/70009 that failed the A02 real-data comparison now match. Actual journal size 126561 bytes.
- Blank return confirmed 00:20:39; existing own-world replay at 00:20:40, original Cathedral position restored. Settled comparison differs only group 9, 30 bits, against the first pre-join capture. Those bits remain unclassified; a local direct EMEVD setter scan found no matches, which is not harmlessness proof. The previously lost 18 own bits are preserved.
- Native Quit/Continue after return preserves all 1,250 settled groups exactly (SHA256 `4354cd1ef29f2df68bf5332d98622640b68f4d1ae3b38848755da745e1beaad5`). This is bounded own-state persistence, not G2 reward/event acceptance.
- Second join accepted 00:24:41, fully guest 00:24:53. A misleading intermediate sample name `failed-rejoin` was renamed `second-joined`; this eventual join is not failed-candidate evidence.
- Verified only test host PID 17012, protected copied host saves, then injected process loss at 00:25:14. Guest's existing 15 s watchdog returned it at 00:25:30, replay 00:25:31. Settled independent 1,250 groups exactly match the preceding own save/reload baseline; original coordinates restored. Initial loading-frame samples excluded.
- Lamp stays at host Dream 2102961 rather than original 2402950, including after normal save/reload: P03 reproduced gap, not a complete G3 PASS.

Guest later Quit Game and normally closed: CloseMainWindow true/exited true. Some premature menu inputs were sent before the rendered game settled and created blood bullets in the copied guest; excluded from inventory-integrity evidence. Use visible ready state and verify each menu.

## Remaining acceptance

- [x] Bounded pending-title/wrong-character isolation and positive owner retry on ownership DLL.
- [x] P02 independent pre-join Dream-key journal preservation and normal-return/save-reload preservation of the previously lost bits.
- [x] P02 actual host-process-loss return and settled world equality to preceding own baseline.
- [x] P03 bounded normal return/lamp equality/save-reload and actual interrupted guest/restart; group 9 integrity remains separate below.
- [ ] Initial journal write failure must be safely handled before admission; current call writes after accepting the summon and does not fail admission closed. Keep experimental recovery OFF.
- [ ] Classify group 9 changes and finish independent own-world/item integrity gates.
- [ ] G2 verified jointly earned boss/story/reward eligibility, old-history exclusion, duplicate/consumed reward handling and independent save/reload. Current production merge/reward policy is unchanged and not accepted.
- [ ] Remaining locked-own-map and stale/failed-candidate native controls plus complete required self-hosted-route correlation. No all-map sweep is required by the user.

G2 investigation retained local primary-source leads for the existing 19 reward events and their death conditions/SetFlag instructions; these are raw script leads, not a verified eligibility policy. Snapshot receipt time alone cannot prove an event was earned while both players were eligible. The corrected external audit branch was fetched read-only; it is not integrated or implementation-ready acceptance.

Next: address initial-write refusal at an earlier native admission boundary, then the demonstrated progress/reward boundaries. The rejected Lua skip is too late. Keep source, fixture and native/gameplay claims separate and update the active plan before publication. See final integrity/review/checkpoint state below; publication is recorded in the tracker after push.

## P03 final native updates

Guest 6524 was deliberately terminated only after visibly settled co-op and current save/journal protection. Journal SHA256 9ec07a68596f90d849e6fc716dc0983a398af3d5498edfb4c6300e25eaefa74b retained. Restart 2444 recovered at 00:39:35, ordinary home load 00:39:36: correct original map/coordinates/lamp and all 1,250 independent flag groups exactly equal the settled pre-join baseline.

A second real join with the initial .bin.tmp path blocked admitted the blue guest without any active .bin at 00:43:07: native storage gate RED. Exact sentinel and empty directory removed, the existing retry created a 126561-byte journal within 2 s; own-key comparison passed. P03 normal Blank return then restored the original Cathedral lamp 2402950 alongside the point/map. Group 9 again differs by the same 30 bits; other groups match. Native Quit/Continue preserves the entire settled state and original lamp exactly, zero group differences. First transient pointer read during the join load failed and was excluded; process remained alive and then joined normally.

Candidate P04 (SHA cb3706dcd85a2c490e905b7df423bbd99817c97a3375d0b4a87494a42fec34dd) FAILED native admission and was fully reverted. It reuses the existing Lua dispatcher skip flag under the existing experimental switch. Lifecycle effects run before capture-file/hit sampling gates. Build exit 0, 159/159 hooks on guest 20264; healthy host remains P03 8940. Revert candidate if refusal/retry is not clean.


## Rejected P04 and concrete next leads

At 00:55:57.149 candidate guest 20264 logged journal refusal, displayed its notice and suspended persistence after failing the initial write. The existing function-entry skip did run, yet the native session still entered Dream as a blue guest with no journal by 00:56:13. This dispatcher is too late to prevent admission; its message is not proof of cancellation. No clean-refusal/healthy-retry PASS. The temporary skip, cleanup helper and moved lifecycle code were fully reverted, including hook arguments. P03 is the retained implementation/artifact. The rejected source/patch, logs and copied suspect saves remain ignored under `.superpowers/r03-a03`; never resume from that suspect save as a clean baseline.

Candidate guest was deliberately terminated after preserving evidence. Exact test sentinel/empty directory removed; only copied B saves reset from the protected `.superpowers/r03-claim/before-b-savedata/1`. Final host 8940 Quit Game, title visibly verified, CloseMainWindow true/exited true. No game test process remains. Earlier P03 guest 2444 also normally closed; injected losses are explicitly identified above.

Two source leads need verification before another fix:

- Existing Lua lifecycle effects currently occur behind trace hit sampling and capture-file availability. Future admission work must preserve snapshots independently of logging, but moving them alone does not prevent the already-committed join. No trace-path change remains in this checkpoint.
- Group 9 investigation did scan 27 actual local EMEVD inputs. A broader argument scan found 78 matching instructions; many changed flags are parameters to `common` event 9040 (for example slot 2/flag 9042/lot 17000), whose body includes a parameterized flag wait and AwardItemLot. These are reward-related leads, not proof that the 30-bit delta is harmless or that all are NPC choices. Inspect EMEVD parameter bindings and NPC/script producers plus inventory effects; do not simply label the delta normal or restore entire global groups blindly.
- Existing selected-host `SHAD 0x27` boss-name messages and `BbscGaugeBossId` may help establish an encounter before a reward, but the current producer depends on optional messages and carries a boss name ID, not health or an earned-event receipt. They do not by themselves solve eligibility, late/reordered snapshots or death/loading continuity. G2 policy remains unchanged.

## Final integrity and review

Fresh original before/after path/hash comparison: **3,171 files each, zero differences**. Manifests are ignored `.superpowers/r03-a03/original-before.json` and `original-after.json`; no original save/profile was used for gameplay. Credentials/assets/raw logs/saves remain ignored. No audit-owned documents or FSR-Vulkan state changed.

Checkpoint SHA256 after complete candidate rollback (working bytes):

| Source | SHA256 |
|---|---|
| Pinned reference bloodborne_re.cpp | `6bd5cf815f71ff2a001985df3b7f5988d36729020e6a228406a7eee67b8b9bfa` |
| Complete tracked BBSC patch | `81389184105089c61d8d20ea5f2e4a2109550d011ac213bd7d4c8ac2360768e1` |
| Production home header | `d0451d1a04dff676e50fcd0c4a51f98323215b9911d37ce6a2d2e5dba886afb2` |
| Native header test | `bc8334cba197f30e8db31a152ecc65256fd28c17654c794d2a50dcc65d584f1c` |

Inline review against AGENTS, the active plan and product specification, base `3ff3057cec333251799e585da3ab518263545e1d`: Standards has no new blocker for the bounded three corrections; caller ownership, atomic-write status, existing notices/defaults and rollback reviewed. Spec is **partial**: own-origin/previously-lost-state cases improved, but initial-write refusal and G2/group-9/reward gates prevent complete acceptance. No subagents. Focused tests 5 launcher + 2 actual production-header tests PASS; final full suite remains 1 failure/8 errors/48 skips of 157, exit 1. Reverse patch check and diff whitespace pass. Compiler DWARF inspection exposed no source checksum, so it is not used as byte-identity proof.

Usage at cleanup: 14% primary/41% secondary remaining. Stop new work below 10% in either window and publish this checkpoint. Experimental recovery remains OFF by default. R03 and its three broad gameplay boxes remain IN_PROGRESS/open.
