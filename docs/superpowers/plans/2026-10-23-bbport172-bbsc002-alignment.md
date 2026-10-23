# BBport 1.7.2 + BBSC 0.0.2 development plan

Updated: 2026-10-23. Migrated to the new fork's `seamless` branch. This is the authoritative implementation plan; [progress](../../WINDOWS-PROGRESS.md) records evidence, and [the product specification](../specs/2026-10-18-bbsc-anywhere-coop-design.md) defines required outcomes.

## Scope contract

| Goal | Required behavior |
|---|---|
| Seamless join | Same nonempty password allows cross-map join and placement beside the selected host in supported story maps/Hunter's Dream. Preserve existing same-map rules; Chalice remains unsupported. |
| Jointly earned progress | Persist eligible boss/story progress and necessary verified rewards earned together. Preserve each player's earlier progress/quest choices; prevent duplicate relevant rewards. Do not copy the whole save or the host's older progress. |
| Self-hosted services | All services required for the join/progress flow have a self-hosted route using existing compatible BBSC/shadNet/game-service components. A public service must not be required for these goals. |

Preserve BBport/BBSC graphics, FSR, input, launcher/UI, combat, scaling, spectating, world time, NPC/quest mechanics and unrelated online behavior. Save protection and safe departure/return are required correctness, using existing mechanisms first.

Reproduce the complete reference combination before changing behavior. Every code change must name its goal, pinned baseline reproduction showing the gap, why existing behavior/configuration is insufficient, the smallest responsible producer/consumer and a focused acceptance check. Required build compatibility fixes must be justified and tested separately.

Unscheduled: wholesale legacy module migration, THD/bbhost/public-server/cross-emulator development, new account/backend/transport, custom HMAC/capability framework, generic storage/save-codec/NG framework, whole-game quest/item catalogue, unrelated system upgrades, packaging and live-server redeployment.

## Exact references

