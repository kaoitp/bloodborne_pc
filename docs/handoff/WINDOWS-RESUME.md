# Resume BBSC development in the new fork

Updated: 2026-10-23 (Asia/Bangkok).

## Repository and starting point

- Repository: `https://github.com/kaoitp/bloodborne_pc.git`.
- Development and checkpoint branch: `seamless`.
- Branch created directly from BBport `windows-v1.7.2`, commit `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d`.
- The existing `windows` branch is left unchanged. Its 1.9.4 source is not the development baseline.
- This migration transfers plans and prepares the branch only. Development starts fresh here: no old runtime patches, worktrees, build outputs, private profiles, logs or test PASS results are imported.

Read in order:

1. [Active alignment and implementation plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md).
2. [Progress and precise next action](../WINDOWS-PROGRESS.md).
3. [Approved product outcomes](../superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md).

[Windows direction](../superpowers/plans/2026-10-21-bbsc-windows-only-migration.md) records platform limits; [execution reference](../superpowers/plans/2026-10-21-bbsc-windows-execution.md) records evidence/gate rules. External collaborators read [the Claude work package](CLAUDE-CODE-WINDOWS.md).

## First development task

R02 is READY after this documentation checkpoint: obtain the exact BBSC 0.0.2 reference, inspect and verify its BBport 1.7.2 patch, then assemble the complete baseline with its existing gameplay DLL and loader. All patch/build/load/gameplay checks must be recorded against this repository's source and artifacts. Do not assume the transport patch alone supplies the gameplay mod.

This turn stops after branch and plan publication as requested. Do not resume source implementation, build or game testing as part of the documentation migration.

## Working rules

Stay within supported story-map/Hunter's Dream join, jointly earned boss/story progress and self-hosted services. Use the existing release behavior first. Preserve all other game systems; Chalice is unsupported.

Use copied profiles for later authorized diagnostics. Two-client testing needs distinct accounts/profiles/ports. The user's deployed server source/version is unknown; do not repeat that question or invent a mapping. Use existing compatible services/configuration first; no live-server redeployment.

Codex owns runtime/build/shared plans and works without subagents. Claude's separate audit is limited to four documents. Check usage periodically and stop new work below 10% remaining. Keep custom admission/application OFF until the relevant native gates pass; no packaging. Secrets, saves, game assets and raw logs remain private and ignored.

## New-session prompt

> Read AGENTS.md, this handoff, the active alignment plan and WINDOWS-PROGRESS.md. Work in seamless from the pinned BBport 1.7.2 base. Resume the first incomplete R task only when development is requested. Reproduce the complete BBSC 0.0.2 baseline, then fix only demonstrated gaps in the three goals. Use current-repository evidence, copied profiles and existing loaders/services. Work inline, check usage and checkpoint to origin/seamless. Do not import the old implementation or claim its tests passed here.
