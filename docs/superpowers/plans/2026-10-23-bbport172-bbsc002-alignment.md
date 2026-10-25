# BBport 1.7.2 + BBSC 0.0.2 development plan

Updated: 2026-10-24. Migrated to the new fork's `seamless` branch. This is the authoritative implementation plan; [progress](../../WINDOWS-PROGRESS.md) records evidence, and [the product specification](../specs/2026-10-18-bbsc-anywhere-coop-design.md) defines required outcomes.

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

The pins are carried forward from the approved plan. The local BBport tag was rechecked when creating `seamless`; R02 subsequently verified/applied the pinned patch and assembled/tested the complete native composition here. See the R02 evidence for exact hashes and limitations. A moving upstream branch is not a replacement pin.

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

Owner: Codex. Dependency: R02 composition VERIFIED. Status: IN_PROGRESS. Native same-map and Cathedral Ward -> Dream join/adjacent placement succeeded. [R04-J01](../../handoff/R04-JOIN-RELOAD.md) verified the existing-flag fix for a second-load guest-role/return gap. The earlier pre-claim failure remains unexplained; full G1/G2/G3 remain open. [Progress evidence](../../WINDOWS-PROGRESS.md), [resume](../../handoff/R03-RESUME.md).

- [x] Initialize only required pinned dependencies and build using the baseline's `bash build.sh`; record actual waited exit and source/diff state. Exit 0; hashes/dependency inventory in R02 evidence.
- [x] Run relevant baseline/patch/native load checks and startup smoke. Record honest skips; no blanket port of old tests or unrelated graphics qualification.
- [ ] On two distinct accounts and copied profiles, verify supported cross-map/Dream join, selected-host placement and required self-hosted service routing.
- [ ] Verify jointly earned boss/story progress, own-progress preservation, relevant reward non-duplication and each player's save/reload.
- [ ] Verify normal exit/disconnect/return and interrupted-session exit/reload. Preserve original saves and baseline Kit/Blank behavior.
- [x] Record a three-goal table using EXISTING/PASS, PRESENT-NOT-TESTED, REPRODUCED-GAP or UNSUPPORTED before designing changes.

R03-L01 historical source comparison is VERIFIED (documentation only, 2026-10-24): [join-fix leads](../../handoff/R03-JOIN-LEADS.md). R03-L02 reproduced successful baseline joining but not the earlier pre-claim failure; R04-J01 tests one downstream lead. The three broad R03 gameplay boxes stay open.

Unknown deployed server source/version remains explicit; it does not block unrelated baseline composition. Use existing authorized test services/configuration, not production redeployment. One client can perform setup/load smoke; actual multiplayer needs a distinct second identity.

R03-A01: IN_PROGRESS; [quota checkpoint](../../handoff/R03-ACCEPTANCE.md) records negative join control, older-host-progress gap, post-placement guest crash and partial routing. No broad gameplay box completed. The user requests the four remaining acceptance groups and waives exhaustive map coverage. Use representative same-map/Dream coverage plus invalid-candidate, shared-progress/save-reload, disconnect/interrupted-return and required self-hosted route evidence. Record any remaining case honestly; no implicit gameplay PASS from source inspection.

R03-A02 closure run: IN_PROGRESS. Resume A01 crashed guest recovery, symbolicate the actual null read, establish an existing-toolchain DLL build if possible, then correct and natively verify only demonstrated gaps. User authorizes game tests and retains quota stopping.

## R04 — Minimum fixes for demonstrated goal gaps

Owner: Codex. Dependency: R02/R03 evidence and relevant CL01 findings.

- [ ] For each demonstrated gap, record the five-part change justification in the scope contract. Existing working behavior needs verification only; do not invent a change for every goal.
- [ ] Where join changes are necessary, extend the existing BBSC path. Verify valid selected-host join, relevant wrong/stale password/candidate handling and failed join without guest-world mutation.
- [ ] Where progress changes are necessary, reuse the event/save path. Verify eligibility, own-progress preservation, no duplicate relevant rewards and save/reload. Changes to persistence/recovery also require affected wrong-character/write-failure/crash/retry cases.
- [ ] Where self-hosted configuration changes are necessary, reuse existing components/settings; verify routing and peer exchange without a required public service.
- [ ] Run focused regression/native/gameplay checks for the actual delta, repeat the three-goal end-to-end scenario and review every changed path for scope.

