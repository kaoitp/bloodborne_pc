# Claude Code work package: CL01

Updated: 2026-10-25 (Asia/Bangkok). CL01 is integrated by PR #1; CL02-P01 head `c4cc3c817b71d5ef028eb1f0e00c02804056c073` is integrated by PR #2 at `c5018fba039f5c1a8fe527a3d4b6345d896cf4aa`. Both are source/document acceptance only. The active external assignment is [CL03-P02](#cl03-p02-earned-event-and-party-epoch-source-feasibility); the earlier packages remain historical scope. Parent: R03/R04 in the [active plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md).

## Assignment and ownership

Help the primary owner reproduce supported story-map/Hunter's Dream join, jointly earned progress and self-hosted services by auditing the pinned source and preparing actionable test cases. Preserve other baseline systems; Chalice is unsupported. This is a source/document assignment in your own clone, while Codex continues runtime work.

| Owner | Work | Writable paths |
|---|---|---|
| Codex | R03 copied-profile native/gameplay tests, runtime/build/tests/runner/config changes justified by R03, R04 implementation, shared plans/checkpoints and integration | Everything outside the Claude allowlist; shared plans and this work package |
| External Claude Code | CL01-A gameplay/source reuse map | `docs/collaboration/claude/BBSC-002-MAP.md` |
| External Claude Code | CL01-B service routes and relevant identity/session boundaries | `docs/collaboration/claude/IDENTITY-PROTOCOL.md` |
| External Claude Code | CL01-C acceptance cases after A/B | `docs/collaboration/claude/ACCEPTANCE-CASES.md` |
| External Claude Code | CL01 progress/checks/handback | `docs/collaboration/claude/PROGRESS.md` |

These four paths are the complete Claude write allowlist. Create the three deliverable documents when their slice begins. All source, AGENTS.md, this work package, shared tracker/plan, runtime configuration and other documents are read-only for Claude. Codex will not edit the four deliverables during the external audit; accepted handback integration is Codex's responsibility. A required change outside your allowlist becomes a finding, not an edit.

The friend runs Claude Code directly; neither side dispatches automatic subagents. Root instructions to develop on `seamless` apply to the primary owner; the external audit uses the separate branch explicitly prescribed below. Do not share Codex's checkout, index, private evidence, build directory or game/profile/server session.

## Start and freeze your inputs

Read, in order: root `AGENTS.md`, [Windows handoff](WINDOWS-RESUME.md), [active plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md), [shared progress](../WINDOWS-PROGRESS.md), [R02 evidence](BBSC-BASELINE.md), [product outcomes](../superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md), then this package.

```powershell
git clone --single-branch --branch seamless https://github.com/kaoitp/bloodborne_pc.git bloodborne-cl01
cd bloodborne-cl01
git status --short --branch
git remote -v
$auditBase = git rev-parse HEAD
git merge-base --is-ancestor f3734da56722f21dd2c25dcca89b85d1c93f2109 HEAD
# Continue only if the ancestry command exits 0 and this clone is clean.
git switch -c claude/bbsc002-reference-audit
```

Record the full `$auditBase`, branch and remote in your child tracker. Keep that base frozen for this audit; Codex may advance `origin/seamless` independently. Do not pull/rebase/reset to chase those changes during the audit. If resuming your own branch, inspect status/history and continue without overwriting unfinished work.

Obtain public reference source under ignored `.superpowers/reference/` in your own clone. Verify its full commit, using `core.autocrlf=false` for the reference clone so patch bytes can be hashed without checkout conversion:

```powershell
New-Item -ItemType Directory -Force .superpowers/reference | Out-Null
git -c core.autocrlf=false clone --no-checkout https://github.com/CLSAMG22/BBSC.git .superpowers/reference/BBSC
git -C .superpowers/reference/BBSC -c core.autocrlf=false checkout --detach 4f11faf88b6ba658ebde6fe5fbefdadedba4fa41
git -C .superpowers/reference/BBSC rev-parse HEAD
Get-FileHash .superpowers/reference/BBSC/bbport/bbport-1.7.2-bbsc.patch -Algorithm SHA256
```

