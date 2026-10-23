# BBSC progress: new fork / seamless

Updated: 2026-10-23 (Asia/Bangkok).

## Current state

The user authorized R02 baseline composition on 2026-10-23. Work is on `seamless`, created directly from BBport 1.7.2 `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d`. Existing `windows` stays unchanged. No old source patches/worktrees/builds/profiles are imported; no previous PASS result qualifies this checkout.

Read [the handoff](handoff/WINDOWS-RESUME.md), [active plan](superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md), [product outcomes](superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md) and [execution/evidence rules](superpowers/plans/2026-10-21-bbsc-windows-execution.md).

| ID | Owner | Status | Evidence / next action |
|---|---|---|---|
| F01 plan/branch migration | Codex | VERIFIED | Branch prepared at exact e5d04e2; documentation checks PASS; initial checkpoint 6fc1342 pushed and remote SHA verified. |
| F02 new-session handoff | Codex | VERIFIED | Self-contained startup/R02 prompt and documentation checks PASS; cb9fcab pushed and remote SHA verified. |
| R01 pins/ownership | Codex | VERIFIED | Approved pins/scope/ownership and shared instructions published in F01. |
| R02 composition | Codex | VERIFIED | Exact pinned patch applied; complete release DLL/loader/notices assembled privately; fresh source build and copied-profile native module/image/hooks/override startup PASS. [Detailed evidence](handoff/BBSC-BASELINE.md). Gameplay gates remain open. |
| R03 baseline reproduction | Codex | WAIT_GAME | Source build PASS; narrow native startup PASS. Two distinct accounts/copied profiles, actual service routing/relay or P2P fallback, join/progress/save/return gameplay remain NOT RUN. |
| R04 demonstrated gaps | Codex | WAIT_DEP | R02/R03 and relevant CL01 findings; no custom delta scheduled without reproduction. |
| CL01 audit | External Claude | READY | Separate clone/branch, four-document scope; [child tracker](collaboration/claude/PROGRESS.md). |

## Outcome gates

| Gate | Status | Required evidence |
|---|---|---|
| G1 join | WAIT_DEP | Complete pinned clients: selected peer/password, supported cross-map/Dream join/placement and relevant failed/stale cases. |
| G2 progress | WAIT_DEP | Jointly earned boss/story progress/relevant rewards persist after each save/reload; own progress preserved, no duplicates or older-host-history import. |
| G3 exit/return | WAIT_DEP | Normal departure/disconnect and interrupted-session reload; affected persistence failure/retry/wrong-character checks if changed. |

Custom managed admission/progress application remains OFF until relevant native gates pass. Chalice unsupported. No packaging or live-server redeployment.

## F01 checkpoint: plan migration

- Inspected repository/remotes and clean status. origin is the new `kaoitp/bloodborne_pc`; original `windows` points to `3fabfa7a7af67a34a6dfc630b6ec2539b68fad4d` (1.9.4).
- Command: native Git `rev-parse windows-v1.7.2`, then `switch -c seamless e5d04e2ba4864ccf40de6c3cf6aa532855320b0d`; exit 0, HEAD exact e5d04e2. Remote branch existence check returned no seamless branch before publication.
- Scope: active three-goal plan, eleven approved outcomes, Windows/evidence rules, handoffs, fresh shared/child trackers, root agent entry points and private-evidence ignore rule. No implementation imported; runtime/README/build/dependency files unchanged.
- Previous-reference documents informed scope only. Under the user's final instruction, old worktrees/results are not a dependency or acceptance source for new development.
- Checks: PASS, inline Python UTF-8/content validation of 10 Markdown documents, 28 local links, all 11 approved outcomes, exact seamless base, preserved windows ref, only 11 allowlisted planning/ignore paths changed, and no completed R02-onward checkboxes. Native Git `diff --check --ignore-submodules` and staged `diff --cached --check` exited 0; `check-ignore .superpowers/probe.log` confirms private-evidence exclusion. Build, runtime tests, game launch and server changes: NOT RUN (documentation-only task).
- Publication: `git push -u origin seamless` exited 0. `git ls-remote origin refs/heads/seamless refs/heads/windows` and `git rev-parse HEAD origin/seamless` confirmed initial checkpoint `6fc134256ab2b5e4c85a45b0a50f53b4e4157697` locally and remotely, with windows unchanged at 3fabfa7. Parent is exact e5d04e2. This follow-up records publication and marks F01/R01 complete; it changes only plan/progress documents.
- Next action: stop after the documentation checkpoint. When development is requested, start R02 by obtaining and verifying pinned BBSC input; no recovery of old worktrees.

