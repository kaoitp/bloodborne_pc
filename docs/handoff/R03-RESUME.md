# R03 new-session execution handoff

A02 final gate FAILED: pending recovery crossed from EiEi to Kaori after Quit Game/title. New durable-origin recovery is now experimental and OFF unless SHADPS4_BBSC_EXPERIMENTAL_HOME_RECOVERY=1; do not enable on user profiles. R03 remains IN_PROGRESS. See the blocking final gate in [A02 evidence](R03-A02-RECOVERY.md).

Latest A02: [native crash/profile/origin recovery checkpoint](R03-A02-RECOVERY.md). C01 null-table regression and copied native join passed; per-profile journal and original-point/invalid-point-lamp recovery now have bounded native evidence. G2 older-host import remains unchanged; full world/save integrity, host loss and remaining candidate/routing cases keep R03 IN_PROGRESS. Use the final local V5 DLL recipe and exact artifact hashes in that record; do not reuse older official artifact hashes as the tested A02 composition.

Latest A01 quota checkpoint: [four remaining acceptance groups](R03-ACCEPTANCE.md). User accepts representative maps. Wrong-word control behaved correctly, but progress inherits older host flags and a later guest crashed after placement. Recovery and full service independence remain unverified. Stop threshold reached at 9%/70%; resume from preserved crashed copies and the DLL progress/toolchain boundary, not an all-map sweep.

Prepared: 2026-10-24 (Asia/Bangkok). Owner: Codex, inline. Parent: [active R03 plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md). Read [Windows resume](WINDOWS-RESUME.md), [progress](../WINDOWS-PROGRESS.md), [R02 evidence](BBSC-BASELINE.md) and [product outcomes](../superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md). Latest checkpoint: [R04-J01](R04-JOIN-RELOAD.md) verified same-map and Cathedral Ward -> Dream joining, adjacent guest placement and normal own-world return after disabling the extra reload. Full G1/G2/G3 remain open; earlier failed attempts below are historical.

## Inputs available on this machine

Primary checkout: `C:/Projects/bloodborne_pc` on `seamless`. Private metadata pointer: `.superpowers/r03-resume.json` (ignored; no credentials stored). It records the user-authorized CUSA03173 dump/profile source, distinct ShadNet/game-server addresses and the paths below. Inspect privately; keep addresses, credentials, saves, assets and raw logs out of Git.

| Input | Existing local location / evidence |
|---|---|
| Source-built probe | `out/bb-probe.exe`, SHA256 `a948f6948d934f024f6089d976edf97bd915f0e46381cdeaad45d9595b1a27ca` |
| Gameplay DLL | `.superpowers/baseline/bbsc/bbsc.dll`, SHA256 `1df7d39e31c5d1acf034b5fd990b669e5e82944be477f26b0a46621a91610fdf` |
| Existing injector | `.superpowers/baseline/bbsc/bbsc-launch.exe`, SHA256 `c7fbaa406d972324645153bb8cc8bdad17fcd7db2f05026d67e3ba68f34750c1` |
| Manifest/notices | Same DLL folder; verify all hashes/mandatory markers from R02 record |
| Prior copied test data | `.superpowers/r02-test/profile-a/`; startup-only, not multiplayer-qualified |
| Private split-service redirects | `.superpowers/r02-test/profile-a/user/host_overrides.custom.json`; R02 SHA256 `d0bef3e27f19b3c42406a2f2422005a62ffb3ad229951fca812442020109b419` |
| Pinned BBSC reference / canonical patch | `.superpowers/reference/BBSC` at `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`; canonical patch `.superpowers/reference/bbport/bbport-1.7.2-bbsc.patch`, SHA256 `e34c79b388605998b430ec4eed556fc2cb8c8928f1d3e9f26bf5d2df29732aa3` |
| Toolchain | Existing `C:/msys64` CLANG64; compiler/package inventory and build recipe in R02 record |

The three main artifacts and six input path-presence checks were rechecked on 2026-10-24: PASS. No rebuild, launch or current service check was performed for this preparation. Treat later changes as invalidating affected evidence and recheck/rebuild only what changed. Fresh clone/different machine needs local reconstruction from R02; ignored paths are not in Git.

## Latest checkpoint: R03-L02 / R04-J01

Read [the bounded fix and RED/GREEN evidence](R04-JOIN-RELOAD.md) first. Baseline same-map and cross-map joining succeeded with distinct accounts even when copied CharaId matched; the earlier pre-claim failure was not reproduced. Cross-map second reload then broke guest departure. `run.py` now defaults existing `SHADPS4_BBSC_WARP_JOIN=0` for DLL launches, preserving explicit overrides. The fixed guest joined Dream, warped beside the host and returned to its Cathedral Ward origin. Direct emulator invocation bypasses this launcher default; explicit `1` restores the previous extra-reload behavior.

