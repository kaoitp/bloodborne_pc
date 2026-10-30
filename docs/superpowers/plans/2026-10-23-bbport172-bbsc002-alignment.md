# BBport 1.7.2 + BBSC 0.0.2 development plan

Active R03 ownership2026-10-25: [Claude implementation takeover](../../handoff/R03-CLAUDE-TAKEOVER.md) supersedes historical audit-only/four-document/Codex-only workflow for Claude. Product goals and general baseline-reuse approach stay unchanged; Claude owns implementation/validation and chooses methods independently. Existing R03 acceptance checkboxes remain open until proved.

2026-10-26 acceptance synthesis: [current evidence matrix and remaining checks](../../handoff/R03-ACCEPTANCE-MATRIX.md) reconciles B09-B12 and PR7/8 integration with historical case definitions. This documentation-only checkpoint does not close broad gameplay gates or change Claude's ownership.

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

### Return-to-own-world native test plan (T1–T4)

Status: T1 PASS for protected B17 crash replay ([evidence](../../handoff/R03-T1-POINT-RECOVERY.md)); T2 PASS ([evidence](../../handoff/R03-T2-SAVE-RELOAD.md)); T3 bounded PASS for pending settlement after arrival ([evidence](../../handoff/R03-T3-CHARACTER-CANCEL.md)); pre-arrival cancellation untested; T4 destination/flags PASS on the corrected composition ([evidence](../../handoff/R03-T4-SETTLEMENT-FIX.md)); synthetic-void death avoidance remains open; Echoes protection passes the prepared case ([evidence](../../handoff/R03-RECOVERY-ECHOES.md)). Run in order where practical, preserving the protected B17 crash evidence. These cases use copied profiles and existing authorized inputs, with HOME_RECOVERY enabled only for the copied guest and experimental admission OFF. Record the exact source, patch, DLL and probe hashes, effective configuration, commands, timestamps, positions, flag snapshots and outcomes. Verify original profile paths and hashes before and after; keep saves, credentials and raw logs private. A fixture or an earlier DLL's result is not a native PASS. See [B17 evidence](../../handoff/R03-B17-NATIVE-01.md) and [B19 fix](../../handoff/R03-B19-HOME-POINT.md).

- [x] **T1 — original point after interruption.** Build the current integrated source with its mandatory notices and use a fresh copy of the protected B17 crash save and unchanged owner journal. Resume the owner with recovery enabled; capture the request, settled own-world state and position. PASS requires one accepted original-point request, no lamp fallback or arrived-elsewhere result, the journaled map and rotation, position within 5 m of the journaled point, and unchanged originals. The historical interruption occurred 0.004162 s after placement; this replay tests recovery from that protected input, not a new interruption. If inputs or matching artifacts cannot be established, report NOT RUN.
- [x] **T2 — flags after save and reload.** After a successful T1, take settled own-world flag snapshots, save normally, restart the same copied character and take repeated settled snapshots. Compare all 1,250 groups against the prejoin baseline and a separately captured no-party save/reload control; investigate the six previously unclassified group 12705 bits. PASS requires explaining each difference with evidence and establishing that personal progress is preserved. An unexplained difference remains open, even if the location is correct.
- [x] **T3 — cancellation and character ownership (bounded pending-settlement case).** On a separate copied crash state, start the owner's recovery and interrupt it by returning to title while the return is actually pending. Load a different character, compare its independently captured before/after flags and position, and verify the owner's pending journal remains intact. Then reload the original owner and allow recovery to complete. PASS requires no recovery applied to the other character, unchanged other-character personal state, and successful original-owner retry. A disk-only journal isolation check does not prove in-flight cancellation. The completed case holds settlement with a copied rename blocker after arrival and demonstrates cancellation of active in-memory recovery; cancellation before physical arrival remains a separate open B17 N2 timing boundary.
2026-10-30 recovery Echoes protection: PASS for the prepared void/save-reload case. [Matching-build evidence](../../handoff/R03-RECOVERY-ECHOES.md):535 retained through fallback and independent restart, prior native stain record unchanged; ordinary post-recovery death transfers535 into its stain. Actual-handler fixture RED/GREEN (including nonempty old stain317 and owner/title boundaries),9 checker tests, six settled currency snapshots and original3171 exact. The earlier synthetic-void currency-loss limitation is resolved for this case; native positive-balance prior stain/character-switch and broader default activation remain open.