Expected BBSC commit: `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`; canonical patch SHA256: `e34c79b388605998b430ec4eed556fc2cb8c8928f1d3e9f26bf5d2df29732aa3`. Stop that dependent source task on a mismatch and record it. Preserve the upstream BOM; avoid text-mode re-encoding. Baseline BBport source `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d` is in this clone's history and can be read with `git show`; the actual patched runtime is at your recorded audit base. `seamless` already includes the BBSC patch: do not apply it again. No submodule initialization, dependency install, native build, artifact download or game setup is required for this audit.

## Existing evidence and what remains independent

R02 source/build/native-load checkpoint `f3734da56722f21dd2c25dcca89b85d1c93f2109` and its publication record `4866002514de55c60e6f5e5475d797eed4131f1d` precede this handoff. R02 already verified patch composition, the official DLL/original loader/notices, a fresh CLANG64 build and copied-profile image/hooks/HTTP-override startup. Reuse [that record](BBSC-BASELINE.md); independently explain the source ownership, rather than rerunning R02. Attribute its native results to Codex's recorded evidence, not to tests you executed.

G1/G2/G3 remain open. Last recorded private setup has separate ShadNet and game-server endpoints: ShadNet TCP 31313/31315 and game API TCP 20443 reachable; game relay TCP 20444 not reachable. This is an observation, not a reproduced product gap or proof the relay is required. Deployed versions are unknown. Audit existing relay/P2P fallback and split-service configuration from source; do not contact private services, ask for the deployed version again or propose deployment as your assignment. Private addresses, account credentials and copied game/profile data are unnecessary for your work.

| Slice | Dependency | Can run alongside Codex R03? | Done when |
|---|---|---|---|
| CL01-A | Frozen audit base, pinned BBSC reference | Yes; no live profile/service input | Every row below has source citations and a stated test boundary/unknown |
| CL01-B | Same pins; independent of A | Yes; source/config reading only | Every required route and relevant identity hop below is accounted for |
| CL01-C | A/B findings for final citations; draft IDs may start earlier | Yes; writes specifications only | Every required case has setup, real boundary, assertions, cleanup and evidence/blocker |
| Handback | A/B/C plus document checks | Yes; Codex alone integrates | One scoped commit and complete handback summary |

A and B are independent investigations, but this single external Claude session can do A then B, followed by C. Neither blocks Codex's independent native/gameplay work. R04 fixes still require R03 reproduction and relevant findings; your audit does not authorize implementation.

## CL01-A: gameplay behavior and reuse map

Write `BBSC-002-MAP.md`. Begin with exact source pins and a concise composition/caller summary referencing R02: transport patch versus DLL, existing injector/environment path, required manifest/notices, tables and game-derived data. Explain why `OnBbscHostFollowPacket` / `OnBbscWorldFlagsPacket` in the BBport shim are intentionally empty and which DLL paths own gameplay. No replacement implementation is requested.

Then trace these product boundaries in pinned source:

1. Same-map versus same-nonempty-password cross-map/Dream matching, selected-host placement and guest-map locks.
2. Guest becomes playable/eligible; host's visiting world state versus events actually earned together; departure ends eligibility.
3. Earlier host progress versus jointly earned boss/story flags, guest's own earlier progress/NPC choices, relevant item/reward re-grants and save/reload.
4. Pre-join world/map/position/lamp preservation, normal departure/disconnect, interrupted-session recovery and unsupported-area departure.

For each behavior row include: claim ID (`A-01` etc.), required outcome, actual source behavior, immutable commit + repository/path + symbol + one-based line(s), producer/consumer/caller, source-status, missing runtime evidence, matching C-case IDs, and the smallest candidate change location only if source evidence supports a mismatch. Do not enumerate all game quests/items or design new storage/auth frameworks.

Use PRESENT-NOT-TESTED for source presence, UNSUPPORTED where explicitly established, and cite attributed external evidence separately. EXISTING/PASS requires matching actual runtime evidence for that exact behavior. REPRODUCED-GAP requires an actual R03 reproduction; static suspicions stay labeled **candidate gap (source only)** in the findings column. Native DLL startup does not pass join/progress/return.

## CL01-B: self-hosted route and identity map

Write `IDENTITY-PROTOCOL.md`. Own route/identity facts here; A links to B instead of duplicating them.

