# Claude Code work package: CL01

Updated: 2026-10-23. Parent: R01/R04 in the [active plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md). Read [the Windows handoff](WINDOWS-RESUME.md) and [product outcomes](../superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md).

## Start in a separate clone

```powershell
git clone --single-branch --branch seamless https://github.com/kaoitp/bloodborne_pc.git bloodborne-cl01
cd bloodborne-cl01
git switch -c claude/bbsc002-reference-audit
```

Use independent read-only reference checkouts of BBport `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d` and CLSAMG22/BBSC `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`. Record source SHAs; moving HEAD or release notes alone are not implementation proof. No local Codex worktree, private credentials/saves, dependency installation, native build or game launch is needed for this source audit.

## Ownership

Codex owns runtime/tests/CMake/build/runner/configuration and shared plans/progress. The external human collaborator may create/edit exactly:

- `docs/collaboration/claude/PROGRESS.md`
- `docs/collaboration/claude/BBSC-002-MAP.md`
- `docs/collaboration/claude/IDENTITY-PROTOCOL.md`
- `docs/collaboration/claude/ACCEPTANCE-CASES.md`

Mark CL01 IN_PROGRESS only in its child PROGRESS.md. Shared entry points/tracker/plans are read-only for this task. Codex mirrors accepted findings into shared progress. This is external collaboration, not authorization to spawn subagents.

## Deliverables in order

**CL01-A, BBSC-002-MAP.md:** Identify the complete pinned client/mod DLL, existing loader/configuration, required data/notices and source/artifact recipe. Explain the patch's no-op gameplay callbacks and external DLL ownership. Then map the three goals to pinned commit/path/symbol/line, existing behavior, EXISTING/PASS vs PRESENT-NOT-TESTED vs REPRODUCED-GAP vs UNSUPPORTED, smallest delta if justified, responsible caller and focused acceptance case. Source presence is not runtime PASS.

**CL01-B, IDENTITY-PROTOCOL.md:** Map the existing self-hosted game API/account/Matching2/summon/relay route and client settings required for the goals. Identify required public dependencies, available/reference-only/binary-only server components and missing evidence. Trace selected user/character/session/peer and stale attempts only where a candidate changed join/progress boundary needs it. Preserve authentication/validation; never guess identity from equal numbers/endpoints. The user's deployed source/version is already unknown; do not ask again or contact private services. No new HMAC/account/backend design or public/cross-emulator compatibility project.

**CL01-C, ACCEPTANCE-CASES.md:** For G1/G2/G3, specify case ID, setup/input, actual production boundary, expected allowed/rejected behavior, no-side-effect assertions, cleanup/retry, evidence type and blocker. Cover supported cross-map/Dream/password join, eligible earned progress, own-progress preservation/no duplicate rewards/save-reload, required self-hosted routing, normal exit/disconnect and interrupted-session reload. Add affected wrong-character/write-failure/retry cases if a proposed delta changes persistence. Keep fixture/native/gameplay evidence distinct; invent no API, offset or PASS result.

Preserve all other baseline game systems and unsupported Chalice status. Reuse the release first; old implementation mechanisms are optional references, not a checklist. Proposed source changes stay findings in the owned documents.

## Handback

Review source claims/scope, validate local Markdown links, UTF-8 and whitespace, then commit only the allowlisted documents on your audit branch. Return branch/base/commit, changed paths, actual checks, findings, missing evidence and next action. Do not merge or push into `seamless`/`windows`; the primary owner integrates the audit. A need to change another file is a finding to hand back, not permission to expand ownership.

No runtime changes, game/server/account activity, deployment, packaging, secrets/raw logs in Git or history rewriting. If usage is available and either remaining window is below 10%, stop new work and commit a documented checkpoint.

## Ready-to-paste prompt

> Perform CL01 under this work package in your own clone/branch from seamless. Audit complete BBport 1.7.2 + BBSC 0.0.2 composition and reuse for only supported-map join, jointly earned progress and self-hosted services. Modify only the four allowlisted documents, keep progress in the child tracker, cite pinned source and distinguish source presence from tested behavior. Return a local audit commit and findings; leave runtime/shared plans unchanged.