2026-10-29 user-authorized T4 correction: destination/flags PASS. Native floor=0 false settlement confirmed; actual-function RED/GREEN and9 checker tests pass; matching DLL built. Corrected T4 recorded-lamp persistence and valid-point arrival/flags regression pass. Twelve settled snapshots compare against prejoin or an independent ordinary Hunter's Mark lamp control, fully classifying the six group12705 differences. Original3171 exact, all tests normally closed. [Evidence and limits](../../handoff/R03-T4-SETTLEMENT-FIX.md): the synthetic void still invokes death-style Dream/Echoes loss before fallback; no currency-safety claim or default activation, independent valid-point reload not repeated.

Earlier 2026-10-29 T4 replay: FAIL on unchanged T1 artifacts (superseded for the corrected composition above); [native evidence and separate display verification](../../handoff/R03-T4-LAMP-FALLBACK.md). The edited finite point is accepted and archived as settled, followed by Hunter's Dream; independent restart persists the wrong destination. Three stable snapshots per run differ17/16 bits from prejoin, not fully classified. This established the settlement bug corrected above.

- [x] User-requested small side-by-side test windows: bounded optional BB_WINDOW_RECT in window.cpp; separate display-only probe build exit0, invalid-height default fallback, two900x506 copied offline title windows with58px gap confirmed. Existing T1 probe remains unchanged; fullscreen/co-op gameplay on the new display build not retested.

- [x] **T4 — recorded-lamp fallback (destination/flags gate; corrected composition).** On a separate copy, make only the journal's original point unreachable using the prepared bounded test method, leaving the recorded lamp intact; preserve the unmodified journal. Verify the point fails, fallback reaches the recorded lamp, and personal flags are restored. Save normally and restart; verify the lamp location and settled own flags again. PASS requires correct fallback and persistence, with any flag differences classified using T2's control. Do not alter original saves or the protected crash input.

For every case, record PASS, FAIL or INCONCLUSIVE with its evidence and limitations in the tracker before checking its box. Do not enable recovery by default or close broad R03 acceptance on these tests alone. PR17 reward persistence is deferred separately.

2026-10-28 B17 matching-build native recovery: IN_PROGRESS, user requested N1 early guest interruption/locked-map return, N2 pending-return title/other-character isolation and original-owner retry, N3 journal-point failure/lamp fallback with own-save reload. Use copied profiles and current integrated artifacts; HOME_RECOVERY ON only for copied guests, experimental admission OFF. Keep broad acceptance and production defaults unchanged until actual evidence is recorded.

2026-10-28 B15 normal replay check: IN_PROGRESS at the user's request. Rare write-failure/save-race cases are deferred. Use native04's saved guest with Pendant x1 and a copied live-Amelia host; verify a fresh-process repeated eligible kill, item/log counts, normal return and independent reload on the unchanged native composition. Command-assisted gameplay is authorized while the user is away. No broad checkbox is closed by this scope reduction.

- [x] B15 ordinary replay test completed: default-OFF deduplication gap reproduced; full capacity defers the second reward, using the old Pendant allows a new one, and the duplicate survives independent restart. Exact origin/stable1250/original3171 checks pass. [Native evidence](../../handoff/R03-B15-NORMAL-REPLAY.md). No product fix, B15-ON acceptance or broad R03 closure; rare fault cases deferred.

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

