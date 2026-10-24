# Resume BBSC development on Windows

Updated: 2026-10-24 (Asia/Bangkok). Next task: **remaining R03 G1/G2/G3 acceptance**. Same-map and Cathedral Ward -> Hunter's Dream joins now have actual native evidence. [R04-J01](R04-JOIN-RELOAD.md) disables a demonstrated extra cross-map reload through the existing launch flag; adjacent blue guest placement and normal return to Cathedral Ward passed. The earlier pre-claim deactivation cause remains unconfirmed. R03 is still IN_PROGRESS; do not repeat R02 or claim all-map/progress/recovery acceptance.

## Read before work

1. [Active plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md).
2. [Current progress and next action](../WINDOWS-PROGRESS.md).
3. [R03 session instructions](R03-RESUME.md).
4. [R02 source/artifact/native evidence](BBSC-BASELINE.md).
5. [Product outcomes](../superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md) and [execution/evidence rules](../superpowers/plans/2026-10-21-bbsc-windows-execution.md).

External Claude uses [its separate work package](CLAUDE-CODE-WINDOWS.md) and owns its four audit documents. Codex owns runtime/build/configuration/native/gameplay and shared plans, and works inline without subagents. R03 independent work does not wait for the audit; inspect actual delivered findings when available.

## Checkout and history

Repository: `https://github.com/kaoitp/bloodborne_pc.git`. Primary checkout on this machine: `C:/Projects/bloodborne_pc`, branch `seamless`. The app-created worktree at `C:/Users/numbe/.codex/worktrees/9236/bloodborne_pc` was detached at an older documentation commit. Open the primary checkout for the new session; do not edit the detached copy expecting current R02/R03 state.

Use native Git (`C:/Program Files/Git/cmd/git.exe` on this machine):

```powershell
git remote -v
git status --short --branch
git branch --show-current
git worktree list
git log -3 --oneline
git merge-base --is-ancestor f3734da56722f21dd2c25dcca89b85d1c93f2109 HEAD
```

Expected: this fork, `seamless`, R02 source checkpoint is an ancestor (exit 0). Later documentation commits are expected; use the tracker, not equality to an old HEAD. Preserve local changes and inspect before any fetch/pull/switch. If launched in a detached worktree, locate the existing primary `seamless` checkout; do not force the branch into a second worktree or reset either checkout.

Baseline ancestry remains BBport `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d`. R02 source/evidence checkpoint is `f3734da56722f21dd2c25dcca89b85d1c93f2109`; publication record `4866002514de55c60e6f5e5475d797eed4131f1d`. Claude handoff was published at `afeffc3d2acdbbf32d7cf7f759038b5ab2178a08` with record `04c6e7b4b9a042c872e6ed815dacce6c7a7a0d8e`. `windows` remains unchanged at `3fabfa7a7af67a34a6dfc630b6ec2539b68fad4d`.

For another machine:

```powershell
git clone --single-branch --branch seamless https://github.com/kaoitp/bloodborne_pc.git bloodborne-seamless
cd bloodborne-seamless
```

Cloning restores source/documents, not ignored binaries, profiles, credentials or private input metadata. Reconstruct only missing prerequisites from the R02 recipe; the source patch is already committed and must not be applied again.

## Evidence boundary

| Area | State |
|---|---|
| Pinned BBSC 0.0.2 patch | Verified/applied, 15 destinations; no custom runtime delta |
| DLL/original loader/notices | Official release composition verified; local MSVC DLL rebuild NOT RUN |
| Source build | CLANG64 build exit 0, fresh artifacts hashed; Linux-only tests skipped |
| Copied-profile native startup | Correct DLL, image validation, 52 patch writes, 159/159 hooks and 3 HTTP redirects observed |
| Original saves/profile | All 3,171 original file hashes/path set unchanged after R02 diagnostics |
| Two-client routing/join/progress/return | R02 did not test multiplayer; later same-map/Dream join and normal return verified in [R04-J01](R04-JOIN-RELOAD.md). Full G1/G2/G3 open |

The two tracked FSR-Vulkan patches applied by `build.sh` leave its submodule working tree dirty. This is recorded build state, not permission to discard or commit a Gitlink change. Verify before reuse. R02 artifacts were rehashed on 2026-10-24 and still match [the record](BBSC-BASELINE.md).

Local private inputs are at `.superpowers/r03-resume.json` in the primary checkout. Read that ignored file for already-supplied game/profile paths and separate service addresses; do not copy its contents into Git. See [R03 instructions](R03-RESUME.md) for supplied private account/profile configuration, the concurrent-client resource limitation and current-state checks. Service observations are dated: the DLL TCP service connected during the 2026-10-24 J01 session. Recheck before reuse; this does not authorize server redeployment or prove every required route is self-hosted.

## New-session prompt

Open `C:/Projects/bloodborne_pc` as the project, then paste:

> เริ่ม R03 ตามแผนบน branch seamless อ่าน AGENTS.md, docs/handoff/WINDOWS-RESUME.md, docs/handoff/R03-RESUME.md, docs/handoff/BBSC-BASELINE.md, แผนและ docs/WINDOWS-PROGRESS.md ก่อน ตรวจ checkout/source/artifact hashes และอ่าน .superpowers/r03-resume.json ที่ ignored สำหรับพาธเกม/โปรไฟล์และ IP เดิม ไม่ทำ R02 ซ้ำเมื่อยังตรงหลักฐาน เริ่มด้วย preflight และตรวจเส้นทาง self-hosted แยก ShadNet/game server รวม relay/P2P fallback ตรวจว่ามีบัญชีเดิมสองบัญชีที่ต่างกันและโปรไฟล์สำเนาแยกก่อน multiplayer ถ้ายังขาดให้ถามเฉพาะข้อมูลที่ขาดโดยไม่ขอรหัสผ่านในแชต และทำงานอิสระต่อ ทดสอบ G1 join/placement, G2 jointly earned progress/rewards/save-reload, G3 exit/disconnect/interrupted return ตามลำดับและบันทึกผลจริง ทำเองไม่ใช้ subagents ไม่แตะสี่เอกสารของ Claude ระหว่าง audit ไม่สร้างหรือทำซ้ำบัญชี ไม่แก้/เปิดบริการหรือ firewall บน server ไม่ packaging/redeploy และไม่เปิด custom managed admission/application ตรวจ usage เป็นระยะ ถ้าหน้าต่างใดเหลือต่ำกว่า 10% ให้หยุดงานใหม่ บันทึกและ commit checkpoint อัปเดต tracker/checkboxes แล้ว push origin/seamless โดยไม่ force