R04-J01 is VERIFIED for its bounded case: [five-part justification, native RED/GREEN and checks](../../handoff/R04-JOIN-RELOAD.md). Three added lines in `run.py` default the existing extra-reload switch off for DLL launches; no DLL rebuild or server change.

- [x] Reproduce second cross-map reload and broken guest return on the pinned composition.
- [x] Regression: DLL default, explicit overrides, empty override and stock launch (4 tests PASS).
- [x] Actual fixed Cathedral Ward -> Dream guest placement and normal origin return; original profile unchanged.
- [x] Inline review and honest full-suite results recorded (154 tests, 1 failure, 8 errors, 48 skips); broader gates remain open.

## CL01 — External Claude Code source/reuse audit

CL01-INT01: VERIFIED / INTEGRATED (2026-10-24). User requests the reviewed PR's closure, waiving usage-based stopping. Approved unchanged head `108bf28f069d7017712fd71e24fb7fd6b2bbde36` merged into `seamless` as `7a0a0153cbf36de0b88ab4aeba1e9bb0cdb9d96e`, preserving both audit commits. GitHub confirms PR #1 merged/closed; four threads resolved, no listed commit statuses or PR workflow runs. Fresh 90-citation/27-file, link/coverage/format/scope checks pass; local checkout fast-forwarded. Merge delta is exactly the four accepted audit documents, with identical blobs and no runtime changes. G1/G2/G3 remain open; CL02-P01 remains the separate assigned follow-up.

CL01-REV02: ACCEPTED for source/document scope (2026-10-24). PR #1 correction head `108bf28f069d7017712fd71e24fb7fd6b2bbde36` addresses all four REV01 comments; no new blocking finding. Fresh checks: 90 citation URLs/27 pinned source files, 12 local links/anchors, 29 cases, 11 outcome rows, UTF-8/LF/no-BOM, four-file scope and whitespace PASS. Current R03-A01 independently records the older-host-progress gap; CL01's frozen source findings remain attributed separately. User waives usage-based stopping for this review. Audit accepted, PR merge not performed; G1/G2/G3 remain open.

CL01-REV01: REVIEW COMPLETE / CHANGES REQUESTED (2026-10-24). Reviewed PR #1 at `eb493a40cfc2f2ad0e28f485e4208040b27d897f` against frozen base `04c6e7b4b9a042c872e6ed815dacce6c7a7a0d8e`, the four-path allowlist, pinned source and current `bd24679`. Structural checks passed; four inline corrections are required: conditional relay-necessity inference, baseline versus J01 launch identity, UDP peer-transfer proof and verified-event filtering beyond first-seen deltas. [Review 5637531403](https://github.com/kaoitp/bloodborne_pc/pull/1#pullrequestreview-5637531403) posted successfully. CL01 acceptance checkboxes remain open; next is external correction within the same four paths, then re-review before a new assignment. No runtime changes or gameplay acceptance.

Owner: the user's external friend using Claude Code, in a separate clone/audit branch; not an automatic subagent. CL01 source/document handback ACCEPTED and integrated by CL01-INT01 above. [Work package](../../handoff/CLAUDE-CODE-WINDOWS.md) fixes the four writable documents, frozen audit base, slice dependencies and handback/integration checks. Codex retains runtime/build/config/native/gameplay and shared plans.

- [x] Map the complete release composition and existing support for each goal with pinned source citations.
- [x] Map required self-hosted routes and only relevant selected-peer/session/identity boundaries; distinguish source presence from runtime PASS.
- [x] Deliver scoped acceptance cases, checks and a handback commit within the [four-file allowlist](../../handoff/CLAUDE-CODE-WINDOWS.md).

