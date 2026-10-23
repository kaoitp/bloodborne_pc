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

## Start a new Codex session

Open this repository as the session's project. On this machine the checkout is `C:/Projects/bloodborne_pc`. Root `AGENTS.md` routes future sessions here automatically; no old conversation or worktree is required.

For a different machine or a fresh directory:

```powershell
git clone --single-branch --branch seamless https://github.com/kaoitp/bloodborne_pc.git bloodborne-seamless
cd bloodborne-seamless
```

Before editing, inspect the actual checkout with native Git for Windows (on this machine, `C:/Program Files/Git/cmd/git.exe`):

```powershell
git remote -v
git status --short --branch
git branch --show-current
git log -3 --oneline
git merge-base --is-ancestor e5d04e2ba4864ccf40de6c3cf6aa532855320b0d HEAD
```

Expected: origin is this fork, branch is `seamless`, and the ancestry command exits 0. Read the current tracker rather than requiring HEAD to equal an old documentation SHA. If the wrong branch is selected, preserve local changes and switch only when safe; do not reset or overwrite work to satisfy this checklist. Fetch/pull only when needed and after inspecting local work.

## Evidence at handoff

F01 branch/plan preparation is complete; documentation checkpoint `b42c83af0bcc8b2adab29c0ae3bed546ce33b704` was published before this handoff update. Later documentation commits are expected. See the tracker for F02 verification/publication.

| Area | Evidence in this repository |
|---|---|
| Branch and plan | Exact 1.7.2 ancestry and migrated scope/ownership documents verified. |
| BBSC patch/source | NOT RUN: not obtained, applied or committed here. |
| Gameplay DLL/load configuration | NOT RUN: not assembled or loaded here. |
| Native build/tests | NOT RUN here; no old PASS transferred. |
| Self-hosted multiplayer/progress/return | NOT RUN; G1/G2/G3 remain open. |

## First development task

R02 is READY after this documentation checkpoint: obtain the exact BBSC 0.0.2 reference, inspect and verify its BBport 1.7.2 patch, then assemble the complete baseline with its existing gameplay DLL and loader. All patch/build/load/gameplay checks must be recorded against this repository's source and artifacts. Do not assume the transport patch alone supplies the gameplay mod.

When the user starts development with the prompt below:

1. Read the linked plan/spec/tracker, inspect source and tool availability, then mark R02 IN_PROGRESS before edits. Work directly in the new repository's `seamless` branch; old worktrees are irrelevant.
2. Obtain BBSC at exact commit `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41` in an ignored reference location. Verify its Git commit and the patch SHA256 against the plan, inspect the patch and all destinations, then run `git apply --check` before applying it. Stop on a mismatch and record evidence.
3. Apply only the reviewed baseline patch and record the current source/diff/dependency pins. Identify the complete matching mod DLL, existing loader, required data/notices and configuration from pinned sources. Do not replace source-build outputs with packaged executables or create a new loader.
4. Follow the exact baseline's build instructions and use only needed pinned dependencies. Build-only work may proceed after source/patch checks; actual game/load tests require complete verified composition and a fresh copied-profile setup.
5. Record actual checks at each checkpoint, synchronize checkboxes and commit/push to origin/seamless. R03 handles baseline reproduction; R04 starts only from demonstrated goal gaps. R02 does not need to wait for the external Claude audit.

The preparation sessions were documentation-only. Starting development in a new session is a separate next action; no implementation, build or game launch was performed for this handoff.

## Inputs for later testing

Inspect available tools before installing anything; this new checkout has no verified build environment yet. Use the pinned source's Windows/MSYS2 instructions rather than a moving upstream recipe.

Real game/load testing needs the user's own compatible CUSA03173 1.09 dump, newly configured private test settings and an explicit copied-save/profile location. These inputs, passwords/tokens and server addresses are not in Git and are not restored by cloning. Check their availability privately when needed; missing gameplay setup does not block source inspection/patch verification.

Two-client gameplay eventually needs distinct test accounts/profiles/ports; a single client can perform setup/load smoke. Do not manufacture a second identity by duplicating the same login or create accounts implicitly. Existing user permission allows copied-profile game diagnostics once setup is ready; preserve any active user session and original saves.

## Working rules

Stay within supported story-map/Hunter's Dream join, jointly earned boss/story progress and self-hosted services. Use the existing release behavior first. Preserve all other game systems; Chalice is unsupported.

Use copied profiles for later authorized diagnostics. Two-client testing needs distinct accounts/profiles/ports. The user's deployed server source/version is unknown; do not repeat that question or invent a mapping. Use existing compatible services/configuration first; no live-server redeployment.

Codex owns runtime/build/shared plans and works without subagents. Claude's separate audit is limited to four documents. Check usage periodically and stop new work below 10% remaining. Keep custom admission/application OFF until the relevant native gates pass; no packaging. Secrets, saves, game assets and raw logs remain private and ignored.

## New-session prompt

Paste this to start development, rather than another plan-only session:

> เริ่มพัฒนาตามแผนใน repo นี้บน branch seamless อ่าน AGENTS.md, docs/handoff/WINDOWS-RESUME.md, แผนที่ลิงก์ไว้ และ docs/WINDOWS-PROGRESS.md ก่อน จากนั้นเริ่ม R02 โดยตรวจ BBSC 0.0.2 ที่ commit ตรึงไว้และ patch สำหรับ BBport 1.7.2 แล้วประกอบ baseline ด้วย DLL/loader เดิม ทำงานเองตามลำดับ ไม่ใช้ subagents ไม่ใช้ worktree หรือผลทดสอบจาก repo เก่า รักษาขอบเขตสามเป้าหมายและระบบอื่นตามเดิม ตรวจ usage เป็นระยะ ถ้าเหลือต่ำกว่า 10% ในหน้าต่างใดให้หยุดงานใหม่ บันทึกและ commit checkpoint อัปเดต tracker/checkboxes ตามหลักฐานจริงและ push ไป origin/seamless จุดที่ต้องถามให้ข้ามงานที่ขึ้นอยู่กับคำตอบไปก่อนแล้วสรุปคำถามท้ายรอบ โดยทำงานอิสระส่วนอื่นต่อได้ ไม่ทำ packaging หรือ redeploy server และใช้เฉพาะโปรไฟล์สำเนาเมื่อต้องทดสอบเกม