## F02 checkpoint: new-session handoff

- Scope: three documentation files only: Windows handoff, this tracker and the active plan. Added checkout/branch/ancestry checks, fresh-clone instructions, current NOT RUN evidence, exact first R02 actions, later private test inputs and a Thai development prompt. Replaced the prior turn-specific stopping sentence so a new session can start R02 when requested.
- Tested source: `b42c83af0bcc8b2adab29c0ae3bed546ce33b704` plus the three-file documentation diff. R02 remains READY/unstarted; source, builds, game/server state and Claude-owned documents unchanged.
- Commands/results: inline Python UTF-8/link/content/scope checks PASS for 10 Markdown documents and 28 local links; startup/prompt/pins/evidence/constraints assertions PASS; native Git `merge-base --is-ancestor e5d04e2 HEAD` and `diff --check --ignore-submodules` exited 0. No build/runtime/gameplay tests (NOT RUN; documentation-only).
- Review: handoff no longer requires the old session/worktrees or implies old tests qualify this checkout. It distinguishes available documentation from private inputs needed only at gameplay setup; the ready prompt explicitly authorizes development from R02 rather than another plan-only pass.
- Publication: `git push origin seamless` exited 0; `git ls-remote origin refs/heads/seamless` and `git rev-parse HEAD origin/seamless` matched handoff checkpoint `cb9fcabfe0f5ab6968a3148623b71e56a614701d`. This follow-up records F02 completion; R02 is still unstarted.
- Resume: open this project on seamless and paste the handoff's New-session prompt. Read current progress, then mark R02 IN_PROGRESS and verify the pinned BBSC source/patch before implementation. No outstanding question blocks that first source task.


## R02 start: 2026-10-23

- Authorized scope: exact baseline composition only; dependencies F01/R01 VERIFIED. Acceptance: pinned commit and patch hash, destination review/apply-check, dependency pins, DLL/loader/data/notices provenance, fresh copied-profile boundary, actual native module load. No custom behavior, packaging or server deployment.
- Checkout routing: app worktree is detached at 01f4b7508bd87e1a0cced662db586142635f1a61; native git worktree list locates clean seamless at C:/Projects/bloodborne_pc at the same SHA. Work proceeds in that current primary checkout, without importing old worktrees/results.
- Initial usage: 29%/43% used (71%/57% remaining); above stop threshold. Native ancestry check exit 0; origin is kaoitp/bloodborne_pc.
## R02 checkpoint: complete pinned composition and native startup