CL02-P01: HANDBACK RECEIVED / CHANGES REQUESTED under the [follow-up package](../../handoff/CLAUDE-CODE-WINDOWS.md#cl02-p01-progress-contract-follow-up). [PR #2](https://github.com/kaoitp/bloodborne_pc/pull/2) head 2386dfc reviewed in CL02-REV03 below; two reward lifecycle contradictions remain before acceptance. Same four writable documents; no runtime/build/native/service work delegated. R04 implementation and gameplay proof remain Codex-owned.

CL02-REV03: REVIEW COMPLETE / CHANGES REQUESTED (2026-10-25). User requests PR #2 review; inspected full three-commit delta at `2386dfc6137d502d6464a21fcc16bfec4eb2a31f` against frozen CL01 base `108bf28` and latest correction against c6cb7b3. All REV01 fixes remain closed; REV02's blanket departure/new-epoch discard is removed. Two P2 contradictions remain: A-32/seam (i) require playable/HP-positive/not-loading at every enqueue, excluding eligible kills during same-party death/loading required by outcome 9/G2-19(b); A-32's wrong-owner discard and G2-19(d)'s catch-all discard can delete character A's valid obligation while B is loaded, contradicting G2-19(c3). Keep eligibility once opened until genuine departure; defer valid inactive-owner entries and reject invalid admission records separately. Standards bounded/no new blocker; Spec two findings. Fresh checks PASS: four-file scope/unchanged CL01 byte prefixes, 163 citations/29 pinned files, 18 links, 65 claims/38 cases, 11 outcome rows, UTF-8/LF/no BOM, whitespace and exact parent. [Full commands, document hashes and limitations](../../WINDOWS-PROGRESS.md#cl02-rev03--pr-2-review-review-complete--changes-requested-2026-10-25). No external review/comment submission, merge, runtime change or G2 PASS. Next: focused external correction and re-review; broad R03 boxes and default-OFF gates unchanged.

CL02-REV02: REVIEW COMPLETE / CHANGES REQUESTED (2026-10-25). Reviewed `c6cb7b3d75b164bfbe2b6dc164241141918de615` against prior b48d2b3 and frozen CL01 base. All three REV01 findings addressed; fresh 160 citations/29 source files, 18 links, 65 claims/38 cases, CL01 preservation and format/scope/coverage checks PASS. [One new P2 correction](https://github.com/kaoitp/bloodborne_pc/pull/1#issuecomment-6388357678): A-32/G2-19 must distinguish rejecting events earned after departure from retaining a valid already-earned but unconfirmed reward for its original owner. Dropping every queued entry on departure can lose jointly earned rewards. User waives usage-based stopping; no integration, runtime change or G2 PASS. Next: focused external correction, then re-review; completed REV01 fixes stay closed.

CL02-REV01: REVIEW COMPLETE / CHANGES REQUESTED (2026-10-24). Reviewed handback head `b48d2b36c6e41cb66cfc474287fc5eaf6bec6863` against base `108bf28f069d7017712fd71e24fb7fd6b2bbde36`. Four-file append-only/CL01 preservation, 145 citations/28 source files, 18 links, 61 claims/33 cases, coverage/format/whitespace PASS. [Three correction requests](https://github.com/kaoitp/bloodborne_pc/pull/1#issuecomment-6382726381): receiver does not reject older snapshot IDs; receipt-time/state-6 baselines do not establish playable-party eligibility; reward admission must follow that eligibility rather than unchanged state-6-only hooks. No integration or runtime/gameplay acceptance. Next: focused correction on the same external branch, then re-review; PR #1 stays merged/closed.

[PR approval and CL02 assignment](https://github.com/kaoitp/bloodborne_pc/pull/1#pullrequestreview-5637592348) posted successfully; four REV01 threads resolved. [PR #1](https://github.com/kaoitp/bloodborne_pc/pull/1) is now merged/closed by CL01-INT01.

## Completion and evidence

G1: supported cross-map/Dream join with correct peer/password and placement. G2: jointly earned progress/rewards survive save/reload without importing older host progress, undoing own progress or duplicating relevant rewards. G3: departure/disconnect/interrupted-session reload preserve own world and safe return. All use complete pinned clients and the self-hosted route.

Keep fixture, native, baseline gameplay and custom-change gameplay evidence separate. Old repository results do not pass these checkboxes. Custom managed admission/progress application stays OFF until its relevant native gates pass. No claim of completion while required checks are open.

### A02 bounded checkpoint

- [x] Reproduce shader null-table read against the real header, fix it narrowly and rebuild/replay native join.
- [x] Build pinned-source local DLL with notices; test profile path producer/consumer and native per-slot journal.
- [x] Observe copied interrupted return to original point and final-DLL invalid-point lamp fallback.
- [x] Observe initial wrong-character journal isolation, malformed-file rejection and completion-rename retry.
- [ ] Finish final-source normal/host-loss return, pending-title ownership, initial-write failure and independent world/save integrity.
- [ ] Correct verified-event progress/rewards and prove save/reload; complete remaining candidate/routing evidence.

Full evidence/versions/failed attempts/limitations: [A02 record](../../handoff/R03-A02-RECOVERY.md). R03 remains IN_PROGRESS and its three broad gameplay boxes stay open.

A02 final native gate FAILED: pending recovery crossed characters after title; prototype is OFF by default behind explicit experimental opt-in. The checkboxes above describe bounded observations, not full recovery acceptance. Fix actual character/lifecycle ownership before enabling it; retain all three R03 gameplay boxes open. Stop new work at the usage checkpoint and publish.

A02 checkpoint published as cb336ffa2d5b27142e69fb0fd179eb0f45ee6b3a; origin/remote SHA verified, only existing FSR-Vulkan dirt remains. R03 stays IN_PROGRESS; native recovery ownership FAILED and new origin recovery remains experimental/OFF.

A03: IN_PROGRESS at source base 3ff3057, usage 100%/54%. First close the reproduced pending-recovery ownership gap using the observed ordinary load seam and fresh per-load save ownership, then G2 event/reward and remaining G1/G3/G4 cases. Acceptance and scope are recorded in the tracker before edits; no broad checkbox change yet.


### A03 bounded checkpoint (2026-10-25)

- [x] Pending-title/other-character isolation and positive owner retry on the ownership DLL.
- [x] Keep existing Dream keys before join; native own-state journal comparison and normal save/reload preserve the previously lost bits.
- [x] Actual P02 host process loss returns to original point; settled world equals preceding own baseline.
- [x] P03 actual guest interruption/restart restores original point/lamp and 1250 groups; normal return and save/reload retain original lamp.
- [ ] Initial-write refusal: native RED; P04 Lua skip still admitted and was reverted. Keep new recovery experimental/OFF.
- [ ] G2/group-9/reward integrity and remaining candidate/locked-map/routing cases; no broad R03 closure.

[Exact versions, native evidence, rejected candidate and next seam](../../handoff/R03-A03-OWN-STATE.md). Final full suite: 157 tests, 1 failure, 8 errors, 48 skips; focused 7 PASS. Original 3171 paths/hashes unchanged. Inline Standards review bounded/no new blocker; Spec partial. Publish the checkpoint without force or private artifacts.


### A04 native wait candidate

- [x] Assess native wait: FAILED after delayed release/falling; fully reverted.
- [x] A04-P02 bounded native cancellation before the enclosing join transition; actual blocked-write own-state equality, healthy retry/adjacent placement, normal return and independent save/reload.
- [ ] Remaining G2/group-9/reward, candidate/locked-map/routing and recovery enablement gates. R03 remains IN_PROGRESS; experimental default stays OFF. [Exact attribution and limits](../../handoff/R03-A04-ADMISSION.md).


### B01 personal common-event flags

- [x] Preserve the 29 reproduced personal completion flags: actual fresh native Dream join/normal return/reload preserves all 1250 prejoin groups exactly. [B01 evidence and limits](../../handoff/R03-B01-PERSONAL-FLAGS.md). This does not pass G2 shared-event/reward eligibility.