Both clients Quit Game and were normally closed; 3,171 original profile paths/hashes remain unchanged. All-map G1, all G2 and interrupted/disconnect G3 remain open. Resume with independent copied-world/progress snapshots, other supported routes and invalid-candidate checks; preserve baseline validation and keep managed application OFF. The native pad interface worked reliably with 100-120 ms pulses followed by clearing and 320-450 ms separation; longer pulses can repeat menu movement. Observe before confirmation/item use.

The following retry section records earlier observations; its failure hypothesis and next-step wording are superseded where the latest evidence differs.

## Current checkpoint and remaining work (2026-10-24 retry)

R03 is IN_PROGRESS. The latest [retry checkpoint](../WINDOWS-PROGRESS.md) supersedes the earlier second-machine WAIT_GAME limitation: two native clients ran/play concurrently. Windows grew its system-managed pagefile automatically; no system policy/runtime change was made, and future resource failure is not ruled out.

- Existing distinct authorized accounts remain available in ignored private `.superpowers/r03-retry/launch-test.ps1` (contains credentials; do not print/stage it). Both endpoints use the supplied replacement host. The old `.superpowers/r03-test` holds the previous sequential session, not the current retry evidence.
- Retry profiles `profile-a|b` under `.superpowers/r03-retry`, UDP 3658/3659, include original recovery-directory content; fresh original integrity passed 3171 files unchanged. Never use original saves for tests. Keep new per-character pre-join/recovery/progress/item snapshots before future persistence acceptance; current raw file hashes alone do not qualify G2/G3.
- Use the baseline's existing `BB_PAD_FILE` per-client files for reliable scripted menu input (named D-pad tokens and Cross, held for 150-600 ms, then empty file). User confirmed keyboard i/j/k/l + Space; OS synthetic taps were not observed to work. No input subsystem fix is scheduled. Observe each window and verify its current PID/HWND/profile/input binding before actions; repeated identical window titles confused automatic approval review until labeled proof was added.
- Both accounts authenticated, native hooks/DLL/redirects verified, and actual selected-account signaling reached ESTABLISHED/MUTUAL_ACTIVATED with bidirectional self-hosted UDP relay frames. In first same-map test, A/B were copied EiEi characters with the same visibly verified nonempty password. B explicitly deactivated after ~6 s and never joined; host stayed at zero cooperators. Claims subsequently expired/cleared. Exact logs/timelines/captures and process IDs are in the tracker.
- A distinct existing copied Kaori character loaded on B; Kin Bell use showed a crossed bell indicator and did not yield an equivalent claim/join test. Verify its bell-region eligibility/password and reset host search state before using it to decide whether character identity matters. The memory failure occurred before character load; do not conflate that with the current join failure.
- Latest offline diagnosis: current trace host passes 73/73 local-identity gates and builds two summons; guest has 89 scans, zero identity-pass/matched/build hooks, all observed candidates equal its own NP identity with user_id 0xffffffff. This may be normal self-advertisement filtering, not proven root cause. See the focused diagnosis checkpoint and ignored `join-identity-analysis.json`. First discriminate redacted claim identity/schema/consumption versus native game-handshake failure; do not bypass identity validation or patch teleport without proof. Final diagnostic usage was 10%/86%; honor the below-10% stop rule before restarting native work.
- Next: trace the native mutual-signaling -> explicit guest-deactivate boundary and actual game-socket/session/identity/room flow; inspect relevant delivered CL01 findings before any R04 proposal. G1 cross-map/Dream/placement and invalid candidates, all G2 and co-op G3 remain open. Custom admission/application OFF, no packaging/deployment/system changes.
- Both tests were normally exited; verify latest checkpoint cleanup/exits/original hashes and publication record before resuming. Native smoke checkbox remains complete; three gameplay checkboxes remain open.

## Historical join-fix leads (R03-L01)

[Historical comparison and next discriminators](R03-JOIN-LEADS.md) records pinned old fixes versus the active DLL baseline. L01 is VERIFIED for documentation only: use existing private HTTP capture to establish claim consumption and the first native handshake failure before proposing a patch. Selected-host/single-load and return-origin differences are downstream leads. R03/G1/G2/G3 remain open; no runtime changes or new native run. The user waived usage stopping for this investigation only.

## Execution order and completion checks

