# BBSC progress: new fork / seamless

Updated: 2026-10-23 (Asia/Bangkok).

## Current state

The user requested only plan migration and a ready development branch. Work is on `seamless`, created directly from BBport 1.7.2 `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d`. Existing `windows` stays unchanged. No old source patches/worktrees/builds/profiles are imported; no previous PASS result qualifies this checkout.

Read [the handoff](handoff/WINDOWS-RESUME.md), [active plan](superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md), [product outcomes](superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md) and [execution/evidence rules](superpowers/plans/2026-10-21-bbsc-windows-execution.md).

| ID | Owner | Status | Evidence / next action |
|---|---|---|---|
| F01 plan/branch migration | Codex | VERIFIED | Branch prepared at exact e5d04e2; documentation checks PASS; initial checkpoint 6fc1342 pushed and remote SHA verified. |
| F02 new-session handoff | Codex | VERIFIED | Self-contained startup/R02 prompt and documentation checks PASS; cb9fcab pushed and remote SHA verified. |
| R01 pins/ownership | Codex | VERIFIED | Approved pins/scope/ownership and shared instructions published in F01. |
| R02 composition | Codex | READY | Next development task: obtain/check/apply pinned BBSC reference and assemble complete DLL/loader configuration from scratch here. Not started. |
| R03 baseline reproduction | Codex | WAIT_DEP | R02; build/load/self-hosted multiplayer checks NOT RUN in this repository. |
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
