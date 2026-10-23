# CL01 progress

Status: READY. Parent: R03/R04. Owner: the user's external friend using Claude Code.

Read [the work package](../../handoff/CLAUDE-CODE-WINDOWS.md). This tracker is prepared for assignment; no external audit has started or delivered findings. R02 evidence exists in [the primary record](../../handoff/BBSC-BASELINE.md); it does not count as a test executed by Claude. G1/G2/G3 remain open.

This file is the owned tracker: `docs/collaboration/claude/PROGRESS.md`.

## Inputs to record at external start

- Audit base SHA: NOT STARTED (record full HEAD after clone, before branching).
- Audit branch: `claude/bbsc002-reference-audit` in a separate clone.
- BBport base: `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d`.
- BBSC source: `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`; verification NOT RUN by Claude.
- Canonical patch SHA256: `e34c79b388605998b430ec4eed556fc2cb8c8928f1d3e9f26bf5d2df29732aa3`; verification NOT RUN by Claude.
- Required R02 source ancestor: `f3734da56722f21dd2c25dcca89b85d1c93f2109`.
- Usage availability/remaining windows: NOT CHECKED by Claude.

## Work sequence

| Slice | Status | Dependencies | Owned output / completion |
|---|---|---|---|
| CL01-A | READY | Frozen base and verified reference | `BBSC-002-MAP.md`: complete composition ownership summary; join/progress/return source rows with citations and candidate gaps separated from reproduction |
| CL01-B | READY | Same pins; independent of A | `IDENTITY-PROTOCOL.md`: all required service routes, split-host/relay fallback settings and relevant identity validation, with source/evidence/unknowns |
| CL01-C | WAIT_DEP | A/B for final citations | `ACCEPTANCE-CASES.md`: actionable G1/G2/G3/service cases and all-11-outcome coverage matrix, execution status NOT RUN |
| CL01 handback | WAIT_DEP | A/B/C and document checks | Four-path-only commit; full base/branch/commit, checks, findings, limitations and next action |

A/B may be investigated alongside Codex R03; the external single Claude session can do A then B. C may draft case IDs early but remains WAIT_DEP until A/B citations are ready. Codex owns implementation and test execution. Preparing this tracker does not mark any audit slice IN_PROGRESS or VERIFIED.

## Checkpoint format

For each external checkpoint record:

- Slice/status, full audit base and pinned reference SHAs; current commit and dirty/staged paths.
- Changed deliverable paths (only the four allowed by the work package).
- Actual source/coverage/link/UTF-8/whitespace/scope commands, waited exits and counts; native/gameplay NOT RUN.
- Ranked findings by A/B claim ID and C case ID; candidate source mismatch versus actual reproduced gap; missing evidence.
- Usage or unavailable, limitations, next action, handback branch/full commit/transfer method when ready.

Keep private addresses, credentials, saves, game assets and raw logs out of these files. Source findings need immutable commit/path/symbol/line citations. VERIFIED for an audit slice means its source/document deliverable passed checks; gameplay gates are updated only by Codex from actual evidence. Shared plans/entry points are read-only for Claude.

Checks by Claude: NOT RUN. Findings delivered by Claude: none. Next: clone the published seamless handoff, freeze audit base, verify reference pins, then mark CL01/CL01-A IN_PROGRESS here.