1. **Preflight.** Read current tracker and inspect origin/branch/worktree/dirty state and R02 ancestry using the Windows resume commands. Check usage. Verify source delta, dependency Gitlinks and artifact/manifest/notice hashes; reverse apply-check the canonical patch on this already-patched source. Preserve documented FSR-Vulkan build patches. Do not reapply R02 or replace source outputs with packaged executables. Record the exact tested source/artifact/config state and any missing input.
2. **Protect profiles.** Create fresh R03 test copies from user-authorized profile sources, with separate `BB_DATA_DIR`, `BB_USER_DIR`, `BB_GPU_USER_DIR`, `BB_CONFIG`, copied saves, logs and ports for each actual account. Snapshot original path/hash manifests before/after tests; preserve original-world recovery data required by the baseline. R02's prior 3,171-file manifest is historical evidence, not a substitute for the new snapshots. Inspect active game processes before launch and close only test processes started by this session.
3. **Verify routing independently.** Read private service addresses from the ignored input file. Recheck only required services and local configuration. Confirm actual protocol/authentication/peer exchange later; TCP connection alone is insufficient. Use the service table below, and record required public dependencies if actually observed. No server deployment, firewall/listener change or remote account administration is authorized.
4. **Native startup on the actual test configuration.** Reuse `run.py` with original `BB_PROBE` -> `bbsc-launch.exe` -> `BBSC_EMULATOR` -> source-built `bb-probe.exe`. Isolate inherited environment in the helper process, set absolute copied-profile/config paths and existing `SHADPS4_HTTP_HOST_OVERRIDES_JSON`. Verify loaded DLL path/hash, image validation, hook counts, redirect file and test save path. R02's offline startup remains historical evidence; it did not authenticate or exercise a peer. Complete relevant patch/native startup checks before checking the remaining R03 native-smoke box.
5. **G1 join.** With two distinct accounts/profiles, record pre-join own-world state and run same-map baseline plus same-nonempty-password supported cross-map/Hunter's Dream join, correct selected-host placement and locked-own-map guest visit. Test relevant wrong/stale/failed candidates without guest-world mutation. Use actual supported maps; Chalice excluded. Do not infer join from an open port or room listing.
6. **G2 progress.** Capture each player's initial progress/choices/relevant items. Exercise an eligible boss/story event earned together, distinguish it from the host's older history, preserve guest's earlier/NPC progress, and verify relevant reward non-duplication plus each player's independent save/reload. Eligibility across death/loading must be observed. Read source/Claude cases for a bounded verified event/reward set; do not design a whole-game catalogue or copy whole saves/flag groups.
7. **G3 departure/recovery.** Verify normal Blank/exit/disconnect, own-world restoration and valid original position or recorded fallback lamp; then interrupted-session process exit/reload on copied profiles. Cover unsupported-area departure where applicable. Any later persistence change requires its affected wrong-character/write-failure/crash/retry checks. Do not use the user's original save for interruption tests.
8. **Close the checkpoint.** Separate source/fixture/native/gameplay evidence; classify the three goals as EXISTING/PASS, PRESENT-NOT-TESTED, REPRODUCED-GAP or UNSUPPORTED. A gap requires the actual reproducible baseline symptom/source/config, not an unavailable optional port. Synchronize plan checkboxes and shared tracker, record commands/waited exits/counts/skips/hashes/private evidence locations/limitations/next action, commit and push origin/seamless without force. R04 starts only for demonstrated gaps with its five-part justification and relevant CL01 findings.

## Split-service configuration and last observations

Private addresses are in the local input file, not this document. Last checked on 2026-10-23:

| Endpoint / setting | Role | Last evidence / R03 work |
|---|---|---|
| ShadNet TCP 31313 | Account/matchmaking connection | Reachable only; actual authenticated exchange NOT RUN |
| ShadNet TCP 31315 / `BB_SHADNET_WEBAPI` | WebAPI/summon route | Reachable only; peer exchange NOT RUN |
| Game server TCP 20443 | Game API/discovery redirect | Reachable only; full protocol/returned routes need verification |
| Game server TCP 20444 / `BBSC_RELAY` | BBSC gameplay-mod relay (follow/world/session messages) | Unreachable then; recheck now, do not assume fixed or mandatory |
| Game server UDP 3478 / `SHADPS4_P2P_RELAY` | Pinned transport's relay override for split-service setup | Configured override; UDP protocol/peer use NOT RUN |
| Existing BBSC P2P channel | Gameplay-mod fallback when relay unavailable | Source present; runtime effectiveness NOT RUN |

The pinned native transport selects relay host from ShadNet by default; inspect/use its existing explicit override when services are split. The gameplay DLL has a separate relay/channel path. Do not conflate TCP 20444 with UDP 3478 or treat a configured override as a passing route. For game HTTP, `ss4.scej-network.jp:20443` redirects to the game-server host, while summon-messenger prefixes redirect to ShadNet WebAPI. Verify actual returned discovery routes against this split.

The user asked whether TCP 20444 belongs on the game server: it needs a running compatible relay/listener and allowed access, not just an open firewall rule. No server-side change or completed port opening was reported/authorized. If unavailable, investigate the existing client fallback and record the observation; do not redeploy. Preserve baseline auth and validation.

## Coordination and stop conditions

Claude owns only the four paths in [its work package](CLAUDE-CODE-WINDOWS.md). Inspect delivered audit status/branch when available; do not overwrite audit files, assume findings exist, or send messages to the other session without user authorization. Independent R03 work can proceed before CL01 completion. Revalidate affected source claims if either branch advances.

Keep custom managed admission/progress application OFF. No new loader/account/backend, unrelated renderer/input/launcher work, release EXE/ZIP packaging, live-server redeployment or use of old-repository PASS results. Check usage periodically; below 10% remaining in either window, stop new work, record and commit/publish the precise checkpoint. Missing gameplay inputs may leave honest partial results; never mark G1/G2/G3 complete from R02 native startup alone.