- Map account/authentication, game API discovery/ss.info, summon/WebAPI, Matching2/signaling/STUN/P2P, gameplay-mod channel/relay and transport relay. For each: client producer/config key, destination service, source-declared protocol/default port, server implementation availability and relevant consuming path. Separate source-available, reference-only, binary-only and unknown components.
- Explain same-host and split-host configuration through existing settings, including `BB_PROBE` -> `BBSC_EMULATOR`, `SHADPS4_HTTP_HOST_OVERRIDES_JSON`, `BB_SHADNET_*`, `BBSC_RELAY`, `SHADPS4_P2P_RELAY` and any additional setting only when supported by pinned source. State where defaults would accidentally pick the wrong host or a public service.
- Trace TCP :20444 gameplay relay versus existing P2P-channel fallback and UDP transport relay. Identify prerequisites, routing/peer/session checks and observable evidence needed to prove fallback. A reachable TCP port is not protocol/authentication success; an unreachable optional relay is not proof multiplayer fails.
- Trace selected candidate/online ID/account/user ID, character and party/session/peer only at join/progress boundaries that matter. Show actual conversions and validation/rejection of stale/unrelated traffic. Equal numeric IDs or shared endpoints do not prove identity.

Each route/hop needs immutable commit/path/symbol/line citations and one of SOURCE-PRESENT, BINARY-ONLY, UNKNOWN, or attributed tested evidence. End with concrete questions for Codex's R03 checks and C-case references. Preserve existing auth/validation; no new account/backend/HMAC/public-service/cross-emulator project.

## CL01-C: executable acceptance cases

Write `ACCEPTANCE-CASES.md`, referencing A/B claim IDs and real production symbols. Use stable case IDs (`G1-01`, `G2-01`, `G3-01`, `SVC-01` etc.). Each case must contain:

- Required outcome and setup: distinct authorized existing accounts, separate copied profiles/ports, host/guest map/progress preconditions and service configuration placeholders.
- Action/input and exact producer/consumer boundary from pinned source; what to capture before/during/after.
- Expected allowed/rejected behavior, own-world/no-side-effect assertions, relevant reward/flag deduplication and separate save/reload checks.
- Cleanup/normal exit/retry, evidence type (source/fixture/native/gameplay), execution status NOT RUN, and precise dependency/blocker. Never invent offsets, APIs, results or a deployed-service version.

Coverage must include supported cross-map/Dream and selected host/password, existing same-map behavior, wrong/stale/failed join without guest-world mutation, guest entering a locked own-world map, eligibility across death/loading, no import of older host history, own-progress/NPC preservation, jointly earned flags/rewards without duplicate re-grants, each save/reload, normal Blank/exit/disconnect, process interruption/reload/fallback lamp, unsupported-area exit and self-hosted routes without required public endpoints. Wrong-character/write-failure/crash/retry cases are conditional on an actual proposed persistence change; label the condition. C specifies tests; Codex owns implementing/running them.

Finish with a coverage matrix mapping all 11 numbered [product outcomes](../superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md) to case IDs, evidence needed and blockers. Source questions can be resolved here; absent gameplay access remains an honest NOT RUN, not a reason to invent PASS.

## Checkpoints and handback

Mark CL01 and each active slice IN_PROGRESS in your child `PROGRESS.md` before editing its deliverable. READY means assigned but unstarted; VERIFIED means that slice's source/document deliverable passed checks, never that gameplay passed. Record actual source/base/diff SHAs, commands with waited exits, findings, limitations and precise next action. Leave shared status/checkboxes to Codex. If usage is exposed, check periodically; below 10% in either available window, stop new work and commit the scoped checkpoint. If not exposed, record unavailable.

Before handback:

1. Check every source claim against its pinned revision and line, all 11 outcomes against the C matrix, all local links, UTF-8 and whitespace. Record counts/results; do not just say reviewed.
2. Run `git diff --name-only $auditBase` and confirm every changed/untracked deliverable is in the four-path allowlist. Inspect `git status --short` for accidental outputs; keep references, secrets, assets, saves and raw logs ignored. If baseline CRLF triggers whitespace diagnostics, use `git -c core.whitespace=cr-at-eol diff --check` and report that choice.
3. Stage the four explicit document paths and inspect `git diff --cached --name-only` / `git diff --cached --check` (same CRLF handling if necessary). Commit on `claude/bbsc002-reference-audit`. If interrupted, an honest partial checkpoint with pending slices is acceptable, not a claim all work is done.
4. Return audit base, full branch/commit SHA, changed paths, actual checks, ranked findings with claim/case IDs, unknowns and next action. Supply the commit via a user-provided audit-branch URL or a patch file; never push/merge into `seamless` or `windows`, force-push, or modify deployed services. The user/primary owner decides how to transfer the handback.

