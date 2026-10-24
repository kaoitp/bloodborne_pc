# R03-A02: native crash and interrupted return

2026-10-24, Asia/Bangkok. **IN_PROGRESS; R03 is not closed.** Source base `7d27c14`; this checkpoint extends J01 and preserves the complete pinned composition. Representative maps suffice. Codex worked inline using the implement/TDD/diagnosis/review workflow; no subagents, server deployment, system changes or release packaging.

## Demonstrated gaps and responsible changes

The five-part justifications were recorded IN_PROGRESS in the tracker before implementation:

| Task | Baseline symptom / dependency | Smallest responsible correction | Acceptance boundary |
|---|---|---|---|
| B01 local DLL build | Existing CLANG64 rejects only two MSVC `ifstream(wstring)` extensions; pinned reference and fmt/xbyak required | Pass the same wide path as `path.c_str()`; build the pinned sources and mandatory notices using the existing compiler | Build and native image/patch/hook checks; this alone proves no gameplay behavior |
| C01 crash | A01 guest null read at probe+0x1bae22 resolves to actual `Info::ReadUdReg<AmdGpu::Buffer>` | Return an empty descriptor when the decoded indirect table is null | Actual-header crash RED, valid/null/direct/offset/snapshot regressions, rebuilt probe and playable native join |
| R01 profile isolation | Actual DLL path driver ignored BB_USER_DIR; backup=false; journal rooted beside a shared DLL | Launcher exports its resolved profile; existing DLL GetUserPath/save scan/backup honor that root without APPDATA fallback when configured | A/B/Unicode root driver, launcher regression and actual profile backup/journal creation |
| R02 durable origin | Preserved crash reload stayed solo in Dream; original home point existed only in memory | Versioned home point/heading/lamp pseudo-group in the existing per-slot own-world journal; ordinary native return/load, retain journal through completion | Codec rejection/fallback, actual interruption/wrong-slot/retry/origin return; full safety acceptance remains open below |

The tracked BBSC patch applies to the **external pinned source**, not the canonical emulator patch again. `gpu/bbnet/bbsc_home_spot.h` is included by that DLL build. The source-built probe receives only C01. No new loader or backend. Existing valid join/follow/wipe callers retain session-phase and load-cover setup; own-world recovery skips those two session-specific steps. Existing respawn hook replays preserved world flags before map events and marks the recovery load observed. Quit-to-Title clears pending recovery in memory and retains its character's disk journal.

## Reproduction and builds

Pinned BBSC `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`; fmt `ec73fb72477d80926c758894a3ab2cb3994fd051`; xbyak `44a72f369268f7d552650891b296693e91db86bb`. Existing CLANG64 clang++ 23.1.3, target x86_64-w64-windows-gnu. Only fmt/xbyak were initialized in the ignored reference checkout. The builder checks the source pin, applies/reverse-checks the tracked patch, uses the pinned headers and copies LICENSE/NOTICE/SUPPORTERS. Static runtime avoids new libc++.dll deployment. Existing Windows DLLs remain system dependencies.

```powershell
$env:PATH='C:/msys64/clang64/bin;C:/Program Files/Git/cmd;'+$env:PATH
C:/msys64/clang64/bin/python.exe tools/build_bbsc_mod.py .superpowers/reference/BBSC .superpowers/r03-close/home-v5
C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p test_native_bbsc.py -v
C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p test_run_bbsc.py -v
C:/msys64/clang64/bin/python.exe -m py_compile run.py tools/build_bbsc_mod.py tests/test_native_bbsc.py tests/test_run_bbsc.py
git -C .superpowers/reference/BBSC apply --reverse --check C:/Projects/bloodborne_pc/gpu/patches/bbsc/0001-profile-storage-and-clang64.patch
git diff --ignore-submodules --check
```

Probe build: existing MSYS environment, explicit `cd /c/Projects/bloodborne_pc`, `source ./msys2-env.sh`, `ninja -C out/gpu -j 2 bb-probe`; 70 actions, exit 0. The first bash login-shell invocation changed cwd and failed before compilation. An initial fixture invocation lacked runtime PATH (0xc0000135), corrected before qualifying the actual null-table crash (0xc0000005). One source edit failed on implicit CP1252, another while compilation held the file; no native PASS is attributed to those attempts. Exact logs/exit records stay ignored.

Final local artifact SHA256:

| Artifact | SHA256 |
|---|---|
| out/bb-probe.exe | `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14` |
| home-v5/bbsc.dll | `0769852c0b03bfe757a34d814c4b135ef4ed5808a548b7e27625fb749fff08ed` |
| bbsc_home_spot.h | `3b239e10709cf6cf3601deb99df148fe583722796f40cb064b61893093a105be` |
| BBSC source patch | `5229de264303b1d9e933965695b131653fb51918bee809736cb3e9c0167d0435` |
| build_bbsc_mod.py | `305172dad973a997259a3cc2f5ed7141718164ff7a63f1f9fdec38618611bcd1` |