- User authorized R02, source build and copied-profile diagnostics. Work performed inline on the clean primary checkout's `seamless`; no subagents, old worktree imports, packaging or server changes. See [the composition record](handoff/BBSC-BASELINE.md) for commands, hashes, dependency pins, setup corrections, checks and private evidence paths.
- Tested source: starting HEAD `01f4b7508bd87e1a0cced662db586142635f1a61` plus the exact 15-destination BBSC patch; source runtime staged-diff SHA256 `27d2aa943f3ea7b43d7cc3bff0b8fececdbcdf072727207418d293fb666a8c4a`. BBSC source commit matched `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`; canonical patch SHA256 matched `e34c79b388605998b430ec4eed556fc2cb8c8928f1d3e9f26bf5d2df29732aa3` after bypassing checkout CRLF conversion via Git archive. Apply preflight/application/reverse-check exited 0; independent exact-application content comparison PASS 15/15 (CRLF normalization only).
- Artifact/static checks: official v0.0.2 BBport ZIP SHA256 `001efc0a03b47bd6b2660c598fd6d172d2aaae3201a4982134d1f215918acd3c` matched GitHub release metadata. Extracted matching gameplay DLL, original injector, manifest and required notices to ignored storage; no packaged emulator executable substituted. Manifest/source and 3 mandatory notice markers PASS; PE x86-64/system imports checked. DLL SHA256 `1df7d39e31c5d1acf034b5fd990b669e5e82944be477f26b0a46621a91610fdf`; injector `c7fbaa406d972324645153bb8cc8bdad17fcd7db2f05026d67e3ba68f34750c1`.
- Native build: six unchanged pinned submodules initialized; MSYS2 CLANG64 `bash build.sh` waited exit 0, 336/336 Ninja steps. Fresh `out/bb-probe.exe` SHA256 `a948f6948d934f024f6089d976edf97bd915f0e46381cdeaad45d9595b1a27ca`. Existing build script applied only its two tracked FSR-Vulkan patches to the submodule working tree; no dependency upgrade or compatibility fix.
- Native startup: user-supplied CUSA03173 APP_VER 01.09 verified. Fresh copied profile only, no forced patch override, no online login/gameplay input. Final test probe PID 9016 loaded exactly the pinned DLL: image verified after 93 ms, 52 byte patch writes, 159/159 hooks installed, mod ready after 109 ms, 3 HTTP URL overrides read from copied configuration, kit ready. Game window responsive; test probes closed with normal CloseMainWindow requests. Post-test original profile file set and all 3,171 SHA256 hashes unchanged (PASS).
- Configuration: corrected the initial omitted explicit HTTP-overrides environment variable, then the user's clarification that ShadNet and game server use separate addresses. Only private copied config changed. ShadNet TCP 31313/31315 and game API TCP 20443 reachable; correct game-relay TCP 20444 not reachable. Existing native P2P fallback/UDP relay and actual authentication/peer flow NOT RUN. No deployed-server version inferred. Addresses, game/profile paths, credentials and logs remain out of Git.
- Fixture/native/gameplay separation: source/content/manifest assertions PASS; Windows build and narrow native module/startup PASS; Linux-only test programs SKIP; multiplayer, boss/story/reward persistence and G1/G2/G3 NOT RUN. No new custom behavior or R04 gap inferred. Original baseline's warnings and optional-part/cache misses are documented without unrelated fixes. DLL/loader came from the verified release; local MSVC DLL rebuild NOT RUN (upstream compiler path absent).
- Usage: 71%/57% remaining at start, 67%/56% after patch/build setup, 62%/55% during native checks, 58%/55% before checkpoint; no window below 10%.
- Review: source scope exactly the 15 reviewed upstream destinations; existing CMake NP source glob includes new lookup implementation; gameplay callbacks remain delegated to the original mod. All custom managed admission/application stays OFF. Claude-owned files unchanged. Plan R02 checkboxes and R03 build checkbox synchronized; remaining gameplay checkboxes open.
- Final checkpoint checks: inline Python PASS for 4 UTF-8 documents, 21 local links, five completed R02 checks, open G1/G2/G3, exact 15-source/4-document scope, runtime diff SHA256, unchanged Gitlinks and no private service addresses. Native Git staged whitespace check with cr-at-eol and reverse apply-check exited 0. Test probe/runner no longer running; an empty Get-Process lookup returned 1 (expected absence, not a test failure).
- Publication setup: first commit attempt exited 128 because Git had no configured author identity. The preceding four checkpoint authors/committers agree; reuse that existing repository identity with per-command -c user.name/user.email, without changing global settings. Publication then succeeded: per-command identity commit produced source checkpoint `f3734da56722f21dd2c25dcca89b85d1c93f2109`; `git push origin seamless` exited 0. `git rev-parse HEAD origin/seamless` and `git ls-remote origin refs/heads/seamless refs/heads/windows` matched f3734da locally/remotely, with windows preserved at `3fabfa7a7af67a34a6dfc630b6ec2539b68fad4d`. This documentation-only follow-up records that verified publication; runtime/artifacts are unchanged.
- Next action: R03 on two distinct existing authorized accounts and separate copied profiles; verify the split self-hosted route and relay/P2P fallback before selected-host cross-map/Dream join, jointly earned progress/reward save/reload and normal/interrupted return. Do not duplicate one login, redeploy a server or package a release.