Codex integration gate: inspect the complete base-to-audit changed-path list for the same allowlist, verify citations and document checks, then integrate only the accepted documentation and mirror accepted findings into shared progress. Runtime fixes remain a separate R04 decision with R03 evidence. If Codex has advanced source after your frozen base, revalidate only affected findings against the current source; no automatic rebase/cherry-pick of unrelated changes.

No game/server/account activity, dependency installations, native tests, packaging or deployments belong to CL01. Custom managed admission/progress application stays OFF.

## Ready-to-paste prompt for Claude Code

> ทำ CL01 ตาม docs/handoff/CLAUDE-CODE-WINDOWS.md ใน clone ของคุณเองจาก origin/seamless บน branch claude/bbsc002-reference-audit อ่านเอกสารที่กำหนดและบันทึก base SHA ก่อนเริ่ม R02 ทำเสร็จแล้ว ให้อ้างผลเดิมและตรวจ source ด้วยตนเอง ไม่ apply patch/build/เปิดเกมซ้ำ ทำ A วิเคราะห์ join/progress/return ลง BBSC-002-MAP.md แล้ว B ตรวจเส้นทางบริการ self-hosted แยก ShadNet/game server, relay/P2P fallback และ identity ลง IDENTITY-PROTOCOL.md จากนั้น C ทำ acceptance cases ครบ product outcomes ทั้ง 11 ข้อลง ACCEPTANCE-CASES.md แก้ได้เฉพาะสามไฟล์นี้กับ docs/collaboration/claude/PROGRESS.md ทำเองไม่ใช้ subagents ไม่แตะ runtime/shared plan/config ไม่ติดต่อ server หรือใช้ save/credentials จริง อ้าง commit/path/symbol/line แยก source/native/gameplay และอย่าสรุปว่า PASS จากการอ่านโค้ด ตรวจ scope/links/UTF-8/whitespace แล้ว commit เฉพาะสี่ไฟล์บน branch audit ส่ง full base/commit SHA รายการไฟล์ ผลตรวจ findings และ blockers กลับมา ห้าม push/merge seamless หรือ windows; ถ้าต้องส่งผ่าน remote ให้ผู้ใช้กำหนดช่องทาง branch/patch ก่อน

## CL02-P01: progress contract follow-up

Status: READY; owner: the same external Claude Code session, inline in its separate clone. Dependency: accepted CL01 head `108bf28f069d7017712fd71e24fb7fd6b2bbde36`. Purpose: give Codex a source-backed, bounded correction contract for the demonstrated older-host-progress import; implementation remains Codex's R04-P01 decision.

Start a new branch `claude/p01-progress-contract` at that accepted head after checking the external clone is clean. Keep CL01's historical audit base and pins unchanged; record the accepted head as CL02's comparison base. Do not append CL02 commits to PR #1. Read current primary evidence at `6cff29d75c9f8dedf887bf6b52fefc8a02b9cc5d`: `docs/handoff/R03-ACCEPTANCE.md`, `docs/handoff/R04-JOIN-RELOAD.md` and the product outcomes. Fetch/read those public Git objects without rebasing or replacing the external working tree. Attribute the seven newly set progress entries to Codex's log evidence, not seven independently identified boss kills or a Claude reproduction. The post-placement crash cause and recovery remain unknown.

Only the existing four allowlisted documents may change. Add clearly labelled CL02 sections; preserve accepted CL01 findings, stable claim/case IDs and evidence dates:

