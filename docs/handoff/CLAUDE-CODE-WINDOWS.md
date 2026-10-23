# Claude Code work package: CL01

Updated: 2026-10-23 (Asia/Bangkok). Status: READY FOR EXTERNAL START; no audit has been performed by preparing this package. Parent: R03/R04 in the [active plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md).

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
