# BBSC progress: new fork / seamless

Updated: 2026-10-23 (Asia/Bangkok).

## Current state

The user requested only plan migration and a ready development branch. Work is on `seamless`, created directly from BBport 1.7.2 `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d`. Existing `windows` stays unchanged. No old source patches/worktrees/builds/profiles are imported; no previous PASS result qualifies this checkout.

Read [the handoff](handoff/WINDOWS-RESUME.md), [active plan](superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md), [product outcomes](superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md) and [execution/evidence rules](superpowers/plans/2026-10-21-bbsc-windows-execution.md).

| ID | Owner | Status | Evidence / next action |
|---|---|---|---|
| F01 plan/branch migration | Codex | IN_PROGRESS | seamless created at exact e5d04e2; document checks PASS; committing/publishing this checkpoint. |
| R01 pins/ownership | Codex | WAIT_DEP | Approved pins/scope and ownership checks PASS; awaits F01 publication. |
| R02 composition | Codex | WAIT_DEP | READY after F01/R01; obtain/check/apply pinned BBSC reference and assemble complete DLL/loader configuration from scratch here. |
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
- Checks: PASS, inline Python UTF-8/content validation of 10 Markdown documents, 28 local links, all 11 approved outcomes, exact seamless base, preserved windows ref, only 11 allowlisted planning/ignore paths changed, and no completed R02-onward checkboxes. Native Git `diff --check --ignore-submodules` exit 0; `check-ignore .superpowers/probe.log` confirms private-evidence exclusion. A first checker used an overly broad word match on the loader requirement; corrected to inspect R02-onward checkboxes, then all checks passed. Build, runtime tests, game launch and server changes: NOT RUN (documentation-only task).
- Publication: pending local commit and push to origin/seamless. Source/parent for this documentation diff is e5d04e2; the actual checkpoint SHA will be reported after commit.
- Next action: finish documentation checks/publication and stop. When development is requested, start R02 by obtaining and verifying pinned BBSC input; no recovery of old worktrees.