1. `BBSC-002-MAP.md`: trace the existing `BbscProgressFlags`/`BbscProgressFlagsMore`, `TickBbscProgressBroadcast`, `OnBbscProgressPacket`, `TickBbscSharedProgress`, `MergeBbscSharedProgress` and the existing 19 boss-reward event rows. Produce a finite candidate table of existing flag/event/first-or-repeat reward mappings with immutable source/symbol/line citations. Separate verified event semantics from guesses; unclassified kind-1/NPC/time flags are not eligible merely because they changed. This is not a whole-game quest/item catalogue. Explain the smallest existing producer/consumer seam and what source cannot establish about required progression rewards.
2. `IDENTITY-PROTOCOL.md`: trace only progress-relevant session ownership and ordering: playable join, initial/late/missing snapshots, death/loading, departure, stale packets and rejoin. Explain why a first-seen baseline alone may miss or misclassify events if packets arrive late; distinguish source guarantees from runtime questions. Account for existing pending-progress/own-world file recovery and legacy unfiltered pending data at that seam, without designing a new storage/auth/protocol framework.
3. `ACCEPTANCE-CASES.md`: add a focused P01 matrix reusing G2 IDs: earlier host history excluded; kill before playable excluded; eligible joint kill retained across death/loading; after-departure event excluded; rejoin/retry without reward duplication; consumed reward not re-granted; existing and in-session conflicting NPC choices preserved; both save/reloads. Include affected legacy pending-data, crash/retry, wrong-character and backup/write-failure cases conditionally on the actual proposed persistence delta. State preconditions, production boundary, observations, required assertions, cleanup and blockers. All new execution statuses remain NOT RUN.
4. `PROGRESS.md`: mark CL02 and its active slice IN_PROGRESS before deliverable edits, record base/head/pins, actual commands and results, candidate changes, unknowns and next action. Source/document VERIFIED never means runtime PASS. Return the full branch/commit SHA, exact paths, checks and ranked P01 recommendations.

Acceptance: all new source claims checked against the pinned revision and line; all links/IDs/UTF-8/whitespace checked; full `git diff --name-only 108bf28f069d7017712fd71e24fb7fd6b2bbde36...HEAD` stays within the four paths. Deliver one focused follow-up commit/branch using the already supplied fork as the transfer channel. Do not merge/push to `seamless` or `windows`, force-push, edit runtime/shared plans/config, build/install toolchains, run game/server/account actions or use private saves/logs/credentials. No automatic subagents. Codex reviews this contract before implementation; do not claim the proposed baseline or filter is already implemented.

Ready-to-paste: ทำ CL02-P01 ตามหัวข้อนี้ใน clone เดิม สร้าง branch claude/p01-progress-contract จาก accepted head 108bf28 โดยคง audit base ของ CL01 อ่านหลักฐาน A01/J01 ที่ pin ไว้ แล้วจัดทำ progress/reward mapping, lifecycle/late-packet/recovery contract และ focused G2 acceptance matrix แก้ได้เฉพาะสี่เอกสารเดิม เพิ่มหัวข้อ CL02 ไม่เขียน runtime ไม่ build/เปิดเกม/ติดต่อ server ไม่ใช้ private logs/saves ทำเองไม่ใช้ subagents ตรวจ citations/IDs/links/UTF-8/whitespace/scope แล้วส่ง branch/full commit SHA และข้อเสนอ P01 กลับมาใน PR #1

## CL03-P02: earned-event and party-epoch source feasibility

Status: READY. Owner: the same external Claude Code session, inline in its separate clone. Dependency: integrated CL02 contract and the current B02/B03/B04 records. User authorizes assignment through a comment on merged PR #2. Codex retains runtime, build, diagnostic hooks, copied-profile/native/gameplay tests and integration.

### Freeze and read

Create `claude/p02-event-provenance` from exact seamless checkpoint `7a5eca3fcdc662afcce1de7b6d57510311b710b2` after checking the separate clone is clean. Preserve existing branches/history. Record that full comparison base in the child tracker; keep CL01/CL02 pins and their historical sections unchanged. Fetch/read this updated work package as a public Git object if its publication is newer than the frozen base; do not rebase/reset the external work to follow primary development.

Read the integrated CL02 sections, product outcomes 5/6/8/9, and B02 delivery, B03 backup/owner, C01 locked-map and B04 host-control handoffs **at the frozen base**. Inspect current tracked `gpu/patches/bbsc/0001-profile-storage-and-clang64.patch` and the relevant retained tests as source only. Compare with pinned BBSC B `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41` using immutable Git blobs. Cite the patch file/hunk at the frozen primary commit for current deltas; line numbers in the locally patched ignored reference tree are not pinned B citations.

Evidence boundaries: B02/B03 improve delivery/backup retry but do not establish earn-time admission or party provenance. B04's Hunt Bell search control never reached hosting state3 or a peer, so it does not establish the meaning/writer of group7 or guest-history contamination. Earlier member count and first host summary precede playable completion. SummonSuccess caller/register observations and BlockClear2 are leads, not proven eligibility/event identities. Attribute all native observations to Codex's dated handoffs; external source work does not reproduce them.

