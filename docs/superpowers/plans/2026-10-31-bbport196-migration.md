# BBport 1.7.2 to 1.9.6 Migration Implementation Plan

> **For agentic workers:** When the owner starts migration, use superpowers:executing-plans task-by-task, inline without subagents as required by AGENTS.md. This request prepares the plan only.

**Goal:** Preserve our supported-map seamless join, jointly earned progress/rewards and self-hosted flow while moving the BBport runtime from 1.7.2 to the pinned 1.9.6 release.

**Architecture:** Integrate pinned upstream 1.9.6 in an isolated checkout descending from `seamless`, preserving history. Reuse its network stack and our external BBSC DLL; carry only demonstrated compatibility gaps into the new stack. Keep a verified 1.7.2 composition and copied profiles for comparison and rollback.

**Tech Stack:** Windows/MSYS2 CLANG64, C/C++, Python unittest, existing BBSC DLL/injector, shadNet, game/summon services and relay.

**Spec:** [Product outcomes](../specs/2026-10-18-bbsc-anywhere-coop-design.md), [baseline plan](2026-10-23-bbport172-bbsc002-alignment.md) and [current source/playtest contract](2026-10-31-r03-playtest-follow-up.md).

**Status:** PLAN READY; migration implementation NOT STARTED. Prepared 2026-10-31 (Asia/Bangkok). Source/offline work belongs to the implementer; game launches and multiplayer playtest belong to the user. Existing PT08/PT09 feedback remains pending, independently of this plan.

## Global constraints

- Current production/test baseline remains BBport 1.7.2 + BBSC 0.0.2 + our tracked R03 changes until the owner starts migration and a candidate is qualified. Preparing this plan does not replace that baseline.
- Preserve main-story/Hunter's Dream scope, same nonempty cross-map password, selected-host placement, personal progress/NPC choices, original-owner pending delivery, safe return and self-hosted required routes. Chalice remains excluded.
- Preserve upstream graphics, input, launcher and unrelated online behavior. Reuse existing mechanisms before adding code; do not copy the old network tree over 1.9.6.
- Use copied profiles. Keep credentials, saves, assets, binaries and raw logs outside Git. Keep source, fixture, artifact and user-gameplay evidence separate.
- Keep experimental/custom managed admission/progress defaults OFF pending their existing native gates. Carry deliberate copied-test settings explicitly; migration does not close open R03 gates.
- Agent work is source/build/offline verification only. No agent-run game, release EXE/ZIP packaging, release upload or live-server redeployment is scheduled. The prior local playtest ZIP authorization does not authorize a new migration package.
- Publish reviewable checkpoints to `origin/seamless` with normal history only. Check available usage periodically; below 10% in either window, stop new work and record/commit the checkpoint.

## Pins and existing evidence

| Input | Exact identity / meaning |
| --- | --- |
| BBport 1.7.2 | `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d` |
| Current inspected `seamless` | `4605c9b57a8e51e371ad81006d149aa22b717c84`; runtime source delivery `b3fa095a3513e00dff6ac638ac10b547f6401b26` |
| Target BBport 1.9.6 | `41fa92047006ed5c78b833c3f68a8ecfdc601361`; use this commit, not a moving branch |
| BBSC 0.0.2 source | `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41` plus our complete tracked four-destination patch |
| Current integrated patch, normalized LF SHA256 | `c4a3f65839affd1ab8224d32e3a3a3b491770623f2cd5c535be724beb4df2c8e` |
| Current DLL, recorded SHA256 | `fc4d851a321abf59c5a57d211e1154d9b9cbc39880e4fa5bc8082eca8249307c`; [source/build evidence](../../handoff/R03-PLAYTEST-SOURCE-FIX.md), not a new 1.9.6 result |

The inspected upstream range contains 473 commits and 642 changed paths, including renames/deletions and unrelated systems. These are comparison counts, not a count of required edits. `gpu/third_party/fsr-vulkan` remains pinned at `c64f093404125e960813f95f1996c14780f0dd69` in both tags; build files and tracked patches still differ.

