# R03 playtest follow-up: execution and tracking plan

Created 2026-10-31 (Asia/Bangkok). Owner: Codex, inline. Overall status: **IN_PROGRESS — investigation/planning only**. Current next task: **PT01**. The user's no-code-change instruction remains active; this plan does not authorize implementation, runtime instrumentation or new builds. PT06 onward describes later work, held until the user authorizes code changes. Investigation can continue with existing read-only tools and copied inputs.

## Scope and known evidence

1. **Role/bells/menu:** host -> guest can consume pending type 0 and create a host-type character in a guest session. Find the writer/lifecycle failure and verify bells, Blank, leave menu and Insight behavior; UI symptoms need their own evidence.
2. **Solo boss gauge after interruption:** distinguish real combat/event state from a stale gauge. Investigate collected transient combat flags and restore/merge ordering, preserving earned progress.
3. **Ordinary-enemy loot:** user confirms guests see and collect monster ground loot normally. Investigate retiring automatic compensation and its notice while preserving pickups, boss rewards and persistence.

[Investigation evidence and artifact hashes](../../handoff/R03-PLAYTEST-LEADS.md) are the source record. [Shared tracker](../../WINDOWS-PROGRESS.md#two-player-playtest-follow-up--in_progress-2026-10-30) links here. Gascoigne key and Echoes were received: reward loss is **not** an active issue. The crash's cause is unproved; record crash evidence if available, but do not expand this plan into a general renderer investigation without a relevant finding. These tasks do not close all R03 acceptance gates.

## Status rules

`DONE` means the task's stated output exists with evidence; `READY` means prerequisites are met; `PENDING` means prerequisites remain; `IN_PROGRESS` means actively being worked; `HOLD` means implementation authorization is absent; `BLOCKED` requires a named missing prerequisite and next action. Case verdicts are separate: PASS / FAIL / INCONCLUSIVE / NOT RUN. User gameplay reports, static analysis, fixtures and native gameplay must remain separately labeled. Check a task box only when its output is complete; an investigation task can be DONE with an unresolved cause explicitly recorded.

## Ordered work queue

Work sequentially PT01 -> PT02 -> PT03 -> PT04 -> PT05. Investigations PT03/PT04 depend on PT01, not on a successful fix of PT02. A blocked case does not prevent independent investigation; retain its unresolved status. Do not start fixes during this phase.

| Done | ID / status | Work and dependency | Completion evidence |
| --- | --- | --- | --- |
| [x] | PT00 / DONE | Consolidate existing logs/source leads and user corrections | Linked investigation record, hashes and candidate remedies; checkpoints `6417cd9`, `f935fde`. Static/log review only. |
| [ ] | PT01 / READY | Protect inputs and establish matching composition | Private copies of both clients' relevant saves, journals and logs with hash manifests; installed DLL/probe/settings attribution. Friend DLL hash or explicit missing-artifact limitation. Original files stay untouched. If the exact crash input is gone, label a newly recreated input separately. |
| [ ] | PT02 / PENDING | Diagnose stale pending-role producer; depends PT01 | Trace native writers/readers of slot manager +0x8C. Compare bad and good lifecycle paths; record caller, pending/sign/slot/character role and cooperator count. Identify a supported cause or the exact missing observation; specify the narrow fix boundary. Existing logs are evidence, not a fresh reproduction. |
| [ ] | PT03 / PENDING | Diagnose boss/event replay; depends PT01 | Map start/transform/completion flags to event consumers; compare pre-restore/post-restore/post-merge gauge and flag state on copied inputs using existing tools where sufficient. Classify transient versus durable bits with evidence; distinguish late event initialization from gauge-only state. |
| [ ] | PT04 / PENDING | Establish ordinary-enemy loot behavior; depends PT01 | Counts before kill, after kill without pickup, after pickup for an identified enemy/drop. Record host and guest, automatic grant versus manual pickup, full-inventory behavior and rare-loot coverage. Prove duplication only if observed; identify all compensation callers/helpers and shared-switch users. |
| [ ] | PT05 / PENDING | Write concrete implementation proposal; depends PT02–PT04 | Per issue: proven gap, smallest producer/consumer change, affected callers/config/tests, risks and regression cases. Mark unresolved cases and any diagnostic instrumentation required. No broad flag-range filter, forced type1 tick loop or global GUEST_ITEMS disable. End this phase with a reviewable proposal. |
| [ ] | PT06 / HOLD | Implement scoped changes after authorization and PT05 | Separate reviewable patches for role lifecycle, demonstrated boss-state correction and redundant compensation removal. Preserve ground loot/boss rewards; changes must reach the tracked integrated patch. No speculative fix for an unresolved cause. |
| [ ] | PT07 / HOLD | Focused fixture/build checks; depends PT06 | Meaningful actual-function regression for changed nontrivial logic, relevant existing checks and matching DLL build with mandatory notices. Record commands, exits, skips and exact source/patch/artifact hashes. A fixture PASS does not qualify gameplay. |
| [ ] | PT08 / HOLD | Matching-build copied-profile native cases; depends PT07 | Execute the case matrix below, record actual outcomes and independent save/restart evidence. Any failed or inconclusive required case keeps its issue open. |
| [ ] | PT09 / HOLD | Combined two-player regression and handoff; depends PT08 | Same composition on both clients; role switch, boss completion/interruption recovery and manual loot flow pass together. Update evidence/tracker/parent-plan boxes, record remaining limitations, commit/push normally to origin/seamless. No packaging or live-server deployment in this plan. |

## Case matrix and acceptance

Each case starts from protected copied profiles and records effective settings. Native observations in PT02–PT04 are baseline diagnostics if existing tools suffice. If a case requires code instrumentation or a new build, mark it NOT RUN with that dependency and carry it to PT05; do not silently cross the current no-code boundary. Later run candidate and relevant baseline controls with matching artifacts.

| Case | Scenario / purpose | Required result for a future fix |
| --- | --- | --- |
| R1 | Fresh-process guest joins; control | Slot/character type1, own-world false, cooperator counted by both clients, normal menu. |
| R2 | Host joins party, dies/respawns, ends session with Blank, then joins as guest | First join has correct native role; stale host override not applied. Bells do not loop, normal Blank/leave menu, no unexplained Insight gain. Capture actual menu/item/animation separately from role logs. |
| R3 | Host without death -> guest; normal guest leave/rejoin; guest death/respawn | Native role and phantom flags remain valid; return/rejoin works and own-world role is restored. |
| R4 | Legitimate invader/duel paths if touched by shared code | Intended native roles retained. A shared-role change cannot pass solely on co-op type1 cases. |
| B1 | Completed Cleric Beast/Gascoigne party followed by guest interruption and fresh solo reload | No unintended boss gauge/combat restart; completion and legitimate jointly earned progress remain. Capture all three gauge slots and relevant flags across restore/merge. |
| B2 | Same completed state with normal return; independent solo-load control | No spurious fight; explain differences against controls. Compare settled own-world flags, map/origin and inventory; use repeated snapshots to avoid loading transients. |
| B3 | Genuinely unfinished boss fight, including Gascoigne transformation | Real fight and gauge start normally, transformation/kill/reward work. Filtering must not suppress legitimate combat or completion. |
| L1 | Identified ordinary enemy, with no pickup then manual pickup | After compensation removal, no automatic grant/banner; ground drop pickup adds the actual displayed quantity once. Do not expect every random kill to drop an item. |
| L2 | Full inventory and Wandering Madness/rare material drop | Correct native capacity/loot handling; guest can receive eligible ground loot. If historical rare-loot coverage is unavailable, disclose it and leave that boundary open. |
| L3 | Boss reward and world pickup; return and independent save/restart | Boss rewards still delivered; picked items/counts persist and one-time world pickups do not reappear unexpectedly. Shared GUEST_ITEMS behavior retained. |
| X1 | Combined scenario and original-data check | Role switch -> party play/loot -> completion/interruption -> recovery/restart retains correct role, own progress and eligible rewards. All original profile paths/hashes unchanged. No secret/save/log committed. |

## Candidate boundaries to assess in PT05

- **Role:** fix the lifetime of the pending role at its verified writer or cleanup boundary before character creation consumes it. Inspect death/respawn and session transitions; preserve invader types and phantom initialization. Repeated banners/Insight might require additional evidence even if role is corrected.
- **Boss:** exclude only demonstrated transient combat state from durable collection/replay, or correct restore timing if proven necessary. Preserve completion, shortcuts, personal quest state and rewards. Clearing whole groups or hiding the bar is insufficient.
- **Loot:** remove the ordinary-enemy automatic compensation path and notice if baseline coverage supports it. Preserve ground-loot view, pickability, pickup journaling and `NoteBbscBossRewardEvent`; they share GUEST_ITEMS. Reuse/delete helpers according to actual callers; no new option is required merely to preserve a redundant path.

## Evidence and checkpoint format

Keep raw inputs under a private ignored directory. For every executed case record: ID, date/time/timezone, baseline or candidate, source commit/patch hash, both DLL/probe hashes, effective relevant settings, copied profile/character ownership, starting state, exact commands/actions, timestamps, expected/observed result, exit codes, evidence locations/hashes and limitations. Protect the pre-case save+journals before a destructive copied-profile probe; save/close normally before copying after-state. Do not use original saves as test subjects.

At each checkpoint update the queue and this compact result ledger, then update the shared tracker/parent plan before commit. Do not erase failed baseline evidence after a successful fix. Publish documentation/checkpoints without raw logs, assets, saves or credentials.

| Date | Task/case | Evidence type | Result / output | Next action |
| --- | --- | --- | --- | --- |
| 2026-10-30 | PT00 | Static analysis + existing captured native logs | DONE for leads; gameplay issues unresolved | PT01 input protection/attribution |
| 2026-10-31 | PT00 / loot clarification | User gameplay report + source review | Guest ground loot confirmed by user; duplicate delivery unproved; scope revised | PT04 count comparison; preserve pickup/reward systems |
| 2026-10-31 | Planning | Documentation only | Ordered tasks, dependencies, acceptance and hold boundary recorded | PT01; no implementation in this request |

Completion of this follow-up requires PT09 and the applicable required native cases; unavailable evidence remains explicit. The current deliverable is this plan, not completion of the fixes.