Original official DLL/loader hashes remain those in [R03 resume](R03-RESUME.md); the original loader is reused. Local output is private, not a release artifact. Copying code into this repository does not replace those official binaries automatically; select the local test DLL using existing `run.py --dll`.

## Fixture evidence

Actual production shader header: crash RED before C01, GREEN after; absent indirect table at offsets 0/4, tagged null, valid tagged indirect, direct registers and existing draw snapshot. Actual-DLL GetUserPath driver: RED exit 3 before R01, GREEN for separate A/B/Unicode roots after. This driver is a manual Windows/DLL boundary check, not a portable suite test; legacy/empty-root and Unicode file-read acceptance are not inferred from path equality.

Launcher: RED missing child BB_USER_DIR, then 5 tests PASS. Native compiler wrapper: 2 tests PASS, covering shader reader and real home codec. Home codec covers roundtrip, short/version/unsupported-map rejection, NaN with valid lamp fallback, NaN without usable lamp rejection, existing 20,000-unit bound and zero origin; range test was RED before alignment. These are fixture results, not gameplay proof.

Full suite run once: **157 tests, 1 failure, 8 errors, 48 skips, exit 1**. Unchanged Windows symlink privileges, shell tools and packaged Vulkan/Nix assumptions remain; same categories were present at J01. No full-suite PASS. Focused tests were rerun after affected changes. Raw full-suite output is `.superpowers/r03-close/full-suite.log`.

## Native sequence

All profiles are copies; original manifest captured fresh before A02. Existing distinct accounts and self-hosted settings were reused. **Shared-progress and optional Discord were explicitly OFF only in this G1/G3 test harness**; product progress defaults are unchanged. This run cannot qualify G2. First local profile-DLL startup was disabled by missing mandatory notices; both clients closed, exact pinned notices restored, builder corrected. Do not count those disabled clients.

Home DLL v1 SHA256 `faf1a7964faaa6526b422f58718034668551472c3caace0f0a93177034b027ac`: host PID 19892/HWND 199012, guest 3096/HWND 788844. Both image validation/52 patch writes/159 hooks passed and native mod relays connected. B's correct profile backup and per-slot journal were created. Kaori's crossed Kin Bell did not join despite matching nonempty words; cause remains unconfirmed. An independent snapshot changed flag 12415010; no mutation-free negative PASS.

B then selected known copied EiEi slot 1 in Cathedral Ward, joined A's Dream and appeared as a blue guest beside its host. Movement was observed, no repeat of the original C01 crash before controlled termination. The journal recorded origin map 0x18000000, lamp 2402950, position (15.770329, -9.511212, 103.839012), heading -0.868897. It contains 981 groups: 979 real groups plus time/home records, 126561 bytes. A had no active recovery journal. Guest 3096 was deliberately stopped; original interrupted saves/journal preserved before restart.

Restart B PID 380: loading Kaori slot 0 left EiEi's journal untouched (SHA256 `9bcc9639fa3889f8cc4bd11bfccb0ad348f7ea6544bd4c0fd368823cd606a91d`) and triggered no recovery. Normal Quit/Load EiEi with journal truncated by one byte left it retained with no recovery. Restoring the complete copy caused the poll to retry. The first warp incorrectly set guest phase and eventually reached title; fixed by preserving ordinary own-world phase. No PASS for that attempt.

V3 guest PID 10872 with DLL `7e576890fd229e39aee26c886a1e1f9a6516616064fa03b372c7e9c108921a17` restored Cathedral Ward at the exact recorded point/heading; independent read-only process memory confirmed own_world=1, character_type=0, loading=0. Journal remained pending because the original completion marker watched a guest-only load hook. The existing ordinary respawn hook was then used.

V4 guest PID 12856/HWND 72419706, DLL `1fefcd803c65ce6d9165d71bf8a28cea86ef643c79ecf2fe401787be61414a7e`: 19:25:48 restoration/warp, 19:25:49 ordinary-load replay, exact independent original coordinates and own-world type. A nonempty directory deliberately occupied the copied journal's `.restored` destination: recovery retained its complete journal and waited. Removing only that test sentinel/empty directory at 19:27:50 let retry finalize automatically; journal renamed to `.restored`. This proves completion-rename failure retention, **not** failure to create the initial journal.

Independent snapshots before join and after V3/V4 contain 1250 groups. Eighteen cleared flags remain unclassified: 2300, 2410, 2411, 2412, 2800, 70000030, and 70009260 through 70009370 in steps of ten. No non-global map group difference was observed, but do not claim complete world/NPC/item preservation from these results. Raw snapshots/deltas and the exact journal are preserved for the next discriminator.

## Remaining gates and private evidence

Private `.superpowers/r03-close` holds manifests, compiled drivers, build logs, artifact manifests, copied saves, read-only snapshots and native-home/native-recover/native-recover-v3/v4/native-fallback evidence. Hooks/timelines/HTTP captures also remain under copied profile user/captures. Helpers contain credentials; never print/stage them. The native pad interface uses short pulses; no input subsystem patch. Existing FSR-Vulkan dirt is preserved.

