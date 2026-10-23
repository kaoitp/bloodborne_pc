# Windows execution and evidence reference

Updated: 2026-10-23. Execute the [active R01-R04 plan](2026-10-23-bbport172-bbsc002-alignment.md), following the [product outcomes](../specs/2026-10-18-bbsc-anywhere-coop-design.md) and [tracker](../../WINDOWS-PROGRESS.md).

Order: complete pinned source/mod composition (R02), reproduce baseline on self-hosted services (R03), then fix only demonstrated goal gaps (R04). Old W task IDs are historical labels, not current assignments. No old module/test migration is scheduled by default.

Before changes, identify the task, dependencies, acceptance checks and relevant source callers/configuration. Mark the task IN_PROGRESS. At meaningful checkpoints and before commit/end, synchronize tracker/checkboxes and record source/artifact SHA, dirty state, actual commands/waited exits, test counts/skips, private evidence location, review findings, limitations and next action.

Use READY, IN_PROGRESS, WAIT_DEP, WAIT_GAME, VERIFIED or BLOCKED for task status; PASS, SKIP, NOT RUN or BUILD_FAIL for checks. Verification is specific to its source and evidence type. Behavioral changes invalidate affected gameplay acceptance until retested.

| Gate | Required result |
|---|---|
| G1 join | Correct selected peer/password, supported cross-map/Dream placement; relevant stale/failed joins do not mutate the guest world. |
| G2 progress | Only eligible jointly earned boss/story progress persists, preserving own progress/choices and preventing duplicate relevant rewards after save/reload. |
| G3 return | Safe normal exit/disconnect and interrupted-session reload; affected wrong-character/write-failure/retry cases when persistence changes. |

Run checks appropriate to the actual change. Documentation migration needs Markdown links, UTF-8/content, whitespace and unchanged-runtime checks; no build/game launch. Source changes need focused tests and relevant native/gameplay gates. Preserve baseline safety mechanisms and test them rather than replacing them speculatively.

Check usage periodically. If either available window has less than 10% remaining, stop new work, record a precise checkpoint and commit it. No subagents. Questions that block a dependent step may be collected for the end while independent authorized work continues.