| Component | Pin |
|---|---|
| [Supermedo BBport windows-v1.7.2](https://github.com/Supermedo/bloodborne_pc/releases/tag/windows-v1.7.2) | `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d` |
| [CLSAMG22 BBSC v0.0.2](https://github.com/CLSAMG22/BBSC/releases/tag/v0.0.2) | `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41` |
| [Reference BBport patch](https://github.com/CLSAMG22/BBSC/blob/4f11faf88b6ba658ebde6fe5fbefdadedba4fa41/bbport/bbport-1.7.2-bbsc.patch) | SHA256 `e34c79b388605998b430ec4eed556fc2cb8c8928f1d3e9f26bf5d2df29732aa3`; 15 destination files in the prior reference inspection; recheck before applying here. |

The pins are carried forward from the approved plan. The local BBport tag was rechecked when creating `seamless`. BBSC source/artifacts have not yet been obtained or tested in this new checkout. A moving upstream branch is not a replacement pin.

## F01 — Plan and branch migration

Owner: Codex. Documentation-only; no dependency on old worktrees.

- [x] Create `seamless` directly from exact BBport 1.7.2; preserve `windows`.
- [x] Transfer the current three-goal plan, outcomes, handoffs and fresh progress tracker; verify links/content/whitespace and unchanged runtime.
- [x] Commit and publish only this checkpoint to `origin/seamless`; verify remote SHA. Initial checkpoint `6fc134256ab2b5e4c85a45b0a50f53b4e4157697` was pushed and matched HEAD/origin/seamless; windows stayed unchanged. Follow-up documentation records this outcome.

## F02 — New-session handoff

Owner: Codex. Dependency: F01. Documentation-only; R02 remains unstarted.

- [x] Make the handoff self-contained: repository/branch checks, current evidence boundary, first R02 actions, later private setup needs and a ready-to-paste development prompt.
- [x] Verify links/content/whitespace and documentation-only scope; commit/push the handoff checkpoint to origin/seamless. Handoff checkpoint `cb9fcabfe0f5ab6968a3148623b71e56a614701d` was pushed and matched the remote SHA; this follow-up records the result.

## R01 — Baseline references and ownership

Owner: Codex. Dependency: F01.

- [x] Record approved release pins, scope and existing-loader requirement.
- [x] Publish the shared plan, entry points and Claude audit instructions as part of F01.

## R02 — Complete reference composition

Owner: Codex. Dependency: F01/R01. Status: VERIFIED for composition/native startup (2026-10-23); [evidence](../../handoff/BBSC-BASELINE.md). Gameplay remains R03. Source/evidence checkpoint `f3734da56722f21dd2c25dcca89b85d1c93f2109` pushed to origin/seamless and remote SHA verified.

- [x] Obtain the exact pinned BBSC source/reference patch. Verify source commit and patch SHA256; inspect all destinations and run `git apply --check` against this clean 1.7.2 source. A mismatch is a stop, not permission to guess offsets.
- [x] Apply the reviewed patch; record source commit, diff and dependency/Gitlink pins. Use an additional isolated checkout only if later development needs it; do not recover or depend on old worktrees.
- [x] Identify and assemble the matching gameplay DLL, existing loader/configuration, required data and notices. Verify artifact provenance/hashes. The patch's no-op gameplay callbacks delegate to the external mod; they are not a new implementation task. Do not write a new loader or copy packaged executables over source outputs.
- [x] Establish fresh copied-profile test boundaries and existing self-hosted settings; preserve baseline authentication/validation and keep custom admission/application OFF.
- [x] Verify actual module load/startup at the required native boundaries; keep artifact/source/configuration evidence separate from gameplay acceptance.

## R03 — Reproduce the complete baseline on self-hosted services

Owner: Codex. Dependency: R02 composition. Build-only work may follow the source/patch checks before gameplay is ready.

- [x] Initialize only required pinned dependencies and build using the baseline's `bash build.sh`; record actual waited exit and source/diff state. Exit 0; hashes/dependency inventory in R02 evidence.
- [ ] Run relevant baseline/patch/native load checks and startup smoke. Record honest skips; no blanket port of old tests or unrelated graphics qualification.
- [ ] On two distinct accounts and copied profiles, verify supported cross-map/Dream join, selected-host placement and required self-hosted service routing.
- [ ] Verify jointly earned boss/story progress, own-progress preservation, relevant reward non-duplication and each player's save/reload.
- [ ] Verify normal exit/disconnect/return and interrupted-session exit/reload. Preserve original saves and baseline Kit/Blank behavior.
- [ ] Record a three-goal table using EXISTING/PASS, PRESENT-NOT-TESTED, REPRODUCED-GAP or UNSUPPORTED before designing changes.

Unknown deployed server source/version remains explicit; it does not block unrelated baseline composition. Use existing authorized test services/configuration, not production redeployment. One client can perform setup/load smoke; actual multiplayer needs a distinct second identity.

## R04 — Minimum fixes for demonstrated goal gaps

Owner: Codex. Dependency: R02/R03 evidence and relevant CL01 findings.

- [ ] For each demonstrated gap, record the five-part change justification in the scope contract. Existing working behavior needs verification only; do not invent a change for every goal.
- [ ] Where join changes are necessary, extend the existing BBSC path. Verify valid selected-host join, relevant wrong/stale password/candidate handling and failed join without guest-world mutation.
- [ ] Where progress changes are necessary, reuse the event/save path. Verify eligibility, own-progress preservation, no duplicate relevant rewards and save/reload. Changes to persistence/recovery also require affected wrong-character/write-failure/crash/retry cases.
- [ ] Where self-hosted configuration changes are necessary, reuse existing components/settings; verify routing and peer exchange without a required public service.
- [ ] Run focused regression/native/gameplay checks for the actual delta, repeat the three-goal end-to-end scenario and review every changed path for scope.

## CL01 — External Claude Code source/reuse audit

Owner: the user's external friend using Claude Code, in a separate clone/audit branch; not an automatic subagent. READY alongside Codex R03 now that R02 is verified. [Work package](../../handoff/CLAUDE-CODE-WINDOWS.md) fixes the four writable documents, frozen audit base, slice dependencies and handback/integration checks. Codex retains runtime/build/config/native/gameplay and shared plans; no audit result is claimed by assigning it.

- [ ] Map the complete release composition and existing support for each goal with pinned source citations.
- [ ] Map required self-hosted routes and only relevant selected-peer/session/identity boundaries; distinguish source presence from runtime PASS.
- [ ] Deliver scoped acceptance cases, checks and a handback commit within the [four-file allowlist](../../handoff/CLAUDE-CODE-WINDOWS.md).

## Completion and evidence

G1: supported cross-map/Dream join with correct peer/password and placement. G2: jointly earned progress/rewards survive save/reload without importing older host progress, undoing own progress or duplicating relevant rewards. G3: departure/disconnect/interrupted-session reload preserve own world and safe return. All use complete pinned clients and the self-hosted route.

Keep fixture, native, baseline gameplay and custom-change gameplay evidence separate. Old repository results do not pass these checkboxes. Custom managed admission/progress application stays OFF until its relevant native gates pass. No claim of completion while required checks are open.