G1 join/placement is bounded native evidence; final-DLL normal departure and stale/failed-candidate integrity remain open. C01 avoids the reproduced null read, not every possible renderer crash. R02 still requires final-source lifecycle/cross-character pending recovery, initial-write failure, independent save/reload integrity and controlled host loss. Legacy journals have no position and cannot invent an origin; current finite/range checks do not prove arbitrary terrain is safe. Chalice remains unsupported.

G2 remains **REPRODUCED-GAP**, unchanged. No boss/story event was earned together and no reward/save-reload test was performed. Do not promote receipt-time baselines or first snapshot differences into event-time eligibility; CL02-P01 is still CHANGES REQUESTED. Next use its verified finite event/reward mapping with actual party eligibility and ordered producer/consumer evidence; do not copy whole host progress or merely disable progress to claim completion.

G4: native joins used configured self-hosted ShadNet/HTTP/mod relay with optional Discord OFF. Joined socket snapshot has two ShadNet and two mod-relay connections. UDP fallback and complete progress/no-required-public-route correlation remain unqualified. No server/firewall changes. R03's three gameplay checkboxes stay open.

### Final-source fallback observation

Final V5 guest PID 22544/HWND 395654 passed image validation and 159/159 hooks. With a NaN original coordinate and the preserved lamp, native recovery requested lamp 2402950 at 19:32:18, replayed own-world flags during the ordinary load, and finalized at 19:32:32. Independent process memory: Cathedral Ward 0x18000000, own_world=1, character_type=0, loading=0, position (17.58, -9.509977, 102.65), heading 2.094395. Visual solo player stood at the recorded Cathedral lamp. This qualifies the bounded invalid-point fallback on the final DLL. The subsequent attempt to place a completion blocker happened after finalization, so it is not counted as a second storage-failure case.

### Blocking final gate and containment (supersedes earlier recovery acceptance)

The pending-title test **FAILED** on V5: after replaying the completed copied journal under a deliberately blocked completion target, Quit Game -> title -> Load Kaori slot 0 did not clear the pending EiEi slot 1 recovery. At 19:39:35 the ordinary load replayed EiEi's 979 groups into Kaori (607 differing flags), and at 19:39:49 consumed EiEi's journal. The existing RegistReturnTitle hook was installed but no callback log appeared for this menu path. Initial wrong-slot loading before a recovery is pending passed; that does not cover this failure. The copied Kaori save is affected and must be reset from its preserved source before further integrity testing. Originals remain untouched.

**R02 is an experimental prototype, not accepted functionality.** The checkpoint now requires exactly `SHADPS4_BBSC_EXPERIMENTAL_HOME_RECOVERY=1` before enabling its new durable-origin warp. Unset/0/10 do not enable it; focused production-header configuration checks pass. Existing per-slot flag-journal behavior remains available; this gate contains the new pending-origin state. Do not enable it on user profiles or treat V1-V5 gameplay as final-source acceptance. The final contained V6 build is not gameplay-qualified. This is a temporary safety boundary until active-character ownership and the actual menu lifecycle are established; simply adding another unverified title hook is not a fix.

Final contained source SHA256: home header `d84333ec624c85872c6da08aeead6b887a3b81ec01ac59e36b777671ee7454b5`; source patch `08d3fefd723c6a23bbbc2935fc12aa4c394c7ece05ba98791f1578215063cfc5`. The earlier artifact table records the V5 experiment; these source hashes supersede its header/patch rows. Ordinary build outputs remain ignored.

Inline Standards/Spec review against base 7d27c14 covered all runtime/build/tests/doc paths. Valid shader reads and existing session callers remain intact. The new persistence parser rejects partial records before mutation. Spec review found the blocking pending-character defect above and unclassified global differences; containment is verified by focused default-off checks, not a claim that R02 is fixed. The whole R03 acceptance remains open. No audit-owned document was edited. Profile-root changes do not automatically migrate legacy files from a shared mod directory.

Original profile integrity: fresh before/after 3171 paths/hashes, zero differences. Host Quit Game and normal window exit observed. Native tests stop at this checkpoint; copied evidence is retained. Next: fix pending recovery ownership/menu lifecycle before enabling R02; independently classify the 18 flag differences; then G2 verified jointly earned events/rewards, host loss, initial journal write failure and remaining candidate/routing checks. Do not resume with an all-map sweep.

Contained V6 build: exit 0; DLL SHA256 `ca5f086a6718da74e3e418e597a9cbe554c5a33cf886d6e1e7d7634d2aad42b9`. Final focused native boundary suite: 2 PASS including experimental OFF/explicit-1 checks; launcher 5 PASS; syntax and patch reverse-check PASS. V6 was compiled but not launched. No release packaging or live deployment.