CL02-P01: INTEGRATED / MERGED under the [follow-up package](../../handoff/CLAUDE-CODE-WINDOWS.md#cl02-p01-progress-contract-follow-up). Accepted PR #2 head c4cc3c8 merged as c5018fb; PR closed, source/document handback complete. R04 implementation and native/gameplay proof remain Codex-owned.

CL02-INT01: INTEGRATED / PR #2 MERGED AND CLOSED (2026-10-25). User requests integration after acceptance; approved unchanged head `c4cc3c817b71d5ef028eb1f0e00c02804056c073` merged normally into seamless as `c5018fba039f5c1a8fe527a3d4b6345d896cf4aa`, retaining all four CL02 commits. GitHub confirms closed/merged; local checkout fast-forwarded. Fresh document/citation/link/ID/format/scope checks PASS, no listed statuses or PR workflows. Merge delta exactly four accepted documents/254 additions, every blob byte-identical to reviewed head; no runtime delta. [Integration commands/results](../../WINDOWS-PROGRESS.md#cl02-int01--pr-2-integration-merged--closed-2026-10-25). Source/document handback complete; broad R03/gameplay gates and default-OFF settings remain unchanged.

CL02-REV04: ACCEPTED FOR SOURCE/DOCUMENTS (2026-10-25). Re-reviewed PR #2 correction `c4cc3c817b71d5ef028eb1f0e00c02804056c073` against exact parent 2386dfc and frozen CL01 base 108bf28. Both REV03 findings addressed: party eligibility stays open through same-party death/loading; valid inactive-owner obligations are deferred under their original owner/epoch. A-32/seam (i), G2-19(b)/(c3)/(d) and ranked wording now agree. No new blocking Standards or Spec finding. Fresh four-file/CL01 preservation, 163 citations/29 pinned files, 18 links, 65 claims/38 cases, 11 outcome rows, format/whitespace/parent checks PASS. [APPROVE review 5641948014](https://github.com/kaoitp/bloodborne_pc/pull/2#pullrequestreview-5641948014) posted; both reviewer-owned threads resolved. [Full evidence/hashes](../../WINDOWS-PROGRESS.md#cl02-rev04--pr-2-correction-review-accepted-for-sourcedocuments-2026-10-25). PR description refresh is a non-blocking metadata note. Current B02 delivery evidence is separate; concurrent B03 excluded. No merge/integration, runtime acceptance or new assignment; broad R03 and default-OFF gates unchanged.

CL02-REV03: REVIEW COMPLETE / CHANGES REQUESTED (2026-10-25). User requests PR #2 review; inspected full three-commit delta at `2386dfc6137d502d6464a21fcc16bfec4eb2a31f` against frozen CL01 base `108bf28` and latest correction against c6cb7b3. All REV01 fixes remain closed; REV02's blanket departure/new-epoch discard is removed. Two P2 contradictions remain: A-32/seam (i) require playable/HP-positive/not-loading at every enqueue, excluding eligible kills during same-party death/loading required by outcome 9/G2-19(b); A-32's wrong-owner discard and G2-19(d)'s catch-all discard can delete character A's valid obligation while B is loaded, contradicting G2-19(c3). Keep eligibility once opened until genuine departure; defer valid inactive-owner entries and reject invalid admission records separately. Standards bounded/no new blocker; Spec two findings. Fresh checks PASS: four-file scope/unchanged CL01 byte prefixes, 163 citations/29 pinned files, 18 links, 65 claims/38 cases, 11 outcome rows, UTF-8/LF/no BOM, whitespace and exact parent. [Full commands, document hashes and limitations](../../WINDOWS-PROGRESS.md#cl02-rev03--pr-2-review-review-complete--changes-requested-2026-10-25). No external review/comment submission, merge, runtime change or G2 PASS. Next: focused external correction and re-review; broad R03 boxes and default-OFF gates unchanged.

CL02-REV03 notification follow-up (2026-10-25): user explicitly authorizes notifying the author. Rechecked unchanged head/open PR and posted [REQUEST_CHANGES review 5641693091](https://github.com/kaoitp/bloodborne_pc/pull/2#pullrequestreview-5641693091), API success, with two inline comments and a focused same-branch/four-document correction request. This supersedes the earlier no-submission statement; review checkpoint e2918e4 was already pushed/remote-verified. Await a full correction SHA and re-review; no merge, runtime task, new persistence framework or native/gameplay acceptance assigned.

CL02-REV02: REVIEW COMPLETE / CHANGES REQUESTED (2026-10-25). Reviewed `c6cb7b3d75b164bfbe2b6dc164241141918de615` against prior b48d2b3 and frozen CL01 base. All three REV01 findings addressed; fresh 160 citations/29 source files, 18 links, 65 claims/38 cases, CL01 preservation and format/scope/coverage checks PASS. [One new P2 correction](https://github.com/kaoitp/bloodborne_pc/pull/1#issuecomment-6388357678): A-32/G2-19 must distinguish rejecting events earned after departure from retaining a valid already-earned but unconfirmed reward for its original owner. Dropping every queued entry on departure can lose jointly earned rewards. User waives usage-based stopping; no integration, runtime change or G2 PASS. Next: focused external correction, then re-review; completed REV01 fixes stay closed.

CL02-REV01: REVIEW COMPLETE / CHANGES REQUESTED (2026-10-24). Reviewed handback head `b48d2b36c6e41cb66cfc474287fc5eaf6bec6863` against base `108bf28f069d7017712fd71e24fb7fd6b2bbde36`. Four-file append-only/CL01 preservation, 145 citations/28 source files, 18 links, 61 claims/33 cases, coverage/format/whitespace PASS. [Three correction requests](https://github.com/kaoitp/bloodborne_pc/pull/1#issuecomment-6382726381): receiver does not reject older snapshot IDs; receipt-time/state-6 baselines do not establish playable-party eligibility; reward admission must follow that eligibility rather than unchanged state-6-only hooks. No integration or runtime/gameplay acceptance. Next: focused correction on the same external branch, then re-review; PR #1 stays merged/closed.

[PR approval and CL02 assignment](https://github.com/kaoitp/bloodborne_pc/pull/1#pullrequestreview-5637592348) posted successfully; four REV01 threads resolved. [PR #1](https://github.com/kaoitp/bloodborne_pc/pull/1) is now merged/closed by CL01-INT01.

## CL03 — Existing earned-event and party-epoch feasibility

Owner: external Claude in its separate clone, same four-document allowlist. Status: READY / ASSIGNED. Dependency: integrated CL02 at c5018fb and current B02/B03/C01/B04 records. User authorizes assignment via PR #2 comment. [CL03-P02 work package](../../handoff/CLAUDE-CODE-WINDOWS.md#cl03-p02-earned-event-and-party-epoch-source-feasibility) freezes comparison base `7a5eca3fcdc662afcce1de7b6d57510311b710b2` on new branch `claude/p02-event-provenance`.

Trace existing event/completion/member/host/epoch producers to consumers, test each candidate against C1-C4 on paper, and deliver the smallest discriminating native probes for Codex. Reuse the finite 19 reward events/57 flags; source inability to establish a binding must identify the exact missing evidence. Preserve CL01/CL02 prefixes, stable IDs and historical evidence. No runtime implementation or new protocol/storage/auth framework; external cases remain NOT RUN. New-branch handback uses a new PR; PR #2 stays closed. Codex retains runtime/native/gameplay/integration and all R03/default-OFF gates.

Package published at 80518ab0713b8775248a2a2c63feb025e73d1ae7 after three-document scope/UTF-8/53-link/whitespace and exact staged checks. [Assignment comment 6395443366](https://github.com/kaoitp/bloodborne_pc/pull/2#issuecomment-6395443366) posted successfully with immutable package/base links. Await external start/handback; no execution or gameplay PASS inferred.

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

### B02 boss reward delivery

- [ ] IN_PROGRESS: original-owner retry/confirmed direct delivery for the existing finite boss reward queue; test unavailable state, failed add, departure/other-character isolation and once-only success. Earned-event admission/old-host exclusion remain open; no broad G2 PASS.

- [x] B02 actual-function RED/GREEN and pinned DLL build: owner-bound retry, duplicate protection and frozen first lot. [Evidence and limits](../../handoff/R03-B02-REWARD-DELIVERY.md).
- [x] Frozen same-DLL native join/adjacent placement/normal return; settled and reloaded all 1250 groups exactly equal prejoin. This is join regression, not reward gameplay proof.
- [ ] B02 actual queued reward failure/retry/owner/departure and jointly-earned event gameplay. Old-host-history admission, consumed/owned rewards and crash durability remain open.

### B03 progress merge backup refusal

- [x] Reject mutation/finalization on failed backup or unavailable/mismatching active owner; actual-function RED/GREEN through both callers, pinned build and focused regressions pass. [B03 evidence](../../handoff/R03-B03-PROGRESS-BACKUP.md).
- [x] Native copied-profile backup fault: RED prematurely finalizes; GREEN retains and original-owner retry creates real backup/finalizes; all1250 groups and original3171files preserved. Already-owned synthetic flag, not jointly-earned gameplay.
- [ ] Native in-memory wrong-character owner guard remains unproven: both switch cases timed out before unblocking; file-key isolation and fixtures pass. Other G2/persistence gates remain open.

### C01 locked-own-map acceptance

- [x] Copied fresh Clinic character joins selected Cathedral host; adjacent blue placement, own lamp/all1250 groups and exact journal origin survive return/independent reload. [C01 native evidence](../../handoff/R03-C01-LOCKED-MAP.md). Shared progress and boss items OFF; no jointly-earned proof.
- [x] Record actual self-hosted API/WebAPI/ShadNet/DLLrelay flow and three failing public playlog PUTs that do not stop observed join/return/reload. No blanket unobserved-routing claim.
- [ ] Host flag first writer/consequence remains unresolved: co-op/reload differs, same-DLL five-minute no-peer control stays exact. Remaining G2/candidate/recovery gates remain open.

### B04 host first-writer diagnosis

- [ ] IN_PROGRESS: trace finite C01 host-side flags to actual writer/semantics using existing native sites and exact ELF validation; no speculative restoration or earned-event admission rule.

- [x] B04 narrower no-peer Hunt Bell search control and unchanged-source checks recorded in [B04](../../handoff/R03-B04-HOST-CONTROL.md); no group7 change. Games closed/originals preserved.
- [ ] Actual group7 first writer/meaning and principal G2 earned-event/admission/epoch producer remain unresolved; no source lead promoted to native acceptance.

CL02-REV05 unchanged-head recheck (2026-10-25): user explicitly waives usage stopping for this PR review. Fresh metadata confirms open/unmerged PR #2 at the same accepted c4cc3c8; no commit delta, four-file/254-addition frozen-base stat and whitespace check unchanged. PR description now matches the accepted head and eligibility/deferred-owner correction; prior stale-summary note addressed. Both threads remain resolved and [approval 5641948014](https://github.com/kaoitp/bloodborne_pc/pull/2#pullrequestreview-5641948014) remains present. No new Standards/Spec blocker, duplicate review/comment, merge/integration or runtime test; source/document acceptance stands and R03/default-OFF gates remain unchanged.

CL03-REV01 (2026-10-25): PR #3 head `08c205c08ed75513b02a445f1456fc4e3b349c99` reviewed inline; CHANGES REQUIRED. Four-path/prefix/citation/link/format checks pass. Two Spec P2 findings: local reward callbacks do not prove immunity to delayed world-state input; M1/M3 alone do not close same-host rejoin/epoch C4. See the tracker CL03-REV01 entry. No merge/runtime acceptance; await focused external correction.

CL03-REV02 / INT01 (2026-10-25): both PR3 corrections accepted at `59c91c65f4353dd85dd11a679b029cb23b2e7584`; merged normally as `2707f274edee104b182c59e4d8d7ff347ec831c2`, PR closed and local checkout fast-forwarded. Fresh207citation/32file,27link,41case,11outcome/prefix/scope/format checks pass; exact four-document merge blobs verified. CL03 source handback integrated; NOT IMPLEMENTATION-READY, native probes NOT RUN, R03/default-OFF gates unchanged. See tracker CL03-REV02.

CL04-P03: READY / ASSIGNED via PR3 comment6396665118; package published at6decf55 under the appended handoff package. External source-only observability readiness for the existing CL03 probes; no new runtime ownership or G2 acceptance. Frozen base `7927159f53818d846590b564b4144d6c5e4a0100`, branch `claude/p03-probe-readiness`, same four-path allowlist. Codex retains native execution.

### B05 scheduled native discrimination

- [ ] IN_PROGRESS: G2-20 negative reward-wait probe using the existing B03 DLL, fresh copied before-state and native logs; no new admission/application rule. Host history exclusion, actual joint kill, C1-C4 and other R03 acceptance remain open.


CL04-REV01: IN_PROGRESS (2026-10-25). Review PR #4 against the CL04 package and exact head cb11a4f; verify scoped documents, source-backed observability and unchanged C3/C4 blockers before any merge.

CL04-REV01: ACCEPTED / INTEGRATED. PR #4 exact head cb11a4f merged normally as446183d and confirmed closed. Fresh243-citation/34-file,31-link,41-case,11-outcome,prefix/scope/format/whitespace checks pass; merge blobs match reviewed documents. No blocking Standards/Spec finding. G2-17,C3/C4,R03 and default-OFF gates unchanged; no native test or runtime delta. Existing B05 work preserved.

- [x] B05 bounded G2-20/G2-21 negative native observation and exact1250group normal return. [Evidence/limits](../../handoff/R03-B05-EVENT-PROBES.md).
- [ ] Positive joint kill, dead/loading producer sensitivity, C3/C4 and remaining R03 gates; G2-22(g) graphics-blocked, no actual positive kill; fresh copied tests normally closed.

### B06 completed snapshot ordering

- [x] Actual receiver RED/GREEN for older completed/partial input; duplicate/map/Dream/wrap/reset/invalid input checks, DLLbuild and normal candidate guest native join/adjacent placement/return. [B06 evidence](../../handoff/R03-B06-WORLD-ORDERING.md).
- [x] Classify six reload bits and independent candidate reload: early-load transients, settled reload exact. [B07](../../handoff/R03-B07-INDEPENDENT-RELOAD.md).
- [ ] C3/G2-17 native reordered-input/callback proof. Actual joint earning/first-playable/party epoch/history exclusion/C4 and remaining R03 gates remain OPEN.

### B09/B10 party-earned shared progress (Claude)

- [x] Per-party baseline in the existing collector, kill-time reward event admission, `BBS2` pending magic; actual-function RED/GREEN. [B09](../../handoff/R03-B09-PARTY-PROGRESS.md).
- [x] Merge finished only after the game saves; close-before-save re-merge proven natively.
- [x] Native Amelia: host history excluded, joint boss kept by host and guest after their reloads.
- [ ] G2-17/C3 live reorder, G2-22(d)/(g) boundaries, dead/loading guest earning, wider progress classes.


### PR #7 review (2026-10-26)

- [x] Inline exact-head review `e4e0f8c`, reconstructed pinned source, five actual-function fixtures and two native-header tests PASS; whitespace clean.
- [x] Historical PR07-REV01 blocker resolved by `2522e2f`: independent party-placement latch and spectate-OFF reward regression. Exact head `b66936a` accepted after five actual-function fixtures PASS. This does not close broad R03 gameplay gates.
### B11 party boundaries (Claude)

- [x] Departure (state 6 → other) ends the party: native rejoin and host-character change, fixture for rejoin before the unlock.
- [x] Dead guest at the kill earns and receives after the respawn (native).
- [x] Reward item only after placement (fixture RED/GREEN); native pre-placement window not reproducible with this rig.
- [x] CL03 B-30 label resolved natively.
- [ ] G2-17 native injection seam; a guest in a follow load at the kill; progress classes beyond the boss area.

### PR #7 / #8 integration (2026-10-26)

- [x] Merge reviewed heads `b66936a` then `84d3fbd` locally; preserve both documentation histories. Runtime/tests match the reviewed heads; PR7 7/7 and PR8 8/8 focused actual-function/native-header fixtures PASS, including ASan.
- [x] Publish without force: PR7 merged as `97493d9`, then PR8 as `0251ff2`; GitHub confirms both CLOSED/merged. Remote-tracking seamless matches the published merge. Native gameplay/full R03 acceptance remains separate.

PR09-INTEGRATE (2026-10-26): VERIFIED / MERGED AND CLOSED at `1b2625c`. Integrate documentation head `8502fbe` into current seamless with both tracker histories retained. Author native spectate-off reward evidence is bounded; broad R03 checkboxes remain open. Exact B11 blob, document structure/59 local link targets, whitespace, normal publication and GitHub MERGED readback verified; see the progress tracker for commands and limitations.

### PR #10 review (2026-10-26)

- [x] Exact-head `2bb0d37` inline standards/spec/caller review, seven actual-function fixtures plus two native-header tests PASS (no skips), whitespace clean.
- [x] B13 provenance completed and PR10 integrated as26952d9; native gameplay not replayed and broad R03 gates remain open.

### PR #11 review (2026-10-26)

- [x] Inline exact head `4dc9369`: 9 focused fixtures/header tests PASS, whitespace PASS; two extra actual-function safety controls reproduce same-name and unavailable-name cross-character restoration.
- [x] Original P1 stable identity/unknown deferral and B14 provenance addressed at385db1b; original-owner fixture passes.
- [x] Normal own-file-before-progress ordering fixed at6b406ed; combined10-test union PASS.
- [x] File-status errors defer at both queries in782a74b; all10 exact candidate fixtures PASS.
- [x] Published normal PR11 merge17be9b4; fresh GitHub confirms MERGED. Final native/R03 acceptance remains open.

### PR #10 provenance re-review / integration

- [x] Exact d7da4f2 provenance accepted; source line-ending hashes independently match, reviewed runtime/tests unchanged; approval5650133506.
- [x] Both tracker histories preserved and integrated fixtures/links/whitespace verified.
- [x] Published normal merge26952d9; fresh GitHub confirms PR10 CLOSED/merged=true. Broad R03 gates remain open.

### Graphify local tooling
- [x] Local code graph and query/export/integrity verified; generated outputs ignored. See docs/GRAPHIFY.md and GRAPHIFY-INIT progress checkpoint; scoped publication authorized.

### PR12 / PR13 review (2026-10-27)

- [x] Exact-head inline review and pinned-source/actual-function checks; PR12 union10PASS/1FAIL and unsaved-reward safety control fails; B16 lifecycle evidence and prerequisites read.
- [ ] IN_PROGRESS / awaiting author: preserve integrated PR11 protections in PR12 and make durable reward suppression consistent with actual owner saves (review5662203115).
- [ ] IN_PROGRESS / awaiting author: correct B16 tested composition and bound position/early-load conclusions (review5662203440); durable-origin implementation is already within the active takeover, with safety/native gates still required.

### PR12 / PR13 revision 2 (2026-10-27)

- [x] PR12 integrated owner/title/order/error protection union passes11 tests; original unsaved-success fixture addressed.
- [ ] IN_PROGRESS / awaiting author: failed-grant then save/exit still becomes permanently given; actual-function negative reproduced, REQUEST_CHANGES sent. Save snapshot timing remains unproved natively.
- [x] PR13 B16 provenance and bounded observations corrected at2aab142; acknowledgement sent.
- [ ] Integrate corrected documentation when B15 link dependency is available or changed to PR12 URL; align stale PR descriptions. No broad R03 gate closed.

### PR14 durable-origin review (2026-10-27)

- [x] Exact e149702 source/callers and11 fixture/header tests verified; accepted-request/no-load negative reproduced.
- [ ] IN_PROGRESS / awaiting author: bounded arrival timeout, point-to-lamp fallback, fifth-arrival ordering and tests; REQUEST_CHANGES sent.
- [ ] Matching-build native owner/return/fallback and settled reload before accepting new default. No R03 acceptance closure.

- [x] PR13 exact85e9e12 approved and documentation integration verified; native/origin gates remain open.

### PR12 revision3 / PR14 revision2 (2026-10-27)

- [x] PR13 merged8dd412b and MERGED readback confirmed.
- [ ] PR12 IN_PROGRESS / awaiting author: initial confirmation-write failure plus saved/consumed/restart still duplicates;11 standard tests pass, new actual-function negative fails; request5668258541.
- [x] PR14 exact2e323f9 timeout/fallback/budget corrected and11 tests pass; default OFF candidate approved5668259763; integration source/docs verified.
- [ ] PR14 native N1/N2/N3 and final same-build R03 acceptance remain open; no default enablement.

- [x] PR12 rev4 exact e77f1a6:12 fixture/header checks PASS; initial-write deferral verified.
- [ ] IN_PROGRESS / awaiting author: failed add plus failed removal/save/restart is held forever; actual-function negative reproduced. Resolve safely or keep default-OFF candidate with remaining protocol/native gates.

### PR12 revision5 gated integration (2026-10-27)

- [x] Exact976c13b default-OFF record candidate reviewed;12 actual-function/header tests PASS, normal existing default retained; approved and integration verified.
- [ ] Failed-outcome protocol ambiguity, in-flight-save and matching-build native reward gates remain open. No R03 gate completion/default enablement.


### R03 final native acceptance (2026-10-27)

- [ ] IN_PROGRESS R03-FINAL-NATIVE-01: isolated final-source build, copied-profile native join/return/reloads and bounded pending gates; record actual evidence before closing any acceptance.

- [x] R03-FINAL-NATIVE-01 bounded Clinic/Cathedral join, normal guest return,1250-group preservation through title and fresh-process reload on current composition. Source/build/fixture/native evidence recorded separately.
- [ ] IN_PROGRESS R03-FINAL-NATIVE-02: same-composition positive boss/reward and saved progress, command-assisted boss HP-0 on fresh test copies. Broad R03 and remaining native gates stay open.

- [ ] R03-FINAL-NATIVE-02 remains open: staging inconclusive (guest respawn-map mismatch plus invalid position aid; kill helper precondition stop). Both copied test processes stopped; clean same-map staging and validated boss lookup required before positive reward/save assertions.

- [x] User-requested no-death test setup: existing cheat_no_death=1 in both fresh native03 copied profiles; compiled patch writes independently asserted.
- [ ] Native03: verify both survive actual boss hits; then validate live boss target and complete joint kill/reward/reloads. No-death does not close death/recovery gates.

- [x] Native03 both runtime no-death flags read1; host remained alive at1HP after aided staging.
- [ ] Boss-hit survival on both, stable staging/actual join, validated boss target, kill/rewards/reloads remain open; bounded native03 checkpoint stopped near usage threshold.

- [x] Read-only boss HUD handle-decoding preflight matches existing helper arithmetic (0x164c392..0x164c446); no unproved formula change.
- [ ] Live pointer-state discriminator and pending native03 boss gates remain open. Mandatory usage stop at9% remaining; no native launch this continuation.

### PR15/16 monitor review (2026-10-28)

- [x] PR15 exact7e4d240 checker9 synthetic tests PASS; duplicate-middle-process false PASS and equal-ms false INCOMPLETE reproduced.
- [ ] IN_PROGRESS awaiting author: all-process duplicate checking and entry-sequence timing guards (review5679210406).
- [x] PR16 exact2c59b0d source/table review; map-only journal premise contradicted by Dream keys5/50000.
- [ ] IN_PROGRESS awaiting author: correct persistence claims, full hashes and reproducible static extraction (review5679210861). No native/R03 gates closed.

- [x] Native04 bounded command-assisted Amelia co-op kill, guest reward4001x1, automatic exact-origin return and both fresh-process save+journal reload verified; originals3171 exact. See docs/handoff/R03-FINAL-NATIVE-04.md.
- [ ] Actual boss-hit survival of both, raw-save/journal independence and wider interruption/party-boundary gates remain open. Earlier native02 staging failures preserved as history.

### PR15/16 revision2 review (2026-10-28)

- [x] PR15 exact3e3035e corrected all-process duplicate/line-order/midnight behavior;9 synthetic tests PASS, approved as read-only tooling.
- [ ] PR16 c5d2dfa: source-policy correction accepted; malformed UTF16 archive EOF hang reproduced, parser bounds/test and stale PR description requested.
- [ ] Broad R03/native and B15 protocol gates remain open; no default change or native replay by review.

- [x] PR16 revision3 exact2200710 EOF/table/member guards and5 synthetic checks pass; static research/read-only reader approved.
- [ ] Real-archive replay unavailable on review machine; native reward/protocol/R03 gates unchanged, defaults OFF.

B17 native checkpoint2026-10-28: [evidence](../../handoff/R03-B17-NATIVE-01.md).
- [x] Actual guest interruption within10s, preserved journal, fresh owner recovery observed; originals3171 exact.
- [ ] N1 exact point: FAIL,16.086579m miss followed by lamp fallback.
- [ ] N3 full save/reload: lamp position persists; six group12705 bits unclassified.
- [ ] N2 full in-flight cancellation/other-character flags/owner retry: bounded disk-journal isolation only.
- [ ] N4 optional OFF control: prepared, not run. Defaults OFF; quota checkpoint, no product change.

### PR17/18 monitor review (2026-10-28)

- [x] PR18 exact815feef synchronous recovery guard fix reviewed;12 actual-function/header tests PASS/no skips; merge preserves defaultOFF.
- [ ] PR17 exact22ea102 own-boss suppression blocks never-delivered reward after saved progress/restart; negative reproduced, review5684981623 requests fix/regression and patch regeneration after PR18.
- [ ] Matching-build B19 native point return and remaining B15/B17/R03 gates open; fixtures are not native acceptance.

- [ ] PR17 revision2 exact20513cb IN_PROGRESS:12 focused checks PASS; complete owed-ledger/protocol review after mandatory quota stop (primary2% remaining). No approval/merge/native acceptance.

- [ ] PR17 B18 matching-build native repeat-kill, consumption/reload and never-beaten control: IN_PROGRESS; 2026-10-29 preconditions verified but inventory labels unresolved, no kill; see WINDOWS-PROGRESS checkpoint and PR comment 6476702825.

- [x] PR17 revision3 exact5e70926: focused12 checks, DLL build and copied-profile repeated-Amelia guard/consumption/fresh-process Pendant0 validation PASS; [evidence](../../handoff/R03-PR17-NATIVE-VALIDATION.md).
- [x] PR17 revision3 never-beaten native control: first Pendant x1, one confirmed grant, no owed entry after delivery and exact origin return PASS. Deferred-delivery/fault gates and broad R03 acceptance remain open.

- [ ] PR17 final owner requirement: dedup ON by default only after investigating/addressing lasting owed-write/removal failure loss/duplicate risks with fault/restart/owner regressions and targeted native evidence; PR comment6477809673. Default-OFF remains interim. Quota stop at8% remaining.

### Private two-player test bundle (2026-10-30)

- [ ] TEST-RELEASE-01 PENDING: user-authorized local trial EXE/ZIP for owner and friend; no live-server redeployment. Mandatory quota stop at8% primary remaining before implementation. Reuse existing Windows packaging, exclude assets/saves/secrets/logs, verify current runtime composition/dependencies/notices and startup, record hashes and explain unfinished R03/reward/recovery gates. See WINDOWS-PROGRESS checkpoint; no build/package/publication produced yet.
- [ ] TEST-RELEASE-01 IN_PROGRESS (2026-10-30): user explicitly authorizes GitHub pre-release and default branch change and overrides quota stop. GitHub default branch changed to seamless. Build/package current composition, exclude private data and validate before publication.
- [ ] TEST-RELEASE-01: default branch switched to seamless. Base staging produced; archive step failed in MSYS2, BBSC composition and pre-release publication remain open.

- [ ] Investigate/fix packaged launcher Test connection HTTP Errno 2 despite independent endpoint HTTP 200; reproduce and verify a rebuilt package. See WINDOWS-PROGRESS 2026-10-30.
- [ ] IN_PROGRESS LAUNCHER-HTTP-01 / TEST-RELEASE-01: reproduce packaged HTTP Errno 2, fix root cause, regression-test the frozen launcher and package, then publish user-authorized pre-release; preserve copied profiles and R03 default gates.
- [x] LAUNCHER-HTTP-01: missing custom Python SSL certificate bundled; frozen HTTP probes 200 for both endpoints and closed-port negative passes. GUI and full multiplayer package flow remain unverified; see WINDOWS-PROGRESS.