### Deliver in the same four documents

Append labelled CL03 sections. Preserve the accepted CL01/CL02 byte prefixes, IDs and evidence dates. New claim IDs start A-33 and B-29; extend case IDs from G2-20 only when an existing G2 case cannot express the distinction.

1. **`IDENTITY-PROTOCOL.md`: candidate signal matrix.** Trace the existing producers, callers and consumers for first playable completion, departure, same-party death/follow loading, genuine rejoin/host change, and boss clear. Start with `WriteLuaSessionEvent`, its existing matching/completion trace path, relay host-lock/member/session paths, `BbscBossClearHook`/BlockClear2, `BbscDreamTypeCheckHook`/`NoteBbscBossRewardEvent`, and existing progress packets. For each signal show exactly which character/member/host/attempt, event ID, map, ordering or time it actually carries; distinguish local observation time from host earn time. Show whether the native callee body is present in public source or only referenced by a name/offset/comment. Missing executable/assets/private traces become a precise missing-evidence row, never a guessed signature/offset or inferred member identity.
2. **`BBSC-002-MAP.md`: bounded feasibility decision.** Reuse the existing 19 reward-event rows and 57 listed flags; do not rescan the whole game or invent flag/event mappings. Determine whether existing public-source signals can distinguish the CL02 C1-C4 counterexamples while keeping eligibility through death/loading. Compare the smallest existing producer/consumer candidates and their failure cases. For any claimed viable path, give an end-to-end field/signal trace from earned event plus eligible member/epoch to the existing collector, with immutable citations. If source cannot establish it, explicitly conclude NOT IMPLEMENTATION-READY and identify the missing binding. B02 delivery confirmation/owner retry and B03 merge safety must remain distinct from admission. Do not design a replacement protocol, durable ledger, auth/storage framework or implement a filter.
3. **`ACCEPTANCE-CASES.md`: minimum discriminating native probes for Codex.** Reuse G2-03/04/15..19; add only missing distinctions. Each probe names an existing source boundary, observable fields, paired positive/negative input, required assertion, evidence level and blocker. Cover a kill before initial playable; the first eligible kill before any new summary; delayed/reordered older data; a new kill during same-party death/loading; post-departure kill; same-host rejoin/new host; original-owner deferred delivery. A valid probe must separate the competing explanations, not just reproduce the already-known first-seen-baseline failure. Suggest the smallest order of probes and stopping condition. All executions remain NOT RUN.
4. **`PROGRESS.md`: handback.** Mark CL03 and the active slice IN_PROGRESS before deliverable edits. Record frozen base, source pins, actual commands/results and limitations. End with a ranked conclusion: source-supported candidate or bounded impossibility, the exact next native observation Codex needs, and unresolved risks. VERIFIED means source/document deliverable only.

### Acceptance and transfer

Done when each candidate has pinned producer/caller/consumer evidence or a specific missing-evidence reason; every C1-C4 counterexample is explicitly tested against it on paper; the next native probes discriminate the unresolved bindings; and no source-only claim becomes native/gameplay PASS. A well-supported inability to prove a binding is a complete handback; repeating CL02's open questions without locating the missing producer/consumer is not.

Run citation line-range/source checks, all local links/anchors, defined IDs, UTF-8/LF/no BOM, `git diff --check`, and full `git diff --name-only 7a5eca3fcdc662afcce1de7b6d57510311b710b2...HEAD` against the same four-path allowlist. Verify all four accepted base documents are unchanged byte prefixes. Record actual counts and exited commands; do not reuse CL02 check counts as new results.

Commit only those four documents on the new branch and push to the already authorized `oat018/bloodborne_pc` fork, without force. Return full base/head SHA, branch URL, paths, fresh checks, ranked result and next native probe in a comment on PR #2. PR #2 stays merged/closed. Open a new PR into seamless for the CL03 handback; do not append commits to the merged PR #2 branch or merge/push seamless/windows. Codex reviews before integration.

This is source/document work only: no subagents, dependency installation/build, native hooks, game/assets/private saves/logs/credentials, account/service actions, packaging or deployments. Keep managed application/recovery gates OFF. Follow the ordinary usage checkpoint rule if usage is exposed; the primary user's PR-review waiver is not a new external runtime authorization.