2026-10-31 source checks: `git rev-parse HEAD windows-v1.7.2 windows-v1.9.6` matched the pins; `git diff --shortstat windows-v1.7.2 windows-v1.9.6` reported 642 files, 120363 insertions and 100417 deletions; `git apply --check --directory=.superpowers/compat-196-check C:/Projects/BBSC/bbport/bbport-1.7.2-bbsc.patch` exited1 against exported 1.9.6 destinations. Missing/replaced network files and conflicting glue/header hunks make the original 15-destination patch unsuitable for direct application. These are static checks, not a build or DLL compatibility failure.

| Finding | Primary source / execution implication |
| --- | --- |
| Network moved to shadPS4 0.20 vendor sources | [Port inventory](https://github.com/Supermedo/bloodborne_pc/blob/41fa92047006ed5c78b833c3f68a8ecfdc601361/gpu/bbnet/SHADNET-PORT.md); integration lives under `gpu/bbnet/vendor/shadps4/` and `gpu/CMakeLists.txt`. |
| Launcher recognizes BBSC starts and otherwise settles the public pool | [`started_by_bbsc`, `settled_pool`, `game_environment`](https://github.com/Supermedo/bloodborne_pc/blob/41fa92047006ed5c78b833c3f68a8ecfdc601361/launcher/bbport_launcher_win.py#L839); preserve the intended server and injector through every supported start route. |
| BBSC saves move under `<user>/seamless-coop` | [`coop_user_dir`](https://github.com/Supermedo/bloodborne_pc/blob/41fa92047006ed5c78b833c3f68a8ecfdc601361/run.py#L413); native `--user`, DLL `BB_USER_DIR`, `BBSC_SAVE_DIR` and owner-bound journals must agree. |
| Game P2P relay framing changes | [1.9.6 `SMRL`](https://github.com/Supermedo/bloodborne_pc/blob/41fa92047006ed5c78b833c3f68a8ecfdc601361/gpu/bbnet/vendor/shadps4/core/net/p2p_transport.cpp#L273) versus current `BBR1` in `gpu/shadps4/core/libraries/network/p2p_sockets.cpp` and inspected sibling `bbsc_server/gameserver/bbhost_service.py`. Actual deployed server identity is not verified. |
| shadNet protocol version stays1, but commands expand | [Target client contract](https://github.com/Supermedo/bloodborne_pc/blob/41fa92047006ed5c78b833c3f68a8ecfdc601361/gpu/bbnet/vendor/shadps4/shadnet/client.h). Common explicit command IDs match inspected sibling server `vendor/shadnet/src/protocol.h`; commands including `SetClientVersion=13` and `LookupOnlineId=41` are absent there. Version equality alone is insufficient. |
| DLL already supplies HTTP wrappers and its own channel | Pinned BBSC `emulator/mod/bbsc_http.cpp`, `bbsc_channel.cpp`, `bbsc_hooks.cpp`; the same-game import slots/byte checks offer a reuse path. This does not establish successful hooks on the target runtime. |

## File responsibilities

| Files | Responsibility / treatment |
| --- | --- |
| `run.py`; `launcher/bbport_launcher_win.py` | Existing launch/server selection, single join-load guard and consistent save/profile paths. Extend existing helpers instead of introducing a second launcher. |
| `gpu/patches/bbsc/0001-profile-storage-and-clang64.patch`; `gpu/bbnet/bbsc_home_spot.h`; `tools/build_bbsc_mod.py` | Carry the complete current DLL/recovery implementation and reproducible build. Gameplay source remains `emulator/src/core/bloodborne_re.cpp` in the pinned ignored reference; every change must reach the tracked patch. |
| `gpu/bbnet/bbnet_glue.cpp`; target `gpu/bbnet/vendor/shadps4/core/libraries/np/np_matching2/np_matching2_mm.cpp`, `np/signaling_handler.cpp`, `np/np_utility/np_utility.cpp`; target `core/net/p2p_transport.cpp`, `libraries/net/net_p2p.cpp` | Network integration, lookup/rejoin and required relay compatibility. Modify only boundaries proved missing after testing existing target behavior. |
| Target `gpu/bbnet/vendor/shadps4/core/libraries/network/http.cpp`; pinned DLL `emulator/mod/bbsc_http.cpp` and `bbsc_channel.cpp` | Verify URL rewriting, host placement and BBSC traffic at the DLL boundary first. The target HTTP helper lacks old path-prefix/seamless routing, but DLL wrappers may supply it; do not automatically restore duplicate routing. |
| `gpu/CMakeLists.txt`; `build.sh`; `gpu/patches/fsr-vulkan/`; `gpu/shadps4/shader_recompiler/info.h`; `gpu/shim/window.cpp` | Preserve target build/renderer fixes; reconcile our null-table and optional `BB_WINDOW_RECT` changes with target equivalents. Avoid unrelated rendering work. |
| `packaging/windows/package.sh` | Review integration only: preserve target Windows certificate trust changes; do not blindly retain the local Python certificate-bundle workaround or run packaging. |
| `tests/test_run_bbsc.py`; target `tests/test_run_coop.py`, `tests/test_launcher_hunters.py`; `tests/test_bbsc_*.py`; `tests/test_native_bbsc.py`; `tests/native/` | Extend launch/profile contracts; retain actual-function role/progress/reward/recovery fixtures and native-header checks. Missing ignored sources/skips are not PASS. |
| Sibling `bbsc_server/vendor/shadnet/src/protocol.h`, `client_session.cpp`, `shadnet.proto`; `gameserver/bbhost_service.py`; `tests/smoke.py` | Read compatibility contracts first. Server changes are conditional on MG04 evidence and require that repository's own instructions; this plan does not deploy them. |

## Review focus

1. Existing characters and pending obligations remain with their owner when paths move, including same-name/different-slot characters (MG02).
2. Launcher restart/shortcut/pool selection preserves intended injector, private services and explicit overrides (MG02).
3. Direct P2P success does not conceal a broken required relay or unsupported shadNet command (MG04).
4. A joint kill survives return/reload without old-host history, transient boss-combat replay or duplicate consumed rewards (MG03/MG06).
5. Failure/crash leaves the 1.7.2 comparison copy and its journals usable; candidate data never flows back into that copy automatically (MG01/MG06).

## Execution queue

| Done | ID / status | Dependencies | Deliverable |
| --- | --- | --- | --- |
| [x] | MG00 / PLAN READY | Source inspection and owner request | This saved plan, linked from the active plan/tracker; implementation not started. |
| [ ] | MG01 / WAITING FOR MIGRATION START | Owner starts implementation | Isolated history-preserving target integration and verified comparison inputs. |
| [ ] | MG02 / PENDING | MG01 | Correct launcher/server/profile/journal contracts. |
| [ ] | MG03 / PENDING | MG02 | Reused current DLL, complete patch and focused offline regressions. |
| [ ] | MG04 / PENDING | MG01; MG02/MG03 for integrated checks | Minimal self-hosted matchmaking/P2P/relay compatibility. |
| [ ] | MG05 / PENDING | MG02-MG04 | Same-source clean target build and offline evidence. |
| [ ] | MG06 / USER PLAYTEST PENDING | MG05 | User gameplay comparison, acceptance report and rollback decision. |

### MG01: Freeze comparison inputs and integrate upstream

- [ ] Re-read current tracker and PT08/PT09 feedback, inspect all worktree/remote changes, then mark MG01 IN_PROGRESS. Record unresolved 1.7.2 symptoms separately from new migration failures; full R03 closure is not a prerequisite for source exploration.
- [ ] Preserve the recorded 1.7.2 DLL/runtime/configuration hashes and copied saves **with** own-world/progress/reward journals. Verify the copied file manifest before proceeding. Keep originals and the existing playtest installation untouched.
- [ ] Use a dedicated worktree/branch such as `codex/bbport196-migration` descending from current `seamless`; integrate exact target `41fa920...` with a normal merge. Resolve old-network modify/delete conflicts toward target architecture, retaining necessary behavior through MG02-MG04. Keep all source history.
- [ ] Produce a conflict/disposition inventory for the 15 baseline patch destinations and later local changes. Identify already-covered behavior (including NP utility registration and stronger null-pointer guards), required ports, and obsolete stubs. Acceptance: every local runtime delta has an explicit destination or evidence-backed retirement; both historical pins remain reachable and the baseline composition is unchanged.

### MG02: Launch, private server and owner-bound paths

**Contracts:** existing `seamless_coop(env)`, `coop_user_dir(env, user_dir, game)`, `online_overrides(env, user_dir)` and launcher `game_environment(s, graphics=None)`. Retain the existing `bbsc-launch.exe` injector and `BBSC_EMULATOR` interface.

- [ ] Extend existing launch tests before edits: injector + matching private server retained through GUI/direct/restart routes; offline/other-pool behavior follows upstream; explicit reload override retained; missing/empty override gives `SHADPS4_BBSC_WARP_JOIN=0` for BBSC only. Use a fake child, never a game process.
- [ ] Test a copied `<user>/seamless-coop` profile against native `--user`, effective DLL `BB_USER_DIR`, `BBSC_SAVE_DIR` and resolved journal/receipt paths. Assert they identify the same profile/slot; a second profile, same-name different slot, absent folder and existing pending journal cannot redirect ownership or overwrite the baseline copy. Keep `BB_GPU_USER_DIR` cache separation intact.
- [ ] Adapt the existing helpers at the narrowest point. Use the actual savedata title (`INSTALL_DIR_SAVEDATA`/SFO, historically `CUSA00207/SPRJ0005`), not an assumed CUSA03173 save path. Select one canonical candidate profile root; record an explicit copy mapping for existing saves plus all persistent mod state. Reuse existing owner checks and formats.
- [ ] Run focused `test_run_bbsc.py`, target `test_run_coop.py` and `test_launcher_hunters.py` with `python -m unittest discover -s tests -p <filename>`. Acceptance: all affected assertions pass, copied file manifests match, no public-pool fallback or orphaned pending state. The tests inspect environment/files without launching the game.

### MG03: Reuse the current DLL and carry the complete fixes

- [ ] Reconstruct the exact pinned BBSC reference and apply our whole four-destination patch using `tools/build_bbsc_mod.py`; validate normalized source hashes against the recorded source before edits. Do not substitute stock BBSC for our corrected DLL.
- [ ] Retain actual-function tests for stale host-role handling, six transient combat flags, removal of ordinary-enemy automatic compensation, boss rewards, owner-bound retry, snapshot ordering, home recovery and Echoes protection. Use matching `BBSC_FIXTURE_SOURCE` for every fixture. Historical native evidence remains attributed to its original runtime.
- [ ] Inspect target patch scripts/import bindings against DLL hook bytes, HTTP wrappers and P2P channel. If a new conflict is demonstrated, add one failing boundary fixture and fix its responsible producer/consumer. Keep native pickups and existing protections; do not guess offsets or bypass validation to make hooks appear successful.
- [ ] Run `test_bbsc_*.py`, `test_native_bbsc.py` and the DLL build commands below. Acceptance: affected fixtures pass without missing-input skips, patch apply/reverse checks pass and all four normalized destinations reproduce from pinned source. Runtime hook/import success remains a separate MG06 observation.

### MG04: Self-hosted matchmaking and relay compatibility

- [ ] Compare target client commands/message fields, P2P framing and reconnect lifecycle against the identified server **source/artifact**; do not infer live server identity from a sibling checkout. Inspect `SetClientVersion`, `LookupOnlineId`, required room operations and the error/unknown-command path. Upstream NP lookup now calls resolution services; simple registration is not equivalent to the old implementation.
- [ ] Build a local fixture using real serializers/dispatchers or the existing isolated server harness. Required assertions: supported login/room/lookup requests have correct replies; unsupported optional commands cannot terminate required flow; reconnect/leave/rejoin clears stale membership. Use dummy accounts and loopback only, with no live-service mutation.
- [ ] Choose the smallest compatible route after that evidence: prefer a narrow client adaptation for existing `BBR1` service if it fully works with target transport. If server support for `SMRL` or required new commands is necessary, prepare/test that bounded source change separately under server instructions; record deployment as an external prerequisite, not an action of this plan. Do not add a replacement backend/transport.
- [ ] Exercise direct and forced-relay packet round trips, current/new frame discrimination, malformed/unknown-peer rejection, disconnect and rejoin. Keep BBSC TCP20444 world/placement relay distinct from game UDP relay and shadNet signaling. Acceptance: both clients' required messages route to identified self-hosted services and payload/peer identity survive both transport modes; no claim of gameplay from loopback fixtures.

### MG05: Integrated build and reproducible offline checks

- [ ] Build target upstream composition plus the reviewed compatibility changes from a fresh output directory with the existing CLANG64 toolchain. Preserve target CMake dependency selection, FSR patches and Windows TLS verification; record submodule dirt and do not commit generated Gitlink changes. If build fails, distinguish target baseline/toolchain failure from local integration failure.
- [ ] Run the commands below with the reconstructed matching reference, compiler on PATH and a writable private TEMP/TMP. Require expected fixture execution; retain named unrelated full-suite failures/skips as limitations instead of declaring the full suite green.
- [ ] Verify tracked patch reproduction, notices, source/configuration/dependency hashes and actual output EXE/DLL hashes. Compare all MG01 deltas to the final diff. Acceptance: source/build/offline report identifies one complete candidate composition and its remaining user-gameplay checks; no package or game launch occurs.

Future execution commands, from the candidate checkout; `.superpowers/reference/BBSC` is the reconstructed pinned reference with our complete candidate patch, not an arbitrary existing clone:

```powershell
$env:PATH = 'C:/msys64/clang64/bin;' + $env:PATH
$env:BBSC_FIXTURE_SOURCE = (Resolve-Path '.superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp').Path
# Run the existing build.sh from an MSYS2 CLANG64 shell: bash build.sh
C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p test_run_bbsc.py
C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p test_run_coop.py
C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p test_launcher_hunters.py
C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p 'test_bbsc_*.py'
C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p test_native_bbsc.py
C:/msys64/clang64/bin/python.exe tools/build_bbsc_mod.py .superpowers/reference/BBSC .superpowers/migration196/dll
$bbscPatch = (Resolve-Path 'gpu/patches/bbsc/0001-profile-storage-and-clang64.patch').Path
git -C .superpowers/reference/BBSC apply --reverse --check $bbscPatch
git diff --check
```

### MG06: User playtest and migration acceptance

- [ ] Give the user a source/artifact/configuration manifest and copied-profile instructions; both players use the same complete 1.9.6 candidate. Any later packaging/distribution work requires its own scope; this plan supplies no package.
- [ ] Collect user evidence for same-map, cross-map/locked guest map and Hunter's Dream placement; same/different/empty password controls; host-to-guest after respawn, leave menu and rejoin. Identify peer, role, timing and actual usable placement.
- [ ] Check one joint boss event and both independent save+journal reloads: completion/relevant item retained, old host history excluded, original guest progress/NPC state preserved, no transient combat replay and no re-grant after a consumed reward where supported. Review manual ground pickups/absence of automatic compensation against current PT08 feedback.
- [ ] Check normal return, host/network loss and interrupted visit; exact valid origin or recorded-lamp fallback; pending wrong-character rejection/original-owner retry and Echoes/stain preservation. Use copied data only. Any unexercised existing gate remains open, with its exact limitation.
- [ ] Confirm actual required self-hosted routes and user-observed relay use, separating optional public logs from required flow. Record basic same-scene graphics/input/performance regressions against the retained 1.7.2 composition without promising target renderer improvements.
- [ ] Mark each case PASS/FAIL/INCONCLUSIVE on the exact candidate. Acceptance for migration is a reproducible supported-flow comparison with no unresolved introduced ownership/data-loss or required-transport regression; this does not close broader untested R03 cases. Keep 1.7.2 as the active fallback until the candidate is accepted.

## Rollback and checkpoint record

Rollback uses the untouched 1.7.2 runtime/configuration **and its own matching copied save/journal/receipt set**. Stop the candidate before switching copies. Do not reset Git history, overwrite original profiles or automatically import candidate saves back into 1.7.2; cross-version reverse state migration is unqualified. If a future server deployment is required, document its own reversible compatibility strategy before that separate deployment.

At each task completion, update this queue and [progress](../../WINDOWS-PROGRESS.md) with source commit, normalized patch/source hashes, artifact/configuration hashes, exact commands/exits, executed/skipped cases, limitations and next action. Keep user feedback on the 1.7.2 playtest linked to its original build. Preserve upstream notices and history when publishing reviewed checkpoints.

| Date | Checkpoint | Evidence / next action |
| --- | --- | --- |
| 2026-10-31 | MG00 PLAN READY | Static source/patch comparison only; documentation verification recorded in tracker. Await owner instruction to begin MG01; no 1.9.6 build, fixture run or gameplay result exists. |
