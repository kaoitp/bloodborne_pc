# Resume BBSC development on Windows

2026-10-26 reading guide: [current R03 acceptance matrix](R03-ACCEPTANCE-MATRIX.md) summarizes committed B09-B12 evidence, PR7/8 integration and remaining native checks. Older checkpoint limitations below are historical where later evidence supersedes them; use the matrix before repeating a test.

Active ownership update2026-10-25: [Claude now takes over all R03 implementation and validation](R03-CLAUDE-TAKEOVER.md). The owner retains the product goals/general approach and gives Claude independent choice of methods. Earlier audit-only/four-file/Codex-only process wording below is historical for this takeover; Codex quota does not apply to Claude.

Latest B06: [stale snapshot receiver fix and native regression](R03-B06-WORLD-ORDERING.md). Actual-function RED/GREEN and candidate guest native join/0.85m placement/normal return pass; immediate1250 groups exact. Same-process reload has six unclassified group12705 bits, so full reload integrity stays open. Actual joint earning/C3 callbacks/C4 remain unproved; both copied tests normally closed, managed applicationOFF.

Latest B05: [older-host reward negative and native limits](R03-B05-EVENT-PROBES.md). Actual Amelia-old-host no-fight visit has zero reward/clear logs beyond60s; normal guest return preserves1250 groups exactly. Positive earning/C1-C4 remain open. Same-process host character-change probe hit repeated GPU PM4 errors; fresh copied positive setup is IN_PROGRESS, shared progressOFF. Quota has reset; monitor fresh usage rather than the historical B04 stop.

Latest B04: [host-only search control and source leads](R03-B04-HOST-CONTROL.md). Hunt Bell alone changes three transient bits while group7 stays exact; no peer/state3, so its writer/meaning remains unresolved. No runtime change. Actual earned-event/admission/epoch provenance remains the main G2 blocker. Games normally closed, copied baseline restored, originals3171 unchanged; quota stop at9%/86% remaining; no new work until usage permits.

Latest C01: [fresh-character locked-map native case](R03-C01-LOCKED-MAP.md). New copied Clinic character joins Cathedral beside host, returns to exact journaled origin and reloads with all1250 groups unchanged. Required self-hosted flow observed; three public playlog403 failures do not stop it. Host flag differences remain unclassified after a clean solo control; G2 and remaining acceptance stay open. All tests normally closed, originals unchanged.

Latest B03: [progress backup/owner retry checkpoint](R03-B03-PROGRESS-BACKUP.md). Actual-function backup/owner RED/GREEN passes. Native backup-failure retention and original-owner positive retry pass with an already-owned synthetic flag; native in-memory wrong-character guard remains unproven after timeout. Original 3171 files unchanged; copied tests normally closed/restored. G2 history/eligibility and remaining R03 gates stay open.

Latest B02: [boss reward delivery checkpoint](R03-B02-REWARD-DELIVERY.md). Owner-bound retry, confirmed direct-goods delivery, duplicate queue protection and frozen lot selection pass the actual-function fixture. Frozen same-DLL native Dream join/return preserves all 1250 groups; reward earning/failure-retry gameplay remains untested. G2 admission/history and remaining R03 gates stay open; experimental recovery remains OFF by default.

Latest B01: [personal common-event preservation checkpoint](R03-B01-PERSONAL-FLAGS.md). The demonstrated 29 completion-bit leak is corrected: actual Dream join/normal return/save-reload preserved all 1250 prejoin flag groups. Original 3171 files unchanged; both test clients normally closed. G2 earned-event/reward and remaining candidate/routing/recovery gates keep R03 IN_PROGRESS; experimental recovery remains OFF by default.

Latest A04: [native admission cancellation checkpoint](R03-A04-ADMISSION.md). The bounded initial journal-write fault now cancels without own-state mutation, then healthy retry/adjacent placement/normal return/save-reload pass on the experimental guest build. The earlier native wait was rejected. G2/group-9/rewards and remaining candidate/routing/recovery gates keep R03 IN_PROGRESS; recovery/admission remains OFF by default.

Latest A03: [ownership, own-state and lamp checkpoint](R03-A03-OWN-STATE.md). Bounded native return/interruption/ownership cases improved; initial journal-write refusal and G2/group-9/reward integrity still block R03. The Lua refusal candidate FAILED and was fully reverted. Experimental durable-origin recovery remains OFF unless explicitly opted in on copied profiles. Use A03 source/artifact attribution rather than the historical artifact table below. R03 remains IN_PROGRESS.

Historical A02: [native crash/profile/origin recovery checkpoint](R03-A02-RECOVERY.md). C01 null-table regression and copied native join passed; per-profile journal and original-point/invalid-point-lamp recovery now have bounded native evidence. G2 older-host import remains unchanged; full world/save integrity, host loss and remaining candidate/routing cases keep R03 IN_PROGRESS. Use the final local V5 DLL recipe and exact artifact hashes in that record; do not reuse older official artifact hashes as the tested A02 composition.

Latest A01 quota checkpoint: [four remaining acceptance groups](R03-ACCEPTANCE.md). User accepts representative maps. Wrong-word control behaved correctly, but progress inherits older host flags and a later guest crashed after placement. Recovery and full service independence remain unverified. Stop threshold reached at 9%/70%; resume from preserved crashed copies and the DLL progress/toolchain boundary, not an all-map sweep.

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
