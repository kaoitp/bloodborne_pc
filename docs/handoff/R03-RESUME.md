# R03 new-session execution handoff

Prepared: 2026-10-24 (Asia/Bangkok). Owner: Codex, inline. Parent: [active R03 plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md). Read [Windows resume](WINDOWS-RESUME.md), [progress](../WINDOWS-PROGRESS.md), [R02 evidence](BBSC-BASELINE.md) and [product outcomes](../superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md). This document prepares a session; it does not start R03 gameplay or pass any gate.

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

## Remaining user-dependent inputs

- Two **distinct existing authorized accounts** for the actual self-hosted route, with separate copied profiles and per-client ports. Account credentials and a second client's profile/machine have not been provided in this handoff. One duplicated login is not two clients; do not create accounts implicitly.
- Inspect existing authorized private test configuration or offer user-controlled secure login; ask only for missing account/config/profile paths or the second player's availability. Never ask the user to paste a password/token into chat or put it in a tracked document.
- Two clients may run on separate authorized machines or locally if resources and port isolation permit. Preserve original save files, active user processes and account identity. Do not assume the external Claude collaborator is the second player; CL01 is a source audit.

If these are missing, record the exact dependency and complete independent preflight/source/service checks. R03 remains WAIT_GAME for dependent gameplay until setup is ready; mark the specific authorized active work IN_PROGRESS before edits/tests. Do not stall available work or manufacture a second identity. The user's deployed server source/version remains unknown; do not repeat that question.

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
